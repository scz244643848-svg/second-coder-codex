"""Prepare explicitly designated PDF reading aids; Python 3.10+, PyMuPDF."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest() if hasattr(hashlib, 'file_digest') else hashlib.sha256(stream.read()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding='utf-8')


def page_selection(spec, count):
    pages = set()
    for item in spec.split(','):
        ends = item.strip().split('-')
        if len(ends) not in (1, 2):
            raise ValueError('Invalid page range')
        first, last = int(ends[0]), int(ends[-1])
        if not 1 <= first <= last <= count:
            raise ValueError(f'Page range outside 1..{count}: {item}')
        pages.update(range(first, last + 1))
    return pages


def prepare(source, output, fitz, extra=None):
    source = Path(source).resolve(strict=True)
    sha = digest(source)
    dest = output / (source.stem[:60] + '-' + sha[:16])
    dest.mkdir(parents=True, exist_ok=True)
    report_path = dest / 'quality_report.json'
    with fitz.open(source) as doc:
        if doc.needs_pass:
            raise ValueError('Encrypted PDF requires an accessible decrypted source')
        if extra is not None:
            pages = page_selection(extra, len(doc))
            for number in pages:
                doc[number - 1].get_pixmap(matrix=fitz.Matrix(2, 2)).save(dest / f'page-{number:04d}.png')
            write_json(dest / 'supplemental_render.json', {'source': str(source), 'sha256': sha, 'pages': sorted(pages)})
            return {'source': str(source), 'sha256': sha, 'directory': str(dest.resolve()), 'rendered_pages': sorted(pages)}
        if report_path.exists():
            cached = json.loads(report_path.read_text(encoding='utf-8'))
            required = [dest / 'fulltext.txt', dest / 'table_pages.txt'] + [dest / f'page-{n:04d}.png' for n in cached.get('rendered_pages', [])]
            if cached.get('sha256') == sha and cached.get('helper_version') == 1 and all(p.exists() for p in required):
                return {**cached, 'source': str(source), 'cache_reused': True}
        texts, table_pages, suspicious = [], set(), []
        for index, page in enumerate(doc):
            text = page.get_text('text')
            texts.append(f'\n=== PDF PAGE {index + 1} ===\n{text}')
            if re.search(r'\btable\s+(?:\d+|[A-Z]\d*|[IVX]+)\b', text, re.I):
                table_pages.add(index + 1)
                if index + 2 <= len(doc):
                    table_pages.add(index + 2)
            reasons = []
            if len(text.strip()) < 40:
                reasons.append('little_or_no_extracted_text')
            if '\ufffd' in text or '\x00' in text:
                reasons.append('replacement_or_null_characters')
            if reasons:
                suspicious.append({'pdf_page': index + 1, 'flags': reasons})
        render_pages = table_pages | {p['pdf_page'] for p in suspicious}
        (dest / 'fulltext.txt').write_text(''.join(texts), encoding='utf-8')
        (dest / 'table_pages.txt').write_text(''.join(texts[n-1] for n in sorted(table_pages)), encoding='utf-8')
        for n in sorted(render_pages):
            doc[n-1].get_pixmap(matrix=fitz.Matrix(2, 2)).save(dest / f'page-{n:04d}.png')
        report = {'helper_version': 1, 'source': str(source), 'sha256': sha, 'directory': str(dest.resolve()), 'pdf_pages': len(doc), 'table_keyword_pages_with_successors': sorted(table_pages), 'suspicious_pages': suspicious, 'rendered_pages': sorted(render_pages), 'status': 'prepared_unchecked', 'warning': 'Keyword detection and text heuristics do not prove coverage or readability.'}
        write_json(report_path, report)
        return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--source', type=Path)
    parser.add_argument('--render-pages')
    args = parser.parse_args()
    if bool(args.manifest) == bool(args.source) or bool(args.source) != bool(args.render_pages):
        parser.error('Use --manifest, or --source with --render-pages')
    try:
        import pymupdf as fitz
    except ImportError:
        print('PyMuPDF is unavailable. Locate a suitable runtime or install PyMuPDF in a project-local environment.', file=sys.stderr)
        return 2
    args.output.mkdir(parents=True, exist_ok=True)
    if args.source:
        print(json.dumps(prepare(args.source, args.output, fitz, args.render_pages), ensure_ascii=False))
        return 0
    papers = json.loads(args.manifest.read_text(encoding='utf-8-sig'))['papers']
    ids = [p['paper_id'] for p in papers]
    if len(ids) != len(set(ids)) or any(not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}', i) for i in ids):
        raise ValueError('paper_id must be unique and use safe letters/digits/hyphens/underscores')
    result, failed = [], False
    for paper in papers:
        entries = []
        for value in [paper['pdf'], *paper.get('supplements', [])]:
            source = Path(value)
            if not source.is_absolute():
                source = args.manifest.resolve().parent / source
            try:
                entries.append(prepare(source, args.output / paper['paper_id'], fitz))
            except Exception as error:
                failed = True
                entries.append({'source': str(source), 'status': 'failed', 'error': str(error)})
        result.append({'paper_id': paper['paper_id'], 'sources': entries})
    write_json(args.output / 'batch_preparation_report.json', {'papers': result, 'status': 'needs_attention' if failed else 'prepared_unchecked'})
    print(json.dumps({'papers': len(papers), 'failed_sources': sum(s['status'] == 'failed' for p in result for s in p['sources']), 'report': str((args.output / 'batch_preparation_report.json').resolve())}))
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
