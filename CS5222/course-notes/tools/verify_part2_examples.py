"""Independent numerical verification & original teaching figures for CS5222 Part 2.

Covers Chapters 3 (Part 3), 4, 5, 6, 7, Tutorials 6-12, Assignments 2-3, and 2021A Final.
Generates 100% original Matplotlib diagrams (zero textbook scans) so CS5222-A4.pdf is
fully legal to print and bring into the open-notes final exam.
"""
from __future__ import annotations

import heapq
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# Use clean CJK-capable or ASCII-safe styling (all plot labels strictly clear English/math
# so zero missing glyphs across platforms, paired with detailed Chinese \StudyCaption in TeX).
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9.5,
    "axes.titlesize": 10.5,
    "axes.titleweight": "bold",
    "axes.labelsize": 9.5,
    "axes.edgecolor": "#334155",
    "axes.linewidth": 0.9,
    "figure.facecolor": "white",
    "savefig.dpi": 220,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.12,
})

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)
OUT_JSON = ROOT / "part2-example-results.json"

C_NAVY = "#173F57"
C_BLUE = "#2563EB"
C_TEAL = "#0F766E"
C_AMBER = "#D97706"
C_RED = "#DC2626"
C_SLATE = "#475569"
C_LIGHT = "#F1F5F9"
C_GREEN = "#15803D"

results: dict = {}
checks = 0


def check(cond: bool, msg: str) -> None:
    global checks
    if not cond:
        raise AssertionError(f"FAILED: {msg}")
    checks += 1


# =============================================================================
# 1. Chapter 3 Part 3 + Tutorials 6-7 + Assignment 2 (Ch.3)
# =============================================================================
def verify_ch3p3() -> None:
    # T6 Q2: TCP Seq/ACK
    seq1, len1, len2 = 127, 80, 40
    seq2 = seq1 + len1
    ack_after_1 = seq1 + len1
    ack_after_both = seq2 + len2
    check(seq2 == 207 and ack_after_1 == 207 and ack_after_both == 247, "T6 Q2 TCP seq/ack")

    # T6 Q4: 3 SampleRTTs = 106, 120, 140; initial E=100, D=5, alpha=0.125, beta=0.25
    e, d = 100.0, 5.0
    alpha, beta = 0.125, 0.25
    rtt_trace = []
    for s in [106.0, 120.0, 140.0]:
        e = (1 - alpha) * e + alpha * s
        d = (1 - beta) * d + beta * abs(s - e)
        rto = e + 4 * d
        rtt_trace.append({"sample": s, "E": round(e, 6), "D": round(d, 6), "RTO": round(rto, 6)})
    check(abs(rtt_trace[0]["E"] - 100.75) < 1e-9, "T6 Q4 E1")
    check(abs(rtt_trace[0]["D"] - 5.0625) < 1e-9, "T6 Q4 D1")
    check(abs(rtt_trace[0]["RTO"] - 121.0) < 1e-9, "T6 Q4 RTO1")
    check(abs(rtt_trace[1]["RTO"] - 135.1875) < 1e-6, "T6 Q4 RTO2")
    check(abs(rtt_trace[2]["RTO"] - 164.0234375) < 1e-6, "T6 Q4 RTO3 (~164 ms)")

    # T7 P1: TCP Reno cwnd trace (rounds 1..26)
    cwnd = {
        1: 1, 2: 2, 3: 4, 4: 8, 5: 16, 6: 32,
        **{r: 32 + (r - 6) for r in range(7, 17)},  # r=16 -> 42
        **{r: 24 + (r - 17) for r in range(17, 23)},  # r=17: 21+3=24, r=22 -> 29
        23: 1, 24: 2, 25: 4, 26: 8,
    }
    check(cwnd[16] == 42 and cwnd[17] == 24 and cwnd[22] == 29 and cwnd[26] == 8, "T7 P1 cwnd points")
    # Cumulative segments sent up to round r:
    cum = 0
    r70 = None
    for r in range(1, 27):
        prev = cum
        cum += cwnd[r]
        if prev < 70 <= cum:
            r70 = r
    check(r70 == 7, "T7 P1h 70th segment in round 7 (segs 64..96)")
    # Round 26 3 dup ACKs: ssthresh=8/2=4, cwnd=4+3=7
    check(cwnd[26] // 2 == 4 and cwnd[26] // 2 + 3 == 7, "T7 P1i after round 26")
    # Tahoe at round 16 (cwnd=42): ssthresh=21, r17=1, r18=2, r19=4
    check(cwnd[16] // 2 == 21 and 2 ** (19 - 17) == 4, "T7 P1j Tahoe round 19")

    # T7 P3: seq1=65, seq2=92 -> 27 bytes; if seg1 lost, ACK=65
    check(92 - 65 == 27, "T7 P3 bytes")

    # T7 P4: Pipelining utilization > 97%, R=10^9 bps, L=1200B=9600b, RTT=30ms
    t_trans = (1200 * 8) / 1e9  # 9.6e-6 s
    rtt = 0.030
    n_min = math.ceil(0.97 * (rtt + t_trans) / t_trans)
    check(abs(t_trans * 1e6 - 9.6) < 1e-9 and n_min == 3033, f"T7 P4 N={n_min}")

    # Avg TCP throughput example: W = 64 MSS (1 MSS = 1460B), RTT = 100 ms
    avg_thru_bps = 0.75 * (64 * 1460 * 8) / 0.1
    check(abs(avg_thru_bps / 1e6 - 5.6064) < 1e-4, "TCP 0.75 W/RTT worked example")

    results["ch3p3"] = {
        "t6_q4_trace": rtt_trace,
        "t7_p1_r70": r70,
        "t7_p4_n_min": n_min,
        "tcp_avg_thru_mbps": round(avg_thru_bps / 1e6, 4),
    }


# =============================================================================
# 2. Chapter 4 + Tutorials 8 & 10 + Assignment 2 (Ch.4)
# =============================================================================
def fragment_ipv4(total_len: int, mtu: int, hdr_len: int = 20):
    payload = total_len - hdr_len
    max_data = ((mtu - hdr_len) // 8) * 8
    frags = []
    offset_bytes = 0
    while offset_bytes < payload:
        chunk = min(max_data, payload - offset_bytes)
        mf = 1 if (offset_bytes + chunk) < payload else 0
        frags.append({
            "length": chunk + hdr_len,
            "data": chunk,
            "offset": offset_bytes // 8,
            "MF": mf,
        })
        offset_bytes += chunk
    return frags


def verify_ch4() -> None:
    # Ch.4 slide 31: 4000B datagram, MTU=1500
    f_ch4 = fragment_ipv4(4000, 1500)
    check(len(f_ch4) == 3, "Ch4 frag count")
    check([(x["length"], x["offset"], x["MF"]) for x in f_ch4] ==
          [(1500, 0, 1), (1500, 185, 1), (1040, 370, 0)], "Ch4 frag fields")

    # T8 P2: 1600B datagram, MTU=500, ID=291
    f_t8 = fragment_ipv4(1600, 500)
    check(len(f_t8) == 4, "T8 P2 frag count")
    check([(x["length"], x["offset"], x["MF"]) for x in f_t8] ==
          [(500, 0, 1), (500, 60, 1), (500, 120, 1), (160, 180, 0)], "T8 P2 frag fields")

    # Worked non-multiple-of-8 MTU trap: 2000B datagram, MTU=600 -> max_data = floor(580/8)*8 = 576
    f_trap = fragment_ipv4(2000, 600)
    check([(x["length"], x["offset"], x["MF"]) for x in f_trap] ==
          [(596, 0, 1), (596, 72, 1), (596, 144, 1), (272, 216, 0)], "MTU 600 8-byte alignment")

    # Ch.4 CIDR 137.189.178.73/17 -> net 137.189.128.0, bcast 137.189.255.255
    ip = (137 << 24) | (189 << 16) | (178 << 8) | 73
    mask17 = (0xFFFFFFFF << 15) & 0xFFFFFFFF
    net = ip & mask17
    bcast = net | (~mask17 & 0xFFFFFFFF)
    fmt = lambda x: ".".join(str((x >> s) & 255) for s in (24, 16, 8, 0))
    check(fmt(net) == "137.189.128.0" and fmt(bcast) == "137.189.255.255", "CIDR /17")

    # Ch.4/5 Q&A Slide 2: 219.100.8.32 -> 219 = 11011011 -> Class C -> 2^8 - 2 = 254
    check((219 >> 5) == 0b110 and (2 ** 8 - 2) == 254, "Q&A Class C host count")

    # T10 P1: 223.1.17.0/24 -> Subnet1 /26 (0..63), Subnet2 .128/25 (128..255), Subnet3 .64/28 (64..79)
    s1 = set(range(0, 64))
    s2 = set(range(128, 256))
    s3 = set(range(64, 80))
    check(len(s1) - 2 == 62 and len(s2) - 2 == 126 >= 106 and len(s3) - 2 == 14, "T10 P1 sizes")
    check(s1.isdisjoint(s2) and s1.isdisjoint(s3) and s2.isdisjoint(s3), "T10 P1 disjoint")

    # Buffer sizing RFC 3439 vs Appenzeller sqrt(N): C=10Gbps, RTT=250ms, N=10000
    buf_old_gbit = 0.25 * 10.0  # 2.5 Gbit
    buf_new_mbit = (0.25 * 10000.0) / math.sqrt(10000)  # 25 Mbit
    check(abs(buf_old_gbit - 2.5) < 1e-9 and abs(buf_new_mbit - 25.0) < 1e-9, "Buffer sizing")

    results["ch4"] = {
        "ch4_frags": f_ch4,
        "t8_p2_frags": f_t8,
        "mtu600_trap_frags": f_trap,
        "cidr_17": {"net": fmt(net), "bcast": fmt(bcast)},
    }


# =============================================================================
# 3. Chapter 5 + Tutorials 9 & 10 (Dijkstra + Distance Vector + Count-to-Infinity)
# =============================================================================
def run_dijkstra(nodes, edges, src, tie_order=None):
    """Exact textbook step-by-step Dijkstra table."""
    adj = {n: {} for n in nodes}
    for u, v, w in edges:
        adj[u][v] = w
        adj[v][u] = w
    if tie_order is None:
        tie_order = nodes
    rank = {n: i for i, n in enumerate(tie_order)}

    Nprime = [src]
    D = {n: (0 if n == src else adj[src].get(n, math.inf)) for n in nodes}
    p = {n: (src if n in adj[src] else None) for n in nodes}
    steps = [{"step": 0, "Nprime": list(Nprime),
              "D": {n: (None if math.isinf(D[n]) else D[n]) for n in nodes if n != src},
              "p": {n: p[n] for n in nodes if n != src}}]

    step = 0
    while len(Nprime) < len(nodes):
        step += 1
        cand = [n for n in nodes if n not in Nprime]
        w = min(cand, key=lambda n: (D[n], rank[n]))
        Nprime.append(w)
        for v, cost in adj[w].items():
            if v not in Nprime:
                if D[w] + cost < D[v]:
                    D[v] = D[w] + cost
                    p[v] = w
        steps.append({
            "step": step,
            "picked": w,
            "Nprime": list(Nprime),
            "D": {n: (None if math.isinf(D[n]) else D[n]) for n in nodes if n != src},
            "p": {n: p[n] for n in nodes if n != src},
        })
    return steps, D, p


def verify_ch5() -> None:
    # Ch.5 6-node graph (source u)
    ch5_nodes = ["u", "v", "w", "x", "y", "z"]
    ch5_edges = [
        ("u", "v", 2), ("u", "x", 1), ("u", "w", 5),
        ("v", "x", 2), ("v", "w", 3),
        ("x", "w", 3), ("x", "y", 1),
        ("w", "y", 1), ("w", "z", 5),
        ("y", "z", 2),
    ]
    ch5_steps, ch5_D, ch5_p = run_dijkstra(ch5_nodes, ch5_edges, "u", tie_order=["u", "x", "y", "v", "w", "z"])
    check(ch5_steps[-1]["Nprime"] == ["u", "x", "y", "v", "w", "z"], "Ch5 Dijkstra order")
    check(ch5_D == {"u": 0, "v": 2, "w": 3, "x": 1, "y": 2, "z": 4}, "Ch5 Dijkstra costs")
    check(ch5_p == {"u": None, "v": "u", "w": "y", "x": "u", "y": "x", "z": "y"}, "Ch5 Dijkstra preds")

    # T9 P1 7-node graph (source x)
    t9_nodes = ["x", "t", "u", "v", "w", "y", "z"]
    t9_edges = [
        ("x", "z", 8), ("x", "y", 6), ("x", "v", 3), ("x", "w", 6),
        ("z", "y", 12), ("y", "t", 7), ("y", "v", 8),
        ("v", "t", 4), ("v", "u", 3), ("v", "w", 4),
        ("w", "u", 3), ("u", "t", 2),
    ]
    t9_steps, t9_D, t9_p = run_dijkstra(t9_nodes, t9_edges, "x", tie_order=["x", "v", "u", "w", "y", "t", "z"])
    check(t9_steps[-1]["Nprime"] == ["x", "v", "u", "w", "y", "t", "z"], "T9 P1 Dijkstra order")
    check(t9_D == {"x": 0, "v": 3, "u": 6, "w": 6, "y": 6, "t": 7, "z": 8}, "T9 P1 Dijkstra costs")
    check(t9_p == {"x": None, "v": "x", "u": "v", "w": "x", "y": "x", "t": "v", "z": "x"}, "T9 P1 Dijkstra preds")

    # Ch.5 DV 3-node (x-y:2, y-z:1, x-z:7)
    def run_dv(cost_map, max_iters=60):
        nodes = sorted(cost_map.keys())
        # Initialize D[i][j] = c(i,j)
        D = {i: {j: (0 if i == j else cost_map[i].get(j, math.inf)) for j in nodes} for i in nodes}
        history = [{i: dict(D[i]) for i in nodes}]
        for _ in range(max_iters):
            newD = {i: dict(D[i]) for i in nodes}
            changed = False
            for i in nodes:
                for j in nodes:
                    if i == j:
                        continue
                    best = min(cost_map[i][v] + D[v][j] for v in cost_map[i])
                    if best != D[i][j]:
                        newD[i][j] = best
                        changed = True
            D = newD
            history.append({i: dict(D[i]) for i in nodes})
            if not changed:
                break
        return history

    dv_ch5 = run_dv({"x": {"y": 2, "z": 7}, "y": {"x": 2, "z": 1}, "z": {"x": 7, "y": 1}})
    check(dv_ch5[-1]["x"]["z"] == 3 and dv_ch5[-1]["z"]["x"] == 3, "Ch5 DV converged to 3")

    # Count-to-infinity exact simulation: c(x,y): 4 -> 60, c(y,z)=1, c(x,z)=50
    # Before change: Dy(x)=4, Dz(x)=5. After c(x,y) becomes 60:
    dy_x, dz_x = 4, 5
    cti_y, cti_z = [dy_x], [dz_x]
    # t0: y detects c(y,x)=60; computes Dy(x) = min(60+0, 1+Dz(x)) = 6
    iters = 0
    while True:
        # y updates
        new_y = min(60, 1 + dz_x)
        if new_y == dy_x:
            break
        dy_x = new_y
        iters += 1
        cti_y.append(dy_x); cti_z.append(dz_x)
        # z updates
        new_z = min(50, 1 + dy_x)
        if new_z == dz_x:
            break
        dz_x = new_z
        iters += 1
        cti_y.append(dy_x); cti_z.append(dz_x)
    # Starting from t0 (Dy=6), it takes 50-6 = 44 ping-pong increments for Dz to reach 50,
    # then 1 final update Dy=51 (47 total update messages including t0).
    check(dy_x == 51 and dz_x == 50 and iters == 47 and (50 - 6) == 44,
          f"Count-to-infinity iters={iters}, y={dy_x}, z={dz_x}")

    # T9 P2: c(x,y)=3, c(y,z)=6, c(z,x)=4 -> triangle inequality already holds (3+4=7>6, 3+6=9>4, 4+6=10>3)
    dv_t9p2 = run_dv({"x": {"y": 3, "z": 4}, "y": {"x": 3, "z": 6}, "z": {"x": 4, "y": 6}})
    check(len(dv_t9p2) == 2 and dv_t9p2[-1]["y"]["z"] == 6, "T9 P2 converges immediately (no cheaper indirect path)")

    # T9 P3: c(x,w)=2, c(x,y)=5, c(w,y)=2; Dw(u)=5, Dy(u)=6
    dx_w = min(2 + 0, 5 + 2)
    dx_y = min(2 + 2, 5 + 0)
    dx_u = min(2 + 5, 5 + 6)
    check((dx_w, dx_y, dx_u) == (2, 4, 7), "T9 P3 DV values")

    results["ch5"] = {
        "ch5_dijkstra": ch5_D,
        "t9_p1_dijkstra": t9_D,
        "cti_iters": iters,
        "cti_final": {"Dy_x": dy_x, "Dz_x": dz_x},
        "cti_y_trace": cti_y,
        "cti_z_trace": cti_z,
        "t9_p3": {"Dx_w": dx_w, "Dx_y": dx_y, "Dx_u": dx_u},
    }


# =============================================================================
# 4. Chapter 6 + Tutorials 11 & 12 + Assignment 3 (Ch.6)
# =============================================================================
def crc_mod2(data_bits: str, gen_bits: str):
    r = len(gen_bits) - 1
    buf = [int(b) for b in data_bits] + [0] * r
    gen = [int(b) for b in gen_bits]
    quotient = []
    for i in range(len(data_bits)):
        if buf[i] == 1:
            quotient.append("1")
            for j in range(len(gen)):
                buf[i + j] ^= gen[j]
        else:
            quotient.append("0")
    rem = "".join(str(b) for b in buf[-r:])
    return "".join(quotient), rem


def verify_ch6() -> None:
    # Ch.6 CRC: D=101110, G=1001 -> R=011
    q1, r1 = crc_mod2("101110", "1001")
    check(r1 == "011", f"Ch6 CRC rem={r1}")
    # Verify decoding {D, R} gives 000
    _, r1_chk = crc_mod2("101110" + r1, "1001")
    check(r1_chk == "000", "Ch6 CRC decode check")

    # T11 P2: D=1010101010, G=10011 -> q=1011011100, R=0100
    q2, r2 = crc_mod2("1010101010", "10011")
    check(q2 == "1011011100" and r2 == "0100", f"T11 P2 CRC q={q2}, r={r2}")
    _, r2_chk = crc_mod2("1010101010" + r2, "10011")
    check(r2_chk == "0000", "T11 P2 CRC decode check")

    # T11 P1: 2D even parity on 1110 0110 1001 1101 (4x4 -> min 4+4+1 = 9 parity bits)
    grid = [[1, 1, 1, 0], [0, 1, 1, 0], [1, 0, 0, 1], [1, 1, 0, 1]]
    row_p = [sum(row) % 2 for row in grid]
    col_p = [sum(grid[r][c] for r in range(4)) % 2 for c in range(4)]
    corner = sum(row_p) % 2
    check(row_p == [1, 0, 0, 1] and col_p == [1, 1, 0, 0] and corner == 0 and sum(col_p) % 2 == corner,
          "T11 P1 2D even parity")

    # ALOHA N=4 exact maxima vs N->inf asymptotes
    s_n4_max = 4 * (1 / 4) * (3 / 4) ** 3  # 27/64 = 0.421875
    p_n4_max = 4 * (1 / 7) * (6 / 7) ** 6  # p* = 1/(2N-1) = 1/7
    check(abs(s_n4_max - 27 / 64) < 1e-12, "Slotted ALOHA N=4 max = 27/64")
    check(abs(1 / math.e - 0.36787944) < 1e-6 and abs(1 / (2 * math.e) - 0.18393972) < 1e-6, "ALOHA asymptotes")

    # A3 P18: CSMA/CD 10 Mbps, t_prop = 325 bit times, min frame + preamble = 512 + 64 = 576 bit times
    t_prop_bits = 325
    min_frame_bits = 512 + 64
    worst_detect = 2 * t_prop_bits
    check(worst_detect == 650 > min_frame_bits, "A3 P18 A finishes before detecting collision")

    results["ch6"] = {
        "crc_ch6": {"quotient": q1, "rem": r1},
        "crc_t11_p2": {"quotient": q2, "rem": r2},
        "t11_p1_parity": {"row": row_p, "col": col_p, "corner": corner},
        "aloha_n4": {"slotted_max": round(s_n4_max, 6), "pure_max": round(p_n4_max, 6)},
        "a3_p18": {"min_frame_bits": min_frame_bits, "worst_detect_bits": worst_detect},
    }


# =============================================================================
# 5. Chapter 7 + Assignment 3 P8 (4-node wireless chain brute-force proof!)
# =============================================================================
def verify_ch7() -> None:
    # A3 P8: 4-node wireless chain A-B-C-D
    # Radio coverage: hears(A)={B}, hears(B)={A,C}, hears(C)={B,D}, hears(D)={C}
    hears = {"A": {"B"}, "B": {"A", "C"}, "C": {"B", "D"}, "D": {"C"}}
    directed_links = [("A", "B"), ("B", "A"), ("B", "C"), ("C", "B"), ("C", "D"), ("D", "C")]

    def valid_simultaneous(active_links):
        senders = {u for u, _ in active_links}
        receivers = {v for _, v in active_links}
        # Half-duplex: node cannot both send and receive, nor send twice
        if senders & receivers:
            return False
        if len(senders) < len(active_links) or len(receivers) < len(active_links):
            return False
        # Each intended receiver must hear EXACTLY 1 sender (its intended sender)
        for u, v in active_links:
            heard = senders & hears[v]
            if heard != {u}:
                return False
        return True

    # Verify (b): {A->B, D->C} is valid simultaneously -> rate 2!
    check(valid_simultaneous([("A", "B"), ("D", "C")]), "A3 P8b {A->B, D->C} simultaneous valid -> 2 msg/slot")
    # Verify (c): {A->B, C->D} is INVALID simultaneously (B hears both A and C -> collision!)
    check(not valid_simultaneous([("A", "B"), ("C", "D")]), "A3 P8c {A->B, C->D} collides at B -> 1 msg/slot")
    # Verify (e)-(b): exposed terminal parallelism! B->A and C->D CAN transmit simultaneously
    # because A only hears B and D only hears C (neither receiver hears two senders)!
    check(valid_simultaneous([("B", "A"), ("C", "D")]), "A3 P8eb {B->A, C->D} exposed-terminal simultaneous valid!")
    # Can B->A run with D->C? C hears both B and D -> collision at C!
    check(not valid_simultaneous([("B", "A"), ("D", "C")]), "A3 P8eb {B->A, D->C} collides at C")
    # Can C->D run with A->B? B hears both A and C -> collision at B!
    check(not valid_simultaneous([("C", "D"), ("A", "B")]), "A3 P8eb {C->D, A->B} collides at B")
    # Therefore:
    # - In (e)-(b) (A->B and D->C with ACKs): Slot 1: {A->B, D->C} (both data); Slot 2: {B->A, C->D} (both ACKs)
    #   => 2 messages every 2 slots = 1 msg/slot!
    # - In (e)-(c) (A->B and C->D with ACKs): among {A->B, B->A, C->D, D->C}, BOTH {A->B, D->C} and {B->A, C->D} are valid!
    pairs_ec = [
        (l1, l2) for i, l1 in enumerate([("A", "B"), ("B", "A"), ("C", "D"), ("D", "C")])
        for l2 in [("A", "B"), ("B", "A"), ("C", "D"), ("D", "C")][i + 1:]
        if valid_simultaneous([l1, l2])
    ]
    check(pairs_ec == [(("A", "B"), ("D", "C")), (("B", "A"), ("C", "D"))], f"A3 P8ec valid pairs = {pairs_ec}")
    #   => Steady-state 2-slot pipeline: Slot 1: {A->B (data), D->C (ACK)}; Slot 2: {B->A (ACK), C->D (data)}
    #   => 2 messages every 2 slots = 1 msg/slot (exact same rate as (c) without ACKs)!

    results["ch7"] = {
        "a3_p8_valid_pairs_ec": [list(p) for p in pairs_ec],
        "a3_p8_rates": {
            "a_wireless": "1/2",
            "b_wireless": "2",
            "c_wireless": "1",
            "e_a_wireless_ack": "1/4",
            "e_b_wireless_ack": "1 (2 msgs / 2 slots via exposed-terminal ACKs)",
            "e_c_wireless_ack": "1 (2 msgs / 2 slots via data+ACK overlap)",
        },
    }


# =============================================================================
# 6. 2021A Final Exam Full Numerical Audit
# =============================================================================
def verify_final_2021a() -> None:
    # Q1a: 1.5 GB = 12 Gbits; dial-up 56 kbps vs bus (24h wait + 100Mbps WiFi + 150km/60km/h + 1Gbps)
    bits = 1.5e9 * 8
    t_dialup_s = bits / 56e3
    t_bus_s = 24 * 3600 + bits / 100e6 + (150 / 60) * 3600 + bits / 1e9
    check(abs(t_dialup_s / 3600 - 59.5238) < 1e-3, "2021A Q1a dialup hours")
    check(abs(t_bus_s - 95532.0) < 1e-6 and abs(t_bus_s / 3600 - 26.5367) < 1e-3, "2021A Q1a bus hours")

    # Q1b: 1500B=12000b, 4Mbps -> t_trans=3ms; prop1=2ms -> arr=5ms, dep=8ms; prop2=6ms -> arr=9ms > 8ms -> NO queueing
    t_tr = 1500 * 8 / 4e6 * 1000
    check(t_tr == 3.0 and (2 + t_tr + t_tr) == 8.0 < (6 + t_tr), "2021A Q1b no queueing")

    # Q3: F=10GB=80Gb, N=10, us=10Mbps, di=2Mbps, ui=200kbps
    F = 10e9 * 8
    D_cs = max(10 * F / 10e6, F / 2e6)
    D_p2p = max(F / 10e6, F / 2e6, 10 * F / (10e6 + 10 * 200e3))
    check(D_cs == 80000.0 and abs(D_p2p - 66666.666667) < 1e-3, "2021A Q3 CS & P2P")

    # Q4a/b/d: 70 MSS (1 MSS = 1024B), RTT=100ms
    # 1+2+4+8+16+32 = 63 (6 RTTs of data), + 7th RTT for remaining 7 MSS + 1 RTT handshake = 8 RTTs
    check(sum(2 ** k for k in range(6)) == 63 and 63 + 7 == 70, "2021A Q4a 8 RTTs")
    thru_kbps = (70 * 1024 * 8) / (8 * 0.1) / 1000
    check(abs(thru_kbps - 716.8) < 1e-9, "2021A Q4b 716.8 kbps")
    check((78 + 12, 78 + 12, 78 + 12 + 26) == (90, 90, 116), "2021A Q4d x,y,z")

    # Q5b: 8-bit addresses with LPM: 1->0, 10->1, 111->2, otherwise->3
    counts = {0: 0, 1: 0, 2: 0, 3: 0}
    ranges = {0: [], 1: [], 2: [], 3: []}
    for addr in range(256):
        b = f"{addr:08b}"
        if b.startswith("111"):
            iface = 2
        elif b.startswith("10"):
            iface = 1
        elif b.startswith("1"):
            iface = 0
        else:
            iface = 3
        counts[iface] += 1
        ranges[iface].append(addr)
    check(counts == {0: 32, 1: 64, 2: 32, 3: 128}, f"2021A Q5b counts={counts}")
    check((min(ranges[0]), max(ranges[0])) == (192, 223), "Q5b iface 0")
    check((min(ranges[1]), max(ranges[1])) == (128, 191), "Q5b iface 1")
    check((min(ranges[2]), max(ranges[2])) == (224, 255), "Q5b iface 2")
    check((min(ranges[3]), max(ranges[3])) == (0, 127), "Q5b iface 3")

    # Q6: Dijkstra from a on {a,b,c,d,e}
    f6_nodes = ["a", "b", "c", "d", "e"]
    f6_edges = [("a", "b", 8), ("a", "c", 3), ("a", "d", 2), ("b", "d", 1), ("b", "e", 1), ("c", "d", 4), ("d", "e", 5)]
    f6_steps, f6_D, f6_p = run_dijkstra(f6_nodes, f6_edges, "a", tie_order=["a", "d", "b", "c", "e"])
    check(f6_D == {"a": 0, "b": 3, "c": 3, "d": 2, "e": 4}, "2021A Q6 Dijkstra costs")
    check(f6_p == {"a": None, "b": "d", "c": "a", "d": "a", "e": "b"}, "2021A Q6 Dijkstra preds")

    # Q8b/c: wireless interference graph edges: (1,2),(1,4),(1,5),(2,3),(3,4),(4,5)
    w_adj = {1: {2, 4, 5}, 2: {1, 3}, 3: {2, 4}, 4: {1, 3, 5}, 5: {1, 4}}
    hidden_1_to_4 = sorted((w_adj[4] - {1}) - w_adj[1])
    hidden_1_to_5 = sorted((w_adj[5] - {1}) - w_adj[1])
    check(hidden_1_to_4 == [3] and hidden_1_to_5 == [], "2021A Q8b/c hidden terminals")

    results["final_2021a"] = {
        "q1a_dialup_h": round(t_dialup_s / 3600, 3),
        "q1a_bus_h": round(t_bus_s / 3600, 3),
        "q3_Dcs_s": D_cs,
        "q3_Dp2p_s": round(D_p2p, 2),
        "q4b_kbps": thru_kbps,
        "q5b_counts": counts,
        "q6_D": f6_D,
        "q6_p": f6_p,
        "q8_hidden": {"1_to_4": hidden_1_to_4, "1_to_5": hidden_1_to_5},
    }


# =============================================================================
# 7. Original High-Resolution Teaching Figures (ZERO textbook screenshots!)
# =============================================================================
def draw_box(ax, x, y, w, h, text, fc="#EFF6FF", ec=C_NAVY, fontsize=8.5, weight="normal", z=3):
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
                          facecolor=fc, edgecolor=ec, linewidth=1.1, zorder=z)
    ax.add_patch(rect)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fontsize, weight=weight, color="#0F172A", zorder=z + 1)


def make_fig_ch3p3_cwnd() -> None:
    fig, ax = plt.subplots(figsize=(7.8, 3.6))
    r_reno = list(range(1, 27))
    y_reno = [1, 2, 4, 8, 16, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42,
              24, 25, 26, 27, 28, 29, 1, 2, 4, 8]
    r_tahoe = [16, 17, 18, 19, 20, 21]
    y_tahoe = [42, 1, 2, 4, 8, 16]

    ax.axvspan(1, 6, color="#DBEAFE", alpha=0.45, label="Slow Start (exp.)")
    ax.axvspan(23, 26, color="#DBEAFE", alpha=0.45)
    ax.axvspan(6, 16, color="#DCFCE7", alpha=0.40, label="Congestion Avoidance (linear)")
    ax.axvspan(17, 22, color="#DCFCE7", alpha=0.40)

    ax.plot(r_reno, y_reno, "-o", color=C_NAVY, lw=2.0, ms=4.5, label="TCP Reno cwnd")
    ax.plot(r_tahoe, y_tahoe, "--s", color=C_AMBER, lw=1.6, ms=4.2, label="TCP Tahoe (3 dup ACKs @ r=16)")

    ax.hlines(32, 1, 16, colors=C_SLATE, linestyles=":", lw=1.2)
    ax.text(1.3, 29.8, "init ssthresh = 32", fontsize=7.8, color=C_SLATE)
    ax.hlines(21, 16.5, 22, colors=C_RED, linestyles=":", lw=1.2)
    ax.text(17.1, 18.8, "ssthresh = 21", fontsize=7.8, color=C_RED)
    ax.hlines(14, 22.5, 26, colors=C_RED, linestyles=":", lw=1.2)
    ax.text(22.6, 15.2, "ssthresh = 14", fontsize=7.8, color=C_RED)

    ax.annotate("3 dup ACKs\ncwnd=42 -> 21+3=24", xy=(16, 42), xytext=(17.2, 42.8),
                arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.1, connectionstyle="arc3,rad=0.10"),
                fontsize=7.6, color=C_RED, weight="bold")
    ax.annotate("Timeout\ncwnd=29 -> 1", xy=(22, 29), xytext=(17.8, 35.8),
                arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.1),
                fontsize=7.8, color=C_RED, weight="bold")

    ax.set_xlim(0.5, 26.8)
    ax.set_ylim(0, 49)
    ax.set_xticks(range(0, 27, 2))
    ax.set_xlabel("Transmission Round (RTT)")
    ax.set_ylabel("cwnd (MSS / segments)")
    ax.set_title("TCP Reno vs. TCP Tahoe Congestion Window Evolution (Tutorial 7 P1)")
    ax.grid(True, linestyle="--", alpha=0.35)
    ax.legend(loc="upper left", fontsize=7.2, framealpha=0.94)
    fig.savefig(ASSETS / "ch3p3-tcp-reno-cwnd.png")
    plt.close(fig)


def make_fig_ch3p3_handshake() -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.2, 3.6))

    # Left: 3-way handshake
    ax1.set_xlim(0, 10); ax1.set_ylim(0, 10); ax1.axis("off")
    ax1.set_title("TCP 3-Way Handshake (Connection Setup)", fontsize=9.8)
    ax1.plot([2.5, 2.5], [0.8, 8.8], color=C_NAVY, lw=2)
    ax1.plot([7.5, 7.5], [0.8, 8.8], color=C_TEAL, lw=2)
    ax1.text(2.5, 9.2, "Client", ha="center", weight="bold", color=C_NAVY)
    ax1.text(7.5, 9.2, "Server", ha="center", weight="bold", color=C_TEAL)

    ax1.annotate("", xy=(7.4, 6.9), xytext=(2.6, 8.0), arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=1.6))
    ax1.text(5.0, 7.85, "1. SYN=1, Seq=x", ha="center", fontsize=8.2, color=C_BLUE, weight="bold")
    ax1.text(1.2, 8.0, "SYN_SENT", ha="center", fontsize=7.5, color=C_SLATE)
    ax1.text(8.8, 8.4, "LISTEN", ha="center", fontsize=7.5, color=C_SLATE)
    ax1.text(8.8, 6.7, "SYN_RCVD", ha="center", fontsize=7.5, color=C_SLATE)

    ax1.annotate("", xy=(2.6, 4.9), xytext=(7.4, 6.0), arrowprops=dict(arrowstyle="->", color=C_TEAL, lw=1.6))
    ax1.text(5.0, 5.9, "2. SYN=1, ACK=1\nSeq=y, ACKnum=x+1", ha="center", fontsize=7.8, color=C_TEAL, weight="bold")
    ax1.text(1.2, 4.7, "ESTAB", ha="center", fontsize=7.8, color=C_GREEN, weight="bold")

    ax1.annotate("", xy=(7.4, 2.8), xytext=(2.6, 3.9), arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=1.6))
    ax1.text(5.0, 3.7, "3. SYN=0, ACK=1\nSeq=x+1, ACKnum=y+1\n(may carry data)", ha="center", fontsize=7.6, color=C_BLUE)
    ax1.text(8.8, 2.6, "ESTAB", ha="center", fontsize=7.8, color=C_GREEN, weight="bold")

    # Right: 4-way teardown
    ax2.set_xlim(0, 10); ax2.set_ylim(0, 10); ax2.axis("off")
    ax2.set_title("TCP 4-Way Connection Teardown", fontsize=9.8)
    ax2.plot([2.5, 2.5], [0.5, 8.8], color=C_NAVY, lw=2)
    ax2.plot([7.5, 7.5], [0.5, 8.8], color=C_TEAL, lw=2)
    ax2.text(2.5, 9.2, "Client (active)", ha="center", weight="bold", color=C_NAVY)
    ax2.text(7.5, 9.2, "Server (passive)", ha="center", weight="bold", color=C_TEAL)

    ax2.annotate("", xy=(7.4, 7.4), xytext=(2.6, 8.2), arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.5))
    ax2.text(5.0, 8.1, "1. FIN=1, Seq=x", ha="center", fontsize=8, color=C_RED, weight="bold")
    ax2.text(1.1, 8.0, "FIN_WAIT_1", ha="center", fontsize=7.3, color=C_SLATE)
    ax2.text(8.9, 7.2, "CLOSE_WAIT", ha="center", fontsize=7.3, color=C_SLATE)

    ax2.annotate("", xy=(2.6, 5.8), xytext=(7.4, 6.6), arrowprops=dict(arrowstyle="->", color=C_TEAL, lw=1.5))
    ax2.text(5.0, 6.5, "2. ACK=1, ACKnum=x+1", ha="center", fontsize=7.8, color=C_TEAL)
    ax2.text(1.1, 5.6, "FIN_WAIT_2", ha="center", fontsize=7.3, color=C_SLATE)

    ax2.annotate("", xy=(2.6, 3.8), xytext=(7.4, 4.6), arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.5))
    ax2.text(5.0, 4.5, "3. FIN=1, Seq=y", ha="center", fontsize=8, color=C_RED, weight="bold")
    ax2.text(8.9, 4.6, "LAST_ACK", ha="center", fontsize=7.3, color=C_SLATE)
    ax2.text(1.1, 3.3, "TIME_WAIT\n(2 x MSL)", ha="center", fontsize=7.4, color=C_AMBER, weight="bold")

    ax2.annotate("", xy=(7.4, 2.1), xytext=(2.6, 2.9), arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=1.5))
    ax2.text(5.0, 2.8, "4. ACK=1, ACKnum=y+1", ha="center", fontsize=7.8, color=C_BLUE)
    ax2.text(8.9, 1.9, "CLOSED", ha="center", fontsize=7.6, color=C_NAVY, weight="bold")
    ax2.text(1.1, 1.0, "CLOSED", ha="center", fontsize=7.6, color=C_NAVY, weight="bold")

    fig.tight_layout()
    fig.savefig(ASSETS / "ch3p3-tcp-handshake-teardown.png")
    plt.close(fig)


def make_fig_ch4_frag_nat() -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.8, 3.6), gridspec_kw={"width_ratios": [1.08, 1.0]})

    # Left: IPv4 fragmentation
    ax1.set_xlim(0, 10); ax1.set_ylim(0, 10); ax1.axis("off")
    ax1.set_title("IPv4 Fragmentation (4000 B -> MTU = 1500 B)", fontsize=9.4)
    draw_box(ax1, 0.2, 7.6, 9.6, 1.55, "Original Datagram: Len=4000 (20B hdr + 3980B data)\nID = x,   MF = 0,   Offset = 0", fc="#FEF3C7", ec=C_AMBER, fontsize=7.2, weight="bold")
    ax1.annotate("", xy=(5.0, 6.45), xytext=(5.0, 7.5), arrowprops=dict(arrowstyle="->", color=C_SLATE, lw=1.5))
    ax1.text(5.2, 6.9, "MTU=1500 -> max data = 1480B (185x8B)", fontsize=7.1, color=C_SLATE)

    draw_box(ax1, 0.2, 4.7, 9.6, 1.4, "Frag 1: Len=1500 (20B+1480B) | ID=x | MF=1 | Offset=0", fc="#DBEAFE", ec=C_BLUE, fontsize=7.1)
    draw_box(ax1, 0.2, 2.8, 9.6, 1.4, "Frag 2: Len=1500 (20B+1480B) | ID=x | MF=1 | Offset=185", fc="#DBEAFE", ec=C_BLUE, fontsize=7.1)
    draw_box(ax1, 0.2, 0.9, 9.6, 1.4, "Frag 3: Len=1040 (20B+1020B) | ID=x | MF=0 | Offset=370", fc="#DCFCE7", ec=C_GREEN, fontsize=7.1)

    # Right: NAT translation
    ax2.set_xlim(0, 10); ax2.set_ylim(0, 10); ax2.axis("off")
    ax2.set_title("NAT Translation Walkthrough (WAN <-> LAN)", fontsize=9.4)
    draw_box(ax2, 0.1, 6.7, 2.55, 1.9, "Host (LAN)\n10.0.0.1\nport 3345", fc="#EFF6FF", ec=C_BLUE, fontsize=7.0)
    draw_box(ax2, 3.55, 6.7, 2.9, 1.9, "NAT Router\nWAN: 138.76.29.7\nLAN: 10.0.0.4", fc="#FEF3C7", ec=C_AMBER, fontsize=6.7, weight="bold")
    draw_box(ax2, 7.35, 6.7, 2.55, 1.9, "Web Server\n128.119.40.186\nport 80", fc="#DCFCE7", ec=C_GREEN, fontsize=6.7)

    ax2.annotate("", xy=(3.5, 8.1), xytext=(2.7, 8.1), arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=1.4))
    ax2.text(3.0, 8.95, "1. S:10.0.0.1:3345", ha="center", fontsize=6.6, color=C_BLUE)
    ax2.annotate("", xy=(7.3, 8.1), xytext=(6.5, 8.1), arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.4))
    ax2.text(7.0, 8.95, "2. S:138.76.29.7:5001", ha="center", fontsize=6.6, color=C_RED)

    ax2.annotate("", xy=(6.5, 7.15), xytext=(7.3, 7.15), arrowprops=dict(arrowstyle="->", color=C_GREEN, lw=1.4))
    ax2.text(7.0, 6.05, "3. D:138.76.29.7:5001", ha="center", fontsize=6.6, color=C_GREEN)
    ax2.annotate("", xy=(2.7, 7.15), xytext=(3.5, 7.15), arrowprops=dict(arrowstyle="->", color=C_TEAL, lw=1.4))
    ax2.text(3.0, 6.05, "4. D:10.0.0.1:3345", ha="center", fontsize=6.6, color=C_TEAL)

    draw_box(ax2, 0.3, 1.1, 9.4, 3.9,
             "NAT Translation Table\n"
             "----------------------------------------------\n"
             "WAN (Public IP, Port)  <->  LAN (Private IP, Port)\n"
             "138.76.29.7 , 5001     <->  10.0.0.1 , 3345\n"
             "138.76.29.7 , 5002     <->  10.0.0.2 , 4110",
             fc="#F8FAFC", ec=C_NAVY, fontsize=6.9)

    fig.tight_layout()
    fig.savefig(ASSETS / "ch4-ip-fragmentation-nat.png")
    plt.close(fig)


def draw_graph(ax, pos, edges, spt_edges, title, src):
    ax.set_title(title, fontsize=9.5)
    spt_set = {tuple(sorted((u, v))) for u, v in spt_edges}
    for u, v, w in edges:
        x1, y1 = pos[u]; x2, y2 = pos[v]
        is_spt = tuple(sorted((u, v))) in spt_set
        ax.plot([x1, x2], [y1, y2],
                color=C_RED if is_spt else "#94A3B8",
                lw=2.4 if is_spt else 1.2,
                linestyle="-" if is_spt else "--", zorder=1)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        # tiny perpendicular nudge for overlapping edge labels
        dx, dy = x2 - x1, y2 - y1
        dist = math.hypot(dx, dy) + 1e-9
        nx, ny = -dy / dist * 0.14, dx / dist * 0.14
        ax.text(mx + nx, my + ny, str(w), ha="center", va="center", fontsize=8,
                weight="bold" if is_spt else "normal",
                color=C_RED if is_spt else "#334155",
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.85))
    for n, (x, y) in pos.items():
        fc = "#FEE2E2" if n == src else "#EFF6FF"
        ec = C_RED if n == src else C_NAVY
        circ = plt.Circle((x, y), 0.24, facecolor=fc, edgecolor=ec, lw=1.6, zorder=3)
        ax.add_patch(circ)
        ax.text(x, y, n, ha="center", va="center", fontsize=9.5, weight="bold", color=ec, zorder=4)
    ax.set_aspect("equal")
    ax.axis("off")


def make_fig_ch5_dijkstra() -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.4, 3.6))

    # Left: Ch.5 6-node graph (source u)
    pos1 = {"u": (0, 1), "v": (1.4, 2.0), "x": (1.4, 0.0), "w": (3.0, 2.0), "y": (3.0, 0.0), "z": (4.4, 1.0)}
    edges1 = [("u", "v", 2), ("u", "x", 1), ("u", "w", 5), ("v", "x", 2), ("v", "w", 3),
              ("x", "w", 3), ("x", "y", 1), ("w", "y", 1), ("w", "z", 5), ("y", "z", 2)]
    spt1 = [("u", "v"), ("u", "x"), ("x", "y"), ("y", "w"), ("y", "z")]
    draw_graph(ax1, pos1, edges1, spt1, "Ch.5 Graph & Shortest-Path Tree from u", "u")
    ax1.set_xlim(-0.6, 5.0); ax1.set_ylim(-0.6, 2.6)

    # Right: T9 P1 7-node graph (source x)
    pos2 = {"z": (0.4, 2.7), "y": (1.3, 1.7), "x": (0.0, 0.8), "v": (2.5, 1.2), "t": (4.0, 1.8), "w": (1.8, -0.3), "u": (3.7, 0.3)}
    edges2 = [("x", "z", 8), ("x", "y", 6), ("x", "v", 3), ("x", "w", 6), ("z", "y", 12),
              ("y", "t", 7), ("y", "v", 8), ("v", "t", 4), ("v", "u", 3), ("v", "w", 4), ("w", "u", 3), ("u", "t", 2)]
    spt2 = [("x", "z"), ("x", "y"), ("x", "v"), ("x", "w"), ("v", "t"), ("v", "u")]
    draw_graph(ax2, pos2, edges2, spt2, "Tutorial 9 P1 Graph & SPT from x", "x")
    ax2.set_xlim(-0.6, 4.6); ax2.set_ylim(-0.8, 3.2)

    fig.tight_layout()
    fig.savefig(ASSETS / "ch5-dijkstra-spt.png")
    plt.close(fig)


def make_fig_ch5_dv_bgp() -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.4, 3.4))

    # Left: Count-to-infinity trace
    y_tr = results["ch5"]["cti_y_trace"]
    z_tr = results["ch5"]["cti_z_trace"]
    xs = list(range(len(y_tr)))
    ax1.plot(xs, y_tr, "-o", ms=2.8, lw=1.6, color=C_RED, label="Dy(x)")
    ax1.plot(xs, z_tr, "--s", ms=2.6, lw=1.5, color=C_BLUE, label="Dz(x)")
    ax1.axhline(50, color=C_GREEN, ls=":", lw=1.2)
    ax1.text(2, 51.5, "True path via direct link c(z,x)=50", fontsize=7.6, color=C_GREEN)
    ax1.annotate("Stabilizes at\nDz(x)=50, Dy(x)=51\n(44 bounces 6->50)", xy=(47, 51), xytext=(4, 34),
                 arrowprops=dict(arrowstyle="->", color=C_NAVY, lw=1.1, connectionstyle="arc3,rad=-0.12"),
                 fontsize=7.6, weight="bold")
    ax1.set_xlabel("Iteration (after c(x,y): 4 -> 60)")
    ax1.set_ylabel("Estimated Cost to x")
    ax1.set_title("DV Count-to-Infinity (44 Bounces)")
    ax1.set_ylim(0, 58)
    ax1.grid(True, ls="--", alpha=0.35)
    ax1.legend(loc="lower right", fontsize=8)

    # Right: BGP Hot Potato Routing
    ax2.set_xlim(0, 10); ax2.set_ylim(0, 10); ax2.axis("off")
    ax2.set_title("BGP eBGP / iBGP & Hot Potato Routing", fontsize=9.5)
    ax2.add_patch(FancyBboxPatch((0.2, 1.0), 4.4, 7.6, boxstyle="round,pad=0.1", fc="#EFF6FF", ec=C_BLUE, lw=1.3))
    ax2.text(2.4, 8.2, "AS 2 (OSPF intra-AS)", ha="center", fontsize=8.1, weight="bold", color=C_BLUE)
    ax2.add_patch(FancyBboxPatch((5.6, 5.2), 4.1, 3.4, boxstyle="round,pad=0.1", fc="#FEF3C7", ec=C_AMBER, lw=1.3))
    ax2.text(7.65, 8.2, "AS 1", ha="center", fontsize=8.1, weight="bold", color=C_AMBER)
    ax2.add_patch(FancyBboxPatch((5.6, 1.0), 4.1, 3.4, boxstyle="round,pad=0.1", fc="#DCFCE7", ec=C_GREEN, lw=1.3))
    ax2.text(7.65, 4.0, "AS 3 (owns prefix X)", ha="center", fontsize=8.1, weight="bold", color=C_GREEN)

    for lbl, (rx, ry), col in [("2d", (1.05, 4.6), C_NAVY), ("2a", (3.6, 6.6), C_BLUE), ("2c", (3.6, 2.6), C_BLUE),
                               ("1c", (6.8, 6.6), C_AMBER), ("3a", (6.8, 2.6), C_GREEN)]:
        ax2.add_patch(plt.Circle((rx, ry), 0.55, fc="white", ec=col, lw=1.5, zorder=3))
        ax2.text(rx, ry, lbl, ha="center", va="center", fontsize=8.5, weight="bold", color=col, zorder=4)

    ax2.plot([1.5, 3.1], [5.0, 6.2], color=C_BLUE, lw=1.8)
    ax2.text(1.75, 6.35, "OSPF=201", ha="center", fontsize=7.3, color=C_BLUE, weight="bold")
    ax2.plot([1.5, 3.1], [4.2, 3.0], color=C_SLATE, lw=1.5, ls="--")
    ax2.text(1.75, 2.65, "OSPF=263", ha="center", fontsize=7.3, color=C_SLATE)
    # eBGP links
    ax2.plot([4.05, 6.25], [6.6, 6.6], color=C_RED, lw=1.8)
    ax2.text(5.15, 7.05, "eBGP", ha="center", fontsize=7.5, color=C_RED, weight="bold")
    ax2.plot([4.05, 6.25], [2.6, 2.6], color=C_RED, lw=1.8)
    ax2.text(5.15, 3.05, "eBGP", ha="center", fontsize=7.5, color=C_RED, weight="bold")
    ax2.plot([6.8, 6.8], [6.05, 3.15], color=C_RED, lw=1.4, ls=":")
    ax2.text(7.9, 4.6, "AS1->AS3", fontsize=7.2, color=C_RED)
    ax2.text(5.0, 0.35, "Hot potato: 2d picks 2a (201 < 263), even if AS-PATH is longer!",
             ha="center", fontsize=7.5, color=C_NAVY, weight="bold")

    fig.tight_layout()
    fig.savefig(ASSETS / "ch5-dv-count-to-infinity.png")
    plt.close(fig)


def make_fig_ch6_aloha_switch() -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.4, 3.5))

    # Left: ALOHA efficiency curves
    p = np.linspace(0, 0.7, 300)
    s4 = 4 * p * (1 - p) ** 3
    p4 = 4 * p * (1 - p) ** 6
    ax1.plot(p, s4 * 100, color=C_BLUE, lw=2.0, label="Slotted ALOHA (N=4): 4p(1-p)^3")
    ax1.plot(p, p4 * 100, color=C_RED, lw=1.8, ls="--", label="Pure ALOHA (N=4): 4p(1-p)^6")
    ax1.axhline(100 / math.e, color=C_BLUE, ls=":", lw=1.1, alpha=0.8)
    ax1.axhline(100 / (2 * math.e), color=C_RED, ls=":", lw=1.1, alpha=0.8)
    ax1.scatter([0.25], [42.1875], color=C_BLUE, zorder=5, s=30)
    ax1.annotate("N=4 max: 42.19%\n(p=1/4)", xy=(0.25, 42.19), xytext=(0.35, 43.5),
                 arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=1), fontsize=7.6, color=C_BLUE, weight="bold")
    ax1.text(0.42, 37.8, "N->inf: 1/e = 36.8%", fontsize=7.4, color=C_BLUE)
    ax1.text(0.42, 19.4, "N->inf: 1/(2e) = 18.4%", fontsize=7.4, color=C_RED)
    ax1.set_xlim(0, 0.7); ax1.set_ylim(0, 50)
    ax1.set_xlabel("Per-slot Attempt Probability p")
    ax1.set_ylabel("Channel Efficiency (%)")
    ax1.set_title("Slotted vs. Pure ALOHA Efficiency")
    ax1.grid(True, ls="--", alpha=0.35)
    ax1.legend(loc="lower left", fontsize=7.4)

    # Right: Multi-switch self-learning topology (Tutorial 12 P2)
    ax2.set_xlim(0, 10); ax2.set_ylim(0, 10); ax2.axis("off")
    ax2.set_title("Multi-Switch Self-Learning (Tutorial 12 P2)", fontsize=9.5)
    sw = {"S4": (5.0, 8.2), "S1": (1.8, 5.2), "S2": (5.0, 5.2), "S3": (8.2, 5.2)}
    hosts = {"A": (0.7, 2.2), "B": (1.8, 2.2), "C": (2.9, 2.2),
             "D": (3.9, 2.2), "E": (5.0, 2.2), "F": (6.1, 2.2),
             "G": (7.1, 2.2), "H": (8.2, 2.2), "I": (9.3, 2.2)}
    for child in ["S1", "S2", "S3"]:
        ax2.plot([sw["S4"][0], sw[child][0]], [sw["S4"][1], sw[child][1]], color=C_NAVY, lw=1.6)
    for h, parent in [("A", "S1"), ("B", "S1"), ("C", "S1"), ("D", "S2"), ("E", "S2"), ("F", "S2"), ("G", "S3"), ("H", "S3"), ("I", "S3")]:
        ax2.plot([sw[parent][0], hosts[h][0]], [sw[parent][1], hosts[h][1]], color=C_SLATE, lw=1.2)
    # Highlight A->G unicast path on return
    ax2.annotate("", xy=(7.1, 2.8), xytext=(0.7, 2.8),
                 arrowprops=dict(arrowstyle="<->", color=C_RED, lw=1.4, ls="--", connectionstyle="arc3,rad=-0.45"))
    ax2.text(5.0, 9.35, "1) A->G: all switches flood & learn A;  2) G->A: unicast via S3->S4->S1!",
             ha="center", fontsize=7.3, color=C_RED, weight="bold")
    for k, (x, y) in sw.items():
        draw_box(ax2, x - 0.65, y - 0.45, 1.3, 0.9, k, fc="#DBEAFE", ec=C_NAVY, fontsize=8.5, weight="bold")
    for k, (x, y) in hosts.items():
        fc = "#FEE2E2" if k in ("A", "G") else "#F8FAFC"
        ec = C_RED if k in ("A", "G") else C_SLATE
        draw_box(ax2, x - 0.35, y - 0.42, 0.7, 0.84, k, fc=fc, ec=ec, fontsize=8, weight="bold" if k in ("A", "G") else "normal")
    ax2.text(5.0, 0.65, "Notice: S2 NEVER learns G (unicast G->A never enters S2)!",
             ha="center", fontsize=7.6, color=C_NAVY, weight="bold")

    fig.tight_layout()
    fig.savefig(ASSETS / "ch6-aloha-csma-efficiency.png")
    plt.close(fig)


def make_fig_ch7_wireless_mobile() -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.4, 3.5))

    # Left: Hidden terminal + 802.11 RTS/CTS timeline
    ax1.set_xlim(0, 10); ax1.set_ylim(0, 10); ax1.axis("off")
    ax1.set_title("Hidden Terminal & 802.11 RTS/CTS", fontsize=9.5)
    # Coverage ovals
    ax1.add_patch(mpatches.Ellipse((2.8, 7.6), 4.8, 2.2, fc="#DBEAFE", ec=C_BLUE, alpha=0.45, lw=1.2))
    ax1.add_patch(mpatches.Ellipse((7.2, 7.6), 4.8, 2.2, fc="#FEE2E2", ec=C_RED, alpha=0.40, lw=1.2))
    for lbl, x, col in [("A", 1.5, C_BLUE), ("B\n(AP)", 5.0, C_NAVY), ("C", 8.5, C_RED)]:
        ax1.add_patch(plt.Circle((x, 7.6), 0.62, fc="white", ec=col, lw=1.5, zorder=4))
        ax1.text(x, 7.6, lbl, ha="center", va="center", fontsize=7.0, weight="bold", color=col, zorder=5)
    ax1.text(5.0, 9.25, "A & C cannot hear each other -> collide at B!", ha="center", fontsize=7.5, color=C_RED, weight="bold")

    y0 = 4.6
    draw_box(ax1, 0.2, y0, 1.0, 0.9, "DIFS", fc="#F1F5F9", ec=C_SLATE, fontsize=6.8)
    draw_box(ax1, 1.25, y0, 1.25, 0.9, "RTS(A)", fc="#DBEAFE", ec=C_BLUE, fontsize=6.9, weight="bold")
    draw_box(ax1, 2.55, y0, 0.72, 0.9, "SIFS", fc="#F1F5F9", ec=C_SLATE, fontsize=6.3)
    draw_box(ax1, 3.32, y0, 1.25, 0.9, "CTS(B)", fc="#DCFCE7", ec=C_GREEN, fontsize=6.9, weight="bold")
    draw_box(ax1, 4.62, y0, 0.72, 0.9, "SIFS", fc="#F1F5F9", ec=C_SLATE, fontsize=6.3)
    draw_box(ax1, 5.39, y0, 2.5, 0.9, "DATA (A -> B)", fc="#FEF3C7", ec=C_AMBER, fontsize=7.2, weight="bold")
    draw_box(ax1, 7.94, y0, 0.72, 0.9, "SIFS", fc="#F1F5F9", ec=C_SLATE, fontsize=6.3)
    draw_box(ax1, 8.71, y0, 1.08, 0.9, "ACK", fc="#DCFCE7", ec=C_GREEN, fontsize=7.0, weight="bold")

    draw_box(ax1, 1.5, 2.4, 8.2, 1.15, "Node C hears CTS(B) -> sets NAV (defers until ACK done)", fc="#FEE2E2", ec=C_RED, fontsize=6.4)
    ax1.annotate("", xy=(3.95, 3.6), xytext=(3.95, 4.55), arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.3))
    ax1.text(5.0, 1.1, "Key: RTS/CTS are short; data collisions avoided once CTS heard by all!", ha="center", fontsize=7.1, color=C_NAVY)

    ax2.set_xlim(0, 10); ax2.set_ylim(0, 10); ax2.axis("off")
    ax2.set_title("Mobile IP: Indirect (Triangle) vs. Direct", fontsize=9.5)
    draw_box(ax2, 0.25, 6.7, 3.25, 1.65, "Correspondent\n(sends to perm IP)", fc="#EFF6FF", ec=C_BLUE, fontsize=7.0)
    draw_box(ax2, 6.25, 6.7, 3.5, 1.65, "Home Agent (HA)\nin Home Network", fc="#FEF3C7", ec=C_AMBER, fontsize=7.0, weight="bold")
    draw_box(ax2, 2.3, 1.35, 5.4, 1.85, "Foreign Agent (FA) + Mobile\nCare-of-Address (COA)", fc="#DCFCE7", ec=C_GREEN, fontsize=7.0, weight="bold")

    ax2.annotate("", xy=(6.2, 7.7), xytext=(3.55, 7.7), arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.6))
    ax2.text(4.88, 8.2, "1. to perm IP", ha="center", fontsize=7.2, color=C_RED)
    ax2.annotate("", xy=(6.5, 3.25), xytext=(7.8, 6.65), arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.6))
    ax2.text(8.15, 4.9, "2. tunnel\nto COA", ha="center", fontsize=7.2, color=C_RED)
    ax2.annotate("", xy=(1.8, 6.65), xytext=(3.5, 3.25), arrowprops=dict(arrowstyle="->", color=C_GREEN, lw=1.6))
    ax2.text(1.45, 4.8, "3. direct\nreply", ha="center", fontsize=7.2, color=C_GREEN)

    ax2.annotate("", xy=(4.4, 3.25), xytext=(2.45, 6.65), arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=1.5, ls="--"))
    ax2.text(4.35, 5.1, "Direct\n(to COA)", ha="center", fontsize=7.2, color=C_BLUE, weight="bold")
    ax2.text(5.0, 0.45, "Indirect: transparent, triangle routing | Direct: no triangle, needs Anchor FA",
             ha="center", fontsize=6.9, color=C_NAVY)

    fig.tight_layout()
    fig.savefig(ASSETS / "ch7-hidden-terminal-rtscst.png")
    plt.close(fig)


def main() -> None:
    verify_ch3p3()
    verify_ch4()
    verify_ch5()
    verify_ch6()
    verify_ch7()
    verify_final_2021a()

    make_fig_ch3p3_cwnd()
    make_fig_ch3p3_handshake()
    make_fig_ch4_frag_nat()
    make_fig_ch5_dijkstra()
    make_fig_ch5_dv_bgp()
    make_fig_ch6_aloha_switch()
    make_fig_ch7_wireless_mobile()

    OUT_JSON.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"CS5222 Part 2 verification PASSED: {checks} assertions, 7 original PNGs generated!")


if __name__ == "__main__":
    main()
