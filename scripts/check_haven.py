"""Check Calopi Haven responsive layout, property links, and domain behavior."""
import asyncio,mimetypes
from pathlib import Path
from urllib.parse import urlparse,parse_qs
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch()
  for width in [1440,768,390,320]:
   page=await browser.new_page(viewport={'width':width,'height':1000});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   await page.goto('http://127.0.0.1:8124/',wait_until='networkidle')
   await page.evaluate("Array.from(document.images).forEach(i=>i.loading='eager')")
   await page.wait_for_function('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)')
   assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
   assert await page.locator('.haven-property').count()==2
   for filename in ['redhawk.html','silvermill.html']:
    assert await page.locator(f'a[data-preview-path="{filename}"]').first.get_attribute('href')==filename
    await page.locator(f'.haven-property-actions a[href="{filename}"]').click()
    assert await page.locator('.booking-form').count()==1
    key=await page.locator('[name=propertyKey]').input_value()
    assert key==('bc7244c04d284b70baab4dede8d52fb0' if filename=='redhawk.html' else '3f15f3b1b0f548328ab5276d7014358a')
    await page.locator('a[data-preview-path="index.html"]').first.click()
    assert await page.locator('.haven-property').count()==2
   # Exercise the photo controls and reveal all content before capturing previews.
   slider=page.locator('[data-slider]')
   await slider.locator('[data-next]').click()
   assert await slider.get_attribute('data-active-slide')=='1'
   assert 'RED HAWK' in await slider.locator('.slider-caption').inner_text()
   await slider.press('ArrowRight')
   assert await slider.get_attribute('data-active-slide')=='2'
   await slider.locator('[data-prev]').click()
   assert await slider.get_attribute('data-active-slide')=='1'
   await slider.locator('.slider-dots button').first.click()
   assert await slider.get_attribute('data-active-slide')=='0'
   await slider.locator('[data-pause]').click()
   assert await slider.locator('[data-pause]').get_attribute('aria-pressed')=='true'
   for y in range(0,await page.evaluate('document.documentElement.scrollHeight'),650):
    await page.evaluate('(y)=>window.scrollTo({top:y,behavior:"instant"})',y)
    await page.wait_for_timeout(100)
   await page.evaluate('window.scrollTo({top:0,behavior:"instant"})')
   await page.wait_for_timeout(1000)
   assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
   await page.screenshot(path=str(ROOT/f'previews/calopi-{width}.jpg'),type='jpeg',quality=88,full_page=True)
   assert not errors,errors
   await page.close()
  # Autoplay advances and respects an explicit pause; reduced motion starts static.
  page=await browser.new_page()
  await page.goto('http://127.0.0.1:8124/',wait_until='networkidle')
  await page.wait_for_function('document.querySelector("[data-slider]").dataset.activeSlide === "1"',timeout=8500)
  await page.locator('[data-pause]').click()
  await page.mouse.move(0,0)
  await page.locator('[data-pause]').evaluate('(e)=>e.blur()')
  await page.wait_for_timeout(6800)
  assert await page.locator('[data-slider]').get_attribute('data-active-slide')=='1'
  await page.close()
  page=await browser.new_page(reduced_motion='reduce')
  await page.goto('http://127.0.0.1:8124/',wait_until='networkidle')
  assert await page.locator('[data-pause]').is_hidden()
  assert await page.locator('.slider-track').evaluate('(e)=>getComputedStyle(e).transitionDuration')=='0s'
  await page.wait_for_timeout(6800)
  assert await page.locator('[data-slider]').get_attribute('data-active-slide')=='0'
  await page.locator('[data-next]').click()
  assert await page.locator('[data-slider]').get_attribute('data-active-slide')=='1'
  await page.close()
  # Serve the prepared files under their production hostnames without changing DNS.
  page=await browser.new_page()
  async def serve(route):
   u=urlparse(route.request.url);path=ROOT/'dist'/u.hostname/(u.path.lstrip('/') or 'index.html')
   await route.fulfill(path=str(path),content_type=mimetypes.guess_type(str(path))[0] or 'application/octet-stream')
  await page.route('https://calopihaven.com/**',serve)
  await page.route('https://redhawk2240.com/**',serve)
  await page.route('https://silvermill8294.com/**',serve)
  await page.goto('https://calopihaven.com/')
  for domain in ['redhawk2240.com','silvermill8294.com']:
   link=page.locator(f'.haven-property-actions a[href="https://{domain}/"]')
   await link.click();assert urlparse(page.url).hostname==domain
   assert await page.locator('.booking-form').count()==1
   await page.locator('a[href="https://calopihaven.com/"]').first.click()
  await browser.close()
 print('PASS: Calopi at 1440/768/390/320px, both preview property journeys, both production domain journeys, correct OwnerRez properties, slider controls, autoplay, pause and reduced motion.')
if __name__=='__main__':asyncio.run(main())
