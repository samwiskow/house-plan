# Kitchen, dining and living room tour

A 20-second, 1920 × 1080, 30 fps H.264 video from the approved combined
Blender scene. It has three slow camera moves and no audio:

- 0–6 seconds: kitchen island, sink and the connection to dining.
- 6–13 seconds: dining furniture, timber screen and the living area.
- 13–20 seconds: view back across living towards dining and the kitchen.

The internal folding divider stays open throughout. The source scene,
furniture, finishes and lighting are unchanged. The film uses 600 separately
rendered Cycles frames, with no generated or interpolated frames. Sampling is
16 per frame with denoising and a fixed sampling seed.

## Video

The [finished MP4](../../output/blender/room-tour/l-house-room-tour-1080p.mp4)
is stored in Git LFS. Its format report is beside it. Install Git LFS before
fetching the video, then run from the repository root:

```sh
git lfs install --local
git lfs pull --include="output/blender/room-tour/l-house-room-tour-1080p.mp4"
```

The delivered file was checked for 600 frames at 1920 × 1080 and 30 fps,
then decoded in full and played in Chrome with no dropped or corrupted frames.

## Build

Use Blender 5.2 on the Metal-capable Mac. The source combined scene is local
because it contains the licensed table asset. See `COMBINED-ROOM.md` to rebuild
it. Set the source and output paths to the local files:

```sh
blender -b --disable-autoexec --python-exit-code 1 --python scripts/blender/render_room_tour.py -- --source output/blender/combined-room/combined-kitchen-dining-living.blend --output output/blender/room-tour
python3 scripts/blender/encode_room_tour.py --frames output/blender/room-tour/frames --output output/blender/room-tour/l-house-room-tour-1080p.mp4
python3 scripts/blender/check_room_tour.py output/blender/room-tour/l-house-room-tour-1080p.mp4
```

Encoding requires FFmpeg with libx264. Pass `--ffmpeg /path/to/ffmpeg` if it
is not on PATH. The encoder preserves the sRGB transfer function of the
rendered images, converts to limited-range BT.709 YUV and writes explicit
colour tags. The MP4 header is placed first for browser playback.

Use `--preview --samples 8` for nine 960 × 540 camera checks. `--start` and
`--end` restrict the rendered frame range. Existing final frames are retained
when resuming; use a new output directory after changing the camera or scene.

The source and animated `.blend` files and intermediate frames stay local.
The video and its format report are the deliverables. Check playback and shot
transitions as well as the format report before sharing the result.
