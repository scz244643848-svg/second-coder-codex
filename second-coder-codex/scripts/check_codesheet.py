"""Check exact AI header and approved-estimate-to-data-row correspondence."""
import argparse
import csv
import json
from pathlib import Path
import sys


def load(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        rows = list(csv.reader(stream))
    if not rows or not rows[0] or len(rows[0]) != len(set(rows[0])):
        raise ValueError(f'Empty or duplicate header: {path}')
    if any(len(row) != len(rows[0]) for row in rows[1:]):
        raise ValueError(f'Inconsistent row width: {path}')
    return rows[0], [dict(zip(rows[0], r)) for r in rows[1:]]


def check(template, codesheet, approved, mapping):
    header, _ = load(template)
    ai_header, ai = load(codesheet)
    ah, scope = load(approved)
    mh, links = load(mapping)
    errors = []
    if ai_header != header + ['AI_reason']:
        errors.append('AI header must equal template columns followed by AI_reason')
    if not {'estimate_key', 'paper_id'} <= set(ah) or not {'estimate_key', 'paper_id', 'codesheet_row'} <= set(mh):
        raise ValueError('Approved list/mapping missing required identity columns')
    scope_keys = [(r['paper_id'], r['estimate_key']) for r in scope]
    link_keys = [(r['paper_id'], r['estimate_key']) for r in links]
    if len(scope_keys) != len(set(scope_keys)):
        errors.append('Duplicate approved keys')
    if len(link_keys) != len(set(link_keys)):
        errors.append('Duplicate mapping keys')
    if set(scope_keys) != set(link_keys):
        errors.append('Approved and mapped keys differ (missing or extra estimates)')
    try:
        numbers = [int(r['codesheet_row']) for r in links]
        if sorted(numbers) != list(range(1, len(ai) + 1)):
            errors.append('Mapping does not cover every AI row exactly once')
    except ValueError:
        errors.append('codesheet_row must be a one-based integer')
    if any(not r.get('AI_reason', '').strip() for r in ai):
        errors.append('Empty AI_reason')
    return {'status': 'failed' if errors else 'structural_checks_passed', 'ai_rows': len(ai), 'approved_rows': len(scope), 'errors': errors, 'limitations': 'Does not verify source identity, semantics, allowed values or numerical formulas; coordinator must check these.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ['template', 'codesheet', 'approved', 'mapping']:
        p.add_argument('--' + name, type=Path, required=True)
    p.add_argument('--report', type=Path)
    args = p.parse_args()
    try:
        result = check(args.template, args.codesheet, args.approved, args.mapping)
    except (ValueError, OSError, KeyError) as error:
        result = {'status': 'failed', 'errors': [str(error)]}
    text = json.dumps(result, indent=2, ensure_ascii=False)
    if args.report:
        args.report.write_text(text, encoding='utf-8')
    print(text)
    return 1 if result['status'] == 'failed' else 0


if __name__ == '__main__':
    sys.exit(main())
