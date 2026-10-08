---
name: vrgdg-music-video-builder
description: Make or fix a lip-synced music video with the VRGDG Music Video Builder (comfyui-vrgamedevgirl) on vanilla ComfyUI with MiniMax H3. Use when the user asks for a music video from a song, names the Music Video Builder, VRGDG or vrgamedevgirl, or reports faults in a Builder video such as a missed first syllable at a cut, a singer mouthing an instrumental break, an instrument at the wrong size or height, glass or smoke artifacts, or the same performer on screen too long. Covers scene prompts, performer rotation, checking cuts against the vocal stem, driving the Builder page, splitting scenes, and verifying the stitch.
---

# VRGDG Music Video Builder

The Builder renders one clip per lyric line with the song locked in, then stitches them. Its stitch is exact. Its two weak
points are the ones you must cover: scene prompts and lyric timing. Write the prompts yourself and check every cut against
the vocal stem before rendering.

Learned on one full song (4:15, 53 scenes), October 2026, on an RTX 4070 Ti 12 GB with 32 GB of RAM. Times and
settings below are from that machine.

## Before you start

- Keep one folder per song: the song file, `lyrics.txt`, the style and negative prompts, the performer and location
  reference images, and a `video-notes.md` that records who sings backup, what the user settled by ear, and where the
  Builder project lives. Ask the user where that folder is, read `video-notes.md` first and add to it, use `lyrics.txt`
  as the lyric source of truth when checking the transcription, and copy the final video back into that folder when done.
- Needs the comfyui-vrgamedevgirl node pack (the Builder) and ComfyUI-KJNodes in a plain ComfyUI install, plus the
  MiniMax H3 reference-to-video model, text encoder and VAEs.
- Use a plain ComfyUI server, not an app's bundled engine such as SimpliGen's. Ask the user to start it in their own
  terminal with `--lowvram` and a known `--output-directory` (a server started by the agent may be stopped when the
  agent's session ends), for example:
  `python main.py --listen 127.0.0.1 --port 8188 --disable-auto-launch --lowvram --output-directory <output folder>`
- Check nothing else is generating on the same GPU. Two H3 jobs at once starve 32 GB of RAM.
- Render settings that worked: `minimax_h3_ref2va_pruned_int8_convrot`, TaoMate 3-step LoRA at 1.0, euler/simple, 3 steps,
  0.9 MP, text encoder `qwen3vl_32b_minimax_h3_nvfp4_awq`, video VAE fp16, audio VAE fp32. Below 0.9 MP small faces distort.
- Budget: about 2.5 min per 5 s scene. A 7.8 s scene took 10 min and a 12 s scene 17-21 min. Keep scenes under about 6.5 s.

## Workflow

1. **Transcribe** with the wizard (needs `demucs`, `stable-ts`, `openai-whisper` in the venv).
2. **Check timing before any render.** Run `scripts/vocal_cut_strip.py`. Fix what it flags and show the user the list.
   His ear decides every boundary. Read `references/timing.md`.
3. **Plan the shot list.** Pick a shot type for every scene from the table in `references/prompts.md` (close-up,
   medium, solo cutaway, two-shot, three-shot, over-the-shoulder, short full-band wide, instrument detail, empty room),
   keep every face that matters at about 90 px or taller, apply the rotation rules below, and show the user the
   scene-by-scene list of shot type and performers before rendering.
4. **Write every scene prompt yourself**, into the session file. Do not use the local LLM runner. Read
   `references/prompts.md` first; it has the template, the wording that worked and the fault table.
5. **Render** the batch through the page. Read `references/builder-mechanics.md` before touching the page or the session
   file.
6. **Look at every clip** with `scripts/contact_sheet.py`. Expect about one scene in five to need a second take. Rewrite
   the prompt (same seed and same prompt give a different but not better take) and re-render.
7. **Stitch** with the Builder's Stitch Preview, then run `scripts/check_stitch.py`. Send nothing that fails it.

## Performer rules

- Never more than two scenes in a row on one performer. Separate takes never match, so the cut jumps; a different
  performer hides it.
- Bring every band member back several times, as no-lip-sync cutaways over sung lines.
- A cutaway shows the musician playing for the whole shot, above all where that instrument drives the song. No flourish
  that takes a hand off the instrument.
- Two singer shots in a row: different framing and location, motion in the same direction.
- An instrumental break gets the instrument that plays it. Ask the user which one; you cannot hear it.

## What to check on every clip

1. Instrument against the body: where it sits (keyboard at waist, not collarbone) and its size (drum kit against torso).
   Check this first.
2. Is the performer playing or singing from the first frame to the last?
3. Sung scenes: the first second. The mouth should start closed and open into the line.
4. Extra objects: a second person, text on screens, smoke or glass in front of a face. A microphone on a stand beside a
   band member who sings backup is NOT a fault (see Backing vocals in `references/prompts.md`).
5. Faces at native pixels before saying anything about identity.

## Reporting

- Say what you checked on stills only. Lip sync and whether a shot fits the music are for the user to judge.
- You cannot hear the song. A vocal-stem strip shows where singing is, not what is sung or whether it is a scream.
- Give times as he sees them in the video (m:ss), with the scene number.
- After a stitch, state the audio lag and the worst scene offset from `check_stitch.py`.

## Files

- `references/prompts.md` - prompt shape, template, wording, face-size table, shot types, fault table, rules for
  scripted edits.
- `references/timing.md` - what goes wrong with cuts and how to move or split them.
- `references/builder-mechanics.md` - driving the page, session file fields, renumbering traps.
- `references/split_scene_example.py` - worked example of splitting a rendered scene in three.
- `scripts/vocal_cut_strip.py` - vocal energy around every cut.
- `scripts/contact_sheet.py` - three frames per scene.
- `scripts/check_stitch.py` - stitch length, audio lag, per-scene start frame.
