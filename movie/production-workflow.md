# Production workflow

## 1. Lock the script
Read `screenplay.md` and revise character names, dialogue, and ending before generating shots.

## 2. Create a visual bible
Keep character appearance, wardrobe, locations, lighting, lens language, and color palette consistent across all generated clips.

## 3. Generate in short shots
Use the timeline in `shot-list.md`. Generate one shot at a time, generally 5–15 seconds for coverage or longer where the chosen model supports it. Use stable character descriptions and reference frames where supported. Check the current price before every paid batch.

## 4. Track assets
For each clip record: scene/shot ID, prompt version, model, aspect ratio, duration, generation job ID, asset URL/path, status, and notes. Do not commit API keys, tokens, or private signed URLs.

## 5. Edit
Assemble clips in a video editor. Add room tone, dialogue, sound effects, music, transitions, opening titles, end credits, and subtitles. Use original or properly licensed audio.

## 6. Quality control
- Confirm the final runtime is approximately 30 minutes.
- Check character continuity and geography.
- Check dialogue intelligibility and audio levels.
- Inspect every cut for flicker, visual artifacts, and abrupt motion.
- Confirm music and sound effects are licensed.
- Export and watch the complete file before publishing.

## 7. Publish
Store the final MP4 in a suitable media host or release storage. GitHub is best for screenplay, prompts, shot tracking, and automation code—not for repeatedly committing large video files.
