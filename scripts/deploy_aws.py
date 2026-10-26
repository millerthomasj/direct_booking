"""Upload domain packages and invalidate each owned CloudFront distribution."""
import argparse,boto3,hashlib,json,mimetypes,time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--profile',default='ticosync');args=p.parse_args()
s=boto3.Session(profile_name=args.profile,region_name='us-east-1')
assert s.client('sts').get_caller_identity()['Account']=='175678592495','Unexpected AWS account'
stack=s.client('cloudformation').describe_stacks(StackName='calopihaven-static-sites')['Stacks'][0]
outputs={x['OutputKey']:x['OutputValue'] for x in stack['Outputs']}
(ROOT/'infrastructure/stack-outputs.json').write_text(json.dumps(stack['Outputs'],indent=2)+'\n')
s3=s.client('s3');cf=s.client('cloudfront');bucket=outputs['Bucket']
assert bucket=='ticosync-calopihaven-sites-175678592495'
for name,domain in [('Calopi','calopihaven.com'),('RedHawk','redhawk2240.com'),('Silvermill','silvermill8294.com')]:
 directory=ROOT/'dist'/domain;assert (directory/'index.html').exists()
 def upload(path):
  content=path.read_bytes();key=domain+'/'+str(path.relative_to(directory));digest=hashlib.sha256(content).hexdigest()
  s3.put_object(Bucket=bucket,Key=key,Body=content,ContentType=mimetypes.guess_type(str(path))[0] or 'application/octet-stream',CacheControl=('no-cache,max-age=0,must-revalidate' if path.suffix=='.html' else 'public,max-age=300' if path.suffix in ['.xml','.txt'] else 'public,max-age=86400'),Metadata={'sha256':digest})
 files=[x for x in directory.rglob('*') if x.is_file()]
 with ThreadPoolExecutor(8) as executor:list(executor.map(upload,files))
 invalidation=cf.create_invalidation(DistributionId=outputs[name+'DistributionId'],InvalidationBatch={'Paths':{'Quantity':1,'Items':['/*']},'CallerReference':'calopi-'+str(time.time_ns())})
 print(domain,len(files),'files uploaded; distribution',outputs[name+'DistributionId'],'invalidation',invalidation['Invalidation']['Id'],flush=True)
