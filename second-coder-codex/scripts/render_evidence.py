"""Render original PDF evidence for researcher-visible adjudication; requires PyMuPDF."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def render(source, page_number, output, dpi=180, clip=None):
    import pymupdf
    source = Path(source).resolve(strict=True)
    output = Path(output).resolve()
    if not 72 <= dpi <= 600:
        raise ValueError('dpi must be between 72 and 600')
    with pymupdf.open(source) as doc:
        if doc.needs_pass:
            raise ValueError('PDF requires a password; provide an accessible source')
        if not 1 <= page_number <= len(doc):
            raise ValueError(f'Physical PDF page must be in 1..{len(doc)}')
        page = doc[page_number - 1]
        box = None
        if clip is not None:
            if len(clip) != 4 or not all(math.isfinite(x) for x in clip):
                raise ValueError('clip must have four finite coordinates')
            box = pymupdf.Rect(clip)
            if box.is_empty or not page.rect.contains(box):
                raise ValueError('clip must be a nonempty rectangle within the page')
        # Never silently replace evidence associated with an earlier decision.
        if output.exists():
            raise ValueError('Use a new evidence folder; destination already exists')
        output.mkdir(parents=True)
        full = output / f'pdf-page-{page_number:04d}.png'
        page.get_pixmap(dpi=dpi, alpha=False).save(full)
        images = [{'file': full.name, 'kind': 'full_page', 'sha256': sha256(full)}]
        if box is not None:
            detail = output / f'pdf-page-{page_number:04d}-detail.png'
            page.get_pixmap(dpi=dpi, alpha=False, clip=box).save(detail)
            images.append({'file': detail.name, 'kind': 'detail', 'sha256': sha256(detail)})
        metadata = {'source': str(source), 'source_sha256': sha256(source),
                    'physical_pdf_page': page_number, 'pdf_page_label': page.get_label(),
                    'dpi': dpi, 'page_rectangle': list(page.rect), 'clip': list(box) if box is not None else None,
                    'images': images, 'status': 'rendered_requires_visual_check_and_presentation'}
        (output / 'evidence.json').write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding='utf-8')
    return metadata


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', required=True, type=Path)
    p.add_argument('--page', required=True, type=int)
    p.add_argument('--output', required=True, type=Path)
    p.add_argument('--dpi', type=int, default=180)
    p.add_argument('--clip', type=float, nargs=4)
    args = p.parse_args()
    try:
        metadata = render(args.source, args.page, args.output, args.dpi, args.clip)
    except (ImportError, OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 1
    print(json.dumps(metadata, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
