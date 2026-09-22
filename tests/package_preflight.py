"""Focused synthetic checks for the static final-game-package preflight."""
import json
from pathlib import Path
import subprocess
import sys
import zipfile

sys.dont_write_bytecode = True
SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / 'scripts'))
from verify_game_package import inspect


def exercise(base):
    results = []

    def package(name, entries):
        path = base / name
        with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
            for filename, data in entries.items():
                archive.writestr(filename, data)
        return path

    good = package('good.zip', {
        'index.html': '<link rel="stylesheet" href="assets/site.css"><script src="assets/app.js"></script>',
        'assets/site.css': 'body { background: url(./bg.png) }',
        'assets/bg.png': b'png fixture', 'assets/app.js': 'const appId = "123456";',
    })
    report = inspect(good, '4399', '123456')
    assert report['status'] == 'pass' and report['public_id_check'] == 'literal_found'
    assert '123456' not in json.dumps(report)
    results.append('complete-zip-static-references-and-id')

    report = inspect(good, '4399')
    assert report['status'] == 'needs_review' and report['public_id_check'] == 'not_requested'
    assert any('AppID binding not checked' in x for x in report['unverified'])
    results.append('unknown-id-remains-unverified')

    missing = package('missing.zip', {'index.html': '<script src="missing.js"></script>'})
    assert any('missing static asset' in x for x in inspect(missing, '233')['errors'])
    results.append('reject-missing-static-asset')

    wrong = package('wrong.zip', {'index.html':
        '<script src="https://h.api.4399.com/h5mini-2.0/h5api-interface.php"></script>',
        'src/mockReward.js': 'simulateAdSuccess();'})
    report = inspect(wrong, '233')
    assert any('wrong-channel SDK' in x for x in report['errors'])
    assert any('Test or mock' in x for x in report['errors'])
    results.append('reject-wrong-sdk-and-mock-reward')

    sensitive = package('sensitive.zip', {'index.html': '<html></html>', '.env.233': 'SECRET=fixture',
                                          'tests/test.js': '', '../escape.js': '', 'assets/Same.js': '',
                                          'assets/same.js': ''})
    report = inspect(sensitive, '233')
    assert any('Credential/development' in x for x in report['errors'])
    assert any('Unsafe ZIP path' in x for x in report['errors'])
    assert any('case-colliding' in x for x in report['errors'])
    results.append('reject-secret-test-traversal-and-case-collision')

    nested = package('nested.zip', {'game/index.html': '<script src="assets/app.js"></script>',
                                    'game/assets/app.js': 'window.toy = {};'})
    report = inspect(nested, 'bilibili-toy')
    assert report['status'] == 'pass' and report['entry'] == 'game/index.html'
    results.append('accept-toy-first-level-entry')
    bad_root = package('root-url.zip', {'index.html': '<script src="/assets/app.js"></script>',
                                        'assets/app.js': ''})
    assert any('TOY subpath' in x for x in inspect(bad_root, 'bilibili-toy')['errors'])
    results.append('reject-toy-root-absolute-url')

    xhs = package('xhs.zip', {'index.html': '<script src="https://example.test/app.js"></script>',
                              'music.mp3': b'audio'})
    report = inspect(xhs, 'xiaohongshu')
    assert any('external URL' in x for x in report['errors'])
    assert any('disallowed file type' in x for x in report['errors'])
    results.append('reject-xhs-network-and-disallowed-type')

    inline = package('inline.zip', {'index.html': '<button onclick="go()"></button><script>go()</script>'})
    assert any('inline script' in x for x in inspect(inline, 'xiaohongshu')['errors'])
    results.append('reject-xhs-inline-execution')

    crc = base / 'crc.zip'
    with zipfile.ZipFile(crc, 'w', compression=zipfile.ZIP_STORED) as archive:
        archive.writestr('index.html', 'ORIGINAL_PAYLOAD')
    data = crc.read_bytes().replace(b'ORIGINAL_PAYLOAD', b'CORRUPTED_PAYLOAD')
    crc.write_bytes(data)
    assert any('CRC/read failure' in x for x in inspect(crc, '233')['errors'])
    results.append('reject-corrupt-zip-crc')

    html = base / 'single.html'
    html.write_text('<html><script src="local.js"></script></html>', encoding='utf-8')
    assert any('local file dependency' in x for x in inspect(html, 'bilibili-toy')['errors'])
    results.append('reject-standalone-html-with-missing-local-file')

    report_path = base / 'preflight-report.json'
    args = [sys.executable, str(SKILL / 'scripts/verify_game_package.py'), str(good),
            '--channel', '4399', '--expected-public-id', '123456', '--report', str(report_path)]
    first = subprocess.run(args, capture_output=True, text=True)
    assert first.returncode == 0, first.stderr
    second = subprocess.run(args, capture_output=True, text=True)
    assert second.returncode == 2 and report_path.is_file()
    results.append('cli-no-overwrite')

    return results
