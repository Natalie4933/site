# Natalie — A little space to be

A dark, responsive artist website for Natalie, with her Treblo banner and portrait, a music catalog and a persistent streaming player.

## Publish

1. Commit this directory's contents to `Natalie4933/site`, branch `main`.
2. In repository **Settings → Pages → Build and deployment**, choose **GitHub Actions**.
3. The **Publish Natalie site** workflow deploys on each push or manual run.
4. GitHub returns the deployed URL in the workflow's `github-pages` environment. With standard project Pages configuration the expected URL is `https://natalie4933.github.io/site/`; it is not verified until deployment succeeds.

## Local preview

Run `python3 -m http.server 8080` in this directory and visit `http://localhost:8080`.
There is no build, npm installation, API key, or backend requirement.

## Music

The player streams directly from the public Treblo CDN. The checked-in snapshot contains 12 public tracks exposed by the artist page at creation time. It is not claimed to contain every historical release. Each card links to its original Treblo song.

`python3 scripts/refresh_tracks.py` refreshes the catalog from the server-rendered public artist page and embeds it in `index.html`. The deployment workflow runs this refresh; if Treblo is unavailable it retains the previous catalog. There is no recurring schedule. The extractor depends on Treblo's current server-rendered data format and may need adjustment if that changes. The profile link always leads to the full current catalog.

Playback starts after a user interaction. Controls support play/pause, previous/next, seek, volume, mute, shuffle and repeat, plus supported operating-system media controls. Streams and cover artwork require an internet connection; unavailable streams show an actionable error and preserve a Treblo link. Audio availability and codec support depend on Treblo and the visitor's browser. No audio recordings are copied into the repository.

## Content and assets

Banner and portrait sourced from https://treblo.com/artist/natalie4933 with permission supplied by the commissioning user. Music artwork and stream addresses remain hosted by Treblo. The expanded artist copy is grounded in the supplied meditation/community brief and the public music description; no location, occupation, personal history or invented credentials are included. Fonts load from Google Fonts with system fallbacks.

## Accessibility

Responsive layout, labeled native buttons and sliders, keyboard focus, semantic headings, skip link, live playback status and reduced-motion support. Mobile playback controls sit above the device safe area.

## Verification

JavaScript syntax, HTML links and identifiers, catalog consistency, source extraction and remote audio response checks were performed. Visual browser verification was unavailable in the build environment; review desktop and mobile layout after enabling publication.
