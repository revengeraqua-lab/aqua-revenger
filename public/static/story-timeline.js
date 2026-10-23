import { gsap } from './vendor/gsap/index.js';

// Scroll seeks one paused timeline. Object, camera, scenery and chapter copy
// share the same playhead, so none of the layers drift or run on a timer.
export function createStoryTimeline() {
  const state={roots:1,paper:0,arrival:0,open:0,tilt:0,flow:0,glass:0,fill:0,lineup:0,zoom:0,turn:-.25};
  const timeline=gsap.timeline({paused:true,defaults:{ease:'sine.inOut'}});
  timeline.addLabel('roots',0)
    .to(state,{turn:.08,duration:16},'roots')
    .addLabel('introduce',16)
    .to(state,{roots:0,paper:1,arrival:1,turn:.12,duration:12},'introduce')
    .to(state,{turn:-.09,duration:10},28)
    .addLabel('open',39)
    .to(state,{paper:0,zoom:1,turn:.02,duration:9},'open')
    .to(state,{open:1,duration:12,ease:'none'},43)
    .addLabel('refresh',59)
    .to(state,{zoom:0,tilt:1,glass:1,duration:10},'refresh')
    .to(state,{flow:1,duration:4},68)
    .to(state,{fill:1,duration:12,ease:'none'},70)
    .to(state,{flow:0,duration:4},81)
    .addLabel('everyday',85)
    .to(state,{tilt:0,open:0,glass:0,paper:1,lineup:1,turn:0,duration:12},'everyday')
    .to(state,{duration:3},97);
  return {state,timeline};
}
