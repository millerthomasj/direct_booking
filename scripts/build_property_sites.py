"""Build the selected Alpine sites. Run after build_mockups.py. Requires beautifulsoup4."""
from pathlib import Path
from bs4 import BeautifulSoup
from html import escape
ROOT=Path(__file__).resolve().parents[1]

def selected():
 s=BeautifulSoup((ROOT/'alpine.html').read_text(),'html.parser')
 s.select_one('.concept-bar').decompose()
 s.body['class'].append('selected-site')
 s.title.string='Red Hawk 2240 | A mountain stay in Keystone'
 s.select_one('.hero-image')['src']='assets/photo-01.webp'
 s.select_one('.hero-image')['alt']='Red Hawk 2240 living room with a teal sofa, fireplace and space to gather'
 s.select_one('meta[name=description]')['content']='Stay at Red Hawk 2240 in Keystone: two bedrooms, space for six, a pool and hot tubs on the edge of River Run Village. Check dates and book your stay directly.'
 for a in s.select('.brand'):a['href']='redhawk.html'
 s.select_one('.site-footer > div').append(BeautifulSoup('<a href="silvermill.html">Our other Keystone stay: Silvermill 8294 ↗</a>','html.parser'))
 return s

def image(n,alt,hero=False):
 return f'<img src="assets/silvermill/{n:02}.webp" alt="{escape(alt)}" loading="{"eager" if hero else "lazy"}"'+(' class="hero-image" fetchpriority="high"' if hero else '')+'>'
def photo(n,alt):
 return f'<button class="photo" data-photo="assets/silvermill/{n:02}.webp" data-caption="{escape(alt)}" aria-label="Enlarge: {escape(alt)}">{image(n,alt)}</button>'
def replace(s,selector,html):
 s.select_one(selector).replace_with(BeautifulSoup(html,'html.parser'))

red=selected();(ROOT/'redhawk.html').write_text(str(red))
s=selected()
# Replace property names, public links and OwnerRez identifiers before setting property-specific content.
s=BeautifulSoup(str(s).replace('RED HAWK','SILVERMILL').replace('Red Hawk','Silvermill').replace('2240','8294').replace('45842208','1237080165740047360').replace('checkin.redhawk8294.com','checkin.silvermill8294.com').replace('https://checkin.silvermill8294.com','http://checkin.silvermill8294.com/').replace('f13cd4d5594545a4b410a094355b8b4d','c10114d38806484bbd3c7bfd9bf4858e').replace('bc7244c04d284b70baab4dede8d52fb0','3f15f3b1b0f548328ab5276d7014358a'),'html.parser')
s.title.string='Silvermill 8294 | Your River Run Village retreat'
s.select_one('meta[name=description]')['content']='Stay at Silvermill 8294 in Keystone: a renovated one-bedroom condo for up to 4 adults and 1 child in River Run Village, with hot tubs and a short walk to the gondola. Book your stay directly.'
for a in s.select('.brand'):a['href']='silvermill.html'
form=s.select_one('.booking-form');form['data-max-guests']='5';form['data-max-adults']='4';form['data-max-children']='1'
guest_label=s.select_one('select[name=or_guests]').parent
guest_label.replace_with(BeautifulSoup('<label>ADULTS<select name="or_adults" aria-label="Adults">'+''.join(f'<option value="{i}" {"selected" if i==2 else ""}>{i} adult{"s" if i>1 else ""}</option>' for i in range(1,5))+'</select></label><label>CHILDREN<select name="or_children" aria-label="Children">'+''.join(f'<option value="{i}">{i} child{"ren" if i!=1 else ""}</option>' for i in range(2))+'</select></label>','html.parser'))
replace(s,'.hero-image',image(8,'Silvermill 8294 living room with bright windows, a sectional sofa and mountain-inspired artwork',True))
s.select_one('.alpine-hero .eyebrow').string='SILVERMILL LODGE · RIVER RUN VILLAGE'
s.select_one('h1').clear();s.select_one('h1').append(BeautifulSoup('A little closer<br/>to <em>everything.</em>','html.parser'))
s.select_one('.alpine-hero-copy > p:not(.eyebrow)').clear();s.select_one('.alpine-hero-copy > p:not(.eyebrow)').append(BeautifulSoup('Village mornings. Mountain days.<br/>Your own place in the middle of it all.','html.parser'))
replace(s,'.facts','<div class="facts wrap"><span><b>4 + 1</b> adults + child</span><span><b>1</b> bedroom</span><span><b>1</b> bathroom</span><span><b>&lt;700 ft</b> to the gondola</span></div>')
replace(s,'.editorial',f'''<section class="editorial wrap" id="stay"><div><p class="eyebrow">A SMALLER STAY. A LITTLE MORE EASE.</p><h2>Village life.<br>Mountain views.<br><em>All yours.</em></h2><p>A renovated fifth-floor retreat for couples, small families and a few favorite friends. Slow mornings in a king bed. Coffee by the window. Evenings around the fireplace after a day on the mountain.</p><a class="underlink" href="#gallery">Step inside ↗</a></div><figure>{photo(8,'Silvermill living room with a sectional sofa and village views')}<figcaption>Room to settle in. Every reason to step outside.</figcaption></figure></section>''')
replace(s,'.amenity-story',f'''<section class="amenity-story" id="explore"><div class="amenity-photo">{image(49,'Outdoor hot tubs in the Silvermill courtyard')}</div><div><p class="eyebrow">THE VILLAGE AT YOUR DOORSTEP</p><h2>First chair.<br>Last soak.</h2><p>Walk through River Run Village to the gondola in under three minutes. Come home to a soak in the shared courtyard hot tubs, or find your next favorite spot for dinner just outside.</p><ul class="amenity-list"><li>On-site shared hot tubs &amp; sauna</li><li>Year-round heated pool at nearby Dakota Lodge</li><li>One heated underground parking space</li><li>Private ski locker, fitness center &amp; billiards lounge</li></ul></div></section>''')
items=[(0,'Living room with fireplace and mountain-inspired artwork'),(21,'King bedroom with soft linens and an upholstered headboard'),(10,'Full kitchen with breakfast bar seating'),(25,'Bedroom workspace overlooking River Run Village'),(28,'Bathroom with shower and bathtub'),(53,'Shared billiards lounge at Silvermill Lodge')]
replace(s,'.gallery-grid','<div class="gallery-grid">'+''.join(photo(n,a) for n,a in items)+'</div>')
s.select_one('.gallery-section .section-top > p').clear();s.select_one('.gallery-section .section-top > p').append(BeautifulSoup('Your River Run retreat.<br/>A few very good places to unwind.','html.parser'))
faqs=[('How close is the gondola?','The condo is in River Run Village, less than 700 feet from the River Run Gondola. Walk through the village to reach the lift, dining and shops.'),('Where will everyone sleep?','The one-bedroom condo sleeps up to 4 adults and 1 child, with a king bed, a twin sleeper chair in the bedroom and a pull-out sofa in the living room. There is one full bathroom.'),('Is parking included?','One heated underground garage parking space and a private ski locker are included. An elevator serves the building. Additional vehicles need separate parking arrangements.'),('Where are the pool and hot tubs?','The shared hot tubs are on site at Silvermill. The year-round heated pool is accessed at nearby Dakota Lodge. All shared amenities are subject to building access and maintenance.'),('What are the check-in and check-out times?','Check-in is after 4 PM and check-out is before 10 AM. Arrival instructions are shared with confirmed guests before their stay.'),('Where can I see the rental policies?','Pricing and booking terms are shown for your selected stay. Review the rental agreement and cancellation policy before completing your reservation.')]
replace(s,'.faq > div:last-child','<div>'+''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faqs)+'</div>')
replace(s,'.site-footer > div','''<div><a href="https://www.airbnb.com/rooms/1237080165740047360" target="_blank" rel="noopener">View Airbnb listing ↗</a><a href="redhawk.html">Our other Keystone stay: Red Hawk 2240 ↗</a></div>''')
s.select_one('.site-footer > p').string='Silvermill Lodge · River Run · Keystone, Colorado'
(ROOT/'silvermill.html').write_text(str(s))
print('Built selected Alpine sites for Red Hawk and Silvermill.')

# Public domain links retain working counterparts on the GitHub Pages preview.
for filename in ('redhawk.html','silvermill.html'):
 page=BeautifulSoup((ROOT/filename).read_text(),'html.parser')
 # Reuse the current Calopi header so owner-supplied branding stays consistent.
 brand_page=BeautifulSoup((ROOT/'index.html').read_text(),'html.parser')
 header=brand_page.select_one('.haven-header')
 header['class'].append('property-header')
 property_name='Red Hawk 2240' if filename=='redhawk.html' else 'Silvermill 8294'
 identity=header.select_one('.haven-brand small')
 identity.string=property_name+' · KEYSTONE, COLORADO'
 identity['class']=['property-identity']
 header.select_one('nav').clear()
 header.select_one('nav').append(BeautifulSoup('<a href="#stay">The stay</a><a href="#gallery">Photos</a><a class="haven-outline" href="#book">Check dates ↗</a>','html.parser'))
 page.select_one('.site-header').replace_with(header)
 listing_id='45842208' if filename=='redhawk.html' else '1237080165740047360'
 header.insert_after(BeautifulSoup(f'<aside class="host-trust" aria-label="Your host and Airbnb listing"><p><span aria-hidden="true">✦</span> Hosted by Hope, an Airbnb Superhost</p><a href="https://www.airbnb.com/rooms/{listing_id}" target="_blank" rel="noopener">View {property_name} on Airbnb ↗</a></aside>','html.parser'))
 page.head.append(page.new_tag('link',rel='stylesheet',href='calopi.css'))
 page.select_one('link[rel=icon]')['href']='assets/calopi-monogram.svg'
 page.select_one('link[rel=icon]')['type']='image/svg+xml'
 for a in page.select('a[href]'):
  href=a['href']
  if href in ('redhawk.html','silvermill.html'):
   a['data-preview-path']=href
   a['href']='https://'+('redhawk2240.com' if href=='redhawk.html' else 'silvermill8294.com')+'/'
 page.select_one('.site-footer > div').append(BeautifulSoup('<a href="https://calopihaven.com/" data-preview-path="index.html">Calopi Haven · All our stays ↗</a>','html.parser'))
 (ROOT/filename).write_text(str(page))
