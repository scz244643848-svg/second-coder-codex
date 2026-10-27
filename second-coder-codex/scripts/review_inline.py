"""Prepare an in-conversation review and import researcher-confirmed host messages."""
import argparse
import base64
import copy
import hashlib
import json
import mimetypes
from pathlib import Path
import secrets
import shutil
import review_bridge as core

FORMAT = 'second-coder-inline-v1'
MAX_FRAGMENT_BYTES = 950000


def validate_decisions(data, decisions, complete=False):
    if not isinstance(decisions, dict):
        raise ValueError('Invalid decision mapping')
    for entries in decisions.values():
        if not isinstance(entries, dict):
            raise ValueError('Invalid group decisions')
        for decision in entries.values():
            if not isinstance(decision, dict):
                raise ValueError('Invalid decision record')
            if not isinstance(decision.get('note', ''), str) or type(decision.get('separate', False)) is not bool:
                raise ValueError('Invalid note or exception flag')
    core.decision_map(data, decisions, complete=complete)


def expand_groups(data, groups, complete=False):
    """Expand explicit group defaults and exceptions against the frozen membership."""
    ids = {g['id'] for g in data['issues']}
    if not isinstance(groups, dict) or set(groups) - ids or (complete and set(groups) != ids):
        raise ValueError('Unknown or missing issue groups')
    decisions = {}
    for g in data['issues']:
        entry = groups.get(g['id'], {})
        if not isinstance(entry, dict) or set(entry) - {'default', 'overrides'}:
            raise ValueError('Invalid compact group')
        overrides = entry.get('overrides', {})
        if not isinstance(overrides, dict) or set(overrides) - set(g['members']):
            raise ValueError('Exception outside the approved group')
        records = {}
        for key in g['members']:
            decision = overrides.get(key, entry.get('default'))
            if decision is not None:
                records[key] = copy.deepcopy(decision)
        if records:
            decisions[g['id']] = records
    validate_decisions(data, decisions, complete)
    return decisions


def compact_groups(data, decisions):
    groups = {}
    for g in data['issues']:
        entries = decisions.get(g['id'], {})
        votes = {}
        for key in g['members']:
            signature = json.dumps(entries.get(key), sort_keys=True)
            votes[signature] = votes.get(signature, 0) + 1
        common = json.loads(max(votes, key=votes.get))
        groups[g['id']] = {'default': common, 'overrides': {
            key: entries.get(key) for key in g['members'] if entries.get(key) != common}}
    return groups


def evidence_path(session, evidence, full=False):
    field = 'full_image' if full else 'image'
    name = evidence.get(field)
    if not name:
        raise ValueError('The requested source image is unavailable; use the recorded fallback')
    path = (session / name).resolve()
    if not path.is_relative_to((session / 'assets').resolve()):
        raise ValueError('Evidence must be a prepared session asset')
    if core.digest(path) != evidence.get(field + '_sha256'):
        raise ValueError('Evidence image changed')
    return path


def build(session):
    if (session / 'inline-pending-import.json').exists():
        raise ValueError('Recover the interrupted import before rebuilding the panel')
    data, state = core.checked(session)
    core.validate_review(data)
    validate_decisions(data, state['decisions'], state['confirmed'])
    meta_path = session / 'inline.json'
    old = core.read(meta_path) if meta_path.exists() else {}
    target = session / 'review-panel.html'
    template_path = Path(__file__).resolve().parents[1] / 'assets/grouped-review.html'
    template_hash = core.digest(template_path)
    same = (old.get('base_revision') == state['revision'] and old.get('review_sha256') == state['review_sha256'])
    if same and old.get('template_sha256') == template_hash and target.exists() and old.get('fragment_sha256') == core.digest(target):
        # Validate evidence on reuse as well as on first build.
        for g in data['issues']:
            for e in g['evidence']:
                for full, field in [(False, 'image'), (True, 'full_image')]:
                    if e.get(field):
                        evidence_path(session, e, full)
        return {'fragment': str(target.resolve()), 'reused': True, 'groups': len(data['issues'])}
    review_id = old.get('review_id') or secrets.token_hex(16)
    snapshot_id = old['snapshot_id'] if same else secrets.token_hex(16)
    seed = {'revision': 0, 'confirmed': state['confirmed'], 'groups': compact_groups(data, state['decisions'])}
    # Base data stay in the project. The panel needs issue values and row labels only.
    view = {'paper': data['paper'], 'phase': data['phase'], 'issues': data['issues'],
            'rows': [{'key': r['key'], 'label': r['label']} for r in data['rows']]}
    bundle = {'format': FORMAT, 'review_id': review_id, 'snapshot_id': snapshot_id,
              'source_review_sha256': state['review_sha256'], 'base_revision': state['revision'],
              'session': str(session.resolve()), 'review': view, 'initial_state': seed, 'images': {}}
    template = template_path.read_text(encoding='utf-8')
    if template.count('__REVIEW_BUNDLE__') != 1:
        raise ValueError('Invalid inline template')
    def render():
        payload = json.dumps(bundle, ensure_ascii=True, separators=(',', ':')).replace('<', '\\u003c')
        return template.replace('__REVIEW_BUNDLE__', payload).replace('__ROOT_ID__', 'sc-review-' + review_id)
    if len(render().encode('utf-8')) > MAX_FRAGMENT_BYTES:
        raise ValueError('The complete issue list exceeds the inline size limit. Keep all issues; shorten duplicated explanatory text without dropping values, scope or evidence, then prepare a new review.')
    # All issue groups remain present. Prefer source crops, then full pages.
    candidates, seen = [], set()
    for field in ('image', 'full_image'):
        for g in data['issues']:
            for e in g['evidence']:
                name = e.get(field)
                if name and name not in seen:
                    path = evidence_path(session, e, field == 'full_image')
                    seen.add(name)
                    candidates.append((name, path))
    for name, path in candidates:
        image = 'data:' + mimetypes.guess_type(path.name)[0] + ';base64,' + base64.b64encode(path.read_bytes()).decode('ascii')
        bundle['images'][name] = image
        if len(render().encode('utf-8')) > MAX_FRAGMENT_BYTES:
            del bundle['images'][name]
    fragment = render()
    if old:
        history = session / 'inline-history'
        history.mkdir(exist_ok=True)
        core.save(history / (old['snapshot_id'] + '.json'), old)
        if target.exists():
            shutil.copyfile(target, history / (old['snapshot_id'] + '-' + core.digest(target)[:12] + '.html'))
    target.write_text(fragment, encoding='utf-8')
    meta = {'review_id': review_id, 'snapshot_id': snapshot_id, 'review_sha256': state['review_sha256'],
            'base_revision': state['revision'], 'fragment_sha256': core.digest(target), 'template_sha256': template_hash,
            'embedded_images': len(bundle['images']), 'source_images_in_chat': len(candidates) - len(bundle['images'])}
    core.save(meta_path, meta)
    index = session / 'index.html'
    if index.exists() and '__REVIEW_BUNDLE__' in index.read_text(encoding='utf-8'):
        index.unlink()
    return {'fragment': str(target.resolve()), 'groups': len(data['issues']), 'phase': data['phase'],
            'bytes': len(fragment.encode('utf-8')), **meta}


def show_evidence(session, issue, index, full=False):
    data, _ = core.checked(session)
    group = next((g for g in data['issues'] if g['id'] == issue), None)
    if group is None or index < 0 or index >= len(group['evidence']):
        raise ValueError('Unknown issue or evidence entry')
    e = group['evidence'][index]
    return {'image': str(evidence_path(session, e, full)), 'locator': e['locator'], 'look_at': e['look_at'],
            'issue': group['id'], 'scope': group['scope'], 'field': group['field']}


def import_record_paths(history, file_hash):
    """Use short names; identify submissions only by their complete SHA-256."""
    if len(file_hash) != 64 or any(c not in '0123456789abcdef' for c in file_hash):
        raise ValueError('Invalid submission hash')
    suffix = 0
    while True:
        stem = file_hash[:12] + (f'-{suffix}' if suffix else '')
        submission = history / (stem + '.json')
        receipt = history / (stem + '.r.json')
        if receipt.exists():
            if core.read(receipt).get('file_sha256') == file_hash:
                if submission.exists() and core.digest(submission) != file_hash:
                    raise ValueError('Saved submission does not match its receipt')
                return submission, receipt
        elif not submission.exists() or core.digest(submission) == file_hash:
            return submission, receipt
        suffix += 1


def save_submission(source, target, file_hash):
    """Preserve exact submitted bytes without overwriting an occupied name."""
    try:
        with source.open('rb') as incoming, target.open('xb') as saved:
            shutil.copyfileobj(incoming, saved)
    except FileExistsError:
        pass
    if core.digest(target) != file_hash:
        raise ValueError('Saved submission differs from the confirmed file')


def import_decisions(session, source):
    pending_path = session/'inline-pending-import.json'
    if pending_path.exists():
        transaction = core.read(pending_path)
        if transaction['record']['file_sha256'] != core.digest(source):
            raise ValueError('An interrupted import must be recovered with its original decision file first')
        commit_import(session, transaction)
    data, current = core.checked(session)
    meta = core.read(session/'inline.json')
    incoming = core.read(source)
    if incoming.get('format') != FORMAT or incoming.get('kind') != 'confirmed':
        raise ValueError('A confirmed host submission is required; a draft is not approval')
    for key, expected in (('review_id',meta['review_id']),('snapshot_id',meta['snapshot_id']),
                          ('source_review_sha256',current['review_sha256']),('base_revision',meta['base_revision'])):
        if incoming.get(key) != expected:
            raise ValueError('Wrong or superseded review snapshot: '+key)
    state = incoming.get('state',{})
    revision = state.get('revision')
    if state.get('confirmed') is not True or state.get('review_sha256') != current['review_sha256']:
        raise ValueError('Missing confirmation or mismatched review')
    if type(revision) is not int or revision < 0 or not isinstance(state.get('confirmed_at'),str) or not state['confirmed_at']:
        raise ValueError('Invalid confirmed revision')
    state['decisions'] = expand_groups(data, state.get('groups'), complete=True)
    file_hash = core.digest(source)
    history = session/'inline-imports'
    history.mkdir(exist_ok=True)
    # Each import is recoverable and duplicate imports never create a new approval.
    submission_path, receipt_path = import_record_paths(history, file_hash)
    if receipt_path.exists():
        receipt = core.read(receipt_path)
        if receipt['local_revision'] != current['revision']:
            raise ValueError('This decision file is older than the current imported decisions')
        core.report_receipt(session)
        return
    previous = core.read(session/'inline-last-import.json') if (session/'inline-last-import.json').exists() else None
    if previous and previous['snapshot_id'] == meta['snapshot_id']:
        if revision == previous['panel_revision'] and current['revision'] == previous['local_revision'] and state['decisions'] == current['decisions'] and state['confirmed_at'] == current['confirmed_at']:
            # A repeated host submission may differ only in non-decision metadata.
            save_submission(source, submission_path, file_hash)
            core.save(receipt_path,{**previous,'file_sha256':file_hash,'source_name':source.name})
            core.report_receipt(session)
            return
        if revision <= previous['panel_revision']:
            raise ValueError('Stale or conflicting submission; confirm the latest panel')
        expected_local = previous['local_revision']
    else:
        expected_local = meta['base_revision']
    if current['revision'] != expected_local:
        raise ValueError('Project decisions changed after this panel was built')
    local_revision = current['revision']+1
    # Write-ahead receipt permits recovery if interrupted before state.json is replaced.
    pending = dict(file_sha256=file_hash,source_name=source.name,snapshot_id=meta['snapshot_id'],
                   panel_revision=revision,local_revision=local_revision,imported_at=core.now())
    save_submission(source, submission_path, file_hash)
    confirmed = {**current,'revision':local_revision,'confirmed':True,'decisions':state['decisions'],
                 'confirmed_at':state['confirmed_at'],'updated_at':core.now(),
                 'inline_import':pending}
    transaction=dict(record=pending,state=confirmed)
    core.save(pending_path,transaction)
    commit_import(session,transaction)
    core.report_receipt(session)

def commit_import(session, transaction):
    data,current=core.checked(session)
    pending,confirmed=transaction['record'],transaction['state']
    if current['revision'] not in (confirmed['revision']-1,confirmed['revision']) or current['review_sha256']!=confirmed['review_sha256']:
        raise ValueError('Cannot recover import over changed project state')
    if current['revision']==confirmed['revision'] and current!=confirmed:
        raise ValueError('Conflicting project state during recovery')
    validate_decisions(data,confirmed['decisions'],complete=True)
    folder=session/('confirmed-'+str(confirmed['revision']))
    folder.mkdir(exist_ok=True)
    core.save(folder/'receipt.json',confirmed)
    core.assemble(data,confirmed,folder)
    _, receipt_path = import_record_paths(session/'inline-imports', pending['file_sha256'])
    core.save(receipt_path,pending)
    core.save(session/'inline-last-import.json',pending)
    core.save(session/'state.json',confirmed)
    log=session/'events.jsonl'
    events=log.read_text(encoding='utf-8').splitlines() if log.exists() else []
    if not any(json.loads(line).get('inline_import',{}).get('file_sha256')==pending['file_sha256'] for line in events if line):
        with log.open('a',encoding='utf-8') as stream:
            stream.write(json.dumps({'event':'inline_confirm_import',**confirmed},ensure_ascii=False)+'\n')
    (session/'inline-pending-import.json').unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('prepare', 'build', 'import-decisions', 'evidence'):
        part = sub.add_parser(name)
        part.add_argument('--session', type=Path, required=True)
        if name == 'prepare':
            part.add_argument('--review', type=Path, required=True)
        if name == 'import-decisions':
            part.add_argument('--decisions', type=Path, required=True)
        if name == 'evidence':
            part.add_argument('--issue', required=True)
            part.add_argument('--index', type=int, required=True)
            part.add_argument('--full', action='store_true')
    args = parser.parse_args()
    if args.command == 'prepare':
        core.prepare(args.review, args.session)
        print(json.dumps(build(args.session)))
    elif args.command == 'build':
        print(json.dumps(build(args.session)))
    elif args.command == 'evidence':
        print(json.dumps(show_evidence(args.session, args.issue, args.index, args.full)))
    else:
        import_decisions(args.session, args.decisions)


if __name__ == '__main__':
    main()

