# Driving the Builder

Node `VRGDG_MusicVideoBuilderUI` has a button widget "Open Music Video Builder" that opens a full-screen UI inside the
ComfyUI page at http://127.0.0.1:8188. Use the built-in Browser pane.

## The one rule

The page keeps the whole project in memory and saves over `vrgdg_builder_session.json`. To change anything on disk:

1. Make sure no render is queued (`GET /queue`).
2. Back up and edit the session file.
3. Immediately reload the page, open the builder, Menu > Load Last Project.

Never edit the file while a batch is rendering; the page will overwrite it and a reload would kill the batch.

## Page automation

- Click buttons by their visible text with JavaScript `.click()`. The pane's scale changes and coordinate clicks miss.
- Open the builder:
  `app.graph._nodes.find(n => n.type === 'VRGDG_MusicVideoBuilderUI').widgets.find(w => w.name === 'Open Music Video Builder').callback()`
  If the node is missing: `LiteGraph.createNode('VRGDG_MusicVideoBuilderUI')` and `app.graph.add(n)`.
- Set a text input with the native value setter, then dispatch `input` and `change` events.
- Keep each script call under 45 s.
- A warning dialog can hide behind the wizard. If a click seems to do nothing, list the visible buttons.

## Rendering

Several scenes:
Select Multi > type a list such as `6, 8, 20-51` into the box beside "Apply Scene List" > Apply Scene List > Menu >
Render All > choose radio `redo_videos` and radio `selected` > Run Render.

- The `selected` label reads "Selected scenes only (N)". Check N before running.
- With only ONE scene selected that option is missing and the default is ALL scenes. Cancel and use the single route.
- Once multi-select is on, the toggle button reads "Multi N".
- Confirm the first job uses the right references: read `/queue` and look at the `image_paths` input.

One scene:
click its timeline button ("Scene N ...") > Video tab > "Create MiniMax H3 Scene Video" > "Backup and replace". Check the
dialog text names "N. SCENE N".

The Builder swaps the new clip into `rendered_scene_videos\video_NNNN-audio.mp4` a few seconds AFTER ComfyUI reports
success. Wait for that file's modified time to pass the start of your job before copying or judging it. Never pick "the
newest file in the folder".

Stitch:
Select Multi with the full range > Menu > Stitch Preview > "Use Selected Scenes (N)". About 30 s. Output is the next
`PREVIEW_SCENES_selected<k>.mp4` in the project folder.

## Session file map

- `segments[]`: one per scene, in order. Scene number = index + 1.
  - `start`, `end`, `custom_audio_timeline_start`, `label`, `lyric_text`
  - `minimax_h3_prompt`, `minimax_h3_mode`, `video_prompt_type`, `minimax_h3_prompt_origin`
  - `lyric_no_lip_sync`, `lyric_singers`
  - `video_path`, `video_source_path`, `video_thumbnail_path`, `video_status`
  - `video_history[]`, `video_thumbnail_history[]`, `video_history_index` (what the stitch plays)
  - `minimax_h3_timing` (written at render; includes `requested_warmup_frames`, untested)
- `flux_reference_builder.subjects[]` and `.locations[]`: id, name, description, image path.
- `flux_reference_builder.subject_scene_map[segment_id]`: list of subject ids for the scene, in picture order.
- `flux_reference_builder.scene_map[segment_id]`: location id.

Reference check at render time: an UNCHANGED prompt whose saved binding signature no longer matches the mapping is
refused. A changed prompt is checked only for picture count and for subject names matching the mapping order.

## Other traps

- A health check with a short timeout fails while the GPU is busy. Use 20 s or more before deciding the server is down,
  and never start a second server on the same port.
- LM Studio (only if the user asks for the local runner): the Builder sends its own context length and a mismatch loads a
  second model instance; thinking models crawl on text steps; the prompt step needs a vision model.
- Free the GPU when finished: `POST /free` with `{"unload_models":true,"free_memory":true}`.
- Copy finished clips, the session file and the stitch to a durable folder before the session ends.
