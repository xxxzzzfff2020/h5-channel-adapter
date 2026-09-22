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

VIDEO_FORMATS = {'mp4', 'webm', 'ogg'}
SUFFIXES = {'png': {'.png'}, 'jpeg': {'.jpg', '.jpeg'}, 'webp': {'.webp'},
            'mp4': {'.mp4'}, 'webm': {'.webm'}, 'ogg': {'.ogg'}}


def media_format(path):
    with path.open('rb') as f:
        b = f.read(4096)
    if b.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'png'
    if b.startswith(b'\xff\xd8\xff'):
        return 'jpeg'
    if b.startswith(b'RIFF') and b[8:12] == b'WEBP':
        return 'webp'
    # EBML DocType "webm" (ID 0x4282, four-byte value).
    if b.startswith(b'\x1a\x45\xdf\xa3') and b'\x42\x82\x84webm' in b:
        return 'webm'
    if b.startswith(b'OggS'):
        return 'ogg'
    if len(b) >= 12 and b[4:8] == b'ftyp':
        return 'mp4'
    return 'unknown'


def size_ok(w, h, variant):
    rw, rh, mode = variant
    return w * rh == h * rw and (mode == 'ratio' or
                                ((w == rw and h == rh) if mode == 'exact' else (w >= rw and h >= rh)))


def validate_fields(manifest, rules, errors):
    values = manifest.get('text', {})
    for field, spec in rules['text'].items():
        # Existing v1 rules use a maximum or null and are required.
        if not isinstance(spec, dict):
            spec = {'required': True, 'min_chars': 1, 'max_chars': spec}
        value = values.get(field)
        if value is None and not spec.get('required', True):
            continue
        if not isinstance(value, str):
            errors.append('Missing/invalid text: ' + field)
            continue
        if spec.get('required', True) and not value.strip():
            errors.append('Missing text: ' + field)
        length = (len(value.encode('utf-16-le')) // 2
                  if spec.get('counting') == 'utf16_conservative' else len(value))
        maximum = spec.get('max_chars')
        if maximum is not None and length > maximum:
            errors.append('Text too long: ' + field)
        if length < spec.get('min_chars', 0):
            errors.append('Text too short: ' + field)
        if spec.get('pattern') and not re.fullmatch(spec['pattern'], value):
            errors.append('Invalid text pattern: ' + field)
        if any(c in value for c in spec.get('forbidden_chars', '')):
            errors.append('Forbidden text character: ' + field)
    metadata = manifest.get('metadata', {})
    for field, spec in rules.get('metadata', {}).items():
        value = metadata.get(field)
        if value is None and not spec.get('required', True):
            continue
        if spec['type'] == 'array':
            if not isinstance(value, list) or not all(isinstance(x, str) and x.strip() for x in value):
                errors.append('Missing/invalid metadata array: ' + field)
                continue
            if not spec.get('min_items', 0) <= len(value) <= spec.get('max_items', float('inf')):
                errors.append('Metadata count outside limits: ' + field)
            if len(set(value)) != len(value):
                errors.append('Duplicate metadata items: ' + field)
            items = value
        else:
            if not isinstance(value, str) or not value.strip():
                errors.append('Missing/invalid metadata: ' + field)
                continue
            items = [value]
        if 'choices' in spec and any(x not in spec['choices'] for x in items):
            errors.append('Unknown metadata choice: ' + field)


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
    validate_fields(m, rules, errors)
    files = m.get('files', [])
    if not isinstance(files, list) or not all(isinstance(x, dict) for x in files):
        raise ValueError('files must be an array of objects')
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
            is_video = fmt in VIDEO_FORMATS
            constraints = dict(rule)
            constraints.update(rule.get('media', {}).get('video' if is_video else 'image', {}))
            stream = next((s for s in info.get('streams', []) if s.get('codec_type') == 'video'), {})
            w, h = stream.get('width', 0), stream.get('height', 0)
            record = {'role': role, 'path': rel, 'format': fmt, 'width': w, 'height': h,
                      'bytes': p.stat().st_size, 'sha256': digest(p), 'probe': info}
            records.append(record)
            if 'error' in info:
                errors.append(f'{role}: media probe failed')
            if fmt not in constraints.get('formats', []):
                errors.append(f'{role}: format {fmt} is not {constraints.get("formats", [])}')
            if p.suffix.lower() not in SUFFIXES.get(fmt, set()):
                errors.append(f'{role}: suffix does not match actual encoding')
            if not w or not h:
                errors.append(f'{role}: no visual image/video stream')
            variants = constraints.get('variants')
            if variants and not any(size_ok(w, h, v) for v in variants):
                errors.append(f'{role}: invalid dimensions/ratio {w}x{h}')
            recommended = constraints.get('recommended_ratio', constraints.get('recommended'))
            if recommended and w and h and w * recommended[1] != h * recommended[0]:
                warnings.append(f'{role}: differs from recommended ratio {recommended[0]}:{recommended[1]} (not a hard limit)')
            limit = constraints.get('max_bytes')
            if limit is not None and record['bytes'] > limit:
                errors.append(f'{role}: exceeds {limit} bytes')
            if is_video:
                duration = float(info.get('format', {}).get('duration', 0))
                if not math.isfinite(duration) or duration <= 0:
                    errors.append('video: invalid duration')
                if constraints.get('codecs') and stream.get('codec_name') not in constraints['codecs']:
                    errors.append('video: unexpected codec')
                if constraints.get('max_duration_seconds') is not None and duration > constraints['max_duration_seconds']:
                    errors.append(f'{role}: video exceeds {constraints["max_duration_seconds"]} seconds')
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
                if is_video and kind in {'promo', 'brand', 'gameplay_browser', 'gameplay_host', 'gameplay_device'}:
                    for key in ('source_seconds', 'output_seconds'):
                        times = source.get(key)
                        valid = (isinstance(times, list) and len(times) == 2
                                 and all(isinstance(t, (int, float)) and math.isfinite(t) for t in times)
                                 and 0 <= times[0] < times[1])
                        if not valid:
                            errors.append(f'video: missing/invalid {key}')
                        elif key == 'output_seconds' and times[1] > duration + 0.1:
                            errors.append('video: segment extends beyond output duration')
            if rule.get('require_promo_gameplay'):
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
    return {'schema_version': 2, 'channel': m['channel'], 'game': m.get('game'),
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
