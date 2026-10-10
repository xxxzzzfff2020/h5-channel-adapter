# Images and resources under CDN subdirectory deployment

Use for missing images, XML responses, dynamic resources or deployment-path checks. Reuse the project and assets without starting another device flow; device automation requires its [explicitly selected workflow](android-taptap-automation.md).

Project evidence on 2026-10-10 showed root-relative images working at a local origin root but requesting the CDN origin root after subdirectory deployment: `404` / `application/xml`. Correct package-relative URLs returned `200` / `image/webp` with bytes matching frozen assets. Local root/nested deployment checks passed after the fix, while Android retesting of the fixed package remained pending. This supports a path diagnosis, not unsupported WebP or a universal cause for missing images.

## Inspect actual requests first

Freeze the build, actual page URL/deployment prefix and entry hash. For each failing resource record the final URL including redirects, HTTP status, MIME, response bytes/magic and SHA-256 against the packaged original. A `.webp` suffix does not prove an image response; a server can even mislabel an XML error as `200`. If browser reads are restricted, use permitted network observation/raw HTTP reads without bypassing permissions or downloading unrelated media.

Inspect `img.src`, `currentSrc`, `srcset`, SVG `image` `href`/`xlink:href`, static/runtime CSS `url()`, variables/inline styles, preload references, atlases and animation-state transitions. Do not inspect only HTML or the initial state. CSS relative URLs normally resolve against the stylesheet URL; verify the actual base for JS/SVG-generated paths. `<base>` can affect `document.baseURI`, so validate before applying it universally.

At `https://cdn.example/game/build/index.html`, `/assets/hero.webp` requests the origin root; `./assets/hero.webp` resolves within the current page directory. Configure the existing build tool's relative `base` or explicit deployment prefix and fix runtime resolution consistently. Preserve official SDK URLs and intentional absolute links; do not replace every string or interpret SVG `#fragment` references as file paths.

## Decode and inspect relevant screens

- Serve the same frozen artifact at `/` and a representative nested prefix. The server must not hide wrong URLs behind HTML/false-`200` fallbacks. Cover affected pages, character states/animation changes, actual narrow screens such as 320 pixels, return and refresh; record network failures and page errors.
- `img.complete` can be true after failure. Combine `currentSrc`, `naturalWidth`/`naturalHeight` and actual [Image.decode()](https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement/decode). Detect method availability first; a missing API is not a format-decoding failure. Use existing load events, dimensions and visual evidence, leaving decode pending. For SVG/CSS backgrounds record actual URLs, load/error outcomes and image decoding, then inspect relevant screenshots or visible screens. HTTP/decode success does not establish correct occlusion, clipping or animation.
- Fix wrong paths/responses first. Investigate host format/decoder support only when correct `200` bytes still fail decoding; investigate rendering, geometry, transparency or lifecycle when decoding succeeds but drawing fails. Do not blindly convert everything to PNG, recreate assets or inherit a local-root PASS.
- Preserve asset originals, saves, economy and SDK behavior and run checks proportional to the fix. Without separate artifact-upload confirmation and matching Android retest, report local fix passed/device pending. Desktop WebP decoding does not certify Android WebView decoding.

Hash original bytes. CDP-serialized CSS/DOM may differ; one matching entry hash does not establish all resources match. Keep source, manifests, network, decode, visual and device evidence separate, with real URLs/IDs/tokens in project records only.
