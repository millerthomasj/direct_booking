"""Browser checks and review captures. Run with the static preview on port 8124."""
import asyncio
from datetime import date,timedelta
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch()
  for concept in ('alpine','gatherings','summit'):
   for width,label in ((1440,'desktop'),(390,'mobile')):
    page=await browser.new_page(viewport={'width':width,'height':1000},device_scale_factor=1)
    errors=[];failures=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('response',lambda r:failures.append(r.url) if r.status>=400 else None)
    await page.goto(f'http://127.0.0.1:8124/{concept}.html',wait_until='networkidle')
    await page.evaluate('document.fonts.ready')
    await page.evaluate("document.querySelectorAll('img').forEach(i=>i.loading='eager')")
    await page.wait_for_function('Array.from(document.images).every(i=>!i.src||i.complete)')
    assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(concept,label,'overflow')
    assert await page.locator('img[src]').evaluate_all('(images)=>images.every(i=>i.naturalWidth>0)'),(concept,label,'image')
    await page.screenshot(path=str(ROOT/f'previews/{concept}-{label}.jpg'),type='jpeg',quality=90)
    await page.screenshot(path=str(ROOT/f'previews/{concept}-{label}-full.jpg'),type='jpeg',quality=85,full_page=True)
    await page.locator('.gallery-grid [data-photo]').first.click()
    assert await page.locator('.lightbox').evaluate('(d)=>d.open')
    old=await page.locator('.lightbox img').get_attribute('src')
    await page.keyboard.press('ArrowRight');assert await page.locator('.lightbox img').get_attribute('src')!=old
    await page.keyboard.press('Escape');assert not await page.locator('.lightbox').evaluate('(d)=>d.open')
    arrival=(date.today()+timedelta(days=30)).isoformat();departure=(date.today()+timedelta(days=34)).isoformat()
    await page.locator('[name=arrival]').fill(arrival)
    await page.locator('[name=departure]').fill(departure)
    await page.locator('[name=guests]').select_option('6')
    await page.locator('.booking-form button').click()
    assert '4 nights · 6 guests' in await page.locator('.stay-summary').inner_text()
    assert f'check_in={arrival}' in await page.locator('.airbnb-link').get_attribute('href')
    assert 'does not check availability' in await page.locator('.inquiry-dialog').inner_text()
    await page.keyboard.press('Escape')
    await page.locator('[name=arrival]').fill((date.today()+timedelta(days=40)).isoformat())
    assert await page.locator('[name=departure]').input_value()==''
    await page.locator('.faq summary').first.click();assert await page.locator('.faq details').first.get_attribute('open') is not None
    if concept=='summit':
     await page.locator('[data-season=summer]').click();assert await page.locator('[data-season=summer]').get_attribute('aria-pressed')=='true';assert 'Long days.' in await page.locator('.season-title').inner_text();assert 'photo-00' in await page.locator('.season-image').get_attribute('src')
    assert not errors,(concept,label,errors)
    assert not failures,(concept,label,failures)
    await page.close()
  page=await browser.new_page(viewport={'width':1440,'height':1100})
  await page.goto('http://127.0.0.1:8124/',wait_until='networkidle')
  await page.screenshot(path=str(ROOT/'previews/comparison.jpg'),type='jpeg',quality=90,full_page=True)
  for link in ('alpine.html','gatherings.html','summit.html'):assert await page.locator(f'a[href="{link}"]').count()==1
  await page.set_viewport_size({'width':390,'height':844});assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  await browser.close()
 print('PASS: six desktop/mobile concept flows; local photos/fonts; galleries; keyboard close; dates, guests and summaries; FAQ; seasons; comparison navigation.')
if __name__=='__main__':asyncio.run(main())
