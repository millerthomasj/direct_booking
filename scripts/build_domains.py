"""Package the three static domains with the appropriate root page."""
from pathlib import Path
import shutil
import argparse
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--production',action='store_true',help='Enable indexing and add per-domain canonical, social and sitemap metadata')
args=parser.parse_args()
for domain,page in [('calopihaven.com','index.html'),('redhawk2240.com','redhawk.html'),('silvermill8294.com','silvermill.html')]:
 target=ROOT/'dist'/domain
 if target.exists():shutil.rmtree(target)
 target.mkdir(parents=True)
 shutil.copytree(ROOT/'assets',target/'assets')
 for name in ['styles.css','calopi.css','site.js']:shutil.copy2(ROOT/name,target/name)
 shutil.copy2(ROOT/page,target/'index.html')
 if args.production:
  document=BeautifulSoup((target/'index.html').read_text(),'html.parser')
  document.select_one('meta[name=robots]').decompose()
  canonical='https://'+domain+'/'
  document.head.append(document.new_tag('link',rel='canonical',href=canonical))
  image='assets/keystone-schoolmarm.webp' if domain=='calopihaven.com' else 'assets/photo-00.webp' if domain=='redhawk2240.com' else 'assets/silvermill/81.webp'
  for key,value in {'og:type':'website','og:url':canonical,'og:title':document.title.text,'og:description':document.select_one('meta[name=description]')['content'],'og:image':canonical+image,'twitter:card':'summary_large_image'}.items():
   tag=document.new_tag('meta',attrs={'property' if key.startswith('og:') else 'name':key,'content':value});document.head.append(tag)
  for anchor in document.select('a[href]'):
   if anchor['href'].startswith('http://checkin.'):anchor['href']=anchor['href'].replace('http://','https://',1)
  (target/'index.html').write_text(str(document))
  (target/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+canonical+'sitemap.xml\n')
  (target/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>'+canonical+'</loc></url></urlset>\n')
 print(domain, '<-',page)
