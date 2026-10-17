# Graphic Editor Block Diagram (BDF Equivalent)

## Functional Blocks

```mermaid
flowchart LR
    CLK[CLOCK_50] --> VGA[VGA_SYNC]
    PS2CLK[PS2_CLK] --> MOUSE[MOUSE]
    PS2DAT[PS2_DAT] --> MOUSE
    VGA --> TOP[graphic_editor_top compositor]
    MOUSE --> TOP
    TOP --> CANVAS[pixel_canvas RAM]
    CANVAS --> TOP
    KEY[KEY[3:0]] --> TOP
    SW[SW[17:0]] --> TOP
    TOP --> VGAOUT[VGA_R/G/B HS VS CLK BLANK SYNC]
    TOP --> LED[LEDR status]
```

## Signal Mapping Summary

- `MOUSE.mouse_cursor_row/column` -> brush and cursor location
- `MOUSE.left_button` + `SW[0]` -> draw enable
- `pixel_canvas` stores coarse pixel cells (80x60, RGB 3-bit)
- `VGA_SYNC` raster coordinates drive readback and screen output
- Cursor overlay is composited over canvas content

## How to Build Native Quartus `.bdf`

1. Create a new Block Diagram/Schematic File in Quartus.
2. Place symbols for `MOUSE`, `VGA_SYNC`, `pixel_canvas`, and a wrapper/compositor block.
3. Add top-level I/O pins matching `graphic_editor_top`.
4. Wire control and data paths as shown in the mermaid diagram.
5. Save as `graphic_editor_top.bdf` if a schematic top is required.

## Quartus II 13.0sp1 Note

- Project now includes `graphic_editor_top.bdf` as the top-level design file with top entity `graphic_editor_top_bdf`.
- The schematic instantiates existing VHDL `graphic_editor_top`; VHDL sources remain the implementation source of truth.
- If Quartus shows missing/outdated symbols: open `src/graphic_editor_top.vhd`, run **File -> Create/Update -> Create Symbol Files for Current File**, then reopen `graphic_editor_top.bdf` and use **Edit -> Update Symbol or Block**.
