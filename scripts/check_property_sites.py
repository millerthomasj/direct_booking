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
  for name,key,guests in [('index','bc7244c04d284b70baab4dede8d52fb0',6),('silvermill','3f15f3b1b0f548328ab5276d7014358a',5)]:
   for width in [1440,390,320]:
    page=await b.new_page(viewport={'width':width,'height':1000});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    await page.goto(f'http://127.0.0.1:8124/{name}.html',wait_until='networkidle')
    await page.evaluate("document.images&&Array.from(document.images).forEach(i=>i.loading='eager')")
    await page.wait_for_function('Array.from(document.images).every(i=>!i.getAttribute("src")||(i.complete&&i.naturalWidth>0))')
    assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(name,width,'overflow')
    if name=='index':assert await page.locator('[name=or_guests] option').count()==guests
    else:assert await page.locator('[name=or_adults] option').count()==4
    assert await page.locator('.concept-bar').count()==0
    if name=='silvermill':
     assert await page.locator('img[src*="assets/photo-"]').count()==0
     assert await page.locator('a[href="http://checkin.silvermill8294.com/"]').count()==1
    await page.locator('.gallery-grid .photo').first.click();assert await page.locator('.lightbox').evaluate('(d)=>d.open');await page.keyboard.press('ArrowRight');await page.keyboard.press('Escape')
    await page.locator('.faq summary').first.click()
    arrival=(date.today()+timedelta(days=42)).isoformat();departure=(date.today()+timedelta(days=46)).isoformat()
    await page.locator('[name=or_arrival]').fill(arrival);await page.locator('[name=or_departure]').fill(departure)
    if name=='index':await page.locator('[name=or_guests]').select_option(str(guests))
    else:
     await page.locator('[name=or_adults]').select_option('4');await page.locator('[name=or_children]').select_option('1')
    await page.route('https://app.ownerrez.com/widgets/**',lambda route:route.fulfill(body='Booking handoff verified',content_type='text/html'))
    async with page.expect_navigation():await page.locator('.booking-form button').click()
    q=parse_qs(urlparse(page.url).query);assert q['propertyKey']==[key] and q['or_arrival']==[arrival]
    if name=='index':assert q['or_guests']==[str(guests)]
    else:assert q['or_adults']==['4'] and q['or_children']==['1']
    await page.go_back();await page.screenshot(path=str(ROOT/f'previews/{name}-{width}.jpg'),type='jpeg',quality=85,full_page=True)
    assert not errors,errors
    await page.close()
  await b.close()
 print('PASS: both properties at desktop, mobile and 320px; photos, galleries, FAQs, property-specific OwnerRez date/guest handoff.')
if __name__=='__main__':asyncio.run(main())
