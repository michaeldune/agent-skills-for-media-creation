"""EXAMPLE from one project, not a general tool: edit the scene numbers, times and prompts before running it.
Split scene 47 into three (2026-10-05). The user, by ear: 3:39-3:41 "Upload if found", 3:41-3:44 keyboard
interlude (the singer was lip-syncing it), 3:44-3:46 "Upload if found", 3:46-3:49 sustained wordless scream.
The Builder's scissors refuse rendered scenes, and clip files are named by scene NUMBER, so this inserts two segments by
hand and renames the clip/thumbnail files of the old scenes 48-51 to 50-53 before anything renders."""
import copy, json, os, re, shutil, time, uuid

ROOT = "<ComfyUI output folder>/<project>/"
P = ROOT + "vrgdg_builder_session.json"
shutil.copy(P, P.replace(".json", "_before_claude_split47_%s.json" % time.strftime("%H%M%S")))
s = json.load(open(P, encoding="utf-8"))
segs = s["segments"]
frb = s["flux_reference_builder"]
assert len(segs) == 51 and abs(segs[46]["start"] - 218.75) < 1e-6 and abs(segs[46]["end"] - 230.8) < 1e-6
T1, T2 = 221.375, 224.25
END = ("The air is clear and still. The image is clean and sharp. Cold blue-white datacenter light, desaturated palette, "
       "dark clothing, photorealistic.")
AISLE = "the cold datacenter aisle between two rows of tall black server cabinets with small blue status lights"
MIC = ("She holds the silver handheld microphone in her right hand at her lips, and her left arm hangs at her side below "
       "the frame.")
LOCD = {x["id"]: x["description"] for x in frb["locations"]}
SECTIONS = ("subject_definitions:", "summary:", "retention_analysis:", "detailed_description:", "overall_soundscape:",
            "non_diegetic_music:")


def build(who, loc_id, shot):
    p = ("subject_definitions:\n<Subject 1> is the %s in <Picture 1>; <Picture 1> is the visual authority for character "
         "identity, face, hair, clothing, and body-proportion reference.\n<Subject 2> is the environment in <Picture 2>, used "
         "as environment, location, architecture, layout, and atmosphere reference: %s\n<Audio 1> is the complete synchronized "
         "song and vocal track for the target video, reused as the target video's complete final soundtrack and timing "
         "reference.\n\nsummary:\n[reference generation + audio reuse] The target video is a industrial_metal scene featuring "
         "<Subject 1> (%s) and <Subject 2> (environment). <Audio 1> is reused as the complete soundtrack and timing reference."
         "\n\nretention_analysis:\n<Subject 1> (appears in [Shot 1]): fully_preserved - reference identity, face, hair, "
         "wardrobe, and accessories remain consistent.\n<Subject 2> (appears in [Shot 1]): fully_preserved - the location and "
         "its reference identity remain consistent.\n<Audio 1>: fully_copy - <Audio 1> is reused 1:1 as the target video's "
         "complete final audio track.\n\ndetailed_description:\nThe target video is in a industrial_metal music-video style."
         "\n\n[Shot 1] %s\n\noverall_soundscape:\n<Audio 1> remains the sole complete audience-facing soundtrack with its "
         "original mix, timing, vocals, music, and dynamics intact.\n\nnon_diegetic_music:\n<Audio 1> is reused as the complete "
         "audience-facing song/music track.") % (who, LOCD[loc_id], who, shot)
    for sec in SECTIONS:
        assert p.count(sec) == 1
    assert p.count("[Shot 1] ") == 1
    assert not re.search(r"\b(no|not|never|without)\b", re.sub(r"<d>.*?</d>", "", shot), flags=re.I)
    return p


def blank_video(g):
    for k in ("video_path", "video_thumbnail_path", "video_source_path"):
        g[k] = ""
    for k in ("video_history", "video_thumbnail_history", "video_backup_paths", "video_backup_thumbnail_paths"):
        g[k] = []
    g["video_history_index"] = -1
    g["video_status"] = "none"
    g["video_output"] = None
    g.pop("minimax_h3_timing", None)
    g.pop("minimax_h3_prompt_reference_binding", None)


# --- 1. shift the clip files of old scenes 48..51 up by two, highest first
for old in (51, 50, 49, 48):
    g = segs[old - 1]
    new = old + 2
    for folder, ext, key in (("rendered_scene_videos", "mp4", "video_path"),
                             ("scene_video_thumbnails", "jpg", "video_thumbnail_path")):
        src = ROOT + "%s/video_%04d-audio.%s" % (folder, old, ext)
        dst = ROOT + "%s/video_%04d-audio.%s" % (folder, new, ext)
        assert not os.path.exists(dst), dst
        if os.path.exists(src):
            os.rename(src, dst)
        g[key] = dst.replace("/", chr(92))
    g["video_source_path"] = g["video_path"]
    print("scene %d -> %d  %s" % (old, new, os.path.basename(g["video_path"])))

# --- 2. the three new scenes
a = segs[46]                                   # singer, first line
c = copy.deepcopy(a)                           # singer, second line + scream
c["id"] = "seg_" + str(uuid.uuid4())
b = copy.deepcopy(segs[43])                    # keyboardist (cloned from scene 44)
b["id"] = "seg_" + str(uuid.uuid4())
a["end"] = T1
b["start"], b["end"], b["custom_audio_timeline_start"] = T1, T2, T1
c["start"], c["custom_audio_timeline_start"] = T2, T2
for g in (a, b, c):
    blank_video(g)
a["lyric_text"] = c["lyric_text"] = "Upload if found."
b["lyric_text"] = "[instrumental]"
b["lyric_no_lip_sync"] = True
b["lyric_singers"] = []
b["story_beat"] = "Keyboard interlude: cutaway to the keyboardist."
a["minimax_h3_prompt"] = build("singer", "wizard_beta_location_0",
    "A medium close-up of <Subject 1>, alone in the frame, standing still in " + AISLE + ". " + MIC + " The camera holds "
    "steady at her eye level. She sings at full voice with grief and defiance, her eyes on the camera, her lips and jaw forming "
    "every word: <d>[English] Upload if found.</d> She closes her lips and lowers the microphone a little as the line ends. "
    + END)
b["minimax_h3_prompt"] = build("keyboardist", "wizard_beta_location_1",
    "A waist-up shot of <Subject 1>, alone in the frame, seen from the front at a three-quarter angle. He stands upright at a "
    "full-size black keyboard on a stand at the height of his waist, with a black server rack with rows of small blue, green and "
    "amber status LEDs and bundles of grey network cables behind him. His arms reach down to the keys. His right hand plays a "
    "fast run of short repeated notes and his left hand holds a chord, from the first frame to the last. His mouth is closed "
    "and still and his eyes are on his right hand. The camera holds steady. " + END)
c["minimax_h3_prompt"] = build("singer", "wizard_beta_location_0",
    "A tight close-up of <Subject 1>, alone in the frame, standing still in " + AISLE + ". Her face fills the frame. " + MIC
    + " The camera pushes in very slowly for the whole shot. She sings at full voice, her lips and jaw forming every word: "
    "<d>[English] Upload if found.</d> Then she throws her head back slightly and holds one long, wordless scream, her mouth "
    "wide open and her eyes shut, for several seconds. As the scream ends she closes her lips, opens her eyes, and looks into "
    "the camera, breathing hard. " + END)
frb["subject_scene_map"][b["id"]] = ["wizard_beta_character_4"]
frb["scene_map"][b["id"]] = "wizard_beta_location_1"
frb["subject_scene_map"][c["id"]] = list(frb["subject_scene_map"][a["id"]])
frb["scene_map"][c["id"]] = frb["scene_map"][a["id"]]
segs[47:47] = [b, c]
for i, g in enumerate(segs, 1):
    if re.match(r"^scene\s+\d+$", str(g.get("label", "")), flags=re.I):
        g["label"] = "SCENE %d" % i
assert len(segs) == 53 and len({g["id"] for g in segs}) == 53
for x, y in zip(segs, segs[1:]):
    assert abs(x["end"] - y["start"]) < 1e-6, (x["label"], y["label"])
json.dump(s, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
for g in segs[44:53]:
    print("%-9s %7.3f-%7.3f %-5s %-18s %s" % (g["label"], g["start"], g["end"], g["video_status"], g["lyric_text"][:18],
                                               os.path.basename(g["video_path"])))
