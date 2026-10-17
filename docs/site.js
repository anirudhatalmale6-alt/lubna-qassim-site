/* Lubna Qassim — draft v2 */
(function(){
  var b=document.body;
  // mobile menu
  var menu=document.querySelector('.menu'), nav=document.getElementById('nav');
  if(menu&&nav) menu.addEventListener('click',function(){var o=nav.classList.toggle('open');menu.setAttribute('aria-expanded',o);menu.textContent=o?'Close':'Menu';});

  // homepage opening: portrait alone, settles, glides to its place, then the words. Once per visit.
  if(b.classList.contains('home')){
    var ph=document.querySelector('.ph'), img=ph&&ph.querySelector('img');
    var reduce=matchMedia('(prefers-reduced-motion:reduce)').matches, seen=false, timers=[];
    try{seen=sessionStorage.getItem('lq-opening')==='1';}catch(e){}
    function finish(){timers.forEach(clearTimeout);timers=[];ph.style.transform='';img.style.transform='';img.style.opacity='';b.classList.add('lift');}
    function run(){
      if(reduce||seen){return;}
      try{sessionStorage.setItem('lq-opening','1');}catch(e){}
      ph.style.transition='none';img.style.transition='none';scrollTo(0,0);
      var r=ph.getBoundingClientRect(), vw=innerWidth, vh=innerHeight;
      var s=Math.min(1.25,(vh*.9)/r.height,(vw*.94)/r.width);
      ph.style.transform='translate('+(vw/2-(r.left+r.width/2))+'px,'+(vh/2-(r.top+r.height/2))+'px) scale('+s+')';
      img.style.transform='scale(1.12)';img.style.opacity='0';void ph.offsetWidth;
      b.classList.add('intro');ph.style.transition='';img.style.transition='';
      timers.push(setTimeout(function(){img.style.opacity='1';img.style.transform='scale(1)';},150));
      timers.push(setTimeout(function(){ph.style.transform='';},2600));
      timers.push(setTimeout(function(){b.classList.add('lift');},3500));
      addEventListener('pointerdown',function(){if(!b.classList.contains('lift'))finish();},{once:true});
      addEventListener('keydown',function(){if(!b.classList.contains('lift'))finish();},{once:true});
    }
    if(img){ if(img.complete) run(); else img.addEventListener('load',run); }
  }

  // recognition slider
  var rec=document.getElementById('rec');
  document.querySelectorAll('.sliderctl button').forEach(function(btn){
    btn.addEventListener('click',function(){rec.scrollBy({left:(+btn.dataset.dir)*320,behavior:'smooth'});});
  });

  // map: play once when it scrolls into view
  var mb=document.getElementById('mapband');
  if(mb){var svg=mb.querySelector('svg');
    var startMap=function(){svg.classList.add('play');
      if(matchMedia('(prefers-reduced-motion:reduce)').matches) return;
      // arrows and glows are SVG (SMIL) animations: they run in Safari as well as Chrome
      svg.querySelectorAll('animate,animateMotion').forEach(function(a){try{a.beginElementAt(+a.getAttribute('data-at'));}catch(e){}});};
    if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){startMap();io.disconnect();}});},{threshold:.3});io.observe(mb);}
    else startMap();}

  // contact: preset the enquiry type from ?subject=, and a draft-only submit
  var form=document.getElementById('enquiry');
  if(form){
    var m=location.search.match(/subject=([a-z]+)/), sel=document.getElementById('subject');
    if(m&&sel.querySelector('option[value="'+m[1]+'"]')) sel.value=m[1];
    form.addEventListener('submit',function(e){e.preventDefault();
      document.getElementById('formnote').textContent='Draft preview: in the finished site this sends your message to Lubna directly.';});
  }
})();
