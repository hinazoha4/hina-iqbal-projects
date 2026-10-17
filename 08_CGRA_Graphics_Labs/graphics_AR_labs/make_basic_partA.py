"""
Build BASIC student-looking solutions from professor official examples.
Style: copy example code, only change what exercise asks. No helpers.
"""
import json
import copy
from pathlib import Path

EX = Path(r"c:\Users\Lenovo\Downloads\computer architecture\graphics_AR_labs\examples_official")
OUT = Path(r"c:\Users\Lenovo\Downloads\computer architecture\graphics_AR_labs\BASIC_SOLUTIONS")
OUT.mkdir(exist_ok=True)


def load(name):
    return json.loads((EX / name).read_text(encoding="utf-8"))


def save(name, nb):
    (OUT / name).write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding="utf-8")
    print("wrote", name)


def md(s):
    return {"cell_type": "markdown", "metadata": {}, "source": [line if line.endswith("\n") else line + "\n" for line in s.split("\n")]}


def code(s):
    if not s.endswith("\n"):
        s += "\n"
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line if line.endswith("\n") else line + "\n" for line in s.split("\n")],
    }


# Shared shader cells exactly like professor
VERT = r'''%%html
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
'''

FRAG = r'''%%html
<script id="my-fragment-shader" type="x-shader/x-fragment">
precision highp float;

varying  vec3 ex_Color;

void main(void) {
    gl_FragColor = vec4(ex_Color,1.0);
}
</script>
'''

LIBS = r'''%%html
<script src="https://is3l.isr.uc.pt/~pm/CGRA/JS/deecshader.js"></script>
<script src="https://is3l.isr.uc.pt/~pm/CGRA/JS/deecapp.js"></script>
'''

# Template app - SAME as professor triangle, only placeholders differ
def app_cell(canvas_id, class_name, app_var, vertices, colors, numvertices, draw_mode, extra_init="", extra_render_before="", title=""):
    # draw_mode like: this.gl.TRIANGLES
    return code(f'''%%html
{title}
<canvas id="{canvas_id}" width="400" height="400" style="border:2px solid #000000;">
      Error: Your browser does not support the HTML canvas tag.
</canvas>

<script>

class {class_name} extends DEECapp{{
    counter=0;
    initialize(){{
        super.initialize();
        this.gl.clearColor(1.0,1.0,1.0,1.0);

        this.numvertices = {numvertices};
        this.vertices =
            {vertices};

        this.colors = {colors};

{extra_init}
        this.vertexbuffer=this.gl.createBuffer();
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.vertexbuffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.vertices), this.gl.STATIC_DRAW);

        this.colorbuffer = this.gl.createBuffer();
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.colorbuffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.colors), this.gl.STATIC_DRAW);
    }}

    render(){{
{extra_render_before}
        this.gl.clear(this.gl.COLOR_BUFFER_BIT);
        this.counter++;

        this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.vertexbuffer);
        this.positionLocation = this.gl.getAttribLocation(this.shaderprog.shaderProgram,
                                                          "in_Position");
        this.gl.vertexAttribPointer(this.positionLocation,
                           2,
                           this.gl.FLOAT,
                           this.gl.FALSE,
                           2*Float32Array.BYTES_PER_ELEMENT,
                           0);
        this.gl.enableVertexAttribArray(this.positionLocation);

        this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.colorbuffer);
        this.colorLocation = this.gl.getAttribLocation(this.shaderprog.shaderProgram,
                                                          "in_Color");
        this.gl.vertexAttribPointer(this.colorLocation,
                           3,
                           this.gl.FLOAT,
                           this.gl.FALSE,
                           3*Float32Array.BYTES_PER_ELEMENT,
                           0);
        this.gl.enableVertexAttribArray(this.colorLocation);

        this.shaderprog.startUsing();
        this.gl.drawArrays({draw_mode},0,this.numvertices);
        this.shaderprog.stopUsing();
    }}
}}

var {app_var} = new {class_name}('{canvas_id}');
{app_var}.run();

</script>
''')


# ========== CHAPTER 1 from 01Lines / 02Triangle ==========
ch1 = {
    "cells": [
        md("# My exercises - Chapter 1\nI copied the example from the examples folder and changed only what the exercise asks.\nUse **Voilà**."),
        code(LIBS),
        code(VERT),
        code(FRAG),
        md("## Exercise 1.1\nI changed the colours and the vertex coordinates (still inside -1 to 1)."),
        app_cell(
            "canvas11", "myapp11", "app11",
            """[  0.0,  0.80 ,
              -0.60, -0.70 ,
               0.60, -0.70]""",
            """[
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0]""",
            3, "this.gl.TRIANGLES",
            title="<p>Ex 1.1</p>"
        ),
        md("## Exercise 1.2\nSame idea as Lines example: console.log and changing background."),
        app_cell(
            "canvas12", "myapp12", "app12",
            """[  0.0,  0.70 ,
              -0.60, -0.50 ,
               0.60, -0.50]""",
            """[
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0]""",
            3, "this.gl.TRIANGLES",
            extra_render_before="""        // like the Lines example
        console.log('draw call nr: ' + this.counter);
        var grey=0.5+0.5*Math.sin(this.counter/180*Math.PI);
        this.gl.clearColor(grey,grey,grey,1.0);
""",
            title="<p>Ex 1.2 - open F12 Console</p>"
        ),
        md("## Exercise 1.3\nI added one more point (now 4 points) like the Lines example diamond."),
        app_cell(
            "canvas13", "myapp13", "app13",
            """[  0.0,  0.90 ,
               0.90,  0.0 ,
               0.0, -0.90 ,
              -0.90,  0.0]""",
            """[
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0,
            1.0, 1.0, 0.0]""",
            4, "this.gl.LINE_LOOP",
            title="<p>Ex 1.3</p>"
        ),
        md("## Exercise 1.4\nI only changed drawArrays mode. Try one mode at a time."),
        app_cell(
            "canvas14", "myapp14", "app14",
            """[  0.0,  0.70 ,
              -0.60, -0.50 ,
               0.60, -0.50]""",
            """[
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0]""",
            3, "this.gl.LINE_LOOP",  # student can change to POINTS, TRIANGLES, etc.
            title="<p>Ex 1.4 - change LINE_LOOP to POINTS / LINE_STRIP / LINES / TRIANGLE_STRIP / TRIANGLE_FAN / TRIANGLES</p>"
        ),
    ],
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}
save("Ch1_basic_from_examples.ipynb", ch1)


# ========== CHAPTER 2 ==========
# 2.1 isosceles - just vertices
# 2.2 rectangle + triangle - need two draw calls - student style duplicate
# 2.3-2.7 need time updates - still keep same structure

ch2_cells = [
    md("# My exercises - Chapter 2\nBased on 02Triangle example. Use **Voilà**."),
    code(LIBS),
    code(VERT),
    code(FRAG),
    md("## Exercise 2.1 - vertical isosceles triangle\nI only changed the three points."),
    app_cell(
        "canvas21", "myapp21", "app21",
        """[  0.0,  0.80 ,
          -0.50, -0.60 ,
           0.50, -0.60]""",
        """[
        1.0, 0.0, 0.0,
        0.0, 1.0, 0.0,
        0.0, 0.0, 1.0]""",
        3, "this.gl.TRIANGLES",
        title="<p>Ex 2.1</p>"
    ),
    md("## Exercise 2.2 - red rectangle under the triangle\nI draw the rectangle first, then the triangle (last drawn is on top)."),
    code(r'''%%html
<p>Ex 2.2</p>
<canvas id="canvas22" width="400" height="400" style="border:2px solid #000000;">
      Error: Your browser does not support the HTML canvas tag.
</canvas>
<script>
class myapp22 extends DEECapp{
    counter=0;
    initialize(){
        super.initialize();
        this.gl.clearColor(1.0,1.0,1.0,1.0);

        // triangle
        this.tri_n = 3;
        this.tri_vertices =
            [  0.0,  0.75 ,
              -0.45, -0.55 ,
               0.45, -0.55];
        this.tri_colors = [
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0];

        // red rectangle side 0.8 (from -0.4 to 0.4) = two triangles
        this.rect_n = 6;
        this.rect_vertices =
            [ -0.4, -0.4 ,
               0.4, -0.4 ,
               0.4,  0.4 ,
              -0.4, -0.4 ,
               0.4,  0.4 ,
              -0.4,  0.4 ];
        this.rect_colors = [
            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0];

        this.tri_vbuf=this.gl.createBuffer();
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.tri_vbuf);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.tri_vertices), this.gl.STATIC_DRAW);
        this.tri_cbuf=this.gl.createBuffer();
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.tri_cbuf);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.tri_colors), this.gl.STATIC_DRAW);

        this.rect_vbuf=this.gl.createBuffer();
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.rect_vbuf);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.rect_vertices), this.gl.STATIC_DRAW);
        this.rect_cbuf=this.gl.createBuffer();
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.rect_cbuf);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.rect_colors), this.gl.STATIC_DRAW);
    }

    render(){
        this.gl.clear(this.gl.COLOR_BUFFER_BIT);
        this.counter++;

        // draw rectangle first
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.rect_vbuf);
        this.positionLocation = this.gl.getAttribLocation(this.shaderprog.shaderProgram, "in_Position");
        this.gl.vertexAttribPointer(this.positionLocation, 2, this.gl.FLOAT, this.gl.FALSE, 2*Float32Array.BYTES_PER_ELEMENT, 0);
        this.gl.enableVertexAttribArray(this.positionLocation);
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.rect_cbuf);
        this.colorLocation = this.gl.getAttribLocation(this.shaderprog.shaderProgram, "in_Color");
        this.gl.vertexAttribPointer(this.colorLocation, 3, this.gl.FLOAT, this.gl.FALSE, 3*Float32Array.BYTES_PER_ELEMENT, 0);
        this.gl.enableVertexAttribArray(this.colorLocation);
        this.shaderprog.startUsing();
        this.gl.drawArrays(this.gl.TRIANGLES,0,this.rect_n);
        this.shaderprog.stopUsing();

        // then triangle on top
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.tri_vbuf);
        this.positionLocation = this.gl.getAttribLocation(this.shaderprog.shaderProgram, "in_Position");
        this.gl.vertexAttribPointer(this.positionLocation, 2, this.gl.FLOAT, this.gl.FALSE, 2*Float32Array.BYTES_PER_ELEMENT, 0);
        this.gl.enableVertexAttribArray(this.positionLocation);
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.tri_cbuf);
        this.colorLocation = this.gl.getAttribLocation(this.shaderprog.shaderProgram, "in_Color");
        this.gl.vertexAttribPointer(this.colorLocation, 3, this.gl.FLOAT, this.gl.FALSE, 3*Float32Array.BYTES_PER_ELEMENT, 0);
        this.gl.enableVertexAttribArray(this.colorLocation);
        this.shaderprog.startUsing();
        this.gl.drawArrays(this.gl.TRIANGLES,0,this.tri_n);
        this.shaderprog.stopUsing();
    }
}
var app22 = new myapp22('canvas22');
app22.run();
</script>
'''),
    md("## Exercise 2.3 - top point moves with sin (0.5 Hz)\nI use Date.now() like the PDF says."),
    code(r'''%%html
<p>Ex 2.3</p>
<canvas id="canvas23" width="400" height="400" style="border:2px solid #000000;"></canvas>
<script>
class myapp23 extends DEECapp{
    counter=0;
    initialize(){
        super.initialize();
        this.gl.clearColor(1.0,1.0,1.0,1.0);
        this.numvertices = 3;
        // I keep the base y for bottom points fixed
        this.vertices =
            [  0.0,  0.80 ,
              -0.50, -0.60 ,
               0.50, -0.60];
        this.colors = [
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0];
        this.vertexbuffer=this.gl.createBuffer();
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.vertexbuffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.vertices), this.gl.STATIC_DRAW);
        this.colorbuffer=this.gl.createBuffer();
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.colorbuffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.colors), this.gl.STATIC_DRAW);
        this.starttime = Date.now();
    }
    render(){
        // time in seconds
        var t = (Date.now() - this.starttime) * 0.001;
        // 0.5 Hz => sin(2*pi*0.5*t) = sin(pi*t)
        this.vertices[1] = 0.45 + 0.35 * Math.sin(Math.PI * t);

        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.vertexbuffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.vertices), this.gl.STATIC_DRAW);

        this.gl.clear(this.gl.COLOR_BUFFER_BIT);
        this.counter++;
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.vertexbuffer);
        this.positionLocation = this.gl.getAttribLocation(this.shaderprog.shaderProgram, "in_Position");
        this.gl.vertexAttribPointer(this.positionLocation, 2, this.gl.FLOAT, this.gl.FALSE, 2*Float32Array.BYTES_PER_ELEMENT, 0);
        this.gl.enableVertexAttribArray(this.positionLocation);
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.colorbuffer);
        this.colorLocation = this.gl.getAttribLocation(this.shaderprog.shaderProgram, "in_Color");
        this.gl.vertexAttribPointer(this.colorLocation, 3, this.gl.FLOAT, this.gl.FALSE, 3*Float32Array.BYTES_PER_ELEMENT, 0);
        this.gl.enableVertexAttribArray(this.colorLocation);
        this.shaderprog.startUsing();
        this.gl.drawArrays(this.gl.TRIANGLES,0,this.numvertices);
        this.shaderprog.stopUsing();
    }
}
var app23 = new myapp23('canvas23');
app23.run();
</script>
'''),
    md("## Exercise 2.4 - rotate triangle\nSame formula from the PDF."),
    code(r'''%%html
<p>Ex 2.4</p>
<canvas id="canvas24" width="400" height="400" style="border:2px solid #000000;"></canvas>
<script>
class myapp24 extends DEECapp{
    counter=0;
    initialize(){
        super.initialize();
        this.gl.clearColor(1.0,1.0,1.0,1.0);
        this.numvertices = 3;
        // original points (I keep a copy)
        this.x0 = [ 0.0, -0.40,  0.40];
        this.y0 = [ 0.50, -0.30, -0.30];
        this.vertices = [0,0, 0,0, 0,0];
        this.colors = [
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0];
        this.vertexbuffer=this.gl.createBuffer();
        this.colorbuffer=this.gl.createBuffer();
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.colorbuffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.colors), this.gl.STATIC_DRAW);
        this.starttime = Date.now();
    }
    render(){
        var t = (Date.now() - this.starttime) * 0.001;
        var c = Math.cos(t);
        var s = Math.sin(t);
        // x' = x cos - y sin
        // y' = x sin + y cos
        for(var i=0; i<3; i++){
            this.vertices[2*i]   = this.x0[i]*c - this.y0[i]*s;
            this.vertices[2*i+1] = this.x0[i]*s + this.y0[i]*c;
        }
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.vertexbuffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.vertices), this.gl.STATIC_DRAW);

        this.gl.clear(this.gl.COLOR_BUFFER_BIT);
        this.counter++;
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.vertexbuffer);
        this.positionLocation = this.gl.getAttribLocation(this.shaderprog.shaderProgram, "in_Position");
        this.gl.vertexAttribPointer(this.positionLocation, 2, this.gl.FLOAT, this.gl.FALSE, 2*Float32Array.BYTES_PER_ELEMENT, 0);
        this.gl.enableVertexAttribArray(this.positionLocation);
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.colorbuffer);
        this.colorLocation = this.gl.getAttribLocation(this.shaderprog.shaderProgram, "in_Color");
        this.gl.vertexAttribPointer(this.colorLocation, 3, this.gl.FLOAT, this.gl.FALSE, 3*Float32Array.BYTES_PER_ELEMENT, 0);
        this.gl.enableVertexAttribArray(this.colorLocation);
        this.shaderprog.startUsing();
        this.gl.drawArrays(this.gl.TRIANGLES,0,this.numvertices);
        this.shaderprog.stopUsing();
    }
}
var app24 = new myapp24('canvas24');
app24.run();
</script>
'''),
    md("## Exercise 2.5 - rotate triangle over static rectangle\nRectangle fixed, triangle rotates (like 2.2 + 2.4)."),
    code(r'''%%html
<p>Ex 2.5</p>
<canvas id="canvas25" width="400" height="400" style="border:2px solid #000000;"></canvas>
<script>
class myapp25 extends DEECapp{
    counter=0;
    initialize(){
        super.initialize();
        this.gl.clearColor(1.0,1.0,1.0,1.0);
        this.x0 = [ 0.0, -0.25,  0.25];
        this.y0 = [ 0.40, -0.15, -0.15];
        this.tri_vertices = [0,0, 0,0, 0,0];
        this.tri_colors = [0.0,0.0,1.0, 0.0,1.0,1.0, 1.0,1.0,0.0];
        this.rect_vertices =
            [ -0.4, -0.4 ,  0.4, -0.4 ,  0.4,  0.4 ,
              -0.4, -0.4 ,  0.4,  0.4 , -0.4,  0.4 ];
        this.rect_colors = [
            1,0,0, 1,0,0, 1,0,0,
            1,0,0, 1,0,0, 1,0,0];
        this.tri_vbuf=this.gl.createBuffer();
        this.tri_cbuf=this.gl.createBuffer();
        this.rect_vbuf=this.gl.createBuffer();
        this.rect_cbuf=this.gl.createBuffer();
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.tri_cbuf);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.tri_colors), this.gl.STATIC_DRAW);
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.rect_vbuf);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.rect_vertices), this.gl.STATIC_DRAW);
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.rect_cbuf);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.rect_colors), this.gl.STATIC_DRAW);
        this.starttime = Date.now();
    }
    render(){
        var t = (Date.now() - this.starttime) * 0.001;
        var c = Math.cos(t);
        var s = Math.sin(t);
        for(var i=0; i<3; i++){
            this.tri_vertices[2*i]   = this.x0[i]*c - this.y0[i]*s;
            this.tri_vertices[2*i+1] = this.x0[i]*s + this.y0[i]*c;
        }
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.tri_vbuf);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.tri_vertices), this.gl.STATIC_DRAW);

        this.gl.clear(this.gl.COLOR_BUFFER_BIT);

        // rectangle
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.rect_vbuf);
        this.positionLocation = this.gl.getAttribLocation(this.shaderprog.shaderProgram, "in_Position");
        this.gl.vertexAttribPointer(this.positionLocation, 2, this.gl.FLOAT, this.gl.FALSE, 2*Float32Array.BYTES_PER_ELEMENT, 0);
        this.gl.enableVertexAttribArray(this.positionLocation);
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.rect_cbuf);
        this.colorLocation = this.gl.getAttribLocation(this.shaderprog.shaderProgram, "in_Color");
        this.gl.vertexAttribPointer(this.colorLocation, 3, this.gl.FLOAT, this.gl.FALSE, 3*Float32Array.BYTES_PER_ELEMENT, 0);
        this.gl.enableVertexAttribArray(this.colorLocation);
        this.shaderprog.startUsing();
        this.gl.drawArrays(this.gl.TRIANGLES,0,6);
        this.shaderprog.stopUsing();

        // triangle
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.tri_vbuf);
        this.positionLocation = this.gl.getAttribLocation(this.shaderprog.shaderProgram, "in_Position");
        this.gl.vertexAttribPointer(this.positionLocation, 2, this.gl.FLOAT, this.gl.FALSE, 2*Float32Array.BYTES_PER_ELEMENT, 0);
        this.gl.enableVertexAttribArray(this.positionLocation);
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.tri_cbuf);
        this.colorLocation = this.gl.getAttribLocation(this.shaderprog.shaderProgram, "in_Color");
        this.gl.vertexAttribPointer(this.colorLocation, 3, this.gl.FLOAT, this.gl.FALSE, 3*Float32Array.BYTES_PER_ELEMENT, 0);
        this.gl.enableVertexAttribArray(this.colorLocation);
        this.shaderprog.startUsing();
        this.gl.drawArrays(this.gl.TRIANGLES,0,3);
        this.shaderprog.stopUsing();
    }
}
var app25 = new myapp25('canvas25');
app25.run();
</script>
'''),
    md("## Exercise 2.6 - rotate + move up/down\nAfter rotation I add a sin to y."),
    code(r'''%%html
<p>Ex 2.6</p>
<canvas id="canvas26" width="400" height="400" style="border:2px solid #000000;"></canvas>
<script>
class myapp26 extends DEECapp{
    counter=0;
    initialize(){
        super.initialize();
        this.gl.clearColor(1.0,1.0,1.0,1.0);
        this.numvertices = 3;
        this.x0 = [ 0.0, -0.30,  0.30];
        this.y0 = [ 0.35, -0.20, -0.20];
        this.vertices = [0,0, 0,0, 0,0];
        this.colors = [1,0,0, 0,1,0, 0,0,1];
        this.vertexbuffer=this.gl.createBuffer();
        this.colorbuffer=this.gl.createBuffer();
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.colorbuffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.colors), this.gl.STATIC_DRAW);
        this.starttime = Date.now();
    }
    render(){
        var t = (Date.now() - this.starttime) * 0.001;
        var c = Math.cos(t);
        var s = Math.sin(t);
        var ty = 0.35 * Math.sin(t);
        for(var i=0; i<3; i++){
            var xr = this.x0[i]*c - this.y0[i]*s;
            var yr = this.x0[i]*s + this.y0[i]*c;
            this.vertices[2*i] = xr;
            this.vertices[2*i+1] = yr + ty;
        }
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.vertexbuffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.vertices), this.gl.STATIC_DRAW);
        this.gl.clear(this.gl.COLOR_BUFFER_BIT);
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.vertexbuffer);
        this.positionLocation = this.gl.getAttribLocation(this.shaderprog.shaderProgram, "in_Position");
        this.gl.vertexAttribPointer(this.positionLocation, 2, this.gl.FLOAT, this.gl.FALSE, 2*Float32Array.BYTES_PER_ELEMENT, 0);
        this.gl.enableVertexAttribArray(this.positionLocation);
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.colorbuffer);
        this.colorLocation = this.gl.getAttribLocation(this.shaderprog.shaderProgram, "in_Color");
        this.gl.vertexAttribPointer(this.colorLocation, 3, this.gl.FLOAT, this.gl.FALSE, 3*Float32Array.BYTES_PER_ELEMENT, 0);
        this.gl.enableVertexAttribArray(this.colorLocation);
        this.shaderprog.startUsing();
        this.gl.drawArrays(this.gl.TRIANGLES,0,this.numvertices);
        this.shaderprog.stopUsing();
    }
}
var app26 = new myapp26('canvas26');
app26.run();
</script>
'''),
    md("## Exercise 2.7 - same idea on Z\nPDF says add Z and use 3D vertex shader. Simple version: I change Z with sin (visible with depth if you add another object later)."),
    code(r'''%%html
<p>Ex 2.7</p>
<script id="my-vertex-shader3D" type="x-shader/x-vertex">
precision highp float;
attribute vec3 in_Position;
attribute vec3 in_Color;
varying vec3 ex_Color;
void main(void){
    gl_Position = vec4(in_Position.x, in_Position.y, in_Position.z, 1.0);
    ex_Color = in_Color;
}
</script>
<canvas id="canvas27" width="400" height="400" style="border:2px solid #000000;"></canvas>
<script>
class myapp27 extends DEECapp{
    initialize(){
        // I load the 3D shader from the PDF note
        var fragsrc = document.getElementById("my-fragment-shader").text;
        var vertsrc = document.getElementById("my-vertex-shader3D").text;
        this.shaderprog = new DEECshader(this.gl);
        this.shaderprog.srcShaders(vertsrc, fragsrc);
        this.gl.clearColor(1.0,1.0,1.0,1.0);
        this.numvertices = 3;
        this.x0 = [ 0.0, -0.30,  0.30];
        this.y0 = [ 0.35, -0.20, -0.20];
        // each vertex now has x,y,z
        this.vertices = [0,0,0, 0,0,0, 0,0,0];
        this.colors = [1,0,0, 0,1,0, 0,0,1];
        this.vertexbuffer=this.gl.createBuffer();
        this.colorbuffer=this.gl.createBuffer();
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.colorbuffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.colors), this.gl.STATIC_DRAW);
        this.starttime = Date.now();
    }
    render(){
        var t = (Date.now() - this.starttime) * 0.001;
        var c = Math.cos(t);
        var s = Math.sin(t);
        var z = 0.5 * Math.sin(t);
        for(var i=0; i<3; i++){
            this.vertices[3*i]   = this.x0[i]*c - this.y0[i]*s;
            this.vertices[3*i+1] = this.x0[i]*s + this.y0[i]*c;
            this.vertices[3*i+2] = z;
        }
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.vertexbuffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.vertices), this.gl.STATIC_DRAW);
        this.gl.clear(this.gl.COLOR_BUFFER_BIT);
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.vertexbuffer);
        this.positionLocation = this.gl.getAttribLocation(this.shaderprog.shaderProgram, "in_Position");
        // 3 floats per vertex now
        this.gl.vertexAttribPointer(this.positionLocation, 3, this.gl.FLOAT, this.gl.FALSE, 3*Float32Array.BYTES_PER_ELEMENT, 0);
        this.gl.enableVertexAttribArray(this.positionLocation);
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.colorbuffer);
        this.colorLocation = this.gl.getAttribLocation(this.shaderprog.shaderProgram, "in_Color");
        this.gl.vertexAttribPointer(this.colorLocation, 3, this.gl.FLOAT, this.gl.FALSE, 3*Float32Array.BYTES_PER_ELEMENT, 0);
        this.gl.enableVertexAttribArray(this.colorLocation);
        this.shaderprog.startUsing();
        this.gl.drawArrays(this.gl.TRIANGLES,0,this.numvertices);
        this.shaderprog.stopUsing();
    }
}
var app27 = new myapp27('canvas27');
app27.run();
</script>
'''),
]
save("Ch2_basic_from_examples.ipynb", {
    "cells": ch2_cells,
    "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python"}},
    "nbformat": 4,
    "nbformat_minor": 5,
})

print("part A done")
