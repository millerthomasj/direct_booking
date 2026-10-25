"""Make a four-page, shareable design review from browser captures."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'previews';W,H=1800,1250
FONT='/System/Library/Fonts/Supplemental/Arial.ttf';BOLD='/System/Library/Fonts/Supplemental/Arial Bold.ttf';SERIF='/System/Library/Fonts/Supplemental/Georgia.ttf'
def font(size,bold=False):return ImageFont.truetype(BOLD if bold else FONT,size)
def text(im,xy,value,size=20,fill='#263c33',bold=False):ImageDraw.Draw(im).text(xy,value,font=font(size,bold),fill=fill)
def fitted(im,path,box):
 image=Image.open(path).convert('RGB');image.thumbnail((box[2],box[3]));im.paste(image,(box[0],box[1]))
pages=[]
cover=Image.new('RGB',(W,H),'#f5f3ec');text(cover,(80,65),'RED HAWK 2240  /  KEYSTONE, COLORADO',20,bold=True);text(cover,(80,130),'Three ways to come home to the mountains.',51,bold=True);text(cover,(80,215),'Direct-booking website concepts · October 2026 · Actual property photography',23)
concepts=[('alpine','01  THE ALPINE EDIT','Refined · Forest green + ivory · Photo-led','A quiet, elevated mountain retreat.'),('gatherings','02  THE GATHERING PLACE','Welcoming · Terracotta + teal · Family-first','Warm, colorful and full of personality.'),('summit','03  BASECAMP 2240','Bold · Charcoal + alpine lime · Adventure-first','An energetic home base for mountain days.')]
for i,(key,title,palette,note) in enumerate(concepts):
 x=80+i*565;text(cover,(x,310),title,22,bold=True);shot=Image.open(OUT/f'{key}-desktop.jpg');shot=ImageOps.fit(shot,(515,470),centering=(.5,0));cover.paste(shot,(x,365));text(cover,(x,870),palette,17);text(cover,(x,910),note,19)
text(cover,(80,1020),'My recommendation: The Alpine Edit for the strongest independent hospitality brand.',24,bold=True);text(cover,(80,1080),'All three include responsive pages, photo galleries and a stay-planning preview.',21);text(cover,(80,1120),'Live availability, prices, direct reservations and payments are not connected.',21);pages.append(cover)
for key,title,palette,note in concepts:
 im=Image.new('RGB',(W,H),'#f5f3ec');text(im,(65,48),title,39,bold=True);text(im,(65,110),palette+'  /  '+note,22);text(im,(65,175),'DESKTOP',14,bold=True);text(im,(1390,175),'MOBILE',14,bold=True)
 fitted(im,OUT/f'{key}-desktop.jpg',(65,215,1270,885));fitted(im,OUT/f'{key}-mobile.jpg',(1390,215,345,885));text(im,(65,1155),'Open the interactive concept to browse the full page and try the galleries and stay planner.',22);pages.append(im)
pages[0].save(OUT/'Red-Hawk-2240-design-review.pdf',save_all=True,append_images=pages[1:],resolution=150)
print('Built four-page review PDF.')
if __name__=='__main__':pass
