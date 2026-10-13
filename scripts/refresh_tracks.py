"""Refresh public Natalie tracks from Treblo's server-rendered artist page.
Uses only the standard library. Fails without changing the catalog on source errors.
"""
import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILE = 'https://treblo.com/artist/natalie4933'


def extract_tracks(page):
    decoder = json.JSONDecoder()
    tracks = []
    seen = set()
    for payload in re.findall(r'self\.__next_f\.push\(\[1,("(?:[^"\\]|\\.)*")\]\)', page):
        text = json.loads(payload)
        for match in re.finditer(r'\{"id":"[^"]+","artistUsername":"natalie4933"', text):
            try:
                item, _ = decoder.raw_decode(text[match.start():])
            except ValueError:
                continue
            if item['id'] in seen or not item.get('songPath') or item.get('visibility') != 'public':
                continue
            if not item['songPath'].startswith('https://cdn.treblo.com/'):
                continue
            seen.add(item['id'])
            tracks.append(dict(id=item['id'], title=item['title'].removeprefix('Natalie - '),
                               audio=item['songPath'], artwork='https://scdn.treblo.com/images/' + item['artwork'],
                               duration=item.get('duration', 0), tags=item.get('tags', []),
                               url='https://treblo.com/song/' + item['id']))
    if not tracks:
        raise RuntimeError('No public playable tracks found. Existing catalog preserved.')
    return tracks


def main():
    request = urllib.request.Request(PROFILE, headers={'User-Agent': 'NatalieArtistSite/1.0'})
    with urllib.request.urlopen(request, timeout=45) as response:
        page = response.read().decode('utf-8')
    tracks = extract_tracks(page)
    data = json.dumps(tracks, ensure_ascii=False, indent=2)
    index = ROOT / 'index.html'
    html = index.read_text()
    replacement = '<script id="track-data" type="application/json">' + data.replace('</', '<\\/') + '</script>'
    updated, count = re.subn(r'<script id="track-data" type="application/json">.*?</script>',
                             lambda _: replacement, html, flags=re.S)
    if count != 1:
        raise RuntimeError('Embedded catalog marker missing. Nothing written.')
    (ROOT / 'tracks.json').write_text(data + '\n')
    index.write_text(updated)
    print(f'Refreshed {len(tracks)} public tracks from {PROFILE}')


if __name__ == '__main__':
    main()
