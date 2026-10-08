"""Contact sheets of Builder scene clips for review.

Usage: python contact_sheet.py <project_folder> <out.jpg> <scene> [<scene> ...] [--first]
  default  three frames per scene at 10 / 50 / 90 percent, half resolution, one row per scene
  --first  six frames from the first second of each scene (to see a sung line start: mouth closed, then opening)
Use at most four scenes per sheet so faces stay readable. Check instrument height and size against the body first.
Half resolution is not enough for identity claims: crop faces at native pixels for that.
Run with a Python that has `av`, `cv2` and `numpy` (the ComfyUI venv does).
"""
import sys
import av
import cv2
import numpy as np

args = [a for a in sys.argv[1:] if a != "--first"]
first = "--first" in sys.argv
if len(args) < 3:
    sys.exit(__doc__)
P = args[0].rstrip("/\\") + "/rendered_scene_videos/video_%04d-audio.mp4"
rows = []
for n in [int(x) for x in args[2:]]:
    c = av.open(P % n)
    fr = [f.to_ndarray(format="bgr24") for f in c.decode(video=0)]
    c.close()
    if first:
        pick = [fr[min(i, len(fr) - 1)] for i in (0, 4, 8, 12, 16, 22)]
        w = 320
    else:
        pick = [fr[int(len(fr) * t)] for t in (0.1, 0.5, 0.9)]
        w = 640
    h = int(round(w * fr[0].shape[0] / fr[0].shape[1]))
    row = np.hstack([cv2.resize(f, (w, h)) for f in pick])
    cv2.putText(row, "scene %d  %d frames" % (n, len(fr)), (8, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    rows.append(row)
cv2.imwrite(args[1], np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 88])
print("wrote", args[1])
