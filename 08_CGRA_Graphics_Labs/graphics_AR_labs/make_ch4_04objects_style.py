"""Ch4: exact 04Objects libraries; CGRAobject; one exercise per section; basic glm."""
import json
from pathlib import Path

OUT = Path(r"c:\Users\Lenovo\Downloads\computer architecture\graphics_AR_labs\BASIC_SOLUTIONS")
OUT.mkdir(exist_ok=True)


def md(s):
    return {"cell_type": "markdown", "metadata": {}, "source": [ln + "\n" for ln in s.split("\n")]}


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


# EXACT libraries from official 04Objects (https)
LIBS = r'''%%html
<script src="https://is3l.isr.uc.pt/~pm/CGRA/JS/deecshader.js"></script>
<script src="https://is3l.isr.uc.pt/~pm/CGRA/JS/deecapp.js"></script>
<script src="https://is3l.isr.uc.pt/~pm/CGRA/JS/cgraobject.js"></script>
<script src="https://git.io/glm-js.min.js"></script>
'''

# EXACT shaders from 04Objects (MVP + vec3)
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

cells = [
    md("""# Chapter 4 — like official `04Objects`

**Libraries (same as professor example):**
- `deecshader.js` — shader helper (professor name is still DEEC)
- `deecapp.js` — app loop (`DEECapp`)
- `cgraobject.js` — **CGRA** objects (`CGRAobject`, `setModelTransformation`, `drawit`)
- `glm-js` — matrices (`mat4`, translate, rotate, scale)

**Important:** In `04Objects`, professor still uses `DEECapp` + `DEECshader`.  
The **CGRA** part is `CGRAobject` (not replacing DEECapp).

## What is `mat4`?
`mat4` = **4×4 matrix**.  
With homogeneous coordinates we use 4D points `(x,y,z,1)`.  
One `mat4` can do **scale + rotate + translate** together.

## What is `MVP`?
`MVP` = **Model × View × Projection** (one matrix sent to the shader).

| Letter | Meaning | Simple idea |
|---|---|---|
| **M** Model | object move/rotate/scale | where the triangle is |
| **V** View | camera | we use identity for now |
| **P** Projection | 3D→screen | identity for now |

In shader:
`gl_Position = MVP * vec4(position, 1.0);`

`CGRAobject.drawit()` builds MVP for you from `setModelTransformation(...)`.

Open with **Voilà**.
"""),
    code(LIBS),
    code(VERT),
    code(FRAG),

    # ===== EX 4.1 =====
    md("## Exercise 4.1 — small blue triangle on sinusoid\nOnly **translate** with `glm`."),
    code(r'''%%html
<canvas id="canvas41" width="400" height="400" style="border:2px solid #000000;">
      Error: Your browser does not support the HTML canvas tag.
</canvas>

<script id="myapp41">

// CGRA object = triangle
class triangle41 extends CGRAobject{
    constructor(glcontext){
        super(glcontext);
        this.numvertices = 3;
        // small blue triangle (local coords)
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

class myapp41 extends DEECapp{
    counter=0;
    initialize(){
        // like 04Objects: no super.initialize(), make shader ourselves
        var fragsrc = document.getElementById("my-fragment-shader").text;
        var vertsrc = document.getElementById("my-vertex-shader").text;
        this.shaderprog = new DEECshader(this.gl);
        this.shaderprog.srcShaders(vertsrc,fragsrc);

        this.gl.disable(this.gl.DEPTH_TEST);
        this.gl.clearColor(1.0,1.0,1.0,1.0);

        this.mytriangle = new triangle41(this.gl);
        this.mytriangle.setShader(this.shaderprog);
        this.starttime = Date.now();
    }

    render(){
        this.gl.clear(this.gl.COLOR_BUFFER_BIT);
        this.counter++;

        var t = (Date.now() - this.starttime) * 0.001;
        var x = -1.0 + (t * 0.25) % 2.0;          // left -> right
        var y = 0.4 * Math.sin(3.1416 * x);       // sinusoid

        // mat4 translation only
        var T = glm.translate(glm.mat4(1.0), glm.vec3(x, y, 0.0));
        this.mytriangle.setModelTransformation(T);  // this becomes Model in MVP
        this.mytriangle.drawit();
    }
}

var app41 = new myapp41('canvas41');
app41.run();

</script>
'''),

    # ===== EX 4.2 =====
    md("## Exercise 4.2 — move + rotate\n`M = Translate * Rotate` (like Objects example)."),
    code(r'''%%html
<canvas id="canvas42" width="400" height="400" style="border:2px solid #000000;">
      Error: Your browser does not support the HTML canvas tag.
</canvas>

<script id="myapp42">

class triangle42 extends CGRAobject{
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

class myapp42 extends DEECapp{
    counter=0;
    initialize(){
        var fragsrc = document.getElementById("my-fragment-shader").text;
        var vertsrc = document.getElementById("my-vertex-shader").text;
        this.shaderprog = new DEECshader(this.gl);
        this.shaderprog.srcShaders(vertsrc,fragsrc);
        this.gl.disable(this.gl.DEPTH_TEST);
        this.gl.clearColor(1.0,1.0,1.0,1.0);

        this.mytriangle = new triangle42(this.gl);
        this.mytriangle.setShader(this.shaderprog);
        this.starttime = Date.now();
    }

    render(){
        this.gl.clear(this.gl.COLOR_BUFFER_BIT);
        this.counter++;

        var t = (Date.now() - this.starttime) * 0.001;
        var x = -1.0 + (t * 0.25) % 2.0;
        var y = 0.4 * Math.sin(3.1416 * x);

        // rotate around Z (like 04Objects)
        var R = glm.rotate(glm.mat4(1.0), glm.radians(this.counter), glm.vec3(0.0,0.0,1.0));
        var T = glm.translate(glm.mat4(1.0), glm.vec3(x, y, 0.0));

        // first rotate, then translate
        var M = T['*'](R);
        this.mytriangle.setModelTransformation(M);
        this.mytriangle.drawit();
    }
}

var app42 = new myapp42('canvas42');
app42.run();

</script>
'''),

    # ===== EX 4.3 =====
    md("## Exercise 4.3 — rotating rectangle under moving triangle\nTwo `CGRAobject`s (like two triangles in 04Objects)."),
    code(r'''%%html
<canvas id="canvas43" width="400" height="400" style="border:2px solid #000000;">
      Error: Your browser does not support the HTML canvas tag.
</canvas>

<script id="myapp43">

class triangle43 extends CGRAobject{
    constructor(glcontext){
        super(glcontext);
        this.numvertices = 3;
        var vertices =
            [ -0.05,  0.06, 0 ,
              -0.05, -0.06, 0 ,
               0.05, -0.06, 0 ];
        var colors = [0,0,1, 0,0,1, 0,0,1];
        this.vertexbuffer=this.gl.createBuffer();
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.vertexbuffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(vertices), this.gl.STATIC_DRAW);
        this.colorbuffer = this.gl.createBuffer();
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.colorbuffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(colors), this.gl.STATIC_DRAW);
    }
}

class rectangle43 extends CGRAobject{
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

class myapp43 extends DEECapp{
    counter=0;
    initialize(){
        var fragsrc = document.getElementById("my-fragment-shader").text;
        var vertsrc = document.getElementById("my-vertex-shader").text;
        this.shaderprog = new DEECshader(this.gl);
        this.shaderprog.srcShaders(vertsrc,fragsrc);
        this.gl.disable(this.gl.DEPTH_TEST);
        this.gl.clearColor(1.0,1.0,1.0,1.0);

        this.mytriangle = new triangle43(this.gl);
        this.mytriangle.setShader(this.shaderprog);
        this.myrect = new rectangle43(this.gl);
        this.myrect.setShader(this.shaderprog);
        this.starttime = Date.now();
    }

    render(){
        this.gl.clear(this.gl.COLOR_BUFFER_BIT);
        this.counter++;

        var t = (Date.now() - this.starttime) * 0.001;
        var x = -1.0 + (t * 0.25) % 2.0;
        var y = 0.4 * Math.sin(3.1416 * x);

        // rectangle under (rotate + translate down)
        var R2 = glm.rotate(glm.mat4(1.0), glm.radians(-this.counter), glm.vec3(0,0,1));
        var T2 = glm.translate(glm.mat4(1.0), glm.vec3(0.0, -0.55, 0.0));
        this.myrect.setModelTransformation(T2['*'](R2));
        this.myrect.drawit();

        // triangle on sinusoid
        var R1 = glm.rotate(glm.mat4(1.0), glm.radians(this.counter), glm.vec3(0,0,1));
        var T1 = glm.translate(glm.mat4(1.0), glm.vec3(x, y, 0.0));
        this.mytriangle.setModelTransformation(T1['*'](R1));
        this.mytriangle.drawit();
    }
}

var app43 = new myapp43('canvas43');
app43.run();

</script>
'''),

    # ===== EX 4.4 =====
    md("## Exercise 4.4 — clock (3 hands)\nEach hand = `CGRAobject` rectangle + `glm.scale` + `glm.rotate`."),
    code(r'''%%html
<canvas id="canvas44" width="400" height="400" style="border:2px solid #000000;">
      Error: Your browser does not support the HTML canvas tag.
</canvas>

<script id="myapp44">

class hand extends CGRAobject{
    constructor(glcontext, r,g,b){
        super(glcontext);
        this.numvertices = 6;
        // points UP (along +Y), length 1 — we scale later
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

class myapp44 extends DEECapp{
    initialize(){
        var fragsrc = document.getElementById("my-fragment-shader").text;
        var vertsrc = document.getElementById("my-vertex-shader").text;
        this.shaderprog = new DEECshader(this.gl);
        this.shaderprog.srcShaders(vertsrc,fragsrc);
        this.gl.disable(this.gl.DEPTH_TEST);
        this.gl.clearColor(1.0,1.0,1.0,1.0);

        this.hour = new hand(this.gl, 0.2,0.2,0.2);
        this.min  = new hand(this.gl, 0.0,0.0,0.7);
        this.sec  = new hand(this.gl, 0.8,0.0,0.0);
        this.hour.setShader(this.shaderprog);
        this.min.setShader(this.shaderprog);
        this.sec.setShader(this.shaderprog);
    }

    drawHand(obj, angleDeg, length){
        var S = glm.scale(glm.mat4(1.0), glm.vec3(1.0, length, 1.0));
        // negative angle = clockwise (clock)
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

        var angS = -secs * 6.0;
        var angM = -(minutes + secs/60.0) * 6.0;
        var angH = -(hours + minutes/60.0) * 30.0;

        this.drawHand(this.hour, angH, 0.35);
        this.drawHand(this.min,  angM, 0.50);
        this.drawHand(this.sec,  angS, 0.65);
    }
}

var app44 = new myapp44('canvas44');
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
