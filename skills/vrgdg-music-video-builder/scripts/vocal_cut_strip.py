"""Show where the vocal sits around every scene cut, and find silent gaps inside sung scenes.

Usage: python vocal_cut_strip.py <project_folder> <vocals.wav> [session.json]
  vocals.wav = the demucs vocal stem of the project song, e.g.
    python -m demucs --two-stems vocals -o <out_dir> <project_folder>/project_audio/project_audio.mp3

Each row: one second either side of a cut in 50 ms cells.  # vocal   + faint   . silent   | the cut
Flags:
  ONSET AT CUT   silence before the cut and vocal within 100 ms after it -> move the cut ~0.4 s earlier
  NO VOCAL       a scene labelled with a lyric that has almost no vocal -> label is wrong, treat as instrumental
  GAP            a silent stretch over 2 s inside a sung scene -> the scene probably needs splitting
  LATE CUT       vocal starts in the last 1.5 s of the previous scene after a silence -> the line begins before its cut
This shows where singing is, not what is sung. the user's ear decides.
"""
import json, re, sys
import av
import numpy as np

if len(sys.argv) < 3:
    sys.exit(__doc__)
P = sys.argv[1].rstrip("/\\") + "/"
SR = 44100
c = av.open(sys.argv[2])
rs = av.AudioResampler(format="flt", layout="mono", rate=SR)
v = np.concatenate([x.to_ndarray()[0] for f in c.decode(audio=0) for x in rs.resample(f)])
SESSION = sys.argv[3] if len(sys.argv) > 3 else P + "vrgdg_builder_session.json"
segs = json.load(open(SESSION, encoding="utf-8"))["segments"]
CELL = 0.05


def db(t, w=CELL):
    s = v[max(0, int(t * SR)):int((t + w) * SR)]
    return -99.0 if len(s) == 0 else 20 * np.log10(np.sqrt((s ** 2).mean()) + 1e-9)


def sym(t):
    d = db(t)
    return "#" if d > -30 else ("+" if d > -42 else ".")


def mmss(t):
    return "%d:%04.1f" % (int(t // 60), t % 60)


def instrumental(g):
    return "instrumental" in str(g.get("lyric_text", "")).lower() or not str(g.get("lyric_text", "")).strip()


flags = []
for n, g in enumerate(segs, start=1):
    cut = float(g["start"])
    row = "".join(sym(t) for t in np.arange(cut - 1.0, cut + 1.0 - 1e-9, CELL))
    before, after = row[:20], row[20:]
    notes = []
    sung = not instrumental(g) and not g.get("lyric_no_lip_sync")
    if n > 1 and sung and before[-6:].count("#") == 0 and "#" in after[:3]:
        notes.append("ONSET AT CUT")
    if n > 1 and sung:
        tail = "".join(sym(t) for t in np.arange(cut - 1.5, cut - 1e-9, CELL))
        m = re.search(r"\.{4,}[+#]*#{3,}[+#]*$", tail)
        if m and "ONSET AT CUT" not in notes:
            notes.append("LATE CUT (vocal starts %.2f s before it)" % ((len(tail) - m.end() + len(m.group(0).lstrip("."))) * CELL))
    cells = np.arange(float(g["start"]), float(g["end"]) - 1e-9, CELL)
    loud = np.array([db(t) > -30 for t in cells])
    if not instrumental(g) and len(loud) and loud.mean() < 0.05:
        notes.append("NO VOCAL")
    if sung and len(loud):
        on = np.where(loud)[0]
        if len(on):
            inner = loud[on[0]:on[-1] + 1]
            best, cur, cur_start, best_start = 0, 0, 0, 0
            for i, x in enumerate(inner):
                if not x:
                    if cur == 0:
                        cur_start = i
                    cur += 1
                    if cur > best:
                        best, best_start = cur, cur_start
                else:
                    cur = 0
            if best * CELL > 2.0:
                t0 = float(g["start"]) + (on[0] + best_start) * CELL
                notes.append("GAP %.1f s from %s" % (best * CELL, mmss(t0)))
    line = "scene %2d  cut %-7s %s|%s  %s" % (n, mmss(cut), before, after, str(g.get("lyric_text", ""))[:34])
    if notes:
        line += "   <-- " + ", ".join(notes)
        flags.append((n, mmss(cut), notes))
    print(line)
print("\n%d flagged:" % len(flags))
for n, t, notes in flags:
    print("  scene %d at %s: %s" % (n, t, ", ".join(notes)))
