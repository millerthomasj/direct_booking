(() => {
  const localDate = date => `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`;
  const addDay = value => {const d=new Date(value+'T12:00:00');d.setDate(d.getDate()+1);return localDate(d)};
  const stayDialog=document.querySelector('.inquiry-dialog');
  document.querySelectorAll('.booking-form').forEach(form=>{
    const arrival=form.elements.arrival,departure=form.elements.departure,error=form.querySelector('.date-error');
    arrival.min=localDate(new Date());departure.min=addDay(arrival.min);
    arrival.addEventListener('change',()=>{departure.min=arrival.value?addDay(arrival.value):addDay(arrival.min);if(departure.value&&departure.value<departure.min)departure.value='';error.textContent=''});
    form.addEventListener('submit',event=>{
      event.preventDefault();error.textContent='';
      if(!arrival.value||!departure.value||arrival.value<arrival.min||departure.value<=arrival.value){error.textContent='Choose a future check-in date and a later check-out date.';return}
      const nights=Math.round((Date.parse(departure.value+'T12:00:00Z')-Date.parse(arrival.value+'T12:00:00Z'))/86400000);
      const format=value=>new Intl.DateTimeFormat('en-US',{month:'short',day:'numeric',year:'numeric'}).format(new Date(value+'T12:00:00'));
      const guests=Number(form.elements.guests.value);
      stayDialog.querySelector('.stay-summary').textContent=`${format(arrival.value)} – ${format(departure.value)} · ${nights} night${nights===1?'':'s'} · ${guests} guest${guests===1?'':'s'}`;
      const params=new URLSearchParams({check_in:arrival.value,check_out:departure.value,adults:String(guests)});
      stayDialog.querySelector('.airbnb-link').href='https://www.airbnb.com/rooms/45842208?'+params;
      stayDialog.showModal();
    });
  });
  const lightbox=document.querySelector('.lightbox'),photos=[...document.querySelectorAll('[data-photo]')];let active=0;
  const showPhoto=index=>{active=(index+photos.length)%photos.length;const photo=photos[active];lightbox.querySelector('img').src=photo.dataset.photo;lightbox.querySelector('img').alt=photo.dataset.caption;lightbox.querySelector('p').textContent=photo.dataset.caption};
  photos.forEach((photo,index)=>photo.addEventListener('click',()=>{showPhoto(index);lightbox.showModal()}));
  document.querySelectorAll('dialog').forEach(dialog=>{
    dialog.querySelectorAll('.dialog-close,.dialog-close-secondary').forEach(button=>button.addEventListener('click',()=>dialog.close()));
    dialog.addEventListener('click',event=>{if(event.target===dialog){const r=dialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)dialog.close()}});
  });
  lightbox?.querySelectorAll('[data-direction]').forEach(button=>button.addEventListener('click',()=>showPhoto(active+Number(button.dataset.direction))));
  lightbox?.addEventListener('keydown',event=>{if(event.key==='ArrowRight'){event.preventDefault();showPhoto(active+1)}if(event.key==='ArrowLeft'){event.preventDefault();showPhoto(active-1)}});
  const seasons={winter:{photo:'50',alt:'Snowy slopes and mountain views above Keystone',label:'MAKE TRACKS',title:'Chase the mountain.\nSkip the drive.',text:'Start with the short walk to River Run Gondola. Finish in a hot tub. Your ski-day routine just got an upgrade.'},summer:{photo:'00',alt:'Heated pool and green mountains at Red Hawk Lodge',label:'TAKE THE SCENIC ROUTE',title:'Long days.\nA little more outside.',text:'Trade ski boots for hiking shoes. Explore the trails, wander the village, and come home to a pool with a mountain backdrop.'}};
  document.querySelectorAll('[data-season]').forEach(button=>button.addEventListener('click',()=>{document.querySelectorAll('[data-season]').forEach(b=>{b.classList.toggle('active',b===button);b.setAttribute('aria-pressed',String(b===button))});const s=seasons[button.dataset.season],image=document.querySelector('.season-image');image.src=`assets/photo-${s.photo}.webp`;image.alt=s.alt;document.querySelector('.season-label').textContent=s.label;const title=document.querySelector('.season-title');title.replaceChildren();s.title.split('\n').forEach((line,i)=>{if(i)title.append(document.createElement('br'));title.append(document.createTextNode(line))});document.querySelector('.season-text').textContent=s.text}));
})();
