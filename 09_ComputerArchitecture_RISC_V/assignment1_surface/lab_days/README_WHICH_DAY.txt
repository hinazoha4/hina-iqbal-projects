============================================================
  LAB DAYS — ek din = ek file (poori t1a ek saath MAT dikhao)
============================================================

Min/Max SAWAL KA JAWAB:
  HAAN — humne kiya hai.
  init() mein:
    Maxx = Maxy = +pi/2
    Minx = Miny = -pi/2
    pixcorx/pixcory = (Max-Min)/res
  Aur .data mein bhi ab proper ±pi/2 values hain
  (pehle skeleton ke 1.5/-1.5 the — unhe replace kar diya).

------------------------------------------------------------
AJ (lab mein abhi) PROF KO DIKHAO:
  lab_days\day1_putpixel.asm
  -> Assemble -> Bitmap Connect -> Go -> RED screen
  Bolo: "Aaj putpixel complete; kal init + Min/Max."

AGAR PROF Min/Max POOCHAY AAJ HI:
  lab_days\day2_init_minmax.asm
  Bolo:
    "init mein Minx/Miny = -pi/2, Maxx/Maxy = +pi/2
     assign ho rahe hain, phir pixcor calculate."

AGLAY DIN:
  day3_sin_approx.asm   -> Run I/O mein numbers
  day4_cos_approx.asm
  FINAL: ..\t1a.asm     -> poori surface image

------------------------------------------------------------
PROF KE SAAMNE SHORT SCRIPT (Day 2):
  "Skeleton mein Min/Max pehle galat/placeholder the.
   PDF Algorithm 5 ke mutabiq init mein ±pi/2 set karta hun,
   aur pixcorx = (Maxx-Minx)/cols."

FOLDER:
  assignment1_surface\lab_days\
============================================================
