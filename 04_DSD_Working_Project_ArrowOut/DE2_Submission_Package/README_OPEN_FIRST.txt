DE2 Lab Submission Package (English folder names, portable paths)
================================================================

Location: same parent folder as your original "dsd working project".

1) shared_DE2_reference_design_files
   - de2_library: VHDL / symbols used by both labs (VGA_SYNC, MOUSE, PLL, etc.)
   - DE2_pin_assignments.csv: Terasic DE2 pin reference (import or compare in Pin Planner)

2) 01_DE2_VGA_Mouse_Paint
   - Open in Quartus: de2_vga_mouse_paint.qpf
   - Top-level schematic: de2_vga_mouse_paint.bdf
   - SEARCH_PATH points to ../shared_DE2_reference_design_files/de2_library
   - The .qsf may still list an old Altera install path (e.g. c:\altera\91sp2\...). If Analysis & Synthesis cannot find DE2 megafunctions, remove those SEARCH_PATH lines or point them to your Quartus version's libraries folder under the install directory.

3) 02_DE2_PS2_Keyboard_VGA_Text
   - Open: de2_ps2_keyboard_vga_text.qpf
   - Top-level: de2_ps2_keyboard_vga_text.bdf
   - Same shared DE2 library path as above.

Course integrity: If you used public or third-party examples, cite them in your report per your instructor's rules.

Build artifacts (db, incremental_db, large reports) were omitted to keep zips small — Quartus will regenerate them on compile.
