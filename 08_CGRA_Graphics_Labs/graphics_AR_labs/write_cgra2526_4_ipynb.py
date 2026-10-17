import json
from pathlib import Path

OUT = Path(r"c:\Users\Lenovo\Downloads\computer architecture\graphics_AR_labs\BASIC_SOLUTIONS")
OUT.mkdir(exist_ok=True)


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


cells = []

# ----- title -----
cells.append(
    md(
        "# cgra2526-4 — Exercises 4.1 to 4.4\n"
        "Started from **Transformations** example (as PDF says).\n"
        "GLM `vec4`/`mat4` → then copy x,y to 2D `vertices` and draw.\n"
        "**Open with Voilà** (do not use Run)."
    )
)

# ----- lib: glm -----
cells.append(
    code(
        """%%html
<script src='https://git.io/glm-js.min.js'></script>
"""
    )
)

# ----- lib: deec -----
cells.append(
    code(
        """%%html
<script src="https://is3l.isr.uc.pt/~pm/CGRA/JS/deecshader.js"></script>
<script src="https://is3l.isr.uc.pt/~pm/CGRA/JS/deecapp.js"></script>
"""
    )
)

# ----- vertex shader -----
cells.append(
    code(
        """%%html
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
    )
)

# ----- fragment shader -----
cells.append(
    code(
        """%%html
<script id="my-fragment-shader" type="x-shader/x-fragment">
precision highp float;

varying  vec3 ex_Color;

void main(void) {
    gl_FragColor = vec4(ex_Color,1.0);
}
</script>
"""
    )
)

# ===== EX 4.1 =====
cells.append(md("## Exercise 4.1\nVery small blue triangle follows sinusoid left → right and wraps."))
cells.append(
    code(
        r"""%%html
<canvas id="canvas41" width="400" height="400" style="border:2px solid #000000;">
      Error: Your browser does not support the HTML canvas tag.
</canvas>

<script>

class myapp41 extends DEECapp{
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

var app41 = new myapp41('canvas41');
app41.run();

</script>
"""
    )
)

# ===== EX 4.2 =====
cells.append(md("## Exercise 4.2\nSame triangle, but it also rotates while moving."))
cells.append(
    code(
        r"""%%html
<canvas id="canvas42" width="400" height="400" style="border:2px solid #000000;">
      Error: Your browser does not support the HTML canvas tag.
</canvas>

<script>

class myapp42 extends DEECapp{
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

var app42 = new myapp42('canvas42');
app42.run();

</script>
"""
    )
)

# ===== EX 4.3 =====
cells.append(md("## Exercise 4.3\nSmall red rectangle rotates under the moving triangle."))
cells.append(
    code(
        r"""%%html
<canvas id="canvas43" width="400" height="400" style="border:2px solid #000000;">
      Error: Your browser does not support the HTML canvas tag.
</canvas>

<script>

class myapp43 extends DEECapp{
    counter=0;
    initialize(){
        super.initialize();
        this.gl.clearColor(1.0,1.0,1.0,1.0);
        this.gl.disable(this.gl.DEPTH_TEST);

        this.tv1 = glm.vec4(-0.05,  0.06, 0, 1);
        this.tv2 = glm.vec4(-0.05, -0.06, 0, 1);
        this.tv3 = glm.vec4( 0.05, -0.06, 0, 1);
        this.tri_vertices = [0,0, 0,0, 0,0];
        this.tri_colors = [0,0,1, 0,0,1, 0,0,1];

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

    drawObj(vbuf, cbuf, verts, n){
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

        var qR = glm.angleAxis(-this.counter/180*Math.PI, glm.vec3(0,0,1));
        var RR = glm.toMat4(qR);
        var TR = glm.translate(glm.mat4(1.0), glm.vec3(0.0, -0.55, 0.0));
        var MR = TR['*'](RR);
        for(var i=0;i<6;i++){
            var p = MR['*'](this.rv[i]);
            this.rect_vertices[2*i]=p.x;
            this.rect_vertices[2*i+1]=p.y;
        }
        this.drawObj(this.rect_vbuf, this.rect_cbuf, this.rect_vertices, 6);

        var qT = glm.angleAxis(this.counter/180*Math.PI, glm.vec3(0,0,1));
        var RT = glm.toMat4(qT);
        var TT = glm.translate(glm.mat4(1.0), glm.vec3(x, y, 0.0));
        var MT = TT['*'](RT);
        var p1 = MT['*'](this.tv1);
        var p2 = MT['*'](this.tv2);
        var p3 = MT['*'](this.tv3);
        this.tri_vertices = [p1.x,p1.y, p2.x,p2.y, p3.x,p3.y];
        this.drawObj(this.tri_vbuf, this.tri_cbuf, this.tri_vertices, 3);
    }
}

var app43 = new myapp43('canvas43');
app43.run();

</script>
"""
    )
)

# ===== EX 4.4 =====
cells.append(
    md(
        "## Exercise 4.4\n"
        "Clock with 3 rectangle hands (hour, minute, second).\n"
        "Uses `Date()` as in the PDF."
    )
)
cells.append(
    code(
        r"""%%html
<canvas id="canvas44" width="400" height="400" style="border:2px solid #000000;">
      Error: Your browser does not support the HTML canvas tag.
</canvas>

<script>

class myapp44 extends DEECapp{
    initialize(){
        super.initialize();
        this.gl.clearColor(1.0,1.0,1.0,1.0);
        this.gl.disable(this.gl.DEPTH_TEST);

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

    drawHand(verts, colors){
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

        var today = new Date();
        var hours = today.getHours();
        var minutes = today.getMinutes();
        var secs = today.getSeconds();

        var angS = -secs * (2*Math.PI/60);
        var angM = -(minutes + secs/60.0) * (2*Math.PI/60);
        var angH = -((hours%12) + minutes/60.0) * (2*Math.PI/12);

        this.fillHand(this.hVerts, angH, 0.35);
        this.fillHand(this.mVerts, angM, 0.50);
        this.fillHand(this.sVerts, angS, 0.65);

        this.drawHand(this.hVerts, this.hCol);
        this.drawHand(this.mVerts, this.mCol);
        this.drawHand(this.sVerts, this.sCol);
    }
}

var app44 = new myapp44('canvas44');
app44.run();

</script>
"""
    )
)

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

path = OUT / "cgra2526_4_solutions.ipynb"
path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False), encoding="utf-8")
print("OK", path)
print("cells =", len(cells))
