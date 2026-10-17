// ============================================================
// CGRA A1 — FULL SCENE (basic, for defense)
// Keys:
//   r     = cycle wheels: cube -> cylinder -> sphere
//   w a s d = walk camera
//   v     = toggle ride-along camera on last wagon
// ============================================================

// ---- path: Lemniscate of Bernoulli (from assignment PDF) ----
function lemniPos(omega, a, b) {
    var s = Math.sin(omega);
    var c = Math.cos(omega);
    var den = 1.0 + s * s;
    return {
        x: a * c / den,
        z: b * s * c / den
    };
}

// tangent from analytic derivatives (see report markdown)
function lemniDeriv(omega, a, b, eps) {
    var s = Math.sin(omega);
    var c = Math.cos(omega);
    var den = 1.0 + s * s;
    var den2 = den * den;
    // dx/dt = -a * eps * sin(w) * (2 + cos^2(w)) / (1+sin^2)^2
    var dx = -a * eps * s * (2.0 + c * c) / den2;
    // dy/dt (here z) from quotient rule on y = b*sin*cos/den
    var numer = b * (Math.cos(2.0 * omega) * den - (s * c) * (2.0 * s * c));
    var dz = eps * numer / den2;
    return { dx: dx, dz: dz };
}

function headingFromTangent(dx, dz) {
    // yaw around Y so vehicle faces movement direction
    return Math.atan2(dx, dz);
}

function T(x, y, z) {
    return glm.translate(glm.mat4(1.0), glm.vec3(x, y, z));
}
function R(axisX, axisY, axisZ, deg) {
    return glm.rotate(glm.mat4(1.0), glm.radians(deg), glm.vec3(axisX, axisY, axisZ));
}
function S(sx, sy, sz) {
    // professor style: glm.mat4(glm.mat3(s)) for uniform; glm.scale if available
    if (typeof sy === "undefined") { sy = sx; sz = sx; }
    if (sx === sy && sy === sz) return glm.mat4(glm.mat3(sx));
    if (typeof glm.scale === "function") {
        return glm.scale(glm.mat4(1.0), glm.vec3(sx, sy, sz));
    }
    return glm.mat4(glm.mat3((sx + sy + sz) / 3.0));
}
function mul() {
    // multiply matrices left to right: mul(A,B,C) = A*B*C
    var m = arguments[0];
    for (var i = 1; i < arguments.length; i++) {
        m = m['*'](arguments[i]);
    }
    return m;
}

class myapp extends DEECapp {
    counter = 0;
    wheelMode = 0; // 0 cube, 1 cylinder, 2 sphere
    camMode = 0;   // 0 free walk, 1 ride wagon
    eye = { x: 0, y: 3, z: 14 };
    yaw = 0;       // degrees, look left/right
    keys = {};

    initialize() {
        var fragsrc = document.getElementById("my-fragment-shader").text;
        var vertsrc = document.getElementById("my-vertex-shader").text;
        this.shaderprog = new DEECshader(this.gl);
        this.shaderprog.srcShaders(vertsrc, fragsrc);

        this.gl.enable(this.gl.DEPTH_TEST);
        this.gl.clearColor(0.55, 0.75, 0.95, 1.0); // sky blue

        // shared primitives (two colors = gradient)
        this.cubeWood = new Cube(this.gl, [0.55, 0.32, 0.12], [0.25, 0.12, 0.05]);
        this.cubeStone = new Cube(this.gl, [0.55, 0.55, 0.55], [0.25, 0.25, 0.28]);
        this.cubeDark = new Cube(this.gl, [0.15, 0.12, 0.1], [0.05, 0.05, 0.05]);
        this.cubeGreen = new Cube(this.gl, [0.2, 0.55, 0.15], [0.1, 0.3, 0.08]);
        this.cyl = new Cylinder(this.gl, [0.4, 0.4, 0.4], [0.15, 0.15, 0.15], 12);
        this.cone = new Cone(this.gl, [0.7, 0.35, 0.1], [0.35, 0.15, 0.05], 12);
        this.coneLeaf = new Cone(this.gl, [0.15, 0.55, 0.15], [0.05, 0.25, 0.05], 12);
        this.disc = new Disc(this.gl, [0.9, 0.7, 0.2], [0.7, 0.3, 0.05], 12);
        this.sphere = new Sphere(this.gl, [0.3, 0.3, 0.35], [0.1, 0.1, 0.12], 12, 12);
        this.sphereFire = new Sphere(this.gl, [1.0, 0.5, 0.0], [1.0, 0.1, 0.0], 10, 10);

        var objs = [this.cubeWood, this.cubeStone, this.cubeDark, this.cubeGreen,
                    this.cyl, this.cone, this.coneLeaf, this.disc, this.sphere, this.sphereFire];
        for (var i = 0; i < objs.length; i++) {
            objs[i].setShader(this.shaderprog);
        }

        // path params
        this.pathA = 6.0;
        this.pathB = 4.0;
        this.pathEps = 0.35;
        // wagon spacing offsets theta_i
        this.theta = [0.0, -0.55, -1.1, -1.65];

        this.start = Date.now();

        window.addEventListener("keydown", (e) => {
            this.keys[e.key.toLowerCase()] = true;
            if (e.key.toLowerCase() === "r") {
                this.wheelMode = (this.wheelMode + 1) % 3;
                console.log("wheel mode = " + this.wheelMode + " (0=cube,1=cyl,2=sphere)");
            }
            if (e.key.toLowerCase() === "v") {
                this.camMode = 1 - this.camMode;
                console.log("camera mode = " + (this.camMode === 0 ? "walk" : "ride"));
            }
        }, false);
        window.addEventListener("keyup", (e) => {
            this.keys[e.key.toLowerCase()] = false;
        }, false);
    }

    drawObj(obj, M, view, proj) {
        obj.setModelTransformation(M);
        obj.drawit(view, proj);
    }

    // one wheel at local offset
    drawWheel(parentM, lx, ly, lz, view, proj) {
        var local = mul(T(lx, ly, lz), S(0.25, 0.25, 0.12));
        var M = parentM['*'](local);
        if (this.wheelMode === 0) this.drawObj(this.cubeDark, M, view, proj);
        else if (this.wheelMode === 1) this.drawObj(this.cyl, mul(parentM, T(lx, ly, lz), R(0, 0, 1, 90), S(0.25, 0.12, 0.25)), view, proj);
        else this.drawObj(this.sphere, mul(parentM, T(lx, ly, lz), S(0.25, 0.25, 0.25)), view, proj);
    }

    // vehicle i=0 ram, i=1..3 wagons
    drawVehicle(i, worldM, view, proj) {
        if (i === 0) {
            // battering ram body
            this.drawObj(this.cubeWood, mul(worldM, S(0.6, 0.35, 1.2)), view, proj);
            // ram head (cone in front)
            this.drawObj(this.cone, mul(worldM, T(0, 0.1, 1.5), R(1, 0, 0, 90), S(0.25, 0.7, 0.25)), view, proj);
            // roof
            this.drawObj(this.cubeDark, mul(worldM, T(0, 0.55, 0), S(0.65, 0.12, 1.1)), view, proj);
        } else {
            // supply wagon — different sizes
            var sx = 0.45 + 0.08 * i;
            var sy = 0.30 + 0.05 * ((i % 2));
            var sz = 0.7 + 0.1 * i;
            this.drawObj(this.cubeWood, mul(worldM, S(sx, sy, sz)), view, proj);
            // load on top
            if (i === 1) this.drawObj(this.cubeDark, mul(worldM, T(0, sy + 0.2, 0), S(0.25, 0.2, 0.25)), view, proj);
            if (i === 2) this.drawObj(this.cyl, mul(worldM, T(0, sy + 0.25, 0), S(0.2, 0.2, 0.2)), view, proj);
            if (i === 3) this.drawObj(this.sphere, mul(worldM, T(0, sy + 0.25, 0), S(0.22, 0.22, 0.22)), view, proj);
        }
        // 4 wheels
        this.drawWheel(worldM, -0.55, -0.35, 0.7, view, proj);
        this.drawWheel(worldM, 0.55, -0.35, 0.7, view, proj);
        this.drawWheel(worldM, -0.55, -0.35, -0.7, view, proj);
        this.drawWheel(worldM, 0.55, -0.35, -0.7, view, proj);
    }

    drawTree(x, z, view, proj) {
        this.drawObj(this.cyl, mul(T(x, 0.6, z), S(0.12, 0.6, 0.12)), view, proj);
        this.drawObj(this.coneLeaf, mul(T(x, 1.6, z), S(0.55, 0.7, 0.55)), view, proj);
    }

    drawTorch(x, z, view, proj, t) {
        this.drawObj(this.cyl, mul(T(x, 0.5, z), S(0.08, 0.5, 0.08)), view, proj);
        var flicker = 0.15 + 0.05 * Math.sin(t * 8.0 + x);
        this.drawObj(this.sphereFire, mul(T(x, 1.1, z), S(flicker, flicker * 1.3, flicker)), view, proj);
    }

    drawCastle(view, proj) {
        // floor
        this.drawObj(this.cubeStone, mul(T(0, -0.2, -10), S(8, 0.2, 6)), view, proj);
        // back wall
        this.drawObj(this.cubeStone, mul(T(0, 1.5, -15), S(8, 1.5, 0.4)), view, proj);
        // side walls
        this.drawObj(this.cubeStone, mul(T(-7.5, 1.5, -10), S(0.4, 1.5, 5)), view, proj);
        this.drawObj(this.cubeStone, mul(T(7.5, 1.5, -10), S(0.4, 1.5, 5)), view, proj);
        // towers
        this.drawObj(this.cubeStone, mul(T(-6, 2.5, -14.5), S(1.2, 2.5, 1.2)), view, proj);
        this.drawObj(this.cubeStone, mul(T(6, 2.5, -14.5), S(1.2, 2.5, 1.2)), view, proj);
        this.drawObj(this.cone, mul(T(-6, 5.5, -14.5), S(1.4, 1.0, 1.4)), view, proj);
        this.drawObj(this.cone, mul(T(6, 5.5, -14.5), S(1.4, 1.0, 1.4)), view, proj);
        // gate pillars + arch top (portcullis passage)
        this.drawObj(this.cubeStone, mul(T(-1.8, 1.2, -5), S(0.5, 1.2, 0.5)), view, proj);
        this.drawObj(this.cubeStone, mul(T(1.8, 1.2, -5), S(0.5, 1.2, 0.5)), view, proj);
        this.drawObj(this.cubeStone, mul(T(0, 2.6, -5), S(2.4, 0.4, 0.5)), view, proj);
        // portcullis bars (dark cubes)
        for (var i = -2; i <= 2; i++) {
            this.drawObj(this.cubeDark, mul(T(i * 0.5, 1.0, -4.7), S(0.08, 1.0, 0.08)), view, proj);
        }
        // windows on back wall
        this.drawObj(this.cubeDark, mul(T(-3, 2.0, -14.5), S(0.5, 0.6, 0.2)), view, proj);
        this.drawObj(this.cubeDark, mul(T(3, 2.0, -14.5), S(0.5, 0.6, 0.2)), view, proj);
        this.drawObj(this.cubeDark, mul(T(0, 2.2, -14.5), S(0.5, 0.6, 0.2)), view, proj);
    }

    drawProps(view, proj, t) {
        // trees around path
        this.drawTree(-8, 2, view, proj);
        this.drawTree(8, 2, view, proj);
        this.drawTree(-7, -2, view, proj);
        this.drawTree(7, -3, view, proj);
        this.drawTree(-5, 6, view, proj);
        this.drawTree(5, 6, view, proj);

        // torches / braziers
        this.drawTorch(-4, -4, view, proj, t);
        this.drawTorch(4, -4, view, proj, t);
        this.drawTorch(-3, 5, view, proj, t);
        this.drawTorch(3, 5, view, proj, t);

        // crates
        this.drawObj(this.cubeWood, mul(T(-6, 0.25, -6), S(0.35, 0.25, 0.35)), view, proj);
        this.drawObj(this.cubeWood, mul(T(-5.4, 0.25, -6.3), S(0.3, 0.25, 0.3)), view, proj);
        this.drawObj(this.cubeWood, mul(T(6, 0.25, -7), S(0.4, 0.3, 0.4)), view, proj);

        // barricade
        for (var i = 0; i < 5; i++) {
            this.drawObj(this.cubeWood, mul(T(-2 + i * 1.0, 0.35, 7), R(0, 1, 0, 15), S(0.15, 0.35, 0.5)), view, proj);
        }

        // ground grass disc markers near camp
        this.drawObj(this.disc, mul(T(0, -0.05, 0), S(12, 1, 12)), view, proj);
    }

    // animated trebuchet
    drawTrebuchet(view, proj, t) {
        var base = T(-8, 0, -8);
        this.drawObj(this.cubeWood, mul(base, S(0.8, 0.2, 0.4)), view, proj);
        this.drawObj(this.cyl, mul(base, T(0, 1.0, 0), S(0.12, 1.0, 0.12)), view, proj);
        // swinging arm (pendulum)
        var ang = 40 * Math.sin(t * 1.5);
        var arm = mul(base, T(0, 1.8, 0), R(0, 0, 1, ang));
        this.drawObj(this.cubeWood, mul(arm, T(0.9, 0, 0), S(1.0, 0.1, 0.1)), view, proj);
        this.drawObj(this.sphere, mul(arm, T(1.9, 0, 0), S(0.25, 0.25, 0.25)), view, proj);
    }

    // animated mill / well bucket
    drawMill(view, proj, t) {
        var base = T(8, 0, -8);
        this.drawObj(this.cubeStone, mul(base, S(0.6, 0.15, 0.6)), view, proj);
        this.drawObj(this.cyl, mul(base, T(0, 1.0, 0), S(0.5, 1.0, 0.5)), view, proj);
        // rotating wheel
        var spin = t * 80.0;
        var wheel = mul(base, T(0.7, 1.2, 0), R(0, 0, 1, spin), S(0.15, 0.8, 0.8));
        this.drawObj(this.cyl, wheel, view, proj);
        // bucket going up/down
        var by = 0.4 + 0.35 * Math.sin(t * 2.0);
        this.drawObj(this.cubeDark, mul(base, T(0, by, 0), S(0.2, 0.2, 0.2)), view, proj);
    }

    updateWalkCamera() {
        var speed = 0.12;
        var rad = this.yaw * Math.PI / 180.0;
        var fx = Math.sin(rad);
        var fz = -Math.cos(rad);
        var rx = Math.cos(rad);
        var rz = Math.sin(rad);
        if (this.keys["w"]) { this.eye.x += fx * speed; this.eye.z += fz * speed; }
        if (this.keys["s"]) { this.eye.x -= fx * speed; this.eye.z -= fz * speed; }
        if (this.keys["a"]) { this.eye.x -= rx * speed; this.eye.z -= rz * speed; }
        if (this.keys["d"]) { this.eye.x += rx * speed; this.eye.z += rz * speed; }
        // turn with q/e also (extra, easy)
        if (this.keys["q"]) this.yaw -= 1.5;
        if (this.keys["e"]) this.yaw += 1.5;
    }

    render() {
        this.gl.clear(this.gl.COLOR_BUFFER_BIT | this.gl.DEPTH_BUFFER_BIT);
        this.counter++;
        var t = (Date.now() - this.start) * 0.001;

        // projection
        var aspect = this.canvas.width / this.canvas.height;
        var proj = glm.perspective(glm.radians(50.0), aspect, 0.1, 100.0);

        // convoy positions (needed also for ride camera)
        var wagons = [];
        for (var i = 0; i < 4; i++) {
            var omega = this.pathEps * t + this.theta[i];
            var p = lemniPos(omega, this.pathA, this.pathB);
            var d = lemniDeriv(omega, this.pathA, this.pathB, this.pathEps);
            var yaw = headingFromTangent(d.dx, d.dz);
            wagons.push({ x: p.x, z: p.z, yaw: yaw });
        }

        var view;
        if (this.camMode === 0) {
            this.updateWalkCamera();
            var rad = this.yaw * Math.PI / 180.0;
            var cx = this.eye.x + Math.sin(rad);
            var cz = this.eye.z - Math.cos(rad);
            view = glm.lookAt(
                glm.vec3(this.eye.x, this.eye.y, this.eye.z),
                glm.vec3(cx, this.eye.y, cz),
                glm.vec3(0, 1, 0)
            );
        } else {
            // ride on last wagon (i=3), look forward a bit
            var w = wagons[3];
            var fx = Math.sin(w.yaw);
            var fz = Math.cos(w.yaw);
            var ex = w.x - fx * 0.5;
            var ey = 1.2;
            var ez = w.z - fz * 0.5;
            view = glm.lookAt(
                glm.vec3(ex, ey, ez),
                glm.vec3(w.x + fx * 2.0, 1.0, w.z + fz * 2.0),
                glm.vec3(0, 1, 0)
            );
        }

        // scene
        this.drawProps(view, proj, t);
        this.drawCastle(view, proj);
        this.drawTrebuchet(view, proj, t);
        this.drawMill(view, proj, t);

        // convoy
        for (var i = 0; i < 4; i++) {
            var w = wagons[i];
            var world = mul(
                T(w.x, 0.5, w.z),
                R(0, 1, 0, w.yaw * 180.0 / Math.PI)
            );
            this.drawVehicle(i, world, view, proj);
        }
    }
}

var app = new myapp("myCanvasFull");
app.run();
