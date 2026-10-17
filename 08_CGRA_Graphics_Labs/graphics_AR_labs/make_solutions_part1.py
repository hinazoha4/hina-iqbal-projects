# Generate CGRA exercise solution notebooks for JupyterHub + Voilà
import json
from pathlib import Path

OUT = Path(r"c:\Users\Lenovo\Downloads\computer architecture\graphics_AR_labs\SOLUTIONS")
OUT.mkdir(exist_ok=True)

LIBS = """%%html
<script src="https://is3l.isr.uc.pt/~pm/CGRA/JS/deecshader.js"></script>
<script src="https://is3l.isr.uc.pt/~pm/CGRA/JS/deecapp.js"></script>
"""

GLM = """%%html
<script src="https://git.io/glm-js.min.js"></script>
"""

SHADER2D = """%%html
<script id="my-vertex-shader" type="x-shader/x-vertex">
precision highp float;
attribute vec2 in_Position;
attribute vec3 in_Color;
varying vec3 ex_Color;
void main(void){
  gl_Position = vec4(in_Position.x, in_Position.y, 0.0, 1.0);
  ex_Color = in_Color;
}
</script>
<script id="my-fragment-shader" type="x-shader/x-fragment">
precision highp float;
varying vec3 ex_Color;
void main(void){
  gl_FragColor = vec4(ex_Color, 1.0);
}
</script>
"""

SHADER3D = """%%html
<script id="vert3d" type="x-shader/x-vertex">
precision highp float;
attribute vec3 in_Position;
attribute vec3 in_Color;
varying vec3 ex_Color;
void main(void){
  gl_Position = vec4(in_Position.x, in_Position.y, in_Position.z, 1.0);
  ex_Color = in_Color;
}
</script>
"""


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True) or [text]}


def code(text):
    if not text.endswith("\n"):
        text += "\n"
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": text.splitlines(keepends=True),
    }


def nb(cells):
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def save(name, cells):
    path = OUT / name
    path.write_text(json.dumps(nb(cells), indent=1), encoding="utf-8")
    print("wrote", path.name)


# ---------- helper JS: bind + draw 2D ----------
HELPER_DRAW2D = r"""
function bindDraw2D(app, vbuf, cbuf, nverts, mode){
  var gl = app.gl;
  gl.bindBuffer(gl.ARRAY_BUFFER, vbuf);
  var locP = gl.getAttribLocation(app.shaderprog.shaderProgram, "in_Position");
  gl.vertexAttribPointer(locP, 2, gl.FLOAT, false, 0, 0);
  gl.enableVertexAttribArray(locP);
  gl.bindBuffer(gl.ARRAY_BUFFER, cbuf);
  var locC = gl.getAttribLocation(app.shaderprog.shaderProgram, "in_Color");
  gl.vertexAttribPointer(locC, 3, gl.FLOAT, false, 0, 0);
  gl.enableVertexAttribArray(locC);
  app.shaderprog.startUsing();
  gl.drawArrays(mode, 0, nverts);
  app.shaderprog.stopUsing();
}
function makeBuf(gl, data){
  var b = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, b);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(data), gl.STATIC_DRAW);
  return b;
}
"""

# ===================== EX1 =====================
ex1 = [
    md("# CGRA Solutions — Chapter 1 (Ex 1.1–1.4)\nOpen with **Voilà**. Do not use Run."),
    code(LIBS),
    code(SHADER2D),
    md("## Ex 1.1 — colours + vertices changed (vertical-ish triangle, new colours)"),
    code(
        "%%html\n<canvas id=\"c11\" width=\"400\" height=\"400\" style=\"border:2px solid #000;\"></canvas>\n<script>\n"
        + HELPER_DRAW2D
        + r"""
class App11 extends DEECapp{
  initialize(){
    super.initialize();
    this.gl.clearColor(1,1,1,1);
    // Ex1.1: new coordinates (inside [-1,1]) + new colours
    this.vertices = [ 0.0, 0.85,  -0.6, -0.7,  0.6, -0.7 ];
    this.colors   = [ 1.0, 0.5, 0.0,   0.0, 0.8, 0.8,   0.8, 0.0, 0.8 ];
    this.n = 3;
    this.vbuf = makeBuf(this.gl, this.vertices);
    this.cbuf = makeBuf(this.gl, this.colors);
  }
  render(){
    this.gl.clear(this.gl.COLOR_BUFFER_BIT);
    bindDraw2D(this, this.vbuf, this.cbuf, this.n, this.gl.TRIANGLES);
  }
}
new App11('c11').run();
</script>
"""
    ),
    md("## Ex 1.2 — Console messages (F12 → Console → see draw N)"),
    code(
        "%%html\n<canvas id=\"c12\" width=\"400\" height=\"400\" style=\"border:2px solid #000;\"></canvas>\n<script>\n"
        + HELPER_DRAW2D
        + r"""
class App12 extends DEECapp{
  counter = 0;
  initialize(){
    super.initialize();
    this.gl.clearColor(1,1,1,1);
    this.vertices = [0.0,0.7, -0.6,-0.5, 0.6,-0.5];
    this.colors = [1,0,0, 0,1,0, 0,0,1];
    this.vbuf = makeBuf(this.gl, this.vertices);
    this.cbuf = makeBuf(this.gl, this.colors);
  }
  render(){
    console.log('draw ' + this.counter);
    var g = 0.5 + 0.5*Math.sin(this.counter/60);
    this.gl.clearColor(g,g,g,1);
    this.gl.clear(this.gl.COLOR_BUFFER_BIT);
    this.counter++;
    bindDraw2D(this, this.vbuf, this.cbuf, 3, this.gl.TRIANGLES);
  }
}
new App12('c12').run();
</script>
"""
    ),
    md("## Ex 1.3 — one more point (4 vertices, LINE_LOOP)"),
    code(
        "%%html\n<canvas id=\"c13\" width=\"400\" height=\"400\" style=\"border:2px solid #000;\"></canvas>\n<script>\n"
        + HELPER_DRAW2D
        + r"""
class App13 extends DEECapp{
  initialize(){
    super.initialize();
    this.gl.clearColor(1,1,1,1);
    // 4 points: diamond
    this.vertices = [ 0.0, 0.8,  0.8, 0.0,  0.0,-0.8, -0.8, 0.0 ];
    this.colors   = [ 1,0,0,  0,1,0,  0,0,1,  1,1,0 ];
    this.n = 4;
    this.vbuf = makeBuf(this.gl, this.vertices);
    this.cbuf = makeBuf(this.gl, this.colors);
  }
  render(){
    this.gl.clear(this.gl.COLOR_BUFFER_BIT);
    bindDraw2D(this, this.vbuf, this.cbuf, this.n, this.gl.LINE_LOOP);
  }
}
new App13('c13').run();
</script>
"""
    ),
    md("## Ex 1.4 — different drawArrays modes"),
    code(
        "%%html\n"
        "<p>POINTS</p><canvas id=\"c14a\" width=\"200\" height=\"200\" style=\"border:1px solid #000;\"></canvas>\n"
        "<p>LINE_STRIP</p><canvas id=\"c14b\" width=\"200\" height=\"200\" style=\"border:1px solid #000;\"></canvas>\n"
        "<p>LINES</p><canvas id=\"c14c\" width=\"200\" height=\"200\" style=\"border:1px solid #000;\"></canvas>\n"
        "<p>TRIANGLE_STRIP</p><canvas id=\"c14d\" width=\"200\" height=\"200\" style=\"border:1px solid #000;\"></canvas>\n"
        "<p>TRIANGLE_FAN</p><canvas id=\"c14e\" width=\"200\" height=\"200\" style=\"border:1px solid #000;\"></canvas>\n"
        "<p>TRIANGLES</p><canvas id=\"c14f\" width=\"200\" height=\"200\" style=\"border:1px solid #000;\"></canvas>\n"
        "<script>\n"
        + HELPER_DRAW2D
        + r"""
function makeModeApp(canvasId, modeName){
  class A extends DEECapp{
    initialize(){
      super.initialize();
      this.gl.clearColor(1,1,1,1);
      this.vertices = [0.0,0.7, -0.7,-0.6, 0.7,-0.6, 0.0,-0.1];
      this.colors = [1,0,0, 0,1,0, 0,0,1, 1,1,0];
      this.n = 4;
      this.mode = this.gl[modeName];
      this.vbuf = makeBuf(this.gl, this.vertices);
      this.cbuf = makeBuf(this.gl, this.colors);
    }
    render(){
      this.gl.clear(this.gl.COLOR_BUFFER_BIT);
      bindDraw2D(this, this.vbuf, this.cbuf, this.n, this.mode);
    }
  }
  new A(canvasId).run();
}
makeModeApp('c14a','POINTS');
makeModeApp('c14b','LINE_STRIP');
makeModeApp('c14c','LINES');
makeModeApp('c14d','TRIANGLE_STRIP');
makeModeApp('c14e','TRIANGLE_FAN');
makeModeApp('c14f','TRIANGLES');
</script>
"""
    ),
]
save("CGRA_SOL_Ch1_Ex1.ipynb", ex1)

# ===================== EX2 =====================
ex2 = [
    md("# CGRA Solutions — Chapter 2 (Ex 2.1–2.7)\nOpen with **Voilà**."),
    code(LIBS),
    code(SHADER2D),
    code(SHADER3D),
    md("## Ex 2.1 — vertical isosceles triangle"),
    code(
        "%%html\n<canvas id=\"c21\" width=\"400\" height=\"400\" style=\"border:2px solid #000;\"></canvas>\n<script>\n"
        + HELPER_DRAW2D
        + r"""
class App21 extends DEECapp{
  initialize(){
    super.initialize();
    this.gl.clearColor(1,1,1,1);
    // vertical isosceles: apex top, base bottom, equal sides
    this.vertices = [ 0.0, 0.8,  -0.5, -0.6,  0.5, -0.6 ];
    this.colors = [1,0,0, 0,1,0, 0,0,1];
    this.vbuf = makeBuf(this.gl, this.vertices);
    this.cbuf = makeBuf(this.gl, this.colors);
  }
  render(){
    this.gl.clear(this.gl.COLOR_BUFFER_BIT);
    bindDraw2D(this, this.vbuf, this.cbuf, 3, this.gl.TRIANGLES);
  }
}
new App21('c21').run();
</script>
"""
    ),
    md("## Ex 2.2 — red rectangle under triangle + depth (Z)"),
    code(
        "%%html\n<canvas id=\"c22\" width=\"400\" height=\"400\" style=\"border:2px solid #000;\"></canvas>\n<script>\n"
        + r"""
class App22 extends DEECapp{
  initialize(){
    // 3D shader for Z depth
    var vertsrc = document.getElementById('vert3d').text;
    var fragsrc = document.getElementById('my-fragment-shader').text;
    this.shaderprog = new DEECshader(this.gl);
    this.shaderprog.srcShaders(vertsrc, fragsrc);
    this.gl.enable(this.gl.DEPTH_TEST);
    this.gl.clearColor(1,1,1,1);

    // triangle closer (z = -0.2), rectangle farther (z = 0.2) OR swap to demo
    // rectangle side 0.8 centered: from -0.4 to 0.4
    this.triV = [
      0.0, 0.75, -0.2,
     -0.45,-0.55,-0.2,
      0.45,-0.55,-0.2
    ];
    this.triC = [1,0,0, 0,1,0, 0,0,1];
    this.rectV = [
     -0.4,-0.4, 0.2,   0.4,-0.4, 0.2,   0.4, 0.4, 0.2,
     -0.4,-0.4, 0.2,   0.4, 0.4, 0.2,  -0.4, 0.4, 0.2
    ];
    this.rectC = [
      1,0,0, 1,0,0, 1,0,0,
      1,0,0, 1,0,0, 1,0,0
    ];
    this.tv = this.gl.createBuffer();
    this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.tv);
    this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.triV), this.gl.STATIC_DRAW);
    this.tc = this.gl.createBuffer();
    this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.tc);
    this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.triC), this.gl.STATIC_DRAW);
    this.rv = this.gl.createBuffer();
    this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.rv);
    this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.rectV), this.gl.STATIC_DRAW);
    this.rc = this.gl.createBuffer();
    this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.rc);
    this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.rectC), this.gl.STATIC_DRAW);
  }
  draw3(vbuf,cbuf,n,mode){
    var gl=this.gl;
    gl.bindBuffer(gl.ARRAY_BUFFER, vbuf);
    var lp=gl.getAttribLocation(this.shaderprog.shaderProgram,'in_Position');
    gl.vertexAttribPointer(lp,3,gl.FLOAT,false,0,0);
    gl.enableVertexAttribArray(lp);
    gl.bindBuffer(gl.ARRAY_BUFFER, cbuf);
    var lc=gl.getAttribLocation(this.shaderprog.shaderProgram,'in_Color');
    gl.vertexAttribPointer(lc,3,gl.FLOAT,false,0,0);
    gl.enableVertexAttribArray(lc);
    this.shaderprog.startUsing();
    gl.drawArrays(mode,0,n);
    this.shaderprog.stopUsing();
  }
  render(){
    this.gl.clear(this.gl.COLOR_BUFFER_BIT | this.gl.DEPTH_BUFFER_BIT);
    // with DEPTH_TEST: smaller z (closer in this convention) depends on clear depth
    // draw rect then triangle; depth decides who is on top
    this.draw3(this.rv, this.rc, 6, this.gl.TRIANGLES);
    this.draw3(this.tv, this.tc, 3, this.gl.TRIANGLES);
  }
}
new App22('c22').run();
</script>
"""
    ),
    md("## Ex 2.3 — top vertex moves up/down at 0.5 Hz (sin)"),
    code(
        "%%html\n<canvas id=\"c23\" width=\"400\" height=\"400\" style=\"border:2px solid #000;\"></canvas>\n<script>\n"
        + HELPER_DRAW2D
        + r"""
class App23 extends DEECapp{
  initialize(){
    super.initialize();
    this.gl.clearColor(1,1,1,1);
    this.base = [0.0, 0.8, -0.5,-0.6, 0.5,-0.6];
    this.colors = [1,0,0, 0,1,0, 0,0,1];
    this.vertices = this.base.slice();
    this.vbuf = makeBuf(this.gl, this.vertices);
    this.cbuf = makeBuf(this.gl, this.colors);
    this.t0 = Date.now();
  }
  render(){
    var t = (Date.now() - this.t0) / 1000.0; // seconds
    // 0.5 Hz: omega = 2*pi*0.5 = pi
    var y = 0.1 + 0.7 * (0.5 + 0.5*Math.sin(Math.PI * t)); // between ~0.1 and 0.8
    this.vertices[1] = y;
    this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.vbuf);
    this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.vertices), this.gl.DYNAMIC_DRAW);
    this.gl.clear(this.gl.COLOR_BUFFER_BIT);
    bindDraw2D(this, this.vbuf, this.cbuf, 3, this.gl.TRIANGLES);
  }
}
new App23('c23').run();
</script>
"""
    ),
    md("## Ex 2.4 — rotate triangle (cos/sin)"),
    code(
        "%%html\n<canvas id=\"c24\" width=\"400\" height=\"400\" style=\"border:2px solid #000;\"></canvas>\n<script>\n"
        + HELPER_DRAW2D
        + r"""
class App24 extends DEECapp{
  initialize(){
    super.initialize();
    this.gl.clearColor(1,1,1,1);
    this.initV = [0.0,0.5, -0.4,-0.3, 0.4,-0.3];
    this.colors = [1,0,0, 0,1,0, 0,0,1];
    this.vertices = this.initV.slice();
    this.vbuf = makeBuf(this.gl, this.vertices);
    this.cbuf = makeBuf(this.gl, this.colors);
    this.t0 = Date.now();
  }
  render(){
    var t = (Date.now()-this.t0)/1000.0;
    var w = t; // rad/s
    var c = Math.cos(w), s = Math.sin(w);
    for(var i=0;i<3;i++){
      var x = this.initV[2*i], y = this.initV[2*i+1];
      this.vertices[2*i]   = x*c - y*s;
      this.vertices[2*i+1] = x*s + y*c;
    }
    this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.vbuf);
    this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.vertices), this.gl.DYNAMIC_DRAW);
    this.gl.clear(this.gl.COLOR_BUFFER_BIT);
    bindDraw2D(this, this.vbuf, this.cbuf, 3, this.gl.TRIANGLES);
  }
}
new App24('c24').run();
</script>
"""
    ),
    md("## Ex 2.5 — rotating triangle over static rectangle"),
    code(
        "%%html\n<canvas id=\"c25\" width=\"400\" height=\"400\" style=\"border:2px solid #000;\"></canvas>\n<script>\n"
        + HELPER_DRAW2D
        + r"""
class App25 extends DEECapp{
  initialize(){
    super.initialize();
    this.gl.clearColor(1,1,1,1);
    this.rectV = [-0.4,-0.4, 0.4,-0.4, 0.4,0.4, -0.4,-0.4, 0.4,0.4, -0.4,0.4];
    this.rectC = [1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0];
    this.initV = [0.0,0.45, -0.25,-0.15, 0.25,-0.15];
    this.triC = [0,0,1, 0,1,1, 1,1,0];
    this.triV = this.initV.slice();
    this.rv = makeBuf(this.gl, this.rectV);
    this.rc = makeBuf(this.gl, this.rectC);
    this.tv = makeBuf(this.gl, this.triV);
    this.tc = makeBuf(this.gl, this.triC);
    this.t0 = Date.now();
  }
  render(){
    var t=(Date.now()-this.t0)/1000.0;
    var c=Math.cos(t), s=Math.sin(t);
    for(var i=0;i<3;i++){
      var x=this.initV[2*i], y=this.initV[2*i+1];
      this.triV[2*i]=x*c-y*s; this.triV[2*i+1]=x*s+y*c;
    }
    this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.tv);
    this.gl.bufferData(this.gl.ARRAY_BUFFER,new Float32Array(this.triV),this.gl.DYNAMIC_DRAW);
    this.gl.clear(this.gl.COLOR_BUFFER_BIT);
    bindDraw2D(this,this.rv,this.rc,6,this.gl.TRIANGLES);
    bindDraw2D(this,this.tv,this.tc,3,this.gl.TRIANGLES);
  }
}
new App25('c25').run();
</script>
"""
    ),
    md("## Ex 2.6 — rotate + translate up/down (sin)"),
    code(
        "%%html\n<canvas id=\"c26\" width=\"400\" height=\"400\" style=\"border:2px solid #000;\"></canvas>\n<script>\n"
        + HELPER_DRAW2D
        + r"""
class App26 extends DEECapp{
  initialize(){
    super.initialize();
    this.gl.clearColor(1,1,1,1);
    this.initV = [0.0,0.3, -0.25,-0.2, 0.25,-0.2];
    this.colors = [1,0,0,0,1,0,0,0,1];
    this.vertices = this.initV.slice();
    this.vbuf = makeBuf(this.gl, this.vertices);
    this.cbuf = makeBuf(this.gl, this.colors);
    this.t0 = Date.now();
  }
  render(){
    var t=(Date.now()-this.t0)/1000.0;
    var c=Math.cos(t), s=Math.sin(t);
    var ty = 0.4*Math.sin(t);
    for(var i=0;i<3;i++){
      var x=this.initV[2*i], y=this.initV[2*i+1];
      var xr=x*c-y*s, yr=x*s+y*c;
      this.vertices[2*i]=xr;
      this.vertices[2*i+1]=yr+ty;
    }
    this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.vbuf);
    this.gl.bufferData(this.gl.ARRAY_BUFFER,new Float32Array(this.vertices),this.gl.DYNAMIC_DRAW);
    this.gl.clear(this.gl.COLOR_BUFFER_BIT);
    bindDraw2D(this,this.vbuf,this.cbuf,3,this.gl.TRIANGLES);
  }
}
new App26('c26').run();
</script>
"""
    ),
    md("## Ex 2.7 — same motion on Z (3D shader)"),
    code(
        "%%html\n<canvas id=\"c27\" width=\"400\" height=\"400\" style=\"border:2px solid #000;\"></canvas>\n<script>\n"
        + r"""
class App27 extends DEECapp{
  initialize(){
    var vertsrc = document.getElementById('vert3d').text;
    var fragsrc = document.getElementById('my-fragment-shader').text;
    this.shaderprog = new DEECshader(this.gl);
    this.shaderprog.srcShaders(vertsrc, fragsrc);
    this.gl.enable(this.gl.DEPTH_TEST);
    this.gl.clearColor(1,1,1,1);
    this.initV = [0.0,0.4,0, -0.3,-0.2,0, 0.3,-0.2,0];
    this.colors = [1,0,0,0,1,0,0,0,1];
    this.v = this.initV.slice();
    this.vbuf = this.gl.createBuffer();
    this.cbuf = this.gl.createBuffer();
    this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.cbuf);
    this.gl.bufferData(this.gl.ARRAY_BUFFER,new Float32Array(this.colors),this.gl.STATIC_DRAW);
    this.t0 = Date.now();
  }
  render(){
    var t=(Date.now()-this.t0)/1000.0;
    var c=Math.cos(t), s=Math.sin(t);
    var tz = 0.5*Math.sin(t); // Z motion
    for(var i=0;i<3;i++){
      var x=this.initV[3*i], y=this.initV[3*i+1];
      this.v[3*i]=x*c-y*s;
      this.v[3*i+1]=x*s+y*c;
      this.v[3*i+2]=tz;
    }
    this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.vbuf);
    this.gl.bufferData(this.gl.ARRAY_BUFFER,new Float32Array(this.v),this.gl.DYNAMIC_DRAW);
    this.gl.clear(this.gl.COLOR_BUFFER_BIT|this.gl.DEPTH_BUFFER_BIT);
    var gl=this.gl;
    gl.bindBuffer(gl.ARRAY_BUFFER,this.vbuf);
    var lp=gl.getAttribLocation(this.shaderprog.shaderProgram,'in_Position');
    gl.vertexAttribPointer(lp,3,gl.FLOAT,false,0,0);
    gl.enableVertexAttribArray(lp);
    gl.bindBuffer(gl.ARRAY_BUFFER,this.cbuf);
    var lc=gl.getAttribLocation(this.shaderprog.shaderProgram,'in_Color');
    gl.vertexAttribPointer(lc,3,gl.FLOAT,false,0,0);
    gl.enableVertexAttribArray(lc);
    this.shaderprog.startUsing();
    gl.drawArrays(gl.TRIANGLES,0,3);
    this.shaderprog.stopUsing();
  }
}
new App27('c27').run();
</script>
"""
    ),
]
save("CGRA_SOL_Ch2_Ex2.ipynb", ex2)

print("ch1 ch2 done")
