import json
from pathlib import Path

p = Path(r"c:\Users\Lenovo\Downloads\computer architecture\graphics_AR_labs\examples_official")
for f in sorted(p.glob("*.ipynb")):
    nb = json.loads(f.read_text(encoding="utf-8"))
    parts = []
    for i, c in enumerate(nb["cells"]):
        src = "".join(c.get("source", []))
        parts.append(f"CELL {i} {c['cell_type']}\n{src}\n\n====\n")
    out = p / f"dump_{f.stem}.txt"
    out.write_text("\n".join(parts), encoding="utf-8")
    print("wrote", out.name, "cells", len(nb["cells"]))
