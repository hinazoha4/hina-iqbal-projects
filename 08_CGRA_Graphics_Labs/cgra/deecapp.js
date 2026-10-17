const script = document.createElement("script");
script.src = "https://is3l.isr.uc.pt/~pm/CGRA/JS/QR/qrcode.js";
document.head.appendChild(script);

class DEECapp {
    gl;
    canvas;
    shaderprog;
    ang = 0;
    previous_time = 0;
    frame_rate = 50;

    constructor(canvasname) {
        this.canvas = document.getElementById(canvasname);
        //this.gl = this.canvas.getContext('webgl2');

        //if (!this.gl){
        //    this.webgl_version = 2;
        //} else {
        this.gl = this.canvas.getContext('webgl') || this.canvas.getContext('webgl-experimental');
        if (!this.gl) {
            document.write('<p>This browser does not support webgl. Big trouble!</p>');
            this.webgl_version = 0;
        }
        else {
            this.webgl_version = 1;
        }
        //
        this.glversion = this.gl.getParameter(this.gl.VERSION);
        console.log(this.glversion);
        this.animate_active = false;
    };

    initialize() {
        // prepare the shaders to be used
        var fragsrc = document.getElementById("my-fragment-shader").text;
        var vertsrc = document.getElementById("my-vertex-shader").text;
        if (!fragsrc)
            console.log('Error: you forgot to define my-fragment-shader');
        if (!vertsrc)
            console.log('Error: you forgot to define my-vertex-shader');

        this.shaderprog = new DEECshader(this.gl);
        this.shaderprog.srcShaders(vertsrc, fragsrc);

        // perform the initializations
        this.gl.enable(this.gl.DEPTH_TEST);
        this.gl.clearColor(0.1, 0.1, 0.1, 1);
    };

    prerender(){
           this.gl.clear(this.gl.COLOR_BUFFER_BIT | this.gl.DEPTH_BUFFER_BIT);
    }
    render() { // this method is to be called repeatedly 
     
    };

    animate() {

        var now, elapsed_time;

        if (this.animate_active) {

            // How much time has elapsed since the last frame rendering?
            now = Date.now();
            elapsed_time = now - this.previous_time;

            if (elapsed_time >= this.frame_rate) {

                this.prerender();
                // Render the scene.
                this.render();

                // Remember when this scene was rendered.
                this.previous_time = now;
            }

            requestAnimationFrame(() => this.animate());
        }
    };

    run() {
        this.animate_active = true;
        this.initialize();
        requestAnimationFrame(() => this.animate());
    }
};




class DEECappXR {
      gl;
    canvas;
    shaderprog;
    ang = 0;
    previous_time = 0;
    frame_rate = 0;

    xrSession = null;
    inlineSession = null;
    xrRefSpace = null;
    session = null;
    xrInlineRefSpace = null;
    xrImmersiveRefSpace = null;

    viewM = null;
    projM = null; 
    
    allowMouseRotation = true;
     allowKeyboardMotion = true;
     MOUSE_SPEED = 0.003;
     MOVE_DISTANCE = 0.20;

    xoffset = 0.0;
    yoffset = 0.0;
    zoffset = 0.0; 
    
    constructor(canvasname) {
        this.canvasname=canvasname;
        this.canvas = document.getElementById(canvasname);
        this.gl = null;
        this.xrSession = null;
        this.xrRefSpace = null;

        this.isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
        this.initButtons();  
    }

    
    async initXR() {
        // Is WebXR available on this UA?

        if (navigator.xr) {
            console.log("dentro do xr");
            // If the device allows creation of exclusive sessions set it as the
            // target of the 'Enter XR' button.
            navigator.xr.isSessionSupported('immersive-vr').then((supported) => {
                if (supported) {
    //                console.log("dentro do supported vr");
                    // Updates the button to start an XR session when clicked.
                    //this.xrButton.addEventListener('click', this.onButtonClick("xr-button"));
                    //this.xrButton.addEventListener('click', () => this.onButtonClick("xr-button"));
                    // this.xrButton.addEventListener('click', () => this.onXR_ButtonClicked);
                    this.xrButton.textContent = 'Enter VR';
                    this.xrButton.disabled = false;

                }
            });

            navigator.xr.isSessionSupported('immersive-ar').then((arsupported) => {
                if (arsupported) {
                    console.log("dentro do supported ar");



                    // Updates the button to start an XR session when clicked.
                    //this.arButton.addEventListener('click', this.onButtonClick("ar-button"));
                    this.arButton.addEventListener('click', () => this.onButtonClick("ar-button"));
                    this.arButton.textContent = 'Enter AR';
                    this.arButton.disabled = false;
                }
            });
             this.gl = this.canvas.getContext('webgl', {
            xrCompatible: true,
            alpha: false
        });
            // inline
                 
        try {
            const session = await navigator.xr.requestSession('inline');
            this.inlineSession = session;
            this.onSessionStarted(session);
            session.inInline = true;
        } catch (e) {
            console.warn("Não foi possível iniciar sessão  inline → fallback .", e);
            return this.initFallback();
            return false;
        }

        } else {
            return this.initFallback();  
            return false;
        }

//        console.log("gl", this.gl);

    }

    async initXRnew() {
        // 1) Safari não suporta WebXR → fallback imediato
        if (this.isSafari) {
            console.warn("Safari detectado → WebXR VR não disponível.");
           // return this.initFallback();
           return false;
        }

        // 2) Verificação de suporte WebXR no browser
        if (!navigator.xr) {
            console.warn("WebXR não suportado neste browser.");
            //this.initFallback();
            return false;
        }
        
     
        // 3) Verificar se VR é suportado
        const vrsupported = await navigator.xr.isSessionSupported("immersive-vr")
            .catch(() => false);

        if (vrsupported){
            this.xrButton.textContent = 'Enter VR';
            this.xrButton.disabled = false;
        }else{
            console.log("VR não suportado no dispositivo.");
        } 

        const arsupported = await navigator.xr.isSessionSupported("immersive-ar")
            .catch(() => false);

        if (arsupported){
            this.arButton.textContent = 'Enter AR';
            this.arButton.disabled = false;
        }else{
            console.log("AR não suportado no dispositivo.");
            //return this.initFallback();
        } 

        console.log("create gl context ");

        // 4) Criar WebGL compatível com XR
        this.gl = this.canvas.getContext("webgl", { 
            xrCompatible: true,
            alpha: true 
        });

        if (!this.gl) {
            console.error("Falha ao criar contexto WebGL → fallback 2D.");
           //return this.initFallback(); 
           return false;
        }
        console.log("WebXR inicializado com WebGL compatível.");

        try {
            const session = await navigator.xr.requestSession('inline');
            this.inlineSession = session;
            this.onSessionStarted(session);
            session.inInline = true;
        } catch (e) {
            console.warn("Não foi possível iniciar sessão  inline → fallback .", e);
            //return this.initFallback();
            return false;
        }
        
        console.log("init completed.");
        return true;
    }

     onXR_ButtonClicked() {
        console.log("onXR_Button")
        if (!this.xrSession.isImmersive) {
            console.log("start XR");
            navigator.xr.requestSession('immersive-vr').then((session) => {
                this.xrSession = session;
                this.xrSession.isImmersive = true;
                this.xrButton.textContent = 'Exit VR';

                this.onSessionStarted(this.xrSession);
                this.isAR=false;
            });
        } else {
            console.log("stop XR");
            this.xrSession.isImmersive = false;
            this.xrButton.textContent = 'Enter VR';
            this.xrSession.end();
        }
    }
    onAR_ButtonClicked() {
        if (!this.xrSession.isImmersive) {
            navigator.xr.requestSession('immersive-ar').then((session) => {
                this.xrSession = session;
                session.isImmersive = true;
           this.arButton.textContent = 'Exit AR';

            this.onSessionStarted(session);
            this.isAR=true;

            });
        } else {
                console.log("stop AR");
            this.xrSession.isImmersive = false;
            this.arButton.textContent = 'Enter AR';
            this.xrSession.end();
        }
    }

    // Called when we've successfully acquired a XRSession. In response we
    // will set up the necessary session state and kick off the frame loop.
    onSessionStarted(session) {
      //  console.log("gl", this.gl);
        if (session.isImmersive) {
            console.log("Starting Immersive");
        } else {
            console.log("starting Non Immersive");
        }
        this.xrSession = session;

        // Listen for the sessions 'end' event so we can respond if the user
        // or UA ends the session for any reason.
        session.addEventListener('end', this.onSessionEnded);

        // Use the new WebGL context to create a XRWebGLLayer and set it as the
        // sessions baseLayer. This allows any content rendered to the layer to
        // be displayed on the XRDevice.
        session.updateRenderState({ baseLayer: new XRWebGLLayer(session, this.gl) });

        // Get a reference space, which is required for querying poses. In this
        // case an 'local' reference space means that all poses will be relative
        // to the location where the XRDevice was first detected.
        let refSpaceType = session.isImmersive ? 'local' : 'viewer';
        session.requestReferenceSpace(refSpaceType).then((refSpace) => {
            this.xrRefSpace = refSpace;
            if (session.isImmersive) {
                this.xrImmersiveRefSpace = refSpace;
            } else {
                this.xrInlineRefSpace = refSpace;
            }
     document.addEventListener("keydown", this.handleKeyDown.bind(this));
            // Inform the session that we're ready to begin drawing.
            //session.requestAnimationFrame(this.onXRFrame);
            session.requestAnimationFrame(this.onXRFrame.bind(this));
        });

        // init(gl);
    }

    // Called either when the user has explicitly ended the session by calling
    // session.end() or when the UA has ended the session for any reason.
    // At this point the session object is no longer usable and should be
    // discarded.
    onSessionEnded(event) {
        if (event.session.isImmersive) {
            console.log("End Immersive");
            //this.xrSession.isImmersive = false;
            // this.xrButton.textContent = 'Enter VR';
        } else {
            console.log("End Not Immersive");
        }
    }


    onXRFrame(time, frame) {
        const session = frame.session;

          let refSpace = session.isImmersive ?
            this.xrImmersiveRefSpace :
            this.xrInlineRefSpace;

        // Inform the session that we're ready for the next frame.
        //session.requestAnimationFrame(this.onXRFrame);
        session.requestAnimationFrame(this.onXRFrame.bind(this));

        // Account for the click-and-drag mouse movement or touch movement when
        // calculating the viewer pose for inline sessions.
        // (!session.isImmersive) {
           // console.log("refspace=",this.xrRefSpace);
        let     adjustedrefSpace = this.getAdjustedRefSpace(refSpace);
        //

        let pose = frame.getViewerPose(adjustedrefSpace);

        if (!pose) return;

     
   const layer = session.renderState.baseLayer;

        this.gl.bindFramebuffer(this.gl.FRAMEBUFFER, layer.framebuffer);

                 // Update the clear color so that we can observe the color in the
            // headset changing over time.
            if (!session.isImmersive) {
                this.gl.clearColor(Math.cos(time / 2000),
                    Math.cos(time / 4000),
                    Math.cos(time / 6000), 1.0);
            } else {
                if (this.isAR)
                    this.gl.clearColor(0, 0, 0, 0.0);
                else 
                     this.gl.clearColor(0.1, 0.1, 0.1, 1);

            }

            // do whatever is needed before rendering the scene into the necessary views
            this.prerender();

   
             // Normally you'd loop through each of the views reported by the frame
            // and draw them into the corresponding viewport here, but we're
            // keeping this sample slim so we're not bothering to draw any
            // geometry.

            let ptrans = glm.mat4(pose.transform.matrix);
            //mulfield.innerText = "Pose=" + ptrans.toString() + "\n";
            for (let view of pose.views) {
                
                let viewport = layer.getViewport(view);
                this.gl.viewport(viewport.x, viewport.y,
                    viewport.width, viewport.height);

                // Draw a scene using view.projectionMatrix as the projection matrix
                // and view.transform to position the virtual camera. If you need a
                // view matrix, use view.transform.inverse.matrix.

                this.projM = glm.mat4(view.projectionMatrix);
                this.viewM = glm.mat4(view.transform.inverse.matrix);

                // Maybe we should pass an argument to render to say if we should clear the framebuffer or not.
                // or add a prerender method that may access the left eye pose and use it to generate anything that could be 
                // related with the view... such as pre computing textures or even shadows.
                this.render();
            }
    }

       
 handleKeyDown(event) {
  switch (event.key) {
    // Forward
    case "w":
    case "W":
      this.zoffset += this.MOVE_DISTANCE;
         
      break;
    // Backward
    case "s":
    case "S":
      this.zoffset -= this.MOVE_DISTANCE;
      break;
    // Left
    case "a":
    case "A":
      this.xoffset += this.MOVE_DISTANCE;
      break;
    // Right
    case "d":
    case "D":
      this.xoffset -= this.MOVE_DISTANCE;
      break;
    case "ArrowUp":
      this.yoffset -= this.MOVE_DISTANCE;
      break;
    case "ArrowDown":
      this.yoffset += this.MOVE_DISTANCE;
      break;
    // Reset
    case "r":
    case "R":
      this.xoffset = this.yoffset = this.zoffset = 0;
          
      //mouseYaw = mousePitch = 0;
      break;
    default:
      break;
  }
 }
    
    initButtons(){
        console.log("initButtons()");
        this.xrButton = document.createElement('button');
        this.xrButton.id = this.canvasname + "-xr-button";
        this.xrButton.textContent = "VR not found";
        this.xrButton.className = 'barebones-button';
        this.xrButton.disabled = true;
        this.xrButton.addEventListener('click', () => this.onXR_ButtonClicked());

        this.arButton = document.createElement('button');
        this.arButton.id = this.canvasname + "-ar-button";
        this.arButton.textContent = "AR not found";
        this.arButton.className = 'barebones-button';
        this.arButton.disabled = true;
        this.arButton.addEventListener('click', () => this.onAR_ButtonClicked());

        this.br = document.createElement("br");


        this.canvas.insertAdjacentElement("afterend", this.arButton);
        this.canvas.insertAdjacentElement("afterend", this.xrButton);
        this.canvas.insertAdjacentElement("afterend", this.br);

        if (window.QRCode){
         this.qrdiv=document.createElement('div');
         this.arButton.insertAdjacentElement("afterend",this.qrdiv)
         this.qr=new QRCode(this.qrdiv, window.location.href);
       } else {
           console.warn("QRCode library not loaded — QR code skipped.");
       }
    }
    getAdjustedRefSpaceN(refSpace) {
        // Represent the rotational component of the reference space as a
        // quaternion.
        let invOrientation = quat.create();
        quat.rotateX(invOrientation, invOrientation, -lookPitch);
        quat.rotateY(invOrientation, invOrientation, -lookYaw);
        let xform = new XRRigidTransform(
            { x: 0, y: 0, z: 0 },
            { x: invOrientation[0], y: invOrientation[1], z: invOrientation[2], w: invOrientation[3] });
        return refSpace.getOffsetReferenceSpace(xform);
    }
    getAdjustedRefSpaceOLD(refSpace) {
        return refSpace;
    }

  getAdjustedRefSpace(refSpace) {
        //let invOrientation = quat.create();
        //quat.rotateX(invOrientation, invOrientation, -lookPitch);
        //quat.rotateY(invOrientation, invOrientation, -lookYaw);
        let xform = new XRRigidTransform(
            { x: this.xoffset, y: this.yoffset, z: this.zoffset },
            { x: 0, y:0, z:0, w: 1 });
        return refSpace.getOffsetReferenceSpace(xform);
    }

    initFallback() {
        // A tua inicialização WebGL 2D normal
       
        this.gl = this.canvas.getContext('webgl') || this.canvas.getContext('webgl-experimental');
        if (!this.gl) {
            document.write('<p>This browser does not support webgl. Big trouble!</p>');
            this.webgl_version = 0;
        }
        else {
            this.webgl_version = 1;
        }
        //
        this.glversion = this.gl.getParameter(this.gl.VERSION);
        console.log(this.glversion);
       // this.animate_active = true;
       this.needFallback=true; 
        return true;
    }


    drawFallback() {
         //console.log("drawFallback")

        //if (!this.gl) return;
 
        var now, elapsed_time;

        if (this.animate_active) {

            // How much time has elapsed since the last frame rendering?
            now = Date.now();
            elapsed_time = now - this.previous_time;

            if (elapsed_time >= this.frame_rate) {

                this.prerender();
                // Render the scene.
                this.render();

                // Remember when this scene was rendered.
                this.previous_time = now;
            }
           // console.log("drawFallback 2")
            requestAnimationFrame(() => this.drawFallback());
        }
    }

     initializex() {

        // prepare the shaders to be used
        var fragsrc = document.getElementById("my-fragment-shader").text;
        var vertsrc = document.getElementById("my-vertex-shader").text;
        if (!fragsrc)
            console.log('Error: you forgot to define my-fragment-shader');
        if (!vertsrc)
            console.log('Error: you forgot to define my-vertex-shader');

       // console.log("going to define shaders");
       //console.log("gl", this.gl);
        this.shaderprog = new DEECshader(this.gl);
        this.shaderprog.srcShaders(vertsrc, fragsrc);

        // perform the initializations
        this.gl.enable(this.gl.DEPTH_TEST);
        this.gl.clearColor(0.1, 0.1, 0.1, 1);

        console.log("all good here on init");

    }
    
    prerender(){
        this.gl.clear(this.gl.COLOR_BUFFER_BIT | this.gl.DEPTH_BUFFER_BIT);
    }

    render() {
        
    }
    run() {
        this.initXRnew().then((success) => {
            this.initialize();
        }).catch(()=>{
            this.initFallback();
            this.initialize();
            this.animate_active=true;
            this.drawFallback();
            console.log("FALL");
    });
}

}
