"""Shared adjudication data: validation, confirmation receipts and audited CSVs.

Uses Python 3.10+ standard library. No model calls or external services.
"""
import argparse
import copy
import csv
import hashlib
import json
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path


def now():
    return datetime.now(timezone.utc).isoformat()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, data):
    path = Path(path)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    temp.replace(path)


def write_csv(path, columns, rows):
    with Path(path).open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def validate_review(data):
    columns = data['columns']
    if not columns or len(set(columns)) != len(columns) or not all(isinstance(c, str) and c for c in columns):
        raise ValueError('Template columns must be unique nonempty strings')
    if data['phase'] not in ('coverage', 'fields'):
        raise ValueError('phase must be coverage or fields')
    rows = data['rows']
    keys = [r['key'] for r in rows]
    if len(set(keys)) != len(keys) or not all(isinstance(k, str) and k for k in keys):
        raise ValueError('Duplicate or empty estimate keys')
    for row in rows:
        if set(row['values']) != set(columns) or not all(isinstance(v, str) for v in row['values'].values()):
            raise ValueError('Each row needs exactly the template fields as strings')
        if type(row['included']) is not bool:
            raise ValueError('Each row needs an explicit included flag')
        if data['phase'] == 'fields' and not row['included']:
            raise ValueError('Field review must contain only retained estimates')
    seen, ids = set(), set()
    for issue in data['issues']:
        if not issue['id'] or issue['id'] in ids:
            raise ValueError('Duplicate or empty issue ID')
        ids.add(issue['id'])
        if issue['field'] not in columns and not (data['phase'] == 'coverage' and issue['field'] is None):
            raise ValueError('Unknown issue field')
        if data['phase'] == 'coverage' and issue['field'] is not None:
            raise ValueError('Resolve coverage before field review')
        if not issue['members']:
            raise ValueError('Empty issue group')
        if not all(isinstance(issue[x], str) for x in ('human', 'ai', 'title', 'scope', 'rule', 'explanation', 'recommendation')):
            raise ValueError('Issue labels and comparator values must be strings')
        if data['phase'] == 'coverage' and (issue['human'] not in ('include', 'exclude') or issue['ai'] not in ('include', 'exclude')):
            raise ValueError('Coverage values must be include or exclude')
        for key in issue['members']:
            cell = (key, issue['field'])
            if key not in keys or cell in seen:
                raise ValueError('Unknown or multiply assigned estimate-field')
            seen.add(cell)
        if not issue['evidence']:
            raise ValueError('Evidence or an explicit textual fallback is required')
        for evidence in issue['evidence']:
            if not evidence.get('locator') or not evidence.get('look_at'):
                raise ValueError('Evidence needs an exact locator and what to check')
            if not evidence.get('image') and not (evidence.get('limitation') and evidence.get('excerpt')):
                raise ValueError('Missing screenshot or explained text fallback')
    return data


def prepare(source, session):
    data = validate_review(read(source))
    session.mkdir(parents=True, exist_ok=False)
    assets = session / 'assets'
    assets.mkdir()
    for issue in data['issues']:
        for evidence in issue['evidence']:
            for field in ('image', 'full_image'):
                if not evidence.get(field):
                    continue
                original = Path(evidence[field])
                if not original.is_absolute():
                    original = source.resolve().parent / original
                if original.suffix.lower() not in ('.png', '.jpg', '.jpeg', '.webp'):
                    raise ValueError('Evidence images must be PNG, JPEG or WebP')
                name = digest(original) + original.suffix.lower()
                shutil.copyfile(original, assets / name)
                evidence[field] = 'assets/' + name
                evidence[field + '_sha256'] = digest(original)
    data['prepared_at'] = now()
    save(session / 'review.json', data)
    review_hash = digest(session / 'review.json')
    save(session / 'state.json', {'review_sha256': review_hash, 'revision': 0, 'confirmed': False, 'decisions': {}, 'updated_at': now()})
    save(session / 'session.json', {'review_sha256': review_hash})
    print(json.dumps({'session': str(session.resolve()), 'status': 'ready'}))


def checked(session):
    meta, state = read(session / 'session.json'), read(session / 'state.json')
    if digest(session / 'review.json') != meta['review_sha256'] or state['review_sha256'] != meta['review_sha256']:
        raise ValueError('Review changed; prepare a new session instead of reusing decisions')
    return read(session / 'review.json'), state


def chosen(issue, decision):
    choice = decision.get('choice')
    if choice in ('human', 'ai'):
        return issue[choice]
    if choice == 'custom':
        value = decision.get('value')
        if not isinstance(value, str):
            raise ValueError('Other value must be text')
        if issue['field'] is None and value not in ('include', 'exclude'):
            raise ValueError('Choose include or exclude for coverage')
        # These constraints come from the approved codebook, not a global convention.
        if value == '' and not issue.get('allow_empty', False):
            raise ValueError('Blank is not an approved value for this issue')
        if issue.get('allowed_values') is not None and value not in issue['allowed_values']:
            raise ValueError('Value is not in the approved categories')
        if issue.get('numeric') and value not in issue.get('missing_values', []):
            try:
                if not math.isfinite(float(value)):
                    raise ValueError()
            except ValueError:
                raise ValueError('Enter a finite number or an approved missing value') from None
        return value
    if choice == 'defer':
        return None
    raise ValueError('Unknown decision')


def decision_map(data, decisions, complete=False):
    valid = {(issue['id'], key) for issue in data['issues'] for key in issue['members']}
    if not isinstance(decisions, dict) or set(decisions) - {i['id'] for i in data['issues']}:
        raise ValueError('Unknown issue in submitted decisions')
    found = set()
    for issue in data['issues']:
        entries = decisions.get(issue['id'], {})
        if not isinstance(entries, dict):
            raise ValueError('Invalid decision mapping')
        for key, decision in entries.items():
            if (issue['id'], key) not in valid:
                raise ValueError('Choice applies outside the stated group')
            value = chosen(issue, decision)
            if value is not None:
                found.add((issue['id'], key))
    if complete and found != valid:
        raise ValueError('Resolve all pending and deferred items before confirmation')


def assemble(data, state, folder):
    decision_map(data, state['decisions'], complete=True)
    rows = {r['key']: copy.deepcopy(r) for r in data['rows']}
    audit = []
    for issue in data['issues']:
        for key in issue['members']:
            decision = state['decisions'][issue['id']][key]
            value = chosen(issue, decision)
            if issue['field'] is None:
                rows[key]['included'] = value == 'include'
            else:
                rows[key]['values'][issue['field']] = value
            audit.append({'estimate_key': key, 'field': issue['field'], 'issue_id': issue['id'],
                          'human_value': issue['human'], 'ai_value': issue['ai'], 'final_value': value,
                          'choice': decision['choice'], 'researcher_note': decision.get('note', ''),
                          'rule': issue['rule'], 'issue_explanation': issue['explanation'],
                          'recommendation': issue['recommendation'], 'evidence': issue['evidence'],
                          'approval': state['confirmed_at'], 'review_sha256': state['review_sha256']})
    save(folder / 'decisions.json', audit)
    save(folder / 'reviewed_rows.json', list(rows.values()))
    retained = [r for r in rows.values() if r['included']]
    write_csv(folder / 'Reviewed_Codesheet.csv', data['columns'], [r['values'] for r in retained])
    write_csv(folder / 'estimate_mapping.csv', ['estimate_key', 'codesheet_row'],
              [{'estimate_key': r['key'], 'codesheet_row': i + 1} for i, r in enumerate(retained)])
    save(folder / 'application.json', {'status': 'awaiting_existing_finalization_checks', 'phase': data['phase'],
                                      'retained_rows': len(retained), 'decisions': len(audit),
                                      'note': 'Codex must recompute dependent fields and perform the original finalization checks.'})


def report_receipt(session):
    """Report the current saved confirmation immediately, without polling."""
    data, state = checked(session)
    folder = session / ('confirmed-' + str(state['revision']))
    result = {'confirmed': state['confirmed'], 'revision': state['revision'], 'phase': data['phase']}
    if state['confirmed']:
        # Recover a materialization interrupted after saving the durable confirmation.
        folder.mkdir(exist_ok=True)
        if not (folder / 'application.json').exists():
            save(folder / 'receipt.json', state)
            assemble(data, state, folder)
        result['confirmed_folder'] = str(folder.resolve())
    print(json.dumps(result))


def finalize(session, validation_path, output):
    data, state = checked(session)
    if data['phase'] != 'fields' or not state['confirmed']:
        raise ValueError('A confirmed field review is required')
    decision_map(data, state['decisions'], complete=True)
    folder = session / ('confirmed-' + str(state['revision']))
    receipt = folder / 'receipt.json'
    checks = read(validation_path)
    if checks.get('receipt_sha256') != digest(receipt):
        raise ValueError('Validation does not refer to the current confirmed decisions')
    required = ('coverage', 'schema', 'uniqueness', 'allowed_values', 'missing_zero', 'calculations', 'approved_corrections')
    if checks.get('status') != 'passed' or not all(checks.get('checks', {}).get(k) is True for k in required):
        raise ValueError('Original finalization checks are incomplete')
    candidate = Path(checks['candidate'])
    if not candidate.is_absolute():
        candidate = validation_path.resolve().parent / candidate
    if checks.get('candidate_sha256') != digest(candidate):
        raise ValueError('Validated candidate has changed')
    with candidate.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != data['columns']:
            raise ValueError('Candidate does not have exact template columns')
        rows = list(reader)
    base = read(folder / 'reviewed_rows.json')
    if len(rows) != len(base) or any(set(r) != set(data['columns']) or any(v is None for v in r.values()) for r in rows):
        raise ValueError('Candidate coverage or row width changed')
    # Same order as mapping. Codex may change only documented dependent calculations.
    changes = checks.get('derived_changes', [])
    approved_cells = {(i['field'], k) for i in data['issues'] for k in i['members']}
    actual = {(r['key'], c, r['values'][c], rows[n][c]) for n, r in enumerate(base)
              for c in data['columns'] if r['values'][c] != rows[n][c]}
    documented = {(x['estimate_key'], x['field'], x['before'], x['after']) for x in changes}
    if actual != documented or len(documented) != len(changes):
        raise ValueError('Candidate differs from confirmed data without exact derived-change records')
    if any((x['field'], x['estimate_key']) in approved_cells or not x.get('formula') or not x.get('inputs') for x in changes):
        raise ValueError('Do not override explicit decisions; derived changes require approved formula and inputs')
    output.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(candidate, output / 'Adjudicated_Codesheet.csv')
    shutil.copyfile(folder / 'estimate_mapping.csv', output / 'estimate_mapping.csv')
    shutil.copyfile(folder / 'decisions.json', output / 'decisions.json')
    shutil.copyfile(receipt, output / 'receipt.json')
    shutil.copyfile(validation_path, output / 'finalization_checks.json')
    save(output / 'completion.json', {'status': 'final', 'review_sha256': state['review_sha256'],
                                     'confirmed_revision': state['revision'], 'rows': len(rows),
                                     'codesheet_sha256': digest(output / 'Adjudicated_Codesheet.csv'), 'completed_at': now()})
    print(json.dumps({'status': 'final', 'codesheet': str((output / 'Adjudicated_Codesheet.csv').resolve())}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('prepare', 'receipt', 'finalize'):
        part = sub.add_parser(name)
        part.add_argument('--session', type=Path, required=True)
        if name == 'prepare':
            part.add_argument('--review', type=Path, required=True)
        if name == 'finalize':
            part.add_argument('--validation', type=Path, required=True)
            part.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.command == 'prepare':
        prepare(args.review, args.session)
    elif args.command == 'receipt':
        report_receipt(args.session)
    else:
        finalize(args.session, args.validation, args.output)


if __name__ == '__main__':
    main()
