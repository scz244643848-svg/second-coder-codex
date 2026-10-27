"""Organize classified research outputs into a folder with a navigable index and hashes."""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import quote
import shutil
import tempfile


CATEGORIES = {
    '01_Final_Data': 'Final researcher-approved codesheets',
    '02_Protocol_and_Template': 'Approved prompts, templates and coding-rule decisions',
    '03_Approved_Estimates': 'Approved master and per-paper estimate lists',
    '04_AI_Coding': 'Independent AI master and per-paper coding outputs',
    '05_Adjudication': 'Human inputs, comparisons, decisions, issues and mappings',
    '06_Source_Evidence': 'Source screenshots, excerpts and calculation or lookup evidence',
    '07_PDF_Reading_Aids': 'Stage 2A text, images and preparation reports',
    '08_Validation_and_Run_Records': 'Validation, provenance and run records',
    '09_Superseded': 'Clearly labeled drafts and superseded versions',
}


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def source_path(value, base):
    p = Path(value)
    return (p if p.is_absolute() else base / p).resolve(strict=True)


def destination_path(value):
    if not isinstance(value, str) or '\\' in value:
        raise ValueError('Destination must use forward slashes')
    parts = value.split('/')
    if len(parts) < 2 or parts[0] not in CATEGORIES:
        raise ValueError(f'Destination must start with an output category: {value}')
    for part in parts:
        if not part or part in ('.', '..') or part.endswith(('.', ' ')) or re.search(r'[<>:"|?*\x00-\x1f]', part):
            raise ValueError(f'Unsafe destination: {value}')
        if re.fullmatch(r'(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?', part, re.I):
            raise ValueError(f'Reserved destination filename: {value}')
    return PurePosixPath(value).as_posix()


def build(manifest_path, output):
    manifest_path = Path(manifest_path).resolve(strict=True)
    base = manifest_path.parent
    spec = json.loads(manifest_path.read_text(encoding='utf-8-sig'))
    name = spec['package_name']
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,79}', name):
        raise ValueError('package_name must be a safe folder name')
    status = spec['status']
    if status not in ('final', 'draft'):
        raise ValueError('status must be final or draft')
    output = Path(output).resolve()
    if output.exists():
        raise ValueError('Output exists; choose an unused destination folder')
    roots = [source_path(v, base) for v in spec['artifact_roots']]
    if not roots or any(not r.is_dir() for r in roots):
        raise ValueError('artifact_roots must contain designated output directories')
    if any(output.is_relative_to(root) for root in roots):
        raise ValueError('Keep the delivery folder outside the inventoried artifact roots')
    entries, destinations, sources = [], set(), set()
    for item in spec['files']:
        src = source_path(item['source'], base)
        if not src.is_file():
            raise ValueError(f'Source is not a file: {src}')
        dest = destination_path(item['destination'])
        if not item.get('description', '').strip():
            raise ValueError(f'Missing description: {dest}')
        if dest.casefold() in destinations:
            raise ValueError(f'Duplicate destination: {dest}')
        destinations.add(dest.casefold())
        sources.add(src)
        entries.append({'source': src, 'destination': dest, 'description': item['description'],
                        'size': src.stat().st_size, 'sha256': sha256(src)})
    if not entries:
        raise ValueError('No output artifacts supplied')
    # Detect paths that cannot coexist as a file and a containing directory.
    for dest in destinations:
        parents = PurePosixPath(dest).parents
        if any(str(parent) in destinations for parent in parents):
            raise ValueError(f'File/directory collision: {dest}')
    excluded = set()
    for item in spec.get('excluded', []):
        if not item.get('reason', '').strip():
            raise ValueError('Every exclusion needs a reason')
        src = source_path(item['source'], base)
        if not src.is_file() or src in sources:
            raise ValueError(f'Invalid or also-packaged exclusion: {src}')
        excluded.add(src)
    discovered = {p.resolve() for root in roots for p in root.rglob('*') if p.is_file()}
    missing = discovered - sources - excluded
    if missing:
        raise ValueError('Unaccounted generated files: ' + ', '.join(str(p) for p in sorted(missing)))
    final_files = [e for e in entries if e['destination'].startswith('01_Final_Data/')]
    if status == 'final' and not final_files:
        raise ValueError('A final package requires a final codesheet in 01_Final_Data')
    if status == 'draft' and final_files:
        raise ValueError('Draft package data must not be placed in 01_Final_Data')
    if status == 'final' and not any(e['destination'].lower().endswith(('.csv', '.xlsx')) for e in final_files):
        raise ValueError('Final data folder must include a CSV or XLSX codesheet')
    entries.sort(key=lambda e: e['destination'])
    readme = [f'# {name}', '', f'Status: **{status}**', '', spec.get('summary', ''), '', '## Codesheets to use', '']
    if final_files:
        readme += [f'- [{e["destination"]}]({quote(e["destination"])}) — {e["description"]}' for e in final_files]
    else:
        readme += ['This is a draft package. No finalized codesheet is designated.']
    readme += ['', '## Folders', '']
    for category, description in CATEGORIES.items():
        if any(e['destination'].startswith(category + '/') for e in entries):
            readme.append(f'- `{category}/`: {description}.')
    readme += ['', 'See [File_Index.csv](File_Index.csv) for every artifact and [SHA256SUMS.txt](SHA256SUMS.txt) for integrity checks.', '', '## Notes', '']
    readme += [str(n) for n in spec.get('notes', [])] or ['No additional notes supplied.']
    if spec.get('excluded'):
        readme += ['', '## Explicit inventory exclusions', '']
        readme += [f'- {Path(e["source"]).name}: {e["reason"]}' for e in spec['excluded']]
    buffer = io.StringIO(newline='')
    writer = csv.writer(buffer)
    writer.writerow(['path', 'category', 'description', 'bytes', 'sha256'])
    for e in entries:
        writer.writerow([e['destination'], e['destination'].split('/')[0], e['description'], e['size'], e['sha256']])
    generated = {'README.md': ('\n'.join(readme) + '\n').encode('utf-8'),
                 'File_Index.csv': buffer.getvalue().encode('utf-8-sig')}
    hashes = {e['destination']: e['sha256'] for e in entries}
    hashes.update({k: hashlib.sha256(v).hexdigest() for k, v in generated.items()})
    sums = ''.join(f'{value}  {key}\n' for key, value in sorted(hashes.items()))
    generated['SHA256SUMS.txt'] = sums.encode('utf-8')
    if output.suffix.lower() == '.zip':
        raise ValueError('Output must be a folder path, not a .zip path')
    output.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix='.' + output.name + '-incomplete-', dir=output.parent))
    try:
        for e in entries:
            target = staging / e['destination']
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(e['source'], target)
        for filename, contents in generated.items():
            (staging / filename).write_bytes(contents)
        for filename, expected in hashes.items():
            if sha256(staging / filename) != expected:
                raise ValueError('Copied content differs from inventory: ' + filename)
        if output.exists():
            raise ValueError('Destination appeared during copying; choose another folder')
        staging.rename(output)
    except Exception as error:
        raise ValueError(f'Output not finalized. Incomplete files retained at {staging}: {error}') from error
    return {'status': 'organized_and_hash_verified', 'output': str(output), 'artifacts': len(entries),
            'package_status': status, 'unaccounted_files': 0}



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        result = build(args.manifest, args.output)
    except (OSError, ValueError, KeyError) as error:
        print(str(error), file=sys.stderr)
        return 1
    print(json.dumps(result))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
