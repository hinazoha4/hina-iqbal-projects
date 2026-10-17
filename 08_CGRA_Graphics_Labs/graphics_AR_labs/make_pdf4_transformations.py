"""
cgra2526-4.pdf solutions
PDF says: Start with Transformations example.
Use GLM mat4/vec4, then copy x,y into 2D vertex array to draw.
"""
import json
from pathlib import Path

OUT = Path(r"c:\Users\Lenovo\Downloads\computer architecture\graphics_AR_labs\BASIC_SOLUTIONS")
OUT.mkdir(exist_ok=True)

# Minimal cells like Transformations drawing part + what PDF needs


def md(s):
    return {"cell_type": "markdown", "metadata": {}, "source": [l + "\n" for l in s.split("\n")]}


def code(s):
    if not s.endswith("\n"):
        s += "\n"
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [l + "\n" for l in s.split("\n")],
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
    (OUT / name).write_text(json.dumps(nb(cells), indent=1, ensure_ascii=False), encoding="utf-8")
    print("wrote", name)


# Same setup cells for every exercise (from Transformations example)
GLM = """%%html
<script src='https://git.io/glm-js.min.js'></script>
"""

LIBS = """%%html
<script src="https://is3l.isr.uc.pt/~pm/CGRA/JS/deecshader.js"></script>
<script src="https://is3l.isr.uc.pt/~pm/CGRA/JS/deecapp.js"></script>
"""

VERT = """%%html
<script id="my-vertex-shader" type="x-shader/x-vertex">
precision highp float;

attribute  vec2 in_Position;
attribute  vec3 in_Color;

varying  vec3 ex_Color;

void main(void) {
    gl_Position = vec4(in_Position.x, in_Position.y, 0.0, 1.0);
    ex_Color = in_Color;
}
</script>
"""

FRAG = """%%html
<script id="my-fragment-shader" type="x-shader/x-fragment">
precision highp float;

varying  vec3 ex_Color;

void main(void) {
    gl_FragColor = vec4(ex_Color,1.0);
}
</script>
"""

# ---------- Ex 4.1 ----------
APP41 = r"""%%html
<canvas id="myCanvas" width="400" height="400" style="border:2px solid #000000;">
      Error: Your browser does not support the HTML canvas tag.
</canvas>

<script id="myapp">

class myapp extends DEECapp{
    counter=0;
    initialize(){
        super.initialize();
        this.gl.clearColor(1.0,1.0,1.0,1.0);

        // very small blue triangle (local points as glm.vec4 like Transformations)
        this.v1 = glm.vec4(-0.05,  0.06, 0, 1);
        this.v2 = glm.vec4(-0.05, -0.06, 0, 1);
        this.v3 = glm.vec4( 0.05, -0.06, 0, 1);

        this.numvertices = 3;
        this.vertices = [0,0, 0,0, 0,0];
        this.colors = [
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0];

        this.vertexbuffer=this.gl.createBuffer();
        this.colorbuffer=this.gl.createBuffer();
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.colorbuffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.colors), this.gl.STATIC_DRAW);

        this.starttime = Date.now();
    }

    render(){
        this.gl.clear(this.gl.COLOR_BUFFER_BIT);
        this.counter++;

        // Ex 4.1: move left -> right on sinusoid, then wrap
        var t = (Date.now() - this.starttime) * 0.001;
        var x = -1.0 + (t * 0.25) % 2.0;
        var y = 0.4 * Math.sin(3.1416 * x);

        // GLM translate (4D), then copy x,y to 2D array (as PDF says)
        var T = glm.translate(glm.mat4(1.0), glm.vec3(x, y, 0.0));
        var p1 = T['*'](this.v1);
        var p2 = T['*'](this.v2);
        var p3 = T['*'](this.v3);

        this.vertices[0]=p1.x; this.vertices[1]=p1.y;
        this.vertices[2]=p2.x; this.vertices[3]=p2.y;
        this.vertices[4]=p3.x; this.vertices[5]=p3.y;

        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.vertexbuffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.vertices), this.gl.STATIC_DRAW);

        this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.vertexbuffer);
        this.positionLocation = this.gl.getAttribLocation(this.shaderprog.shaderProgram,"in_Position");
        this.gl.vertexAttribPointer(this.positionLocation, 2, this.gl.FLOAT, this.gl.FALSE, 2*Float32Array.BYTES_PER_ELEMENT, 0);
        this.gl.enableVertexAttribArray(this.positionLocation);

        this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.colorbuffer);
        this.colorLocation = this.gl.getAttribLocation(this.shaderprog.shaderProgram,"in_Color");
        this.gl.vertexAttribPointer(this.colorLocation, 3, this.gl.FLOAT, this.gl.FALSE, 3*Float32Array.BYTES_PER_ELEMENT, 0);
        this.gl.enableVertexAttribArray(this.colorLocation);

        this.shaderprog.startUsing();
        this.gl.drawArrays(this.gl.TRIANGLES,0,this.numvertices);
        this.shaderprog.stopUsing();
    }
}

var app = new myapp('myCanvas');
app.run();

</script>
"""

# ---------- Ex 4.2 ----------
APP42 = r"""%%html
<canvas id="myCanvas" width="400" height="400" style="border:2px solid #000000;">
      Error: Your browser does not support the HTML canvas tag.
</canvas>

<script id="myapp">

class myapp extends DEECapp{
    counter=0;
    initialize(){
        super.initialize();
        this.gl.clearColor(1.0,1.0,1.0,1.0);

        this.v1 = glm.vec4(-0.05,  0.06, 0, 1);
        this.v2 = glm.vec4(-0.05, -0.06, 0, 1);
        this.v3 = glm.vec4( 0.05, -0.06, 0, 1);

        this.numvertices = 3;
        this.vertices = [0,0, 0,0, 0,0];
        this.colors = [
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0];

        this.vertexbuffer=this.gl.createBuffer();
        this.colorbuffer=this.gl.createBuffer();
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.colorbuffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.colors), this.gl.STATIC_DRAW);
        this.starttime = Date.now();
    }

    render(){
        this.gl.clear(this.gl.COLOR_BUFFER_BIT);
        this.counter++;

        var t = (Date.now() - this.starttime) * 0.001;
        var x = -1.0 + (t * 0.25) % 2.0;
        var y = 0.4 * Math.sin(3.1416 * x);

        // Ex 4.2: rotate (like Transformations) then translate on sinusoid
        var q = glm.angleAxis(this.counter/180*Math.PI, glm.vec3(0,0,1));
        var R = glm.toMat4(q);
        var T = glm.translate(glm.mat4(1.0), glm.vec3(x, y, 0.0));
        var M = T['*'](R);

        var p1 = M['*'](this.v1);
        var p2 = M['*'](this.v2);
        var p3 = M['*'](this.v3);

        this.vertices[0]=p1.x; this.vertices[1]=p1.y;
        this.vertices[2]=p2.x; this.vertices[3]=p2.y;
        this.vertices[4]=p3.x; this.vertices[5]=p3.y;

        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.vertexbuffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.vertices), this.gl.STATIC_DRAW);

        this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.vertexbuffer);
        this.positionLocation = this.gl.getAttribLocation(this.shaderprog.shaderProgram,"in_Position");
        this.gl.vertexAttribPointer(this.positionLocation, 2, this.gl.FLOAT, this.gl.FALSE, 2*Float32Array.BYTES_PER_ELEMENT, 0);
        this.gl.enableVertexAttribArray(this.positionLocation);

        this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.colorbuffer);
        this.colorLocation = this.gl.getAttribLocation(this.shaderprog.shaderProgram,"in_Color");
        this.gl.vertexAttribPointer(this.colorLocation, 3, this.gl.FLOAT, this.gl.FALSE, 3*Float32Array.BYTES_PER_ELEMENT, 0);
        this.gl.enableVertexAttribArray(this.colorLocation);

        this.shaderprog.startUsing();
        this.gl.drawArrays(this.gl.TRIANGLES,0,this.numvertices);
        this.shaderprog.stopUsing();
    }
}

var app = new myapp('myCanvas');
app.run();

</script>
"""

# ---------- Ex 4.3 ----------
APP43 = r"""%%html
<canvas id="myCanvas" width="400" height="400" style="border:2px solid #000000;">
      Error: Your browser does not support the HTML canvas tag.
</canvas>

<script id="myapp">

class myapp extends DEECapp{
    counter=0;
    initialize(){
        super.initialize();
        this.gl.clearColor(1.0,1.0,1.0,1.0);
        this.gl.disable(this.gl.DEPTH_TEST);

        // small blue triangle
        this.tv1 = glm.vec4(-0.05,  0.06, 0, 1);
        this.tv2 = glm.vec4(-0.05, -0.06, 0, 1);
        this.tv3 = glm.vec4( 0.05, -0.06, 0, 1);
        this.tri_vertices = [0,0, 0,0, 0,0];
        this.tri_colors = [0,0,1, 0,0,1, 0,0,1];

        // small red rectangle (2 triangles)
        this.rv = [
            glm.vec4(-0.12,-0.06,0,1),
            glm.vec4( 0.12,-0.06,0,1),
            glm.vec4( 0.12, 0.06,0,1),
            glm.vec4(-0.12,-0.06,0,1),
            glm.vec4( 0.12, 0.06,0,1),
            glm.vec4(-0.12, 0.06,0,1)
        ];
        this.rect_vertices = [0,0,0,0,0,0,0,0,0,0,0,0];
        this.rect_colors = [
            1,0,0, 1,0,0, 1,0,0,
            1,0,0, 1,0,0, 1,0,0];

        this.tri_vbuf=this.gl.createBuffer();
        this.tri_cbuf=this.gl.createBuffer();
        this.rect_vbuf=this.gl.createBuffer();
        this.rect_cbuf=this.gl.createBuffer();
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.tri_cbuf);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.tri_colors), this.gl.STATIC_DRAW);
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.rect_cbuf);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.rect_colors), this.gl.STATIC_DRAW);

        this.starttime = Date.now();
    }

    draw2D(vbuf, cbuf, verts, n){
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, vbuf);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(verts), this.gl.STATIC_DRAW);

        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, vbuf);
        this.positionLocation = this.gl.getAttribLocation(this.shaderprog.shaderProgram,"in_Position");
        this.gl.vertexAttribPointer(this.positionLocation, 2, this.gl.FLOAT, this.gl.FALSE, 2*Float32Array.BYTES_PER_ELEMENT, 0);
        this.gl.enableVertexAttribArray(this.positionLocation);

        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, cbuf);
        this.colorLocation = this.gl.getAttribLocation(this.shaderprog.shaderProgram,"in_Color");
        this.gl.vertexAttribPointer(this.colorLocation, 3, this.gl.FLOAT, this.gl.FALSE, 3*Float32Array.BYTES_PER_ELEMENT, 0);
        this.gl.enableVertexAttribArray(this.colorLocation);

        this.shaderprog.startUsing();
        this.gl.drawArrays(this.gl.TRIANGLES,0,n);
        this.shaderprog.stopUsing();
    }

    render(){
        this.gl.clear(this.gl.COLOR_BUFFER_BIT);
        this.counter++;

        var t = (Date.now() - this.starttime) * 0.001;
        var x = -1.0 + (t * 0.25) % 2.0;
        var y = 0.4 * Math.sin(3.1416 * x);

        // rectangle rotates under the triangle
        var qR = glm.angleAxis(-this.counter/180*Math.PI, glm.vec3(0,0,1));
        var RR = glm.toMat4(qR);
        var TR = glm.translate(glm.mat4(1.0), glm.vec3(0.0, -0.55, 0.0));
        var MR = TR['*'](RR);
        for(var i=0;i<6;i++){
            var p = MR['*'](this.rv[i]);
            this.rect_vertices[2*i]=p.x;
            this.rect_vertices[2*i+1]=p.y;
        }
        this.draw2D(this.rect_vbuf, this.rect_cbuf, this.rect_vertices, 6);

        // triangle moves + rotates on sinusoid
        var qT = glm.angleAxis(this.counter/180*Math.PI, glm.vec3(0,0,1));
        var RT = glm.toMat4(qT);
        var TT = glm.translate(glm.mat4(1.0), glm.vec3(x, y, 0.0));
        var MT = TT['*'](RT);
        var p1 = MT['*'](this.tv1);
        var p2 = MT['*'](this.tv2);
        var p3 = MT['*'](this.tv3);
        this.tri_vertices = [p1.x,p1.y, p2.x,p2.y, p3.x,p3.y];
        this.draw2D(this.tri_vbuf, this.tri_cbuf, this.tri_vertices, 3);
    }
}

var app = new myapp('myCanvas');
app.run();

</script>
"""

# ---------- Ex 4.4 ----------
APP44 = r"""%%html
<canvas id="myCanvas" width="400" height="400" style="border:2px solid #000000;">
      Error: Your browser does not support the HTML canvas tag.
</canvas>

<script id="myapp">

class myapp extends DEECapp{
    initialize(){
        super.initialize();
        this.gl.clearColor(1.0,1.0,1.0,1.0);
        this.gl.disable(this.gl.DEPTH_TEST);

        // one unit hand pointing up; we scale/rotate with GLM
        this.handLocal = [
            glm.vec4(-0.02, 0.0, 0, 1),
            glm.vec4( 0.02, 0.0, 0, 1),
            glm.vec4( 0.02, 1.0, 0, 1),
            glm.vec4(-0.02, 0.0, 0, 1),
            glm.vec4( 0.02, 1.0, 0, 1),
            glm.vec4(-0.02, 1.0, 0, 1)
        ];

        this.hVerts = new Array(12);
        this.mVerts = new Array(12);
        this.sVerts = new Array(12);

        this.hCol = [0.2,0.2,0.2, 0.2,0.2,0.2, 0.2,0.2,0.2, 0.2,0.2,0.2, 0.2,0.2,0.2, 0.2,0.2,0.2];
        this.mCol = [0.0,0.0,0.7, 0.0,0.0,0.7, 0.0,0.0,0.7, 0.0,0.0,0.7, 0.0,0.0,0.7, 0.0,0.0,0.7];
        this.sCol = [0.8,0.0,0.0, 0.8,0.0,0.0, 0.8,0.0,0.0, 0.8,0.0,0.0, 0.8,0.0,0.0, 0.8,0.0,0.0];

        this.vbuf=this.gl.createBuffer();
        this.cbuf=this.gl.createBuffer();
    }

    fillHand(outVerts, angleRad, length){
        var S = glm.scale(glm.mat4(1.0), glm.vec3(1.0, length, 1.0));
        var q = glm.angleAxis(angleRad, glm.vec3(0,0,1));
        var R = glm.toMat4(q);
        var M = R['*'](S);
        for(var i=0;i<6;i++){
            var p = M['*'](this.handLocal[i]);
            outVerts[2*i]=p.x; outVerts[2*i+1]=p.y;
        }
    }

    draw(verts, colors){
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.vbuf);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(verts), this.gl.STATIC_DRAW);
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.cbuf);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(colors), this.gl.STATIC_DRAW);

        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.vbuf);
        this.positionLocation = this.gl.getAttribLocation(this.shaderprog.shaderProgram,"in_Position");
        this.gl.vertexAttribPointer(this.positionLocation, 2, this.gl.FLOAT, this.gl.FALSE, 2*Float32Array.BYTES_PER_ELEMENT, 0);
        this.gl.enableVertexAttribArray(this.positionLocation);

        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.cbuf);
        this.colorLocation = this.gl.getAttribLocation(this.shaderprog.shaderProgram,"in_Color");
        this.gl.vertexAttribPointer(this.colorLocation, 3, this.gl.FLOAT, this.gl.FALSE, 3*Float32Array.BYTES_PER_ELEMENT, 0);
        this.gl.enableVertexAttribArray(this.colorLocation);

        this.shaderprog.startUsing();
        this.gl.drawArrays(this.gl.TRIANGLES,0,6);
        this.shaderprog.stopUsing();
    }

    render(){
        this.gl.clear(this.gl.COLOR_BUFFER_BIT);

        // PDF code
        var today = new Date();
        var hours = today.getHours();
        var minutes = today.getMinutes();
        var secs = today.getSeconds();

        // clock angles (negative = clockwise)
        var angS = -secs * (2*Math.PI/60);
        var angM = -(minutes + secs/60.0) * (2*Math.PI/60);
        var angH = -((hours%12) + minutes/60.0) * (2*Math.PI/12);

        this.fillHand(this.hVerts, angH, 0.35);
        this.fillHand(this.mVerts, angM, 0.50);
        this.fillHand(this.sVerts, angS, 0.65);

        this.draw(this.hVerts, this.hCol);
        this.draw(this.mVerts, this.mCol);
        this.draw(this.sVerts, this.sCol);
    }
}

var app = new myapp('myCanvas');
app.run();

</script>
"""


def make(name, ex_title, app):
    cells = [
        md(
            f"# {ex_title}\n"
            "From PDF **cgra2526-4**.\n"
            "Started from examples **Transformations** (as PDF says).\n"
            "GLM mat4/vec4 → then copy x,y to 2D vertices.\n"
            "Open with **Voilà**."
        ),
        code(GLM),
        code(LIBS),
        code(VERT),
        code(FRAG),
        code(app),
    ]
    save(name, cells)


make("PDF4_Ex4_1.ipynb", "Exercise 4.1 (cgra2526-4)", APP41)
make("PDF4_Ex4_2.ipynb", "Exercise 4.2 (cgra2526-4)", APP42)
make("PDF4_Ex4_3.ipynb", "Exercise 4.3 (cgra2526-4)", APP43)
make("PDF4_Ex4_4.ipynb", "Exercise 4.4 (cgra2526-4)", APP44)

(OUT / "PDF4_README.txt").write_text(
"""cgra2526-4.pdf SOLUTIONS
========================
PDF page 3-4 says:
  "Start with the example Transformations"
  Use GLM 4D, then convert to 2D vertex arrays to draw.

Files:
  PDF4_Ex4_1.ipynb  - small blue triangle on sinusoid L->R wrap
  PDF4_Ex4_2.ipynb  - same + rotate
  PDF4_Ex4_3.ipynb  - rotating rectangle under triangle
  PDF4_Ex4_4.ipynb  - clock with Date()

Upload -> Voila

What to say:
  I started from Transformations example.
  I keep points as glm.vec4, multiply by mat4, then put x,y in vertices[] for drawArrays.
""",
    encoding="utf-8",
)
print("DONE")
