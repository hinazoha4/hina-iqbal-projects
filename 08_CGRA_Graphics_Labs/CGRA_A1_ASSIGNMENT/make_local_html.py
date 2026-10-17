# -*- coding: utf-8 -*-
from pathlib import Path

root = Path(__file__).resolve().parent
shapes = (root / "js" / "shapes_basic.js").read_text(encoding="utf-8")
scene = (root / "js" / "scene_app.js").read_text(encoding="utf-8")

vert = """
<script id="my-vertex-shader" type="x-shader/x-vertex">
precision mediump float;
attribute vec3 in_Position;
attribute vec3 in_Color;
uniform mat4 MVP;
varying vec3 ex_Color;
void main(void){
  gl_Position = MVP * vec4(in_Position, 1.0);
  ex_Color = in_Color;
}
</script>
"""

frag = """
<script id="my-fragment-shader" type="x-shader/x-fragment">
precision mediump float;
varying vec3 ex_Color;
void main(void){ gl_FragColor = vec4(ex_Color,1.0); }
</script>
"""

libs = """
<script src="../js/deecshader.js"></script>
<script src="../js/deecapp.js"></script>
<script src="../js/cgraobject.js"></script>
<script src="https://cdn.jsdelivr.net/gh/stephengold/glm-js@master/build/glm-js.min.js"></script>
"""

exa1 = shapes + """
class myapp extends DEECapp{
  counter=0;
  initialize(){
    var fragsrc=document.getElementById('my-fragment-shader').text;
    var vertsrc=document.getElementById('my-vertex-shader').text;
    this.shaderprog=new DEECshader(this.gl);
    this.shaderprog.srcShaders(vertsrc,fragsrc);
    this.gl.enable(this.gl.DEPTH_TEST);
    this.gl.clearColor(0.9,0.9,0.95,1);
    this.shapes=[
      new Cube(this.gl,[1,0,0],[0,0,1]),
      new Sphere(this.gl,[0.2,0.6,1],[1,0.2,0.4],12,12),
      new Cylinder(this.gl,[0.6,0.6,0.6],[0.2,0.2,0.2],12),
      new Cone(this.gl,[0.9,0.5,0.1],[0.4,0.2,0.05],12),
      new Disc(this.gl,[1,1,0],[1,0.4,0],12)
    ];
    for(var i=0;i<this.shapes.length;i++) this.shapes[i].setShader(this.shaderprog);
  }
  render(){
    this.gl.clear(this.gl.COLOR_BUFFER_BIT|this.gl.DEPTH_BUFFER_BIT);
    this.counter++;
    var proj=glm.perspective(glm.radians(45), this.canvas.width/this.canvas.height, 0.1, 50);
    var view=glm.lookAt(glm.vec3(0,2,8), glm.vec3(0,0,0), glm.vec3(0,1,0));
    var spacing=[-4,-2,0,2,4];
    for(var i=0;i<this.shapes.length;i++){
      var rot=glm.rotate(glm.mat4(1), glm.radians(this.counter*0.5), glm.vec3(0.3,1,0.2));
      if(i===4) rot=glm.rotate(rot, glm.radians(70), glm.vec3(1,0,0));
      var M=glm.translate(glm.mat4(1),glm.vec3(spacing[i],0,0))['*'](rot['*'](glm.scale(glm.mat4(1),glm.vec3(0.6,0.6,0.6))));
      this.shapes[i].setModelTransformation(M);
      this.shapes[i].drawit(view,proj);
    }
  }
}
var app=new myapp('myCanvas'); app.run();
"""


def html(title, bodyjs, hint):
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{title}</title></head>
<body>
<h2>{title}</h2>
<p>{hint}</p>
{libs}
{vert}
{frag}
<canvas id="myCanvas" width="800" height="560" style="border:2px solid #000"></canvas>
<script>
{bodyjs}
</script>
</body></html>
"""


out = root / "local_test"
out.mkdir(exist_ok=True)
(out / "test_shapes.html").write_text(
    html("CGRA A1 - Shapes", exa1, "Local test: Cube Sphere Cylinder Cone Disc"),
    encoding="utf-8",
)
(out / "test_full_scene.html").write_text(
    html(
        "CGRA A1 - Full Scene",
        shapes + "\n" + scene,
        "Keys: r wheels | wasd walk | qe turn | v ride. Click canvas first.",
    ),
    encoding="utf-8",
)
print("wrote local_test html")
