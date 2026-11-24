"""Generate 4 original high-resolution Matplotlib diagrams for CS5222 2021A Final Q&A.

Zero exam-paper screenshots or textbook scans: 100% vector-drawn original figures
matching the exact topology, parameters, and labels of CS5222 2021/22 Sem A Final.
"""
from __future__ import annotations

import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9.2,
    "axes.titlesize": 10.2,
    "axes.titleweight": "bold",
    "figure.facecolor": "white",
    "savefig.dpi": 220,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.10,
})

ASSETS = Path(__file__).resolve().parents[1] / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)

C_NAVY = "#173F57"
C_BLUE = "#2563EB"
C_TEAL = "#0F766E"
C_AMBER = "#D97706"
C_RED = "#DC2626"
C_GREEN = "#15803D"
C_SLATE = "#475569"


def box(ax, x, y, w, h, txt, fc="#EFF6FF", ec=C_NAVY, fs=8.4, weight="bold"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.08",
                                facecolor=fc, edgecolor=ec, lw=1.3, zorder=3))
    ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", fontsize=fs, weight=weight, color="#0F172A", zorder=4)


def make_q1b() -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.4, 3.1), gridspec_kw={"width_ratios": [1.05, 1.0]})

    # Left: Network topology
    ax1.set_xlim(0, 10); ax1.set_ylim(0, 6.2); ax1.axis("off")
    ax1.set_title("Q1(b) Topology (1500 B pkts, 4 Mbps links)", fontsize=9.4)
    box(ax1, 0.2, 4.1, 2.0, 1.25, "Host 1\n(t = 0)", fc="#DBEAFE", ec=C_BLUE, fs=8.0)
    box(ax1, 0.2, 0.85, 2.0, 1.25, "Host 2\n(t = 0)", fc="#DCFCE7", ec=C_GREEN, fs=8.0)
    ax1.add_patch(plt.Circle((5.4, 3.1), 0.72, fc="#FEF3C7", ec=C_AMBER, lw=1.6, zorder=3))
    ax1.text(5.4, 3.1, "Router\nA", ha="center", va="center", fontsize=8.0, weight="bold", color=C_NAVY, zorder=4)
    ax1.add_patch(plt.Circle((9.1, 3.1), 0.72, fc="#F1F5F9", ec=C_NAVY, lw=1.6, zorder=3))
    ax1.text(9.1, 3.1, "Router\nB", ha="center", va="center", fontsize=8.0, weight="bold", color=C_NAVY, zorder=4)

    ax1.plot([2.25, 4.7], [4.7, 3.45], color=C_BLUE, lw=1.8)
    ax1.text(3.7, 4.65, "4 Mbps\nprop = 2 ms", ha="center", fontsize=7.5, color=C_BLUE, weight="bold")
    ax1.plot([2.25, 4.7], [1.45, 2.75], color=C_GREEN, lw=1.8)
    ax1.text(3.7, 1.05, "4 Mbps\nprop = 6 ms", ha="center", fontsize=7.5, color=C_GREEN, weight="bold")
    ax1.plot([6.15, 8.35], [3.1, 3.1], color=C_NAVY, lw=2.0)
    ax1.text(7.25, 3.65, "4 Mbps\nprop = 10 ms", ha="center", fontsize=7.6, color=C_NAVY, weight="bold")

    # Right: Timeline at Router A (proving zero queueing!)
    ax2.set_xlim(0, 13.5); ax2.set_ylim(0, 4.2)
    ax2.set_title("Arrival & Departure Timeline at Router A", fontsize=9.4)
    # Pkt 1 (2ms link): trans 0..3, arrives 5, forwarded 5..8
    ax2.barh(3.0, 3.0, left=0, height=0.55, color="#BFDBFE", edgecolor=C_BLUE, lw=1.2)
    ax2.text(1.5, 3.0, "Host1 tx (3ms)", ha="center", va="center", fontsize=7.3, color=C_NAVY)
    ax2.barh(3.0, 2.0, left=3, height=0.55, color="#EFF6FF", edgecolor=C_BLUE, lw=1.0, ls="--")
    ax2.text(4.0, 3.0, "prop 2", ha="center", va="center", fontsize=6.9, color=C_BLUE)
    ax2.barh(3.0, 3.0, left=5, height=0.55, color=C_BLUE, alpha=0.85, edgecolor=C_NAVY, lw=1.2)
    ax2.text(6.5, 3.0, "A->B tx [5,8]", ha="center", va="center", fontsize=7.2, color="white", weight="bold")

    # Pkt 2 (6ms link): trans 0..3, arrives 9, forwarded 9..12
    ax2.barh(1.4, 3.0, left=0, height=0.55, color="#BBF7D0", edgecolor=C_GREEN, lw=1.2)
    ax2.text(1.5, 1.4, "Host2 tx (3ms)", ha="center", va="center", fontsize=7.3, color=C_NAVY)
    ax2.barh(1.4, 6.0, left=3, height=0.55, color="#F0FDF4", edgecolor=C_GREEN, lw=1.0, ls="--")
    ax2.text(6.0, 1.4, "prop = 6 ms", ha="center", va="center", fontsize=7.2, color=C_GREEN)
    ax2.barh(1.4, 3.0, left=9, height=0.55, color=C_GREEN, alpha=0.85, edgecolor=C_NAVY, lw=1.2)
    ax2.text(10.5, 1.4, "A->B tx [9,12]", ha="center", va="center", fontsize=7.2, color="white", weight="bold")

    ax2.axvspan(8.0, 9.0, color="#FEF3C7", alpha=0.75)
    ax2.text(8.5, 2.22, "1 ms gap\nNO queue!", ha="center", va="center", fontsize=7.4, color=C_RED, weight="bold")
    ax2.set_yticks([1.4, 3.0]); ax2.set_yticklabels(["Pkt 2\n(6ms link)", "Pkt 1\n(2ms link)"], fontsize=8)
    ax2.set_xlabel("Time (ms)")
    ax2.set_xticks(range(0, 14, 1))
    ax2.grid(axis="x", ls=":", alpha=0.5)

    fig.tight_layout()
    fig.savefig(ASSETS / "final-2021a-q1b.png")
    plt.close(fig)


def make_q4d() -> None:
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    ax.set_title("Q4(d) TCP Back-to-Back Segments & Lost ACKs (x=90, y=90, z=116)", fontsize=9.6)

    ax.plot([2.2, 2.2], [0.6, 8.7], color=C_NAVY, lw=2.0)
    ax.plot([7.8, 7.8], [0.6, 8.7], color=C_TEAL, lw=2.0)
    box(ax, 1.2, 8.8, 2.0, 0.9, "Host A", fc="#DBEAFE", ec=C_NAVY, fs=9.0)
    box(ax, 6.8, 8.8, 2.0, 0.9, "Host B\n(has 0..77)", fc="#DCFCE7", ec=C_TEAL, fs=8.0)

    # Seg 1
    ax.annotate("", xy=(7.7, 6.75), xytext=(2.3, 8.15), arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=1.8))
    ax.text(5.1, 8.05, "Seg 1: Seq = 78, 12 bytes (78..89)", ha="center", fontsize=8.2, color=C_BLUE, weight="bold",
            bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.9))

    # Seg 2
    ax.annotate("", xy=(7.7, 4.85), xytext=(2.3, 6.25), arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=1.8))
    ax.text(4.65, 6.22, "Seg 2: Seq = x = 90, 26 bytes (90..115)", ha="center", fontsize=8.1, color=C_BLUE, weight="bold",
            bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.9))

    # ACK y (lost)
    ax.annotate("", xy=(4.4, 4.25), xytext=(7.7, 6.45), arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.6, ls="--"))
    ax.text(4.15, 4.10, "X", ha="center", va="center", fontsize=13, color=C_RED, weight="bold")
    ax.text(6.65, 5.45, "ACK = y = 90 (lost)", ha="center", fontsize=7.8, color=C_RED, weight="bold",
            bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.92))

    # ACK z (lost)
    ax.annotate("", xy=(4.4, 2.25), xytext=(7.7, 4.55), arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.6, ls="--"))
    ax.text(4.15, 2.10, "X", ha="center", va="center", fontsize=13, color=C_RED, weight="bold")
    ax.text(6.45, 3.25, "ACK = z = 116 (lost)", ha="center", fontsize=7.8, color=C_RED, weight="bold",
            bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.92))

    ax.text(5.0, 0.8, "In-order arrival: x = 78 + 12 = 90,   y = 78 + 12 = 90,   z = 90 + 26 = 116",
            ha="center", fontsize=8.4, color=C_NAVY, weight="bold",
            bbox=dict(boxstyle="round,pad=0.3", fc="#FEF3C7", ec=C_AMBER))

    fig.tight_layout()
    fig.savefig(ASSETS / "final-2021a-q4d.png")
    plt.close(fig)


def make_q6() -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.2, 3.3))
    pos = {"a": (0.5, 2.2), "b": (2.3, 2.2), "c": (0.5, 0.5), "d": (2.3, 0.5), "e": (4.0, 0.5)}
    edges = [("a", "b", 8), ("a", "c", 3), ("a", "d", 2), ("b", "d", 1), ("b", "e", 1), ("c", "d", 4), ("d", "e", 5)]
    spt = {("a", "d"), ("a", "c"), ("b", "d"), ("b", "e")}

    for ax, show_spt, title in [
        (ax1, False, "Q6 Original Weighted Graph"),
        (ax2, True, "Q6(b) Resulting Shortest-Path Tree from a"),
    ]:
        ax.set_title(title, fontsize=9.5)
        for u, v, w in edges:
            x1, y1 = pos[u]; x2, y2 = pos[v]
            in_spt = tuple(sorted((u, v))) in spt
            if show_spt and not in_spt:
                ax.plot([x1, x2], [y1, y2], color="#CBD5E1", lw=1.0, ls=":", zorder=1)
                continue
            col = C_RED if (show_spt and in_spt) else C_SLATE
            lw = 2.6 if (show_spt and in_spt) else 1.5
            ax.plot([x1, x2], [y1, y2], color=col, lw=lw, zorder=1)
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            dx, dy = x2 - x1, y2 - y1
            d = math.hypot(dx, dy) + 1e-9
            nx, ny = -dy / d * 0.16, dx / d * 0.16
            ax.text(mx + nx, my + ny, str(w), ha="center", va="center", fontsize=8.5, weight="bold",
                    color=C_RED if show_spt else "#1E293B",
                    bbox=dict(boxstyle="round,pad=0.14", fc="white", ec="none", alpha=0.88))

        costs = {"a": "0", "d": "2", "c": "3", "b": "3", "e": "4"}
        for n, (x, y) in pos.items():
            fc = "#FEE2E2" if n == "a" else "#EFF6FF"
            ec = C_RED if n == "a" else C_NAVY
            ax.add_patch(plt.Circle((x, y), 0.28, fc=fc, ec=ec, lw=1.7, zorder=3))
            lbl = f"{n}\n({costs[n]})" if show_spt else n
            ax.text(x, y, lbl, ha="center", va="center", fontsize=8.3 if show_spt else 9.8, weight="bold", color=ec, zorder=4)
        ax.set_xlim(-0.2, 4.7); ax.set_ylim(-0.2, 2.9)
        ax.set_aspect("equal"); ax.axis("off")

    fig.tight_layout()
    fig.savefig(ASSETS / "final-2021a-q6.png")
    plt.close(fig)


def make_q8() -> None:
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    pos = {3: (1.5, 2.8), 4: (4.1, 2.5), 2: (0.8, 0.8), 1: (3.2, 0.55), 5: (5.6, 1.1)}
    edges = [(1, 2), (1, 4), (1, 5), (2, 3), (3, 4), (4, 5)]

    ax.set_title("Q8(b)-(c) Wireless Interference Graph (Dashed = Mutual Range)", fontsize=9.6)
    for u, v in edges:
        x1, y1 = pos[u]; x2, y2 = pos[v]
        col = C_RED if {u, v} == {3, 4} else (C_BLUE if {u, v} == {1, 4} else C_SLATE)
        lw = 2.0 if {u, v} in ({1, 4}, {3, 4}) else 1.3
        ax.plot([x1, x2], [y1, y2], color=col, lw=lw, ls="--", zorder=1)

    ax.annotate("", xy=(3.95, 2.15), xytext=(3.35, 0.92),
                arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=2.2))
    ax.text(3.05, 1.65, "1 -> 4", fontsize=8.0, color=C_BLUE, weight="bold")
    ax.text(2.8, 2.92, "Station 3 hears 4\nbut NOT 1 -> HIDDEN!", ha="center", fontsize=7.8, color=C_RED, weight="bold")
    ax.text(5.15, 0.32, "For 1 -> 5:\nN(5)={1,4}, 4 hears 1\n-> NO hidden terminal", ha="center", fontsize=7.6, color=C_GREEN, weight="bold")

    for n, (x, y) in pos.items():
        fc = "#FEE2E2" if n == 3 else ("#DBEAFE" if n == 1 else "#F8FAFC")
        ec = C_RED if n == 3 else (C_BLUE if n == 1 else C_NAVY)
        ax.add_patch(plt.Circle((x, y), 0.34, fc=fc, ec=ec, lw=1.7, zorder=3))
        ax.text(x, y, str(n), ha="center", va="center", fontsize=10, weight="bold", color=ec, zorder=4)

    ax.set_xlim(-0.1, 6.6); ax.set_ylim(-0.1, 3.5)
    ax.set_aspect("equal"); ax.axis("off")
    fig.tight_layout()
    fig.savefig(ASSETS / "final-2021a-q8.png")
    plt.close(fig)


def main() -> None:
    make_q1b()
    make_q4d()
    make_q6()
    make_q8()
    print("Generated 4 original PNGs in", ASSETS)


if __name__ == "__main__":
    main()
