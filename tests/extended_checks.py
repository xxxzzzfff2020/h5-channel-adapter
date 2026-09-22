"""Behavioral fixtures for supplied listing forms and actual artifact budgets."""
import base64
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import zipfile
from inventory_project import digest
from verify_materials import validate
from check_package_budget import check as budget, exit_code


def exercise(base, skill, still, ff, item):
    results = []
    rules = skill / 'assets/material-rules.json'
    package_rules = skill / 'assets/package-rules.json'
    square = still('square-small.png', 128, 128)
    wide = still('wide.png', 160, 90)
    poster = still('poster-small.jpg', 160, 120)

    def manifest(channel, text, files, metadata=None):
        return {'game': 'synthetic fixture', 'source_version': 'synthetic-fixture',
                'channel': channel, 'text': text, 'files': files, 'metadata': metadata or {}}

    def verify(name, value, expected, rule_path=rules):
        path = base / (name + '.json')
        path.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')
        report = validate(path, rule_path)
        assert (report['technical_status'] == 'pass') == expected, (name, report)
        results.append(name)
        return report

    xhs = manifest('xiaohongshu', {'name': '字' * 14, 'description': '字' * 14, 'version': 'v1'},
                   [item('icon', square)], {'scene': '休闲游戏', 'permissions': ['storage']})
    verify('xhs-valid-14-character-boundary', xhs, True)
    bad = copy.deepcopy(xhs)
    bad['text']['description'] += '字'
    verify('xhs-description-over-14', bad, False)
    bad = copy.deepcopy(xhs)
    bad['text']['name'] = '😀' * 8
    verify('xhs-conservative-emoji-count', bad, False)
    bad = copy.deepcopy(xhs)
    del bad['text']['version']
    verify('xhs-version-required', bad, False)
    bad = copy.deepcopy(xhs)
    bad['metadata']['permissions'] = ['unknown-permission']
    verify('xhs-reject-unknown-permission', bad, False)
    optional = copy.deepcopy(xhs)
    optional['files'] = [item('icon', wide)]
    report = verify('xhs-recommended-ratio-is-not-hard-limit', optional, True)
    assert any('not a hard limit' in x for x in report['warnings'])
    huge = base / 'huge-icon.png'
    huge.write_bytes(square.read_bytes())
    with huge.open('ab') as stream:
        stream.truncate(5000001)
    bad = copy.deepcopy(xhs)
    bad['files'] = [item('icon', huge)]
    verify('xhs-icon-over-five-mb', bad, False)

    toy = manifest('bilibili-toy', {'name': 'fixture', 'slug': 'fixture-game'},
                   [item('poster', poster), item('icon', square)])
    verify('toy-ratios-with-nonrecommended-pixel-sizes', toy, True)
    bad = copy.deepcopy(toy)
    bad['files'][0] = item('poster', wide)
    verify('toy-poster-hard-ratio', bad, False)
    bad = copy.deepcopy(toy)
    bad['files'][1] = item('icon', wide)
    verify('toy-icon-hard-ratio', bad, False)
    bad = copy.deepcopy(toy)
    bad['text']['slug'] = '../another'
    verify('toy-invalid-slug', bad, False)

    star = manifest('xingxia', {'name': 'fixture', 'description': 'fixture'},
                    [item('cover', wide)], {'categories': ['经营策略'], 'tags': ['经营']})
    verify('xingxia-optional-text-and-media-absent', star, True)
    bad = copy.deepcopy(star)
    bad['text']['about'] = '字' * 1001
    verify('xingxia-optional-copy-limits', bad, False)
    bad = copy.deepcopy(star)
    bad['metadata']['categories'] = ['one', 'two', 'three']
    verify('xingxia-category-count', bad, False)

    # A synthetic 1x1 WebP fixture needs no optional image encoder.
    webp = base / 'fixture.webp'
    webp.write_bytes(base64.b64decode('UklGRiIAAABXRUJQVlA4IBYAAAAwAQCdASoBAAEADsD+JaQAA3AAAAAA'))
    movie = base / 'fixture.webm'
    ff(['-f', 'lavfi', '-i', 'color=c=red:s=160x90:r=5', '-t', '0.6',
        '-c:v', 'libvpx', '-b:v', '50k', str(movie)])

    def promotional_video(path, seconds):
        entry = item('promo_media', path, 'promo')
        entry['sources'][0].update(source_seconds=[0, seconds], output_seconds=[0, seconds])
        return entry

    mixed = copy.deepcopy(star)
    mixed['files'] += [item('promo_media', webp), promotional_video(movie, 0.5)]
    for i in range(6):
        image = base / f'gallery-{i}.png'
        image.write_bytes(square.read_bytes())
        mixed['files'].append(item('promo_media', image))
    verify('xingxia-eight-mixed-items-and-promo-only-video', mixed, True)
    ninth = base / 'ninth.png'
    ninth.write_bytes(square.read_bytes())
    bad = copy.deepcopy(mixed)
    bad['files'].append(item('promo_media', ninth))
    verify('xingxia-nine-combined-items', bad, False)
    bad = copy.deepcopy(star)
    bad['files'] = [item('cover', webp)]
    verify('xingxia-cover-excludes-webp-form', bad, False)
    long_video = base / 'long-video.mp4'
    ff(['-f', 'lavfi', '-i', 'color=c=red:s=160x90:r=1', '-t', '61',
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', str(long_video)])
    bad = copy.deepcopy(star)
    bad['files'].append(promotional_video(long_video, 61))
    verify('xingxia-video-over-sixty-seconds', bad, False)
    # Generate an exact boundary; a stream-copy cut may retain a later keyframe.
    boundary = base / 'sixty-seconds.mp4'
    ff(['-f', 'lavfi', '-i', 'color=c=red:s=160x90:r=1', '-frames:v', '60',
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', str(boundary)])
    good = copy.deepcopy(star)
    good['files'].append(promotional_video(boundary, 60))
    verify('xingxia-video-sixty-second-boundary', good, True)
    padded = base / 'over-hundred-mb.mp4'
    padded.write_bytes(boundary.read_bytes())
    with padded.open('ab') as stream:
        stream.truncate(100000001)
    bad = copy.deepcopy(star)
    bad['files'].append(promotional_video(padded, 60))
    verify('xingxia-video-over-hundred-mb', bad, False)
    audio = base / 'audio-only.ogg'
    ff(['-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=mono', '-t', '0.2',
        '-c:a', 'libopus', str(audio)])
    bad = copy.deepcopy(star)
    bad['files'].append(promotional_video(audio, 0.1))
    report = verify('xingxia-audio-only-ogg-is-not-video', bad, False)
    assert any('no visual' in x for x in report['errors'])

    artifact = base / '游戏 baseline.zip'
    with zipfile.ZipFile(artifact, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr('index.html', '<video src="data:video/mp4;base64,fixture"></video>')
        archive.writestr('assets/data.js', b'0' * 11000000)
        archive.writestr('assets/theme.mp3', os.urandom(5120))
    original_hash = digest(artifact)
    report = budget(artifact, ['xiaohongshu', 'bilibili-toy', 'xingxia'], package_rules)
    assert exit_code(report) == 0
    assert report['inspection']['category_totals']['code_data']['uncompressed_bytes'] > 10000000
    assert report['artifact_bytes'] < 10000000
    assert report['inspection']['embedded_media_markers']
    assert report['inspection']['warnings']  # bounded scan reported honestly
    results.append('budget-actual-zip-not-uncompressed-source-and-inline-markers')
    local_rules = json.loads(package_rules.read_text(encoding='utf-8'))
    local_rules['channels']['xiaohongshu']['max_bytes'] = artifact.stat().st_size - 1
    custom = base / 'test-package-rules.json'
    custom.write_text(json.dumps(local_rules), encoding='utf-8')
    report = budget(artifact, ['xiaohongshu', 'bilibili-toy'], custom)
    assert exit_code(report) == 1 and report['checks'][0]['over_by_bytes'] == 1
    assert report['checks'][0]['requires_user_choice']
    assert report['checks'][1]['budget_status'] == 'within_limit'
    assert digest(artifact) == original_hash and not report['content_reduction_authorized']
    results.append('budget-one-byte-over-needs-choice-only-affected-channel-no-mutation')
    local_rules['channels']['xiaohongshu']['max_bytes'] = artifact.stat().st_size
    custom.write_text(json.dumps(local_rules), encoding='utf-8')
    assert exit_code(budget(artifact, ['xiaohongshu'], custom, 'candidate')) == 0
    results.append('budget-exact-limit-boundary')
    assert exit_code(budget(artifact, ['233', '4399'], package_rules)) == 3
    results.append('budget-unknown-not-unlimited')
    html = base / 'small.html'
    html.write_text('<html>fixture</html>', encoding='utf-8')
    assert exit_code(budget(html, ['xiaohongshu'], package_rules, 'candidate')) == 2
    assert exit_code(budget(html, ['bilibili-toy'], package_rules, 'candidate')) == 0
    results.append('budget-channel-specific-candidate-format')
    out = base / '预算 report.json'
    cmd = [sys.executable, str(skill / 'scripts/check_package_budget.py'), str(artifact),
           '--channels', '233', '--report', str(out)]
    result = subprocess.run(cmd, capture_output=True, encoding='utf-8')
    assert result.returncode == 3 and json.loads(result.stdout)['overall_status'] == 'needs_limit_verification'
    assert subprocess.run(cmd, capture_output=True).returncode == 2
    results.append('budget-cli-unicode-and-no-overwrite')
    fake = base / 'invalid.zip'
    fake.write_bytes(b'not a zip')
    try:
        budget(fake, ['xiaohongshu'], package_rules)
    except ValueError:
        results.append('budget-reject-fake-zip')
    else:
        raise AssertionError('Fake ZIP accepted')
    return results
