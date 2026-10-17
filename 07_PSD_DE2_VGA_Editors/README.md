# DE2 Quartus Projects: Text and Graphic Editors

This workspace now contains two independent Quartus VHDL projects for DE2:

- `text_editor_project`
- `graphic_editor_project`

Each project is self-contained with:

- Quartus project files (`.qpf`, `.qsf`)
- `src/` VHDL sources
- `constraints/DE2_pin_assignments.csv` reference copy
- `docs/` block diagram and report template

## Build and Program (Quartus GUI)

1. Open Quartus and select `File -> Open Project`.
2. For text editor, open `text_editor_project/text_editor_project.qpf`.
3. For graphic editor, open `graphic_editor_project/graphic_editor_project.qpf`.
4. Compile with `Processing -> Start Compilation`.
5. Program DE2 using `Tools -> Programmer` and generated `.sof`.

## Build from Command Line (if `quartus_sh` is available)

Run from workspace root:

```powershell
quartus_sh --flow compile text_editor_project\text_editor_project.qpf
quartus_sh --flow compile graphic_editor_project\graphic_editor_project.qpf
```

## Board Demo Notes

### Text Editor Project

- Connect PS/2 keyboard and VGA monitor.
- `KEY[0]`: active-low reset.
- `W/A/S/D`: move cursor.
- Any key updates displayed glyph selection.
- `SW[0]`: invert display mode.
- `SW[2:1]`: color variation.

### Graphic Editor Project

- Connect PS/2 mouse and VGA monitor.
- `KEY[0]`: active-low reset for mouse logic.
- `KEY[1]`: hold to clear canvas.
- `SW[0]`: draw enable mode.
- `SW[3:1]`: brush RGB color.
- `SW[4]`: cursor accent behavior.
- Left mouse button draws on canvas grid.

## BDF Workflow

Each project includes a BDF-equivalent markdown diagram in `docs/block_diagram.md`.
To recreate native Quartus `.bdf`:

1. `File -> New -> Block Diagram/Schematic File`.
2. Place symbols for listed modules/entities from the diagram.
3. Wire signals as documented.
4. Save as `.bdf` and (optionally) set as top-level wrapper or keep VHDL top as-is.

## Packaging / ZIP (Exclude Quartus databases)

PowerShell examples from workspace root:

```powershell
# Text editor package
Compress-Archive -Path "text_editor_project\*" -DestinationPath "text_editor_project.zip" -Force

# Graphic editor package
Compress-Archive -Path "graphic_editor_project\*" -DestinationPath "graphic_editor_project.zip" -Force
```

Before zipping, remove generated DB folders if present:

```powershell
Remove-Item -Recurse -Force "text_editor_project\db","text_editor_project\db_inc" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "graphic_editor_project\db","graphic_editor_project\db_inc" -ErrorAction SilentlyContinue
```

Or use `7z` with explicit excludes:

```powershell
7z a text_editor_project.zip .\text_editor_project\* -xr!db -xr!db_inc
7z a graphic_editor_project.zip .\graphic_editor_project\* -xr!db -xr!db_inc
```
