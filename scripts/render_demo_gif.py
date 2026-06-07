#!/usr/bin/env python3
"""Render the README demo GIF from synthetic SVG frames.

Requires macOS `sips` for SVG-to-PNG rasterization and `ffmpeg` for GIF
assembly. The GIF is intentionally synthetic: no real terminals, private repo
names, tokens, vendor UI, or user data are captured.
"""

from __future__ import annotations

import argparse
import html
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import TypedDict

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "assets" / "demo-workflow.gif"
WIDTH = 960
HEIGHT = 540


class Frame(TypedDict):
    step: int
    headline: str
    subhead: str
    agent_title: str
    agent_lines: list[str]
    badge: str


FRAMES: list[Frame] = [
    {
        "step": 0,
        "headline": "1. Pick the workflow that matches the situation",
        "subhead": "Start from a proven operating procedure, not a blank prompt.",
        "agent_title": "Situation",
        "agent_lines": [
            "Bug report: checkout total is wrong",
            "Need: smallest safe fix",
            "Risk: agent may edit unrelated code",
        ],
        "badge": "choose a card",
    },
    {
        "step": 1,
        "headline": "2. Copy a bounded Agent brief",
        "subhead": "Goal, scope, non-goals, verification, and stop conditions travel together.",
        "agent_title": "Copied brief",
        "agent_lines": [
            "Goal: fix failing checkout total",
            "Scope: src/cart and tests/cart",
            "Non-goals: no deploys or repo settings",
            "Verification: pytest tests/cart -q",
            "Stop if: secrets or destructive actions",
        ],
        "badge": "scope boxed",
    },
    {
        "step": 2,
        "headline": "3. Paste it into any agent tool",
        "subhead": "Claude Code, Codex CLI, Cursor, Aider, OpenCode, local agents, or your own runner.",
        "agent_title": "Agent input",
        "agent_lines": [
            "Workflow: regression-test-first bug fix",
            "Goal: fix failing checkout total",
            "Allowed: src/cart and tests/cart",
            "Required: failing test before patch",
            "Final response: evidence + risks",
        ],
        "badge": "tool-neutral",
    },
    {
        "step": 3,
        "headline": "4. Let the agent work inside the contract",
        "subhead": "The workflow blocks drive-by edits and keeps the trail auditable.",
        "agent_title": "Agent run",
        "agent_lines": [
            "[1] Read targeted cart tests",
            "[2] Added failing regression test",
            "[3] Patched checkout total logic",
            "[4] Prepared verification evidence",
        ],
        "badge": "bounded work",
    },
    {
        "step": 4,
        "headline": "5. Verify before any success claim",
        "subhead": "The repo treats agent summaries as untrusted until commands prove the result.",
        "agent_title": "Verification",
        "agent_lines": [
            "$ pytest tests/cart -q",
            "12 passed in 1.8s",
            "$ git diff --check",
            "OK",
        ],
        "badge": "evidence first",
    },
    {
        "step": 5,
        "headline": "6. Ship a report with traceable evidence",
        "subhead": "Every claim points back to files, commands, checks, or remaining risks.",
        "agent_title": "Final report",
        "agent_lines": [
            "Summary: checkout total fixed",
            "Files: src/cart.py, tests/test_cart.py",
            "Cmd: pytest tests/cart -q -> 12 passed",
            "Risks: no production changes made",
        ],
        "badge": "less vibes",
    },
]

WORKFLOW_CARD_LINES = [
    ("WORKFLOW CARD", 18, "#93C5FD", "mono"),
    ("Regression-Test-First", 24, "#F8FAFC", "sans"),
    ("Bug Fix", 24, "#F8FAFC", "sans"),
    ("Goal: capture a bug as a failing test", 18, "#CBD5E1", "mono"),
    ("Scope: targeted files and commands only", 18, "#CBD5E1", "mono"),
    ("Verify: exact command output required", 18, "#CBD5E1", "mono"),
    ("Stop: ask before secrets or side effects", 18, "#CBD5E1", "mono"),
]

PROGRESS = ["Pick", "Brief", "Agent", "Verify", "Evidence", "Report"]


SANS = "Inter, -apple-system, BlinkMacSystemFont, 'SF Pro Text', Helvetica, Arial, sans-serif"
MONO = "'SF Mono', SFMono-Regular, ui-monospace, Menlo, Consolas, monospace"


def command_bin(name: str) -> str:
    binary = shutil.which(name)
    if not binary:
        raise SystemExit(f"{name} is required to render assets/demo-workflow.gif")
    return binary


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def rect(x: int, y: int, w: int, h: int, fill: str, *, stroke: str | None = None, sw: int = 0, rx: int = 0, opacity: float | None = None) -> str:
    attrs = [f'x="{x}"', f'y="{y}"', f'width="{w}"', f'height="{h}"', f'fill="{fill}"']
    if rx:
        attrs.append(f'rx="{rx}"')
    if stroke:
        attrs.append(f'stroke="{stroke}"')
        attrs.append(f'stroke-width="{sw}"')
    if opacity is not None:
        attrs.append(f'opacity="{opacity}"')
    return f"<rect {' '.join(attrs)}/>"


def text(value: str, x: int, y: int, size: int, fill: str = "#F8FAFC", *, family: str = SANS, weight: int | str = 500) -> str:
    return (
        f'<text x="{x}" y="{y}" fill="{fill}" font-family="{family}" '
        f'font-size="{size}" font-weight="{weight}">{esc(value)}</text>'
    )


def render_svg(frame: Frame) -> str:
    step = frame["step"]
    pieces: list[str] = [
        f'<svg width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" xmlns="http://www.w3.org/2000/svg" role="img">',
        "<title>Awesome Agent Workflows demo</title>",
        "<defs>",
        '<linearGradient id="bg" x1="0" y1="0" x2="960" y2="540" gradientUnits="userSpaceOnUse">',
        '<stop stop-color="#0B1020"/><stop offset="0.55" stop-color="#121A3A"/><stop offset="1" stop-color="#1D0B2E"/>',
        "</linearGradient>",
        '<radialGradient id="glow" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(740 92) rotate(130) scale(360 220)">',
        '<stop stop-color="#7C3AED" stop-opacity="0.55"/><stop offset="1" stop-color="#7C3AED" stop-opacity="0"/>',
        "</radialGradient>",
        "</defs>",
        rect(0, 0, WIDTH, HEIGHT, "url(#bg)"),
        rect(0, 0, WIDTH, HEIGHT, "url(#glow)"),
        rect(34, 28, 892, 484, "#0F172A", rx=24),
        rect(34, 28, 892, 8, "#38BDF8", rx=4),
        rect(58, 52, 13, 13, "#F87171", rx=7),
        rect(80, 52, 13, 13, "#FBBF24", rx=7),
        rect(102, 52, 13, 13, "#34D399", rx=7),
        text("Awesome Agent Workflows", 136, 65, 24, "#F8FAFC", weight=800),
        rect(678, 43, 214, 32, "#102A26", stroke="#22C55E", sw=2, rx=16),
        text("copy -> verify -> ship", 696, 64, 17, "#BBF7D0", weight=700),
    ]

    start_x = 84
    for index, label in enumerate(PROGRESS):
        x = start_x + index * 136
        active = index <= step
        fill = "#0EA5E9" if active else "#334155"
        label_fill = "#E0F2FE" if active else "#94A3B8"
        pieces.append(rect(x, 91, 96, 27, fill, rx=12))
        pieces.append(text(label, x + 15, 110, 15, label_fill, weight=700))
        if index < len(PROGRESS) - 1:
            pieces.append(rect(x + 98, 103, 34, 3, "#38BDF8" if index < step else "#334155", rx=2))

    pieces.extend(
        [
            text(frame["headline"], 70, 153, 26, "#F8FAFC", weight=800),
            text(frame["subhead"], 70, 189, 18, "#CBD5E1"),
            rect(70, 214, 386, 238, "#111827", stroke="#38BDF8" if step <= 1 else "#475569", sw=2, rx=18),
            rect(88, 236, 140, 28, "#172554", rx=12),
        ]
    )

    y = 256
    for line, size, fill, family in WORKFLOW_CARD_LINES:
        pieces.append(text(line, 96, y, size, fill, family=MONO if family == "mono" else SANS, weight=800 if size >= 24 else 700))
        y += 31 if size >= 24 else 29

    if step == 1:
        pieces.extend(
            [
                rect(88, 312, 344, 111, "#052E24", stroke="#22C55E", sw=2, rx=12, opacity=0.85),
                text("COPY", 370, 342, 16, "#BBF7D0", weight=900),
            ]
        )

    pieces.extend(
        [
            rect(504, 214, 386, 238, "#020617", stroke="#A78BFA" if step >= 2 else "#475569", sw=2, rx=18),
            rect(504, 214, 386, 36, "#1E293B", rx=18),
            rect(504, 232, 386, 18, "#1E293B"),
            text(frame["agent_title"], 522, 238, 18, "#F8FAFC", weight=800),
        ]
    )

    y = 289
    for line in frame["agent_lines"]:
        line_fill = "#BBF7D0" if (step == 4 and (line.startswith("$") or "passed" in line or line == "OK")) else "#E2E8F0"
        pieces.append(text(line, 526, y, 17, line_fill, family=MONO, weight=650))
        y += 33

    pieces.extend(
        [
            rect(70, 468, 170, 30, "#2A1608", stroke="#F97316", sw=2, rx=15),
            text(frame["badge"], 88, 489, 16, "#FED7AA", weight=800),
            text("Copy a workflow. Require evidence. Ship with less trust in vibes.", 270, 490, 18, "#F8FAFC", weight=750),
            "</svg>",
        ]
    )
    return "\n".join(pieces)


def render_png(sips: str, frame: Frame, svg_path: Path, png_path: Path) -> None:
    svg_path.write_text(render_svg(frame))
    cmd = [sips, "-s", "format", "png", svg_path.as_posix(), "--out", png_path.as_posix()]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def concat_path(path: Path) -> str:
    """Escape a path for a single-quoted ffmpeg concat-demuxer line."""
    return path.as_posix().replace("\\", "\\\\").replace("'", "\\'")


def render_gif(ffmpeg: str, frame_paths: list[Path], output: Path) -> None:
    list_file = frame_paths[0].parent / "demo-workflow.concat.txt"
    durations = [1.15, 1.25, 1.25, 1.25, 1.35, 1.65]
    lines: list[str] = []
    for frame_path, duration in zip(frame_paths, durations, strict=True):
        lines.append(f"file '{concat_path(frame_path)}'")
        lines.append(f"duration {duration}")
    lines.append(f"file '{concat_path(frame_paths[-1])}'")
    list_file.write_text("\n".join(lines) + "\n")
    try:
        palette = (
            "fps=8,scale=720:-1:flags=lanczos,split[s0][s1];"
            "[s0]palettegen=max_colors=96[p];"
            "[s1][p]paletteuse=dither=bayer:bayer_scale=5"
        )
        cmd = [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            list_file.as_posix(),
            "-vf",
            palette,
            "-loop",
            "0",
            output.as_posix(),
        ]
        subprocess.run(cmd, check=True)
    finally:
        list_file.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="GIF output path. Defaults to assets/demo-workflow.gif.",
    )
    args = parser.parse_args()

    sips = command_bin("sips")
    ffmpeg = command_bin("ffmpeg")
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="agent-workflows-demo-") as tmp:
        tmpdir = Path(tmp)
        frame_paths: list[Path] = []
        for index, frame in enumerate(FRAMES):
            svg_path = tmpdir / f"frame-{index:02d}.svg"
            png_path = tmpdir / f"frame-{index:02d}.png"
            render_png(sips, frame, svg_path, png_path)
            frame_paths.append(png_path)
        render_gif(ffmpeg, frame_paths, output)

    display_path = output.relative_to(ROOT) if output.is_relative_to(ROOT) else output
    print(f"rendered {display_path}")


if __name__ == "__main__":
    main()
