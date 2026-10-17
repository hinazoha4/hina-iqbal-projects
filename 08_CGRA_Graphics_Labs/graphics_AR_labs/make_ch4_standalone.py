"""Four standalone Ch4 exercise notebooks - each fully executable like 04Objects."""
import json
from pathlib import Path

OUT = Path(r"c:\Users\Lenovo\Downloads\computer architecture\graphics_AR_labs\BASIC_SOLUTIONS")
OUT.mkdir(exist_ok=True)

LIBS = '''%%html
<script src="https://is3l.isr.uc.pt/~pm/CGRA/JS/deecshader.js"></script>
<script src="https://is3l.isr.uc.pt/~pm/CGRA/JS/deecapp.js"></script>
<script src="https://is3l.isr.uc.pt/~pm/CGRA/JS/cgraobject.js"></script>
<script src="https://git.io/glm-js.min.js"></script>
'''

VERT = '''%%html
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

FRAG = '''%%html
<script id="my-fragment-shader" type="x-shader/x-fragment">
precision mediump float;

varying  vec3 ex_Color;

void main(void) {
    gl_FragColor = vec4(ex_Color,1.0);
}
</script>
'''


def cell_md(s):
    return {"cell_type": "markdown", "metadata": {}, "source": [l + "\n" for l in s.split("\n")]}


def cell_code(s):
    if not s.endswith("\n"):
        s += "\n"
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [l + "\n" for l in s.split("\n")],
    }


def save(name, title, app_html):
    nb = {
        "cells": [
            cell_md(f"# {title}\nCopy of style from examples/04Objects.\nOpen with **Voilà** (do not use Run)."),
            cell_code(LIBS),
            cell_code(VERT),
            cell_code(FRAG),
            cell_code(app_html),
        ],
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    path = OUT / name
    path.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding="utf-8")
    print("wrote", name)


# ---- Ex 4.1 ----
save(
    "Ch4_Ex4_1.ipynb",
    "Exercise 4.1",
    r'''%%html
<canvas id="myCanvas" width="400" height="400" style="border:2px solid #000000;">
      Error: Your browser does not support the HTML canvas tag.
</canvas>

<script id="myapp">

class triangle extends CGRAobject{
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

class myapp extends DEECapp{
    counter=0;
    initialize(){
        var fragsrc = document.getElementById("my-fragment-shader").text;
        var vertsrc = document.getElementById("my-vertex-shader").text;
        this.shaderprog = new DEECshader(this.gl);
        this.shaderprog.srcShaders(vertsrc,fragsrc);
        this.gl.disable(this.gl.DEPTH_TEST);
        this.gl.clearColor(1.0,1.0,1.0,1.0);

        this.mytriangle = new triangle(this.gl);
        this.mytriangle.setShader(this.shaderprog);
        this.starttime = Date.now();
    }

    render(){
        this.gl.clear(this.gl.COLOR_BUFFER_BIT);
        this.counter++;

        var t = (Date.now() - this.starttime) * 0.001;
        var x = -1.0 + (t * 0.25) % 2.0;
        var y = 0.4 * Math.sin(3.1416 * x);

        var T = glm.translate(glm.mat4(1.0), glm.vec3(x, y, 0.0));
        this.mytriangle.setModelTransformation(T);
        this.mytriangle.drawit();
    }
}

var app = new myapp('myCanvas');
app.run();

</script>
''',
)

# ---- Ex 4.2 ----
save(
    "Ch4_Ex4_2.ipynb",
    "Exercise 4.2",
    r'''%%html
<canvas id="myCanvas" width="400" height="400" style="border:2px solid #000000;">
      Error: Your browser does not support the HTML canvas tag.
</canvas>

<script id="myapp">

class triangle extends CGRAobject{
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

class myapp extends DEECapp{
    counter=0;
    initialize(){
        var fragsrc = document.getElementById("my-fragment-shader").text;
        var vertsrc = document.getElementById("my-vertex-shader").text;
        this.shaderprog = new DEECshader(this.gl);
        this.shaderprog.srcShaders(vertsrc,fragsrc);
        this.gl.disable(this.gl.DEPTH_TEST);
        this.gl.clearColor(1.0,1.0,1.0,1.0);

        this.mytriangle = new triangle(this.gl);
        this.mytriangle.setShader(this.shaderprog);
        this.starttime = Date.now();
    }

    render(){
        this.gl.clear(this.gl.COLOR_BUFFER_BIT);
        this.counter++;

        var t = (Date.now() - this.starttime) * 0.001;
        var x = -1.0 + (t * 0.25) % 2.0;
        var y = 0.4 * Math.sin(3.1416 * x);

        var R = glm.rotate(glm.mat4(1.0), glm.radians(this.counter), glm.vec3(0.0,0.0,1.0));
        var T = glm.translate(glm.mat4(1.0), glm.vec3(x, y, 0.0));
        var M = T['*'](R);

        this.mytriangle.setModelTransformation(M);
        this.mytriangle.drawit();
    }
}

var app = new myapp('myCanvas');
app.run();

</script>
''',
)

# ---- Ex 4.3 ----
save(
    "Ch4_Ex4_3.ipynb",
    "Exercise 4.3",
    r'''%%html
<canvas id="myCanvas" width="400" height="400" style="border:2px solid #000000;">
      Error: Your browser does not support the HTML canvas tag.
</canvas>

<script id="myapp">

class triangle extends CGRAobject{
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

class rectangle extends CGRAobject{
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
            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0];
        this.vertexbuffer=this.gl.createBuffer();
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.vertexbuffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(vertices), this.gl.STATIC_DRAW);
        this.colorbuffer = this.gl.createBuffer();
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.colorbuffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(colors), this.gl.STATIC_DRAW);
    }
}

class myapp extends DEECapp{
    counter=0;
    initialize(){
        var fragsrc = document.getElementById("my-fragment-shader").text;
        var vertsrc = document.getElementById("my-vertex-shader").text;
        this.shaderprog = new DEECshader(this.gl);
        this.shaderprog.srcShaders(vertsrc,fragsrc);
        this.gl.disable(this.gl.DEPTH_TEST);
        this.gl.clearColor(1.0,1.0,1.0,1.0);

        this.mytriangle = new triangle(this.gl);
        this.mytriangle.setShader(this.shaderprog);
        this.myrectangle = new rectangle(this.gl);
        this.myrectangle.setShader(this.shaderprog);
        this.starttime = Date.now();
    }

    render(){
        this.gl.clear(this.gl.COLOR_BUFFER_BIT);
        this.counter++;

        var t = (Date.now() - this.starttime) * 0.001;
        var x = -1.0 + (t * 0.25) % 2.0;
        var y = 0.4 * Math.sin(3.1416 * x);

        var R2 = glm.rotate(glm.mat4(1.0), glm.radians(-this.counter), glm.vec3(0.0,0.0,1.0));
        var T2 = glm.translate(glm.mat4(1.0), glm.vec3(0.0, -0.55, 0.0));
        this.myrectangle.setModelTransformation(T2['*'](R2));
        this.myrectangle.drawit();

        var R1 = glm.rotate(glm.mat4(1.0), glm.radians(this.counter), glm.vec3(0.0,0.0,1.0));
        var T1 = glm.translate(glm.mat4(1.0), glm.vec3(x, y, 0.0));
        this.mytriangle.setModelTransformation(T1['*'](R1));
        this.mytriangle.drawit();
    }
}

var app = new myapp('myCanvas');
app.run();

</script>
''',
)

# ---- Ex 4.4 ----
save(
    "Ch4_Ex4_4.ipynb",
    "Exercise 4.4",
    r'''%%html
<canvas id="myCanvas" width="400" height="400" style="border:2px solid #000000;">
      Error: Your browser does not support the HTML canvas tag.
</canvas>

<script id="myapp">

class hand extends CGRAobject{
    constructor(glcontext, r, g, b){
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
            r, g, b,
            r, g, b,
            r, g, b,
            r, g, b,
            r, g, b,
            r, g, b];
        this.vertexbuffer=this.gl.createBuffer();
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.vertexbuffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(vertices), this.gl.STATIC_DRAW);
        this.colorbuffer = this.gl.createBuffer();
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.colorbuffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(colors), this.gl.STATIC_DRAW);
    }
}

class myapp extends DEECapp{
    initialize(){
        var fragsrc = document.getElementById("my-fragment-shader").text;
        var vertsrc = document.getElementById("my-vertex-shader").text;
        this.shaderprog = new DEECshader(this.gl);
        this.shaderprog.srcShaders(vertsrc,fragsrc);
        this.gl.disable(this.gl.DEPTH_TEST);
        this.gl.clearColor(1.0,1.0,1.0,1.0);

        this.hourHand = new hand(this.gl, 0.2, 0.2, 0.2);
        this.minHand  = new hand(this.gl, 0.0, 0.0, 0.7);
        this.secHand  = new hand(this.gl, 0.8, 0.0, 0.0);
        this.hourHand.setShader(this.shaderprog);
        this.minHand.setShader(this.shaderprog);
        this.secHand.setShader(this.shaderprog);
    }

    drawHand(obj, angleDeg, length){
        var S = glm.scale(glm.mat4(1.0), glm.vec3(1.0, length, 1.0));
        var R = glm.rotate(glm.mat4(1.0), glm.radians(angleDeg), glm.vec3(0.0,0.0,1.0));
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

        this.drawHand(this.hourHand, angH, 0.35);
        this.drawHand(this.minHand,  angM, 0.50);
        this.drawHand(this.secHand,  angS, 0.65);
    }
}

var app = new myapp('myCanvas');
app.run();

</script>
''',
)

print("ALL OK")
