# Generate CGRA Ch3 + Ch4 solution notebooks
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
FRAG = """%%html
<script id="my-fragment-shader" type="x-shader/x-fragment">
precision highp float;
varying vec3 ex_Color;
void main(void){ gl_FragColor = vec4(ex_Color,1.0); }
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


BASE_VERT = """
<script id="vert-base" type="x-shader/x-vertex">
precision highp float;
attribute vec2 in_Position;
attribute vec3 in_Color;
varying vec3 ex_Color;
void main(void){
  gl_Position = vec4(in_Position.x, in_Position.y, 0.0, 1.0);
  ex_Color = in_Color;
}
</script>
"""

# Also need my-vertex-shader for DEECapp default - provide base as both
DEFAULT_SHADERS = """%%html
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
void main(void){ gl_FragColor = vec4(ex_Color,1.0); }
</script>
"""

INIT_CUSTOM = r"""
function initCustom(app, vertId, fragId){
  var vertsrc = document.getElementById(vertId).text;
  var fragsrc = document.getElementById(fragId).text;
  app.shaderprog = new DEECshader(app.gl);
  app.shaderprog.srcShaders(vertsrc, fragsrc);
  app.gl.enable(app.gl.DEPTH_TEST);
  app.gl.clearColor(1,1,1,1);
}
function makeBuf(gl, data){
  var b = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, b);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(data), gl.STATIC_DRAW);
  return b;
}
function draw2(app, vbuf, cbuf, n, mode){
  var gl = app.gl;
  gl.bindBuffer(gl.ARRAY_BUFFER, vbuf);
  var lp = gl.getAttribLocation(app.shaderprog.shaderProgram, 'in_Position');
  gl.vertexAttribPointer(lp, 2, gl.FLOAT, false, 0, 0);
  gl.enableVertexAttribArray(lp);
  gl.bindBuffer(gl.ARRAY_BUFFER, cbuf);
  var lc = gl.getAttribLocation(app.shaderprog.shaderProgram, 'in_Color');
  gl.vertexAttribPointer(lc, 3, gl.FLOAT, false, 0, 0);
  gl.enableVertexAttribArray(lc);
  app.shaderprog.startUsing();
  gl.drawArrays(mode, 0, n);
  app.shaderprog.stopUsing();
}
"""

TRI_V = "[0.0,0.7, -0.6,-0.5, 0.6,-0.5]"
TRI_C = "[1,0,0, 0,1,0, 0,0,1]"

ex3 = [
    md("# CGRA Solutions — Chapter 3 (Ex 3.1–3.7)\nShaders + uniforms. Open with **Voilà**."),
    code(LIBS),
    code(
        DEFAULT_SHADERS
        + """
<script id="vert-31" type="x-shader/x-vertex">
precision highp float;
attribute vec2 in_Position;
attribute vec3 in_Color;
varying vec3 ex_Color;
void main(void){
  // Ex 3.1: scale by 0.5
  gl_Position = vec4(in_Position.x * 0.5, in_Position.y * 0.5, 0.0, 1.0);
  ex_Color = in_Color;
}
</script>
<script id="vert-32" type="x-shader/x-vertex">
precision highp float;
attribute vec2 in_Position;
attribute vec3 in_Color;
varying vec3 ex_Color;
void main(void){
  gl_Position = vec4(in_Position.x, in_Position.y, 0.0, 1.0);
  // Ex 3.2: red always 1
  ex_Color = vec3(1.0, in_Color.g, in_Color.b);
}
</script>
<script id="frag-33" type="x-shader/x-fragment">
precision highp float;
varying vec3 ex_Color;
void main(void){
  // Ex 3.3: blue threshold
  float blue = ex_Color.b < 0.5 ? 0.0 : 1.0;
  gl_FragColor = vec4(ex_Color.r, ex_Color.g, blue, 1.0);
}
</script>
<script id="vert-34" type="x-shader/x-vertex">
precision highp float;
attribute vec2 in_Position;
attribute vec3 in_Color;
varying vec3 ex_Color;
uniform float timepar;
void main(void){
  float K1 = 0.2;
  float K2 = 500.0;
  float y = in_Position.y + K1 * sin(timepar / K2);
  gl_Position = vec4(in_Position.x, y, 0.0, 1.0);
  ex_Color = in_Color;
}
</script>
<script id="vert-35" type="x-shader/x-vertex">
precision highp float;
attribute vec2 in_Position;
attribute vec3 in_Color;
varying vec3 ex_Color;
uniform float timepar;
void main(void){
  float K2 = 500.0;
  float scale = 0.5 + 0.25 * sin(timepar / K2);
  gl_Position = vec4(in_Position.x * scale, in_Position.y * scale, 0.0, 1.0);
  ex_Color = in_Color;
}
</script>
<script id="vert-36" type="x-shader/x-vertex">
precision highp float;
attribute vec2 in_Position;
attribute vec3 in_Color;
varying vec3 ex_Color;
uniform float timepar;
void main(void){
  float ang = timepar / 1000.0;
  float c = cos(ang);
  float s = sin(ang);
  float x = in_Position.x * c - in_Position.y * s;
  float y = in_Position.x * s + in_Position.y * c;
  gl_Position = vec4(x, y, 0.0, 1.0);
  ex_Color = in_Color;
}
</script>
<script id="frag-37" type="x-shader/x-fragment">
precision highp float;
varying vec3 ex_Color;
uniform float timepar;
void main(void){
  float K2 = 500.0;
  float g = 0.5 + 0.5 * sin(timepar / K2);
  gl_FragColor = vec4(ex_Color.r, g, ex_Color.b, 1.0);
}
</script>
"""
    ),
    md("## Ex 3.1 — vertex shader scale 0.5"),
    code(
        "%%html\n<canvas id=\"c31\" width=\"400\" height=\"400\" style=\"border:2px solid #000;\"></canvas>\n<script>\n"
        + INIT_CUSTOM
        + f"""
class App31 extends DEECapp{{
  initialize(){{
    initCustom(this,'vert-31','my-fragment-shader');
    this.vbuf = makeBuf(this.gl, {TRI_V});
    this.cbuf = makeBuf(this.gl, {TRI_C});
  }}
  render(){{
    this.gl.clear(this.gl.COLOR_BUFFER_BIT);
    draw2(this,this.vbuf,this.cbuf,3,this.gl.TRIANGLES);
  }}
}}
new App31('c31').run();
</script>
"""
    ),
    md("## Ex 3.2 — red component always 1"),
    code(
        "%%html\n<canvas id=\"c32\" width=\"400\" height=\"400\" style=\"border:2px solid #000;\"></canvas>\n<script>\n"
        + INIT_CUSTOM
        + f"""
class App32 extends DEECapp{{
  initialize(){{
    initCustom(this,'vert-32','my-fragment-shader');
    this.vbuf = makeBuf(this.gl, {TRI_V});
    this.cbuf = makeBuf(this.gl, {TRI_C});
  }}
  render(){{
    this.gl.clear(this.gl.COLOR_BUFFER_BIT);
    draw2(this,this.vbuf,this.cbuf,3,this.gl.TRIANGLES);
  }}
}}
new App32('c32').run();
</script>
"""
    ),
    md("## Ex 3.3 — fragment blue threshold"),
    code(
        "%%html\n<canvas id=\"c33\" width=\"400\" height=\"400\" style=\"border:2px solid #000;\"></canvas>\n<script>\n"
        + INIT_CUSTOM
        + f"""
class App33 extends DEECapp{{
  initialize(){{
    initCustom(this,'my-vertex-shader','frag-33');
    this.vbuf = makeBuf(this.gl, {TRI_V});
    this.cbuf = makeBuf(this.gl, {TRI_C});
  }}
  render(){{
    this.gl.clear(this.gl.COLOR_BUFFER_BIT);
    draw2(this,this.vbuf,this.cbuf,3,this.gl.TRIANGLES);
  }}
}}
new App33('c33').run();
</script>
"""
    ),
    md("## Ex 3.4 — y += K1*sin(time/K2) via uniform"),
    code(
        "%%html\n<canvas id=\"c34\" width=\"400\" height=\"400\" style=\"border:2px solid #000;\"></canvas>\n<script>\n"
        + INIT_CUSTOM
        + f"""
class App34 extends DEECapp{{
  initialize(){{
    initCustom(this,'vert-34','my-fragment-shader');
    this.vbuf = makeBuf(this.gl, {TRI_V});
    this.cbuf = makeBuf(this.gl, {TRI_C});
    this.t0 = Date.now();
    this.timeLoc = null;
  }}
  render(){{
    var timevariable = (Date.now()-this.t0)*1.0;
    this.shaderprog.startUsing();
    if(this.timeLoc===null)
      this.timeLoc = this.gl.getUniformLocation(this.shaderprog.shaderProgram,'timepar');
    this.gl.uniform1f(this.timeLoc, timevariable);
    this.shaderprog.stopUsing();
    this.gl.clear(this.gl.COLOR_BUFFER_BIT);
    draw2(this,this.vbuf,this.cbuf,3,this.gl.TRIANGLES);
  }}
}}
new App34('c34').run();
</script>
"""
    ),
    md("## Ex 3.5 — pulsing scale with time"),
    code(
        "%%html\n<canvas id=\"c35\" width=\"400\" height=\"400\" style=\"border:2px solid #000;\"></canvas>\n<script>\n"
        + INIT_CUSTOM
        + f"""
class App35 extends DEECapp{{
  initialize(){{
    initCustom(this,'vert-35','my-fragment-shader');
    this.vbuf = makeBuf(this.gl, {TRI_V});
    this.cbuf = makeBuf(this.gl, {TRI_C});
    this.t0 = Date.now();
    this.timeLoc = null;
  }}
  render(){{
    var timevariable = (Date.now()-this.t0)*1.0;
    this.shaderprog.startUsing();
    if(this.timeLoc===null)
      this.timeLoc = this.gl.getUniformLocation(this.shaderprog.shaderProgram,'timepar');
    this.gl.uniform1f(this.timeLoc, timevariable);
    this.shaderprog.stopUsing();
    this.gl.clear(this.gl.COLOR_BUFFER_BIT);
    draw2(this,this.vbuf,this.cbuf,3,this.gl.TRIANGLES);
  }}
}}
new App35('c35').run();
</script>
"""
    ),
    md("## Ex 3.6 — rotate in vertex shader with time"),
    code(
        "%%html\n<canvas id=\"c36\" width=\"400\" height=\"400\" style=\"border:2px solid #000;\"></canvas>\n<script>\n"
        + INIT_CUSTOM
        + f"""
class App36 extends DEECapp{{
  initialize(){{
    initCustom(this,'vert-36','my-fragment-shader');
    this.vbuf = makeBuf(this.gl, {TRI_V});
    this.cbuf = makeBuf(this.gl, {TRI_C});
    this.t0 = Date.now();
    this.timeLoc = null;
  }}
  render(){{
    var timevariable = (Date.now()-this.t0)*1.0;
    this.shaderprog.startUsing();
    if(this.timeLoc===null)
      this.timeLoc = this.gl.getUniformLocation(this.shaderprog.shaderProgram,'timepar');
    this.gl.uniform1f(this.timeLoc, timevariable);
    this.shaderprog.stopUsing();
    this.gl.clear(this.gl.COLOR_BUFFER_BIT);
    draw2(this,this.vbuf,this.cbuf,3,this.gl.TRIANGLES);
  }}
}}
new App36('c36').run();
</script>
"""
    ),
    md("## Ex 3.7 — green varies with time in fragment shader"),
    code(
        "%%html\n<canvas id=\"c37\" width=\"400\" height=\"400\" style=\"border:2px solid #000;\"></canvas>\n<script>\n"
        + INIT_CUSTOM
        + f"""
class App37 extends DEECapp{{
  initialize(){{
    initCustom(this,'my-vertex-shader','frag-37');
    this.vbuf = makeBuf(this.gl, {TRI_V});
    this.cbuf = makeBuf(this.gl, {TRI_C});
    this.t0 = Date.now();
    this.timeLoc = null;
  }}
  render(){{
    var timevariable = (Date.now()-this.t0)*1.0;
    this.shaderprog.startUsing();
    if(this.timeLoc===null)
      this.timeLoc = this.gl.getUniformLocation(this.shaderprog.shaderProgram,'timepar');
    this.gl.uniform1f(this.timeLoc, timevariable);
    this.shaderprog.stopUsing();
    this.gl.clear(this.gl.COLOR_BUFFER_BIT);
    draw2(this,this.vbuf,this.cbuf,3,this.gl.TRIANGLES);
  }}
}}
new App37('c37').run();
</script>
"""
    ),
]
save("CGRA_SOL_Ch3_Ex3.ipynb", ex3)

# ===================== EX4 =====================
ex4 = [
    md("# CGRA Solutions — Chapter 4 (Ex 4.1–4.4)\nGLM transforms. Open with **Voilà**."),
    code(GLM),
    code(LIBS),
    code(DEFAULT_SHADERS),
    md("## Ex 4.1 — small blue triangle follows sinusoid L→R, wraps"),
    code(
        r"""%%html
<canvas id="c41" width="400" height="400" style="border:2px solid #000;"></canvas>
<script>
class App41 extends DEECapp{
  initialize(){
    super.initialize();
    this.gl.clearColor(1,1,1,1);
    this.local = [
      glm.vec4(-0.05, 0.06, 0, 1),
      glm.vec4(-0.05,-0.06, 0, 1),
      glm.vec4( 0.05,-0.06, 0, 1)
    ];
    this.colors = [0,0,1, 0,0,1, 0,0,1];
    this.vertices = new Array(6);
    this.vbuf = this.gl.createBuffer();
    this.cbuf = this.gl.createBuffer();
    this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.cbuf);
    this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.colors), this.gl.STATIC_DRAW);
    this.t0 = Date.now();
  }
  render(){
    var t = (Date.now()-this.t0)/1000.0;
    var x = -1.0 + ((t*0.3) % 2.0); // wrap -1..1
    if(x > 1) x -= 2;
    var y = 0.4 * Math.sin(2.0 * Math.PI * x);
    var T = glm.mat4(1.0);
    T[3] = glm.vec4(x, y, 0, 1);
    for(var i=0;i<3;i++){
      var p = T['*'](this.local[i]);
      this.vertices[2*i]=p.x; this.vertices[2*i+1]=p.y;
    }
    this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.vbuf);
    this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.vertices), this.gl.DYNAMIC_DRAW);
    this.gl.clear(this.gl.COLOR_BUFFER_BIT);
    this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.vbuf);
    var lp=this.gl.getAttribLocation(this.shaderprog.shaderProgram,'in_Position');
    this.gl.vertexAttribPointer(lp,2,this.gl.FLOAT,false,0,0);
    this.gl.enableVertexAttribArray(lp);
    this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.cbuf);
    var lc=this.gl.getAttribLocation(this.shaderprog.shaderProgram,'in_Color');
    this.gl.vertexAttribPointer(lc,3,this.gl.FLOAT,false,0,0);
    this.gl.enableVertexAttribArray(lc);
    this.shaderprog.startUsing();
    this.gl.drawArrays(this.gl.TRIANGLES,0,3);
    this.shaderprog.stopUsing();
  }
}
new App41('c41').run();
</script>
"""
    ),
    md("## Ex 4.2 — same + rotate while moving"),
    code(
        r"""%%html
<canvas id="c42" width="400" height="400" style="border:2px solid #000;"></canvas>
<script>
class App42 extends DEECapp{
  initialize(){
    super.initialize();
    this.gl.clearColor(1,1,1,1);
    this.local = [glm.vec4(-0.05,0.06,0,1), glm.vec4(-0.05,-0.06,0,1), glm.vec4(0.05,-0.06,0,1)];
    this.colors = [0,0,1, 0,0.5,1, 0,1,1];
    this.vertices = new Array(6);
    this.vbuf = this.gl.createBuffer();
    this.cbuf = this.gl.createBuffer();
    this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.cbuf);
    this.gl.bufferData(this.gl.ARRAY_BUFFER,new Float32Array(this.colors),this.gl.STATIC_DRAW);
    this.t0 = Date.now();
  }
  render(){
    var t=(Date.now()-this.t0)/1000.0;
    var x = -1.0 + ((t*0.3)%2.0); if(x>1)x-=2;
    var y = 0.4*Math.sin(2*Math.PI*x);
    var q = glm.angleAxis(t, glm.vec3(0,0,1));
    var R = glm.toMat4(q);
    var T = glm.mat4(1.0); T[3]=glm.vec4(x,y,0,1);
    var M = T['*'](R); // rotate then translate
    for(var i=0;i<3;i++){
      var p=M['*'](this.local[i]);
      this.vertices[2*i]=p.x; this.vertices[2*i+1]=p.y;
    }
    this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.vbuf);
    this.gl.bufferData(this.gl.ARRAY_BUFFER,new Float32Array(this.vertices),this.gl.DYNAMIC_DRAW);
    this.gl.clear(this.gl.COLOR_BUFFER_BIT);
    this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.vbuf);
    var lp=this.gl.getAttribLocation(this.shaderprog.shaderProgram,'in_Position');
    this.gl.vertexAttribPointer(lp,2,this.gl.FLOAT,false,0,0);
    this.gl.enableVertexAttribArray(lp);
    this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.cbuf);
    var lc=this.gl.getAttribLocation(this.shaderprog.shaderProgram,'in_Color');
    this.gl.vertexAttribPointer(lc,3,this.gl.FLOAT,false,0,0);
    this.gl.enableVertexAttribArray(lc);
    this.shaderprog.startUsing();
    this.gl.drawArrays(this.gl.TRIANGLES,0,3);
    this.shaderprog.stopUsing();
  }
}
new App42('c42').run();
</script>
"""
    ),
    md("## Ex 4.3 — rotating rectangle under moving triangle"),
    code(
        r"""%%html
<canvas id="c43" width="400" height="400" style="border:2px solid #000;"></canvas>
<script>
class App43 extends DEECapp{
  initialize(){
    super.initialize();
    this.gl.clearColor(1,1,1,1);
    this.triLocal=[glm.vec4(-0.05,0.06,0,1),glm.vec4(-0.05,-0.06,0,1),glm.vec4(0.05,-0.06,0,1)];
    this.rectLocal=[
      glm.vec4(-0.15,-0.08,0,1),glm.vec4(0.15,-0.08,0,1),glm.vec4(0.15,0.08,0,1),
      glm.vec4(-0.15,-0.08,0,1),glm.vec4(0.15,0.08,0,1),glm.vec4(-0.15,0.08,0,1)
    ];
    this.triC=[0,0,1,0,0,1,0,0,1];
    this.rectC=[1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0];
    this.triV=new Array(6); this.rectV=new Array(12);
    this.tv=this.gl.createBuffer(); this.rv=this.gl.createBuffer();
    this.tc=this.gl.createBuffer(); this.rc=this.gl.createBuffer();
    this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.tc);
    this.gl.bufferData(this.gl.ARRAY_BUFFER,new Float32Array(this.triC),this.gl.STATIC_DRAW);
    this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.rc);
    this.gl.bufferData(this.gl.ARRAY_BUFFER,new Float32Array(this.rectC),this.gl.STATIC_DRAW);
    this.t0=Date.now();
  }
  draw(vbuf,cbuf,arr,n){
    this.gl.bindBuffer(this.gl.ARRAY_BUFFER,vbuf);
    this.gl.bufferData(this.gl.ARRAY_BUFFER,new Float32Array(arr),this.gl.DYNAMIC_DRAW);
    var lp=this.gl.getAttribLocation(this.shaderprog.shaderProgram,'in_Position');
    this.gl.vertexAttribPointer(lp,2,this.gl.FLOAT,false,0,0);
    this.gl.enableVertexAttribArray(lp);
    this.gl.bindBuffer(this.gl.ARRAY_BUFFER,cbuf);
    var lc=this.gl.getAttribLocation(this.shaderprog.shaderProgram,'in_Color');
    this.gl.vertexAttribPointer(lc,3,this.gl.FLOAT,false,0,0);
    this.gl.enableVertexAttribArray(lc);
    this.shaderprog.startUsing();
    this.gl.drawArrays(this.gl.TRIANGLES,0,n);
    this.shaderprog.stopUsing();
  }
  render(){
    var t=(Date.now()-this.t0)/1000.0;
    var x=-1+((t*0.3)%2); if(x>1)x-=2;
    var y=0.4*Math.sin(2*Math.PI*x);
    var qT=glm.angleAxis(t,glm.vec3(0,0,1));
    var RT=glm.toMat4(qT);
    var TT=glm.mat4(1.0); TT[3]=glm.vec4(x,y,0,1);
    var MT=TT['*'](RT);
    for(var i=0;i<3;i++){var p=MT['*'](this.triLocal[i]); this.triV[2*i]=p.x; this.triV[2*i+1]=p.y;}
    var qR=glm.angleAxis(-0.7*t,glm.vec3(0,0,1));
    var RR=glm.toMat4(qR);
    var TR=glm.mat4(1.0); TR[3]=glm.vec4(0,-0.55,0,1);
    var MR=TR['*'](RR);
    for(var i=0;i<6;i++){var p=MR['*'](this.rectLocal[i]); this.rectV[2*i]=p.x; this.rectV[2*i+1]=p.y;}
    this.gl.clear(this.gl.COLOR_BUFFER_BIT);
    this.draw(this.rv,this.rc,this.rectV,6);
    this.draw(this.tv,this.tc,this.triV,3);
  }
}
new App43('c43').run();
</script>
"""
    ),
    md("## Ex 4.4 — clock (hour / minute / second hands as rectangles)"),
    code(
        r"""%%html
<canvas id="c44" width="400" height="400" style="border:2px solid #000;"></canvas>
<script>
class App44 extends DEECapp{
  initialize(){
    super.initialize();
    this.gl.clearColor(1,1,1,1);
    // rectangle pointing UP (y+), pivot at origin bottom-center style: from (0,0) upward
    // hand local: thin rectangle along +Y
    this.makeHand = function(len, halfW){
      return [
        glm.vec4(-halfW, 0, 0, 1),
        glm.vec4( halfW, 0, 0, 1),
        glm.vec4( halfW, len, 0, 1),
        glm.vec4(-halfW, 0, 0, 1),
        glm.vec4( halfW, len, 0, 1),
        glm.vec4(-halfW, len, 0, 1)
      ];
    };
    this.hLocal = this.makeHand(0.35, 0.025);
    this.mLocal = this.makeHand(0.50, 0.018);
    this.sLocal = this.makeHand(0.62, 0.010);
    this.hC=[0.2,0.2,0.2, 0.2,0.2,0.2, 0.2,0.2,0.2, 0.2,0.2,0.2, 0.2,0.2,0.2, 0.2,0.2,0.2];
    this.mC=[0.1,0.1,0.6, 0.1,0.1,0.6, 0.1,0.1,0.6, 0.1,0.1,0.6, 0.1,0.1,0.6, 0.1,0.1,0.6];
    this.sC=[0.8,0,0, 0.8,0,0, 0.8,0,0, 0.8,0,0, 0.8,0,0, 0.8,0,0];
    // clock face circle approx as many triangles optional - skip, just hands
    this.hv=new Array(12); this.mv=new Array(12); this.sv=new Array(12);
    this.hb=this.gl.createBuffer(); this.mb=this.gl.createBuffer(); this.sb=this.gl.createBuffer();
    this.hc=this.gl.createBuffer(); this.mc=this.gl.createBuffer(); this.sc=this.gl.createBuffer();
    this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.hc); this.gl.bufferData(this.gl.ARRAY_BUFFER,new Float32Array(this.hC),this.gl.STATIC_DRAW);
    this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.mc); this.gl.bufferData(this.gl.ARRAY_BUFFER,new Float32Array(this.mC),this.gl.STATIC_DRAW);
    this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.sc); this.gl.bufferData(this.gl.ARRAY_BUFFER,new Float32Array(this.sC),this.gl.STATIC_DRAW);
  }
  fill(local, ang, out){
    var q=glm.angleAxis(ang, glm.vec3(0,0,1));
    var R=glm.toMat4(q);
    for(var i=0;i<6;i++){
      var p=R['*'](local[i]);
      out[2*i]=p.x; out[2*i+1]=p.y;
    }
  }
  draw(vbuf,cbuf,arr){
    this.gl.bindBuffer(this.gl.ARRAY_BUFFER,vbuf);
    this.gl.bufferData(this.gl.ARRAY_BUFFER,new Float32Array(arr),this.gl.DYNAMIC_DRAW);
    var lp=this.gl.getAttribLocation(this.shaderprog.shaderProgram,'in_Position');
    this.gl.vertexAttribPointer(lp,2,this.gl.FLOAT,false,0,0);
    this.gl.enableVertexAttribArray(lp);
    this.gl.bindBuffer(this.gl.ARRAY_BUFFER,cbuf);
    var lc=this.gl.getAttribLocation(this.shaderprog.shaderProgram,'in_Color');
    this.gl.vertexAttribPointer(lc,3,this.gl.FLOAT,false,0,0);
    this.gl.enableVertexAttribArray(lc);
    this.shaderprog.startUsing();
    this.gl.drawArrays(this.gl.TRIANGLES,0,6);
    this.shaderprog.stopUsing();
  }
  render(){
    var today = new Date();
    var hours = today.getHours() % 12;
    var minutes = today.getMinutes();
    var secs = today.getSeconds();
    // angles: 12 o'clock = up = 0 in our local (+Y). Clockwise negative Z rotation in RH? 
    // Screen: clockwise for clock. angleAxis positive is CCW. So use negative.
    var angS = -secs * (2*Math.PI/60);
    var angM = -(minutes + secs/60) * (2*Math.PI/60);
    var angH = -(hours + minutes/60) * (2*Math.PI/12);
    this.fill(this.hLocal, angH, this.hv);
    this.fill(this.mLocal, angM, this.mv);
    this.fill(this.sLocal, angS, this.sv);
    this.gl.clear(this.gl.COLOR_BUFFER_BIT);
    this.draw(this.hb,this.hc,this.hv);
    this.draw(this.mb,this.mc,this.mv);
    this.draw(this.sb,this.sc,this.sv);
  }
}
new App44('c44').run();
</script>
"""
    ),
]
save("CGRA_SOL_Ch4_Ex4.ipynb", ex4)

readme = """UPLOAD TO JUPYTERHUB
====================
1. VPN ON
2. https://seeds.deec.uc.pt/CGRA/
3. Upload these 4 notebooks from folder SOLUTIONS:
   - CGRA_SOL_Ch1_Ex1.ipynb   (Ex 1.1-1.4)
   - CGRA_SOL_Ch2_Ex2.ipynb   (Ex 2.1-2.7)
   - CGRA_SOL_Ch3_Ex3.ipynb   (Ex 3.1-3.7)
   - CGRA_SOL_Ch4_Ex4.ipynb   (Ex 4.1-4.4)
4. Open one → Voilà (NOT Run)
5. Scroll to see each exercise canvas

ALSO copy official examples from Jupyter examples/ folder for reference.
"""
(OUT / "HOW_TO_UPLOAD.txt").write_text(readme, encoding="utf-8")
print("all done")
