"""TapTap conditional scene constraints, without FFmpeg or real app data."""
import json
from unittest.mock import patch

from verify_materials import validate


def exercise(base, skill, image, item):
    results = []
    manifest = {'channel': 'taptap', 'game': 'fixture', 'source_version': 'fixture',
                'text': {}, 'processing': {'video': False}, 'files': []}
    path = base / 'tap-manifest.json'

    def check(files, expected_error=None, video=False, metadata=None):
        manifest['files'] = files
        manifest['processing']['video'] = video
        path.write_text(json.dumps(manifest))
        with patch('verify_materials.probe', return_value=metadata):
            report = validate(path, skill / 'assets/material-rules.json')
        if expected_error:
            assert any(expected_error in e for e in report['errors']), report
        else:
            assert not report['errors'], report
        assert not report['profile_complete']  # Current CLI visibility is still needed.
        return report

    check([])
    results.append('tap-invisible-windows-not-unconditionally-required')
    cover = image('tap-pc-cover.png', 460, 215)
    check([item('windows_cover', cover)])
    check([item('windows_cover', image('tap-wrong-pc-cover.png', 1920, 1080))], 'dimensions/ratio')
    results.append('tap-pc-cover-distinct-from-landscape-promo')
    landscape = image('tap-logoless.png', 1920, 1080)
    portrait = image('tap-logoless-vertical.png', 720, 1080)
    pair = [item('windows_logoless_banner', landscape), item('windows_logoless_vertical_banner', portrait)]
    check(pair[:1], 'Paired materials')
    check(pair)
    results.append('tap-logoless-pair-conditional')
    check([item('windows_logo', image('tap-wide-logo.png', 1280, 250))])
    check([item('windows_logo', image('tap-tall-logo.png', 320, 720))])
    check([item('windows_logo', image('tap-small-logo.png', 600, 400))], 'alternative minimum')
    results.append('tap-logo-width-or-height-not-both')
    shots = [item('screenshots', image('tap-shot-%d.png' % i, 720, 1280), 'screenshot_browser') for i in range(3)]
    check(shots[:2], 'minimum when provided')
    check(shots)
    check(shots[:2] + [item('screenshots', image('tap-shot-other-ratio.png', 800, 1280), 'screenshot_browser')], 'one aspect ratio')
    results.append('tap-screenshot-minimum-and-consistent-ratio')
    movie = base / 'tap-clip.mp4'
    movie.write_bytes(b'\x00\x00\x00\x18ftypisom' + b'\x00' * 20)
    metadata = {'streams': [{'codec_type': 'video', 'codec_name': 'h264', 'width': 1080, 'height': 1920}],
                'format': {'duration': '15.001'}}
    clip = item('gameplay_demo_video', movie, 'continuous_browser_capture')
    check([clip], 'Conditional material missing', video=True, metadata=metadata)
    square = item('square_promo_image', image('tap-square.png', 1440, 1440))
    check([clip, square], video=True, metadata=metadata)
    metadata['format']['duration'] = '14'
    check([clip, square], 'more than 15', video=True, metadata=metadata)
    metadata['format']['duration'] = '15'
    check([clip, square], 'more than 15', video=True, metadata=metadata)
    metadata['format']['duration'] = '15.001'
    metadata['streams'][0].update(width=1920, height=1080)
    check([clip], video=True, metadata=metadata)
    results.append('tap-portrait-gameplay-needs-square-landscape-does-not')
    results.append('tap-minimum-video-duration-exclusive-boundary')
    metadata['format']['duration'] = '15'
    trailer = item('trailer', movie, 'continuous_browser_capture')
    check([trailer], video=True, metadata=metadata)
    metadata['format']['duration'] = '14.999'
    check([trailer], 'at least 15', video=True, metadata=metadata)
    results.append('tap-trailer-inclusive-duration-boundary')
    deferred = check([clip], video=False)
    assert deferred['deferred'] and not deferred['files']
    results.append('tap-video-selection-still-respected')
    return results
