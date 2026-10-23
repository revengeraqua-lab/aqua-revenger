// Horizontal model inspection: right/left drag, touch swipe, or keyboard.
// Native vertical touch scrolling and wheel-driven storytelling stay available.
export function attachBottleRotation(canvas,{stage,isEnabled,onChange}) {
  let angle=0,drag=null;
  const reset=stage.querySelector('.rotation-reset');
  const hint=stage.querySelector('.rotation-hint');
  const publish=()=>{reset.hidden=Math.abs(angle)<.001;onChange();};
  function finish(event) {
    if(!drag || (event && event.pointerId!==drag.id))return;
    if(canvas.hasPointerCapture(drag.id))canvas.releasePointerCapture(drag.id);
    drag=null;stage.classList.remove('is-rotating');
  }
  canvas.addEventListener('pointerdown',event=>{
    if(!isEnabled() || ![0,2].includes(event.button) || drag)return;
    drag={id:event.pointerId,x:event.clientX,startX:event.clientX,startY:event.clientY,pending:event.pointerType==='touch'};
    canvas.setPointerCapture(event.pointerId);
    if(event.pointerType!=='touch'){event.preventDefault();canvas.focus({preventScroll:true});stage.classList.add('is-rotating');}
  });
  canvas.addEventListener('pointermove',event=>{
    if(!drag || drag.id!==event.pointerId)return;
    if(!isEnabled()){finish(event);return;}
    if(drag.pending) {
      const dx=Math.abs(event.clientX-drag.startX),dy=Math.abs(event.clientY-drag.startY);
      if(dy>8 && dy>dx){finish(event);return;}
      if(dx<8)return;
      drag.pending=false;stage.classList.add('is-rotating');
    }
    if(event.cancelable)event.preventDefault();
    angle+=(event.clientX-drag.x)*Math.PI*2/Math.max(240,stage.clientWidth*.55);
    drag.x=event.clientX;publish();
  });
  for(const type of ['pointerup','pointercancel','lostpointercapture'])canvas.addEventListener(type,finish);
  canvas.addEventListener('contextmenu',event=>{if(isEnabled())event.preventDefault();});
  canvas.addEventListener('keydown',event=>{
    if(!isEnabled())return;
    if(event.key==='ArrowLeft' || event.key==='ArrowRight') {
      event.preventDefault();angle+=(event.key==='ArrowRight'?1:-1)*Math.PI/12;publish();
    }else if(event.key==='Home'){event.preventDefault();angle=0;publish();}
  });
  reset.addEventListener('click',()=>{angle=0;publish();canvas.focus({preventScroll:true});});
  return {
    get angle(){return angle;},
    get dragging(){return Boolean(drag && !drag.pending);},
    sync(enabled){canvas.tabIndex=enabled?0:-1;stage.classList.toggle('can-rotate',enabled);hint.hidden=!enabled;reset.hidden=!enabled||Math.abs(angle)<.001;},
  };
}
