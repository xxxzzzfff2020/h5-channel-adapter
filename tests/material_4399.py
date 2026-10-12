"""Synthetic 4399 cover checks using real JPEGs and legal comment padding."""
import base64
import copy
import json
import struct
import zlib

from inventory_project import digest
from verify_materials import validate

# Solid-color JPEGs encoded once, decoded when prepared, then compressed here.
# No encoder or pixel-decoder dependency is needed to run the preflight tests.
JPEG = {
    'promo': 'eNr7f+P/AwYBLzdPNwZGRgYGRiBk+H+bwZmBi52dg52Ni4ODg5uLi5tPQoCPl5dPVlRMUEJZXlVFSV5JUU3bXF9N00RTUcnA0dDE0trOzk5Vz8XT2cbD3NbOGmQIIxc3Nx8vn4yAgIy1hpKGNcng/wEGQQ6GE4w6zIxKDEyCjMyCjP+PMIiCnYoCWIHCIgLoogwgxYwYitlAigUxFd9i4GFmBFrDLMhgzzCLqVGLYRTQF/y/CQA9MC63',
    'cover': 'eNrtzk1OAkEQhuFqRplOj9N2J2BYYAitEH4SkIQEzegYgyHiqfQansaFh/Bn403aGXfKyo2r96ndly9VFV/jp7j7zXYjSomoaiR+yFpMmuq0abTWmTGZ7Tib5/a4feQ7J73BaeiF/nC6mg/Hy3E/nN0slhdFWZaD2e12fXm3uiqLeokyWWZz23WuW4zCqPiz+Cxepw9754kK0vAq8Sq+SPv71R/2q7jlfqdSl9VOuVmX/W75XQ4SVZ1JvFzLU+NxIgAAAAAAAAAAAAAAAAAAAAAA4J8dxrcv1BAulA==',
    'wrong_cover': 'eNrtzs1qwkAUBeB7E2KGSTPOgIoLi2RaRS34A4JIbEpJCdW38jX6NC76AF36s/FNpkl31pVrz3d3h8O91+3dmfSmWBfETMTlkDtRTjIMRViTQohIyki1tYpj9dhsmfZTt/dsuzbpvywm/eF8mNjp+2y+TLMs640/1vnqc/GapdUSllGkYtXRupMO7CC9mduREQF5Pz5b8gz7ht03Nf9evRCUcUP/T6kq81W5VpXNdflIDz6XZ3xDb/TlbUcEAAAAAAAAAAAAcFfq7vALjhguqA==',
}


def exercise(base, skill, image, item, run):
    results = []
    rules_path = skill / 'assets/material-rules.json'
    rules = json.loads(rules_path.read_text())['channels']['4399']['roles']
    assert rules['video_cover']['max_bytes'] == 500000
    assert all(rules[role]['max_bytes'] is None for role in ('icon', 'promo', 'detail'))

    def jpeg(name, kind, size=None):
        data = zlib.decompress(base64.b64decode(JPEG[kind]))
        comments = bytearray()
        remaining = 0 if size is None else size - len(data)
        assert remaining >= 0
        while remaining:
            chunk = min(remaining, 65537)
            if 0 < remaining - chunk < 4:
                chunk -= 4
            assert chunk >= 4
            comments += b'\xff\xfe' + struct.pack('>H', chunk - 2) + b'0' * (chunk - 4)
            remaining -= chunk
        path = base / name
        path.write_bytes(data[:2] + comments + data[2:])
        if size is not None:
            assert path.stat().st_size == size
        return path

    icon = image('4399-icon.png', 124, 124)
    promo = jpeg('4399-promo.jpg', 'promo')
    cover = jpeg('4399-cover-boundary.jpg', 'cover', 500000)
    manifest = {'channel': '4399', 'game': 'synthetic fixture', 'source_version': 'fixture',
                'processing': {'video': False}, 'text': {'description': 'fixture', 'controls': 'fixture'},
                'files': [item('icon', icon), item('promo', promo), item('video_cover', cover)]}

    def verify(name, value):
        path = base / (name + '.json')
        path.write_text(json.dumps(value), encoding='utf-8')
        return path, validate(path, rules_path)

    _, report = verify('4399-exact-limit', manifest)
    assert report['technical_status'] == 'pass' and not report['profile_complete']
    checked = next(f for f in report['files'] if f['role'] == 'video_cover')
    assert (checked['width'], checked['height'], checked['bytes']) == (1080, 1920, 500000)
    assert checked['probe']['method'] == 'image_header'
    assert {d['role'] for d in report['deferred']} == {'video'}
    results.append('4399-cover-exact-byte-limit-checked-with-video-off')

    requested = copy.deepcopy(manifest)
    requested['files'][2]['target_dimensions'] = [1080, 1920]
    assert verify('4399-explicit-portrait-target', requested)[1]['technical_status'] == 'pass'
    results.append('material-explicit-width-height-target-matches')
    requested['files'][2]['target_dimensions'] = [1920, 1080]
    assert any('explicitly selected' in e for e in verify('4399-swapped-target', requested)[1]['errors'])
    results.append('material-explicit-width-height-target-rejects-swapped-orientation')
    requested['files'][2]['target_dimensions'] = [True, 1920]
    assert any('invalid target_dimensions' in e for e in verify('4399-invalid-target', requested)[1]['errors'])
    results.append('material-explicit-target-rejects-invalid-width')

    oversized = jpeg('4399-cover-one-byte-over.jpg', 'cover', 500001)
    bad = copy.deepcopy(manifest)
    bad['files'][2] = item('video_cover', oversized)
    bad_path, report = verify('4399-one-byte-over', bad)
    assert report['technical_status'] == 'fail'
    assert report['errors'] == ['video_cover: exceeds 500000 bytes']
    results.append('4399-cover-one-byte-over-fails-despite-valid-dimensions')
    output = base / '4399-cli-failure.json'
    run('verify_materials.py', [str(bad_path), '--report', str(output)], 1)
    assert json.loads(output.read_text())['technical_status'] == 'fail'
    results.append('4399-cover-cli-overflow-exits-one-and-writes-failure')

    original = jpeg('4399-original-oversized.jpg', 'cover', 594458)
    original_hash = digest(original)
    bad['files'][2] = item('video_cover', original)
    _, report = verify('4399-feedback-byte-size', bad)
    assert report['errors'] == ['video_cover: exceeds 500000 bytes']
    results.append('4399-cover-feedback-size-reproduced-with-synthetic-jpeg')
    replacement = jpeg('4399-new-candidate.jpg', 'cover', 499999)
    repaired = copy.deepcopy(bad)
    repaired['files'][2] = item('video_cover', replacement)
    path, report = verify('4399-replacement', repaired)
    output = base / '4399-cli-replacement.json'
    run('verify_materials.py', [str(path), '--report', str(output)])
    assert report['technical_status'] == 'pass' and digest(original) == original_hash
    checked = next(f for f in report['files'] if f['role'] == 'video_cover')
    assert checked['bytes'] == 499999 and checked['sha256'] != original_hash
    assert json.loads(output.read_text())['technical_status'] == 'pass'
    results.append('4399-new-candidate-rechecked-original-preserved')

    wrong = jpeg('4399-wrong-dimensions.jpg', 'wrong_cover')
    bad['files'][2] = item('video_cover', wrong)
    _, report = verify('4399-wrong-size', bad)
    assert any('invalid dimensions/ratio' in error for error in report['errors'])
    assert not any('exceeds' in error for error in report['errors'])
    results.append('4399-cover-wrong-dimensions-fail-below-byte-limit')

    large_promo = jpeg('4399-promo-unknown-limit.jpg', 'promo', 500001)
    other_role = copy.deepcopy(manifest)
    other_role['files'][1] = item('promo', large_promo)
    _, report = verify('4399-role-specific-limit', other_role)
    assert report['technical_status'] == 'pass'
    results.append('4399-cover-limit-does-not-spread-to-other-image-roles')

    omitted = copy.deepcopy(manifest)
    omitted['files'].pop()
    _, report = verify('4399-video-not-selected', omitted)
    assert report['technical_status'] == 'pass' and not report['profile_complete']
    assert {d['role'] for d in report['deferred']} == {'video', 'video_cover'}
    results.append('4399-cover-omission-remains-deferred-with-video-off')
    return results
