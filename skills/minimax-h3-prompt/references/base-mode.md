# T2VA / I2VA / FL2VA / L2VA — the three-field brief

Use this when there are no references, or when the only images are **frame
anchors** — the video literally begins or ends on them.

| Mode | Media | What the timeline does |
|---|---|---|
| T2VA | none | builds the whole timeline from text |
| I2VA | 1 image = first frame | develops forward from that image |
| FL2VA | 2 images = first and last | a continuous path from the first to the last |
| L2VA | 1 image = last frame | converges from a plausible earlier state onto it |

## Structure

For **T2VA**, the brief is just the three core fields. For the other three, a
fixed alignment instruction comes first, then one blank line, then the fields.

```text
integrated_multimodal_description: [Shot 1] ...
overall_soundscape: ...
non_diegetic_music: ...
```

- **integrated_multimodal_description** — visuals, actions, shots, speakers,
  dialogue, singing and diegetic audio along the timeline
- **overall_soundscape** — ambience, physical action sound, non-verbal human
  sound across the whole video
- **non_diegetic_music** — score only the audience hears (`None.` if absent)

## The alignment instruction lines

These are fixed wording. `N` is the index of the actual final shot; `S.SS` is the
effective duration to exactly two decimal places.

**I2VA:**
```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.
```

**FL2VA:**
```text
How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; Picture 2 (from Shot N) aligns with the S.SS-second mark of the target video.
```

**L2VA:**
```text
How the reference pictures align with the target video — <Picture 1> (from [Shot N]) aligns with the S.SS-second mark of the target video.
```

The instruction must be the **first line** of the prompt, followed by one blank
line before the core fields.

## Worked T2VA example

```text
integrated_multimodal_description: [Shot 1] Live-action, cinematic, a medium-wide shot frames a baker opening the shutters of a small street bakery before sunrise. The camera pushes in with small amplitude at slow speed as the middle-aged baker with a calm, slightly raspy voice (S1) places a fresh loaf on the wooden counter and says: <d>[English] First batch of the morning.</d> [Shot 2] At 00:05.000, the camera cuts to a close-up of steam rising from the sliced bread while the baker's final words carry over from the previous shot.
overall_soundscape: Wooden shutters scrape open over a quiet street as trays clink softly inside the bakery. The doorbell rings once, followed by light footsteps and the crisp sound of bread being sliced.
non_diegetic_music: A soft acoustic-guitar pattern at a moderate tempo, joined by sparse upright-bass notes and a gentle fade at the end.
```

Worth noticing in that example: the voice is characterised *outside* the `<d>`
tag ("calm, slightly raspy"), the camera move names type, amplitude and speed,
and the second shot carries the line across the cut rather than restating it.

## Camera vocabulary

Zoom In/Out · Push In/Pull Out · Pan Left/Right · Truck Left/Right ·
Tilt Up/Down · Pedestal Up/Down · Arc Shot · Tracking Shot · Static Shot ·
Shake Slightly/Strongly · POV · Roll Clockwise/Counterclockwise

Write the move as natural English action within the shot, giving motion type +
amplitude + speed where it matters — medium amplitude and normal speed can be
left unsaid. Name **one** move per shot and say what visibly changes as a result.

## On-screen text

If the shot needs legible text — a sign, a title, a screen — state it explicitly
and quote it exactly. Text is one of the least reliable things to render, so
expect to generate several takes and keep the one where it reads correctly, and
avoid making a shot depend on text that has to be perfect.
