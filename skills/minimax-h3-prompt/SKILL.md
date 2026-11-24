---
name: minimax-h3-prompt
description: Write MiniMax H3 video prompts as structured Context-IR briefs instead of prose. Use this whenever generating video with MiniMax H3 in any form — SimpliGen H3 presets (t2v/i2v/r2v, turbo or full), ComfyUI MiniMax H3 nodes, or the MiniMax API — and whenever the user asks for an H3 prompt, a shot with dialogue or singing, a video that must keep a specific character's or product's appearance, a multi-character or full-cast wide shot, or a clip built from reference images. Also use it when an H3 result came back with the wrong people, drifting camera, ignored staging, or mouths that keep moving after speech ends, since those are usually prompt-format failures rather than model limits.
---

# Writing MiniMax H3 prompts

H3 is not a "describe your video in a sentence" model. It was trained on a
structured intermediate representation, and MiniMax built a separate model —
**H3-Context-IR** — whose whole job was turning a user's request into that
structure before generation. That model was never open-sourced. Their own model
card says Context-IR "is critical to the quality of the final output" and tells
you to build your own.

That is what this skill is. You are standing in for the missing rewriter:
understand the request and its media, then serialise that understanding into the
format H3 expects. Prose gets you a plausible-looking video that ignores half of
what was asked; the structured brief gets you the shot you specified.

Be clear-eyed about what the structure does and does not buy, because it is easy
to over-claim here. Two A/B tests on the same model, same seed, same references —
a five-character wide shot and a two-hander with dialogue — produced results a
careful viewer rated as comparable, with a mild subjective preference for the
structured version. So the format is not magic.

What actually fixed the five-character shot was **one reference picture per
person** instead of a single composite. That is a media decision, and it works in
prose too. Do not attribute it to the format.

Where the structure genuinely cannot be replaced:

- the **alignment instruction lines** for I2VA/FL2VA/L2VA are fixed wording the
  model was trained on; prose has no equivalent
- **speaker IDs, `<d>` tags and lip-closure** are the documented controls for
  who speaks, what they say, and when the mouth stops
- **timed `[Shot N]` cuts** put a real cut inside a single generation
- `retention_analysis` gives per-subject control over what may drift

The rest is a good default rather than a proven win: it makes decisions explicit
so the model does not make them for you, and it makes a prompt you can diff and
edit later. That is worth something. It is not worth pretending it is a
transformation.

## Step 1 — Pick the mode from the media, not from what anyone called it

The mode is decided by what media is actually attached, never by a label in the
request:

| Media attached | Mode | Template |
|---|---|---|
| none | **T2VA** | three core fields |
| one image, video starts on it | **I2VA** | alignment line + three core fields |
| two images, video runs first→last | **FL2VA** | alignment line + three core fields |
| one image, video *ends* on it | **L2VA** | alignment line + three core fields |
| anything used as a *reference* rather than a frame | **Ref2VA** | six sections |

The split that matters: a picture used as a **frame anchor** (the video literally
begins or ends on it) takes a base-mode template with an alignment instruction.
A picture used as a **reference** (this is what the character looks like, this is
the room, this is the style) takes the full six-section reference template.

Read `references/base-mode.md` for T2VA/I2VA/FL2VA/L2VA, including the exact
alignment instruction lines, which are fixed wording.

Read `references/reference-mode.md` for Ref2VA — the six sections, the retention
markers, and a full worked example. A performer **singing a supplied song** is
Ref2VA too: its vocal stem goes in as `<Audio 1>`, see "A sung shot from a vocal
stem" there. For speakers whose voices come from reference clips, read "Voice
references for speakers" there: attach voices in the order the characters
first speak (tested: H3 ignores the labels and swaps voices otherwise) and use
WAV, not MP3.

For a **character PV** (a 15-second, 13-shot anime-style character reveal with
kinetic typography cards, driven by one design-sheet reference), use the two
templates in order: `references/design-sheet.md` writes the image prompt that
produces the sheet, and `references/character-pv.md` is the fixed 13-shot
Ref2VA skeleton with the card strings, name, title and venue as fill-in fields.

## Step 2 — Number the references before you write anything

H3 labels references **by input order**, and its positional clock advances on
them. `<Picture 1>` is whatever image was attached first. Reordering the same
references is a different request.

So: fix the order first, write the labels to match, and never renumber mid-brief.
Numbering is independent per type — the first video is `<Video 1>` even if the
first image is `<Picture 1>`.

If you are the one choosing the order (e.g. building an API call), put the
environment or establishing reference first and the characters after it, in the
order they appear on screen left to right. That costs nothing and makes the brief
readable later when something needs changing.

## Step 3 — Write the brief

Both templates share the same timeline grammar. The details that repeatedly
matter:

**Shots.** `[Shot 1]` carries no timestamp. Every later shot is
`[Shot N] At MM:SS.mmm, the camera cuts to …` with strictly increasing times, all
inside the target duration. A cut should introduce genuinely new information —
new subject, space, state, viewpoint, or time. If only the framing needs to
change, move the camera instead of cutting.

**Camera — always state it.** Left unsaid, H3 drifts and reframes continuously,
which is why "static" shots come back wandering. Name one move, its amplitude and
speed, and what visibly changes because of it: *"The camera pushes in with small
amplitude at slow speed toward her hands."* For a locked-off shot, open the
camera line with **"Locked-off composition, … fixed camera, no reframing."**
(adding "tripod" is fine). Tested 2026-11-24 on a 2-step and an 8-step H3
checkpoint, text to video, two seeds: that wording held the frame to 1-3 px of
drift over 5 s, while "the frame never moves: no pan, no push-in, no
reframing" on its own crept and pushed in by 14-38 px on every take. Keeping
"the frame never moves" after the lock wording does no harm. Saying "the
camera does not move" is weaker still. What H3 does with lens, gear and phone
words is in `references/camera-capture.md`. Never
stack moves that contradict each other in one beat (locked-off plus orbit plus
handheld shake): H3 renders an average of them, which is none of them.

For a tight shot, write the size outright and where it starts: H3 opens
wider than asked when a reference picture is wider. "Starts already framed
from the waist up" still opened wide on a wide garden picture, while a
close-up framing choice plus "starts already tight on the face and
shoulders" opened tight on four of four takes.

**Beats.** Give each beat one primary change and an observable end state
something a viewer could point at — an empty surface, a door now closed. Budget
roughly four seconds for anything involving a prop change or hand-off. Put the
most important beat in the *middle*: the last one gets squeezed. If the duration
cannot hold every beat, cut one rather than compressing all of them.

**Interaction between characters must be spelled out physically.** H3 renders
each described action faithfully and in order, but it has no model of intent:
a call and a laugh are two unrelated events unless the prompt binds them. A
market test (2026-09-06) is the canonical failure — "he calls out, she laughs
and turns" rendered as her laughing and walking off *without ever looking at
him*. Any beat where two characters react to each other needs all three of:

- an **eye line** — who is looking at whom, restated in every beat where it
  matters ("her eyes on him", "still looking at him"). This is the single most
  reliable connector.
- a **facing or distance end state** — "turns her whole body to face the
  stall", "standing in front of the stall, hand out". Orientation and position
  are things it can render; "responds to him" is not.
- a **timestamp for the reaction**, separate from the line that provokes it
  (speech at 2 s, reaction at 3.5 s), or the reaction can land before or during
  the line.

Give the reaction a physical cause where you can (coins held up in a hand give
her something to walk back to), and once you have seen a specific failure, name
that exact behaviour as a prohibition ("she never walks off toward the camera").

**Name only what the frame holds.** A thing the brief names tends to be
drawn, whatever "off frame" says: "a caged work lamp off frame" put a
blown-out caged lamp in the shot. For light from outside the frame, write
only the glow and its direction ("a dim warm glow from off frame, low at
frame left"), and say what stands beside a lone subject rather than who must
not appear. The sound line works the same way (see "The soundscape can add
people" under Sound).

**Keep the eyes off the lens.** An eye line to someone off screen renders as
a look into the lens: "looks straight at him" did it in a single close-up,
and a short prompt with no acting in it stared blank into the lens from 3 s.
Place the partner in frame terms and give the eyes something to do: "turns
her head to her right, toward him off-screen at the left edge of frame, her
eyes on him just past the side of the lens; she never looks into the
camera", with natural blinks. On the same seed that wording kept her eyes
off the lens for the whole shot.

**Speakers and dialogue.** Every vocal source gets a stable ID — `(S1)`, `(S2)`,
`(S1,S2)` for simultaneous speech — kept consistent across shots. Characters who
never vocalise get no ID. Establish who they are *outside* the tag on first
appearance: type, age, gender, on- or off-screen, pitch, timbre, rate, accent.
Then all spoken content goes inside `<d>[Language] The actual words.</d>` with a
real language tag (Arabic, Chinese, English, French, German, Italian, Japanese,
Korean, Portuguese, Russian, Spanish). Reproduce the words verbatim — never
translate or paraphrase inside `<d>`. Place each line after the action or event
that motivates it in the timeline, not before it.

Two details that fix visible artefacts: **describe the lips closing and the
speaking motion ceasing** when a line ends, or the mouth keeps moving; and for
voiceover use the exact phrase *"says in an off-screen voiceover"* followed by a
statement that the lips remain completely closed.

**Claim the time after the line, or H3 fills it with words you never wrote.**
H3 generates audio for the *whole* duration, so a line shorter than the shot
leaves a gap it resolves by repeating and mangling your line. A one-sentence
line is about six seconds of speech (≈5 words/sec), so a 13-second shot leaves
roughly eight seconds of gap, and it garbles reliably — reproduced on two seeds.
The fix is three sentences, and it removed the invented words completely on the
same seed that had failed twice, leaving 6.4 s of held silence:

- the closure **as an event**, not an instruction: *"the instant that sentence
  ends, her lips close completely and all speaking motion stops"*
- an **observable end state for the leftover time**: *"for the entire remainder
  of the shot she stays silent with her lips closed and still, hands resting on
  the desk"*
- the failure **named as a prohibition**: *"she speaks only once, does not repeat
  any part of the line, and no further words or vocal sound occur"*

Two near-misses worth knowing, because they are what you reach for first:
**generator-directed meta-instructions do nothing** — *"do not pad for length"*,
*"keep it short"*, *"don't add anything"* have no referent in the scene, the same
way *"responds to him"* has none. And a prompt that covers **only** the moment
speech ends — *"when the dialogue ends she should close her mouth and stop
talking"* — does not remove the extra words, it **relocates them to the
unclaimed remainder**: tested, and the invented words moved from before the line
to after it. Modal phrasing (*"she should close her mouth"*) is also weaker than
describing the closure happening.

**Write behaviour, not thoughts.** H3 can voice any phrase that sits near a
speaking act. "Then he shouts his one line once" came back as "One line
once. I won!", and an inner thought written into the action ("a costume on
her roster") came back as "...a roster named..." until it was rewritten as
what the eyes and body do: "her eyes search it, flick to the trail, come
straight back and search it again, while her hands stay easy on the wheel".
Describe the act ("he throws his head back and shouts with joy"), keep
"line", "once" and any paraphrase of the words away from the speaking verb,
and open a dialogue shot with the person and the action, not a phrase that
could be spoken.

When a line crosses a cut, put `<scenetrans>` at both connection points and say
the audio continues across the cut. Mark speech cut off by the end with
`<cutoff>`.

**Sound.** `overall_soundscape` is ambience and physical sound — what exists in
the room. `non_diegetic_music` is score only the audience hears. If there is no
score, write `None.` rather than omitting the field.

- **`None.` works for the score, not for the soundscape.** `non_diegetic_music:
  None.` kept music out on two test renders, but `overall_soundscape: None.`
  does not buy silence: H3 always writes an audio track, and with nothing named
  it invented hiss and stray sound events (measured, two checkpoints). Name
  what should be heard (*"light wind, footsteps on concrete"*) and H3 renders
  that. For a truly silent clip, strip the audio afterwards
  (`ffmpeg -i in.mp4 -c:v copy -an out.mp4`).
- **Anything written in the prompt can be spoken.** Plain English in any field
  can end up voiced into spare time after a short line, including boilerplate a
  workflow adds to your prompt without you seeing it. When a render has extra
  words, check them against every string the workflow injects, and keep
  injected markers bare (for example `<Audio 1>: fully_copy` with no
  explanation after it).
- **The soundscape can add people.** A solo close-up of one musician grew the
  rest of the band at the frame edges on every take when the prompt said
  "concert footage" and the soundscape named drums, bass and guitar; a new seed
  and "no other musician enters" did not help. What cleared it: "footage of the
  drummer, alone", a soundscape naming only that instrument, a positive
  description of what stands beside them, and "the frame never moves". When a
  fault survives a seed change, it is in the inputs: look for anything in the
  brief that names the intruder.

## Step 4 — Check it before spending GPU time

A brief is cheap to fix and a render is not. Before submitting, confirm:

- the template matches the media actually attached
- `<Picture N>` / `<Video N>` / `<Audio N>` numbering matches input order, with
  none skipped, renamed, or invented
- `[Shot 1]` has no timestamp; later shots increase and stay inside the duration
- the camera is specified in every shot
- every speaker has a stable ID and every line sits inside `<d>[Language] …</d>`
- speech that ends has its lips closing described
- every two-character beat states the eye line, a facing/distance end state,
  and a timestamp for the reaction (see "Interaction" in Step 3)
- in reference mode: all six sections present, in order, and every `<Subject N>`
  defined in `subject_definitions` also appears in `retention_analysis`

A low-resolution, few-step draft is worth running first, but it confirms only
the timing and the words. It does not predict who lip syncs a line or how a
performance plays at full quality (a 480p draft kept a listener's lips closed
on four seeds; the 768p render of one of them had her mouthing the other
speaker's words), so check every mouth again on the final render.

After the render: transcribe it and compare the words with the line (Whisper
invents phrases such as "thank you for watching" on noise, so watch the mouth
before calling a sound speech), check the eyes against the lens, and compare
frame 3 with each reference picture, since a clip can open on a reference
photo and dissolve into the scene without a hard cut.

## What this buys you, and when to reach for it

**Multi-character shots are the strongest case.** Give each person their own
reference picture, define each as a `<Subject N>`, and mark them
`fully_preserved`. Models that scramble identities when handed one composite
image hold them when each is cited individually. The official example goes
further and cites *three* pictures for one subject — multiple angles of the same
character is the intended usage, not an edge case.

**Retention markers are how you control drift**: `fully_preserved` for identity
you need kept, `partially_preserved` for a setting that can flex,
`weak_reference` for composition or style, `attribute_transfer` for moving one
property onto a different subject.

**Identity belongs inside the subject line**, not as a standalone picture
definition: `<Subject 1> is the woman in <Picture 1>, with …`. Standalone
`<Picture N>` definitions are for pictures playing a role in their own right —
first frame, composition, setting, style.

A brief this explicit is longer than a prose prompt, and that is the point: every
sentence you leave out is a decision the model makes for you.
