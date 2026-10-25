# Flexatar Free Access

A mobile-friendly free-access interface prototype for Flexatar.

- $0 free-access screen; no checkout, account, or payment processing.
- Workspace screen with local audio-file playback and microphone-permission test.
- Responsive dark violet and mint UI.
- No build step or npm dependencies required for the static interface.

## Deploy to Cloudflare Workers

This repo includes a minimal Worker that serves the static files via Cloudflare's assets binding.

1. Install Node.js and run `npx wrangler login`.
2. From this repository root, run `npx wrangler deploy`.
3. The deployed URL is shown by Wrangler.

## Important

This is a UI prototype. The original Flexatar real-time avatar engine is not integrated, so the avatar graphic is illustrative only. Audio upload plays the selected file locally; microphone button checks permission and immediately stops the test stream.