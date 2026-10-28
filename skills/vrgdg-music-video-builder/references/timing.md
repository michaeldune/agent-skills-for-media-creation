# Lyric timing and cuts

The wizard's transcription decides where every scene starts. On "Upload If Found" it was wrong in four ways:

1. Three cuts sat exactly on a vocal entry. The first syllable was sung before the mouth could open ("we miss her
   enunciating 'up'").
2. One 12 s scene held a line, a keyboard interlude, a second line and a scream, labelled as one line. The singer
   mouthed the interlude.
3. An instrumental stretch carried a lyric label.
4. One line began 1.1 s before its cut, so its first words fell under the previous shot.

## Find them before rendering

Run demucs once on the song, then:

`python scripts/vocal_cut_strip.py <project_folder> <vocals.wav>`

Each row shows one second either side of a cut in 50 ms cells: `#` vocal, `+` faint, `.` silent, `|` the cut.

- `.......|####` with the vocal starting within about 100 ms after the cut: move the cut earlier.
- `####|####` is a cut inside continuous singing: usually fine, the line carries across.
- `....|....` for a scene labelled with a lyric: the label is wrong; treat it as instrumental.
- The script also lists silent gaps longer than 2 s inside scenes marked as sung: those scenes need splitting.

Give the user the flagged list with times. WhisperX and stable-ts are unreliable on sustained notes, screams and background
vocals (one heard "Upload if found" as "Unload and found" and reduced a 5 s scream to a single stray word). The user's ear
decides; ask them what an unclear stretch is and which instrument plays a break.

## Timing lines you already have the words for

When the lyrics are known, FORCE-ALIGN them to the vocal stem instead of transcribing and matching words. In one test,
`whisperx.align` on the demucs vocal stem placed all 115 words of a 100 s song in 9 s on CPU, at 0.14 s mean error
against clip-confirmed line starts; a transcribe-then-match script was 1-3 s out on three lines because it anchored on a
common word.

- Align ONE LINE PER WINDOW, each window starting after the previous line's last word. A single long segment drifted
  3.15 s on one line while staying within 0.25 s elsewhere; windowed, it scored 0.10 s mean, 0.15 s worst.
- Two checks that need no ear: line starts must strictly increase, and the smallest gap between consecutive line starts
  must be plausible (a line starting before the one above it, or 0.3 s after it, is an aligner failure).
- Separating the stem buys COVERAGE, not accuracy: it found every line where the mix missed some, but did not make the
  found ones more precise. Separate when lines go missing, not when they are merely mistimed.
- Transcription is still the right tool for the other question: WHETHER the singer sang the written words.
- Do not move a line into a loud stretch the transcriber left untranscribed: that stretch may be wordless vocalising.

## Times taken by ear

A time someone calls out while listening to the whole song carries reaction latency: in one test the by-ear line starts
ran 0.5-1.1 s later than the onsets measured on the vocal stem, because a listener marks the first intelligible word and
a recogniser the first vocal sound. Treat a by-ear time as plus or minus a second. To check a disputed line without that
latency, cut a clip that starts exactly at the claimed time and ask whether it opens on the word or before it; those
readings matched the recognisers to a tenth of a second.

## Move a cut

Pick a time about 0.4 s before the vocal onset, inside the silent gap, on a 1/24 s frame boundary. Change three fields in
the session file: the left scene's `end`, the right scene's `start` and `custom_audio_timeline_start`. Reload the page,
re-render BOTH scenes (their lengths changed), stitch, check.

Both neighbours are re-rolled, so a cutaway the user already liked may come back different. Tell them before you do it.

## Split a scene

The scissors refuse a scene that already has a render, so split by hand. `references/split_scene_example.py` is the
worked example. In order:

1. Back up the session file.
2. Rename the clip and thumbnail files of every LATER scene up by the number of scenes you are inserting, highest first.
   Clips are named by scene number.
3. For those later scenes fix `video_path`, `video_source_path`, `video_thumbnail_path`, and rewrite `video_history` and
   `video_thumbnail_history` so the current file is the entry `video_history_index` points at. The stitch plays the
   history entry, not `video_path`.
4. Insert the new segments (deep copies with new `seg_<uuid>` ids), set times, lyric, lip-sync flags and prompts, blank
   their video fields, and add their entries to `subject_scene_map` and `scene_map`.
5. Relabel all scenes in order. Assert every scene's `end` equals the next scene's `start`.
6. Reload, render the new scenes, stitch, run `check_stitch.py`. A frame count that differs from the song means wrong
   clips somewhere.
