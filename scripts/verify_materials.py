#!/usr/bin/env python3
"""Validate explicit material manifest. Technical checks do not certify visual truth."""
import argparse
from collections import Counter
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
from inventory_project import digest, probe


def media_format(path):
    with path.open('rb') as f:
        b = f.read(64)
    if b.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'png'
    if b.startswith(b'\xff\xd8\xff'):
        return 'jpeg'
    if len(b) >= 12 and b[4:8] == b'ftyp':
        return 'mp4'
    return 'unknown'


def size_ok(w, h, variant):
    rw, rh, mode = variant
    return w * rh == h * rw and ((w == rw and h == rh) if mode == 'exact' else (w >= rw and h >= rh))


def validate(manifest_path, rules_path):
    m = json.loads(manifest_path.read_text(encoding='utf-8'))
    all_rules = json.loads(rules_path.read_text(encoding='utf-8'))['channels']
    if m.get('channel') not in all_rules:
        raise ValueError('Unknown platform; add verified platform rules first')
    rules = all_rules[m['channel']]
    errors, records, warnings = [], [], list(rules.get('unverified', []))
    base = manifest_path.parent
    for k in ('game', 'source_version'):
        if not isinstance(m.get(k), str) or not m[k].strip():
            errors.append('Missing ' + k)
    for field, maximum in rules['text'].items():
        s = m.get('text', {}).get(field)
        if not isinstance(s, str) or not s.strip():
            errors.append('Missing text: ' + field)
        elif maximum is not None and len(s) > maximum:
            errors.append('Text too long: ' + field)
    files = m.get('files', [])
    if not isinstance(files, list):
        raise ValueError('files must be an array')
    counts = Counter(x.get('role') for x in files)
    for role, rule in rules['roles'].items():
        if not rule['count'][0] <= counts[role] <= rule['count'][1]:
            errors.append(f'{role}: count {counts[role]} outside {rule["count"]}')
    for unknown in counts.keys() - rules['roles'].keys():
        errors.append('Unknown role: ' + str(unknown))
    seen, hash_cache, detail_number = set(), {}, 0
    for entry in files:
        role = entry.get('role')
        if role not in rules['roles']:
            continue
        rule = rules['roles'][role]
        if role == 'detail':
            detail_number += 1
        rel = entry.get('path')
        if not isinstance(rel, str) or not rel:
            errors.append(f'{role}: missing path')
            continue
        p = (base / rel).resolve()
        # Deliverables stay inside the material directory; sources may live elsewhere.
        if Path(rel).is_absolute() or not p.is_relative_to(base.resolve()):
            errors.append(f'{role}: deliverable path escapes manifest directory')
            continue
        if p in seen:
            errors.append(f'{role}: repeated output path {rel}')
        seen.add(p)
        if not p.is_file():
            errors.append(f'{role}: missing file {rel}')
            continue
        try:
            fmt, info = media_format(p), probe(p)
            stream = next((s for s in info.get('streams', []) if s.get('codec_type') == 'video'), {})
            w, h = stream.get('width', 0), stream.get('height', 0)
            record = {'role': role, 'path': rel, 'format': fmt, 'width': w, 'height': h,
                      'bytes': p.stat().st_size, 'sha256': digest(p), 'probe': info}
            records.append(record)
            if 'error' in info:
                errors.append(f'{role}: media probe failed')
            if fmt not in rule['formats']:
                errors.append(f'{role}: format {fmt} is not {rule["formats"]}')
            valid_suffix = {'png': {'.png'}, 'jpeg': {'.jpg', '.jpeg'}, 'mp4': {'.mp4'}}
            if p.suffix.lower() not in valid_suffix.get(fmt, set()):
                errors.append(f'{role}: suffix does not match actual encoding')
            if not any(size_ok(w, h, v) for v in rule['variants']):
                errors.append(f'{role}: invalid dimensions/ratio {w}x{h}')
            limit = rule.get('max_bytes')
            if limit is not None and record['bytes'] > limit:
                errors.append(f'{role}: exceeds {limit} bytes')
            if role == 'video':
                duration = float(info.get('format', {}).get('duration', 0))
                if not math.isfinite(duration) or duration <= 0:
                    errors.append('video: invalid duration')
                if stream.get('codec_name') not in rule['codecs']:
                    errors.append('video: unexpected codec')
            sources = entry.get('sources', [])
            if not sources:
                errors.append(f'{role}: missing provenance')
            kinds = set()
            for source in sources:
                kind = source.get('kind', '')
                kinds.add(kind)
                sp = (base / source.get('path', '')).resolve()
                expected_hash = source.get('sha256', '')
                if not sp.is_file() or not re.fullmatch(r'[0-9a-f]{64}', expected_hash):
                    errors.append(f'{role}: invalid source file/hash record')
                    continue
                if sp not in hash_cache:
                    hash_cache[sp] = digest(sp)
                if hash_cache[sp] != expected_hash:
                    errors.append(f'{role}: source hash mismatch')
                if kind.startswith(('gameplay_', 'screenshot_')):
                    if not source.get('version'):
                        errors.append(f'{role}: missing capture version')
                    elif source['version'] != m.get('source_version'):
                        warnings.append(f'{rel}: capture version differs from current source')
                if role == 'video' and kind in {'promo', 'brand'} | {'gameplay_browser', 'gameplay_host', 'gameplay_device'}:
                    for key in ('source_seconds', 'output_seconds'):
                        times = source.get(key)
                        valid = (isinstance(times, list) and len(times) == 2
                                 and all(isinstance(t, (int, float)) and math.isfinite(t) for t in times)
                                 and 0 <= times[0] < times[1])
                        if not valid:
                            errors.append(f'video: missing/invalid {key}')
                        elif key == 'output_seconds' and times[1] > duration + 0.1:
                            errors.append('video: segment extends beyond output duration')
            if role == 'video':
                if not kinds & {'promo', 'brand'} or not kinds & {'gameplay_browser', 'gameplay_host', 'gameplay_device'}:
                    errors.append('video: needs both promotional and real gameplay source records')
            if role == 'detail' and detail_number > 1 and not kinds & {'screenshot_browser', 'screenshot_host', 'screenshot_device'}:
                errors.append('detail: only first detail may use brand artwork without real screenshot')
        except (OSError, subprocess.TimeoutExpired, ValueError, TypeError) as e:
            errors.append(f'{role}: {str(e)[:250]}')
    # 233 horizontal video needs a horizontal cover, and vice versa.
    if m['channel'] == '233':
        videos = [r for r in records if r['role'] == 'video']
        covers = [r for r in records if r['role'] == 'video_cover']
        if videos and covers and (videos[0]['width'] > videos[0]['height']) != (covers[0]['width'] > covers[0]['height']):
            errors.append('video_cover: orientation differs from video')
    return {'schema_version': 1, 'channel': m['channel'], 'game': m.get('game'),
            'technical_status': 'pass' if not errors else 'fail', 'errors': errors,
            'warnings': warnings, 'files': records, 'manual_review': m.get('manual_review', {}),
            'not_certified': ['visual authenticity/quality', 'full decode and listening',
                              'current platform form', 'real SDK/device/review/release']}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('manifest', type=Path)
    ap.add_argument('--report', type=Path, required=True)
    ap.add_argument('--rules', type=Path, default=Path(__file__).resolve().parents[1] / 'assets/material-rules.json')
    a = ap.parse_args()
    if not shutil.which('ffprobe'):
        ap.error('ffprobe required; locate existing runtime before installing anything')
    if a.report.exists():
        ap.error('report exists; choose a new evidence filename')
    try:
        report = validate(a.manifest.resolve(), a.rules.resolve())
    except (ValueError, OSError, KeyError, TypeError, AttributeError) as e:
        ap.error(str(e))
    a.report.parent.mkdir(parents=True, exist_ok=True)
    with a.report.open('x', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(json.dumps({'report': str(a.report.resolve()), 'technical_status': report['technical_status'],
                      'errors': report['errors'], 'warnings': report['warnings']}, ensure_ascii=True))
    return int(bool(report['errors']))


if __name__ == '__main__':
    raise SystemExit(main())
