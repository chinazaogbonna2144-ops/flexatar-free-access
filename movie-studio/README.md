# AI Movie Studio (added without replacing Flexatar)

This app lives at **/movie-studio/** in this repository. The existing Flexatar homepage and movie notes are preserved.

## Features
- Mobile-friendly movie setup form
- Creates an editable five-scene storyboard from a story idea
- Scene prompts can be edited and saved in the browser
- Generates each scene separately through fal.ai's MiniMax Hailuo 2.3 Standard text-to-video model
- Queue status polling, video preview, and per-scene download
- Exports the storyboard as JSON

## Connect video generation
1. Create a fal.ai account and API key: https://fal.ai/dashboard/keys
2. In Cloudflare, open the Worker named `flexatar-free-access`.
3. Open **Settings → Variables and Secrets → Add**.
4. Add a secret named `FAL_KEY` and paste the fal.ai key. Do not put the key in GitHub source files or browser code.
5. Redeploy the Worker.

The GitHub Actions deployment workflow also needs the existing `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` repository secrets to deploy automatically.

## Open the app
After the Worker is deployed, open:
`https://YOUR-WORKER-DOMAIN/movie-studio/`

## Costs and limitations
- Video generation is a paid fal.ai service. Check current model pricing before generating clips.
- The app asks for confirmation before every generation request.
- This version uses text-to-video only. Image-to-video, scriptwriting with an LLM, user accounts, cloud project storage, and automatic final-video stitching are not included yet.
- Generated clip URLs are hosted by the provider and may expire. Download clips to your device promptly.
- A storyboard is saved locally in the current browser on the current device.

Model API: https://fal.ai/models/fal-ai/minimax/hailuo-2.3/standard/text-to-video/api
