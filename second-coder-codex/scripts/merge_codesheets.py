"""Merge checked per-paper CSVs and adjust their auxiliary row mappings."""
import argparse
import csv
import json
from pathlib import Path
from check_codesheet import load, check


def write(path, header, rows):
    with path.open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifest', type=Path, required=True)
    p.add_argument('--template', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    entries = json.loads(args.manifest.read_text(encoding='utf-8-sig'))['papers']
    template, _ = load(args.template)
    data, links, scopes, seen = [], [], [], set()
    scope_header = None
    for item in entries:
        paths = {}
        for field in ['codesheet', 'approved', 'mapping']:
            path = Path(item[field])
            paths[field] = path if path.is_absolute() else args.manifest.resolve().parent / path
        report = check(args.template, paths['codesheet'], paths['approved'], paths['mapping'])
        if report['status'] == 'failed':
            raise ValueError(report['errors'])
        _, rows = load(paths['codesheet'])
        _, mapping = load(paths['mapping'])
        sh, approved = load(paths['approved'])
        if scope_header is None:
            scope_header = sh
        if sh != scope_header:
            raise ValueError('Per-paper approved lists must have the same header')
        for row in approved:
            key = (row['paper_id'], row['estimate_key'])
            if key in seen:
                raise ValueError(f'Duplicate approved identity across files: {key}')
            seen.add(key)
        links.extend({'estimate_key': row['estimate_key'], 'paper_id': row['paper_id'], 'codesheet_row': str(int(row['codesheet_row']) + len(data))} for row in mapping)
        data.extend(rows)
        scopes.extend(approved)
    args.output.mkdir(parents=True, exist_ok=True)
    targets = [args.output/n for n in ['AI_Codesheet.csv', 'AI_estimate_mapping.csv', 'AI_approved_estimates.csv']]
    if any(path.exists() for path in targets):
        raise ValueError('Use a new version folder; existing master files will not be overwritten')
    write(targets[0], template + ['AI_reason'], data)
    write(targets[1], ['estimate_key', 'paper_id', 'codesheet_row'], links)
    write(targets[2], scope_header or ['estimate_key', 'paper_id'], scopes)
    report = check(args.template, targets[0], targets[2], targets[1])
    (args.output/'structural_validation.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report))
    return 1 if report['status'] == 'failed' else 0


if __name__ == '__main__':
    raise SystemExit(main())
