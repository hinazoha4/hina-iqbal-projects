# Graphic Editor Project Report Template

> Target length: 2-6 pages (max 10 pages if needed).

## 1) Overview

- Project goal and context
- Main DE2 peripherals used (VGA, PS/2 mouse, switches, keys)
- Brief feature list

## 2) Building Blocks Figure

Insert the architecture figure (from `docs/block_diagram.md` or Quartus BDF screenshot).

**Figure placeholder:**  
`[Insert Figure 1: Graphic editor system block diagram]`

## 3) Implementation Details

### Reused Modules

- `VGA_SYNC` (+ `video_PLL`)
- `MOUSE`

### Modules Implemented From Scratch

- `graphic_editor_top`
- `pixel_canvas` (cell-based drawing memory)
- Cursor overlay and brush control logic

### Integration Notes

- Top-level port mapping to DE2 pins via `.qsf`
- Draw/clear mode behavior
- Known simplifications

## 4) Results (Screenshots / Video)

Add concise evidence of operation:

- VGA output with cursor
- Drawing mode and color changes
- Canvas clear behavior
- Optional short demo video link

**Placeholders:**  
- `[Insert Screenshot A: Startup/blank canvas]`  
- `[Insert Screenshot B: Drawing in one color]`  
- `[Insert Screenshot C: Color change and redraw]`  
- `[Insert Screenshot D: Clear operation]`  
- `[Insert Video Link: Demo clip]`

## 5) Demo Notes

- Step-by-step live demo sequence on DE2
- Interaction plan for mouse and switches
- Any troubleshooting notes

## 6) Packaging

- Confirm project archive excludes `db/` and `db_inc/`
- Mention included files (`.qpf`, `.qsf`, `src/`, `docs/`)
