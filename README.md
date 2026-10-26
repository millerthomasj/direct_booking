# Keystone direct-booking sites

Calopi Haven is the shared homepage. Both property websites use the selected
Alpine design.

| Site | Review URL | Planned domain |
| --- | --- | --- |
| Calopi Haven | https://millerthomasj.github.io/direct_booking/ | calopihaven.com |
| Red Hawk 2240 | https://millerthomasj.github.io/direct_booking/redhawk.html | redhawk2240.com |
| Silvermill 8294 | https://millerthomasj.github.io/direct_booking/silvermill.html | silvermill8294.com |

Public links point to the planned domains in HTML. On the GitHub Pages review
host and localhost, `site.js` maps those links to the matching preview pages so
all three sites can be reviewed together before DNS changes. `data-preview-path`
contains only the review counterpart. On real domains, the links remain public
URLs. Both property footers link back to Calopi Haven and to the other property.

The original design comparison remains at `concepts.html`. Both selected sites
use compact date/guest forms that pass selections to the correct OwnerRez hosted
booking widget. Red Hawk accommodates six; Silvermill accommodates five (at most four adults).
Silvermill passes separate adult and child counts to match its OwnerRez rules.
No API keys are stored. Availability, pricing, rental terms and checkout are
handled by OwnerRez. No inquiry, reservation or payment was submitted in testing.

The current custom domains and check-in guides are unchanged. These review URLs
remain noindex until the custom-domain launch.

## Rebuild and preview

```sh
python3 scripts/build_mockups.py
python3 scripts/build_property_sites.py
python3 -m http.server 8124 --bind 127.0.0.1
```

The selected-site builder needs beautifulsoup4. Calopi Haven's hand-authored
homepage is `index.html`, styled by `calopi.css`; the property builder only writes
`redhawk.html` and `silvermill.html`.

`python3 scripts/build_domains.py` creates separate static hosting directories
under `dist/calopihaven.com`, `dist/redhawk2240.com`, and `dist/silvermill8294.com`,
each with the correct root `index.html` and shared assets. This packages the
sites; it does not update DNS or deploy any custom domain. Keep review noindex
until the launch configuration is finalized.

Browser verification:

```sh
python scripts/check_property_sites.py
python scripts/check_haven.py
```

This checks both properties at 1440px, 390px and 320px, including image loading,
photo dialogs, FAQ, guest limits and property-specific OwnerRez URL parameters.
`check_mockups.py` checks the three archived designs. The Calopi check covers
1440/768/390/320px and follows both property journeys on the preview host and on
locally simulated production hostnames using the domain packages.

## Property sources

Red Hawk: Airbnb listing 45842208 and the owner's guest guide, inspected October
25, 2026. Photo attribution/source URLs: `docs/photo-sources.json`.

Silvermill: https://www.airbnb.com/rooms/1237080165740047360 and the welcome page
of the guide linked by http://checkin.silvermill8294.com/, inspected October 26,
2026. Downloaded listing photos and source URLs are recorded in
`docs/silvermill-photo-sources.json`. Silvermill is a fifth-floor, one-bedroom,
one-bath condo for five with a king bed, twin sleeper chair and living-room sofa
bed. The pool is at nearby Dakota Lodge; hot tubs are at Silvermill. No access
codes, Wi-Fi credentials or private arrival instructions were copied.

## OwnerRez

- Red Hawk widget: `f13cd4d5594545a4b410a094355b8b4d`
- Silvermill widget: `c10114d38806484bbd3c7bfd9bf4858e`

Each widget is restricted to its own property and attributes the source to
"My Website". These IDs are public embed identifiers. Dates and guests use the
[documented OwnerRez parameters](https://www.ownerrez.com/support/articles/prepopulate-widget-fields).
The compact native date pickers do not mark booked dates; OwnerRez confirms
availability and quotes after the guest continues. Dates and occupancy were
verified against the live Silvermill form without submitting contact details.

Property photographs are the owner's supplied listing material. Outfit font is
bundled under its OFL license in `assets/outfit-LICENSE.txt`.
