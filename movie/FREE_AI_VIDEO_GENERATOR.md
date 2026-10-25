# Free AI video generator for the film

## Recommended source: LTX-Video / LTX Desktop

- Official model/code: https://github.com/Lightricks/LTX-Video
- LTX Desktop (free local editor and generation app): https://ltx.io/ltx-desktop
- Official model page: https://ltx.io/model/open-source

LTX is an open-source video-generation option. Local generation does not charge per clip, but it uses your computer's hardware and storage. It is not something GitHub Actions can reliably run for free: video models need substantial GPU memory and compute. Do not add paid API keys or enable paid cloud inference unless separately approved.

## Alternative: Wan 2.1

- Official repository: https://github.com/Wan-Video/Wan2.1
- The repository states its models are licensed under Apache 2.0. Check the specific model card and requirements before use.

## Important for a phone-only workflow

GitHub stores the screenplay, shot prompts, workflow, and project files; it does not render the movie. Running a model locally is generally intended for a capable computer with a supported GPU. On an Android phone, use a reputable hosted demo only if it clearly shows a free allowance and does not ask for payment details or an API key with billing enabled. Free hosted capacity and limits can change.

## 30-minute film production plan

A 30-minute film is too long to generate as one prompt. Generate short shots, then assemble them with an editor:

1. Start with a 5–10 second test shot of the rainy Nigerian family house.
2. Review visual quality, character consistency, audio, and whether the workflow is truly free.
3. Generate shots from `shot-list.md` in small batches, keeping a reference image and prompt for Amara to improve continuity.
4. Assemble clips, dialogue, ambience, and music in a video editor; use captions where needed.
5. Export the final film and store only small project files in GitHub. Avoid committing large generated video files to normal Git history.

## Test prompt

> Cinematic supernatural mystery, rainy night in an old family house in southeastern Nigeria. A young Nigerian woman named Amara stands in a dim corridor, holding a small flashlight. Rain runs down the wooden window, a distant lightning flash briefly reveals an old family photograph, and the camera slowly pushes toward her as she hears a faint familiar woman's voice from an empty room. Naturalistic acting, restrained suspense, realistic lighting, subtle camera movement, consistent character appearance, no text or subtitles.

## Cost and safety rule

This plan is designed to start without paid generation. Before using any hosted service, verify its current free allowance. Never expose GitHub tokens, API keys, or other secrets in prompts, source files, or public repository commits.
