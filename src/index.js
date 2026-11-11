const MODEL_ID = "fal-ai/minimax/hailuo-2.3/standard/text-to-video";
const FAL_BASE = "https://queue.fal.run";

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" }
  });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/api/health") {
      return json({ ok: true, configured: Boolean(env.FAL_KEY), model: MODEL_ID });
    }

    if (url.pathname === "/api/video" && request.method === "POST") {
      if (!env.FAL_KEY) return json({ error: "Video generation is not connected yet. Add FAL_KEY to your Cloudflare Worker secrets." }, 503);
      let body;
      try { body = await request.json(); } catch { return json({ error: "Send valid JSON." }, 400); }
      const prompt = typeof body.prompt === "string" ? body.prompt.trim() : "";
      const duration = String(body.duration || "6");
      if (prompt.length < 12 || prompt.length > 2000) return json({ error: "Scene prompt must be between 12 and 2,000 characters." }, 400);
      if (!["6", "10"].includes(duration)) return json({ error: "Choose a 6- or 10-second scene." }, 400);

      const upstream = await fetch(FAL_BASE + "/" + MODEL_ID, {
        method: "POST",
        headers: { "Authorization": "Key " + env.FAL_KEY, "Content-Type": "application/json" },
        body: JSON.stringify({ prompt, duration, enable_safety_checker: true, prompt_optimizer: true })
      });
      const data = await upstream.json().catch(() => ({}));
      if (!upstream.ok) return json({ error: data.detail || data.error || "The video provider rejected the request.", providerStatus: upstream.status }, upstream.status);
      return json({ request_id: data.request_id, status: data.status || "IN_QUEUE", status_url: data.status_url, model: MODEL_ID }, 202);
    }

    const statusMatch = url.pathname.match(/^\/api\/video\/([0-9a-f-]{20,})$/i);
    if (statusMatch && request.method === "GET") {
      if (!env.FAL_KEY) return json({ error: "Video provider is not configured." }, 503);
      const requestId = statusMatch[1];
      const statusResponse = await fetch(FAL_BASE + "/" + MODEL_ID + "/requests/" + requestId + "/status", {
        headers: { "Authorization": "Key " + env.FAL_KEY }
      });
      const statusData = await statusResponse.json().catch(() => ({}));
      if (!statusResponse.ok) return json({ error: statusData.detail || "Could not check video status." }, statusResponse.status);
      if (statusData.status !== "COMPLETED") return json({ status: statusData.status, queue_position: statusData.queue_position ?? null });

      const resultResponse = await fetch(FAL_BASE + "/" + MODEL_ID + "/requests/" + requestId, {
        headers: { "Authorization": "Key " + env.FAL_KEY }
      });
      const resultData = await resultResponse.json().catch(() => ({}));
      if (!resultResponse.ok) return json({ error: resultData.detail || "Video result is not ready." }, resultResponse.status);
      if (resultData.video?.url) return json({ status: "COMPLETED", video_url: resultData.video.url });
      return json({ status: "FAILED", error: "The provider completed the job but returned no video URL." }, 502);
    }

    return env.ASSETS.fetch(request);
  }
};
