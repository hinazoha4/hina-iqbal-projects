# DE2 Lab Projects — Modules and Files (English reference for defence)

This document describes **what each part of the design does** and **how files connect**. Use it to prepare your viva: explain **inputs/outputs**, **clock domains**, and **where the top-level BDF sits** in the hierarchy.

**Integrity note:** Understanding and explaining this design is your responsibility. If you used lab handouts, GitHub, or a teammate’s baseline, your course may require you to **say so** in the report. This guide explains the **circuit behaviour**, not who originally typed each line.

---

## 1. Big picture: FPGA on DE2

- **FPGA:** Altera Cyclone II (device `EP2C35F672C6` on Terasic DE2).
- **Quartus:** compiles VHDL + BDF schematics → bitstream (`.sof`) → downloaded to FPGA via USB-Blaster.
- **Top level:** Each project has one **top-level entity** set in the `.qsf` (`TOP_LEVEL_ENTITY`). Here it is a **BDF** (block diagram) file with the same base name as the entity (Quartus convention).

### 1.1 What is a `.bdf` file?

- **BDF (Block Design File)** is a **schematic** entry: boxes are **components** (VHDL entities, megafunctions, or other BDFs); wires are **signals**.
- The **top BDF** connects board pins (`CLOCK_50`, `PS2_CLK`, `VGA_R`, …) to internal blocks.
- **Why use BDF?** Fast wiring of many IP blocks; **why use VHDL?** Easier for state machines, arithmetic, and tables (e.g. scan-code → character).

### 1.2 What is `de2_board_ip/`?

Shared VHDL from the DE2 reference design (VGA timing, PS/2 keyboard/mouse, PLL, character ROM, etc.). Your `.qsf` adds:

```text
SEARCH_PATH "../de2_board_ip"
```

so the compiler finds entities such as `VGA_SYNC`, `keyboard`, `MOUSE`, `CHAR_ROM`, `video_PLL` without copying every file into each project folder.

---

## 2. Project 1 — Text editor (`de2_text_editor_lab`)

**Open in Quartus:** `de2_text_editor_lab.qpf`  
**Top schematic:** `de2_text_editor_top.bdf`  
**Top-level entity name:** `de2_text_editor_top`

### 2.1 Intended behaviour (board)

- **PS/2 keyboard** sends **scan codes** (8-bit) serially.
- Design decodes keys, maintains a **text buffer** (typically in on-chip RAM), and drives **VGA** so characters appear on screen (via **CHAR_ROM** glyph bitmaps inside `VGA_SYNC` path).
- **Cursor** moves with typing, **Enter**, **Backspace**, and **arrow** keys (see `CursorControl`).

### 2.2 Main file types in this folder

| File pattern | Role |
|--------------|------|
| `*.vhd` | RTL: behaviour described in VHDL. |
| `*.bdf` | Schematic hierarchy. |
| `*.qip` | Quartus IP “pointer” file; includes generated `lpm_*.vhd` for RAM, mux, flops, etc. |
| `mem_space.hex` | Initial contents / data for memory (if used by the RAM megafunction). |
| `de2_text_editor_lab.qsf` | **Project settings:** device, pin assignments, list of all design files, `TOP_LEVEL_ENTITY`. |
| `de2_text_editor_lab.qpf` | **Project pointer:** which revision name (usually matches `.qsf` base name). |

### 2.3 Hierarchy (conceptual)

```text
de2_text_editor_top (BDF)  ← TOP
  ├─ keyboard / PS2 interface (from de2_board_ip, wired in BDF)
  ├─ keyboard_processor (BDF) — glue + registers + FSM wiring
  │    └─ Keyboard_Controller (VHDL) — FSM: read scan, detect break prefixes
  ├─ ScancodeToCharAddress (VHDL) — maps scan code → CHAR_ROM address
  ├─ CursorControl (VHDL) — row/col cursor, write address for buffer
  ├─ ReadAddress (VHDL) — maps pixel position → read address (40×30 style grid)
  ├─ lpm_ram_dp* — dual-port RAM for character buffer
  ├─ Char_ROM / font path (from de2_board_ip, instantiated in VGA block)
  └─ VGA_SYNC (from de2_board_ip) — pixel timing, sync, mixes colour with character pixels
```

*(Exact instance names appear on the BDF in Quartus.)*

### 2.4 Key VHDL modules (what to say in defence)

#### `ScancodeToCharAddress.vhd`

- **Inputs:** `scan_code (7:0)` — PS/2 **make code** for a key.  
- **Outputs:** `char_address (5:0)` — index into **character ROM** / font table.  
- **Behaviour:** Large concurrent `when` / mux: each supported key maps to a 6-bit character code (letters, digits, punctuation, space). Unknown codes map to a default (e.g. blank).

#### `Keyboard_Controller.vhd`

- **Role:** Small **finite-state machine** around `scan_ready` and `scan_code`.  
- Detects **break** prefix bytes (`0xF0`, `0xE0`) so the system can ignore release sequences if needed.  
- **Outputs:** `read`, `wren`, `next_state` — handshake with the PS/2 receiver so you only **latch** a new character when appropriate.

#### `CursorControl.vhd`

- **Role:** Maintains **cursor column/row** in a text grid (e.g. 40 columns).  
- On each valid write event (`wren` edge), updates position from `scan_code`: **Enter** wraps to next line; **Backspace** moves back; **arrows** move within grid; printable keys advance column (with end-of-line wrap).  
- **Outputs:** `w_addr` — linear address into RAM for **write**; flags like `backspace`, `arrow` for other logic.

#### `ReadAddress.vhd`

- **Role:** For a given pixel block (`px_row`, `px_col` upper bits), compute **read address** of the character memory: `row * 40 + col` (text framebuffer addressing).

#### `KeyboardManager.vhd`

- Often a **variant or duplicate** controller pattern (if instantiated). Be ready to say whether your top uses **only** `Keyboard_Controller` or both; check the BDF.

#### Megafunction files (`lpm_ram_dp*.vhd`, `lpm_mux*.vhd`, `lpm_ff*.vhd`, …)

- Generated by **MegaWizard / IP catalog**: **dual-port RAM** (separate read/write ports for VGA read vs keyboard write), **muxes**, **registers**, **comparators**.  
- Defence line: *“RAM is inferred or instantiated as altsyncram via Quartus IP; addresses come from CursorControl / ReadAddress.”*

### 2.5 `keyboard_processor.bdf`

- Middle level schematic: connects **keyboard controller**, **flip-flops**, **RAM ports**, and status signals.  
- Say: *“This BDF is the PS/2-to-memory datapath; the top BDF connects it to VGA and board pins.”*

---

## 3. Project 2 — Graphic editor (`de2_graphic_editor_lab`)

**Open:** `de2_graphic_editor_lab.qpf`  
**Top schematic:** `de2_graphic_editor_top.bdf`  
**Top-level entity:** `de2_graphic_editor_top`

### 3.1 Intended behaviour

- **PS/2 mouse** provides position and buttons (via `MOUSE` entity from `de2_board_ip`).
- **Framebuffer / colour memory** (RAM + mux tree — many `lpm_mux*` and `lpm_ram_dp0`) stores per-pixel or per-cell colour.
- **`PAINT_CONTROL`** / **`Cursor`** combine **stored RGB** with **mouse cursor overlay**.
- **`Vertical_RGB_Pattern`** can generate **test patterns** (bars, checkerboard, line) for bring-up (also wired through mux hierarchy in BDF).

### 3.2 Key VHDL modules

#### `PAINT_CONTROL.vhd`

- **Inputs:** current pixel (`px_col`, `px_row`), mouse pixel (`px_col_mouse`, `px_row_mouse`), `paint_colour`, `clear`, `left_b`, `right_b`.  
- **Outputs:** `red`, `green`, `blue`, `cursor`.  
- **Behaviour:** When the current raster pixel equals the mouse cell, output **paint colour** or **erase** depending on buttons; assert `cursor` when drawing the pointer cell.

#### `Cursor.vhd`

- Overlays **white** (or fixed highlight) at the mouse coordinate on top of `memory_rgb` from memory so the pointer is always visible.

#### `Name_Address.vhd`

- For a **fixed screen region** (hard-coded pixel ranges), outputs a **sequence of character codes** spelling a banner (e.g. name string) — used as a **static label** on screen.

#### `Vertical_RGB_Pattern.vhd`

- **Test pattern generator:** selects among vertical colour bands, checkerboard, diagonal line, etc., based on `pattern_select` and current pixel coordinates.

### 3.3 Other BDFs in this project

- `MOUSE_position.bdf`, `Vertical_Pattern.bdf`, `KEYBOARD_keycode.bdf`, `VGA_*_TEST.bdf`, `CHAR_ROM_TEST.bdf`: **subsystems or experiments**. Only files listed in `.qsf` are guaranteed in the build; the **top** is `de2_graphic_editor_top.bdf`.

---

## 4. Pin and clock summary (both projects)

- **`CLOCK_50`:** 50 MHz board oscillator → usually through **PLL** (`video_PLL`) to generate **pixel clock** for VGA.  
- **`PS2_CLK`, `PS2_DAT`:** PS/2 clock and data (open-collector style; design may use input-only or bidir depending on top-level ports).  
- **`VGA_R/G/B`, `VGA_HS`, `VGA_VS`, `VGA_CLK`, `VGA_BLANK`, `VGA_SYNC`:** standard DE2 VGA interface.  
- Full pin list is in `DE2_pin_assignments.csv` and duplicated as `set_location_assignment` lines inside each `.qsf`.

---

## 5. What was the old Portuguese `report.txt`?

In the original **text editor** folder there was a file **`report.txt` written in Portuguese**. It was **not executable hardware**; it was a **student lab write-up** explaining:

- PS/2 **make code** vs **break code** (key press vs release).  
- That **break codes** often use prefix `F0h` before the make code.  
- That the design only relied on a small key subset (e.g. Space, Enter, Backspace).  
- How the **`keyboard`** module signals **`read`** and **`scan_ready`** to handshake one scan code at a time.

**English takeaway:** the Portuguese file was **documentation of the keyboard protocol and FSM idea**, not a separate “Portuguese program”. Your submission should use **English** reports (like the separate `LAB_REPORT_10_PAGES_SOURCE_EN.md` template).

---

## 6. Typical defence questions — short answers

1. **Why BDF on top?** Easier to connect many IP blocks and buses; VHDL used where combinational tables or FSMs are clearer.  
2. **Where is the text stored?** In **on-chip RAM** (`lpm_ram_dp*`), addressed by cursor (write) and by video scan (read).  
3. **How does VGA know which pixel to show?** `VGA_SYNC` tracks **horizontal/vertical counters**; those index the framebuffer / CHAR_ROM.  
4. **What is `SEARCH_PATH`?** Tells Quartus where to search for **extra VHDL** not explicitly listed (here: `de2_board_ip`).  
5. **What does compile do?** Analysis & Synthesis → Fitter → Assembler → produces `.sof` for SRAM programming on DE2.

---

## 7. File checklist before demo

- [ ] Correct `.qpf` opened.  
- [ ] `TOP_LEVEL_ENTITY` matches top BDF name.  
- [ ] `../de2_board_ip` exists relative to project folder.  
- [ ] Compile **0 errors**; warnings reviewed.  
- [ ] Programmer sees USB-Blaster; `.sof` loads.

Good luck with your defence.
