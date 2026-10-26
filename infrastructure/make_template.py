"""Generate the CloudFormation template for private static hosting and public DNS."""
import json
from pathlib import Path
DOMAINS=['calopihaven.com','redhawk2240.com','silvermill8294.com']
ref=lambda x:{'Ref':x}
att=lambda x,y:{'Fn::GetAtt':[x,y]}
sub=lambda x:{'Fn::Sub':x}
resources={
 'SitesBucket':{'Type':'AWS::S3::Bucket','DeletionPolicy':'Retain','UpdateReplacePolicy':'Retain','Properties':{'BucketName':sub('ticosync-calopihaven-sites-${AWS::AccountId}'),'PublicAccessBlockConfiguration':{'BlockPublicAcls':True,'IgnorePublicAcls':True,'BlockPublicPolicy':True,'RestrictPublicBuckets':True},'OwnershipControls':{'Rules':[{'ObjectOwnership':'BucketOwnerEnforced'}]},'BucketEncryption':{'ServerSideEncryptionConfiguration':[{'ServerSideEncryptionByDefault':{'SSEAlgorithm':'AES256'}}]},'VersioningConfiguration':{'Status':'Enabled'},'Tags':[{'Key':'Application','Value':'calopihaven'}]}},
 'OriginAccess':{'Type':'AWS::CloudFront::OriginAccessControl','Properties':{'OriginAccessControlConfig':{'Name':sub('${AWS::StackName}-s3'),'OriginAccessControlOriginType':'s3','SigningBehavior':'always','SigningProtocol':'sigv4'}}},
 'SecurityHeaders':{'Type':'AWS::CloudFront::ResponseHeadersPolicy','Properties':{'ResponseHeadersPolicyConfig':{'Name':sub('${AWS::StackName}-headers'),'SecurityHeadersConfig':{'ContentTypeOptions':{'Override':True},'FrameOptions':{'FrameOption':'DENY','Override':True},'ReferrerPolicy':{'ReferrerPolicy':'strict-origin-when-cross-origin','Override':True},'StrictTransportSecurity':{'AccessControlMaxAgeSec':31536000,'IncludeSubdomains':False,'Preload':False,'Override':True}}}}}
}
outputs={'Bucket':{'Value':ref('SitesBucket')}}
arns=[]
for i,domain in enumerate(DOMAINS):
 name=['Calopi','RedHawk','Silvermill'][i]
 resources[name+'Zone']={'Type':'AWS::Route53::HostedZone','DeletionPolicy':'Retain','UpdateReplacePolicy':'Retain','Properties':{'Name':domain,'HostedZoneConfig':{'Comment':'Calopi Haven public DNS; existing email and guest guides preserved before delegation'},'HostedZoneTags':[{'Key':'Application','Value':'calopihaven'}]}}
 resources[name+'Redirect']={'Type':'AWS::CloudFront::Function','Properties':{'Name':sub('${AWS::StackName}-'+name.lower()+'-www'),'AutoPublish':True,'FunctionConfig':{'Comment':'Redirect www to the canonical apex; preserve query strings','Runtime':'cloudfront-js-2.0'},'FunctionCode':'''function handler(event) { var r=event.request; if(r.headers.host.value==='www.DOMAIN'){var q=[];for(var k in r.querystring){var p=r.querystring[k];(p.multiValue||[p]).forEach(function(v){q.push(encodeURIComponent(k)+'='+encodeURIComponent(v.value));});}return {statusCode:301,statusDescription:'Moved Permanently',headers:{location:{value:'https://DOMAIN'+r.uri+(q.length?'?'+q.join('&'):'')}}};}return r;}'''.replace('DOMAIN',domain)}}
 # Preserve the existing guest-guide destination independently of Squarespace.
 guides={'redhawk2240.com':'https://www.canva.com/design/DAERjZ0Ev_I/bEX8H5mgrrcJFfqGkm_j7w/view','silvermill8294.com':'https://www.canva.com/design/DAGY2AeTcdk/S1pbqUKvIRAhRwRREwAWig/view?utm_content=DAGY2AeTcdk&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=hb09b2cb887'}
 if domain in guides:
  code=resources[name+'Redirect']['Properties']['FunctionCode']
  code=code.replace('var r=event.request;',"var r=event.request;if(r.headers.host.value==='checkin."+domain+"'){return {statusCode:302,statusDescription:'Found',headers:{location:{value:"+json.dumps(guides[domain])+"}}};}")
  # Red Hawk can serve www during the DNSSEC delegation transition without a loop.
  if name=='RedHawk':code=code.replace("if(r.headers.host.value==='www.redhawk2240.com')","if(false)")
  resources[name+'Redirect']['Properties']['FunctionCode']=code
 resources[name+'CDN']={'Type':'AWS::CloudFront::Distribution','Properties':{'DistributionConfig':{'Enabled':True,'Comment':'Calopi Haven: '+domain,'DefaultRootObject':'index.html','HttpVersion':'http2and3','IPV6Enabled':True,'PriceClass':'PriceClass_100','Aliases':{'Fn::If':['CustomDomains',[domain,'www.'+domain],ref('AWS::NoValue')]},'ViewerCertificate':{'Fn::If':['CustomDomains',{'AcmCertificateArn':ref('CertificateArn'),'SslSupportMethod':'sni-only','MinimumProtocolVersion':'TLSv1.2_2021'},{'CloudFrontDefaultCertificate':True}]},'Origins':[{'Id':'PrivateS3','DomainName':att('SitesBucket','RegionalDomainName'),'OriginPath':'/'+domain,'OriginAccessControlId':ref('OriginAccess'),'S3OriginConfig':{'OriginAccessIdentity':''}}],'DefaultCacheBehavior':{'TargetOriginId':'PrivateS3','ViewerProtocolPolicy':'redirect-to-https','AllowedMethods':['GET','HEAD'],'CachedMethods':['GET','HEAD'],'Compress':True,'CachePolicyId':'658327ea-f89d-4fab-a63d-7e88639e58f6','ResponseHeadersPolicyId':ref('SecurityHeaders'),'FunctionAssociations':[{'EventType':'viewer-request','FunctionARN':att(name+'Redirect','FunctionARN')}]}}}}
 outputs[name+'DistributionId']={'Value':ref(name+'CDN')};outputs[name+'CloudFrontDomain']={'Value':att(name+'CDN','DomainName')};outputs[name+'ZoneId']={'Value':ref(name+'Zone')};outputs[name+'Nameservers']={'Value':{'Fn::Join':[', ',att(name+'Zone','NameServers')]}}
 arns.append(sub('arn:${AWS::Partition}:cloudfront::${AWS::AccountId}:distribution/${'+name+'CDN}'))
 for suffix in ['A','AAAA']:
  for prefix in ['', 'www.']:
   resources[name+('WWW' if prefix else 'Apex')+suffix]={'Type':'AWS::Route53::RecordSet','Properties':{'HostedZoneId':ref(name+'Zone'),'Name':prefix+domain,'Type':suffix,'AliasTarget':{'DNSName':att(name+'CDN','DomainName'),'HostedZoneId':'Z2FDTNDATAQYW2','EvaluateTargetHealth':False}}}
 if domain in guides:
  for suffix in ['A','AAAA']:
   resources[name+'Checkin'+suffix]={'Type':'AWS::Route53::RecordSet','Properties':{'HostedZoneId':ref(name+'Zone'),'Name':'checkin.'+domain,'Type':suffix,'AliasTarget':{'DNSName':att(name+'CDN','DomainName'),'HostedZoneId':'Z2FDTNDATAQYW2','EvaluateTargetHealth':False}}}
  aliases=resources[name+'CDN']['Properties']['DistributionConfig']['Aliases']['Fn::If'][1]
  aliases.append('checkin.'+domain)
resources['BucketPolicy']={'Type':'AWS::S3::BucketPolicy','Properties':{'Bucket':ref('SitesBucket'),'PolicyDocument':{'Version':'2012-10-17','Statement':[{'Sid':'AllowCloudFrontOnly','Effect':'Allow','Principal':{'Service':'cloudfront.amazonaws.com'},'Action':'s3:GetObject','Resource':sub('${SitesBucket.Arn}/*'),'Condition':{'StringEquals':{'AWS:SourceArn':arns}}},{'Sid':'DenyInsecureTransport','Effect':'Deny','Principal':'*','Action':'s3:*','Resource':[att('SitesBucket','Arn'),sub('${SitesBucket.Arn}/*')],'Condition':{'Bool':{'aws:SecureTransport':'false'}}}]}}}
template={'AWSTemplateFormatVersion':'2010-09-09','Description':'Calopi Haven: private S3, three CloudFront distributions and Route 53 zones','Parameters':{'EnableCustomDomains':{'Type':'String','AllowedValues':['true','false'],'Default':'false'},'CertificateArn':{'Type':'String','Default':''}},'Conditions':{'CustomDomains':{'Fn::Equals':[ref('EnableCustomDomains'),'true']}},'Resources':resources,'Outputs':outputs}
Path(__file__).with_name('static-sites.json').write_text(json.dumps(template,indent=2)+'\n')
