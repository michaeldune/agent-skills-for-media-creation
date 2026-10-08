"""Verify a Builder stitch against the song and the timeline.

Usage: python check_stitch.py <project_folder> <stitch.mp4> [fps]
  project_folder  e.g. <ComfyUI output folder>/<project>
  stitch.mp4      file name inside the project folder, or a full path

Checks: frame count vs song length, audio vs project_audio (5 s windows, lag search +-100 ms), and for every scene
whether its clip's first frame lands on its timeline start frame. Exit code 1 if anything is off.
Run with a Python that has `av` and `numpy` (the ComfyUI venv does).
"""
import glob, json, os, sys
import av
import numpy as np

if len(sys.argv) < 3:
    sys.exit(__doc__)
P = sys.argv[1].rstrip("/\\") + "/"
F = sys.argv[2] if os.path.isabs(sys.argv[2]) else P + sys.argv[2]
FPS = float(sys.argv[3]) if len(sys.argv) > 3 else 24.0
SR = 44100


def mono(path):
    c = av.open(path)
    r = av.AudioResampler(format="flt", layout="mono", rate=SR)
    return np.concatenate([x.to_ndarray()[0] for f in c.decode(audio=0) for x in r.resample(f)])


def gray(path, first_only=False):
    out = []
    for f in av.open(path).decode(video=0):
        out.append(f.to_ndarray(format="gray")[::4, ::4].astype(np.float32))
        if first_only:
            break
    return out


songs = glob.glob(P + "project_audio/project_audio.*")
if not songs:
    sys.exit("no project_audio/project_audio.* in " + P)
song = mono(songs[0])
frames = gray(F)
a = mono(F)
bad = []
print("stitched: %d frames = %.3f s | audio %.3f s | song %.3f s" % (len(frames), len(frames) / FPS, len(a) / SR, len(song) / SR))

res = []
for t in range(0, int(len(a) / SR) - 5, 5):
    x = a[t * SR:(t + 5) * SR]
    best = max((np.corrcoef(x, song[t * SR + l:(t + 5) * SR + l])[0, 1], l)
               for l in range(-4410, 4411, 49) if t * SR + l >= 0 and (t + 5) * SR + l <= len(song))
    res.append((best[0], best[1] / SR * 1000))
min_r, max_lag = min(r for r, _ in res), max(abs(l) for _, l in res)
print("audio vs song, 5 s windows: min r=%.3f, max |lag| %.0f ms" % (min_r, max_lag))
if min_r < 0.9 or max_lag > 25:
    bad.append("audio does not match the song")

segs = json.load(open(P + "vrgdg_builder_session.json", encoding="utf-8"))["segments"]
expected = int(round(float(segs[-1]["end"]) * FPS))
if abs(len(frames) - expected) > 2:
    bad.append("frame count %d, timeline expects about %d: wrong or missing clips" % (len(frames), expected))
worst = 0
for n, g in enumerate(segs, start=1):
    hist, idx = g.get("video_history") or [], g.get("video_history_index", -1)
    clip = hist[idx] if hist and 0 <= idx < len(hist) else (g.get("video_path") or P + "rendered_scene_videos/video_%04d-audio.mp4" % n)
    numbered = "video_%04d-audio.mp4" % n
    note = "" if os.path.basename(clip) == numbered else "  <-- plays %s" % os.path.basename(clip)
    if not os.path.exists(clip):
        bad.append("scene %d: clip missing (%s)" % (n, clip))
        print("scene %2d: CLIP MISSING %s" % (n, clip))
        continue
    first = gray(clip, first_only=True)[0]
    want = int(round(float(g["start"]) * FPS))
    lo, hi = max(0, want - 12), min(len(frames), want + 13)
    d = [np.abs(frames[i] - first).mean() for i in range(lo, hi)]
    if not d:
        bad.append("scene %d: start frame beyond the stitch" % n)
        continue
    got = lo + int(np.argmin(d))
    worst = max(worst, abs(got - want))
    flag = ""
    if got != want or min(d) > 5:
        flag = "  <-- CHECK"
        bad.append("scene %d: offset %+d frames, match diff %.1f" % (n, got - want, min(d)))
    print("scene %2d: start frame %5d, found %5d (%+d), diff %.1f%s%s" % (n, want, got, got - want, min(d), flag, note))
print("worst picture offset: %d frames = %.0f ms" % (worst, worst / FPS * 1000))
if bad:
    print("\nFAILED:\n  " + "\n  ".join(bad))
    sys.exit(1)
print("\nOK: length, audio and all %d scene starts match." % len(segs))
