# Character design sheet — the prompt template for the image step

This is the first half of the "character PV" pipeline (Smart Bobo / 机智波玩ai,
2026-09). An LLM reads one source image and writes a long image-generation
prompt for a 16:9 character design sheet. That sheet is then the single
`<Picture 1>` reference for the H3 PV brief in `character-pv.md`.

The sheet is not a Banana Pro identity lock. It is a composed poster whose
panels are themselves what the video animates through, so layout discipline
matters as much as likeness.

Source can be anything: a real photo, a phone snap of a figurine on a desk, a
game or anime character, an existing three-view sheet, two characters in one
frame. The template isolates the subject and drops the environment.

## How to use it

Paste the template below as the instruction, attach the source image, and
optionally add `Name: <name>`. If no name is given, the LLM invents one. The
output is fed straight to an image model (GPT Image / "G2" in Bobo's canvas
tool; Banana Pro also works). Two runs of the same prompt give the same layout
with small title and pose variance; pick the cleaner one.

## The template

```
You are writing a single image-generation prompt for a professional character
design sheet based on the attached image. Output only the prompt, in flowing
paragraphs, no headings, no lists, no commentary. Write in English.

The prompt must follow this structure, in this order:

1. FORMAT AND MEDIUM. Open with: a 16:9 landscape, highly finished professional
   character visual design board. State the character's name and that the page's
   main title must render exactly as that name, letter for letter. Then lock the
   medium by reading it from the source: if the source is a real person, keep a
   photoreal medium unless the user asks for a conversion; if it is an anime or
   game character, use polished digitally hand-painted thick-paint anime
   illustration (layered blocked colour, soft light-to-dark transitions, ambient
   colour, warm-cool variation, reflected light, local highlights, natural
   hard/soft edge changes, suppressed closed line art); if it is a vinyl figure
   or toy, keep the toy medium (glossy vinyl, soft flock or fur, blind-box
   proportions). Name what the image must NOT look like (the other two media).

2. IDENTITY LOCK. One paragraph describing the character as a person: age
   impression, build, proportions, face shape, eyes (colour and shape), brows,
   nose and mouth treatment, lip colour, gaze and attitude. Then hair: colour,
   length, silhouette, layering, bangs, stray strands, and how the hair must be
   rendered (clustered volumes with gradients and a few broken strands, never
   plastic 3D blocks). End with the consistency clause: every panel on the sheet
   keeps strictly the same face, the same eye shape and pupil colour, the same
   hair structure, the same age impression and the same proportions.

3. WARDROBE INVENTORY. Fully keep the outfit from the source. Walk it top to
   bottom: top, neck, waist, bottom, legs, wrists, feet, with every graphic,
   badge, buckle, chain, ring, strap and hardware item named and placed. Close
   with the palette: the dominant colours, the accent colours, what each is used
   for.

4. MATERIAL RENDERING. One paragraph giving each material its own shading logic
   in the chosen medium (cotton absorbs light with restrained reflection; woven
   tartan reads through local-colour relationships and pleat shading; leather
   has concentrated soft highlights; metal has cool reflected light, crisp
   edges, a few bright hits). End with: do not let different materials use the
   same shadow logic.

5. BACKGROUND AND LAYOUT. Background is a uniform clean low-saturation warm
   white or light grey-beige. Fixed skeleton: the complete main standing figure
   strictly at the centre; left side holds ONLY the title, three silhouettes and
   four expression heads; right side holds ONLY a three-view turnaround, four
   pose studies and four key details. Generous white space, minimal fine lines,
   small English labels only. Forbid: numbering, dense arrows, decorative
   symbols, paper texture, stains, splatter, dry brush, grain, distressed
   effects, any visual noise. All auxiliary panels clearly smaller than the
   centre figure, arranged calmly around it.

6. CENTRE FIGURE. One very large complete full-body figure at the exact
   horizontal centre, about 82 to 90 percent of frame height and 28 to 36
   percent of frame width, head to toe, footwear and both feet fully in frame,
   never cropped. Natural standing pose, frontal with a very slight
   three-quarter turn, one leg bearing weight, shoulders slightly tilted, arms
   relaxed, one hand may rest on a named wardrobe item. Gaze calmly out of
   frame. List the wardrobe items that must all be clearly visible. State that
   this figure carries the most complete rendering (skin light / half-tone /
   core shadow / reflected light; hair clusters and local brushwork; clothing
   shadow depth; edges hard or soft by focus) and that clean negative space
   must surround it.

7. TURNAROUND. Upper right, three clearly reduced full-body views in a row
   labelled FRONT, BACK, SIDE, identical size, neutral standing pose, head to
   footwear. Give each view its own checklist of what it must show (FRONT: face,
   hair, neckline, chest graphic, belt, skirt, chains; BACK: back-of-head hair,
   hair-end length, how the choker or collar closes, back of the top and its
   straps, back of the belt and skirt, where chains connect; SIDE: hair length
   at the jaw, shoulder/neck profile, garment volume, waist height, hem
   thickness, leg accessory, footwear side structure). Same medium as the main
   figure, only lower detail density, never flat colour or simple cel shading.

8. POSE STUDIES. Right side, middle-to-lower area, four small POSE STUDY panels,
   four actions that must not repeat each other, each described as body
   mechanics with an observable end state (a true seated pose with contact on a
   surface and the skirt compressed; a low centre-of-gravity half-crouch; a
   walking or turning pose with the hem and chains in motion; one more distinct
   pose). Say what wardrobe items each pose reveals.

9. LEFT COLUMN. Under the title, three solid black silhouettes of the full body
   in three distinct stances, then a row of four expression heads (name four
   expressions that fit the character), same face and hair every time.

10. KEY DETAILS. Bottom right, four detail crops: one eye, one signature
    accessory, one fabric or pattern swatch, one footwear or hardware close-up.

If the source contains more than one character, keep the same skeleton and
repeat per character: both figures share the centre slot, the silhouette set
doubles, each character gets its own turnaround row and expression row on the
right, and the detail crops cover both.

Name: {name or leave blank}
Extra instructions: {optional}
```

## What the outputs look like

Three observed sheets (punk girl from a three-view photo sheet, a Molly-style
blind-box figure from a desk photo, two figures from one photo) all produced
the same skeleton: title top left, silhouettes below it, expression heads bottom
left, big centre figure, turnaround top right, pose studies middle right, detail
crops bottom right. The medium followed the source (anime conversion for the
girl, vinyl toy look for the figures). Desk clutter never survived.

## Medium caveat

The video inherits the sheet's medium, not the source's. Bobo's punk girl went
in photoreal and came out anime because his template converts to anime. If a
photoreal PV is wanted, keep the sheet photoreal at step 1.
