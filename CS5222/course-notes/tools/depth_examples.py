"""Recompute the October CS5222 teaching examples; --write also emits two SVGs.

Uses only the Python standard library. No course data, sockets or experiments.
"""
from pathlib import Path
import argparse
from collections import Counter
from fractions import Fraction
import json

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'docs/reviews/cs5222-teaching-depth-2026-10-16/calculations.json'
ASSETS = ROOT / 'CS5222/course-notes/assets'
checks = []


def check(name, actual, expected):
    assert actual == expected, (name, actual, expected)
    checks.append({'name': name, 'actual': actual, 'expected': expected})


def queue_events(length_bytes, rate_bps, waiting_slots, arrivals):
    """FCFS event schedule; count the transmitting packet outside waiting slots."""
    duration = Fraction(length_bytes * 8 * 1000, rate_bps)
    completions, records = [], []
    for label, time in arrivals:
        time = Fraction(time)
        completions = [finish for finish in completions if finish > time]
        if len(completions) == waiting_slots + 1:
            records.append([label, 'dropped'])
            continue
        start = max(time, completions[-1] if completions else time)
        end = start + duration
        completions.append(end)
        records.append([label, float(start), float(end), float(start - time)])
    return records


check('Queue: four-packet burst', queue_events(1000, 8_000_000, 2,
      [(p, 0) for p in 'ABCD']),
      [['A', 0., 1., 0.], ['B', 1., 2., 1.], ['C', 2., 3., 2.], ['D', 'dropped']])
check('Queue: changed packet length/rate/capacity', queue_events(500, 2_000_000, 1,
      [(p, 0) for p in 'ABC']), [['A', 0., 2., 0.], ['B', 2., 4., 2.], ['C', 'dropped']])
check('Queue: offered traffic intensity despite one dropped packet',
      float(Fraction(4 * 8000, 1) / (8_000_000 * Fraction(10, 1000))), .4)
check('DNS: independent TTL expiry', [max(0, ttl - 90) for ttl in [300, 60]], [210, 0])
neighbors = {'P1': {'A', 'B'}, 'P2': {'A', 'B'}, 'P3': {'A', 'C'}}
def copies(active):
    counts = Counter(chunk for peer in active for chunk in neighbors[peer])
    return [counts[chunk] for chunk in 'ABC']
check('BitTorrent: visible copies before departures', copies(['P1', 'P2', 'P3']), [3, 2, 1])
check('BitTorrent: two tied rarest candidates', copies(['P1', 'P3']), [2, 1, 1])
check('BitTorrent: rarest does not create an unavailable chunk', copies(['P1']), [1, 1, 0])

# Simulate playback at 1/4-second intervals, independently of max(download-buffer,0).
for rate, expected in [(Fraction(1, 2), [2., 0., 5.]), (Fraction(1), [4., 1., 4.]),
                       (Fraction(2), [8., 5., 4.])]:
    remaining = 4 * rate  # Mbit; each segment represents four seconds.
    buffer, elapsed, stalled = Fraction(3), Fraction(0), Fraction(0)
    step = Fraction(1, 4)
    while remaining > 0:
        assert remaining >= step
        remaining -= step  # 1 Mbps throughput.
        played = min(buffer, step)
        buffer -= played
        stalled += step - played
        elapsed += step
    buffer += 4  # The whole chunk becomes available only after download.
    check(f'DASH: {float(rate)} Mbps representation',
          [float(elapsed), float(stalled), float(buffer)], expected)


def echo(first_a, first_b, payload):
    """Two endpoint byte counters, using actual ASCII payload lengths."""
    send_next = {'A': first_a, 'B': first_b}
    receive_next = {'A': first_b, 'B': first_a}
    rows = []
    for sender, receiver, data in [('A', 'B', payload), ('B', 'A', payload), ('A', 'B', b'')]:
        rows.append([sender + '->' + receiver, send_next[sender], receive_next[sender], len(data)])
        assert send_next[sender] == receive_next[receiver]
        receive_next[receiver] += len(data)
        send_next[sender] += len(data)
    return rows, send_next['A']


for label, a, b, payload, expected in [
    ('Classroom Telnet', 42, 79, b'C',
     [['A->B', 42, 79, 1], ['B->A', 79, 43, 1], ['A->B', 43, 80, 0]]),
    ('Independent two-byte echo', 1000, 5000, b'OK',
     [['A->B', 1000, 5000, 2], ['B->A', 5000, 1002, 2], ['A->B', 1002, 5002, 0]])]:
    rows, next_byte = echo(a, b, payload)
    check(label + ': all transmitted fields', rows, expected)
    check(label + ': pure ACK does not consume sequence space', next_byte, a + len(payload))

# Compare a cumulative prefix with a selectively acknowledged set.
received_acks, base, bases = set(), 0, []
for ack in [0, 2, 3, 1]:
    received_acks.add(ack)
    while base in received_acks:
        base += 1
    bases.append(base)
check('SR base after ACK0, ACK2, ACK3, ACK1', bases, [1, 1, 1, 4])
check('GBN base after cumulative ACK0 then ACK2', [ack + 1 for ack in [0, 2]], [1, 3])

# A finite duplicate-delivery trace, not a proof for arbitrary channel histories.
expected_seq, delivered, replies = 0, [], []
for seq, data in [(0, 'A'), (0, 'A'), (1, 'B')]:
    if seq == expected_seq:
        delivered.append(data)
        expected_seq = 1 - expected_seq
    replies.append(1 - expected_seq)
check('rdt2.2 receiver: retransmitted A is not delivered twice', delivered, ['A', 'B'])
check('rdt2.2 receiver: feedback after new/duplicate/new packets', replies, [0, 0, 1])


def svg(body, width, height):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<title>CS5222 teaching diagram</title>
<defs><marker id="arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0 0 L10 4 L0 8 Z" fill="#1e3344"/></marker></defs>
<rect width="100%" height="100%" fill="white"/>
<g font-family="Arial, sans-serif" font-size="30" fill="#15222c">{body}</g></svg>\n'''


def text(x, y, lines, size=30):
    return f'<text x="{x}" y="{y}" text-anchor="middle" font-size="{size}">' + ''.join(
        f'<tspan x="{x}" dy="{0 if i == 0 else 38}">{line}</tspan>' for i, line in enumerate(lines)) + '</text>'


def path(d, dashed=False):
    dash = ' stroke-dasharray="12 9"' if dashed else ''
    return f'<path d="{d}" fill="none" stroke="#1e3344" stroke-width="4" marker-end="url(#arrow)"{dash}/>'


def figures():
    body = ''
    for x, y, label in [(250, 160, ['Ready for', 'data 0']), (930, 160, ['Wait for', 'ACK0']),
                        (930, 550, ['Ready for', 'data 1']), (250, 550, ['Wait for', 'ACK1'])]:
        body += f'<ellipse cx="{x}" cy="{y}" rx="145" ry="70" fill="#f3f6f8" stroke="#1e3344" stroke-width="3"/>'
        body += text(x, y - 10, label)
    body += path('M395 160 L780 160') + text(590, 87, ['new data /', 'save and send packet 0'], 28)
    body += path('M930 230 L930 474') + text(720, 345, ['valid ACK0 /', 'complete packet 0'], 28)
    body += path('M785 550 L402 550') + text(590, 615, ['new data /', 'save and send packet 1'], 28)
    body += path('M250 480 L250 238') + text(460, 345, ['valid ACK1 /', 'complete packet 1'], 28)
    body += path('M1060 130 C1220 30 1230 300 1060 205')
    body += text(1115, 315, ['bad ACK', 'or ACK1 /', 'resend 0'], 27)
    body += path('M120 580 C-35 690 -35 415 120 510')
    body += text(100, 340, ['bad ACK', 'or ACK0 /', 'resend 1'], 27)
    body += text(640, 730, ['rdt2.2 sender: event / action; successful ACK enables the next application call'], 25)
    sender = svg(body, 1280, 770)
    body = text(190, 50, ['Host A', 'next data byte: 42']) + text(1010, 50, ['Host B', 'next data byte: 79'])
    body += '<path d="M190 115 V660 M1010 115 V660" stroke="#727b82" stroke-width="3"/>'
    body += path('M190 160 L1010 255') + text(600, 145, ['1. Seq=42, ACK=79, 1 byte: C'], 30)
    body += path('M1010 340 L190 435') + text(600, 325, ['2. Seq=79, ACK=43, 1 byte: C'], 30)
    body += path('M190 515 L1010 610', True) + text(600, 500, ['3. Seq=43, ACK=80, 0 bytes'], 30)
    body += text(600, 710, ['Already established; no other data, SYN or FIN. Time runs downward.'], 26)
    return {'chapter03-rdt22-fsm.svg': sender, 'chapter03-telnet.svg': svg(body, 1200, 750)}


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--write', action='store_true', help='Write computed report and teaching figures')
args = parser.parse_args()
report = {'status': 'passed', 'scope': 'Teaching examples and finite event traces; no network experiment or general protocol proof',
          'checks': checks}
if args.write:
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    for name, content in figures().items():
        (ASSETS / name).write_text(content)
else:
    assert json.loads(OUT.read_text()) == report, 'Saved calculation report is stale'
    for name, content in figures().items():
        assert (ASSETS / name).read_text() == content, name + ' is stale'
print(f'Passed {len(checks)} CS5222 calculation/event checks; figures match their generator.')
