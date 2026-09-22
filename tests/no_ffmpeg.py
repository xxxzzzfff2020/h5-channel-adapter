#!/usr/bin/env python3
"""Image/copy and package checks with no FFmpeg executable on PATH."""
import base64
import copy
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import zipfile
import zlib

sys.dont_write_bytecode = True
SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / 'scripts'))
from image_metadata import image_probe
from inventory_project import digest
from verify_materials import validate
from package_preflight import exercise as package_preflight

JPEG = '/9j/4AAQSkZJRgABAgAAAQABAAD//gAQTGF2YzYyLjI4LjEwMQD/2wBDAAgEBAQEBAUFBQUFBQYGBgYGBgYGBgYGBgYHBwcICAgHBwcGBgcHCAgICAkJCQgICAgJCQoKCgwMCwsODg4RERT/xABMAAEBAAAAAAAAAAAAAAAAAAAABwEBAQAAAAAAAAAAAAAAAAAABQcQAQAAAAAAAAAAAAAAAAAAAAARAQAAAAAAAAAAAAAAAAAAAAD/wAARCAAMABADASIAAhEAAxEA/9oADAMBAAIRAxEAPwCOAL+Kf//Z'
WEBP = 'UklGRiIAAABXRUJQVlA4IBYAAAAwAQCdASoBAAEADsD+JaQAA3AAAAAA'


def png(width, height):
    def chunk(kind, payload):
        return (struct.pack('>I', len(payload)) + kind + payload +
                struct.pack('>I', zlib.crc32(kind + payload)))
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)) +
            chunk(b'IDAT', zlib.compress((b'\0' + b'\x20\x80\xb0' * width) * height)) + chunk(b'IEND', b''))


def main():
    results = []
    with tempfile.TemporaryDirectory(prefix='h5-no-ffmpeg-') as tmp:
        base = Path(tmp) / '图文 assets'
        base.mkdir()
        env = dict(os.environ, PATH=str(base / 'empty-path'))

        def run(script, args, code=0):
            p = subprocess.run([sys.executable, str(SKILL / 'scripts' / script)] + args,
                               env=env, capture_output=True, encoding='utf-8', errors='replace')
            assert p.returncode == code, (script, p.stdout, p.stderr)
            return p

        def image(name, width, height):
            path = base / name
            path.write_bytes(png(width, height))
            return path

        def item(role, path, kind='brand'):
            return {'role': role, 'path': path.name, 'sources': [
                {'path': path.name, 'sha256': digest(path), 'kind': kind, 'version': 'fixture'}]}

        icon = image('icon.png', 512, 512)
        jpg = base / 'fixture.jpg'; jpg.write_bytes(base64.b64decode(JPEG))
        webp = base / 'fixture.webp'; webp.write_bytes(base64.b64decode(WEBP))
        for path, width, height in [(icon,512,512),(jpg,16,12),(webp,1,1)]:
            info = image_probe(path)
            assert 'error' not in info, info
            assert (info['streams'][0]['width'], info['streams'][0]['height']) == (width,height)
            results.append('header-' + path.suffix[1:])
        for name, data in [('bad.png', png(10,10)[:29]+b'\0'*4),
                           ('bad.jpg', b'\xff\xd8\xff\xc0\0\x11\x08'),
                           ('bad.webp', b'RIFF\0\0\0\0WEBP')]:
            path = base / name; path.write_bytes(data)
            assert 'error' in image_probe(path)
            path.unlink()
            results.append('reject-' + name)

        # Extended and lossless WebP dimension headers, without a pixel decoder.
        for kind, payload, expected in [
            (b'VP8X', b'\0'*4 + (255).to_bytes(3,'little') + (127).to_bytes(3,'little'), (256,128)),
            (b'VP8L', b'\x2f'+(4 | (6 << 14)).to_bytes(4,'little'), (5,7))]:
            chunk = kind + len(payload).to_bytes(4,'little') + payload + b'\0'*(len(payload)%2)
            path=base/'header.webp'; path.write_bytes(b'RIFF'+(4+len(chunk)).to_bytes(4,'little')+b'WEBP'+chunk)
            info=image_probe(path); frame=info['streams'][0]
            assert (frame['width'],frame['height'])==expected
            results.append('dimensions-' + kind.decode().strip())
        path.unlink()

        home=image('home.png',1920,1080); home13=image('home13.png',1280,1040)
        details=[image('detail%d.png'%n,720,1280) for n in range(4)]
        manifest={'channel':'233','game':'fixture','source_version':'fixture',
                  'processing':{'video':False}, 'text':{'description':'fixture','one_liner':'fixture','recommendation':'fixture'},
                  'files':[item('icon',icon),item('home_16_9',home),item('home_16_13',home13)] +
                          [item('detail',p,'screenshot_browser') for p in details]}
        source=base/'manifest.json'; source.write_text(json.dumps(manifest),encoding='utf-8')
        output=base/'report.json'
        run('verify_materials.py',[str(source),'--report',str(output)])
        report=json.loads(output.read_text())
        assert report['technical_status']=='pass' and not report['profile_complete']
        assert {d['role'] for d in report['deferred']}=={'video','video_cover'}
        assert all(f['probe']['method']=='image_header' for f in report['files'])
        results.append('233-images-pass-video-deferred-without-ffmpeg')
        original=digest(icon)
        run('verify_materials.py',[str(source),'--report',str(output)],2)
        assert digest(icon)==original
        results.append('no-overwrite-and-source-preserved')

        default=copy.deepcopy(manifest); default.pop('processing')
        source.write_text(json.dumps(default),encoding='utf-8')
        report=validate(source,SKILL/'assets/material-rules.json')
        assert report['processing']['video'] is False and report['technical_status']=='pass'
        results.append('omitted-video-selection-defaults-off')
        default['processing']={'video':'false'}
        source.write_text(json.dumps(default),encoding='utf-8')
        run('verify_materials.py',[str(source),'--report',str(base/'invalid-report.json')],2)
        results.append('reject-string-video-choice')

        toy={'channel':'bilibili-toy','game':'fixture','source_version':'fixture',
             'text':{'name':'fixture','slug':'fixture'}, 'files':[item('poster',jpg),item('icon',icon)]}
        source.write_text(json.dumps(toy),encoding='utf-8')
        output=base/'toy.json'; run('verify_materials.py',[str(source),'--report',str(output)])
        assert json.loads(output.read_text())['profile_complete']
        results.append('toy-jpeg-and-png-complete-without-ffmpeg')

        # A video remains untouched when skipped; selecting it requires ffprobe.
        movie=base/'pending.mp4'; movie.write_bytes(b'\x00\x00\x00\x18ftypisom'+b'\0'*12)
        manifest['files'].append(item('video',movie))
        before=digest(movie); source.write_text(json.dumps(manifest),encoding='utf-8')
        run('verify_materials.py',[str(source),'--report',str(base/'skipped.json')])
        assert digest(movie)==before
        results.append('unselected-video-not-probed-or-modified')
        manifest['processing']['video']=True
        source.write_text(json.dumps(manifest),encoding='utf-8')
        output=base/'selected.json'; run('verify_materials.py',[str(source),'--report',str(output)],1)
        report=json.loads(output.read_text())
        assert any('ffprobe' in f.get('probe',{}).get('error','') for f in report['files'])
        results.append('selected-video-missing-tool-reported')

        inventory=base/'inventory.json'
        run('inventory_project.py',[str(base),'--output',str(inventory)])
        report=json.loads(inventory.read_text())
        assert not report['ffprobe_used'] and not report['errors']
        assert any(f.get('media',{}).get('method')=='image_header' for f in report['files'])
        assert 'media' not in next(f for f in report['files'] if f['path']=='pending.mp4')
        results.append('default-inventory-inspects-images-skips-av')
        run('inventory_project.py',[str(base),'--output',str(base/'av.json'),'--probe-av'],2)
        results.append('av-inspection-requires-explicit-tool')
        artifact=base/'game.zip'
        with zipfile.ZipFile(artifact,'w') as archive: archive.writestr('index.html','<html>fixture</html>')
        run('check_package_budget.py',[str(artifact),'--channels','xiaohongshu','--report',str(base/'budget.json')])
        results.append('package-budget-without-ffmpeg')
        results.extend(package_preflight(base))
    print(json.dumps({'passed':len(results),'cases':results,'ffmpeg_on_child_path':False,'platform':sys.platform}))


if __name__=='__main__':
    main()
