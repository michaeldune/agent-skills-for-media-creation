# Camera, lens and capture words on H3

What H3 does with cinematography vocabulary: focal lengths, camera gear,
phone footage, selfie framing. Each line below was rendered, not assumed.

Test (2026-11-24): one cafe scene (a woman sipping coffee by a rainy window),
text to video, 864x480, 5 s, two seeds, on a 2-step distilled H3 checkpoint,
with the lock wording repeated on an 8-step one. Camera motion was measured as
the median optical-flow path over the clip; framing and gear were judged from
contact sheets. One scene and two seeds: treat these as strong hints, not law.

## What works

- **Locking the frame.** "Locked-off composition, medium close-up ..., fixed
  camera, no reframing." held to 1-3 px of drift over 5 s on both checkpoints,
  with or without the word "tripod". "The frame never moves: no pan, no
  push-in, no reframing" by itself crept and pushed in by 14-38 px. Lead with
  the lock wording; the "never moves" list after it is harmless.
- **Selfie view: use the trade term.** "Front-facing smartphone selfie-style
  cinematography: arm's-length framing, eye-level phone position, phone-wide
  lens perspective, mild natural hand sway" gave a real selfie viewpoint (her
  arm reaching to the lens at the frame edge) on one seed and lens eye contact
  without the arm on the other.

## What does nothing, or backfires

- **Focal lengths.** "24mm wide-angle lens look, the camera close" and "85mm
  portrait-lens look, the camera several metres away, the background softly
  compressed" gave the same field of view and the same background blur. Any
  extra words reshuffle the sample, so a lens cue can look like it did
  something on one seed; it did not hold across two. Describe what the picture
  shows (how much of her, how blurred the street) instead.
- **Gear words are not drawn and change nothing alone.** "Tripod", "rear-camera
  smartphone" and "phone" produced no tripod or phone in frame. "The camera on
  a tripod" alone held the frame only loosely (about 2 px); the lock wording
  above is what holds it.
- **"Handheld ... smartphone footage, small operator adjustments" adds no
  shake.** Jitter matched the plain control.
- **"Shake Slightly" adds no shake either; "shakes strongly" does.** Tested on
  the 2-step checkpoint, same scene and seeds: "the camera shakes slightly
  throughout the shot" and "Camera move: Shake Slightly." both gave
  frame-to-frame jitter of 0.06-0.08 (plain control 0.10, locked-off 0.01),
  with less drift than the control (8-15 px vs 29-30 px), so they read as a
  near-still camera. "The camera shakes strongly throughout the shot" gave
  jitter 0.43 on both seeds (four times the control) and a wandering
  86-116 px path, a visible handheld wobble, with the picture and the action
  intact. For a handheld look, write "shakes strongly"; there is no tested
  middle setting yet.
- **Plain-words selfie draws the phone.** "She holds her phone out at arm's
  length and films herself; the picture is what that phone's front camera
  sees" rendered a third-person shot of a woman holding a phone, on both
  seeds, and one pushed in by over 100 px. Describing the device makes H3 put
  the device in the picture.
- **Shot size on text to video.** "Medium close-up from the chest up" was
  ignored in every arm: each opened seated, waist-up. See the tight-shot note
  in SKILL.md Step 3 for what did work.

Not tested: image to video and Ref2VA, where a reference picture sets the
framing.
