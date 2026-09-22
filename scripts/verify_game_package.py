#!/usr/bin/env python3
"""Static preflight for a built channel game artifact; not a host/runtime test."""
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path, PurePosixPath
import posixpath
import re
import stat
from urllib.parse import unquote, urlsplit
import zipfile

from inventory_project import digest

CHANNELS = {'233', '4399', 'xiaohongshu', 'bilibili-toy', 'xingxia'}
SDK_URLS = {
    '233': 'https://cdn.233xyx.com/h5ad/metah5ad_v1.min.js',
    '4399': 'https://h.api.4399.com/h5mini-2.0/h5api-interface.php',
    'bilibili-toy': 'https://s1.hdslb.com/bfs/seed/toy/app/sdk/toy-sdk.js',
    'xingxia': 'https://gz-vchar-pub.nosdn.127.net/star-letter/game-sdk/v2/sdk.iife.js',
}
TEXT_SUFFIXES = {'.html', '.htm', '.css', '.js', '.mjs', '.json'}
PER_FILE_SCAN = 24 * 1024 * 1024
TOTAL_SCAN = 32 * 1024 * 1024
TEST_CODE = re.compile(rb'\b(?:simulateAdSuccess|grantRewardForTest|mockReward|star-letter\.mock\.)\b', re.I)
WRONG_4399_API = re.compile(rb'\b(?:window\.)?H5API\b')
CSS_URL = re.compile(r'url\(\s*[\'\"]?([^\'\")]+)|@import\s+[\'\"]([^\'\"]+)', re.I)
DRIVE = re.compile(r'^[A-Za-z]:')


class HTMLRefs(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs = []
        self.scripts = []
        self.inline_scripts = 0
        self.inline_handlers = 0
        self.iframes = 0

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        for key in ('src', 'href', 'poster'):
            if values.get(key) and (key != 'href' or tag == 'link'):
                self.refs.append(values[key])
        if tag == 'script' and values.get('src'):
            self.scripts.append(values['src'])
        elif tag == 'script':
            self.inline_scripts += 1
        if tag == 'iframe':
            self.iframes += 1
        self.inline_handlers += sum(key.lower().startswith('on') for key, _ in attrs)
        for key in ('srcset', 'imagesrcset'):
            for candidate in values.get(key, '').split(','):
                if candidate.strip():
                    self.refs.append(candidate.strip().split()[0])


def unsafe_name(name):
    parts = name.split('/')
    return (not name or name.startswith('/') or '\\' in name or DRIVE.match(name)
            or any(part in {'', '.', '..'} for part in parts))


def sensitive_name(name):
    parts = [p.lower() for p in name.split('/')]
    leaf = parts[-1]
    return (any(p in {'.git', '__macosx', 'node_modules'} for p in parts)
            or leaf in {'.ds_store', 'credentials.json', 'secrets.json', 'id_rsa', 'id_ed25519'}
            or leaf.startswith('.env') or leaf.endswith(('.pem', '.p12', '.pfx', '.key')))


def test_name(name):
    parts = [p.lower() for p in name.split('/')]
    leaf = parts[-1]
    return (any(p in {'tests', '__tests__', 'evidence'} for p in parts[:-1])
            or bool(re.search(r'(?:^|[._-])(?:test|spec|mock|debug)(?:[._-]|$)', leaf))
            and Path(leaf).suffix.lower() in {'.html', '.js', '.mjs'})


def static_ref(source, target, names, channel, errors, unverified):
    target = target.strip()
    if not target or target.startswith('#') or target.startswith(('data:', 'blob:', 'javascript:')):
        if channel == 'xiaohongshu' and target.startswith(('blob:', 'javascript:')):
            errors.append(f'{source}: disallowed URL scheme in HTML/CSS')
        return
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc:
        if channel == 'xiaohongshu':
            errors.append(f'{source}: external URL in HTML/CSS')
        else:
            unverified.append(f'{source}: external dependency needs host/network review')
        return
    decoded = unquote(parsed.path)
    if decoded.startswith('/'):
        if channel == 'bilibili-toy':
            errors.append(f'{source}: root-absolute asset path breaks TOY subpath')
        else:
            unverified.append(f'{source}: root-absolute asset path needs host review')
        return
    resolved = posixpath.normpath(posixpath.join(posixpath.dirname(source), decoded))
    if resolved.startswith('../') or resolved == '..':
        errors.append(f'{source}: asset reference escapes ZIP')
    elif resolved not in names:
        errors.append(f'{source}: missing static asset {resolved}')


def inspect(path, channel, expected_public_id=None):
    if channel not in CHANNELS:
        raise ValueError('Unknown channel')
    if expected_public_id is not None and (channel != '4399' or not expected_public_id.strip()):
        raise ValueError('Expected public ID check currently applies only to 4399 and needs a nonempty value')
    if not path.is_file():
        raise ValueError('Provide an existing game ZIP or, for TOY, standalone HTML')
    before = path.stat()
    errors, unverified = [], []
    if path.suffix.lower() in {'.html', '.htm'}:
        if channel != 'bilibili-toy':
            errors.append('Standalone HTML is only supported for Bilibili TOY')
        with path.open('rb') as stream:
            data = stream.read(PER_FILE_SCAN)
        parser = HTMLRefs()
        parser.feed(data.decode('utf-8', 'replace'))
        if before.st_size > PER_FILE_SCAN:
            unverified.append('Standalone HTML exceeds static scan limit')
        for ref in parser.refs:
            if not (ref.startswith('#') or urlsplit(ref).scheme or urlsplit(ref).netloc):
                errors.append('Standalone HTML has a local file dependency: ' + ref[:120])
        for url in parser.scripts:
            for owner, official in SDK_URLS.items():
                if owner != channel and url.split('?', 1)[0] == official:
                    errors.append(f'Wrong-channel SDK script: {owner}')
        if TEST_CODE.search(data):
            errors.append('Test or mock reward marker in game code')
        entry = path.name
        names = [entry]
        checked_bytes = len(data)
    elif path.suffix.lower() == '.zip':
        if not zipfile.is_zipfile(path):
            raise ValueError('Artifact has .zip suffix but is not a ZIP')
        with zipfile.ZipFile(path) as archive:
            files = [i for i in archive.infolist() if not i.is_dir()]
            names = [i.filename for i in files]
            name_set = set(names)
            if not files:
                errors.append('ZIP contains no files')
            if len(name_set) != len(names) or len({n.casefold() for n in names}) != len(names):
                errors.append('Duplicate or case-colliding ZIP paths')
            for item in archive.infolist():
                name = item.filename
                if unsafe_name(name.rstrip('/') if item.is_dir() else name):
                    errors.append('Unsafe ZIP path: ' + name[:120])
                if stat.S_IFMT(item.external_attr >> 16) == stat.S_IFLNK:
                    errors.append('ZIP contains a symlink: ' + name[:120])
                if not item.is_dir() and sensitive_name(name):
                    errors.append('Credential/development file in ZIP: ' + name[:120])
                if not item.is_dir() and test_name(name):
                    errors.append('Test/evidence file in ZIP: ' + name[:120])
                if item.flag_bits & 0x1:
                    errors.append('Encrypted ZIP entry: ' + name[:120])
            html = [n for n in names if PurePosixPath(n).suffix.lower() in {'.html', '.htm'}]
            if channel in {'233', '4399'}:
                if 'index.html' not in name_set:
                    errors.append('Root index.html is missing')
                entry = 'index.html'
            elif channel == 'xiaohongshu':
                if len(html) != 1:
                    errors.append('Xiaohongshu package must have exactly one HTML entry')
                entry = html[0] if html else None
            else:
                valid = [n for n in names if n == 'index.html' or re.fullmatch(r'[^/]+/index\.html', n)]
                if len(valid) != 1:
                    errors.append('Expected one index.html at root or one first-level directory')
                entry = valid[0] if valid else None
            if sum(item.file_size for item in files) > 1024 * 1024 * 1024:
                unverified.append('ZIP expands beyond 1 GiB; CRC scan stopped')
            else:
                try:
                    bad_crc = archive.testzip()
                    if bad_crc:
                        errors.append('ZIP CRC/read failure: ' + bad_crc[:120])
                except (OSError, RuntimeError, zipfile.BadZipFile, NotImplementedError):
                    errors.append('ZIP CRC/read failure')
            checked_bytes = 0
            id_found = False
            for item in files:
                name = item.filename
                if PurePosixPath(name).suffix.lower() not in TEXT_SUFFIXES or unsafe_name(name):
                    continue
                remaining = TOTAL_SCAN - checked_bytes
                if remaining <= 0:
                    unverified.append('Static text scan stopped at total byte limit')
                    break
                amount = min(item.file_size, PER_FILE_SCAN, remaining)
                try:
                    with archive.open(item) as stream:
                        data = stream.read(amount)
                except (OSError, RuntimeError, zipfile.BadZipFile, NotImplementedError):
                    errors.append('Could not read ZIP entry: ' + name[:120])
                    continue
                checked_bytes += len(data)
                if len(data) < item.file_size:
                    unverified.append(name + ': static scan incomplete')
                if expected_public_id and expected_public_id.encode() in data:
                    id_found = True
                if TEST_CODE.search(data):
                    errors.append('Test or mock reward marker in game code: ' + name[:120])
                if channel == '4399' and WRONG_4399_API.search(data):
                    errors.append('4399 page-game H5API marker; expected h5api: ' + name[:120])
                suffix = PurePosixPath(name).suffix.lower()
                if suffix in {'.html', '.htm'}:
                    parser = HTMLRefs()
                    parser.feed(data.decode('utf-8', 'replace'))
                    if channel == 'xiaohongshu' and (parser.inline_scripts or parser.inline_handlers or parser.iframes):
                        errors.append(f'{name}: Xiaohongshu-disallowed inline script, event handler or iframe')
                    for ref in parser.refs:
                        static_ref(name, ref, name_set, channel, errors, unverified)
                    for url in parser.scripts:
                        for owner, official in SDK_URLS.items():
                            if owner != channel and url.split('?', 1)[0] == official:
                                errors.append(f'{name}: wrong-channel SDK script: {owner}')
                elif suffix == '.css':
                    for match in CSS_URL.finditer(data.decode('utf-8', 'replace')):
                        static_ref(name, match.group(1) or match.group(2), name_set, channel, errors, unverified)
            if expected_public_id and not id_found:
                if any('scan incomplete' in x or 'scan stopped' in x for x in unverified):
                    unverified.append('Expected public ID could not be confirmed in partial scan')
                else:
                    errors.append('Expected public ID missing from checked code/data')
            if channel == 'xiaohongshu':
                allowed = {'.html', '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.woff', '.woff2', '.json'}
                for name in names:
                    if PurePosixPath(name).suffix.lower() not in allowed:
                        errors.append('Xiaohongshu disallowed file type: ' + name[:120])
    else:
        raise ValueError('Provide a built game ZIP or TOY HTML, not a source directory/material archive')
    sha = digest(path)
    after = path.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise ValueError('Artifact changed during inspection; freeze and retry')
    if channel == '4399' and not expected_public_id:
        unverified.append('AppID binding not checked: pass --expected-public-id for a final candidate')
    unverified.append('Dynamic resource paths, SDK callbacks, host permissions and device behavior need runtime checks')
    status = 'fail' if errors else 'needs_review' if any(
        marker in note for note in unverified for marker in
        ('scan incomplete', 'scan stopped', 'static scan limit', 'could not be confirmed',
         'AppID binding not checked')) else 'pass'
    return {'schema_version': 1, 'channel': channel, 'artifact': str(path.resolve()),
            'sha256': sha, 'bytes': before.st_size, 'entry': entry, 'entries': len(names),
            'status': status, 'errors': sorted(set(errors)),
            'unverified': sorted(set(unverified)), 'static_bytes_checked': checked_bytes,
            'public_id_check': 'literal_found' if expected_public_id and not any('Expected public ID' in x for x in errors + unverified)
                               else 'missing_or_incomplete' if expected_public_id else 'not_requested',
            'scope': 'Static package checks only; no SDK, host, device, upload or review certification.'}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('artifact', type=Path)
    ap.add_argument('--channel', choices=sorted(CHANNELS), required=True)
    ap.add_argument('--expected-public-id', help='Optional public AppID to locate; value is not written to report')
    ap.add_argument('--report', type=Path, required=True)
    args = ap.parse_args()
    if args.report.exists():
        ap.error('report exists; choose a new evidence filename')
    try:
        result = inspect(args.artifact, args.channel, args.expected_public_id)
    except (ValueError, OSError, zipfile.BadZipFile, RuntimeError) as error:
        ap.error(str(error))
    args.report.parent.mkdir(parents=True, exist_ok=True)
    with args.report.open('x', encoding='utf-8') as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps({'report': str(args.report.resolve()), 'status': result['status'],
                      'errors': result['errors'], 'unverified': result['unverified']}, ensure_ascii=True))
    return {'pass': 0, 'fail': 1, 'needs_review': 3}[result['status']]


if __name__ == '__main__':
    raise SystemExit(main())
