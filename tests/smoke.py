#!/usr/bin/env python3
"""Portable, synthetic behavioral checks. Never touches real game projects."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / 'scripts'))
from inventory_project import digest
from verify_materials import validate
from extended_checks import exercise


def run(args):
    result = subprocess.run(args, capture_output=True, encoding='utf-8', errors='replace')
    if result.returncode:
        raise AssertionError(result.stderr or result.stdout)
    return result


def main():
    for tool in ('ffmpeg', 'ffprobe'):
        if not shutil.which(tool):
            raise SystemExit(tool + ' is required for synthetic media fixtures')
    results = []
    with tempfile.TemporaryDirectory(prefix='h5-adapter-') as temp:
        base = Path(temp) / '测试 assets with spaces'
        base.mkdir()
        media = base / 'media'
        media.mkdir()

        def ff(args):
            run(['ffmpeg', '-hide_banner', '-loglevel', 'error'] + args)

        def still(name, width, height):
            path = media / name
            ff(['-f', 'lavfi', '-i', f'color=c=blue:s={width}x{height}',
                '-frames:v', '1', str(path)])
            return path

        def clip(name, width, height):
            path = media / name
            ff(['-f', 'lavfi', '-i', f'color=c=red:s={width}x{height}:r=10',
                '-t', '0.6', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', str(path)])
            return path

        def item(role, path, kind='brand'):
            return {'role': role, 'path': path.relative_to(base).as_posix(),
                    'sources': [{'path': path.relative_to(base).as_posix(), 'kind': kind,
                                 'version': 'synthetic-fixture', 'sha256': digest(path)}]}

        def video(path):
            result = item('video', path, 'promo')
            result['sources'] += item('video', path, 'gameplay_browser')['sources']
            for n, source in enumerate(result['sources']):
                source.update(source_seconds=[0, 0.3], output_seconds=[n * 0.3, (n + 1) * 0.3])
            return result

        icon = still('图标 icon.png', 512, 512)
        home = still('home.jpg', 1920, 1080)
        home13 = still('home13.jpg', 1280, 1040)
        details = [still(f'detail-{i}.png', 720, 1280) for i in range(4)]
        cover = still('cover.jpg', 1280, 720)
        movie = clip('video.mp4', 1280, 720)
        manifest = {'channel': '233', 'game': '合成 fixture', 'source_version': 'synthetic-fixture',
                    'text': {'description': '测试', 'one_liner': '测试', 'recommendation': '测试'},
                    'files': [item('icon', icon), item('home_16_9', home), item('home_16_13', home13)]
                    + [item('detail', p, 'brand' if i == 0 else 'screenshot_browser')
                       for i, p in enumerate(details)] + [video(movie), item('video_cover', cover)]}

        def check(name, value, passes):
            path = base / (name + '.json')
            path.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')
            report = validate(path, SKILL / 'assets/material-rules.json')
            assert (report['technical_status'] == 'pass') == passes, (name, report['errors'])
            results.append(name)
            return path

        valid_path = check('valid-233', manifest, True)
        bad = copy.deepcopy(manifest)
        bad['files'] = [x for x in bad['files'] if x['role'] != 'video']
        check('missing-video', bad, False)
        bad = copy.deepcopy(manifest)
        bad['files'][3]['role'] = 'unknown'
        check('missing-detail-and-unknown-role', bad, False)
        bad = copy.deepcopy(manifest)
        bad['text']['recommendation'] = '字' * 26
        check('long-copy', bad, False)
        bad = copy.deepcopy(manifest)
        bad['files'][0]['path'] = home.relative_to(base).as_posix()
        check('wrong-icon-ratio', bad, False)
        bad = copy.deepcopy(manifest)
        bad['files'][-2]['sources'] = bad['files'][-2]['sources'][:1]
        check('no-gameplay-provenance', bad, False)
        bad = copy.deepcopy(manifest)
        bad['files'][0]['sources'][0]['sha256'] = '0' * 64
        check('source-hash-mismatch', bad, False)
        bad = copy.deepcopy(manifest)
        bad['files'][0]['path'] = '../escape.png'
        check('output-path-escape', bad, False)
        fake = media / 'fake.jpg'
        fake.write_bytes(icon.read_bytes())
        bad = copy.deepcopy(manifest)
        bad['files'][0]['path'] = fake.relative_to(base).as_posix()
        check('false-jpeg-extension', bad, False)

        small = still('icon-124.png', 124, 124)
        promo = still('promo-300.jpg', 300, 200)
        portrait = still('portrait.jpg', 1080, 1920)
        movie4399 = clip('video4399.mp4', 1920, 1080)
        check('valid-4399', {'channel': '4399', 'game': '合成 fixture',
                           'source_version': 'synthetic-fixture',
                           'text': {'description': '测试', 'controls': '测试'},
                           'files': [item('icon', small), item('promo', promo),
                                     item('video_cover', portrait), video(movie4399)]}, True)

        source = base / '游戏 source'
        (source / 'src').mkdir(parents=True)
        (source / 'src/main.js').write_text('const value = 1;', encoding='utf-8')
        (source / '.env').write_text('SYNTHETIC_TEST_VALUE=not-a-credential', encoding='utf-8')
        (source / 'credentials.json').write_text('{}', encoding='utf-8')
        (source / '图标.png').write_bytes(icon.read_bytes())
        (source / 'runtime.wasm').write_bytes(b'\0asm-fixture')
        (source / 'archive.zip').write_bytes(b'PK-fixture')
        (source / 'node_modules').mkdir()
        (source / 'node_modules/ignored.js').write_text('ignored', encoding='utf-8')
        symlinks = 0
        try:
            (source / 'external').symlink_to(media, target_is_directory=True)
            symlinks += 1
            (source / 'source-link.js').symlink_to(source / 'src/main.js')
            symlinks += 1
        except OSError:
            # Some Windows accounts cannot create symlinks without developer mode.
            pass
        before = digest(source / 'src/main.js')
        output = base / '盘点 report.json'
        cmd = [sys.executable, str(SKILL / 'scripts/inventory_project.py'), str(source),
               '--output', str(output)]
        stdout = json.loads(run(cmd).stdout)
        report = json.loads(output.read_text(encoding='utf-8'))
        paths = {Path(x['path']).as_posix(): x['kind'] for x in report['files']}
        assert set(paths) == {'src/main.js', '图标.png', 'runtime.wasm', 'archive.zip'}, paths
        assert paths['runtime.wasm'] == 'other_resource' and paths['archive.zip'] == 'archive'
        assert before == digest(source / 'src/main.js')
        assert report['skipped_counts']['sensitive'] == 2
        assert report['skipped_counts']['symlinks'] == symlinks
        assert stdout['errors'] == 0
        assert subprocess.run(cmd, capture_output=True).returncode != 0
        results.append('inventory-isolation-unicode-no-overwrite-and-all-resource-types')

        out = base / '校验 report.json'
        cmd = [sys.executable, str(SKILL / 'scripts/verify_materials.py'), str(valid_path),
               '--report', str(out)]
        assert json.loads(run(cmd).stdout)['technical_status'] == 'pass'
        assert json.loads(out.read_text(encoding='utf-8'))['game'] == '合成 fixture'
        assert subprocess.run(cmd, capture_output=True).returncode != 0
        results.append('validator-cli-unicode-and-no-overwrite')

        results.extend(exercise(base, SKILL, still, ff, item))

    print(json.dumps({'passed': len(results), 'cases': results,
                      'symlink_checks': symlinks, 'platform': sys.platform}))


if __name__ == '__main__':
    main()
