# 🎬 Production Guide — "What If Elon Musk Takes Over NVIDIA?"

**Goal:** Turn the design in `video_design.md` into a finished, upload-ready YouTube Short using the best market web tools (verified live: Nov 2026).

**Recommended stack (free-first, all in the browser):**

| Step | Tool | Why | Cost |
|---|---|---|---|
| 1. Voiceover | **ElevenLabs** (elevenlabs.io) | Best realistic AI narration; Eleven v4 / multilingual | Free 10 min/mo; ~$5/mo is plenty |
| 2. Visuals | **CapCut AI Video Generator** (capcut.com, online) | Text-to-video in-browser; switch between **Veo 3.1, Sora 2, Seedance 2.5** models; no watermark on export | Free daily credits; cheap Pro |
| 3. Editing + captions | **CapCut** (same account) | Assemble the clips, AI auto-captions, SFX, music, vertical 9:16 | Same as above |
| 4. (Quality alt) | **Pika** (pika.art) or **Runway** (runway.com) | Pika H3 Flex (video+stereo audio), Runway Gen-4.5 (best motion) | Paid; optional upgrade path |

---

## Step 1 — Narration (ElevenLabs)

1. Go to **elevenlabs.io** → **Text to Speech** (or the app's Speech editor).
2. Pick a voice: search the **Voice Library** for a deep, cinematic male narrator, e.g. "Daniel", "George", "Adam" (or "Josh").
3. Paste the full narration below (one scene per line = one generation → gives you per-clip voice files that match each visual):
   - **Please note:** the raw script uses all-caps captions for visuals; for audio use the natural sentences below.

**Narration text (paste each line separately):**

```
1. Elon Musk just asked NVIDIA to bring Jensen Huang back.
2. But what if the board says no? And Musk takes the whole company instead?
3. His robot empire runs on NVIDIA chips. So does Mars. So does his AI.
4. Three billion-dollar projects. One chip supplier. And he can't let anyone control it.
5. Watch this. First he buys ten percent of NVIDIA's stock. Then he pushes out Jensen's replacement.
6. (no voice — beat)
7. (no voice — beat)
8. The good news? AI gets faster. Cars. Robots. Research. The bad news? One person now controls the factory where all AI is born.
9. Not the Pentagon. Not a government. Just one man with the keys to every AI on Earth.
10. So the real question isn't who runs NVIDIA. It's whether anyone should.
11. What do you think?
```

4. Settings: **Stability ~50**, **Similarity ~80**, **Style ~60**, speaking rate a touch slow (dramatic). Export each line as a separate `.mp3`/`.wav`.

---

## Step 2 — AI visuals (CapCut Video Studio / AI Video Generator)

1. Go to **capcut.com** → **Online** → **Video Studio** or **Create → AI Video**.
2. Choose the model — start with **Veo 3.1** (most cinematic for these dark tech shots); if the motion feels stiff, retry the same prompt on **Seedance 2.5** or **Sora 2**.
3. Generate **vertical (9:16)**, one clip per scene, using these prompts:

**Scene prompts (copy-paste each):**
```
1. Cinematic dark server room, red emergency lights, giant NVIDIA logo glitching, dramatic low angle, tech thriller style, 4K
2. Aerial shot of tech company headquarters at night, then a dark corporate boardroom door slams shut, moody cyan lighting
3. Humanoid Tesla-like robot assembling a glowing computer chip in a dark factory, sparks, cinematic, shallow depth of field
4. Futuristic Mars colony at dusk, autonomous electric cars, holographic AI interface, epic scale, lens flare
5. A giant chess move: chess pieces in a boardroom, air of scheming, moody lighting, slow push-in
6. A glowing "10%" holographic stock ticker rising above a skyline, dark tech, cyan accents
7. Empty boardroom glass table, seats around it, one silhouette sitting at the head, ominous
8. Split screen: green futuristic city accelerating (AI research, robots) vs red dark server hall, single man silhouette
9. A silhouette of a man sitting on a throne made of glowing circuit boards, world map of servers behind him, epic
10. Zoom out from a glowing orb to show Earth wrapped in a web of light networks, one figure at the center, cosmic scale
11. Freeze-frame front-facing shot, camera looks into lens, floating text bracket empty, question mark energy, loopable
```

4. Export each as **9:16, 1080×1920** (or keep higher res) with watermark OFF (free tier exports have no CapCut watermark; paid tiers also remove extra effects watermarks).

---

## Step 3 — Editing + captions (CapCut)

1. New project → **Timeline as Storyboard / Timeline**, set canvas **9:16, 1080×1920, 30fps**.
2. Import clips in order 1→11. Place the matching voiceover file on each.
3. Aim total ~45–55 s (trim each clip to its narration + ~0.5 s).
4. **Captions:** use **Auto Captions** (stylize → ALL CAPS, bold, white with black outline), punch text in at ~2.2 words/sec. Keep text above the bottom 480 px (Shorts UI overlaps the bottom ~30%).
5. **Sound:** YouTube Audio Library or CapCut Soundtrack — track type "Cinematic / Dark Tech / Suspense". Add **whoosh** SFX on each transition and a **heartbeat** layer under scene 9. Fade music to near-silence during scene 10's last line.
6. Quick cut: 1.2–1.8 s average shot length; **hard cuts**, no long dissolves.

---

## Step 4 — First frame / thumbnail

Shorts uses the first frame as the cover. Add a static opening card at 0–0.6 s: big text **"MUSK SENDS NVIDIA A DEMAND"**, red vs cyan split, lightning bolt. Use CapCut's text + the scene-1 clip frame.

---

## Step 5 — Export + YouTube settings

1. Export: **1080×1920, 30fps, H.264, high bitrate**, audio 192 kbps. File size typically 10–40 MB for this length.
2. Upload as a **Short** (YouTube auto-detects vertical < 3 min).
3. Title: `What If Elon Musk Takes Over NVIDIA?`
4. Description + hashtags → use `video_design.md` Section 4.
5. Post timing: **6–8 PM** local time. First 48 h is the algorithm test.

---

## Cost summary

- **$0 path:** ElevenLabs free minutes + CapCut free credits (a few clips/day) — export everything with no CapCut watermark. Slow but fully free.
- **~$10–20/mo path (recommended):** ElevenLabs Starter ($5) + CapCut Pro (~$10) → no wait, watermark-free, 4K, all models.

## Quality checklist before upload

- [ ] Hook line on screen in first 2 s
- [ ] ALL-CAPS captions match every spoken sentence
- [ ] Total length 45–55 s (under 60 s ideal)
- [ ] Loop-friendly ending ("What do you think? 👇") + freeze frame
- [ ] No watermark; crisp 1080×1920
