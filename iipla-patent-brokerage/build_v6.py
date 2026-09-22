#!/usr/bin/env python3
"""Copy-only v6 update. Preserve intake contracts, IDs and interaction code."""
import hashlib
import html
import json
import re
import sys
from pathlib import Path

BASE_SHA256 = '3ac1a0d781e2bb991e64b21ed1918b686e2d2e42a17490da78b2af4d2452fa6c'

def build(source: bytes, root: Path) -> bytes:
    if hashlib.sha256(source).hexdigest() != BASE_SHA256:
        raise ValueError('Source changed; reconcile the latest page before applying this update.')
    text = source.decode('utf-8')
    replacements = json.loads((root / 'copy-v6.json').read_text())
    for old, new in replacements:
        if old not in text:
            raise ValueError('Missing replacement target: ' + old[:100])
        text = text.replace(old, new)
    for item in json.loads((root / 'faqs-v6.json').read_text()):
        key = item['id']
        pattern = r'<details data-faq-item id="' + re.escape(key) + r'">.*?</details>'
        node = '<details data-faq-item id="' + key + '"><summary>' + html.escape(item['question']) + '</summary><p>' + item['answer'] + '</p></details>'
        if re.search(pattern, text, re.S):
            text, n = re.subn(pattern, lambda _: node, text, count=1, flags=re.S)
            assert n == 1
        else:
            parent, number = key.rsplit('-', 1)
            previous = parent + '-' + str(int(number) - 1)
            anchor = r'(<details data-faq-item id="' + re.escape(previous) + r'">.*?</details>)'
            text, n = re.subn(anchor, lambda m: m.group(0) + node, text, count=1, flags=re.S)
            assert n == 1, 'Missing insertion anchor: ' + previous
    # Counts in the no-JS view must match the interactive FAQ index.
    for key, old, new in [('getting-started', 5, 6), ('deal-options', 6, 7)]:
        pattern = r'(<a href="#faq-' + key + r'">.*?<span class="faq-nav-count">)' + str(old) + r'(</span>)'
        text, n = re.subn(pattern, lambda m: m.group(1) + str(new) + m.group(2), text, count=1)
        assert n == 1
    assert len(re.findall(r'<details data-faq-item\b', text)) == 30
    assert 'License your technology' not in text and 'license your technology' not in text
    assert 'University / technology transfer' not in text
    assert 'Patent<br>Monetization' in text
    assert "mode: 'preview'" in text and "mode:'preview'" in text
    assert 'noindex,nofollow' in text and 'privacyApproved: false' in text
    assert 'patent-monetization-2026-09-22-v2' in text and 'BP-2026-09-22-2' in text
    assert 'PM-2026-09-22-1' not in text and 'BP-2026-09-22-1' not in text
    return text.encode('utf-8')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('Usage: build_v6.py BASE.html OUTPUT.html')
    source, destination = map(Path, sys.argv[1:])
    result = build(source.read_bytes(), Path(__file__).resolve().parent)
    destination.write_bytes(result)
    print('Built', destination.name, len(result), hashlib.sha256(result).hexdigest())
