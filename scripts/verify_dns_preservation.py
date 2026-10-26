"""Verify that every copied non-web DNS record is present before delegating zones."""
import json,boto3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=boto3.Session(profile_name='ticosync',region_name='us-east-1');r=s.client('route53')
outputs={x['OutputKey']:x['OutputValue'] for x in json.loads((ROOT/'infrastructure/stack-outputs.json').read_text())}
backup=json.loads((ROOT/'infrastructure/dns-before.json').read_text())
for name,domain in [('Calopi','calopihaven.com'),('RedHawk','redhawk2240.com'),('Silvermill','silvermill8294.com')]:
 current={(x['Name'],x['Type']):x for page in r.get_paginator('list_resource_record_sets').paginate(HostedZoneId=outputs[name+'ZoneId']) for x in page['ResourceRecordSets']}
 for old in backup[domain]['preserved_recordsets']:
  new=current[(old['Name'],old['Type'])];assert {x['Value']for x in old['ResourceRecords']}=={x['Value']for x in new['ResourceRecords']},(domain,old['Name'])
  assert old['TTL']==new['TTL']
 print(domain,': all',len(backup[domain]['preserved_recordsets']),'email / verification / ancillary recordsets preserved')
