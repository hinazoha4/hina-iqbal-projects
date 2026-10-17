# DE2 VGA Text and Graphics Editors - Complete Project Report

## 1. Project Overview

This work implements two FPGA applications for the Altera DE2 board (Cyclone II, EP2C35F672C6) using Quartus II 13.0 SP1 and VHDL:

- VGA text editor controlled by a PS/2 keyboard
- VGA graphics editor controlled by a PS/2 mouse

Both projects were prepared as independent Quartus projects so they can be compiled and programmed separately as `.sof` files.

### Objectives

- Reuse stable DE2 peripheral IP (VGA timing, PS/2 keyboard/mouse interfaces)
- Build custom top-level editor logic in VHDL
- Apply DE2-compatible pin assignments through Quartus `.qsf`
- Keep architecture simple enough for undergraduate-level FPGA demonstration

## 2. Platform and Toolchain

- Board: DE2 (Cyclone II EP2C35F672C6)
- Software: Quartus II 13.0 SP1
- Language: VHDL
- Interfaces used:
  - VGA (640x480 timing through existing sync module)
  - PS/2 keyboard for text editor
  - PS/2 mouse for graphic editor
  - Switches and keys for mode/select/reset features
  - LEDs for runtime diagnostics

## 3. Source Organization

The delivered package includes:

- `text_editor_project/`
  - `text_editor_project.qpf`, `text_editor_project.qsf`
  - `src/text_editor_top.vhd` (custom top-level)
  - `src/vga_sync.vhd`, `src/video_PLL.vhd`, `src/KEYBOARD.VHD`, `src/CHAR_ROM.VHD`
  - `text_editor_top.bdf`
  - `constraints/DE2_pin_assignments.csv`
- `graphic_editor_project/`
  - `graphic_editor_project.qpf`, `graphic_editor_project.qsf`
  - `src/graphic_editor_top.vhd` (custom top-level)
  - `src/pixel_canvas.vhd` (custom drawing memory)
  - `src/vga_sync.vhd`, `src/video_PLL.vhd`, `src/MOUSE.VHD`
  - `graphic_editor_top.bdf`
  - `constraints/DE2_pin_assignments.csv`

## 4. Text Editor Design

### 4.1 Functional Behavior

- VGA screen is divided into text-like 8x8 cells
- Keyboard scan codes are captured over PS/2
- Cursor moves with `W`, `A`, `S`, `D`
- Character pattern changes with key input (`char_sel`)
- `SW[0]` enables invert mode
- `SW[2:1]` change display coloration

### 4.2 Architecture

Major blocks:

1. `keyboard` decoder captures scan code events
2. `VGA_SYNC` generates raster timing and pixel coordinates
3. `char_rom` returns per-pixel font bit
4. `text_editor_top` composes glyph, cursor highlight, and color output

### 4.3 I/O Behavior on DE2

- `KEY[0]`: active-low reset
- `PS2_CLK`, `PS2_DAT`: keyboard interface
- `VGA_*`: full VGA output group
- `LEDR`: scan code, status, and cursor diagnostics

## 5. Graphic Editor Design

### 5.1 Functional Behavior

- Screen is divided into coarse drawing cells (80x60 logical grid)
- Mouse position creates a cursor crosshair overlay
- Holding left mouse button writes brush color to canvas memory
- `SW[0]` enables/disables drawing
- `SW[3:1]` select RGB brush color
- `KEY[1]` clears canvas

### 5.2 Architecture

Major blocks:

1. `MOUSE` PS/2 interface provides mouse cursor and button state
2. `pixel_canvas` stores color per cell in FPGA memory array
3. `VGA_SYNC` supplies pixel scan timing
4. `graphic_editor_top` maps pixel to cell, overlays cursor, and drives VGA RGB

### 5.3 Memory and Performance Notes

- Canvas memory depth: `80 x 60 = 4800` cells
- Color depth: 3 bits per cell (R/G/B on-off)
- Clear operation iterates memory sequentially; `busy_clear` protects write behavior

## 6. Pin Assignment Method

- DE2 pin mappings are defined in each project `.qsf`
- Reference CSV (`DE2_pin_assignments.csv`) is included in each project under `constraints/`
- Essential mappings verified for:
  - `CLOCK_50`
  - `KEY[3:0]`, `SW[17:0]`, `LEDR[17:0]`
  - `PS2_CLK`, `PS2_DAT`
  - `VGA_R[9:0]`, `VGA_G[9:0]`, `VGA_B[9:0]`
  - `VGA_HS`, `VGA_VS`, `VGA_CLK`, `VGA_BLANK`, `VGA_SYNC`

## 7. Quartus Build and Programming Procedure

### 7.1 Compile

For each project:

1. Open Quartus II 13.0 SP1
2. `File -> Open Project`
3. Open the required `.qpf`
4. `Processing -> Start Compilation`

Expected output:

- `output_files/<project_name>.sof`

### 7.2 Program FPGA

1. Connect DE2 via USB-Blaster
2. `Tools -> Programmer`
3. Add generated `.sof`
4. Ensure `Program/Configure` checked
5. Click `Start`

## 8. Demonstration Procedure

### 8.1 Text Editor Demo

1. Connect VGA monitor and PS/2 keyboard
2. Program text editor `.sof`
3. Move cursor using `W/A/S/D`
4. Press different keys to change displayed glyph data
5. Toggle `SW[0]` invert mode and `SW[2:1]` color options

### 8.2 Graphic Editor Demo

1. Connect VGA monitor and PS/2 mouse
2. Program graphic editor `.sof`
3. Set color with `SW[3:1]`
4. Enable draw with `SW[0]`
5. Hold left button and move mouse to draw
6. Press/hold `KEY[1]` to clear

## 9. Verification Checklist

- Text editor VGA output stable and synchronized
- Keyboard scan codes visible on LEDs
- Cursor movement constrained to visible cell range
- Graphic editor cursor tracks mouse movement
- Draw mode only active when enabled
- Clear functionality resets canvas without hanging

## 10. Known Limitations

- Text editor currently demonstrates single-cell dynamic glyph behavior instead of full multi-character typed buffer
- Graphic editor uses low-resolution logical cell grid instead of per-pixel framebuffer
- No undo/redo history in either editor

These tradeoffs were intentional to keep timing closure and resource use simple for Cyclone II.

## 11. Deliverables Summary

Completed deliverables in this package:

- VHDL source files for both editors
- Quartus project files (`.qpf`, `.qsf`)
- Top-level BDF files (`text_editor_top.bdf`, `graphic_editor_top.bdf`)
- DE2 pin assignment reference CSV in each project
- Complete implementation report (this document)

`.sof` files are generated after local Quartus compilation because they are tool-output binaries dependent on the compile environment.
