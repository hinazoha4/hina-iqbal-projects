class CGRAobject{
    vertexbuffer = -1;
    colorbuffer;
    shaderprog = -1;
    gl;
    objname = "NoName"
     constructor(glcontext){
         this.gl = glcontext;
         this.projMat = glm.mat4(1.0); // identity transformation by default
         this.viewMat = glm.mat4(1.0); // identity transformation by default
         this.modelMat = glm.mat4(1.0); // identity transformation by default
	
     }
    
    setShader(shader){
        this.shaderprog = shader;
    }
    
    setModelTransformation(modelmat4){
        this.modelMat = modelmat4;
    }

	clone(){
	let deepClone = JSON.parse(JSON.stringify(this));
	//	var acopy = new CGRAobject(this.glcontext);
	//	acopy.objname = "copy of "  + this.objname;
	//	acopy.vertexbuffer = this.vertexbuffer;
	//	acopy.colorbuffer = this.colorbuffer;
	//	acopy.shaderprog=this.shaderprog;
	//	acopy.modelMat= this.modelMat;
	//	return acopy;
	return deepClone;
	}
    
    drawit(viewMat4 = glm.mat4(1.0), projectionMat4 = glm.mat4(1.0), parentMat4 = glm.mat4(1.0)){

        if (this.shaderprog == -1){
             alert('No shader assigned to object ' + this.objname+ '. It will not be drawn!');
            throw new Error("No shader!")
        }
        if (this.vertexbuffer == -1){
             alert('No VBO assigned to object ' + this.name + '. It will not be drawn!');
             throw new Error("No VBO!")
        }
        this.viewMat = viewMat4;
//console.log("view="+this.viewMat);
	this.projMat = projectionMat4;
//console.log("projection="+this.projMat);
        this.shaderprog.startUsing();
        var mvploc = this.gl.getUniformLocation(this.shaderprog.shaderProgram,"MVP");
        var localT = parentMat4['*'](this.modelMat); 
	
        var MVP = this.projMat['*'](this.viewMat['*'](localT));
        this.gl.uniformMatrix4fv(mvploc,false, MVP.array);
        
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.vertexbuffer);
       
        this.positionLocation = this.gl.getAttribLocation(this.shaderprog.shaderProgram,
                                                          "in_Position");
        this.gl.vertexAttribPointer(this.positionLocation, // Attribute location
                           3, // number of elements per attribute
                           this.gl.FLOAT,  // Type of elements
                           this.gl.FALSE,  // 
                           3*Float32Array.BYTES_PER_ELEMENT, // size of a vertex in bytes 
                           0); // Offset from the begining of a single vertex to this attribute

        this.gl.enableVertexAttribArray(this.positionLocation);

        this.gl.bindBuffer(this.gl.ARRAY_BUFFER,this.colorbuffer);
        this.colorLocation = this.gl.getAttribLocation(this.shaderprog.shaderProgram,
                                                          "in_Color");
        if (this.colorLocation != -1){
	    this.gl.vertexAttribPointer(this.colorLocation, // Attribute location
				       3, // number of elements per attribute
				       this.gl.FLOAT,  // Type of elements
				       this.gl.FALSE,  // 
				       3*Float32Array.BYTES_PER_ELEMENT, // size of a vertex in bytes 
				       0); // Offset from the begining of a single vertex to this attribute

            this.gl.enableVertexAttribArray(this.colorLocation);
	}
        this.gl.drawArrays(this.gl.TRIANGLES,0,this.numvertices);
        this.shaderprog.stopUsing();
        
    }
};

