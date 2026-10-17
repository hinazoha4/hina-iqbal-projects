cgra2526-4.pdf SOLUTIONS
========================
PDF page 3-4 says:
  "Start with the example Transformations"
  Use GLM 4D, then convert to 2D vertex arrays to draw.

Files:
  PDF4_Ex4_1.ipynb  - small blue triangle on sinusoid L->R wrap
  PDF4_Ex4_2.ipynb  - same + rotate
  PDF4_Ex4_3.ipynb  - rotating rectangle under triangle
  PDF4_Ex4_4.ipynb  - clock with Date()

Upload -> Voila

What to say:
  I started from Transformations example.
  I keep points as glm.vec4, multiply by mat4, then put x,y in vertices[] for drawArrays.
