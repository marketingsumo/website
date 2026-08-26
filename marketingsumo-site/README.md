# Marketing Sumo website

Landing page + blog for marketingsumo.co. Built with [Hugo](https://gohugo.io),
hosted on Netlify. Every push to this repo rebuilds and republishes the site.

## Structure

- `static/index.html` — the landing page, served as-is at the site root.
- `content/blog/*.md` — blog posts (one Markdown file per post).
- `layouts/` — the blog design templates.
- `hugo.toml` — site config. `netlify.toml` — build settings.

## How to publish a new blog post (no tools needed)

1. Go to the `content/blog/` folder in this repo on GitHub.
2. Click **Add file → Create new file**.
3. Name it something like `my-post-title.md`.
4. Paste this at the top and edit it:

   ```
   ---
   title: "Your post title"
   date: 2026-09-01
   category: "Positioning"
   description: "One sentence shown on the blog index and in Google."
   # image: "https://link-to-a-featured-image.jpg"   ← optional cover image
   ---

   Write your post here in Markdown. ## makes a heading, **bold**, - bullet, > quote.
   ```

5. Scroll down, click **Commit changes**.
6. Wait ~1 minute. The post appears at `marketingsumo.co/blog/my-post-title/`.

To add a featured image: uncomment the `image:` line and point it at any image URL,
or upload an image into `static/images/` and use `image: "/images/your-file.jpg"`.
Posts without an image get an on-brand generated cover automatically.
