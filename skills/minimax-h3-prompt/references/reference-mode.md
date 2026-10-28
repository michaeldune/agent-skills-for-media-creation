# Ref2VA — the six-section reference brief

Use this when any attached media is a **reference** (this is what the character
looks like, this is the room, this is the voice timbre, this is the style) rather
than a literal first or last frame.

## The six sections, in this order

| Section | Purpose |
|---|---|
| `subject_definitions` | Names each referenced thing and binds it to its reference label |
| `summary` | Task type, what the target video is, main reference relationships |
| `retention_analysis` | How strongly each reference must be preserved, and where |
| `detailed_description` | Visuals, actions, shots, sound and dialogue in playback order |
| `overall_soundscape` | Ambience and physical sound |
| `non_diegetic_music` | Score only the audience hears (`None.` if there is none) |

A reference brief starts directly with `subject_definitions:` — never with a
frame-alignment line, which belongs to base mode.

## subject_definitions

One line per subject, binding it to the picture(s), video(s) or audio it comes
from, followed by the distinguishing details.

```text
<Subject 1> is the coffee-shop environment in <Picture 1>, featuring an exposed brick wall, an orange tufted sofa with patterned pillows, a neon sign, and a wooden coffee table.
<Subject 2> is the fluffy white Samoyed in <Picture 2>, <Picture 3>, and <Picture 4>, with thick white fur, pointed ears, a dark nose, and a curved tail.
<Subject 3> is the young blonde woman in <Video 1>, with long blonde hair and a light-pink button-down shirt with rolled-up sleeves.
<Audio 1> is the voice-timbre reference for <Subject 3> (S1), containing a spoken English vocal layer.
```

Note `<Subject 2>` citing **three** pictures. Multiple angles of one character is
the intended usage — a single reference gives the model less to work with and
identity gets softer as the camera moves.

**Identity references belong inside the subject line**, as above. A standalone
`<Picture N>` definition is for a picture playing a role in its own right:

| Role | Retention marker | Task type |
|---|---|---|
| First frame | `fully_preserved` | keyframe completion |
| Last frame | `fully_preserved` | keyframe completion |
| Composition | `weak_reference` | reference generation |
| Look / style | `weak_reference` | reference generation |
| Setting | `partially_preserved` | reference generation |
| Attribute → subject | `attribute_transfer` | reference generation |
| Storyboard | `weak_reference` | reference generation |

## summary

Opens with the task type in brackets, then states the target video and how the
references relate to it.

```text
summary:
[reference generation + audio reference] The target video shows <Subject 3> eating a cookie in <Subject 1>. <Subject 4> enters with <Subject 2>, which lunges toward the cookie. The three-shot exchange uses <Audio 1> as the voice-timbre reference for <Subject 3> and ends with a canned audience laugh.
```

## retention_analysis

One line per subject: which shots it appears in, its retention marker, and
exactly which attributes are being held. This is the lever that controls drift —
be specific about the attributes, because "preserved" alone leaves the model to
decide what mattered.

```text
<Subject 1> (appears in [Shot 1], [Shot 2], [Shot 3]): fully_preserved - the exposed brick wall, orange tufted sofa, patterned pillows, neon sign, and wooden coffee table are retained.
<Subject 2> (appears in [Shot 1], [Shot 2]): fully_preserved - the Samoyed's thick white fur, pointed ears, dark nose, and curved tail are retained.
<Audio 1>: reference - its vocal timbre guides the dialogue delivery of <Subject 3> without copying the original signal.
```

Every subject defined above should appear here. A subject that is defined and
never given a retention line is one the model is free to reinvent.

## detailed_description

Opens with a one-line style statement, then the timeline. Cite subjects by label
**and** restate their key attributes as they appear — the redundancy is
deliberate and helps the model hold them.

```text
detailed_description:
The target video uses a realistic multi-camera sitcom style with warm indoor lighting.
[Shot 1] A medium shot establishes <Subject 1>, the coffee shop with its exposed brick wall, orange tufted sofa, patterned pillows, neon sign, and wooden coffee table. <Subject 3> (S1), the young woman with long blonde hair and a light-pink button-down shirt with rolled-up sleeves, sits on the sofa holding a chocolate-chip cookie. From the left, <Subject 4>, the young man with short wavy brown hair and a dark-grey hoodie with drawstrings, enters holding the leash of <Subject 2>, the thick-furred white Samoyed with pointed ears, a dark nose, and a curved tail. The dog lunges toward the cookie and pulls the leash taut. <Subject 3> (S1) jerks her hand back and, using the clear youthful voice timbre referenced from <Audio 1>, exclaims with light annoyance, <d>[English] Hey! Watch your dog!</d> She closes her lips and guards the cookie while <Subject 4> pulls the dog back.
[Shot 2] At 00:03.000, the shot cuts to a close-up of <Subject 4> (S2), the young man in the dark-grey hoodie from Shot 1, sitting beside <Subject 3> …
```

## A worked multi-character example

This pattern held five distinct people in one wide shot. Note carefully what did
the work: **six separate reference pictures, one per subject**. A single
composite reference produced five strangers; six individual ones fixed it. In a
controlled A/B, plain prose with the same six references held the cast just as
well — so credit the references, not the format. The structure is what makes the
staging, retention and camera explicit and editable, which is a different and
smaller benefit.

The shape generalises to any full-cast frame — a band, a team, a family, a
product line-up.

```text
subject_definitions:
<Subject 1> is the small dark club stage environment in <Picture 1>, featuring a low riser, Marshall amplifier stacks, monitor wedges and tangled cables on the floor, an overhead lighting truss, and thick haze lit by blue and magenta beams.
<Subject 2> is the lead singer in <Picture 2>, a woman in her late twenties with long straight brunette hair, wearing a deep-red velvet biker jacket over a black top, standing at a microphone on a stand.
<Subject 3> is the guitarist in <Picture 3>, a young woman with long natural ginger-red hair wearing an open green and black flannel shirt, playing a glossy black Les Paul electric guitar.

summary:
[reference generation] The target video is a single wide locked-off shot of a five-piece rock band performing live on <Subject 1>. <Subject 3> plays stage left, <Subject 2> sings centre stage at her microphone stand … All five identities are taken from their reference pictures and preserved.

retention_analysis:
<Subject 2> (appears in [Shot 1]): fully_preserved - her long straight brunette hair, deep-red velvet biker jacket and black top are retained.
<Subject 3> (appears in [Shot 1]): fully_preserved - her long ginger-red hair, green and black flannel shirt and glossy black Les Paul are retained.

detailed_description:
The target video is a realistic live-concert style wide shot with hard coloured stage lighting and heavy haze.
[Shot 1] A wide locked-off shot frames the whole of <Subject 1> from the front of the room, slightly below stage height. <Subject 3> stands at the far left playing her black Les Paul, head down … Everyone remains in their own fixed position on the stage throughout. The frame never moves — no pan, no push-in, no reframing.

overall_soundscape:
A loud live rock band in a small hard-walled room, drums and bass guitar filling the space, amplifier hum, and the close ambience of a crowded club.

non_diegetic_music:
None.
```

## A sung shot from a vocal stem

To make a performer sing a real song in sync, attach the song's **vocal stem**
(separated with demucs, cut to the shot) as `<Audio 1>` and write its lyrics
with their measured times into the brief. H3 returns the stem as the clip's
soundtrack almost verbatim (waveform correlation 0.94 after the audio VAE round
trip) and lip syncs the performer to it. Tested on two reference-to-video
checkpoints, three seeds each, 11.5 s at 480p, with a 3.5 s gap between two
sung lines; watched and judged in sync on both.

The parts of the brief that do it (the lyric is a placeholder):

```text
<Audio 1> is the sung vocal of <Subject 1> (S1) for this shot: two sung English lines with a silence between them.
...
<Audio 1>: reference - its sung vocal, melody, words and timing are performed by <Subject 1>.
...
[Shot 1] A medium close-up frames <Subject 1> from the chest up, holding the microphone just below her chin so her mouth stays fully visible. At 00:00.500 <Subject 1> (S1) sings <d>[English] the first line, word for word as sung</d> and at 00:03.860 her lips close completely and all singing motion stops. From 00:03.860 to 00:07.360 ...
```

- Take every start and end time from the stem itself (forced-aligned word
  timings on the stem), relative to the cut, and give every gap a closed-lips
  end state.
- Keep the mouth visible: the microphone below the chin, framing chest-up or wider.
- The verbatim copy seems tied to the brief's lyrics matching the audio: a plain
  voice clip with different words is not copied, it only lends its timbre. That
  link is a guess, not tested.
- Untested: the full mix instead of the stem, the stem with backing at -14 dB,
  lyrics that differ from the audio, two or more singers, 768p, 15 s shots.

## Voice references for speakers

When a speaker's voice comes from a reference clip (`<Audio N>` as a
voice-timbre reference, one per speaker), two rules from Cosmo-Edge Labs'
[MiniMax H3 Dialogue: From Robotic to Near-Studio Voices](https://www.youtube.com/watch?v=7LXAhgvaoVA):

- **Attach the voice references in the order the characters first speak.**
  The first speaker's voice is `<Audio 1>`, the second's `<Audio 2>`.
- **Use uncompressed WAV taken from the source, never MP3.** H3 copies the
  whole sound of a timbre reference, compression artifacts included, so an MP3
  reference gives a muffled, metallic voice. Converting an MP3 to WAV does not
  help; the WAV must come from the original recording or a generation exported
  as WAV. A good reference is one isolated voice: no music, no background
  noise, no room echo, a steady level.

Both confirmed here (turbo reference-to-video checkpoint, 480p, 8 s, two seeds
per arm):

- **Order.** Two women at a table, voice references that differ only in pitch
  (174 Hz and 211 Hz), each `<Audio N>` explicitly bound to its subject in
  subject_definitions and retention_analysis. Attached in speaking order, each
  woman got her own voice on both seeds. Attached in reverse order, with the
  labels rewritten so every binding was still correct, the voices swapped on
  both seeds. H3 gives the first-attached voice to the first speaker whatever
  the labels say. With a woman and a man the gender in the prompt won and no
  swap showed, so a mixed pair hides the problem rather than avoiding it.
- **Format.** The same voice as WAV and as a 32 kbps MP3, same prompt and
  seeds: the MP3 renders kept 0.01-0.02% of the speech energy above 6 kHz,
  against 0.71-0.89% for WAV. Words and pitch were unchanged. That is a
  measurement of lost top end, not a listening test.

## Practical notes

- **One reference per person** is what makes a cast shot work. Purpose-built
  references beat repurposed ones: a close-up cropped for a different job carries
  the wrong framing and lighting into the new shot.
- **State each subject's position** ("stage left", "behind and slightly left of")
  and say explicitly that everyone stays in place, or they wander.
- For a performer singing a supplied song, use the vocal-stem route above. A wide
  with no visible mouths still belongs over an instrumental passage.
- Reference encoding costs real time. Six references took ~1m40s on a distilled
  model versus ~2m20s for one image, and ~27 min on the full model. The
  identities come from the references and the brief, not from the larger model —
  the full model buys resolution. Iterate on the fast one, finish on the slow one.
