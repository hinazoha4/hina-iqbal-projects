// ============================================================
// CGRA A1 — BASIC shapes (all extend CGRAobject)
// Keep this simple for oral defense.
// Color: smooth gradient from color1 to color2 along X.
// ============================================================

function mixColor(c1, c2, t) {
    // t from 0 to 1
    return [
        c1[0] * (1 - t) + c2[0] * t,
        c1[1] * (1 - t) + c2[1] * t,
        c1[2] * (1 - t) + c2[2] * t
    ];
}

function pushTri(verts, cols, ax, ay, az, bx, by, bz, cx, cy, cz, c1, c2) {
    // one triangle = 3 vertices
    var pts = [[ax, ay, az], [bx, by, bz], [cx, cy, cz]];
    for (var i = 0; i < 3; i++) {
        verts.push(pts[i][0], pts[i][1], pts[i][2]);
        // gradient by X: -1..1 mapped to 0..1
        var t = (pts[i][0] + 1.0) * 0.5;
        if (t < 0) t = 0;
        if (t > 1) t = 1;
        var col = mixColor(c1, c2, t);
        cols.push(col[0], col[1], col[2]);
    }
}

function uploadBuffers(obj, verts, cols) {
    obj.numvertices = verts.length / 3;
    obj.vertexbuffer = obj.gl.createBuffer();
    obj.gl.bindBuffer(obj.gl.ARRAY_BUFFER, obj.vertexbuffer);
    obj.gl.bufferData(obj.gl.ARRAY_BUFFER, new Float32Array(verts), obj.gl.STATIC_DRAW);

    obj.colorbuffer = obj.gl.createBuffer();
    obj.gl.bindBuffer(obj.gl.ARRAY_BUFFER, obj.colorbuffer);
    obj.gl.bufferData(obj.gl.ARRAY_BUFFER, new Float32Array(cols), obj.gl.STATIC_DRAW);
}

// ---------- CUBE: 6 faces * 2 triangles * 3 verts = 36 ----------
class Cube extends CGRAobject {
    constructor(glcontext, color1, color2) {
        super(glcontext);
        var c1 = color1 || [1, 0, 0];
        var c2 = color2 || [0, 0, 1];
        var verts = [];
        var cols = [];

        // unit cube corners from -1 to 1
        // faces: front, back, left, right, top, bottom
        // each face = 2 triangles
        var f = [
            // front z=+1
            [-1, -1, 1, 1, -1, 1, 1, 1, 1, -1, -1, 1, 1, 1, 1, -1, 1, 1],
            // back z=-1
            [1, -1, -1, -1, -1, -1, -1, 1, -1, 1, -1, -1, -1, 1, -1, 1, 1, -1],
            // left x=-1
            [-1, -1, -1, -1, -1, 1, -1, 1, 1, -1, -1, -1, -1, 1, 1, -1, 1, -1],
            // right x=+1
            [1, -1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1, 1, 1, -1, 1, 1, 1],
            // top y=+1
            [-1, 1, 1, 1, 1, 1, 1, 1, -1, -1, 1, 1, 1, 1, -1, -1, 1, -1],
            // bottom y=-1
            [-1, -1, -1, 1, -1, -1, 1, -1, 1, -1, -1, -1, 1, -1, 1, -1, -1, 1]
        ];

        for (var fi = 0; fi < f.length; fi++) {
            var a = f[fi];
            // two triangles already listed as 6 verts
            pushTri(verts, cols, a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], c1, c2);
            pushTri(verts, cols, a[9], a[10], a[11], a[12], a[13], a[14], a[15], a[16], a[17], c1, c2);
        }
        uploadBuffers(this, verts, cols);
    }
}

// ---------- DISC: center + ring (>=10) ----------
class Disc extends CGRAobject {
    constructor(glcontext, color1, color2, n) {
        super(glcontext);
        var c1 = color1 || [1, 1, 0];
        var c2 = color2 || [1, 0.5, 0];
        n = n || 12; // at least 10
        var verts = [];
        var cols = [];
        var r = 1.0;
        for (var i = 0; i < n; i++) {
            var a0 = (i / n) * 2 * Math.PI;
            var a1 = ((i + 1) / n) * 2 * Math.PI;
            var x0 = r * Math.cos(a0), z0 = r * Math.sin(a0);
            var x1 = r * Math.cos(a1), z1 = r * Math.sin(a1);
            // triangle: center, p0, p1  (in XZ plane, y=0)
            pushTri(verts, cols, 0, 0, 0, x0, 0, z0, x1, 0, z1, c1, c2);
        }
        uploadBuffers(this, verts, cols);
    }
}

// ---------- CONE: apex + base circle (>=10) ----------
class Cone extends CGRAobject {
    constructor(glcontext, color1, color2, n) {
        super(glcontext);
        var c1 = color1 || [0.8, 0.4, 0.1];
        var c2 = color2 || [0.3, 0.15, 0.05];
        n = n || 12;
        var verts = [];
        var cols = [];
        var r = 1.0;
        var apexY = 1.0;
        var baseY = -1.0;
        for (var i = 0; i < n; i++) {
            var a0 = (i / n) * 2 * Math.PI;
            var a1 = ((i + 1) / n) * 2 * Math.PI;
            var x0 = r * Math.cos(a0), z0 = r * Math.sin(a0);
            var x1 = r * Math.cos(a1), z1 = r * Math.sin(a1);
            // side triangle
            pushTri(verts, cols, 0, apexY, 0, x0, baseY, z0, x1, baseY, z1, c1, c2);
            // base triangle (optional close)
            pushTri(verts, cols, 0, baseY, 0, x1, baseY, z1, x0, baseY, z0, c1, c2);
        }
        uploadBuffers(this, verts, cols);
    }
}

// ---------- CYLINDER: two circles (>=10), quads -> 2 tris ----------
class Cylinder extends CGRAobject {
    constructor(glcontext, color1, color2, n) {
        super(glcontext);
        var c1 = color1 || [0.6, 0.6, 0.6];
        var c2 = color2 || [0.2, 0.2, 0.2];
        n = n || 12;
        var verts = [];
        var cols = [];
        var r = 1.0;
        var yTop = 1.0, yBot = -1.0;
        for (var i = 0; i < n; i++) {
            var a0 = (i / n) * 2 * Math.PI;
            var a1 = ((i + 1) / n) * 2 * Math.PI;
            var x0 = r * Math.cos(a0), z0 = r * Math.sin(a0);
            var x1 = r * Math.cos(a1), z1 = r * Math.sin(a1);
            // side: two triangles
            pushTri(verts, cols, x0, yBot, z0, x1, yBot, z1, x1, yTop, z1, c1, c2);
            pushTri(verts, cols, x0, yBot, z0, x1, yTop, z1, x0, yTop, z0, c1, c2);
            // top cap
            pushTri(verts, cols, 0, yTop, 0, x0, yTop, z0, x1, yTop, z1, c1, c2);
            // bottom cap
            pushTri(verts, cols, 0, yBot, 0, x1, yBot, z1, x0, yBot, z0, c1, c2);
        }
        uploadBuffers(this, verts, cols);
    }
}

// ---------- SPHERE: latitude strips (>=10) * rings (>=10) ----------
class Sphere extends CGRAobject {
    constructor(glcontext, color1, color2, stacks, slices) {
        super(glcontext);
        var c1 = color1 || [0.2, 0.6, 1.0];
        var c2 = color2 || [1.0, 0.2, 0.4];
        stacks = stacks || 12; // latitude strips
        slices = slices || 12; // vertices per ring
        var verts = [];
        var cols = [];
        var R = 1.0;

        for (var i = 0; i < stacks; i++) {
            // elevation from -PI/2 to +PI/2
            var lat0 = -Math.PI / 2 + (i / stacks) * Math.PI;
            var lat1 = -Math.PI / 2 + ((i + 1) / stacks) * Math.PI;
            var y0 = R * Math.sin(lat0);
            var y1 = R * Math.sin(lat1);
            var r0 = R * Math.cos(lat0);
            var r1 = R * Math.cos(lat1);

            for (var j = 0; j < slices; j++) {
                var a0 = (j / slices) * 2 * Math.PI;
                var a1 = ((j + 1) / slices) * 2 * Math.PI;

                var x00 = r0 * Math.cos(a0), z00 = r0 * Math.sin(a0);
                var x01 = r0 * Math.cos(a1), z01 = r0 * Math.sin(a1);
                var x10 = r1 * Math.cos(a0), z10 = r1 * Math.sin(a0);
                var x11 = r1 * Math.cos(a1), z11 = r1 * Math.sin(a1);

                // two triangles between rings
                pushTri(verts, cols, x00, y0, z00, x01, y0, z01, x11, y1, z11, c1, c2);
                pushTri(verts, cols, x00, y0, z00, x11, y1, z11, x10, y1, z10, c1, c2);
            }
        }
        uploadBuffers(this, verts, cols);
    }
}
