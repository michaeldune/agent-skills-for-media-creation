---
name: ai-filmmaker-director
description: Direct AI image and video generations like a film director - turn an idea into shot-by-shot prompts with clear intent, one beat per shot, motivated camera, believable performance and physics, planned sound, and a defined end state. Use this whenever the user wants a prompt for text-to-video, image-to-video, text-to-image or image editing and no model-specific prompt skill fits (LTX, Wan, Krea, Qwen, Flux, Kling, Veo, Sora, generic "write me a video prompt"), whenever a scene, story beat, ad or music-video idea must be broken into a shot list or sequence, and whenever a generated clip came back with too many actions, random camera moves, drifting characters or no clean ending. Also use it as the planning step before a model-specific skill (MiniMax H3, Seedance, Higgsfield) writes the final prompt.
---

# AI Filmmaker Director

Turn an idea into prompts the way a director briefs a crew: every instruction has a purpose. The goal is the
simplest prompt that communicates the shot, not the most cinematic-sounding one. Keyword piles ("epic, stunning,
cinematic, masterpiece") do not direct anything; nouns, verbs, positions and light sources do.

## First: which model, and is there a skill for it?

This skill is the general layer. Models differ in the prompt format they were trained on, so the wording that
works for one can fail on another.

1. Find out the target model and mode (text-to-video, image-to-video, text-to-image, image edit). If the user
   did not say and it changes the answer, ask once; otherwise assume a prose-prompt model.
2. If a prompt skill for that model is available, do the shot planning here (steps below), then hand the plan to
   that skill to write the final prompt in its format. Known examples: `minimax-h3-prompt`, `h3-prompt-writing`
   and `dynamic-ad-camera-minimax-h3` for MiniMax H3 / Hailuo; `cinema-director-v3` for Seedance and Higgsfield
   video; `banana-pro-director-30` for Higgsfield images. Their format rules win over the templates below.
3. If no such skill exists, write the final prompt here using the templates below.

## Plan the shot

Decide these silently, in order. Not every item appears in the final prompt; keep only what improves the shot.

1. **Intent** - what should the viewer notice or feel (tension, scale, isolation, intimacy, speed). Everything
   else serves this.
2. **Subject and action** - who or what, doing what, moving where. One primary action per shot.
3. **Frame** - shot size, angle, and composition, chosen because it serves the intent.
4. **Optics** - lens feel. Descriptive language ("compressed background", "strong environmental perspective")
   usually works better than an exact focal length.
5. **Camera** - one movement, with a reason, or static. A static shot is a real choice.
6. **Performance and physics** - behaviour instead of emotion labels; weight, momentum, cloth, contact with
   surfaces.
7. **Light and space** - a motivated light source, and only the environment details that matter.
8. **Sound** - what is heard (see below).
9. **Continuity** - what must match the previous and next shot.
10. **End state** - the exact, observable condition the shot ends on.

Vocabulary for frames, angles, composition, lenses, camera moves, performance details, physics and lighting is in
`references/vocabulary.md`. Read it when you need options; do not paste lists from it into a prompt.

## One shot, one beat

Short generations cannot hold a whole scene. Size the action to the clip:

- up to about 5 s: one simple action
- 6 to 10 s: one main action plus a small reaction or transition
- 10 to 15 s: one main action with controlled secondary movement, or an action followed by a held end state
- more than that, or several actions: split into more shots

When the idea has more beats than the clip can hold, splitting is the answer, not a footnote. Say so in one
line, then write every split shot as a complete prompt. Do not deliver a single prompt that still walks through
all the beats with a note that it may be overloaded, and do not stop at an outline with an offer to write the
rest: the user asked for something they can generate now. If they clearly want one clip only, pick the beat
that carries the intent, start the shot there, and name what was left out.

A cut is an edit, not a camera move: do not ask one generation for several camera setups or locations. If one
shot really must hold a short progression, give it a plain order: first X, then Y, finally Z.

Bad: "A woman runs, jumps over a car, fights a man, picks up a weapon, and enters a building."
Better: "A woman sprints through the alley while looking over her shoulder at someone pursuing her."

## Direct behaviour, not labels

Instead of "She is scared", write what the camera can see: "Her breathing becomes shallow, her shoulders tense,
and her eyes repeatedly glance toward the dark hallway." The same goes for physics: "His coat trails behind him
as he accelerates" gives the model something to render; "realistic physics" does not. Keep performance subtle
unless the user asks for big.

## End state, and claiming the whole clip

Give every video shot a start condition, an action, and an end condition the viewer could verify ("he remains
aiming down the corridor, completely still"). Two reasons: the end state of one shot is the start of the next,
and a model fills any time the prompt leaves unclaimed with something it invents. If the action finishes early,
say what the rest of the clip shows.

## Sound

Many video models now generate audio with the picture (MiniMax H3, LTX 2.5, Veo and others). If the target does,
plan sound like any other department:

- Dialogue: give the exact line, who says it, and how. After the line, describe the mouth closing as an event.
- Ambience and effects: name the two or three sounds that belong to the scene.
- Music: say what it is, or say there is none.

Leaving sound unspecified invites an invented voice or stray music. If the model is silent, skip this section.

## Continuity: describe it, do not command it

Across shots keep identity, wardrobe, props, location, weather, time of day, light direction, colour palette and
screen direction consistent. A character moving left-to-right keeps moving left-to-right unless the camera
deliberately crosses the line; eye lines and spatial relationships carry over.

How you write it matters. Video models render what is described in the scene and often ignore instructions
addressed to the generator. "Maintain identical facial features and clothing throughout" has nothing in the
scene to attach to. Prefer scene facts: repeat the identifying details ("the same grey wool coat, collar up"),
and for anything that must match across shots, start from a still (see Sequences); words alone do not hold a
face. The exception is image editing, where an explicit keep-list is the right tool.

## Templates (for models without their own skill)

**Text to video** - there is no reference, so the prompt carries the whole scene:
`[frame + optics] of [subject + action] in [environment]. [camera movement]. [performance + physics]. [light + materials]. [sound]. [end state].`

Example: "Medium-wide chest-height shot of a black-clad ninja sprinting through a rain-soaked alley, shop signs
close on both sides. The camera tracks backward at his running speed. His stride is heavy and athletic; loose
straps whip behind him. Neon storefronts reflect across wet pavement, warm window light cutting through cool rain
haze. Rain hiss and fast footsteps on wet concrete, no music. He slows at an intersection, turns sharply toward
something off-screen, and stops completely still."

**Image to video** - the image already fixes character, wardrobe, composition, style and place, so do not spend
words re-describing them. That only works if you know what the image shows. Look at the still before writing
the motion prompt: open it if you can, otherwise ask the user for it or for a one-line description of the
framing and what is already in shot. A prompt written blind guesses, and the guess becomes a conflict: in a
test, "a train glides in from the left" was written for an empty platform, the still already had two trains in
it, and the model reshaped one carriage to reconcile them. If you must write without seeing it, say which
assumptions the prompt makes (framing, what is in frame, which side things enter from) so the user can check
them against the picture.

When the still does not exist yet, write it into the answer: give a **start-frame prompt** alongside the motion
prompt. People often make the still by pasting the video prompt into an image model. That works when the subject
just acts in place, but a video prompt describes the whole event, so the image model draws the event already
happening (the arriving train is already at the platform) and the video then has nothing left to do, or fights
the picture. The start-frame prompt describes the scene at second zero, before the action: same subject,
framing, light and place, with whatever is about to enter still out of frame or far off ("an empty platform, a
single headlight far down the track"). Write it with the text-to-image template, as a still, with no motion
verbs. Then the motion prompt only has to describe what changes from that picture.

Describe what changes:
`[camera movement] as [subject action]. [performance + physics]. [secondary environmental motion]. [sound]. [end state].`

Example: "The camera slowly pushes toward her as she raises her eyes to the doorway. Her shoulders tighten
slightly. Loose hair lifts in the draught from the open window and the curtain moves behind her. Quiet room
tone, a distant car. She ends looking directly at the doorway, motionless."

**Text to image** - a single frame, so no movement sequences:
`[shot type + lens feel] of [subject] [pose] in [environment], [composition], [lighting], [materials], [atmosphere], [visual style].`

**Image edit** - say exactly what changes, then list what stays:
"Change only her pose so that she stands with both arms crossed. Keep her face, hairstyle, clothing, body
proportions, camera angle, background, lighting and colour grade as they are."

## Sequences

For a scene, write a shot list first: establishing, character introduction, main action, reaction, detail or
insert, resolution - use as many or as few as the scene needs. Each shot gets its own complete prompt with shot
type, action, camera, performance, light where relevant, sound, and end state.

### Recurring characters: stills first, then image-to-video

When the same person, creature, product or distinctive place appears in more than one shot, make image-to-video
(or reference-to-video) the default, not text-to-video. Each generation starts from nothing, so a description
alone is re-cast every time: in a test of this skill, a lighthouse keeper described identically in three
text-to-video prompts came out as three different men, and a "hand only" insert became a different person. A
described character can hold by luck (a barista did across three shots), but a still is what makes it reliable.

So for a multi-shot piece, deliver in this order:

1. **Reference stills.** One text-to-image prompt per recurring character (and per key location if it must
   match), written with the text-to-image template. Plain, evenly lit and readable beats moody here; the still
   is a casting photo, not a shot.
2. **Start frames, when the model animates from a first frame.** For each shot, a still of that shot's opening
   composition with the same character: an image-edit prompt from the reference still ("same woman, now in
   profile at the counter holding a kettle"), or a text-to-image prompt if no edit model is available.
3. **Shot prompts as image-to-video.** Use the image-to-video template: describe what moves, the sound and the
   end state, and do not re-describe what the still already fixes. Say which still each shot uses.

For models that take reference images instead of a first frame, skip step 2 and tell the user which reference
goes in which slot. Shots with no recurring subject (an insert of beans, a landscape) can stay text-to-video.

Fall back to text-to-video for everything only when the target has no image input or the user asks for it. Then
repeat the identifying details word for word in every prompt and say plainly that the face may change between
shots.

### Check each cut

Does the next shot open where the last one ended, and is screen direction consistent? Avoid cutting between two
near-identical setups; change size or angle so the cut reads as intended.

## Keep settings out of the prose

Resolution, aspect ratio, duration, FPS, seed, steps, CFG, motion strength, sampler, model, preset and LoRA
choices belong in generation parameters, not in the cinematic text. Mention them under generation notes. A LoRA
is a parameter too: add its trigger word if it needs one, but do not re-describe its whole look in the prompt,
and check that stacked LoRAs do not pull in opposite directions.

## Check before returning

Fix these yourself rather than flagging them: more than one beat, conflicting camera moves, several lenses in
one shot, impossible motion the user did not ask for, an unclear subject or direction of travel, identity or
wardrobe drift between shots, lighting or screen-direction breaks, a camera move with no reason, a missing end
state, unplanned sound on an audio model, and length that is not earning its place.

## Output

Single generation:

```
DIRECTOR'S INTENT
One or two sentences on the visual goal.

START FRAME PROMPT   (image-to-video only, when the user has no still yet)
The text-to-image prompt for the opening picture, ready to paste into an image model.

FINAL PROMPT
The complete prompt, ready to paste.

GENERATION NOTES
Only settings or model-specific advice that matters (duration, aspect ratio, reference slots).
```

Scene or sequence: `SCENE INTENT`, then `REFERENCE STILLS` (and `START FRAMES` if the model needs them) when a
subject recurs, then `SHOT 1`, `SHOT 2`, ... each with its complete prompt and the still it starts from, then
generation notes once.

Every prompt shown is complete, word for word. People paste these straight into a generator, so never shorten
one with "(same as above)" or an ellipsis; a model will render the placeholder.

## Iterating on a result

When a generation is close but wrong, change one variable at a time, or you cannot tell which change helped.
Work in this order, because each layer depends on the one before it: action first (subject and a clear goal),
then camera (frame, lens feel, movement), then performance and physics, then light and environment, then
continuity and end state. Rerun the unmodified prompt alongside a change when you can: the same prompt and seed
can still differ between runs on some video models, so one bad render is not proof the wording caused it.

---
Credits: adapted from the "AI Filmmaker Director" skill document shared by Magnavex on the SimpliGen Discord
(2026-10-03, offered for anyone to modify), which was built from the infographic "How to Prompt Like an AI
Filmmaker" by Shailesh (@BEGINNERSBLOG). The original text is kept in `references/source-original.md`.
