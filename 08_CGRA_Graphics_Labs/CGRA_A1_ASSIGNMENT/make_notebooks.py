# -*- coding: utf-8 -*-
"""Build CGRA A1 Jupyter notebooks — Voilà-safe (wait for libs + professor style)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NB = ROOT / "notebooks"
NB.mkdir(exist_ok=True)
JS = ROOT / "js"

SHAPES = (JS / "shapes_basic.js").read_text(encoding="utf-8")
SCENE = (JS / "scene_app.js").read_text(encoding="utf-8")

# Same URLs as assignment + https (seeds is https)
LIBS_TAGS = """
<script src="https://is3l.isr.uc.pt/~pm/CGRA/JS/deecshader.js"></script>
<script src="https://is3l.isr.uc.pt/~pm/CGRA/JS/deecapp.js"></script>
<script src="https://is3l.isr.uc.pt/~pm/CGRA/JS/cgraobject.js"></script>
<script src="https://git.io/glm-js.min.js"></script>
"""

VERT_TAG = """
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
"""

FRAG_TAG = """
<script id="my-fragment-shader" type="x-shader/x-fragment">
precision mediump float;
varying  vec3 ex_Color;
void main(void) {
    gl_FragColor = vec4(ex_Color,1.0);
}
</script>
"""

# Wait until professor libs exist, THEN define classes (fixes blank Voilà canvas)
BOOT_HEAD = r"""
<div id="cgraStatus" style="color:#a00;font-family:monospace;"></div>
<script>
function cgraReady(){
  return (typeof DEECapp !== 'undefined')
      && (typeof DEECshader !== 'undefined')
      && (typeof CGRAobject !== 'undefined')
      && (typeof glm !== 'undefined');
}
function cgraBoot(startFn){
  var tries = 0;
  function go(){
    tries++;
    if (!cgraReady()){
      if (tries < 200){
        if (tries === 20){
          var el = document.getElementById('cgraStatus');
          if (el) el.textContent = 'Waiting for libraries (deecapp / cgraobject / glm)...';
        }
        setTimeout(go, 50);
        return;
      }
      var el2 = document.getElementById('cgraStatus');
      if (el2) el2.textContent = 'ERROR: libraries did not load. Check F12 console / VPN.';
      return;
    }
    var el3 = document.getElementById('cgraStatus');
    if (el3) el3.textContent = '';
    try { startFn(); }
    catch(err){
      console.error(err);
      var el4 = document.getElementById('cgraStatus');
      if (el4) el4.textContent = 'ERROR: ' + err.message;
      alert('CGRA error: ' + err.message);
    }
  }
  go();
}
</script>
"""


def md_cell(text):
    if not text.endswith("\n"):
        text += "\n"
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.split("\n")],
    }


def code_cell(text):
    if not text.endswith("\n"):
        text += "\n"
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in text.split("\n")],
    }


def save_nb(name, cells):
    nb = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python"},
        },
        "cells": cells,
    }
    path = NB / name
    path.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding="utf-8")
    print("wrote", path)


def one_cell_app(canvas_id, js_inside_boot, width=700, height=500):
    """Libs + shaders + canvas + boot wrapper in ONE %%html cell (Voilà-safe)."""
    return f"""%%html
{LIBS_TAGS}
{VERT_TAG}
{FRAG_TAG}
{BOOT_HEAD}
<canvas id="{canvas_id}" width="{width}" height="{height}" style="border:2px solid #000000; background:#ddd;">
Error: Your browser does not support the HTML canvas tag.
</canvas>
<script>
cgraBoot(function(){{
{js_inside_boot}
}});
</script>
"""


# professor-style helpers (NO glm.scale — use mat4(mat3(s)) like Objects.ipynb)
HELPERS = r"""
function T(x,y,z){ return glm.translate(glm.mat4(1.0), glm.vec3(x,y,z)); }
function R(deg, ax,ay,az){ return glm.rotate(glm.mat4(1.0), glm.radians(deg), glm.vec3(ax,ay,az)); }
function Su(s){ return glm.mat4(glm.mat3(s)); } // uniform scale (professor style)
function mul(a,b,c,d){
  var m = a['*'](b);
  if (c) m = m['*'](c);
  if (d) m = m['*'](d);
  return m;
}
"""

# ---------- Ex A.1: like Objects example (NDC, drawit with defaults) ----------
EXA1_INNER = SHAPES + HELPERS + r"""
class myapp extends DEECapp{
    counter=0;
    initialize(){
        // same pattern as professor Objects.ipynb
        var fragsrc = document.getElementById("my-vertex-shader") ? document.getElementById("my-fragment-shader").text : null;
        fragsrc = document.getElementById("my-fragment-shader").text;
        var vertsrc = document.getElementById("my-vertex-shader").text;
        this.shaderprog = new DEECshader(this.gl);
        this.shaderprog.srcShaders(vertsrc, fragsrc);
        this.gl.enable(this.gl.DEPTH_TEST);
        this.gl.clearColor(0.85, 0.85, 0.9, 1.0);

        this.shapes = [
            new Cube(this.gl, [1,0,0], [0,0,1]),
            new Sphere(this.gl, [0.2,0.6,1], [1,0.2,0.4], 12, 12),
            new Cylinder(this.gl, [0.7,0.7,0.7], [0.2,0.2,0.2], 12),
            new Cone(this.gl, [0.9,0.5,0.1], [0.4,0.2,0.05], 12),
            new Disc(this.gl, [1,1,0], [1,0.4,0], 12)
        ];
        for (var i=0;i<this.shapes.length;i++){
            this.shapes[i].setShader(this.shaderprog);
        }
        console.log('A1 shapes ready: ' + this.shapes.length);
    }
    render(){
        this.gl.clear(this.gl.COLOR_BUFFER_BIT | this.gl.DEPTH_BUFFER_BIT);
        this.counter++;
        // Like professor: NO lookAt/perspective — just model matrix in clip space
        var spacing = [-0.75, -0.35, 0.05, 0.45, 0.85];
        for (var i=0;i<this.shapes.length;i++){
            var rot = R(this.counter * 0.7, 0.4, 1.0, 0.2);
            if (i === 4) rot = mul(rot, R(70, 1,0,0)); // tilt disc
            var M = mul(T(spacing[i], 0.0, 0.0), rot, Su(0.18));
            this.shapes[i].setModelTransformation(M);
            this.shapes[i].drawit(); // defaults view=I, proj=I (Objects style)
        }
    }
}
var app = new myapp('myCanvasA1');
app.run();
"""

# ---------- A.2 + A.3 ----------
EXA23_INNER = SHAPES + HELPERS + r"""
function lemniPos(omega, a, b){
    var s=Math.sin(omega), c=Math.cos(omega);
    var den=1.0+s*s;
    return {x:a*c/den, z:b*s*c/den};
}
function lemniDeriv(omega, a, b, eps){
    var s=Math.sin(omega), c=Math.cos(omega);
    var den=1.0+s*s, den2=den*den;
    var dx=-a*eps*s*(2.0+c*c)/den2;
    var numer=b*(Math.cos(2.0*omega)*den-(s*c)*(2.0*s*c));
    var dz=eps*numer/den2;
    return {dx:dx, dz:dz};
}
class myapp extends DEECapp{
    counter=0;
    wheelMode=0;
    initialize(){
        var fragsrc=document.getElementById("my-fragment-shader").text;
        var vertsrc=document.getElementById("my-vertex-shader").text;
        this.shaderprog=new DEECshader(this.gl);
        this.shaderprog.srcShaders(vertsrc,fragsrc);
        this.gl.enable(this.gl.DEPTH_TEST);
        this.gl.clearColor(0.7,0.85,0.95,1.0);
        this.cube=new Cube(this.gl,[0.55,0.32,0.12],[0.25,0.12,0.05]);
        this.cone=new Cone(this.gl,[0.7,0.35,0.1],[0.3,0.15,0.05],12);
        this.cyl=new Cylinder(this.gl,[0.4,0.4,0.4],[0.15,0.15,0.15],12);
        this.sph=new Sphere(this.gl,[0.3,0.3,0.35],[0.1,0.1,0.12],12,12);
        this.dark=new Cube(this.gl,[0.1,0.1,0.1],[0.05,0.05,0.05]);
        var all=[this.cube,this.cone,this.cyl,this.sph,this.dark];
        for(var i=0;i<all.length;i++) all[i].setShader(this.shaderprog);
        this.a=0.55; this.b=0.35; this.eps=0.4;
        this.theta=[0,-0.6,-1.2,-1.8];
        this.start=Date.now();
        window.addEventListener("keydown",(e)=>{
            if(e.key.toLowerCase()==='r'){ this.wheelMode=(this.wheelMode+1)%3; console.log('wheels',this.wheelMode); }
        },false);
        console.log('A2/A3 convoy ready');
    }
    draw(obj,M){
        obj.setModelTransformation(M);
        obj.drawit(); // NDC / Objects style
    }
    render(){
        this.gl.clear(this.gl.COLOR_BUFFER_BIT|this.gl.DEPTH_BUFFER_BIT);
        var t=(Date.now()-this.start)*0.001;
        for(var i=0;i<4;i++){
            var w=this.eps*t+this.theta[i];
            var p=lemniPos(w,this.a,this.b);
            var d=lemniDeriv(w,this.a,this.b,this.eps);
            var yaw=Math.atan2(d.dx,d.dz)*180.0/Math.PI;
            var world=mul(T(p.x, 0.0, p.z*0.01), R(yaw,0,1,0)); // flatten z a bit for 2.5D view
            // better: show path in x-y plane for simple view
            world=mul(T(p.x, p.z, 0.0), R(this.counter*0.2 + i*10, 0.2,1,0.1));
            var body = (i===0) ? Su(0.08) : Su(0.06 + 0.01*i);
            this.draw(this.cube, mul(world, body));
            if(i===0) this.draw(this.cone, mul(world, T(0.12,0,0), R(90,0,0,1), Su(0.05)));
            var offs=[[-0.05,-0.05],[0.05,-0.05],[-0.05,0.05],[0.05,0.05]];
            for(var k=0;k<4;k++){
                var o=offs[k];
                var Wm=mul(world, T(o[0], o[1], 0.0), Su(0.025));
                if(this.wheelMode===0) this.draw(this.dark, Wm);
                else if(this.wheelMode===1) this.draw(this.cyl, Wm);
                else this.draw(this.sph, Wm);
            }
        }
        this.counter++;
    }
}
var app=new myapp('myCanvasA23');
app.run();
"""

# Full scene: keep 3D camera but boot-wrapped; fix scale to Su / helpers
# Patch scene: remove trailing app.run and wrap; replace glm.scale with safe helper
SCENE_FIXED = SCENE.replace(
    'var app = new myapp("myCanvas");\napp.run();',
    'var app = new myapp("myCanvasFull");\napp.run();',
).replace(
    'var app = new myapp("myCanvas");\r\napp.run();',
    'var app = new myapp("myCanvasFull");\napp.run();',
)

# scene_app uses S() with glm.scale — patch S to professor style + non-uniform via mat3 trick
SCENE_PREFIX = HELPERS + r"""
// override S used in scene_app.js — non-uniform scale without glm.scale
function S(sx, sy, sz){
  if (typeof sy === 'undefined'){ sy = sx; sz = sx; }
  if (sx === sy && sy === sz) return glm.mat4(glm.mat3(sx));
  // build from uniform + extra: use glm.scale if present, else uniform approx
  if (typeof glm.scale === 'function'){
    try { return glm.scale(glm.mat4(1.0), glm.vec3(sx,sy,sz)); }
    catch(e){}
  }
  return glm.mat4(glm.mat3((sx+sy+sz)/3.0));
}
"""

FULL_INNER = SHAPES + "\n" + SCENE_PREFIX + "\n" + SCENE_FIXED


def build_all():
    save_nb(
        "ExA1_Shapes.ipynb",
        [
            md_cell(
                """# CGRA A1 — Exercise A.1 (Shapes)

Based on professor **Objects.ipynb**.

**Voilà** only (do not press Run). If you see red error text above the canvas, open F12 console.

You should see **5 rotating shapes**: Cube, Sphere, Cylinder, Cone, Disc.
"""
            ),
            code_cell(one_cell_app("myCanvasA1", EXA1_INNER, 700, 420)),
        ],
    )

    save_nb(
        "ExA2A3_Convoy_Path.ipynb",
        [
            md_cell(
                """# CGRA A1 — A.2 + A.3 (Convoy + Lemniscate)

Press **r** after clicking the canvas: wheels cube → cylinder → sphere.

**Voilà** only.
"""
            ),
            code_cell(one_cell_app("myCanvasA23", EXA23_INNER, 700, 500)),
        ],
    )

    save_nb(
        "CGRA_A1_FULL_SUBMISSION.ipynb",
        [
            md_cell(
                """# CGRA A1 — Full submission (Medieval siege)

**Voilà** only. Click canvas, then keys:
- **r** wheels | **wasd** walk | **qe** turn | **v** ride camera

---

# Report

## Shapes (A.1)
Cube 36 verts; Sphere/Cylinder/Cone/Disc with N>=10; two-color X gradient.

## Convoy (A.2)
Ram + 3 wagons; key `r` cycles wheel geometry.

## Path (A.3)
Lemniscate: `x=a cos w/(1+sin^2 w)`, `z=b sin w cos w/(1+sin^2 w)`, `w=eps t + theta_i`.
Yaw from tangent `atan2(dx,dz)`.

## Scene (A.4–A.5)
Torches, trees, trebuchet pendulum, mill, castle walls/gate/windows/crates.

## Camera (A.6–A.7)
WASD walk; `v` toggles ride-along on last wagon.
"""
            ),
            code_cell(one_cell_app("myCanvasFull", FULL_INNER, 800, 560)),
        ],
    )

    save_nb(
        "ExA6A7_Camera_Notes.ipynb",
        [
            md_cell(
                """# Camera notes (A.6 / A.7)

Code lives in `CGRA_A1_FULL_SUBMISSION.ipynb`.

- WASD moves `eye` along forward/right from `yaw`
- `v` switches to lookAt from last wagon
"""
            )
        ],
    )

    # short fix note for user
    (ROOT / "02_FIX_BLANK_CANVAS.txt").write_text(
        """BLANK CANVAS FIX
================
Problem: Voilà showed empty white canvas.
Cause: JS classes ran BEFORE deecapp/cgraobject/glm finished loading.

Fix in new notebooks:
1) libraries + shaders + app in ONE cell
2) cgraBoot() waits until glm + CGRAobject exist
3) A.1 draws like professor Objects (drawit without camera)

RE-UPLOAD these files to seeds Jupyter:
  notebooks/ExA1_Shapes.ipynb
  notebooks/ExA2A3_Convoy_Path.ipynb
  notebooks/CGRA_A1_FULL_SUBMISSION.ipynb

Then Voilà again (hard refresh Ctrl+F5).
""",
        encoding="utf-8",
    )
    print("DONE")


if __name__ == "__main__":
    build_all()
