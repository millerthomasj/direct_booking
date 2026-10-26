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
  checks across the main site and both properties. `calopi.css` styles the
  brand homepage and shared Calopi header on both property sites. Property
  headers reuse the main logo/wordmark and name the current property below it.
- Each property hero must show its own living room immediately: Red Hawk uses
  `assets/photo-01.webp`; Silvermill uses `assets/silvermill/08.webp`. Production
  social previews use the same property-specific photos. Keep Keystone skiing
  as the main Calopi hero’s first slide.
- Alpine is the selected property design. `gatherings.html`, `summit.html`,
  `concepts.html` and the older review PDF are historical design concepts.
- GitHub Pages is the **review preview**, not the production hosting target:
  `https://millerthomasj.github.io/direct_booking/`.
- Public HTML uses actual domain links. `data-preview-path` plus `site.js` maps
  them to local pages only on localhost / GitHub Pages. Preserve both routes.
- Typography: keep small labels/captions at least 12px, body copy around 16–17px,
  and phone date/select inputs at 16px. The user found the previous tiny text
  difficult to read; do not restore it to fit layouts. Adjust wrapping instead.
- Main page design: lead with beautifully designed, carefully maintained homes
  and personal hosting by Hope & Tom. The owner’s October 26 feedback moved
  the brand toward “why book one of our condos,” supported by real guest reviews.
  Keep the Keystone skiing headline photo, clear summaries of both property
  choices near the top. The owner removed the comparison-table section; do not
  restore it or links to #compare. Retain photo credits.
- Brand presentation: use the owner-supplied three-mountain logo,
  `assets/mountains-logo-transparent.png`, with the Calopi Haven wordmark across all headers
  and matching logos in the footers. Favicon: `assets/mountains-favicon-transparent.png`.
  Source `mountains_logo.jpeg` was converted to PNG on the owner’s Desktop; the
  active web PNG removes the background with real alpha transparency; keep it
  transparent and do not flatten it onto a colored canvas or apply blend modes. This replaces the older family
  illustration and text-only phase. Keep headers compact. Do not publish the
  children’s names or explain the origin of Calopi.
- Silvermill is hosted, not owned, by Hope & Tom. Do not imply ownership of
  both properties; describe them as the two condos they host.
- Red Hawk is on the edge of River Run Village, for a slightly quieter stay.
  Do not describe it as outside the village.
- Main-page motion lives in `calopi.js`; preserve reduced-motion and pause support.
- All three live pages mention Hope’s Airbnb Superhost status and link directly
  to the relevant Airbnb listing(s). Both statuses were verified October 26,
  2026 in the owner browser. Keep these visible alongside direct booking.
- Guest review provenance: `docs/guest-review-sources.json`. Use verified short
  excerpts with guest first name, property, month/year and Airbnb source links.
  Ratings/counts are dated snapshots; verify before updating. Do not invent a
  combined rating, imply all reviews are positive, or retain private reservation
  details / full guest reviews in the repository.

## Property and booking distinctions

| Property | Capacity / layout | OwnerRez widget ID | OwnerRez property key |
| --- | --- | --- | --- |
| Red Hawk 2240 | 6 guests; 2 bedrooms; 2 baths | `f13cd4d5594545a4b410a094355b8b4d` | `bc7244c04d284b70baab4dede8d52fb0` |
| Silvermill 8294 | Up to 4 adults and 1 child; 1 bedroom; 1 bath | `c10114d38806484bbd3c7bfd9bf4858e` | `3f15f3b1b0f548328ab5276d7014358a` |

- Keep booking-provider branding out of public copy and metadata. Use the
  OwnerRez widget silently; preserve its functional URLs, fields and identifiers.
- Keep the compact date/occupancy selector. The user rejected the full embedded
  OwnerRez contact form as too ugly. The compact selector opens the FULL live
  widget in an on-page `<dialog>` popup. Preserve selected dates/occupancy. The
  popup embeds the widget endpoint directly (without `view=form`) to avoid a
  double iframe; the fallback separate link uses the hosted `view=form` page.
  Keep native target=_blank fallback for no-JS/unsupported browsers. “Browse
  dates first” opens the popup without requiring dates, but carries any dates
  and guest counts already selected. Keep generous padding inside the popup. All runtime calendar,
  rates and Book Now behavior belongs to the live widget. No API key is needed.
  For booking changes, verify real quotes/calendar fields as well as mocked
  navigation tests. The provider rejects localhost referrers: test with the
  real domain origin (production packages can be routed locally in Playwright).
  Iframe height messages must match the provider origin and iframe window.
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
  Preserve their existing Canva destinations for confirmed guests, but do not
  link to either guide from any public page: they include lockbox information.
  Never copy access codes, Wi-Fi
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
- All three `www` hostnames use HTTPS and permanently redirect (301) to their
  matching apex domain, preserving the path and query string. The former Red
  Hawk migration exception was removed after nameserver cutover.
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

## DNS migration completed — 2026-10-26

- All three registrar delegations now use Route 53. Red Hawk’s nameservers were
  switched October 26 at the owner’s explicit request to proceed early despite
  the old DNSSEC cache risk. The `.com` parent delegation was verified on AWS.
- There is **no remaining scheduled or pending Red Hawk cutover**. Do not redo it.
- The original DNSSEC safety deadline remains October 27, 2026 at 1 PM Costa Rica
  (19:00 UTC). Until then, resolvers caching the old DS can temporarily fail.
  The parent DS is absent; no new DS was published. Do not re-enable DNSSEC
  without deliberately configuring signing and a matching DS.
- Registrar results, explicit early-risk acceptance and verification are in
  `infrastructure/dns-migration.json`. All preserved email/verification records,
  direct custom-domain HTTPS and the existing guest-guide redirect were checked.
- `scripts/finish_redhawk_dns.py` retains its default time guard. Its explicit
  `--accept-dnssec-cache-risk` override was used for this owner-authorized cutover.

Old Squarespace apex/www forwarding points to each AWS endpoint as a temporary
bridge for cached DNS, and while old delegations remain cached. A response with
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
