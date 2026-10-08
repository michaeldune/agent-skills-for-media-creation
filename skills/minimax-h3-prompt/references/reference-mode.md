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

## Practical notes

- **One reference per person** is what makes a cast shot work. Purpose-built
  references beat repurposed ones: a close-up cropped for a different job carries
  the wrong framing and lighting into the new shot.
- **State each subject's position** ("stage left", "behind and slightly left of")
  and say explicitly that everyone stays in place, or they wander.
- H3 does **not** lip sync to supplied music. If the shot needs mouths matched to
  a song, that is a different tool; H3 wides belong over instrumental passages.
- Reference encoding costs real time. Six references took ~1m40s on a distilled
  model versus ~2m20s for one image, and ~27 min on the full model. The
  identities come from the references and the brief, not from the larger model —
  the full model buys resolution. Iterate on the fast one, finish on the slow one.
