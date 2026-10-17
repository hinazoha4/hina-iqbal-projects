"""Basic Ch3 + Ch4 from professor style + explain file."""
import json
from pathlib import Path

OUT = Path(r"c:\Users\Lenovo\Downloads\computer architecture\graphics_AR_labs\BASIC_SOLUTIONS")
OUT.mkdir(exist_ok=True)


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


def save(name, cells):
    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    (OUT / name).write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding="utf-8")
    print("wrote", name)


LIBS = r'''%%html
<script src="https://is3l.isr.uc.pt/~pm/CGRA/JS/deecshader.js"></script>
<script src="https://is3l.isr.uc.pt/~pm/CGRA/JS/deecapp.js"></script>
'''

GLM = r'''%%html
<script src="https://git.io/glm-js.min.js"></script>
'''

# For ch3: each exercise is a SMALL change to shader like professor asks
# One notebook with separate shader ids and simple apps

ch3 = [
    md("# My exercises - Chapter 3\nI started from the Triangle example. For each exercise I only changed the shader a little, like the PDF says.\nUse **Voilà**."),
    code(LIBS),
    code(r'''%%html
<script id="my-fragment-shader" type="x-shader/x-fragment">
precision highp float;
varying  vec3 ex_Color;
void main(void) {
    gl_FragColor = vec4(ex_Color,1.0);
}
</script>

<!-- Ex 3.1 vertex: scale 0.5 -->
<script id="vert31" type="x-shader/x-vertex">
precision highp float;
attribute  vec2 in_Position;
attribute  vec3 in_Color;
varying  vec3 ex_Color;
void main(void) {
    gl_Position = vec4(in_Position.x * 0.5, in_Position.y * 0.5, 0.0, 1.0);
    ex_Color = in_Color;
}
</script>

<!-- Ex 3.2 vertex: red always 1 -->
<script id="vert32" type="x-shader/x-vertex">
precision highp float;
attribute  vec2 in_Position;
attribute  vec3 in_Color;
varying  vec3 ex_Color;
void main(void) {
    gl_Position = vec4(in_Position.x, in_Position.y, 0.0, 1.0);
    ex_Color = vec3(1.0, in_Color.g, in_Color.b);
}
</script>

<!-- normal vertex for other exercises -->
<script id="vertNormal" type="x-shader/x-vertex">
precision highp float;
attribute  vec2 in_Position;
attribute  vec3 in_Color;
varying  vec3 ex_Color;
void main(void) {
    gl_Position = vec4(in_Position.x, in_Position.y, 0.0, 1.0);
    ex_Color = in_Color;
}
</script>

<!-- Ex 3.3 fragment -->
<script id="frag33" type="x-shader/x-fragment">
precision highp float;
varying  vec3 ex_Color;
void main(void) {
    float b;
    if (ex_Color.b < 0.5) {
        b = 0.0;
    } else {
        b = 1.0;
    }
    gl_FragColor = vec4(ex_Color.r, ex_Color.g, b, 1.0);
}
</script>

<!-- Ex 3.4 vertex with time -->
<script id="vert34" type="x-shader/x-vertex">
precision highp float;
attribute  vec2 in_Position;
attribute  vec3 in_Color;
varying  vec3 ex_Color;
uniform float timepar;
void main(void) {
    float K1 = 0.2;
    float K2 = 500.0;
    float y = in_Position.y + K1 * sin(timepar / K2);
    gl_Position = vec4(in_Position.x, y, 0.0, 1.0);
    ex_Color = in_Color;
}
</script>

<!-- Ex 3.5 scale with time -->
<script id="vert35" type="x-shader/x-vertex">
precision highp float;
attribute  vec2 in_Position;
attribute  vec3 in_Color;
varying  vec3 ex_Color;
uniform float timepar;
void main(void) {
    float K2 = 500.0;
    float scale = 0.5 + 0.25 * sin(timepar / K2);
    gl_Position = vec4(in_Position.x * scale, in_Position.y * scale, 0.0, 1.0);
    ex_Color = in_Color;
}
</script>

<!-- Ex 3.6 rotate with time -->
<script id="vert36" type="x-shader/x-vertex">
precision highp float;
attribute  vec2 in_Position;
attribute  vec3 in_Color;
varying  vec3 ex_Color;
uniform float timepar;
void main(void) {
    float ang = timepar / 1000.0;
    float c = cos(ang);
    float s = sin(ang);
    float x = in_Position.x * c - in_Position.y * s;
    float y = in_Position.x * s + in_Position.y * c;
    gl_Position = vec4(x, y, 0.0, 1.0);
    ex_Color = in_Color;
}
</script>

<!-- Ex 3.7 fragment green with time -->
<script id="frag37" type="x-shader/x-fragment">
precision highp float;
varying  vec3 ex_Color;
uniform float timepar;
void main(void) {
    float K2 = 500.0;
    float g = 0.5 + 0.5 * sin(timepar / K2);
    gl_FragColor = vec4(ex_Color.r, g, ex_Color.b, 1.0);
}
</script>
'''),
]

# Simple student app factory as raw duplicated cells
def simple_shader_app(ex_num, canvas, cls, vert_id, frag_id, use_time=False):
    time_bits_init = "        this.starttime = Date.now();\n" if use_time else ""
    time_bits_render = ""
    if use_time:
        time_bits_render = """        var timevariable = (Date.now() - this.starttime) * 1.0;
        this.shaderprog.startUsing();
        var timeLoc = this.gl.getUniformLocation(this.shaderprog.shaderProgram, "timepar");
        this.gl.uniform1f(timeLoc, timevariable);
"""
    return code(f'''%%html
<p>Ex {ex_num}</p>
<canvas id="{canvas}" width="400" height="400" style="border:2px solid #000000;"></canvas>
<script>
class {cls} extends DEECapp{{
    counter=0;
    initialize(){{
        // I choose which shader scripts to use for this exercise
        var vertsrc = document.getElementById("{vert_id}").text;
        var fragsrc = document.getElementById("{frag_id}").text;
        this.shaderprog = new DEECshader(this.gl);
        this.shaderprog.srcShaders(vertsrc, fragsrc);
        this.gl.clearColor(1.0,1.0,1.0,1.0);

        this.numvertices = 3;
        this.vertices =
            [ -0.90, -0.90 ,
               0.85, -0.90 ,
              -0.90,  0.85];
        this.colors = [
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0];

{time_bits_init}
        this.vertexbuffer=this.gl.createBuffer();
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.vertexbuffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.vertices), this.gl.STATIC_DRAW);
        this.colorbuffer=this.gl.createBuffer();
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.colorbuffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.colors), this.gl.STATIC_DRAW);
    }}
    render(){{
{time_bits_render}
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
    }}
}}
var app{ex_num.replace(".","")} = new {cls}('{canvas}');
app{ex_num.replace(".","")}.run();
</script>
''')


ch3 += [
    md("## Ex 3.1 - scale 0.5 in vertex shader"),
    simple_shader_app("3.1", "c31", "myapp31", "vert31", "my-fragment-shader"),
    md("## Ex 3.2 - red always 1"),
    simple_shader_app("3.2", "c32", "myapp32", "vert32", "my-fragment-shader"),
    md("## Ex 3.3 - blue threshold in fragment shader"),
    simple_shader_app("3.3", "c33", "myapp33", "vertNormal", "frag33"),
    md("## Ex 3.4 - y += sin(time)"),
    simple_shader_app("3.4", "c34", "myapp34", "vert34", "my-fragment-shader", use_time=True),
    md("## Ex 3.5 - scale changes with time"),
    simple_shader_app("3.5", "c35", "myapp35", "vert35", "my-fragment-shader", use_time=True),
    md("## Ex 3.6 - rotate in vertex shader with time"),
    simple_shader_app("3.6", "c36", "myapp36", "vert36", "my-fragment-shader", use_time=True),
    md("## Ex 3.7 - green changes with time"),
    simple_shader_app("3.7", "c37", "myapp37", "vertNormal", "frag37", use_time=True),
]
save("Ch3_basic_from_examples.ipynb", ch3)


# Chapter 4 - based closely on 03Transformations example
ch4 = [
    md("# My exercises - Chapter 4\nI used the Transformations example (glm-js + rotating triangle) and changed it for each exercise.\nUse **Voilà**."),
    code(GLM),
    code(LIBS),
    code(r'''%%html
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
<script id="my-fragment-shader" type="x-shader/x-fragment">
precision highp float;
varying  vec3 ex_Color;
void main(void) {
    gl_FragColor = vec4(ex_Color,1.0);
}
</script>
'''),
    md("## Ex 4.1 - small blue triangle on a sinusoid (left to right, wraps)\nLike Transformations example, but I translate with GLM instead of only rotate."),
    code(r'''%%html
<p>Ex 4.1</p>
<canvas id="c41" width="400" height="400" style="border:2px solid #000000;"></canvas>
<script>
class myapp41 extends DEECapp{
    counter=0;
    initialize(){
        super.initialize();
        this.gl.clearColor(1.0,1.0,1.0,1.0);
        this.numvertices = 3;
        // very small triangle in local coords
        this.v1 = glm.vec4(-0.05,  0.06, 0, 1);
        this.v2 = glm.vec4(-0.05, -0.06, 0, 1);
        this.v3 = glm.vec4( 0.05, -0.06, 0, 1);
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
        var t = (Date.now() - this.starttime) * 0.001;
        // x goes left to right and wraps
        var x = -1.0 + (t * 0.25) % 2.0;
        var y = 0.4 * Math.sin(3.14 * x);

        // translation matrix (like Transformations example style)
        var T = glm.mat4(1.0);
        T[3] = glm.vec4(x, y, 0, 1);

        var p1 = T['*'](this.v1);
        var p2 = T['*'](this.v2);
        var p3 = T['*'](this.v3);
        this.vertices[0]=p1.x; this.vertices[1]=p1.y;
        this.vertices[2]=p2.x; this.vertices[3]=p2.y;
        this.vertices[4]=p3.x; this.vertices[5]=p3.y;

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
var app41 = new myapp41('c41');
app41.run();
</script>
'''),
    md("## Ex 4.2 - same + rotate (like Transformations example rotation)"),
    code(r'''%%html
<p>Ex 4.2</p>
<canvas id="c42" width="400" height="400" style="border:2px solid #000000;"></canvas>
<script>
class myapp42 extends DEECapp{
    counter=0;
    initialize(){
        super.initialize();
        this.gl.clearColor(1.0,1.0,1.0,1.0);
        this.numvertices = 3;
        this.v1 = glm.vec4(-0.05,  0.06, 0, 1);
        this.v2 = glm.vec4(-0.05, -0.06, 0, 1);
        this.v3 = glm.vec4( 0.05, -0.06, 0, 1);
        this.vertices = [0,0, 0,0, 0,0];
        this.colors = [0,0,1, 0,0,1, 0,0,1];
        this.vertexbuffer=this.gl.createBuffer();
        this.colorbuffer=this.gl.createBuffer();
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.colorbuffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.colors), this.gl.STATIC_DRAW);
        this.starttime = Date.now();
    }
    render(){
        var t = (Date.now() - this.starttime) * 0.001;
        var x = -1.0 + (t * 0.25) % 2.0;
        var y = 0.4 * Math.sin(3.14 * x);

        // rotation like Transformations example
        var q = glm.angleAxis(t, glm.vec3(0, 0, 1));
        var R = glm.toMat4(q);
        var T = glm.mat4(1.0);
        T[3] = glm.vec4(x, y, 0, 1);
        // first rotate, then translate
        var M = T['*'](R);

        var p1 = M['*'](this.v1);
        var p2 = M['*'](this.v2);
        var p3 = M['*'](this.v3);
        this.vertices[0]=p1.x; this.vertices[1]=p1.y;
        this.vertices[2]=p2.x; this.vertices[3]=p2.y;
        this.vertices[4]=p3.x; this.vertices[5]=p3.y;

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
    initialize(){
        super.initialize();
        this.gl.clearColor(1.0,1.0,1.0,1.0);
        // small triangle
        this.tv1 = glm.vec4(-0.05, 0.06, 0, 1);
        this.tv2 = glm.vec4(-0.05,-0.06, 0, 1);
        this.tv3 = glm.vec4( 0.05,-0.06, 0, 1);
        this.tri_vertices = [0,0, 0,0, 0,0];
        this.tri_colors = [0,0,1, 0,0,1, 0,0,1];
        // small rectangle (2 triangles) around origin
        this.rv = [
            glm.vec4(-0.12,-0.06,0,1), glm.vec4(0.12,-0.06,0,1), glm.vec4(0.12,0.06,0,1),
            glm.vec4(-0.12,-0.06,0,1), glm.vec4(0.12, 0.06,0,1), glm.vec4(-0.12,0.06,0,1)
        ];
        this.rect_vertices = new Array(12);
        this.rect_colors = [1,0,0, 1,0,0, 1,0,0, 1,0,0, 1,0,0, 1,0,0];
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
    render(){
        var t = (Date.now() - this.starttime) * 0.001;
        var x = -1.0 + (t * 0.25) % 2.0;
        var y = 0.4 * Math.sin(3.14 * x);

        var q = glm.angleAxis(t, glm.vec3(0,0,1));
        var R = glm.toMat4(q);
        var T = glm.mat4(1.0);
        T[3] = glm.vec4(x,y,0,1);
        var M = T['*'](R);
        var p1=M['*'](this.tv1), p2=M['*'](this.tv2), p3=M['*'](this.tv3);
        this.tri_vertices=[p1.x,p1.y, p2.x,p2.y, p3.x,p3.y];

        // rectangle rotates under, fixed position y=-0.55
        var q2 = glm.angleAxis(-0.7*t, glm.vec3(0,0,1));
        var R2 = glm.toMat4(q2);
        var T2 = glm.mat4(1.0);
        T2[3] = glm.vec4(0, -0.55, 0, 1);
        var M2 = T2['*'](R2);
        for(var i=0;i<6;i++){
            var p = M2['*'](this.rv[i]);
            this.rect_vertices[2*i]=p.x;
            this.rect_vertices[2*i+1]=p.y;
        }

        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.tri_vbuf);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.tri_vertices), this.gl.STATIC_DRAW);
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.rect_vbuf);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(this.rect_vertices), this.gl.STATIC_DRAW);

        this.gl.clear(this.gl.COLOR_BUFFER_BIT);

        // draw rectangle
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

        // draw triangle
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
var app43 = new myapp43('c43');
app43.run();
</script>
'''),
    md("## Ex 4.4 - simple clock (3 rectangle hands)\nI use Date() like the PDF."),
    code(r'''%%html
<p>Ex 4.4</p>
<canvas id="c44" width="400" height="400" style="border:2px solid #000000;"></canvas>
<script>
class myapp44 extends DEECapp{
    initialize(){
        super.initialize();
        this.gl.clearColor(1.0,1.0,1.0,1.0);
        // one rectangle pointing up (along +y), different lengths later by scale in y
        this.hand = [
            glm.vec4(-0.02, 0.0, 0, 1),
            glm.vec4( 0.02, 0.0, 0, 1),
            glm.vec4( 0.02, 1.0, 0, 1),
            glm.vec4(-0.02, 0.0, 0, 1),
            glm.vec4( 0.02, 1.0, 0, 1),
            glm.vec4(-0.02, 1.0, 0, 1)
        ];
        this.h_len = 0.35;
        this.m_len = 0.50;
        this.s_len = 0.65;
        this.h_col = [0.2,0.2,0.2, 0.2,0.2,0.2, 0.2,0.2,0.2, 0.2,0.2,0.2, 0.2,0.2,0.2, 0.2,0.2,0.2];
        this.m_col = [0,0,0.7, 0,0,0.7, 0,0,0.7, 0,0,0.7, 0,0,0.7, 0,0,0.7];
        this.s_col = [0.8,0,0, 0.8,0,0, 0.8,0,0, 0.8,0,0, 0.8,0,0, 0.8,0,0];
        this.vbuf=this.gl.createBuffer();
        this.cbuf=this.gl.createBuffer();
    }
    drawHand(ang, len, colors){
        // scale in y, then rotate
        var S = glm.mat4(1.0);
        S[1][1] = len; // scale y
        var q = glm.angleAxis(ang, glm.vec3(0,0,1));
        var R = glm.toMat4(q);
        var M = R['*'](S);
        var verts = [];
        for(var i=0;i<6;i++){
            var p = M['*'](this.hand[i]);
            verts.push(p.x); verts.push(p.y);
        }
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.vbuf);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(verts), this.gl.STATIC_DRAW);
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.cbuf);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(colors), this.gl.STATIC_DRAW);

        this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.vbuf);
        this.positionLocation = this.gl.getAttribLocation(this.shaderprog.shaderProgram, "in_Position");
        this.gl.vertexAttribPointer(this.positionLocation, 2, this.gl.FLOAT, this.gl.FALSE, 2*Float32Array.BYTES_PER_ELEMENT, 0);
        this.gl.enableVertexAttribArray(this.positionLocation);
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.cbuf);
        this.colorLocation = this.gl.getAttribLocation(this.shaderprog.shaderProgram, "in_Color");
        this.gl.vertexAttribPointer(this.colorLocation, 3, this.gl.FLOAT, this.gl.FALSE, 3*Float32Array.BYTES_PER_ELEMENT, 0);
        this.gl.enableVertexAttribArray(this.colorLocation);
        this.shaderprog.startUsing();
        this.gl.drawArrays(this.gl.TRIANGLES,0,6);
        this.shaderprog.stopUsing();
    }
    render(){
        var today = new Date();
        var hours = today.getHours();
        var minutes = today.getMinutes();
        var secs = today.getSeconds();

        // clock angles (negative = clockwise on screen)
        var angS = -secs * (2*3.1416/60);
        var angM = -(minutes + secs/60.0) * (2*3.1416/60);
        var angH = -((hours%12) + minutes/60.0) * (2*3.1416/12);

        this.gl.clear(this.gl.COLOR_BUFFER_BIT);
        this.drawHand(angH, this.h_len, this.h_col);
        this.drawHand(angM, this.m_len, this.m_col);
        this.drawHand(angS, this.s_len, this.s_col);
    }
}
var app44 = new myapp44('c44');
app44.run();
</script>
'''),
]
save("Ch4_basic_from_examples.ipynb", ch4)

explain = r'''BASIC SOLUTIONS - HAR LINE KA MATLAB
=====================================
Folder: graphics_AR_labs\BASIC_SOLUTIONS\

Upload Jupyter pe:
  Ch1_basic_from_examples.ipynb
  Ch2_basic_from_examples.ipynb
  Ch3_basic_from_examples.ipynb
  Ch4_basic_from_examples.ipynb

Pehle examples folder se 01Lines / 02Triangle / 03Transformations
dekh lo - YE CODE USI STYLE MEIN HAI.


COMMON TEMPLATE (har exercise me yahi hota hai)
-----------------------------------------------
%%html
  = Jupyter ko bolta hai: yeh HTML/JS cell hai

<script src="...deecshader.js">
<script src="...deecapp.js">
  = professor ki libraries (example jaisi)

my-vertex-shader
  = har corner (vertex) pe chalta hai
  in_Position = x,y
  in_Color = r,g,b
  gl_Position = screen pe kahan
  ex_Color = colour aage bhejo

my-fragment-shader
  = har pixel ka final colour
  gl_FragColor = dikhne wala rang

<canvas id="...">
  = drawing box (har exercise ka alag id)

class myappXX extends DEECapp
  = professor ka app class extend

initialize()
  super.initialize() = shaders load
  clearColor(1,1,1,1) = white background
  vertices = [x,y, x,y, ...]  MUST be -1..1
  colors = [r,g,b, r,g,b, ...]
  createBuffer / bindBuffer / bufferData = data GPU pe

render()
  clear = screen saaf
  getAttribLocation + vertexAttribPointer = shader ko data se jodo
  drawArrays(MODE, 0, n) = draw
  MODE examples:
    TRIANGLES, LINE_LOOP, POINTS, LINE_STRIP, LINES,
    TRIANGLE_STRIP, TRIANGLE_FAN

var app = new myappXX('canvasId');
app.run();
  = start


AGAR PROFESSOR CHANGE BOLAY - KYA EDIT KARNA
--------------------------------------------
Colours change     -> colors array
Shape change       -> vertices array
Outline vs fill    -> drawArrays mode
Speed of motion    -> Math.sin(...) ke andar number
Size               -> vertices numbers chhote/bade
Add point          -> vertices me 2 numbers + colors me 3 + numvertices++


CHAPTER WISE - MAINE KYA CHANGE KIYA (example se)
------------------------------------------------
Ch1:
  1.1 vertices + colors
  1.2 console.log + grey background (Lines example jaisa)
  1.3 4 points + LINE_LOOP (Lines example jaisa)
  1.4 sirf drawArrays mode (tum POINTS etc try karo)

Ch2:
  2.1 isosceles vertices
  2.2 do objects: rect pehle, triangle baad
  2.3 vertices[1] = sin(time)  (Date.now)
  2.4 rotation formula from PDF
  2.5 2.2 + 2.4
  2.6 rotation + ty = sin
  2.7 3D shader from PDF + z = sin

Ch3: (Triangle points same as professor example)
  3.1 shader me * 0.5
  3.2 ex_Color.r = 1
  3.3 if blue < 0.5
  3.4-3.7 uniform timepar (PDF jaisa)

Ch4: (Transformations example + glm)
  4.1 translate on sinusoid
  4.2 + rotate (angleAxis like example)
  4.3 + rectangle under
  4.4 Date() hours/minutes/secs
'''

(OUT / "SAMJHO_HAR_LINE.txt").write_text(explain, encoding="utf-8")
(OUT / "UPLOAD.txt").write_text(
    "1) VPN + JupyterHub\n"
    "2) Upload 4 notebooks from BASIC_SOLUTIONS\n"
    "3) Open -> Voila (not Run)\n"
    "4) Read SAMJHO_HAR_LINE.txt\n",
    encoding="utf-8",
)
print("done")
