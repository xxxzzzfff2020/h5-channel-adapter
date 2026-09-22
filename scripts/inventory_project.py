#!/usr/bin/env python3
"""Read-only resource discovery; outputs metadata, never credential contents."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
from datetime import datetime, timezone

SKIP = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', '.cache',
        'backups', 'backup', 'logs', 'evidence', 'release', 'dist', 'build',
        'dist-233', 'dist-4399', 'dist-taptap', '制作缓存'}
MEDIA = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.mp4', '.webm', '.mov',
         '.m4v', '.mp3', '.wav', '.ogg', '.m4a'}
SOURCE = {'.js', '.mjs', '.cjs', '.ts', '.tsx', '.jsx', '.html', '.css',
          '.py', '.json', '.md', '.txt', '.ttf', '.woff', '.woff2', '.svg', '.lua'}


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def sensitive(path):
    n = path.name.lower()
    return (n.startswith('.env') or path.suffix.lower() in {'.pem', '.key', '.p12', '.pfx'}
            or any(x in n for x in ('secret', 'credential', 'token')))


def probe(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                        'format=format_name,duration:stream=codec_type,codec_name,width,height,r_frame_rate',
                        '-of', 'json', str(path)], capture_output=True, text=True,
                       encoding='utf-8', errors='replace', timeout=30)
    if r.returncode:
        return {'error': r.stderr.strip()[:300]}
    return json.loads(r.stdout)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('root', type=Path)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--no-probe', action='store_true')
    a = ap.parse_args()
    root, output = a.root.resolve(), a.output.resolve()
    if not root.is_dir():
        ap.error('root must be a directory')
    if output.exists():
        ap.error('output exists; choose a new evidence filename')
    files, skipped, errors = [], {'directories': 0, 'symlinks': 0, 'sensitive': 0}, []
    has_probe = bool(shutil.which('ffprobe')) and not a.no_probe
    for base, dirs, names in os.walk(root, followlinks=False):
        kept = []
        for d in sorted(dirs):
            p = Path(base) / d
            if p.is_symlink():
                skipped['symlinks'] += 1
            elif d in SKIP or d.startswith('.'):
                skipped['directories'] += 1
            else:
                kept.append(d)
        dirs[:] = kept
        for name in sorted(names):
            p = Path(base) / name
            if p == output or name == '.DS_Store':
                continue
            if p.is_symlink():
                skipped['symlinks'] += 1
                continue
            if sensitive(p):
                skipped['sensitive'] += 1
                continue
            ext = p.suffix.lower()
            rel = str(p.relative_to(root))
            try:
                before = p.stat()
                item = {'path': rel, 'bytes': before.st_size, 'sha256': digest(p),
                        'kind': ('media' if ext in MEDIA else 'source_or_document' if ext in SOURCE
                                 else 'archive' if ext in {'.zip', '.rar', '.7z', '.tar'} else 'other_resource')}
                if ext in MEDIA and has_probe:
                    item['media'] = probe(p)
                    if 'error' in item['media']:
                        errors.append({'path': rel, 'error': 'media_probe_failed'})
                after = p.stat()
                if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
                    errors.append({'path': rel, 'error': 'changed_during_inventory'})
                files.append(item)
            except (OSError, subprocess.TimeoutExpired, ValueError) as e:
                errors.append({'path': rel, 'error': str(e)[:300]})
    report = {'schema_version': 1, 'root': str(root),
              'created_at': datetime.now(timezone.utc).isoformat(),
              'ffprobe_used': has_probe, 'source_read_only': True,
              'excluded_directory_names': sorted(SKIP), 'skipped_counts': skipped,
              'files': files, 'errors': errors}
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(json.dumps({'output': str(output), 'files': len(files),
                      'media': sum(x['kind'] == 'media' for x in files),
                      'errors': len(errors), 'ffprobe_used': has_probe}, ensure_ascii=True))
    return int(bool(errors))


if __name__ == '__main__':
    raise SystemExit(main())
