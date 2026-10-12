"""Synthetic built-artifact checks for channel branding, names and resources."""
import base64
from unittest.mock import patch
import zipfile

from verify_game_package import inspect, PACKAGE_RULES
from check_package_budget import check


def exercise(base, skill):
    results = []

    def package(name, entries):
        path = base / name
        with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
            for key, value in entries.items():
                archive.writestr(key, value)
        return path

    for channel in ('233', '4399'):
        for label, html in [('text', '<p>去TapTap听完整音乐</p>'),
                            ('link', '<a href="https://www.taptap.cn/">Music</a>'),
                            ('label', '<button aria-label="TapTap music">Music</button>')]:
            artifact = package(f'brand-{channel}-{label}.zip', {'index.html': html})
            report = inspect(artifact, channel)
            assert any('HTML player text' in e for e in report['errors'])
            results.append(f'{channel}-reject-built-competing-brand-{label}')
    dynamic = package('dynamic-brand.zip', {'index.html': '<script src="app.js"></script>',
                                            'app.js': 'const hint="TapTap music";'})
    assert any('player-facing review' in u for u in inspect(dynamic, '233')['unverified'])
    assert inspect(dynamic, '233')['status'] == 'needs_review'
    results.append('dynamic-brand-needs-runtime-review')
    legal = package('legal-notice.zip', {'index.html': '<!-- TapTap legal notice --><p>Play</p>'})
    assert not inspect(legal, '233')['errors']
    results.append('legal-notice-is-not-auto-classified-as-player-copy')
    own = package('own-brand.zip', {'game/index.html': '<p>TapTap</p>'})
    assert not inspect(own, 'taptap')['errors']
    results.append('branding-policy-does-not-reject-own-platform')

    for label, name, expected in [('ascii', 'Game_(2)-v3.zip', False), ('extra-dot', 'Game.v3.zip', True),
                                  ('non-ascii', '游戏.zip', True), ('space', 'Game name.zip', True)]:
        p = package(name, {'index.html': '<p>Play</p>'})
        report = inspect(p, '4399')
        assert any('ASCII basename' in e for e in report['errors']) == expected
        results.append('4399-upload-name-' + ('reject-' if expected else 'accept-') + label)
    p = package('Game.zip', {'index.html': '<p>Play</p>'})
    size = p.stat().st_size
    assert PACKAGE_RULES['4399']['max_bytes'] == 2000000000
    with patch.dict(PACKAGE_RULES['4399'], max_bytes=size):
        assert not inspect(p, '4399')['errors']
    with patch.dict(PACKAGE_RULES['4399'], max_bytes=size - 1):
        assert any('main game-upload file exceeds' in e for e in inspect(p, '4399')['errors'])
    results.append('4399-main-file-limit-exact-and-one-byte-over')
    budget = check(p, ['xiaohongshu', 'bilibili-toy', '233', '4399'], skill/'assets/package-rules.json')
    limits = {c['channel']: c['max_bytes'] for c in budget['checks']}
    assert limits == {'xiaohongshu': 10000000, 'bilibili-toy': 140000000, '233': None, '4399': 2000000000}
    results.append('music-budgets-remain-channel-specific-and-unknown-is-not-unlimited')

    for size, status in [(100*1024, 'pass'), (100*1024+1, 'needs_review'),
                         (1024*1024, 'needs_review'), (1024*1024+1, 'fail')]:
        payload = base64.b64encode(b'0'*size).decode()
        p = package(f'embedded-{size}.zip', {'index.html': '<script src="audio.js"></script>',
                                           'audio.js': f'const audioBytes="{payload}";'})
        report = inspect(p, 'xiaohongshu')
        assert report['status'] == status, report
        assert report['embedded_resource_review'][0]['decoded_bytes'] == size
        results.append(f'xhs-embedded-budget-{size}-{status}')
    p = package('binary-renamed.zip', {'index.html': '<script src="audio.js"></script>',
                                       'audio.js': b'ID3\0\xff\xfeaudio'})
    assert any('under text extension' in e for e in inspect(p, 'xiaohongshu')['errors'])
    results.append('xhs-reject-binary-disguised-as-js')
    for tag in ('audio', 'video'):
        p = package(tag+'.zip', {'index.html': f'<{tag}><source src="data:audio/mp3;base64,AAAA"></{tag}>'})
        assert any('data/blob audio or video' in e for e in inspect(p, 'xiaohongshu')['errors'])
        results.append('xhs-reject-data-media-' + tag)
    p = package('inline-image.zip', {'index.html': '<img src="data:image/png;base64,AAAA">'})
    assert inspect(p, 'xiaohongshu')['status'] == 'pass'
    results.append('xhs-retain-allowed-data-image')
    return results
