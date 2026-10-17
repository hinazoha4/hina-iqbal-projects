# Text Editor Project Report Template

> Target length: 2-6 pages (max 10 pages if needed).

## 1) Overview

- Project goal and context
- Main DE2 peripherals used (VGA, PS/2 keyboard, switches, keys)
- Brief feature list

## 2) Building Blocks Figure

Insert the architecture figure (from `docs/block_diagram.md` or Quartus BDF screenshot).

**Figure placeholder:**  
`[Insert Figure 1: Text editor system block diagram]`

## 3) Implementation Details

### Reused Modules

- `VGA_SYNC` (+ `video_PLL`)
- `keyboard`
- `Char_ROM` and `TCGROM.MIF`

### Modules Implemented From Scratch

- `text_editor_top`
- Cursor movement and simple text rendering logic
- Display mode control and LED status output

### Integration Notes

- Top-level port mapping to DE2 pins via `.qsf`
- Clocking and reset strategy
- Known simplifications

## 4) Results (Screenshots / Video)

Add concise evidence of operation:

- VGA output screenshot(s)
- Keyboard interaction screenshot(s)
- Optional short demo video link

**Placeholders:**  
- `[Insert Screenshot A: Initial screen]`  
- `[Insert Screenshot B: Cursor movement]`  
- `[Insert Screenshot C: Different display mode]`  
- `[Insert Video Link: Demo clip]`

## 5) Demo Notes

- Step-by-step live demo sequence on DE2
- What to show first, interaction flow, expected behavior
- Any troubleshooting notes

## 6) Packaging

- Confirm project archive excludes `db/` and `db_inc/`
- Mention included files (`.qpf`, `.qsf`, `src/`, `docs/`)
