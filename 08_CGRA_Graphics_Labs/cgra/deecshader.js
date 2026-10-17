class DEECshader {
    gl;
    vertexshader;
    fragmentshader;
    shaderProgram;
    constructor(gl){this.gl=gl;};
    
    filetobuf(file){
        
    };
    loadShaders(vertex_file_path,fragment_file_path){
        
    };
    srcShaders(vertex_src,fragment_src){
        
        var vertexShader = this.gl.createShader(this.gl.VERTEX_SHADER);
        this.gl.shaderSource(vertexShader,vertex_src);
        this.gl.compileShader(vertexShader);
  
        if (!this.gl.getShaderParameter(vertexShader, this.gl.COMPILE_STATUS)) {
          alert('Error compiling vertex shader!' + this.gl.getShaderInfoLog(vertexShader));
	console.log("VERTEX SHADER "+ vertex_src);
          return null;
        }
  
        // now compile the fragment shader
        var fragmentShader = this.gl.createShader(this.gl.FRAGMENT_SHADER);
        this.gl.shaderSource(fragmentShader,fragment_src);
	//console.log('SRC:'+fragment_src);
        this.gl.compileShader(fragmentShader);
  
        if (!this.gl.getShaderParameter(fragmentShader, this.gl.COMPILE_STATUS)) {
            alert('Error compiling fragment shader!'+ this.gl.getShaderInfoLog(fragmentShader));
	    
          return null;
        }

        // OK, we have a pair of shaders, we need to put them together
        // into a "shader program" object
        this.shaderProgram = this.gl.createProgram();
        this.gl.attachShader(this.shaderProgram, vertexShader);
        this.gl.attachShader(this.shaderProgram, fragmentShader);
        this.gl.linkProgram(this.shaderProgram);
        this.gl.validateProgram(this.shaderProgram);
        if (!this.gl.getProgramParameter(this.shaderProgram,this.gl.LINK_STATUS)){
            var msg='ERROR linking program!' + this.gl.getProgramInfoLog(this.shaderProgram);
	    alert(msg);
	    console.log("Error: " + msg);
        }
        this.gl.validateProgram(this.shaderProgram);
        if (!this.gl.getProgramParameter(this.shaderProgram,this.gl.VALIDATE_STATUS)){
            alert('ERROR validating program!' + this.gl.getProgramInfoLog(this.shaderProgram));
		console.log("Error Validating Program Shader");
        }
    }
    linkShaderProgram() {};
    cleanup(){};
    startUsing(){
	this.gl.useProgram(this.shaderProgram);
    }
   
    stopUsing(){}

    // the next method can be used to list all the active attributes and uniforms of a shader program
    printattrunif(){
	const numAttribs = this.gl.getProgramParameter(this.shaderProgram, this.gl.ACTIVE_ATTRIBUTES);
	console.log("There are ", numAttribs," attributes listed bellow");
	for (let ii = 0; ii < numAttribs; ++ii) {
	    const attribInfo = this.gl.getActiveAttrib(this.shaderProgram, ii);
	    const index = this.gl.getAttribLocation(this.shaderProgram, attribInfo.name);
	    console.log(attribInfo.name);
	}
	const numUnifs = this.gl.getProgramParameter(this.shaderProgram, this.gl.ACTIVE_UNIFORMS);
	console.log("There are ", numUnifs," uniforms listed bellow");
	for (let ii = 0; ii < numUnifs; ++ii) {
	    const uniformInfo = this.gl.getActiveUniform(this.shaderProgram, ii);
	    const index = this.gl.getUniformLocation(this.shaderProgram, uniformInfo.name);
	    console.log(uniformInfo.name);
	}
	console.log("----- end ---");
    }
}
