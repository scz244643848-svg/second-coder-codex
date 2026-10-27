"""Prepare a data-free inline capability check and verify its returned message.

Python 3.10+ standard library only. This never approves scientific decisions.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import secrets

FORMAT = 'second-coder-client-check-v1'
START = 'SECOND_CODER_COMPATIBILITY_CHECK'
END = 'END_SECOND_CODER_COMPATIBILITY_CHECK'

def now():
    return datetime.now(timezone.utc).isoformat()

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def save(path, value):
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    tmp.replace(path)

def prepared(folder):
    meta = read(folder / 'check.json')
    if meta.get('format') != FORMAT or meta.get('status') not in ('prepared', 'passed'):
        raise ValueError('Not a recognized compatibility check')
    if digest(folder / 'compatibility-check.html') != meta['fragment_sha256']:
        raise ValueError('The saved check fragment changed; use a new check folder')
    return meta

def prepare(folder):
    folder = folder.resolve()
    if folder.exists():
        meta = prepared(folder)
        return {'fragment': str(folder / 'compatibility-check.html'), 'reused': True, **meta}
    template = (Path(__file__).resolve().parents[1] / 'assets/compatibility-check.html').read_text(encoding='utf-8')
    if template.count('__CHECK_BUNDLE__') != 1:
        raise ValueError('Invalid compatibility template')
    check_id = secrets.token_hex(16)
    bundle = json.dumps({'format': FORMAT, 'check_id': check_id}, separators=(',', ':'))
    fragment = template.replace('__CHECK_ROOT__', 'second-coder-check-' + check_id).replace('__CHECK_BUNDLE__', bundle.replace('<', '\\u003c'))
    folder.mkdir(parents=True, exist_ok=False)
    target = folder / 'compatibility-check.html'
    target.write_text(fragment, encoding='utf-8', newline='\n')
    meta = {'format': FORMAT, 'check_id': check_id, 'prepared_at': now(),
            'status': 'prepared', 'fragment_sha256': digest(target)}
    save(folder / 'check.json', meta)
    return {'fragment': str(target), 'reused': False, **meta}

def record_paths(received, message_hash):
    """Use short names; identify messages only by their complete SHA-256."""
    suffix = 0
    while True:
        stem = message_hash[:12] + (f'-{suffix}' if suffix else '')
        message_copy = received / (stem + '.txt')
        receipt = received / (stem + '.json')
        if receipt.exists():
            if read(receipt).get('message_sha256') == message_hash:
                if message_copy.exists() and digest(message_copy) != message_hash:
                    raise ValueError('Saved compatibility message does not match its receipt')
                return message_copy, receipt
        elif not message_copy.exists() or digest(message_copy) == message_hash:
            return message_copy, receipt
        suffix += 1

def verify(folder, message):
    folder = folder.resolve()
    meta = prepared(folder)
    raw = message.read_bytes()
    lines = raw.decode('utf-8-sig').splitlines()
    starts = [i for i, line in enumerate(lines) if line.strip() == START]
    ends = [i for i, line in enumerate(lines) if line.strip() == END]
    if len(starts) != 1 or len(ends) != 1 or starts[0] >= ends[0]:
        raise ValueError('Save the exact returned compatibility message, including its markers')
    payload = json.loads('\n'.join(lines[starts[0] + 1:ends[0]]))
    if not isinstance(payload, dict) or payload.get('format') != FORMAT or payload.get('check_id') != meta['check_id']:
        raise ValueError('The message belongs to a different compatibility check')
    if payload.get('rendered') is not True or payload.get('follow_up_available') is not True:
        raise ValueError('The panel-to-chat capability was not confirmed')
    if type(payload.get('widget_state_available')) is not bool:
        raise ValueError('Missing widget-state diagnostic')
    sha = hashlib.sha256(raw).hexdigest()
    received = folder / 'received'
    received.mkdir(exist_ok=True)
    message_copy, receipt = record_paths(received, sha)
    if not message_copy.exists():
        with message_copy.open('xb') as stream:
            stream.write(raw)
    if digest(message_copy) != sha:
        raise ValueError('Saved compatibility message differs from the received bytes')
    if receipt.exists():
        result = read(receipt)
        if result.get('message_sha256') != sha or result.get('check_id') != meta['check_id']:
            raise ValueError('Conflicting compatibility receipt')
    else:
        result = {'status': 'passed', 'check_id': meta['check_id'], 'checked_at': now(),
                  'message_sha256': sha, 'capabilities': payload,
                  'scope': 'Panel display and follow-up return only; no research approvals or extraction validation.'}
        save(receipt, result)
    # Preserve the original saved receipt on repeated verification.
    if meta.get('status') != 'passed':
        save(folder / 'check.json', {**meta, 'status': 'passed', 'passed_at': result['checked_at'],
                                    'receipt': receipt.relative_to(folder).as_posix()})
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('prepare')
    p.add_argument('--output', required=True, type=Path)
    p = sub.add_parser('verify')
    p.add_argument('--check-dir', required=True, type=Path)
    p.add_argument('--message', required=True, type=Path)
    args = parser.parse_args()
    try:
        result = prepare(args.output) if args.command == 'prepare' else verify(args.check_dir, args.message)
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1, str(error) + '\n')
    print(json.dumps(result, ensure_ascii=False))

if __name__ == '__main__':
    main()
