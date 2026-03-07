#!/usr/bin/env python3
"""Generate the Malak architecture diagram as SVG — matches the TikZ version."""

import os

W, H = 700, 380

def rect(x, y, w, h, fill, stroke, title, sub, rx=6):
    return (
        f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="2"/>\n'
        f'  <text x="{x+w/2}" y="{y+h/2-5}" text-anchor="middle" '
        f'font-family="Segoe UI,Arial,sans-serif" font-size="13" font-weight="bold" fill="#222">{title}</text>\n'
        f'  <text x="{x+w/2}" y="{y+h/2+11}" text-anchor="middle" '
        f'font-family="Segoe UI,Arial,sans-serif" font-size="9" fill="#666">{sub}</text>'
    )

def arrow_h(x1, y, x2, dashed=False):
    """Horizontal arrow from (x1,y) to (x2,y)."""
    col = "#aaa" if dashed else "#555"
    dash = ' stroke-dasharray="5,4"' if dashed else ""
    mid = "D" if dashed else ""
    return (f'  <line x1="{x1}" y1="{y}" x2="{x2-6}" y2="{y}" '
            f'stroke="{col}" stroke-width="1.8"{dash} marker-end="url(#ah{mid})"/>')

def arrow_v(x, y1, y2, dashed=False):
    """Vertical arrow from (x,y1) to (x,y2)."""
    col = "#aaa" if dashed else "#555"
    dash = ' stroke-dasharray="5,4"' if dashed else ""
    mid = "D" if dashed else ""
    return (f'  <line x1="{x}" y1="{y1}" x2="{x}" y2="{y2-6}" '
            f'stroke="{col}" stroke-width="1.8"{dash} marker-end="url(#ah{mid})"/>')

def main():
    bw, bh = 160, 58          # box size
    gap_x, gap_y = 30, 40     # gaps
    left = 90                  # left margin for labels
    c1 = left + 10
    c2 = c1 + bw + gap_x
    c3 = c2 + bw + gap_x
    r1 = 55
    r2 = r1 + bh + gap_y
    r3 = r2 + bh + gap_y

    # Separators y
    sep1 = r1 + bh + gap_y/2
    sep2 = r2 + bh + gap_y/2

    modules = [
        # Row 1 — Preparation
        (c1, r1, bw, bh, "#dbeafe", "#3b82f6", "Training",     "SGD / Adam"),
        (c2, r1, bw, bh, "#dcfce7", "#22c55e", "Quantization", "PTQ, QAT"),
        (c3, r1, bw, bh, "#ffedd5", "#f97316", "Compression",  "Prune, Distill"),
        # Row 2 — Deployment
        (c1, r2, bw, bh, "#fee2e2", "#ef4444", "Compiler",     "ONNX Export"),
        (c2, r2, bw, bh, "#f3e8ff", "#a855f7", "Runtime",      "Latency, Tput"),
        (c3, r2, bw, bh, "#cffafe", "#06b6d4", "Monitoring",   "Profile, Drift"),
    ]

    # CLI bar
    cli_w = c3 + bw - c1
    cli_x, cli_y = c1, r3
    cli_h = bh

    boxes = "\n".join(rect(*m) for m in modules)
    cli_box = rect(cli_x, cli_y, cli_w, cli_h, "#f3f4f6", "#9ca3af",
                   "CLI  edgeai", "train | quantize | evaluate | export | profile")

    cx1, cx2, cx3 = c1+bw/2, c2+bw/2, c3+bw/2

    arrows = "\n".join([
        # Row 1 horizontal
        arrow_h(c1+bw, r1+bh/2, c2),
        arrow_h(c2+bw, r1+bh/2, c3),
        # Row 1 → Row 2 vertical
        arrow_v(cx1, r1+bh, r2),
        arrow_v(cx2, r1+bh, r2),
        arrow_v(cx3, r1+bh, r2),
        # Row 2 horizontal
        arrow_h(c1+bw, r2+bh/2, c2),
        arrow_h(c2+bw, r2+bh/2, c3),
        # CLI → Row 2 dashed vertical
        arrow_v(cx1, cli_y, r2+bh, dashed=True),
        arrow_v(cx2, cli_y, r2+bh, dashed=True),
        arrow_v(cx3, cli_y, r2+bh, dashed=True),
    ])

    # Phase labels (rotated)
    labels = (
        f'  <text x="45" y="{r1+bh/2}" text-anchor="middle" '
        f'transform="rotate(-90,45,{r1+bh/2})" font-family="Segoe UI,Arial,sans-serif" '
        f'font-size="9" font-weight="bold" fill="#bbb" letter-spacing="2">PREPARATION</text>\n'
        f'  <text x="45" y="{r2+bh/2}" text-anchor="middle" '
        f'transform="rotate(-90,45,{r2+bh/2})" font-family="Segoe UI,Arial,sans-serif" '
        f'font-size="9" font-weight="bold" fill="#bbb" letter-spacing="2">DEPLOYMENT</text>\n'
        f'  <text x="45" y="{r3+bh/2}" text-anchor="middle" '
        f'transform="rotate(-90,45,{r3+bh/2})" font-family="Segoe UI,Arial,sans-serif" '
        f'font-size="9" font-weight="bold" fill="#bbb" letter-spacing="2">INTERFACE</text>'
    )

    seps = (
        f'  <line x1="65" y1="{sep1}" x2="{c3+bw+15}" y2="{sep1}" stroke="#e5e7eb" stroke-width="1.2"/>\n'
        f'  <line x1="65" y1="{sep2}" x2="{c3+bw+15}" y2="{sep2}" stroke="#e5e7eb" stroke-width="1.2"/>'
    )

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <defs>
    <marker id="ah" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0,8 3,0 6" fill="#555"/>
    </marker>
    <marker id="ahD" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0,8 3,0 6" fill="#aaa"/>
    </marker>
  </defs>
  <rect width="{W}" height="{H}" fill="white" rx="8"/>
  <text x="{W/2}" y="30" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif"
        font-size="15" font-weight="bold" fill="#333">Malak Software Architecture</text>

{labels}
{seps}
{boxes}
{cli_box}
{arrows}
</svg>"""

    out = os.path.expanduser("~/Desktop/Malak_Architecture.svg")
    with open(out, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
