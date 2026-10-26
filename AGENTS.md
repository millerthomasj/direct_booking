# Calopi Haven / direct_booking — agent instructions

Read this file and `docs/aws-deployment.md` before changing or deploying the sites.
This repository contains **one main brand site and two separate property sites**.
Do not treat it as one site with interchangeable booking widgets.

## Site map and source of truth

| Site | Domain | Source / generation | Production package |
| --- | --- | --- | --- |
| Main brand / property comparison | `calopihaven.com` | Hand-authored `index.html`; `calopi.css` | `dist/calopihaven.com/index.html` |
| Red Hawk 2240 | `redhawk2240.com` | Alpine template in `scripts/build_mockups.py` → `alpine.html` → `scripts/build_property_sites.py` → `redhawk.html` | `dist/redhawk2240.com/index.html` |
| Silvermill 8294 | `silvermill8294.com` | Property-specific content in `scripts/build_property_sites.py` → `silvermill.html` | `dist/silvermill8294.com/index.html` |

- **Never replace the main `index.html` with a property page.** The main site
  introduces and compares both properties, then links to their separate domains.
- Edit property generators, then regenerate; do not make lasting changes only to
  generated `redhawk.html`, `silvermill.html`, or `alpine.html`.
- `styles.css`, `site.js`, fonts and photo assets are shared. Shared changes need
  checks across the main site and both properties. `calopi.css` only styles the
  brand homepage.
- Alpine is the selected property design. `gatherings.html`, `summit.html`,
  `concepts.html` and the older review PDF are historical design concepts.
- GitHub Pages is the **review preview**, not the production hosting target:
  `https://millerthomasj.github.io/direct_booking/`.
- Public HTML uses actual domain links. `data-preview-path` plus `site.js` maps
  them to local pages only on localhost / GitHub Pages. Preserve both routes.
- Main page design: Keystone skiing headline photo; make the two choices and
  their differences clear immediately. Avoid long generic hospitality copy
  above the property choices. Retain photo attribution/license links.

## Property and booking distinctions

| Property | Capacity / layout | OwnerRez widget ID | OwnerRez property key |
| --- | --- | --- | --- |
| Red Hawk 2240 | 6 guests; 2 bedrooms; 2 baths | `f13cd4d5594545a4b410a094355b8b4d` | `bc7244c04d284b70baab4dede8d52fb0` |
| Silvermill 8294 | Up to 4 adults and 1 child; 1 bedroom; 1 bath | `c10114d38806484bbd3c7bfd9bf4858e` | `3f15f3b1b0f548328ab5276d7014358a` |

- Keep the compact date/occupancy selector. The user rejected the full embedded
  OwnerRez contact form as too ugly. Submit GET to the correct hosted OwnerRez
  widget with `view=form`, `propertyKey`, `or_arrival`, and `or_departure`.
- Red Hawk uses `or_guests`; Silvermill uses separate `or_adults` / `or_children`
  and limits occupancy to at most four adults and one child. No OwnerRez API key is needed.
- The compact selector does not know booked dates or rates. OwnerRez confirms
  availability, quoting, rental terms and secure checkout after continuing.
- Never swap property IDs or send test inquiries/reservations/payments while
  checking layout or navigation.
- Red Hawk: king, queen and Murphy bed; approximately 900 ft to gondola; shared
  heated pool and hot tubs at Red Hawk Lodge.
- Silvermill: king, twin sleeper chair and sofa bed; less than 700 ft to gondola;
  hot tubs on site, **pool at nearby Dakota Lodge**, not at Silvermill.
- Guest guides: `checkin.redhawk2240.com` and `checkin.silvermill8294.com`.
  Preserve their existing Canva destinations. Never copy access codes, Wi-Fi
  passwords or other private arrival details into public site files.
- Source notes and photo licenses live in `docs/*photo*.json` and the README.

## Production hosting — use the existing infrastructure

- AWS profile: `ticosync`; account: **`175678592495`**; region: `us-east-1`.
- CloudFormation stack: **`calopihaven-static-sites`** (termination protected).
- One private, encrypted, versioned bucket:
  **`ticosync-calopihaven-sites-175678592495`**.
- Separate bucket prefixes / CloudFront distributions / Route 53 hosted zones:

| Site | S3 prefix | CloudFront ID | CloudFront hostname |
| --- | --- | --- | --- |
| Main | `calopihaven.com/` | `E1DS8J1PE1YDRD` | `dvte5np9w3can.cloudfront.net` |
| Red Hawk | `redhawk2240.com/` | `E25YRLB4R10XHN` | `ddafqpgye8k2a.cloudfront.net` |
| Silvermill | `silvermill8294.com/` | `EWVFX88JNB0Y9` | `d1zm64ienf7zps.cloudfront.net` |

- Routine content changes only require packaging, upload and invalidation.
  **Do not recreate buckets/distributions/certificates or change DNS for updates.**
- S3 access is private; CloudFront uses signed Origin Access Control. Do not
  enable public S3 website hosting or public ACLs/policies.
- `infrastructure/stack-outputs.json` and live CloudFormation outputs contain the
  zone IDs and assigned nameservers. ACM is in `us-east-1`; its ARN and validation
  records are recorded in `infrastructure/certificate.json` and
  `infrastructure/acm-validation.json`.
- Roots use Route 53 A/AAAA aliases to CloudFront. **Do not put resolved
  CloudFront IPs into permanent A records.** No fixed IPs are needed.
- Registrations remain at Squarespace. Preserve MX, SPF, DKIM, verification,
  guest-guide behavior and certificate validation records in any future DNS work.
- Exact copied records and migration audit: `infrastructure/dns-before.json`,
  `infrastructure/dns-migration.json`; check with `scripts/verify_dns_preservation.py`.
- Infrastructure changes use `infrastructure/make_template.py` →
  `infrastructure/static-sites.json`. Preserve the stack's active certificate
  and EnableCustomDomains parameter; see the runbook command.

## Environment, build, check, deploy

Use an existing Python environment with BeautifulSoup, boto3, Playwright and
Pillow, or create a local environment:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m playwright install chromium
```

Commands below assume that environment is activated. For property-source changes:

```sh
python scripts/build_mockups.py
python scripts/build_property_sites.py
```

For **every production deployment**, build fresh production packages:

```sh
python scripts/build_domains.py --production
```

The production flag removes preview noindex, sets each site's own canonical and
social URLs, generates robots.txt/sitemap.xml, and makes guest-guide URLs HTTPS.
Do not upload preview/noindex packages or reuse stale `dist/` after edits.

For meaningful UI, linking or booking changes, serve the repository and check:

```sh
python -m http.server 8124 --bind 127.0.0.1
# In another terminal, with the same environment:
python scripts/check_property_sites.py
python scripts/check_haven.py
```

These check responsive layouts, property navigation and the correct OwnerRez
date/guest handoff. The tests simulate final domain navigation using `dist/`, so
build packages before running them. No actual booking is submitted. Do not add
extra tests for small copy-only changes unless there is a concrete concern.

Deploy when authorized:

```sh
aws --profile ticosync sts get-caller-identity
python scripts/deploy_aws.py
```

The uploader verifies account/bucket, uploads each package to its own prefix,
sets content type/cache controls/hash metadata, then invalidates all three owned
CloudFront distributions. Upload is versioned; it does not delete unrelated keys.
Commit/push source changes to `main` as well; pushing to GitHub alone updates the
review site, **not production S3**.

Verify the changed live pages after deployment: HTTP 200, correct property/name,
assets, canonical, no accidental noindex, and relevant links / OwnerRez property
key. Follow CloudFront deployment/invalidation status when investigating stale
content. Keep the runbook and migration state current if infrastructure changes.

## Outstanding migration at last update — 2026-10-26

- Calopi Haven and Silvermill registrar nameservers were switched to Route 53;
  the parent `.com` delegation was verified. Recheck live DNS rather than assume
  a historical propagation state is still current.
- **Red Hawk's final NS change is pending**, because its previous DNSSEC DS had
  an 86400-second TTL. Old DS absence was confirmed by October 26 at 19:00 UTC.
- The guarded finalization command is safe **after October 27, 2026 at 1 PM
  Costa Rica time (19:00 UTC)**, with the authenticated Squarespace Chrome tab:

```sh
python scripts/finish_redhawk_dns.py          # inspect plan only
python scripts/finish_redhawk_dns.py --apply  # time/DS/preservation guarded
```

This step was authorized in the original deployment task but is not scheduled.
Check current migration JSON and actual registrar delegation first; do not redo
it if already completed. After completing it, update this section and the runbook.
Do not restart the 24-hour hold unless a new DS record was actually introduced.

Old Squarespace apex/www forwarding points to each AWS endpoint as a temporary
bridge for cached DNS, and for Red Hawk during its hold. A response with
`Server: Squarespace` and a 302 to CloudFront is this old-DNS path, **not** the
final AWS root-domain behavior. Calopi's correct AWS response is HTTP 200 at its
own hostname with no Location header. Do not disable the fallback while old DNS
still routes visitors to Squarespace. The local Mac/network cached old IPv4 DNS
at launch even after public resolvers had updated.

To bypass a cached lookup while preserving the real domain's TLS/SNI:

```sh
curl -I --connect-to calopihaven.com:443:dvte5np9w3can.cloudfront.net:443 https://calopihaven.com/
```

Compare authoritative DNS / `dig @1.1.1.1` / `dig @8.8.8.8` with local resolution
before diagnosing redirects as an AWS configuration failure. Do not claim a
standard local curl has stopped redirecting until that exact path is verified.
