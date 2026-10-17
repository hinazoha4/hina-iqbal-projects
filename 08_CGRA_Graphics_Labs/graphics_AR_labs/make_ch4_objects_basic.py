"""Ch4 basic = same style as official 04Objects example (CGRAobject + glm)."""
import json
from pathlib import Path

OUT = Path(r"c:\Users\Lenovo\Downloads\computer architecture\graphics_AR_labs\BASIC_SOLUTIONS")
OUT.mkdir(exist_ok=True)


def md(s):
    lines = [ln + "\n" for ln in s.split("\n")]
    return {"cell_type": "markdown", "metadata": {}, "source": lines}


def code(s):
    if not s.endswith("\n"):
        s += "\n"
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [ln + "\n" for ln in s.split("\n")],
    }


LIBS = r'''%%html
<script src="https://is3l.isr.uc.pt/~pm/CGRA/JS/deecshader.js"></script>
<script src="https://is3l.isr.uc.pt/~pm/CGRA/JS/deecapp.js"></script>
<script src="https://is3l.isr.uc.pt/~pm/CGRA/JS/cgraobject.js"></script>
<script src="https://git.io/glm-js.min.js"></script>
'''

VERT = r'''%%html
<script id="my-vertex-shader" type="x-shader/x-vertex">
precision mediump float;

attribute  vec3 in_Position;
attribute  vec3 in_Color;
uniform mat4 MVP;

varying  vec3 ex_Color;

void main(void) {
    gl_Position = MVP * vec4(in_Position.x, in_Position.y, in_Position.z, 1.0);
    ex_Color = in_Color;
}
</script>
'''

FRAG = r'''%%html
<script id="my-fragment-shader" type="x-shader/x-fragment">
precision mediump float;

varying  vec3 ex_Color;

void main(void) {
    gl_FragColor = vec4(ex_Color,1.0);
}
</script>
'''

# shared object classes - like professor example, very simple
OBJECTS = r'''%%html
<script>
// small blue triangle (local size ~0.1)
class smallTriangle extends CGRAobject{
    constructor(glcontext){
        super(glcontext);
        this.numvertices = 3;
        var vertices =
            [ -0.05,  0.06, 0 ,
              -0.05, -0.06, 0 ,
               0.05, -0.06, 0 ];
        var colors = [
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0];
        this.vertexbuffer=this.gl.createBuffer();
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.vertexbuffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(vertices), this.gl.STATIC_DRAW);
        this.colorbuffer = this.gl.createBuffer();
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.colorbuffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(colors), this.gl.STATIC_DRAW);
    }
}

// red rectangle made of 2 triangles (local size about 0.3 x 0.15)
class redRect extends CGRAobject{
    constructor(glcontext){
        super(glcontext);
        this.numvertices = 6;
        var vertices =
            [ -0.15, -0.08, 0 ,
               0.15, -0.08, 0 ,
               0.15,  0.08, 0 ,
              -0.15, -0.08, 0 ,
               0.15,  0.08, 0 ,
              -0.15,  0.08, 0 ];
        var colors = [
            1,0,0, 1,0,0, 1,0,0,
            1,0,0, 1,0,0, 1,0,0];
        this.vertexbuffer=this.gl.createBuffer();
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.vertexbuffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(vertices), this.gl.STATIC_DRAW);
        this.colorbuffer = this.gl.createBuffer();
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.colorbuffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(colors), this.gl.STATIC_DRAW);
    }
}

// thin rectangle pointing UP (for clock hands) - length 1 in y, then we scale
class handRect extends CGRAobject{
    constructor(glcontext, r,g,b){
        super(glcontext);
        this.numvertices = 6;
        var vertices =
            [ -0.02, 0.0, 0 ,
               0.02, 0.0, 0 ,
               0.02, 1.0, 0 ,
              -0.02, 0.0, 0 ,
               0.02, 1.0, 0 ,
              -0.02, 1.0, 0 ];
        var colors = [
            r,g,b, r,g,b, r,g,b,
            r,g,b, r,g,b, r,g,b];
        this.vertexbuffer=this.gl.createBuffer();
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.vertexbuffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(vertices), this.gl.STATIC_DRAW);
        this.colorbuffer = this.gl.createBuffer();
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.colorbuffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(colors), this.gl.STATIC_DRAW);
    }
}

// helper: start shader like Objects example
function makeShader(app){
    var fragsrc = document.getElementById("my-fragment-shader").text;
    var vertsrc = document.getElementById("my-vertex-shader").text;
    app.shaderprog = new DEECshader(app.gl);
    app.shaderprog.srcShaders(vertsrc,fragsrc);
    app.gl.disable(app.gl.DEPTH_TEST);
    app.gl.clearColor(1.0,1.0,1.0,1.0);
}
</script>
'''

cells = [
    md("# Chapter 4 - basic (like Objects example)\nSame style as `04Objects`: `CGRAobject` + `glm` + `setModelTransformation` + `drawit`.\nOpen with **Voilà**."),
    code(LIBS),
    code(VERT),
    code(FRAG),
    code(OBJECTS),

    md("## Ex 4.1 - small blue triangle moves on a sinusoid (left → right)"),
    code(r'''%%html
<p>Ex 4.1</p>
<canvas id="c41" width="400" height="400" style="border:2px solid #000000;"></canvas>
<script>
class myapp41 extends DEECapp{
    counter=0;
    initialize(){
        makeShader(this);
        this.tri = new smallTriangle(this.gl);
        this.tri.setShader(this.shaderprog);
        this.starttime = Date.now();
    }
    render(){
        this.gl.clear(this.gl.COLOR_BUFFER_BIT);
        this.counter++;

        var t = (Date.now() - this.starttime) * 0.001;
        var x = -1.0 + (t * 0.25) % 2.0;   // wrap left to right
        var y = 0.4 * Math.sin(3.1416 * x);

        // only translation (basic)
        var T = glm.translate(glm.mat4(1.0), glm.vec3(x, y, 0.0));
        this.tri.setModelTransformation(T);
        this.tri.drawit();
    }
}
var app41 = new myapp41('c41');
app41.run();
</script>
'''),

    md("## Ex 4.2 - same + rotate (like Objects example)"),
    code(r'''%%html
<p>Ex 4.2</p>
<canvas id="c42" width="400" height="400" style="border:2px solid #000000;"></canvas>
<script>
class myapp42 extends DEECapp{
    counter=0;
    initialize(){
        makeShader(this);
        this.tri = new smallTriangle(this.gl);
        this.tri.setShader(this.shaderprog);
        this.starttime = Date.now();
    }
    render(){
        this.gl.clear(this.gl.COLOR_BUFFER_BIT);
        this.counter++;

        var t = (Date.now() - this.starttime) * 0.001;
        var x = -1.0 + (t * 0.25) % 2.0;
        var y = 0.4 * Math.sin(3.1416 * x);

        // rotate then translate (same idea as Objects example)
        var R = glm.rotate(glm.mat4(1.0), glm.radians(this.counter), glm.vec3(0,0,1));
        var T = glm.translate(glm.mat4(1.0), glm.vec3(x, y, 0.0));
        var M = T['*'](R);

        this.tri.setModelTransformation(M);
        this.tri.drawit();
    }
}
var app42 = new myapp42('c42');
app42.run();
</script>
'''),

    md("## Ex 4.3 - rotating rectangle under the moving triangle"),
    code(r'''%%html
<p>Ex 4.3</p>
<canvas id="c43" width="400" height="400" style="border:2px solid #000000;"></canvas>
<script>
class myapp43 extends DEECapp{
    counter=0;
    initialize(){
        makeShader(this);
        this.tri = new smallTriangle(this.gl);
        this.tri.setShader(this.shaderprog);
        this.rect = new redRect(this.gl);
        this.rect.setShader(this.shaderprog);
        this.starttime = Date.now();
    }
    render(){
        this.gl.clear(this.gl.COLOR_BUFFER_BIT);
        this.counter++;

        var t = (Date.now() - this.starttime) * 0.001;
        var x = -1.0 + (t * 0.25) % 2.0;
        var y = 0.4 * Math.sin(3.1416 * x);

        // rectangle: rotate + put below
        var Rrect = glm.rotate(glm.mat4(1.0), glm.radians(-this.counter), glm.vec3(0,0,1));
        var Trect = glm.translate(glm.mat4(1.0), glm.vec3(0.0, -0.55, 0.0));
        this.rect.setModelTransformation(Trect['*'](Rrect));
        this.rect.drawit();

        // triangle: rotate + move on sinusoid
        var Rtri = glm.rotate(glm.mat4(1.0), glm.radians(this.counter), glm.vec3(0,0,1));
        var Ttri = glm.translate(glm.mat4(1.0), glm.vec3(x, y, 0.0));
        this.tri.setModelTransformation(Ttri['*'](Rtri));
        this.tri.drawit();
    }
}
var app43 = new myapp43('c43');
app43.run();
</script>
'''),

    md("## Ex 4.4 - simple clock (3 hands)\nUses `Date()` like the PDF."),
    code(r'''%%html
<p>Ex 4.4</p>
<canvas id="c44" width="400" height="400" style="border:2px solid #000000;"></canvas>
<script>
class myapp44 extends DEECapp{
    initialize(){
        makeShader(this);
        // grey hour, blue minute, red second
        this.hour = new handRect(this.gl, 0.2, 0.2, 0.2);
        this.min  = new handRect(this.gl, 0.0, 0.0, 0.7);
        this.sec  = new handRect(this.gl, 0.8, 0.0, 0.0);
        this.hour.setShader(this.shaderprog);
        this.min.setShader(this.shaderprog);
        this.sec.setShader(this.shaderprog);
    }
    drawHand(obj, angleDeg, length){
        // scale length, then rotate (clock wise = negative)
        var S = glm.scale(glm.mat4(1.0), glm.vec3(1.0, length, 1.0));
        var R = glm.rotate(glm.mat4(1.0), glm.radians(angleDeg), glm.vec3(0,0,1));
        obj.setModelTransformation(R['*'](S));
        obj.drawit();
    }
    render(){
        this.gl.clear(this.gl.COLOR_BUFFER_BIT);

        var today = new Date();
        var hours = today.getHours() % 12;
        var minutes = today.getMinutes();
        var secs = today.getSeconds();

        // 12 o'clock is UP. Clockwise = negative angle in glm.rotate
        var angS = -secs * 6.0;                         // 360/60
        var angM = -(minutes + secs/60.0) * 6.0;
        var angH = -(hours + minutes/60.0) * 30.0;      // 360/12

        this.drawHand(this.hour, angH, 0.35);
        this.drawHand(this.min,  angM, 0.50);
        this.drawHand(this.sec,  angS, 0.65);
    }
}
var app44 = new myapp44('c44');
app44.run();
</script>
'''),
]

nb = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}
path = OUT / "Ch4_examples.ipynb"
path.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding="utf-8")
print("wrote", path)

explain = OUT / "Ch4_SAMJHO.txt"
explain.write_text(
"""Ch4 = Objects example style (basic)
=====================================

Same as professor 04Objects:
  - CGRAobject
  - setModelTransformation(matrix)
  - drawit()
  - glm.translate / glm.rotate / glm.scale

Libraries cell:
  deecshader.js, deecapp.js, cgraobject.js, glm-js

Shader has: uniform mat4 MVP

Ex 4.1  T = translate only, x along sinusoid
Ex 4.2  M = T * R   (rotate then move)
Ex 4.3  draw rect under, then triangle
Ex 4.4  3 hands with Date() hours/minutes/seconds

Upload Ch4_examples.ipynb -> Voila
""",
    encoding="utf-8",
)
print("done")
