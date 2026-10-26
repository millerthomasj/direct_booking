"""Package the three static domains with the appropriate root page."""
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parents[1]
for domain,page in [('calopihaven.com','index.html'),('redhawk2240.com','redhawk.html'),('silvermill8294.com','silvermill.html')]:
 target=ROOT/'dist'/domain
 if target.exists():shutil.rmtree(target)
 target.mkdir(parents=True)
 shutil.copytree(ROOT/'assets',target/'assets')
 for name in ['styles.css','calopi.css','site.js']:shutil.copy2(ROOT/name,target/name)
 shutil.copy2(ROOT/page,target/'index.html')
 print(domain, '<-',page)
