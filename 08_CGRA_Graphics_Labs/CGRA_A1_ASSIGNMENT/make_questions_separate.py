# -*- coding: utf-8 -*-
"""
CGRA A1 — QUESTIONS only (clean view + attractive colors)
Does NOT touch old notebooks/ files — only notebooks/QUESTIONS/
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "notebooks" / "QUESTIONS"
OUT.mkdir(parents=True, exist_ok=True)
SHAPES = (ROOT / "js" / "shapes_basic.js").read_text(encoding="utf-8")

LIBS = """
<script src="https://is3l.isr.uc.pt/~pm/CGRA/JS/deecshader.js"></script>
<script src="https://is3l.isr.uc.pt/~pm/CGRA/JS/deecapp.js"></script>
<script src="https://is3l.isr.uc.pt/~pm/CGRA/JS/cgraobject.js"></script>
<script src="https://git.io/glm-js.min.js"></script>
"""

VERT = """
<script id="my-vertex-shader" type="x-shader/x-vertex">
precision mediump float;
attribute vec3 in_Position;
attribute vec3 in_Color;
uniform mat4 MVP;
varying vec3 ex_Color;
void main(void){
  gl_Position = MVP * vec4(in_Position.x, in_Position.y, in_Position.z, 1.0);
  ex_Color = in_Color;
}
</script>
"""

FRAG = """
<script id="my-fragment-shader" type="x-shader/x-fragment">
precision mediump float;
varying vec3 ex_Color;
void main(void){ gl_FragColor = vec4(ex_Color, 1.0); }
</script>
"""

BOOT = r"""
<div id="cgraStatus" style="font:13px/1.4 system-ui,sans-serif;color:#0a7;min-height:1.2em;"></div>
<script>
function cgraReady(){
  return typeof DEECapp!=='undefined' && typeof DEECshader!=='undefined'
      && typeof CGRAobject!=='undefined' && typeof glm!=='undefined';
}
function cgraBoot(fn){
  var n=0;
  (function wait(){
    n++;
    if(!cgraReady()){
      if(n===30){ var e=document.getElementById('cgraStatus'); if(e){ e.style.color='#c60'; e.textContent='Waiting libraries...'; } }
      if(n<250) return setTimeout(wait,40);
      var e2=document.getElementById('cgraStatus'); if(e2){ e2.style.color='#c00'; e2.textContent='ERROR: libs not loaded (F12)'; }
      return;
    }
    var e3=document.getElementById('cgraStatus'); if(e3) e3.textContent='';
    try{ fn(); }catch(err){ console.error(err); alert('Error: '+err.message); }
  })();
}
</script>
"""

HELPERS = r"""
function T(x,y,z){ return glm.translate(glm.mat4(1.0), glm.vec3(x,y,z)); }
function Rdeg(deg,x,y,z){ return glm.rotate(glm.mat4(1.0), glm.radians(deg), glm.vec3(x,y,z)); }
function Su(s){ return glm.mat4(glm.mat3(s)); }
function mul2(a,b){ return a['*'](b); }
function mul3(a,b,c){ return a['*'](b['*'](c)); }
function mul4(a,b,c,d){ return a['*'](b['*'](c['*'](d))); }
function makeShader(app){
  var fs=document.getElementById('my-fragment-shader').text;
  var vs=document.getElementById('my-vertex-shader').text;
  app.shaderprog=new DEECshader(app.gl);
  app.shaderprog.srcShaders(vs,fs);
  app.gl.enable(app.gl.DEPTH_TEST);
}
function setSh(obj, app){ obj.setShader(app.shaderprog); }
function draw(obj, M){ obj.setModelTransformation(M); obj.drawit(); }
function drawVP(obj, M, view, proj){ obj.setModelTransformation(M); obj.drawit(view, proj); }
"""


def md(text):
    if not text.endswith("\n"):
        text += "\n"
    return {"cell_type": "markdown", "metadata": {}, "source": [l + "\n" for l in text.split("\n")]}


def code(text):
    if not text.endswith("\n"):
        text += "\n"
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [l + "\n" for l in text.split("\n")],
    }


def save(name, cells):
    nb = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "cells": cells,
    }
    (OUT / name).write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding="utf-8")
    print("OK", name)


def page(canvas_id, js, tip, w=720, h=460):
    return f"""%%html
{LIBS}
{VERT}
{FRAG}
{BOOT}
<div style="font:14px/1.45 system-ui,sans-serif;color:#243;margin:0 0 8px 0;max-width:{w}px;">
  {tip}<br>
  <span style="color:#666;">Voilà only (not Run). Click canvas before keys.</span>
</div>
<canvas id="{canvas_id}" width="{w}" height="{h}"
  style="border:1px solid #2a3340;border-radius:8px;background:#1a2230;display:block;box-shadow:0 8px 24px rgba(0,0,0,.18);"></canvas>
<script>
cgraBoot(function(){{
{js}
}});
</script>
"""


# ===================== Q1 =====================
Q1 = SHAPES + HELPERS + r"""
class myapp extends DEECapp{
  counter=0;
  initialize(){
    makeShader(this);
    // soft sky
    this.gl.clearColor(0.62, 0.78, 0.95, 1);
    // ATTRACTIVE colors: [color1, color2] = gradient left->right
    this.shapes=[
      new Cube(this.gl,     [0.95,0.35,0.35], [0.35,0.45,0.95]),   // coral -> blue
      new Sphere(this.gl,   [0.20,0.85,0.95], [0.95,0.35,0.75],12,12), // cyan -> pink
      new Cylinder(this.gl, [0.95,0.80,0.25], [0.90,0.40,0.15],12), // gold -> orange
      new Cone(this.gl,     [0.55,0.90,0.40], [0.15,0.55,0.35],12), // lime -> green
      new Disc(this.gl,     [0.95,0.55,0.85], [0.55,0.30,0.95],12)  // pink -> violet
    ];
    this.ground = new Disc(this.gl, [0.45,0.70,0.40], [0.25,0.50,0.30], 24);
    for(var i=0;i<this.shapes.length;i++) setSh(this.shapes[i], this);
    setSh(this.ground, this);
  }
  render(){
    this.gl.clear(this.gl.COLOR_BUFFER_BIT|this.gl.DEPTH_BUFFER_BIT);
    this.counter++;
    // clean ground plate
    draw(this.ground, mul3(T(0,-0.42,0), Rdeg(90,1,0,0), Su(1.15)));
    // OVERLAP FIX:
    // xs = har shape ka X position (door rakho = gap zyada)
    // Su(s) = size (chota number = choti shape, overlap kam)
    var xs=[-0.80,-0.40,0.0,0.40,0.80];
    for(var i=0;i<5;i++){
      var rot=Rdeg(this.counter*0.45, 0.2,1,0.12);
      if(i===4) rot=mul2(rot, Rdeg(78,1,0,0));
      draw(this.shapes[i], mul3(T(xs[i], 0.05, 0), rot, Su(0.14)));
    }
  }
}
new myapp('cQ1').run();
"""

# ===================== Q2 =====================
Q2 = SHAPES + HELPERS + r"""
class myapp extends DEECapp{
  counter=0; wheelMode=0;
  initialize(){
    makeShader(this);
    this.gl.clearColor(0.55, 0.72, 0.88, 1);
    this.ground=new Disc(this.gl,[0.42,0.62,0.35],[0.28,0.48,0.25],28);
    this.wood=new Cube(this.gl,[0.72,0.48,0.22],[0.40,0.22,0.08]);      // warm oak
    this.metal=new Cube(this.gl,[0.55,0.60,0.70],[0.25,0.28,0.35]);     // steel
    this.ram=new Cone(this.gl,[0.95,0.75,0.25],[0.75,0.35,0.10],12);     // brass tip
    this.cyl=new Cylinder(this.gl,[0.35,0.40,0.48],[0.15,0.18,0.22],12);
    this.sph=new Sphere(this.gl,[0.85,0.55,0.25],[0.45,0.22,0.10],12,12); // bronze
    this.loadR=new Cube(this.gl,[0.85,0.25,0.25],[0.45,0.10,0.10]);
    this.loadG=new Cube(this.gl,[0.25,0.70,0.40],[0.10,0.40,0.20]);
    this.loadB=new Sphere(this.gl,[0.35,0.55,0.95],[0.15,0.25,0.70],10,10);
    var a=[this.ground,this.wood,this.metal,this.ram,this.cyl,this.sph,this.loadR,this.loadG,this.loadB];
    for(var i=0;i<a.length;i++) setSh(a[i],this);
    window.addEventListener('keydown',(e)=>{
      if(e.key.toLowerCase()==='r'){ this.wheelMode=(this.wheelMode+1)%3; console.log('wheel',this.wheelMode); }
    },false);
  }
  wheel(M,x,y){
    var Wm=mul3(M, T(x,y,0), Su(0.045));
    if(this.wheelMode===0) draw(this.metal,Wm);
    else if(this.wheelMode===1) draw(this.cyl,Wm);
    else draw(this.sph,Wm);
  }
  vehicle(M, i){
    var s = (i===0)? 0.13 : (0.09+0.012*i);
    draw(this.wood, mul2(M, Su(s)));
    if(i===0) draw(this.ram, mul3(M, T(0.20,0,0), mul2(Rdeg(90,0,0,1), Su(0.07))));
    if(i===1) draw(this.loadR, mul3(M, T(0,0.13,0), Su(0.045)));
    if(i===2) draw(this.loadG, mul3(M, T(0,0.13,0), Su(0.045)));
    if(i===3) draw(this.loadB, mul3(M, T(0,0.14,0), Su(0.05)));
    this.wheel(M,-0.09,-0.09); this.wheel(M,0.09,-0.09);
    this.wheel(M,-0.09, 0.09); this.wheel(M,0.09, 0.09);
  }
  render(){
    this.gl.clear(this.gl.COLOR_BUFFER_BIT|this.gl.DEPTH_BUFFER_BIT);
    draw(this.ground, mul3(T(0,-0.38,0), Rdeg(90,1,0,0), Su(1.2)));
    // clean row, slight tilt for depth (no crazy spin)
    var base=Rdeg(18,1,0,0);
    var xs=[0.58, 0.18, -0.22, -0.62];
    for(var i=0;i<4;i++){
      var M=mul3(base, T(xs[i], -0.05, 0), Rdeg(8,0,1,0));
      this.vehicle(M,i);
    }
  }
}
new myapp('cQ2').run();
"""

# ===================== Q3 =====================
Q3 = SHAPES + HELPERS + r"""
function lemni(w,a,b){
  var s=Math.sin(w), c=Math.cos(w), d=1+s*s;
  return {x: a*c/d, y: b*s*c/d};
}
function lemniD(w,a,b,eps){
  var s=Math.sin(w), c=Math.cos(w), d=1+s*s, d2=d*d;
  var dx=-a*eps*s*(2+c*c)/d2;
  var dy=eps*b*(Math.cos(2*w)*d - s*c*2*s*c)/d2;
  return {dx:dx, dy:dy};
}
class myapp extends DEECapp{
  wheelMode=0;
  initialize(){
    makeShader(this);
    this.gl.clearColor(0.58, 0.74, 0.92, 1);
    this.ground=new Disc(this.gl,[0.40,0.62,0.36],[0.22,0.45,0.24],32);
    this.wood=new Cube(this.gl,[0.78,0.50,0.24],[0.42,0.22,0.08]);
    this.metal=new Cube(this.gl,[0.50,0.55,0.65],[0.22,0.25,0.32]);
    this.ram=new Cone(this.gl,[1.0,0.78,0.28],[0.80,0.35,0.08],12);
    this.cyl=new Cylinder(this.gl,[0.40,0.45,0.55],[0.18,0.20,0.28],12);
    this.sph=new Sphere(this.gl,[0.90,0.55,0.20],[0.50,0.22,0.08],10,10);
    var a=[this.ground,this.wood,this.metal,this.ram,this.cyl,this.sph];
    for(var i=0;i<a.length;i++) setSh(a[i],this);
    this.a=0.72; this.b=0.42; this.eps=0.40;
    this.theta=[0,-0.55,-1.1,-1.65];
    this.t0=Date.now();
    window.addEventListener('keydown',(e)=>{ if(e.key.toLowerCase()==='r') this.wheelMode=(this.wheelMode+1)%3; },false);
  }
  render(){
    this.gl.clear(this.gl.COLOR_BUFFER_BIT|this.gl.DEPTH_BUFFER_BIT);
    draw(this.ground, mul3(T(0,-0.55,0), Rdeg(90,1,0,0), Su(1.25)));
    var t=(Date.now()-this.t0)*0.001;
    var wh=(this.wheelMode===0)?this.metal:(this.wheelMode===1?this.cyl:this.sph);
    for(var i=0;i<4;i++){
      var w=this.eps*t+this.theta[i];
      var p=lemni(w,this.a,this.b);
      var d=lemniD(w,this.a,this.b,this.eps);
      var yaw=Math.atan2(d.dy,d.dx)*180/Math.PI;
      var root=mul2(T(p.x, p.y, 0), Rdeg(yaw,0,0,1));
      draw(this.wood, mul2(root, Su(0.075)));
      if(i===0) draw(this.ram, mul3(root, T(0.13,0,0), mul2(Rdeg(90,0,0,1), Su(0.055))));
      draw(wh, mul3(root, T(-0.05,-0.06,0), Su(0.028)));
      draw(wh, mul3(root, T( 0.05,-0.06,0), Su(0.028)));
    }
  }
}
new myapp('cQ3').run();
"""

# ===================== Q4 =====================
Q4 = SHAPES + HELPERS + r"""
class myapp extends DEECapp{
  initialize(){
    makeShader(this);
    this.gl.clearColor(0.52, 0.70, 0.48, 1); // meadow
    this.ground=new Disc(this.gl,[0.38,0.58,0.32],[0.22,0.42,0.22],32);
    this.wood=new Cube(this.gl,[0.70,0.45,0.20],[0.38,0.20,0.08]);
    this.stone=new Cube(this.gl,[0.62,0.64,0.68],[0.35,0.38,0.42]);
    this.trunk=new Cylinder(this.gl,[0.55,0.32,0.14],[0.28,0.14,0.06],12);
    this.leaf=new Cone(this.gl,[0.25,0.75,0.30],[0.08,0.40,0.15],12);
    this.fire=new Sphere(this.gl,[1.0,0.70,0.15],[1.0,0.25,0.05],10,10);
    this.dark=new Cube(this.gl,[0.25,0.18,0.12],[0.10,0.08,0.05]);
    var a=[this.ground,this.wood,this.stone,this.trunk,this.leaf,this.fire,this.dark];
    for(var i=0;i<a.length;i++) setSh(a[i],this);
    this.t0=Date.now();
  }
  tree(x,y){
    draw(this.trunk, mul3(T(x,y-0.02,0), Rdeg(90,1,0,0), Su(0.045)));
    draw(this.leaf, mul2(T(x,y+0.14,0), Su(0.14)));
  }
  torch(x,y,t){
    draw(this.trunk, mul3(T(x,y,0), Rdeg(90,1,0,0), Su(0.028)));
    var f=0.055+0.018*Math.sin(t*7+x*9);
    draw(this.fire, mul2(T(x,y+0.13,0), Su(f)));
  }
  render(){
    this.gl.clear(this.gl.COLOR_BUFFER_BIT|this.gl.DEPTH_BUFFER_BIT);
    var t=(Date.now()-this.t0)*0.001;
    draw(this.ground, mul3(T(0,-0.48,0), Rdeg(90,1,0,0), Su(1.2)));
    this.tree(-0.72,0.35); this.tree(0.72,0.32); this.tree(-0.68,-0.42); this.tree(0.70,-0.40);
    this.torch(-0.35,0.50,t); this.torch(0.35,0.50,t); this.torch(-0.28,-0.55,t); this.torch(0.28,-0.55,t);
    // trebuchet
    draw(this.wood, mul2(T(-0.18,-0.18,0), Su(0.16)));
    draw(this.trunk, mul3(T(-0.18,0.02,0), Rdeg(90,1,0,0), Su(0.04)));
    var ang=32*Math.sin(t*1.5);
    var arm=mul3(T(-0.18,0.14,0), Rdeg(ang,0,0,1), T(0.20,0,0));
    draw(this.wood, mul2(arm, Su(0.13)));
    draw(this.dark, mul3(arm, T(0.16,0,0), Su(0.055)));
    // mill / well
    draw(this.stone, mul2(T(0.38,-0.22,0), Su(0.13)));
    draw(this.trunk, mul3(T(0.38,-0.02,0), Rdeg(90,1,0,0), Su(0.09)));
    draw(this.trunk, mul3(T(0.55,0.02,0), Rdeg(t*85,0,0,1), Su(0.11)));
    var by=-0.08+0.09*Math.sin(t*2.1);
    draw(this.dark, mul2(T(0.38, by, 0), Su(0.055)));
  }
}
new myapp('cQ4').run();
"""

# ===================== Q5 =====================
Q5 = SHAPES + HELPERS + r"""
class myapp extends DEECapp{
  initialize(){
    makeShader(this);
    this.gl.clearColor(0.60, 0.76, 0.94, 1);
    this.ground=new Disc(this.gl,[0.40,0.58,0.34],[0.24,0.42,0.24],32);
    this.stone=new Cube(this.gl,[0.68,0.70,0.76],[0.40,0.42,0.48]);
    this.roof=new Cone(this.gl,[0.85,0.30,0.28],[0.45,0.12,0.12],12);
    this.dark=new Cube(this.gl,[0.18,0.16,0.22],[0.06,0.06,0.08]);
    this.wood=new Cube(this.gl,[0.72,0.48,0.22],[0.38,0.20,0.08]);
    this.trunk=new Cylinder(this.gl,[0.50,0.30,0.12],[0.25,0.12,0.05],12);
    this.leaf=new Cone(this.gl,[0.22,0.70,0.28],[0.08,0.38,0.14],12);
    var a=[this.ground,this.stone,this.roof,this.dark,this.wood,this.trunk,this.leaf];
    for(var i=0;i<a.length;i++) setSh(a[i],this);
  }
  render(){
    this.gl.clear(this.gl.COLOR_BUFFER_BIT|this.gl.DEPTH_BUFFER_BIT);
    // FIXED view angle only (NO spinning).
    // Pehle bug: spin = Rdeg(this.counter*...) har frame badalta tha -> poori castle ghumti thi.
    var view = mul2(Rdeg(18, 1,0,0), Rdeg(-22, 0,1,0));
    function D(obj, local){ draw(obj, mul2(view, local)); }

    D(this.ground, mul3(T(0,-0.45,0), Rdeg(90,1,0,0), Su(1.15)));
    // back wall
    D(this.stone, mul2(T(0, 0.05, -0.45), Su(0.65)));
    // towers + roofs
    D(this.stone, mul2(T(-0.50,0.22,-0.42), Su(0.16)));
    D(this.stone, mul2(T( 0.50,0.22,-0.42), Su(0.16)));
    D(this.roof,  mul2(T(-0.50,0.48,-0.42), Su(0.18)));
    D(this.roof,  mul2(T( 0.50,0.48,-0.42), Su(0.18)));
    // gate pillars + arch
    D(this.stone, mul2(T(-0.18,0.02,0.05), Su(0.09)));
    D(this.stone, mul2(T( 0.18,0.02,0.05), Su(0.09)));
    D(this.stone, mul2(T(0,0.22,0.05), Su(0.22)));
    // portcullis
    for(var i=-2;i<=2;i++) D(this.dark, mul2(T(i*0.055,0.02,0.12), Su(0.028)));
    // windows
    D(this.dark, mul2(T(-0.22,0.22,-0.38), Su(0.06)));
    D(this.dark, mul2(T( 0.22,0.22,-0.38), Su(0.06)));
    D(this.dark, mul2(T(0,0.28,-0.38), Su(0.06)));
    // props
    for(var k=0;k<5;k++) D(this.wood, mul2(T(-0.40+k*0.20, -0.28, 0.40), Su(0.05)));
    D(this.wood, mul2(T(0.55,-0.28,0.15), Su(0.07)));
    D(this.wood, mul2(T(0.66,-0.20,0.20), Su(0.05)));
    D(this.trunk, mul3(T(-0.62,-0.18,0.25), Rdeg(90,1,0,0), Su(0.04)));
    D(this.leaf, mul2(T(-0.62,0.08,0.25), Su(0.12)));
  }
}
new myapp('cQ5').run();
"""

# ===================== Q6 =====================
Q6 = SHAPES + HELPERS + r"""
class myapp extends DEECapp{
  eye={x:0,y:0.45,z:1.6}; yaw=0; keys={};
  initialize(){
    makeShader(this);
    this.gl.clearColor(0.55, 0.72, 0.92, 1);
    this.grass=new Cube(this.gl,[0.35,0.62,0.32],[0.20,0.42,0.20]);
    this.stone=new Cube(this.gl,[0.65,0.68,0.74],[0.38,0.40,0.46]);
    this.wood=new Cube(this.gl,[0.75,0.48,0.22],[0.40,0.22,0.08]);
    this.leaf=new Cone(this.gl,[0.22,0.72,0.30],[0.08,0.40,0.14],12);
    this.trunk=new Cylinder(this.gl,[0.50,0.30,0.12],[0.25,0.12,0.05],12);
    this.accent=new Sphere(this.gl,[0.95,0.55,0.25],[0.80,0.25,0.15],10,10);
    var a=[this.grass,this.stone,this.wood,this.leaf,this.trunk,this.accent];
    for(var i=0;i<a.length;i++) setSh(a[i],this);
    window.addEventListener('keydown',(e)=>{ this.keys[e.key.toLowerCase()]=true; },false);
    window.addEventListener('keyup',(e)=>{ this.keys[e.key.toLowerCase()]=false; },false);
  }
  render(){
    this.gl.clear(this.gl.COLOR_BUFFER_BIT|this.gl.DEPTH_BUFFER_BIT);
    var sp=0.025, rad=this.yaw*Math.PI/180;
    var fx=Math.sin(rad), fz=-Math.cos(rad);
    var rx=Math.cos(rad), rz=Math.sin(rad);
    if(this.keys['w']){ this.eye.x+=fx*sp; this.eye.z+=fz*sp; }
    if(this.keys['s']){ this.eye.x-=fx*sp; this.eye.z-=fz*sp; }
    if(this.keys['a']){ this.eye.x-=rx*sp; this.eye.z-=rz*sp; }
    if(this.keys['d']){ this.eye.x+=rx*sp; this.eye.z+=rz*sp; }
    if(this.keys['q']) this.yaw-=1.3;
    if(this.keys['e']) this.yaw+=1.3;
    var aspect=this.canvas.width/this.canvas.height;
    var proj=glm.perspective(glm.radians(55), aspect, 0.05, 50);
    var view=glm.lookAt(
      glm.vec3(this.eye.x,this.eye.y,this.eye.z),
      glm.vec3(this.eye.x+fx, this.eye.y, this.eye.z+fz),
      glm.vec3(0,1,0)
    );
    function D(obj,M){ drawVP(obj,M,view,proj); }
    D(this.grass, mul2(T(0,-0.45, -0.2), Su(1.4)));
    D(this.stone, mul2(T(0,0.25,-1.6), Su(1.05)));
    D(this.wood, mul2(T(-0.7,0,-0.4), Su(0.16)));
    D(this.wood, mul2(T(0.65,0,-0.2), Su(0.14)));
    D(this.accent, mul2(T(0.65,0.22,-0.2), Su(0.08)));
    D(this.trunk, mul3(T(-0.9,0,0.3), Rdeg(90,1,0,0), Su(0.09)));
    D(this.leaf, mul2(T(-0.9,0.28,0.3), Su(0.22)));
  }
}
new myapp('cQ6').run();
"""

# ===================== Q7 =====================
Q7 = SHAPES + HELPERS + r"""
function lemni(w,a,b){
  var s=Math.sin(w), c=Math.cos(w), d=1+s*s;
  return {x:a*c/d, z:b*s*c/d};
}
function lemniD(w,a,b,eps){
  var s=Math.sin(w), c=Math.cos(w), d=1+s*s, d2=d*d;
  return { dx:-a*eps*s*(2+c*c)/d2, dz:eps*b*(Math.cos(2*w)*d - s*c*2*s*c)/d2 };
}
class myapp extends DEECapp{
  camMode=0;
  eye={x:0,y:0.9,z:3.2}; yaw=0; keys={};
  initialize(){
    makeShader(this);
    this.gl.clearColor(0.52, 0.70, 0.90, 1);
    this.grass=new Cube(this.gl,[0.34,0.58,0.30],[0.18,0.40,0.18]);
    this.wood=new Cube(this.gl,[0.76,0.48,0.22],[0.40,0.20,0.08]);
    this.stone=new Cube(this.gl,[0.64,0.66,0.72],[0.36,0.38,0.44]);
    this.ram=new Cone(this.gl,[1.0,0.78,0.28],[0.80,0.35,0.10],12);
    this.roof=new Cone(this.gl,[0.85,0.28,0.25],[0.45,0.10,0.10],12);
    var a=[this.grass,this.wood,this.stone,this.ram,this.roof];
    for(var i=0;i<a.length;i++) setSh(a[i],this);
    this.a=1.6; this.b=1.05; this.eps=0.48; this.theta=[0,-0.5,-1.0,-1.5];
    this.t0=Date.now();
    window.addEventListener('keydown',(e)=>{
      var k=e.key.toLowerCase(); this.keys[k]=true;
      if(k==='v'){ this.camMode=1-this.camMode; console.log(this.camMode?'ride':'walk'); }
    },false);
    window.addEventListener('keyup',(e)=>{ this.keys[e.key.toLowerCase()]=false; },false);
  }
  render(){
    this.gl.clear(this.gl.COLOR_BUFFER_BIT|this.gl.DEPTH_BUFFER_BIT);
    var t=(Date.now()-this.t0)*0.001;
    var wagons=[];
    for(var i=0;i<4;i++){
      var w=this.eps*t+this.theta[i];
      var p=lemni(w,this.a,this.b);
      var d=lemniD(w,this.a,this.b,this.eps);
      wagons.push({x:p.x, z:p.z, yaw:Math.atan2(d.dx,d.dz)});
    }
    var aspect=this.canvas.width/this.canvas.height;
    var proj=glm.perspective(glm.radians(55),aspect,0.05,80);
    var view;
    if(this.camMode===0){
      var sp=0.045, rad=this.yaw*Math.PI/180;
      var fx=Math.sin(rad), fz=-Math.cos(rad);
      var rx=Math.cos(rad), rz=Math.sin(rad);
      if(this.keys['w']){ this.eye.x+=fx*sp; this.eye.z+=fz*sp; }
      if(this.keys['s']){ this.eye.x-=fx*sp; this.eye.z-=fz*sp; }
      if(this.keys['a']){ this.eye.x-=rx*sp; this.eye.z-=rz*sp; }
      if(this.keys['d']){ this.eye.x+=rx*sp; this.eye.z+=rz*sp; }
      if(this.keys['q']) this.yaw-=1.5;
      if(this.keys['e']) this.yaw+=1.5;
      view=glm.lookAt(glm.vec3(this.eye.x,this.eye.y,this.eye.z),
                      glm.vec3(this.eye.x+fx,this.eye.y,this.eye.z+fz), glm.vec3(0,1,0));
    } else {
      var W=wagons[3];
      var fx=Math.sin(W.yaw), fz=Math.cos(W.yaw);
      view=glm.lookAt(glm.vec3(W.x-fx*0.35,0.55,W.z-fz*0.35),
                      glm.vec3(W.x+fx*2.2,0.4,W.z+fz*2.2), glm.vec3(0,1,0));
    }
    function D(obj,M){ drawVP(obj,M,view,proj); }
    D(this.grass, mul2(T(0,-0.35,0), Su(3.2)));
    D(this.stone, mul2(T(0,0.4,-5.2), Su(1.6)));
    D(this.roof, mul2(T(-1.2,1.5,-5.0), Su(0.55)));
    D(this.roof, mul2(T( 1.2,1.5,-5.0), Su(0.55)));
    for(var i=0;i<4;i++){
      var W=wagons[i];
      var M=mul3(T(W.x,0.22,W.z), Rdeg(W.yaw*180/Math.PI,0,1,0), Su(0.22));
      D(this.wood, M);
      if(i===0) D(this.ram, mul4(T(W.x,0.28,W.z), Rdeg(W.yaw*180/Math.PI,0,1,0), T(0,0,0.42), Su(0.16)));
    }
  }
}
new myapp('cQ7').run();
"""


COLOR_TIP = """
### Colors kaise change karein (bahut easy)
Har shape aise banti hai:
```
new Cube(this.gl, [R1,G1,B1], [R2,G2,B2])
```
- pehla array = left color  
- doosra array = right color (gradient)  
- values **0 se 1** (example red = `[1, 0, 0]`, gold = `[0.95, 0.75, 0.2]`)

Background:
```
this.gl.clearColor(R, G, B, 1);
```
"""


def build():
    save(
        "Q1_A1_Shapes.ipynb",
        [
            md("# Question 1 — Exercise A.1 (Shapes)\n\n5 primitives + horizontal color gradient.\n" + COLOR_TIP),
            code(page("cQ1", Q1, "<b>Q1 Shapes</b> — Cube, Sphere, Cylinder, Cone, Disc")),
        ],
    )
    save(
        "Q2_A2_Convoy.ipynb",
        [
            md("# Question 2 — Exercise A.2 (Convoy)\n\nRam + 3 wagons. Key <b>r</b> = wheels cube/cylinder/sphere.\n" + COLOR_TIP),
            code(page("cQ2", Q2, "<b>Q2 Convoy</b> — press <b>r</b> to change wheels")),
        ],
    )
    save(
        "Q3_A3_Lemniscate_Path.ipynb",
        [
            md("# Question 3 — Exercise A.3 (Path)\n\nLemniscate figure-8 + tangent orientation. Key <b>r</b> wheels.\n"),
            code(page("cQ3", Q3, "<b>Q3 Path</b> — figure-8 patrol (key <b>r</b> = wheels)")),
        ],
    )
    save(
        "Q4_A4_Props_Animations.ipynb",
        [
            md("# Question 4 — Exercise A.4\n\nTrees, torches, trebuchet pendulum, mill wheel + bucket.\n"),
            code(page("cQ4", Q4, "<b>Q4 Camp</b> — decorations + 2 animations")),
        ],
    )
    save(
        "Q5_A5_Castle.ipynb",
        [
            md("# Question 5 — Exercise A.5 (Castle)\n\nFloor, walls, towers, gate/portcullis, windows, props.\n"),
            code(page("cQ5", Q5, "<b>Q5 Castle</b> — gatehouse + props")),
        ],
    )
    save(
        "Q6_A6_WASD_Camera.ipynb",
        [
            md("# Question 6 — Exercise A.6 (WASD)\n\n**W A S D** move, **Q E** turn. Click canvas first.\n"),
            code(page("cQ6", Q6, "<b>Q6 Camera</b> — WASD walk, QE turn", 760, 500)),
        ],
    )
    save(
        "Q7_A7_Camera_Toggle.ipynb",
        [
            md("# Question 7 — Exercise A.7\n\n**V** = walk camera ↔ ride last wagon. Also WASD / QE.\n"),
            code(page("cQ7", Q7, "<b>Q7 Toggle</b> — key <b>v</b> ride wagon", 800, 520)),
        ],
    )

    (OUT / "README_QUESTIONS.txt").write_text(
        """QUESTIONS folder (CLEAN + COLORS) — alag from old notebooks
============================================================
Purani files notebooks/ mein hain — unko touch NAHI kiya.
Yeh folder: notebooks/QUESTIONS/

Q1..Q7 = Exercise A.1 .. A.7

Colors change:
  new Cube(gl, [R1,G1,B1], [R2,G2,B2])   // 0..1
  this.gl.clearColor(R,G,B,1);           // background

Upload ONLY this QUESTIONS folder to seeds, Voila each file.
""",
        encoding="utf-8",
    )
    (OUT / "HOW_TO_CHANGE_COLORS.txt").write_text(
        """ATTRACTIVE COLORS — kaise add/change
=====================================

1) Shape colors (gradient):
   new Sphere(this.gl, [0.2, 0.85, 0.95], [0.95, 0.35, 0.75], 12, 12);
        color1 (left) ---------------> color2 (right)

2) RGB examples (0 to 1):
   Red     [1.0, 0.2, 0.2]
   Gold    [0.95, 0.75, 0.25]
   Cyan    [0.2, 0.85, 0.95]
   Pink    [0.95, 0.35, 0.75]
   Lime    [0.55, 0.90, 0.40]
   Violet  [0.55, 0.30, 0.95]
   Oak     [0.72, 0.48, 0.22]
   Stone   [0.68, 0.70, 0.76]

3) Sky / background:
   this.gl.clearColor(0.62, 0.78, 0.95, 1);

4) Save notebook -> Voila tab Ctrl+F5
""",
        encoding="utf-8",
    )
    print("DONE QUESTIONS only")


if __name__ == "__main__":
    build()
