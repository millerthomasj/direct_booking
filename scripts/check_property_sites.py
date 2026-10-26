"""Check the selected Alpine sites and their property-specific booking handoffs."""
import asyncio
from datetime import date,timedelta
from pathlib import Path
from urllib.parse import urlparse,parse_qs
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch()
  for name,key,guests in [('redhawk','bc7244c04d284b70baab4dede8d52fb0',6),('silvermill','3f15f3b1b0f548328ab5276d7014358a',5)]:
   for width in [1440,390,320]:
    page=await b.new_page(viewport={'width':width,'height':1000});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    await page.goto(f'http://127.0.0.1:8124/{name}.html',wait_until='networkidle')
    await page.evaluate("document.images&&Array.from(document.images).forEach(i=>i.loading='eager')")
    await page.wait_for_function('Array.from(document.images).every(i=>!i.getAttribute("src")||(i.complete&&i.naturalWidth>0))')
    assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(name,width,'overflow')
    if name=='redhawk':assert await page.locator('[name=or_guests] option').count()==guests
    else:
     assert await page.locator('[name=or_adults] option').count()==4
     assert await page.locator('[name=or_children] option').evaluate_all('(options)=>options.map(o=>o.value)')==['0','1']
    assert await page.locator('.concept-bar').count()==0
    header=page.locator('.property-header')
    assert await header.locator('.haven-brand').is_visible()
    assert await header.locator('img.calopi-logo').count()==0
    assert ('Red Hawk 2240' if name=='redhawk' else 'Silvermill 8294') in await header.locator('.property-identity').inner_text()
    assert await header.locator('.property-identity').is_visible()
    assert await header.locator('a[data-preview-path="index.html"]').get_attribute('href')=='index.html'
    if name=='silvermill':
     assert await page.locator('img[src*="assets/photo-"]').count()==0
     assert await page.locator('a[href*="checkin."]').count()==0
    await page.locator('.gallery-grid .photo').first.click();assert await page.locator('.lightbox').evaluate('(d)=>d.open');await page.keyboard.press('ArrowRight');await page.keyboard.press('Escape')
    await page.locator('.faq summary').first.click()
    arrival=(date.today()+timedelta(days=42)).isoformat();departure=(date.today()+timedelta(days=46)).isoformat()
    await page.locator('[name=or_arrival]').fill(arrival);await page.locator('[name=or_departure]').fill(departure)
    if name=='redhawk':await page.locator('[name=or_guests]').select_option(str(guests))
    else:
     await page.locator('[name=or_adults]').select_option('4');await page.locator('[name=or_children]').select_option('1')
    await page.context.route('https://app.ownerrez.com/widgets/**',lambda route:route.fulfill(body='Booking handoff verified',content_type='text/html'))
    await page.locator('.booking-form button').click()
    dialog=page.locator('.booking-dialog')
    assert await dialog.evaluate('(e)=>e.open')
    frame_url=await dialog.locator('iframe').get_attribute('src')
    q=parse_qs(urlparse(frame_url).query);assert q['propertyKey']==[key] and q['or_arrival']==[arrival]
    assert 'view' not in q
    if name=='redhawk':assert q['or_guests']==[str(guests)]
    else:assert q['or_adults']==['4'] and q['or_children']==['1']
    await dialog.locator('.dialog-close').click()
    assert not await dialog.evaluate('(e)=>e.open')
    await page.locator('[data-booking-window]').click()
    assert await dialog.evaluate('(e)=>e.open')
    q=parse_qs(urlparse(await dialog.locator('iframe').get_attribute('src')).query)
    assert 'or_arrival' not in q and q['propertyKey']==[key]
    await page.keyboard.press('Escape')
    assert not await dialog.evaluate('(e)=>e.open')
    assert page.url.endswith(name+'.html')
    await page.screenshot(path=str(ROOT/f'previews/{name}-{width}.jpg'),type='jpeg',quality=85,full_page=True)
    assert not errors,errors
    await page.close()
  await b.close()
 print('PASS: both properties at desktop, mobile and 320px; photos, galleries, FAQs, property-specific OwnerRez date/guest handoff.')
if __name__=='__main__':asyncio.run(main())
