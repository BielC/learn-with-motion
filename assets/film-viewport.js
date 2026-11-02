// Layout and optional detail navigation. Playback remains owned by lessonInspection.
(() => {
  const app=document.querySelector('.motion-app'),stage=app.querySelector('.stage'),film=app.querySelector('.film');
  const portrait=matchMedia('(max-width:760px) and (min-height:500px)');
  function fit(){
    if(document.body.classList.contains('export'))return;
    const {width,height}=stage.getBoundingClientRect();
    const w=portrait.matches?width:Math.min(width,height*16/9);
    film.style.width=`${Math.max(1,w)}px`;
    film.style.height=`${Math.max(1,portrait.matches?height:w*9/16)}px`;
  }
  const observer=new ResizeObserver(fit);observer.observe(stage);portrait.addEventListener('change',fit);fit();
  const menus=[...app.querySelectorAll('.menu')];
  menus.forEach(menu=>menu.addEventListener('toggle',()=>{if(menu.open)menus.filter(m=>m!==menu).forEach(m=>m.open=false)}));
  document.addEventListener('click',e=>{menus.filter(m=>!m.contains(e.target)).forEach(m=>m.open=false)});
  document.addEventListener('keydown',e=>{if(e.key==='Escape')menus.forEach(m=>m.open=false)});
  const chapterMenu=document.getElementById('chapter-menu');
  document.getElementById('chapters')?.addEventListener('click',e=>{
    if(chapterMenu&&e.target.closest('button')){chapterMenu.open=false;chapterMenu.querySelector('summary').focus()}
  });
  const dialog=document.getElementById('resource-dialog'),title=document.getElementById('resource-title');
  let returnFocus=null;
  document.addEventListener('keydown',e=>{
    if(dialog?.open&&['Space','ArrowLeft','ArrowRight'].includes(e.code))e.stopPropagation();
  },true);
  const names={explore:'Explore the mechanism',code:'Connect to the code',sources:'Source and scope',transcript:'Full explanation'};
  function openPanel(name){
    if(!dialog||!title)return;
    if(!dialog.open){const focused=document.activeElement;returnFocus=focused.closest('.menu')?.querySelector('summary')||focused}
    window.lessonInspection.pause();
    app.querySelectorAll('.resource-panel').forEach(panel=>panel.hidden=panel.id!==`resource-${name}`);
    dialog.querySelectorAll('[data-panel]').forEach(b=>b.toggleAttribute('aria-current',b.dataset.panel===name));
    title.textContent=names[name];
    dialog.querySelector('.resource-body').scrollTop=0;
    menus.forEach(m=>m.open=false);
    if(!dialog.open)dialog.showModal();
  }
  app.querySelectorAll('[data-panel]').forEach(b=>b.addEventListener('click',()=>openPanel(b.dataset.panel)));
  document.getElementById('close-resources')?.addEventListener('click',()=>dialog.close());
  dialog?.addEventListener('close',()=>returnFocus?.focus());
  document.getElementById('transcript')?.addEventListener('click',e=>{if(e.target.closest('button'))dialog.close()});
  document.getElementById('fullscreen')?.addEventListener('click',async()=>{
    try{if(document.fullscreenElement)await document.exitFullscreen();else await app.requestFullscreen()}
    catch{const message=document.getElementById('playback-error');if(message){message.hidden=false;message.textContent='Full screen is unavailable in this browser.'}}
  });
  document.addEventListener('fullscreenchange',()=>{document.getElementById('fullscreen')?.setAttribute('aria-pressed',String(!!document.fullscreenElement));fit()});
})();
