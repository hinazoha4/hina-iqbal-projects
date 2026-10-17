# Text Editor Block Diagram (BDF Equivalent)

## Functional Blocks

```mermaid
flowchart LR
    CLK[CLOCK_50] --> VGA[VGA_SYNC]
    PS2CLK[PS2_CLK] --> KBD[keyboard]
    PS2DAT[PS2_DAT] --> KBD
    VGA --> TOP[text_editor_top control/render]
    KBD --> TOP
    TOP --> ROM[Char_ROM]
    ROM --> TOP
    TOP --> VGA
    TOP --> VGAOUT[VGA_R/G/B HS VS CLK BLANK SYNC]
    TOP --> LED[LEDR status]
    SW[SW[17:0]] --> TOP
    KEY[KEY[3:0]] --> TOP
```

## Signal Mapping Summary

- `keyboard.scan_code/scan_ready` -> cursor and glyph control
- `VGA_SYNC.pixel_row/pixel_column/video_on` -> text grid raster generation
- `Char_ROM` -> 8x8 glyph pixel fetch
- Top-level compositor -> 1-bit RGB expanded to DE2 10-bit VGA buses

## How to Build Native Quartus `.bdf`

1. Create a new Block Diagram/Schematic File in Quartus.
2. Insert symbols for `keyboard`, `VGA_SYNC`, `Char_ROM`, and a custom wrapper block.
3. Add top-level pins matching `text_editor_top` ports.
4. Connect according to the mermaid diagram and mapping summary.
5. Save as `text_editor_top.bdf` if you want a schematic top variant.

## Quartus II 13.0sp1 Note

- Project now includes `text_editor_top.bdf` as the top-level design file with top entity `text_editor_top_bdf`.
- The schematic instantiates existing VHDL `text_editor_top`; VHDL sources remain the implementation source of truth.
- If Quartus shows missing/outdated symbols: open `src/text_editor_top.vhd`, run **File -> Create/Update -> Create Symbol Files for Current File**, then reopen `text_editor_top.bdf` and use **Edit -> Update Symbol or Block**.
