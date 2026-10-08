# Scene prompts for the Builder (MiniMax H3 reference-to-video, locked audio)

## Shape

Six sections, each exactly once, in this order. The Builder checks the subject definitions against the scene's mapped
references at render time and refuses a mismatch, so name the performers in mapping order and the location last.

```
subject_definitions:
<Subject 1> is the {performer} in <Picture 1>; <Picture 1> is the visual authority for character identity, face, hair, clothing, and body-proportion reference.
<Subject 2> is the environment in <Picture 2>, used as environment, location, architecture, layout, and atmosphere reference: {location description}
<Audio 1> is the complete synchronized song and vocal track for the target video, reused as the target video's complete final soundtrack and timing reference.

summary:
[reference generation + audio reuse] The target video is a {style} scene featuring <Subject 1> ({performer}) and <Subject 2> (environment). <Audio 1> is reused as the complete soundtrack and timing reference.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - reference identity, face, hair, wardrobe, and accessories remain consistent.
<Subject 2> (appears in [Shot 1]): fully_preserved - the location and its reference identity remain consistent.
<Audio 1>: fully_copy - <Audio 1> is reused 1:1 as the target video's complete final audio track.

detailed_description:
The target video is in a {style} music-video style.

[Shot 1] {shot text}

overall_soundscape:
<Audio 1> remains the sole complete audience-facing soundtrack with its original mix, timing, vocals, music, and dynamics intact.

non_diegetic_music:
<Audio 1> is reused as the complete audience-facing song/music track.
```

Two performers in one shot: `<Subject 2> is the {performer} in <Picture 2>, used as character identity, face, hair,
clothing, and body-proportion reference: {description}` and the environment becomes Subject 3 / Picture 3.

Per segment also set: `minimax_h3_mode = "reference_to_video"`, `video_prompt_type = "rtv"`,
`minimax_h3_prompt_origin = "manual"`, `lyric_no_lip_sync` (true for cutaways), `lyric_singers` (`["singer"]` or `[]`),
and delete `minimax_h3_prompt_reference_binding`.

## Shot text that worked

Write plain, positive description. Use none of "no", "not", "never", "without" outside the lyric tag.

Singer, lip-synced:

> A medium close-up of <Subject 1>, alone in the frame, standing still in {place}. She holds the silver handheld microphone
> in her right hand at her lips, and her left arm hangs at her side below the frame. The camera holds steady at her eye
> level. She sings {manner}, her eyes on the camera, her lips and jaw forming every word:
> <d>[English] {lyric line}</d> {what she does when the line ends}. The air is clear and still. The image is clean and
> sharp. {palette and light}.

Cutaway, playing:

> A waist-up shot of <Subject 1>, alone in the frame, seen from {angle}. He stands upright at a full-size black keyboard
> on a stand at the height of his waist, with {background} behind him. His arms reach down to the keys. {what the hands
> play}, from the first frame to the last. His mouth is closed and still and his eyes are on {hands}. The camera holds
> steady. The air is clear and still. The image is clean and sharp. {palette and light}.

Rules behind those templates:

- "alone in the frame" on every single-performer shot.
- The lyric inside `<d>[English] ...</d>` must match the scene's `lyric_text` word for word. Assert it in the script.
- Claim the time after the line with an event ("She closes her lips and opens her eyes"). Unclaimed time fills with
  invented singing.
- A scream or wordless hold is an action described after the lyric tag, never inside it.
- Close-ups are for faces only. If the instrument must be seen, frame waist-up or wider and state its height and size.
- Drum kit: "a full-size black drum kit: the large kick drum stands on the floor in front of her, the snare drum is at the
  height of her knees, and the cymbals are on tall stands at the height of her shoulders".
- Vary framing, angle and location between a performer's shots; keep the camera move simple (hold, slow push-in, slow arc).

## Face size decides face quality

Measured on "Baked Into the Bone" (1056x608, one model, one set of settings, one mid-shot frame from each of 9 shots,
40 faces), face height in native pixels:

| Face height | Result |
|---|---|
| under about 45 px | mush: smeared eyes, melted mouths |
| about 65 px | recognisable but soft |
| about 95 px | clean |
| 150 px and up | sharp |

Distorted faces are a pixel budget problem, not a model fault. A full-body five-piece wide at 1056x608 puts faces at
17-45 px; at 1280x736 that is still only about 20-55 px. Plan shots so every face that matters is at least about 90 px
tall: waist-up, three-shots with the others close behind, over-the-shoulder. Use a full-band full-body wide only as a
short establishing shot where faces do not need to read. Measure with YuNet at native pixels before judging identity.

## Shot types

Plan the shot list from this vocabulary before writing prompts. "UIF" = proven in the Builder on "Upload If Found".
"BITB" = seen working in "Baked Into the Bone" (a different pipeline, same model); try one before relying on it in the
Builder, because it needs more reference pictures in one scene than we have rendered there.

| Shot | What is in frame | Face size | Status | Use it for |
|---|---|---|---|---|
| Singer close-up | Head and shoulders, mic at lips | 150 px and up | UIF | Sung lines; the strongest lip sync |
| Singer medium / waist-up | Waist up, mic at lips | about 100-150 px | UIF | Sung lines, variety against the close-up |
| Solo cutaway | One band member waist-up, playing, instrument at its real height | about 100 px and up | UIF | Over sung lines and instrumental breaks |
| Two-shot | Two band members side by side, both playing | about 60-100 px | UIF (scenes 3, 20) | Intros and breaks; rhythm section together |
| Three-shot | Singer in the center, two band members beside her at the same distance | 100-250 px at 1280x736 | Builder-tested once (see below) | Sung lines; keeps the band present while she sings |
| Over-the-shoulder | Singer facing camera past a band member's shoulder and instrument neck | singer about 170-180 px at 1280x736, the other is a back | Builder-tested once (see below) | Sung lines; depth; hides one face completely |
| Full-band wide | All five head to toe on the shared stage | 17-45 px, mush | BITB | Establishing only: intro, chorus entry, final shot. Keep it short |
| Instrument detail | Hands on keys, strings or sticks, face out of frame on purpose | none | BITB | Breaks; a face-free way to show an instrument |
| Empty room / rack detail | The location with nobody in it | none | BITB | First and last shots, breathers between sections |

Planning rules:

- Decide the stage first: where each performer stands in the one room. The three-shot, over-the-shoulder and wide only
  read as one performance if everyone keeps the same place in all of them.
- For sung lines alternate singer close-up or medium with a three-shot or over-the-shoulder, and put solo cutaways on
  the lines in between. This satisfies the rotation rule and keeps the band visible.
- Backing vocals differ per song: read `video-notes.md` in the song's folder, and if it does not say, ask the user which
  band members sing backup and write the answer there (Baked Into the Bone: guitarist and drummer; Upload If Found:
  never specified). Those performers have a microphone on a
  stand in every shot they are in, singing or about to; that is correct staging, so prompt it and do not re-render to
  remove it. Only the lead singer holds a handheld microphone. What IS a
  fault: a mouth moving on someone who is not singing at that moment, a microphone hiding a face, or a stand mic on a
  performer who does not sing on this song.
- Never use the same setup twice within about four shots, and never two near-identical shots back to back.
- Open and close on the empty room. Put a wide at the first chorus entry if the song wants scale, and cut away from it
  within 3 to 4 seconds.
- Instrument detail shots crop the face on purpose. A waist-up shot that accidentally crops the head is a fault.
- Multi-person shots need every performer mapped to the scene in picture order, then the location last. For an empty
  room map the location only and set `no_character_present`.
- Known trap from BITB: in that pipeline, adding the room plate as a second reference to a shot with people made H3
  treat it as two scenes and cross-dissolve to an empty corridor. The Builder's performer + location pair has not done
  this, but check the end of any multi-reference clip for a dissolve.

### Three-shot in the Builder (tested 2026-10-05, two takes, scene of 5.8 s, 3 performers + location = 4 pictures)

The Builder accepts four pictures in one scene and renders in the usual time (about 3.5 min). Map the three performers in
order, then the location, and define `<Subject 1..3>` as people and `<Subject 4>` as the environment.

- Take 1 FAILED. Wording: singer "closest to the camera", the others "one step behind her", named only by subject tag.
  The model merged two people: the guitarist held the microphone and sang with her guitar on, the singer was missing,
  and the drummer was half hidden and blurred.
- Take 2 WORKED. All three present as themselves, singer singing (face about 205-255 px), guitarist playing with her
  mouth closed (about 150-170 px), drummer playing (about 100-105 px), no dissolve. What changed:
  - "three people standing side by side ... Three people are in the frame for the whole shot."
  - each person named by tag AND appearance: "<Subject 1>, the woman with long straight dark brown hair in a black
    leather biker jacket"
  - positions as center / left of the frame / right of the frame, all "at the same distance from the camera"
  - "her hands hold only the microphone" for the singer; "plays her white electric guitar with both hands" for the guitarist
  - "Each of the three faces is in sharp focus and fully visible, with clear space between the three people."
  - "Only <Subject 1> in the center sings"
- In take 2 the drummer got a microphone at her mouth. Whether that is wrong depends on whether the drummer sings
  backup on the song (never specified for Upload If Found). If she does not, add "The kit is drums and
  cymbals only".
- Two takes, two variables changed together (side-by-side staging and appearance naming). Treat the take 2 wording as a
  recipe that worked once, and expect to need retakes.


### Over-the-shoulder in the Builder (tested 2026-10-05, one take, 5.8 s, singer + guitarist + location = 3 pictures)

Worked on the first take: singer facing the camera and singing (face about 170-180 px), the guitarist's back and hair
filling the right foreground, the guitar headstock and her fretting hand at the bottom left, no dissolve. Wording used:

- "An over-the-shoulder shot ... Two people are in the frame for the whole shot."
- Singer by tag and appearance, "stands in the left and center of the frame, faces the camera, and is in sharp focus from
  the chest up", "her hands hold only the microphone".
- "In the right foreground, close to the camera and slightly soft, <Subject 2>, the woman with wavy copper-red hair in a
  dark grey overshirt, stands with her back to the camera: the camera looks past her right shoulder and the back of her
  head, her face is turned away and hidden, and the maple headstock and neck of her white electric guitar reach into the
  bottom of the frame as her left hand moves on the neck."
- "The camera holds steady just behind the shoulder of <Subject 2>." and "Only <Subject 1> sings".

A microphone on a stand appeared between them, pointing at the guitarist. That is not a fault: it is right for a
guitarist who sings backup. One take only.

## Fault table

| Fault seen | What the prompt had | Fix that worked |
|---|---|---|
| Keyboardist "kneeling" (keys at collarbone); drummer a giant at a toy kit | Close-up that also had to show the instrument | Waist-up or wider plus stated heights |
| Stand microphone on a performer who does not sing on this song | Nothing about it | "The kit is drums and cymbals only" (drummer). Not a fault on a backing singer |
| Lips pressed in, cheeks puffed | "Her lips rest together" | "her mouth closed and still and her cheeks at rest" |
| Flat bright light on one face | Nothing about light | "The cool overhead strip lights of the aisle light her face softly and evenly, the same light that falls on the cabinets behind her" |
| Glass streaks, smoke rings in front of a face, glass fingers | "Thin grey smoke drifts slowly behind her" | Drop the smoke sentence; "The air is clear and still." (coincided with clean takes every time; cause not isolated) |
| Flames on the bass | "lets each one ring" | Plain wording: "plucking each note with two fingers" |
| Performer stops playing and turns away | Camera slide, loose action | "stays in place facing the keyboard ... keep playing from the first frame to the last"; camera holds |
| Hand off the instrument at a guitar-driven moment | "her right arm rising after every stroke" | "her right hand stays over the strings ... her left hand stays on the neck" |
| Second singer appears | No count | "alone in the frame" |
| Extra hand | Free left arm | "her left arm hangs at her side below the frame" |
| Text on server screens | Rack described loosely | "plain unmarked perforated metal panels" |
| Opens on boots, head cut off | Tilt-up from the feet | "Her whole head and her shoulders are in the frame from the first frame to the last" |
| Singer mouths an instrumental break | One long scene with one lyric | Split the scene (see timing.md) |
| Whole clip blurred (once) | Walking toward camera | Stand still, slow push-in. One occurrence, cause unknown |

## Rules for scripted prompt edits

- Build whole prompts from the template rather than patching text. If you must patch, anchor on
  `detailed_description:` and never on the first `[Shot 1]`: that string also appears inside `retention_analysis`.
- After every write, assert each of the six headers appears exactly once and `[Shot 1] ` appears exactly once, then print
  one full prompt and read it.
- Back up the session file before each script run.
- One take proves nothing about a sentence: the same prompt and seed re-render differently. Do not tell the user a phrase
  caused a fault unless a control reproduces it.
