#!/usr/bin/env python3
"""Read-only game artifact budget check; never removes or rewrites resources."""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import re
import zipfile
from inventory_project import digest

CATEGORIES = {
    'audio': {'.mp3', '.ogg', '.wav', '.m4a', '.aac', '.flac', '.opus'},
    'video': {'.mp4', '.webm', '.mov', '.m4v', '.ogv'},
    'images': {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg', '.avif'},
    'fonts': {'.ttf', '.otf', '.woff', '.woff2'},
    'code_data': {'.html', '.htm', '.js', '.mjs', '.css', '.json', '.wasm', '.data'},
}
TEXT_EXTENSIONS = {'.html', '.htm', '.js', '.mjs', '.json', '.css'}
PER_ENTRY_SCAN = 2 * 1024 * 1024
TOTAL_SCAN = 16 * 1024 * 1024


def category(name):
    ext = Path(name).suffix.lower()
    return next((key for key, exts in CATEGORIES.items() if ext in exts), 'other')


def inspect_artifact(path):
    rows, markers, warnings = [], [], []
    extension = path.suffix.lower().lstrip('.')
    if extension == 'zip':
        if not zipfile.is_zipfile(path):
            raise ValueError('Artifact has .zip suffix but is not a ZIP')
        remaining = TOTAL_SCAN
        with zipfile.ZipFile(path) as archive:
            for item in archive.infolist():
                if item.is_dir():
                    continue
                rows.append({'path': item.filename, 'category': category(item.filename),
                             'compressed_bytes': item.compress_size, 'uncompressed_bytes': item.file_size})
                if Path(item.filename).suffix.lower() in TEXT_EXTENSIONS:
                    amount = min(PER_ENTRY_SCAN, remaining)
                    if item.file_size > amount:
                        warnings.append('Embedded-media scan incomplete: ' + item.filename)
                    if amount:
                        try:
                            with archive.open(item) as stream:
                                data = stream.read(amount)
                            remaining -= len(data)
                            kinds = sorted({match.decode('ascii').lower()
                                            for match in re.findall(rb'data:(audio|video)/', data, re.I)})
                            if kinds:
                                markers.append({'path': item.filename, 'media_types': kinds})
                        except (RuntimeError, OSError, zipfile.BadZipFile, NotImplementedError) as error:
                            warnings.append('Could not inspect embedded media: ' + item.filename + ': ' + str(error))
    elif extension in {'html', 'htm'}:
        size = path.stat().st_size
        rows.append({'path': path.name, 'category': 'code_data',
                     'compressed_bytes': size, 'uncompressed_bytes': size})
        with path.open('rb') as stream:
            data = stream.read(PER_ENTRY_SCAN)
        if size > len(data):
            warnings.append('Embedded-media scan incomplete: ' + path.name)
        kinds = sorted({match.decode('ascii').lower()
                        for match in re.findall(rb'data:(audio|video)/', data, re.I)})
        if kinds:
            markers.append({'path': path.name, 'media_types': kinds})
    else:
        raise ValueError('Provide a built game ZIP or HTML artifact, not a source directory/material archive')
    totals = defaultdict(lambda: {'files': 0, 'compressed_bytes': 0, 'uncompressed_bytes': 0})
    for item in rows:
        total = totals[item['category']]
        total['files'] += 1
        total['compressed_bytes'] += item['compressed_bytes']
        total['uncompressed_bytes'] += item['uncompressed_bytes']
    return {'format': extension, 'entries': len(rows), 'category_totals': dict(totals),
            'largest_entries': sorted(rows, key=lambda x: x['compressed_bytes'], reverse=True)[:20],
            'embedded_media_markers': markers, 'warnings': warnings,
            'notes': ['Category totals use filenames and cannot distinguish BGM from SFX or optional from essential content.',
                      'OGG may contain audio or video; inspect streams before selecting a removal plan.',
                      'ZIP upload size includes archive overhead; uncompressed source size is not the upload size.',
                      'Embedded or packed media may be counted as code/data; absence of a marker is not proof of absence.',
                      'This is a size check, not full CRC, entry-point, runtime or release verification.']}


def check(path, channels, rules_path, stage='baseline'):
    path = path.resolve()
    if not path.is_file():
        raise ValueError('Artifact must be an existing file')
    if stage not in {'baseline', 'candidate'}:
        raise ValueError('Unknown stage')
    if stage == 'candidate' and len(channels) != 1:
        raise ValueError('Check one channel per final candidate')
    rules = json.loads(rules_path.read_text(encoding='utf-8'))['channels']
    if not channels or any(c not in rules for c in channels):
        raise ValueError('Select known channels from package-rules.json')
    before = path.stat()
    inspection = inspect_artifact(path)
    sha = digest(path)
    after = path.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise ValueError('Artifact changed during inspection; freeze and retry')
    checks, errors = [], []
    for channel in dict.fromkeys(channels):
        rule = rules[channel]
        maximum = rule.get('max_bytes')
        if maximum is None:
            status = 'unknown_limit'
        else:
            status = 'over_limit' if before.st_size > maximum else 'within_limit'
        checks.append({'channel': channel, 'max_bytes': maximum, 'actual_bytes': before.st_size,
                       'over_by_bytes': max(0, before.st_size - maximum) if maximum is not None else None,
                       'budget_status': status, 'basis': rule['basis'],
                       'requires_user_choice': status == 'over_limit',
                       'next_action': ('present_measured_options_and_ask' if status == 'over_limit' else
                                       'verify_current_platform_limit' if maximum is None else
                                       'continue_adaptation_and_recheck_final_artifact')})
        if stage == 'candidate' and inspection['format'] not in rule['formats']:
            errors.append(channel + ': candidate format is not allowed')
    overall = ('invalid_candidate' if errors else
               'needs_user_choice' if any(c['budget_status'] == 'over_limit' for c in checks) else
               'needs_limit_verification' if any(c['budget_status'] == 'unknown_limit' for c in checks) else
               'within_known_limits')
    return {'schema_version': 1, 'stage': stage, 'artifact': str(path), 'sha256': sha,
            'artifact_bytes': before.st_size, 'overall_status': overall,
            'checks': checks, 'errors': errors, 'inspection': inspection,
            'source_read_only': True, 'content_reduction_authorized': False,
            'scope': 'Size/format only; user choice must be recorded separately before content removal.'}


def exit_code(report):
    return {'within_known_limits': 0, 'needs_user_choice': 1,
            'invalid_candidate': 2, 'needs_limit_verification': 3}[report['overall_status']]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('artifact', type=Path)
    ap.add_argument('--channels', nargs='+', required=True)
    ap.add_argument('--stage', choices=['baseline', 'candidate'], default='baseline')
    ap.add_argument('--report', type=Path, required=True)
    ap.add_argument('--rules', type=Path, default=Path(__file__).resolve().parents[1] / 'assets/package-rules.json')
    args = ap.parse_args()
    if args.report.exists():
        ap.error('report exists; choose a new evidence filename')
    try:
        report = check(args.artifact, args.channels, args.rules, args.stage)
    except (ValueError, OSError, KeyError, TypeError, zipfile.BadZipFile) as error:
        ap.error(str(error))
    args.report.parent.mkdir(parents=True, exist_ok=True)
    with args.report.open('x', encoding='utf-8') as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps({'report': str(args.report.resolve()), 'overall_status': report['overall_status'],
                      'checks': report['checks'], 'errors': report['errors']}, ensure_ascii=True))
    return exit_code(report)


if __name__ == '__main__':
    raise SystemExit(main())
