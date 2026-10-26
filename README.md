# Red Hawk 2240 — direct-booking design concepts

Three complete static website mockups for the Keystone, Colorado condo.
Shareable preview: https://millerthomasj.github.io/direct_booking/

GitHub Pages serves this review from `main` at the repository root. No custom
domain was changed. Pages use `noindex,nofollow` while the designs are reviewed.

Start at [the comparison page](index.html), or open:

1. [The Alpine Edit](alpine.html) — forest green/ivory, refined editorial hospitality.
2. [The Gathering Place](gatherings.html) — warm terracotta/teal, family-oriented.
3. [Basecamp 2240](summit.html) — charcoal/lime, bold mountain adventure.

[Four-page design review PDF](previews/Red-Hawk-2240-design-review.pdf).
Desktop, phone and full-page JPGs are in `previews/`.

## Preview

No build or runtime dependencies. Open `index.html` directly, or:

```sh
python3 -m http.server 8124 --bind 127.0.0.1
```

Then visit http://127.0.0.1:8124. All fonts and photos are local; there are no API keys. The three concepts embed the OwnerRez booking widget. This mockup does not change
the existing `www.redhawk2240.com` redirect or `checkin.redhawk2240.com` guide.

## Implemented

Responsive desktop/phone layouts, photo dialogs, FAQs and seasonal controls.
All three concepts now embed the same OwnerRez Book Now/Inquiry widget, restricted
to Red Hawk 2240. Availability, quotes, inquiries and checkout are handled by
OwnerRez using the existing property configuration. These are live forms.

Widget ID: `f13cd4d5594545a4b410a094355b8b4d` (public embed identifier).
The widget includes a hosted-booking fallback link; no secret or backend is needed.
No reservations, inquiries or payments were submitted during verification.

## Sources and content

Inspected the owner's signed-in Airbnb listing editor, listing 45842208, and its
62-photo tour on October 25, 2026. Public property photos were downloaded and
optimized to WebP; source URLs/captions are in `docs/photo-sources.json`. The
current editor confirms six guests, two bedrooms, two bathrooms, pool/two hot
tubs, private balcony and approximately 900 feet to River Run. Bedroom setup,
heated garage space, ski locker and other amenities were cross-checked with the
public listing: https://www.airbnb.com/rooms/45842208.

Inspected the welcome page in the owner's Canva guest guide. No access codes,
Wi-Fi credentials or private arrival instructions are copied into this repo.
Photos remain the owner's supplied property material. Outfit font is bundled
under its OFL license in `assets/outfit-LICENSE.txt`.

No review scores, stale construction notices, fabricated testimonials, rates or
promised savings are used. Confirm current house rules, bedroom setup and shared
amenity access before the final launch. New copy is specific to these designs.

## Rebuild and review

`python3 scripts/build_mockups.py` regenerates the three concept HTML files;
edit its templates for content/layout changes. Shared styles/interactions are
`styles.css` and `site.js`. The hand-written comparison page is `index.html`.

With Playwright and Pillow installed and the preview server running:

```sh
python scripts/check_mockups.py
python scripts/build_review_pdf.py
```

The browser check exercises all three concepts at 1440px and 390px, rejects
horizontal overflow and broken assets, checks photo dialogs/keyboard handling,
booking dates/guests, FAQs, seasonal controls, and comparison navigation. It
refreshes the screenshot artifacts; the PDF script packages the review.
OwnerRez rejects localhost iframe referrers; verify the live form on the HTTPS
GitHub Pages preview. The hosted-booking fallback also works from local previews.

## After choosing a design

The OwnerRez booking integration is connected. Confirm the property's existing
rates, taxes, rental agreement and payment configuration before sharing broadly,
then point the real domain at the chosen site. The current domain redirect and
check-in guide are unchanged.
