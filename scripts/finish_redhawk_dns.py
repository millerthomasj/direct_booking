"""Finish the authorized DNS migration after the old DNSSEC DS cache expires.

Requires the owner's signed-in Squarespace tab in Google Chrome. No credentials
or cookies are stored. Run without --apply to inspect the plan.
"""
import argparse,json,subprocess,time
from pathlib import Path
from datetime import datetime,timezone
import boto3
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--apply',action='store_true');p.add_argument('--accept-dnssec-cache-risk',action='store_true',help='Explicit owner-authorized early cutover; cached old DS records may temporarily cause resolution failures');args=p.parse_args()
state=json.loads((ROOT/'infrastructure/dns-migration.json').read_text());hold=state['redhawk2240.com'];deadline=datetime.fromisoformat(hold['safe_nameserver_cutover_after'].replace('Z','+00:00'))
outputs={x['OutputKey']:x['OutputValue']for x in json.loads((ROOT/'infrastructure/stack-outputs.json').read_text())}
servers=[x.strip()for x in outputs['RedHawkNameservers'].split(',')]
print('Red Hawk nameservers:',', '.join(servers));print('Earliest safe cutover:',deadline.isoformat())
if not args.apply:raise SystemExit('Plan only. Use --apply after the DNSSEC cache deadline.')
early_cutover=datetime.now(timezone.utc)<deadline
if early_cutover and not args.accept_dnssec_cache_risk:raise SystemExit('DNSSEC hold has not expired; refusing early migration without explicit risk acceptance.')
if early_cutover:print('Owner-authorized early migration: accepting temporary DNSSEC cache resolution risk.')
s=boto3.Session(profile_name='ticosync',region_name='us-east-1');assert s.client('sts').get_caller_identity()['Account']=='175678592495'
current={(r['Name'],r['Type']):r for page in s.client('route53').get_paginator('list_resource_record_sets').paginate(HostedZoneId=outputs['RedHawkZoneId'])for r in page['ResourceRecordSets']}
for old in json.loads((ROOT/'infrastructure/dns-before.json').read_text())['redhawk2240.com']['preserved_recordsets']:
 actual=current[(old['Name'],old['Type'])];assert actual['ResourceRecords']==old['ResourceRecords'] or {x['Value']for x in actual['ResourceRecords']}=={x['Value']for x in old['ResourceRecords']}
answer=subprocess.run(['dig','+time=3','+tries=1','+short','@a.gtld-servers.net','redhawk2240.com','DS'],capture_output=True,text=True,check=True).stdout.strip()
assert not answer,('DS delegation still present',answer)
def browser(js):
 script='''tell application "Google Chrome"
repeat with w in windows
repeat with t in tabs of w
if URL of t contains "account.squarespace.com" then
return execute t javascript JS
end if
end repeat
end repeat
error "Open the signed-in Squarespace account in Chrome first"
end tell'''.replace('JS',json.dumps(js))
 return subprocess.run(['osascript','-e',script],capture_output=True,text=True,check=True).stdout.strip()
js='''window.__havenFinishRedHawk={pending:true};(async()=>{try{const info=await fetch('/api/account/1/domains/byName/redhawk2240.com').then(r=>r.json());if(info.id!=='667eff7ccb71114350c00dea'||info.isDnssecSigned)throw Error('Unexpected domain or DNSSEC remains enabled');const crumb=decodeURIComponent(document.cookie.split(';').map(x=>x.trim()).find(x=>x.startsWith('crumb=')).slice(6));const r=await fetch('/api/account/1/domains/'+info.id+'/nameservers',{method:'PUT',headers:{'Content-Type':'application/json','X-CSRF-Token':crumb},body:JSON.stringify({nameServers:SERVERS.map(hostName=>({hostName}))})});const body=await r.text();if(!r.ok)throw Error('Registrar returned '+r.status+': '+body);const after=await fetch('/api/account/1/domains/'+info.id+'/nameservers').then(r=>r.json());window.__havenFinishRedHawk={status:r.status,after,time:new Date().toISOString()};}catch(e){window.__havenFinishRedHawk={error:String(e)}}})();'Migration requested';'''.replace('SERVERS',json.dumps(servers))
browser(js)
for _ in range(30):
 result=json.loads(browser('JSON.stringify(window.__havenFinishRedHawk);'))
 if not result.get('pending'):break
 time.sleep(1)
else:raise SystemExit('Registrar response still pending; inspect the browser before retrying.')
if 'error'in result:raise SystemExit(result['error'])
assert sorted(x['hostName']for x in result['after']['nameServers'])==sorted(servers),result
state['redhawk2240.com'].update(status='nameservers_updated',registrar_result=result)
if early_cutover:state['redhawk2240.com']['early_cutover_authorization']={'accepted_dnssec_cache_risk':True,'reason':'Owner explicitly requested immediate switch despite the previously explained waiting period because traffic is negligible.','time':result['time']}
(ROOT/'infrastructure/dns-migration.json').write_text(json.dumps(state,indent=2)+'\n')
print('Red Hawk registrar nameservers updated and verified. Check parent delegation and HTTPS as DNS propagates.')
