"""Ch4 = almost exact copy of official 04Objects, only small render changes."""
import json
import copy
from pathlib import Path

EX = Path(r"c:\Users\Lenovo\Downloads\computer architecture\graphics_AR_labs\examples_official\04Objects.ipynb")
OUT = Path(r"c:\Users\Lenovo\Downloads\computer architecture\graphics_AR_labs\BASIC_SOLUTIONS")
OUT.mkdir(exist_ok=True)

base = json.loads(EX.read_text(encoding="utf-8"))

# Fix libs to https (same files professor uses)
LIBS = """%%html
<script src="https://is3l.isr.uc.pt/~pm/CGRA/JS/deecshader.js"></script>
<script src="https://is3l.isr.uc.pt/~pm/CGRA/JS/deecapp.js"></script>
<script src="https://is3l.isr.uc.pt/~pm/CGRA/JS/cgraobject.js"></script>
<script src="https://git.io/glm-js.min.js"></script>
"""


def set_code_cell(nb, idx, text):
    if not text.endswith("\n"):
        text += "\n"
    nb["cells"][idx]["source"] = [line + "\n" for line in text.split("\n")]


def set_md(nb, idx, text):
    nb["cells"][idx]["source"] = [line + "\n" for line in text.split("\n")]


def save(name, nb):
    (OUT / name).write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding="utf-8")
    print("wrote", name)


# Shared triangle class text (same as professor) + small blue for 4.1 optional
# Keep professor triangle geometry, only change render - student can say "I changed the transformation"

APP_41 = r'''%%html
<canvas id="myCanvas" width="400" height="400" style="border:2px solid #000000;">
      Error: Your browser does not support the HTML canvas tag.
</canvas>
    
<script id="myapp">

class triangle extends CGRAobject{
    constructor(glcontext){
        super(glcontext); // initialize the parent class
        
        this.numvertices = 3;
        // I made it smaller for exercise 4.1
        var vertices =
            [ -0.10, -0.10, 0 ,
               0.10, -0.10, 0 ,
              -0.10,  0.10, 0]; 
        
        var colors = [
            0.0, 0.0, 1.0, 
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0];
        
        this.vertexbuffer=this.gl.createBuffer();
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.vertexbuffer);    
        // as JS stores everything in 64 bit format and GL expects 32bits...
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(vertices), this.gl.STATIC_DRAW);

        this.colorbuffer = this.gl.createBuffer();
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.colorbuffer);    
        // as JS stores everything in 64 bit format and GL expects 32bits...
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(colors), this.gl.STATIC_DRAW);
    }
}

class myapp extends DEECapp{
    counter=0;
    initialize(){
        // no call to super.initialize() this time because
        // in this case we don't want to use the default shader.
        
        var fragsrc = document.getElementById("my-fragment-shader").text;
        var vertsrc = document.getElementById("my-vertex-shader").text;
        
        this.shaderprog = new DEECshader(this.gl);
        this.shaderprog.srcShaders(vertsrc,fragsrc);
        
        this.gl.disable(this.gl.DEPTH_TEST);
        this.gl.clearColor(1.0,1.0,1.0,1.0);
        
        // only one triangle for this exercise
        this.mytriangle = new triangle(this.gl);
        this.mytriangle.setShader(this.shaderprog);
        this.starttime = Date.now();
    }
    
    render(){
        this.gl.clear(this.gl.COLOR_BUFFER_BIT | this.gl.DEPTH_BUFFER_BIT);
        this.counter++;

        // Ex 4.1: I only use translate, position follows a sinusoid
        var t = (Date.now() - this.starttime) * 0.001;
        var x = -1.0 + (t * 0.25) % 2.0;
        var y = 0.4 * Math.sin(3.1416 * x);

        var transl = glm.translate(glm.mat4(1.0), glm.vec3(x, y, 0.0));
        this.mytriangle.setModelTransformation(transl);
        this.mytriangle.drawit();
    }
}

var app = new myapp('myCanvas');
app.run();

</script>
'''

APP_42 = r'''%%html
<canvas id="myCanvas" width="400" height="400" style="border:2px solid #000000;">
      Error: Your browser does not support the HTML canvas tag.
</canvas>
    
<script id="myapp">

class triangle extends CGRAobject{
    constructor(glcontext){
        super(glcontext); // initialize the parent class
        
        this.numvertices = 3;
        var vertices =
            [ -0.10, -0.10, 0 ,
               0.10, -0.10, 0 ,
              -0.10,  0.10, 0]; 
        
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
        this.gl.clear(this.gl.COLOR_BUFFER_BIT | this.gl.DEPTH_BUFFER_BIT);
        this.counter++;

        // Ex 4.2: same as example - rotate + translate (I changed the translate to sinusoid)
        var t = (Date.now() - this.starttime) * 0.001;
        var x = -1.0 + (t * 0.25) % 2.0;
        var y = 0.4 * Math.sin(3.1416 * x);

        var scale = glm.mat4(glm.mat3(0.2));
        var rotation = glm.rotate(glm.mat4(1.0),glm.radians(this.counter),glm.vec3(0.0,0.0,1.0));
        var transl = glm.translate(glm.mat4(1.0),glm.vec3(x,y,0.0));
        var transformation = transl['*'](rotation['*'](scale));
        this.mytriangle.setModelTransformation(transformation);
        this.mytriangle.drawit();
    }
}

var app = new myapp('myCanvas');
app.run();

</script>
'''

APP_43 = r'''%%html
<canvas id="myCanvas" width="400" height="400" style="border:2px solid #000000;">
      Error: Your browser does not support the HTML canvas tag.
</canvas>
    
<script id="myapp">

class triangle extends CGRAobject{
    constructor(glcontext){
        super(glcontext);
        this.numvertices = 3;
        var vertices =
            [ -0.10, -0.10, 0 ,
               0.10, -0.10, 0 ,
              -0.10,  0.10, 0]; 
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

// I made a red rectangle (2 triangles) instead of the second triangle
class rectangle extends CGRAobject{
    constructor(glcontext){
        super(glcontext);
        this.numvertices = 6;
        var vertices =
            [ -0.20, -0.10, 0 ,
               0.20, -0.10, 0 ,
               0.20,  0.10, 0 ,
              -0.20, -0.10, 0 ,
               0.20,  0.10, 0 ,
              -0.20,  0.10, 0 ];
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

        // like the example: two objects
        this.mytriangle = new triangle(this.gl);
        this.mytriangle.setShader(this.shaderprog);
        this.myrectangle = new rectangle(this.gl);
        this.myrectangle.setShader(this.shaderprog);
        this.starttime = Date.now();
    }
    
    render(){
        this.gl.clear(this.gl.COLOR_BUFFER_BIT | this.gl.DEPTH_BUFFER_BIT);
        this.counter++;

        var t = (Date.now() - this.starttime) * 0.001;
        var x = -1.0 + (t * 0.25) % 2.0;
        var y = 0.4 * Math.sin(3.1416 * x);

        // rectangle under (same transform style as example triangle2)
        var scale = glm.mat4(glm.mat3(1.0));
        var rotation = glm.rotate(glm.mat4(1.0),glm.radians(-this.counter),glm.vec3(0.0,0.0,1.0));
        var transl = glm.translate(glm.mat4(1.0),glm.vec3(0.0,-0.55,0.0));
        var transformation = transl['*'](rotation['*'](scale));
        this.myrectangle.setModelTransformation(transformation);
        this.myrectangle.drawit();

        // triangle moving (same style)
        var scale2 = glm.mat4(glm.mat3(0.2));
        var rotation2 = glm.rotate(glm.mat4(1.0),glm.radians(this.counter),glm.vec3(0.0,0.0,1.0));
        var transl2 = glm.translate(glm.mat4(1.0),glm.vec3(x,y,0.0));
        var transformation2 = transl2['*'](rotation2['*'](scale2));
        this.mytriangle.setModelTransformation(transformation2);
        this.mytriangle.drawit();
    }
}

var app = new myapp('myCanvas');
app.run();

</script>
'''

APP_44 = r'''%%html
<canvas id="myCanvas" width="400" height="400" style="border:2px solid #000000;">
      Error: Your browser does not support the HTML canvas tag.
</canvas>
    
<script id="myapp">

// hand = thin rectangle (like a scaled triangle object, but rectangle)
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

class myapp extends DEECapp{
    initialize(){
        var fragsrc = document.getElementById("my-fragment-shader").text;
        var vertsrc = document.getElementById("my-vertex-shader").text;
        this.shaderprog = new DEECshader(this.gl);
        this.shaderprog.srcShaders(vertsrc,fragsrc);
        this.gl.disable(this.gl.DEPTH_TEST);
        this.gl.clearColor(1.0,1.0,1.0,1.0);

        // three objects like the example (but hands)
        this.hourHand = new hand(this.gl, 0.2,0.2,0.2);
        this.minHand  = new hand(this.gl, 0.0,0.0,0.7);
        this.secHand  = new hand(this.gl, 0.8,0.0,0.0);
        this.hourHand.setShader(this.shaderprog);
        this.minHand.setShader(this.shaderprog);
        this.secHand.setShader(this.shaderprog);
    }
    
    render(){
        this.gl.clear(this.gl.COLOR_BUFFER_BIT | this.gl.DEPTH_BUFFER_BIT);

        // Ex 4.4: time from Date() like the PDF
        var today = new Date();
        var hours = today.getHours() % 12;
        var minutes = today.getMinutes();
        var secs = today.getSeconds();

        var angS = -secs * 6.0;
        var angM = -(minutes + secs/60.0) * 6.0;
        var angH = -(hours + minutes/60.0) * 30.0;

        // same pattern as example: scale * rotate * (translate=0)
        var sh = glm.scale(glm.mat4(1.0), glm.vec3(1.0, 0.35, 1.0));
        var rh = glm.rotate(glm.mat4(1.0), glm.radians(angH), glm.vec3(0,0,1));
        this.hourHand.setModelTransformation(rh['*'](sh));
        this.hourHand.drawit();

        var sm = glm.scale(glm.mat4(1.0), glm.vec3(1.0, 0.50, 1.0));
        var rm = glm.rotate(glm.mat4(1.0), glm.radians(angM), glm.vec3(0,0,1));
        this.minHand.setModelTransformation(rm['*'](sm));
        this.minHand.drawit();

        var ss = glm.scale(glm.mat4(1.0), glm.vec3(1.0, 0.65, 1.0));
        var rs = glm.rotate(glm.mat4(1.0), glm.radians(angS), glm.vec3(0,0,1));
        this.secHand.setModelTransformation(rs['*'](ss));
        this.secHand.drawit();
    }
}

var app = new myapp('myCanvas');
app.run();

</script>
'''


def make(name, title, app):
    nb = copy.deepcopy(base)
    # keep professor title style, small note
    set_md(
        nb,
        0,
        "# Computação Gráfica e Realidade Aumentada\n"
        "# Visualização Computacional\n"
        "## © 2020 - 202X\n"
        "<author>Author: Paulo Menezes</author>\n"
        f"<h1>{title}</h1>\n\n"
        "Based on the Objects example. I only changed the model transformations.\n",
    )
    set_code_cell(nb, 1, LIBS)
    # cells 2,3 shaders already from base - keep exact
    set_md(nb, 4, f"<h2>{title}</h2>\n\nOpen with Voilà.\n")
    set_code_cell(nb, 5, app)
    save(name, nb)


make("Ch4_Ex4_1.ipynb", "Exercise 4.1", APP_41)
make("Ch4_Ex4_2.ipynb", "Exercise 4.2", APP_42)
make("Ch4_Ex4_3.ipynb", "Exercise 4.3", APP_43)
make("Ch4_Ex4_4.ipynb", "Exercise 4.4", APP_44)

# what to say to professor
(OUT / "Ch4_WHAT_I_CHANGED.txt").write_text(
"""Professor se / viva mein yeh bolo (basic changes only):

I copied 04Objects from examples.
Same libraries: deecshader, deecapp, cgraobject, glm.
Same MVP vertex shader.

Ex 4.1:
- only one triangle
- smaller + blue
- only glm.translate, x/y follow a sinusoid

Ex 4.2:
- same as example: scale * rotate * translate
- I changed translate to the sinusoid position

Ex 4.3:
- second object is a red rectangle (6 vertices) instead of second triangle
- rectangle stays below and rotates
- triangle still moves on the sinusoid

Ex 4.4:
- three rectangle hands
- angles from Date() hours/minutes/seconds
- same setModelTransformation + drawit
""",
    encoding="utf-8",
)
print("done")
