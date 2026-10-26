# Calopi Haven production hosting

Deployed October 26, 2026, in TicoSync AWS account `175678592495` (`ticosync`
profile), region `us-east-1`. Domain registration remains at Squarespace.

## Hosting

One private, encrypted, versioned S3 bucket:
`ticosync-calopihaven-sites-175678592495`. Each site has its own prefix and
CloudFront distribution, using signed Origin Access Control. Direct anonymous
S3 object access returns 403. CloudFront requires HTTPS and adds security headers.

| Site | Distribution | DNS target | Route 53 zone |
| --- | --- | --- | --- |
| calopihaven.com | E1DS8J1PE1YDRD | dvte5np9w3can.cloudfront.net | Z0033926373ZHUWIOYRP3 |
| redhawk2240.com | E25YRLB4R10XHN | ddafqpgye8k2a.cloudfront.net | Z08767391XDZBRJXZY7X5 |
| silvermill8294.com | EWVFX88JNB0Y9 | d1zm64ienf7zps.cloudfront.net | Z05599972IEKPN3C5J3AA |

Route 53 A and AAAA **alias records** handle the root names and `www`. There
are no fixed IP addresses to configure. Check-in subdomains also use aliases to
the appropriate property distribution, whose CloudFront Function redirects to
the existing Canva guide. Both guide destinations were preserved exactly.

ACM certificate `c19efc25-5588-4fc7-ad9a-0d4903a1e6ed` is issued in `us-east-1`.
It covers all three roots, all three `www` names, and both `checkin` names.
Eight validation CNAMEs were added to both the existing DNS and Route 53. Keep
these records for automatic renewal. Exact records: `infrastructure/acm-validation.json`.
The earlier six-name pending certificate created during setup was deleted.

## DNS migration status

- **Calopi Haven:** Squarespace accepted Route 53 nameservers at
  `2026-10-26T19:00:54Z`. Parent `.com` delegation verified on AWS.
- **Silvermill:** accepted at `2026-10-26T19:00:56Z`. Parent delegation verified.
- **Red Hawk:** AWS site, certificate, aliases, records and guest-guide redirect
  are ready. Existing DNS remains at Squarespace pending the old DNSSEC DS TTL.
  DNSSEC was disabled at `2026-10-26T18:56:13Z`; DS absence was subsequently
  confirmed at the parent. Original DS TTL was **86400 seconds**. Do not switch
  nameservers before **October 27, 2026, 1 PM Costa Rica / 19:00 UTC**.
  This final switch is staged, **not automatically scheduled**.

Email, DKIM, SPF, Google verification and Domain Connect recordsets were copied
from the authenticated Squarespace inventory before any delegation changes.
Their exact values and TTLs were compared against Route 53: 4 recordsets for
Calopi Haven, 7 for Red Hawk, 4 for Silvermill. Apex/web records are intentionally
replaced by CloudFront aliases. Original records: `infrastructure/dns-before.json`.
Registrar responses and timestamps: `infrastructure/dns-migration.json`.
No email messages were sent as part of verification.

The original Squarespace apex and www forwarding destinations now point to each
site's AWS endpoint instead of Airbnb. This is a **temporary bridge for cached
old DNS**, and also lets Red Hawk's existing domain reach its new site during
the DNSSEC hold. Requests that reach Squarespace can therefore show a 302 to
`*.cloudfront.net` while caches expire. The actual root-domain configuration on
AWS serves HTTP 200 directly; Calopi/Silvermill www redirect to their root names.
Red Hawk currently serves both root and www with a root canonical URL.
Do not delete the old forwarding rules while cached DNS may still reach them.

On October 26 at 19:06 UTC, Google and Cloudflare public DNS returned CloudFront
addresses for Calopi while the local macOS IPv4 lookup still cached Squarespace.
This explains a local `curl -I` showing the fallback redirect after migration.
Verify the real custom-domain response, preserving TLS/SNI, with:

```sh
curl -I --connect-to calopihaven.com:443:dvte5np9w3can.cloudfront.net:443 https://calopihaven.com/
```

That request was verified as HTTP 200 with the Calopi page and no Location header.
Do not copy a currently resolved CloudFront IP into a permanent DNS A record.

## Final Red Hawk nameserver step

After the DNSSEC hold expires, with the owner's authenticated Squarespace tab
open in Google Chrome:

```sh
python scripts/finish_redhawk_dns.py          # inspect only
python scripts/finish_redhawk_dns.py --apply  # guarded cutover
```

The script checks the time, absence of the parent DS, the AWS account and all
preserved email records before updating the registrar. It uses the active
browser session without storing credentials. Then verify parent NS delegation,
HTTPS, MX/TXT and the guest guide. Its assigned nameservers are:

- ns-1849.awsdns-39.co.uk
- ns-1499.awsdns-59.org
- ns-990.awsdns-59.net
- ns-421.awsdns-52.com

Calopi Haven nameservers:

- ns-872.awsdns-45.net
- ns-1701.awsdns-20.co.uk
- ns-1195.awsdns-21.org
- ns-189.awsdns-23.com

Silvermill nameservers:

- ns-2018.awsdns-60.co.uk
- ns-377.awsdns-47.com
- ns-960.awsdns-56.net
- ns-1234.awsdns-26.org

## Updates and verification

The CloudFormation stack is `calopihaven-static-sites`; termination protection
is enabled. The bucket and hosted zones have retain policies. Its template and
generator are in `infrastructure/`. No existing TicoSync app distributions,
load balancers or DNS zones were modified.

```sh
python scripts/build_domains.py --production
python scripts/deploy_aws.py
python scripts/verify_dns_preservation.py
```

The production build removes preview noindex, adds per-domain canonical and social
metadata, generates robots.txt/sitemap.xml, and makes guest-guide links HTTPS.
Preview HTML remains noindex. The uploader verifies the AWS account, uploads
only each site's own prefix with content types/cache controls/hash metadata,
and invalidates the three distributions. S3 versioning supports rollback.

All three distributions reached Deployed. All eight custom-domain HTTPS routes
were tested directly against CloudFront before DNS cutover. Root pages, local
images/fonts/scripts, robots and sitemaps returned 200. Production navigation
from the public Calopi homepage to both properties and the correct OwnerRez
GET date handoff was tested without sending an inquiry, reservation or payment.

For future infrastructure changes, preserve the active certificate parameters:

```sh
python infrastructure/make_template.py
aws --profile ticosync --region us-east-1 cloudformation update-stack \
  --stack-name calopihaven-static-sites \
  --template-body file://infrastructure/static-sites.json \
  --parameters ParameterKey=EnableCustomDomains,UsePreviousValue=true \
               ParameterKey=CertificateArn,UsePreviousValue=true
```

DNS migration reference:
https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/migrate-dns-domain-in-use.html
