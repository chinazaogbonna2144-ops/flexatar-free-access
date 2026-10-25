# Seedance short-film assembly

Workflow: `.github/workflows/assemble-seedance-film.yml`

The workflow assembles six 10-second Seedance 2.5 clips into a single vertical MP4 named `the-girl-who-heard-her-dead-mother-seedance.mp4` and uploads it as a GitHub Actions artifact for 30 days.

## Before running

1. Generate all six clips in Seedance 2.5 at 720p, 9:16, with audio enabled.
2. Copy each clip's downloadable HTTPS URL into the matching repository Actions secret:
   - `SEEDANCE_CLIP_1_URL`
   - `SEEDANCE_CLIP_2_URL`
   - `SEEDANCE_CLIP_3_URL`
   - `SEEDANCE_CLIP_4_URL`
   - `SEEDANCE_CLIP_5_URL`
   - `SEEDANCE_CLIP_6_URL`
3. Add secrets under **Settings → Secrets and variables → Actions → New repository secret**. Do not commit signed download URLs into the repository; they may be temporary.
4. Open **Actions → Assemble Seedance 2.5 Short Film → Run workflow** on the `video-generator` branch.
5. When the run finishes, open the workflow run and download the `the-girl-who-heard-her-dead-mother-seedance-mp4` artifact.

The workflow downloads the six clips in story order, normalizes them to 1080×1920 at 30 fps, joins them with FFmpeg, and uploads the final MP4. Download URLs must still be valid when the workflow runs. If they expire, generate fresh links and update the secrets.

## Current status

The assembly workflow is ready, but no Seedance clips have been generated yet: the video service rejected all six generation requests with `credit_admission_rejected` and reported zero credits reserved and charged. The workflow will stop with a clear message until all six URL secrets are populated.
