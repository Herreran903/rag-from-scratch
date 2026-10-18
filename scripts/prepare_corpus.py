"""Download, verify, or prepare the agreed five-article source corpus.

Run with Python and the recorded pypdf dependency. This preparation utility does not
install packages, call a model, build a search index, or implement a RAG system.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import logging
from pathlib import Path
import re
import sys
from urllib.request import Request, urlopen

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "outputs" / "corpus"
PDF = CORPUS / "sources" / "fia-f1-2026-section-c-issue-20.pdf"
EXPECTED_SOURCE_SHA256 = "cf0b919eef5eecc27497fb6de012f8d27e200f6dbd34d62b7e5385f7274ff652"
DOCUMENT_ID = "fia-f1-2026-section-c-issue-20"
CORPUS_ID = "fia-f1-2026-engine-subset-v1"
SOURCE_URL = (
    "https://www.fia.com/system/files/documents/"
    "fia_2026_f1_regulations_-_section_c_technical_-_iss_20_-_2026-08-05.pdf"
)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def normalize(text):
    # Normalize only typographical ligatures and whitespace. Preserve numerical
    # signs, degree symbols, case, wording, punctuation, and cross-references.
    ligatures = str.maketrans({"\ufb00": "ff", "\ufb01": "fi", "\ufb02": "fl",
                              "\ufb03": "ffi", "\ufb04": "ffl"})
    return " ".join(text.translate(ligatures).split())


def main():
    global CORPUS, PDF
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--download", action="store_true", help="Download the pinned official PDF if missing, then prepare records")
    modes.add_argument("--check", action="store_true", help="Verify existing records and any available local PDF without modifying files")
    parser.add_argument("--output-dir", type=Path, help="Optional corpus directory, mainly for isolated reproduction checks")
    args = parser.parse_args()
    if args.output_dir is not None:
        CORPUS = args.output_dir.resolve()
        PDF = CORPUS / "sources" / PDF.name
    if args.check:
        manifest = json.loads((CORPUS / "manifest.json").read_text(encoding="utf-8"))
        records = (CORPUS / manifest["records_file"]).read_bytes()
        rows = [json.loads(line) for line in records.decode("utf-8").splitlines()]
        if digest(records) != manifest["records_sha256"]:
            raise ValueError("Records checksum differs from the manifest")
        if len(rows) != manifest["record_count"] or len({r["record_id"] for r in rows}) != len(rows):
            raise ValueError("Record count or identifiers are inconsistent")
        if [r["article_id"] for r in rows] != manifest["selected_articles"]:
            raise ValueError("Article scope differs from the manifest")
        for row in rows:
            if digest(row["text"].encode("utf-8")) != row["text_sha256"]:
                raise ValueError(f"Text checksum mismatch: {row['record_id']}")
            if row["source_sha256"] != manifest["source_sha256"]:
                raise ValueError(f"Source identity mismatch: {row['record_id']}")
        if PDF.exists() and digest(PDF.read_bytes()) != manifest["source_sha256"]:
            raise ValueError("Local PDF checksum differs from the manifest")
        print(json.dumps({"checks": "passed", "record_count": len(rows), "local_pdf_present": PDF.exists()}, indent=2))
        return

    download = None
    if args.download and not PDF.exists():
        request = Request(SOURCE_URL, headers={"User-Agent": "FIA-RAG-Learning-Project/1.0"})
        with urlopen(request, timeout=60) as response:
            data = response.read()
            download = {
                "source_url": SOURCE_URL,
                "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
                "status_code": response.status,
                "content_type": response.headers.get("Content-Type", ""),
                "etag": response.headers.get("ETag", ""),
                "last_modified": response.headers.get("Last-Modified", ""),
            }
        if digest(data) != EXPECTED_SOURCE_SHA256:
            raise ValueError("Official download differs from the pinned snapshot; review the edition before proceeding")
        PDF.parent.mkdir(parents=True, exist_ok=True)
        PDF.write_bytes(data)
    if not PDF.exists():
        parser.error("Local PDF missing. Use --download or follow outputs/corpus/sources/README.md")
    source_bytes = PDF.read_bytes()
    assert source_bytes.startswith(b"%PDF-"), "Downloaded source is not a PDF"
    source_hash = digest(source_bytes)
    if source_hash != EXPECTED_SOURCE_SHA256:
        raise ValueError("Local PDF differs from the pinned source snapshot")
    # The file has recoverable cross-reference-offset warnings. Preserve this
    # fact in the manifest and compare the selected text with page renderings.
    logging.getLogger("pypdf").setLevel(logging.ERROR)
    reader = PdfReader(PDF)
    cover = normalize(reader.pages[0].extract_text())
    assert len(reader.pages) == 254
    assert "Version: Issue 20" in cover and "Date: 05/08/2026" in cover
    assert "WMSC approval date: 03/08/2026" in cover

    pages = {number: reader.pages[number - 1].extract_text()
             for number in (61, 62)}
    specs = [
        ("C5.1.1", 61, r"\bC5\.1\.2\b"),
        ("C5.1.2", 61, r"\bC5\.1\.3\b"),
        ("C5.1.3", 61, r"\bC5\.1\.4\b"),
        ("C5.1.4", 61, r"\bC5\.1\.5\b"),
        ("C5.1.18", 62, r"\bC5\.2\s+Power Unit Energy"),
    ]
    rows = []
    for article, page, end_pattern in specs:
        page_text = pages[page]
        start_match = re.search(r"\b" + re.escape(article) + r"\b", page_text)
        assert start_match, f"Missing start: {article}"
        end_match = re.search(end_pattern, page_text[start_match.end():])
        assert end_match, f"Missing end: {article}"
        start = start_match.end()
        end = start + end_match.start()
        raw = page_text[start:end].strip()
        text = normalize(raw)
        heading = None
        if article == "C5.1.18":
            heading = "Treatment of Numerical Values"
            assert text.startswith(heading)
            text = text[len(heading):].strip()
        references = []
        if article == "C5.1.4":
            references = ["C5.7.8 g)", "C5.6.2", "C5.1.7 a)"]
            assert all(reference in text for reference in references)
        text_hash = digest(text.encode("utf-8"))
        rows.append({
            "record_id": f"{DOCUMENT_ID}:{article}",
            "corpus_id": CORPUS_ID,
            "document_id": DOCUMENT_ID,
            "logical_document_id": "fia-f1-2026-section-c",
            "season": 2026,
            "section": "C",
            "issue": 20,
            "document_date": "2026-08-05",
            "article_id": article,
            "article_heading": heading,
            "parent_heading": "Engine specification",
            "pdf_page": page,
            "printed_page": f"C{page}",
            "source_url": SOURCE_URL,
            "source_file": "sources/fia-f1-2026-section-c-issue-20.pdf",
            "source_sha256": source_hash,
            "text_raw": raw,
            "text": text,
            "text_sha256": text_hash,
            "unresolved_cross_references": references,
            "extraction_review": "assistant_visual_check_completed",
        })

    selected = [row["article_id"] for row in rows]
    assert selected == ["C5.1.1", "C5.1.2", "C5.1.3", "C5.1.4", "C5.1.18"]
    assert len({row["record_id"] for row in rows}) == 5
    previous_manifest_path = CORPUS / "manifest.json"
    if download is None and previous_manifest_path.exists():
        previous_manifest = json.loads(previous_manifest_path.read_text(encoding="utf-8"))
        if previous_manifest.get("source_sha256") == source_hash:
            download = previous_manifest.get("download")
    if download is None:
        download = {"source_url": SOURCE_URL, "retrieved_at_utc": None,
                    "note": "Source supplied locally; download time was not recorded"}
    manifest = {
        "schema_version": 1,
        "corpus_id": CORPUS_ID,
        "purpose": "Minimal source corpus for a gradual RAG learning project",
        "document_id": DOCUMENT_ID,
        "logical_document_id": "fia-f1-2026-section-c",
        "source_url": SOURCE_URL,
        "catalogue_url": "https://www.fia.com/regulations/category/110",
        "source_file": "sources/fia-f1-2026-section-c-issue-20.pdf",
        "source_sha256": source_hash,
        "source_size_bytes": len(source_bytes),
        "source_page_count": len(reader.pages),
        "document_date": "2026-08-05",
        "wmsc_approval_date": "2026-08-03",
        "catalogue_publication_date_previously_observed": "2026-10-01",
        "catalogue_observation_date": "2026-10-17",
        "download": download,
        "records_file": "articles.jsonl",
        "record_count": len(rows),
        "selected_articles": selected,
        "extraction": {
            "engine": "pypdf",
            "version": importlib.metadata.version("pypdf"),
            "python_version": sys.version.split()[0],
            "normalization": "Expand ff/fi/fl/ffi/ffl ligatures and collapse whitespace; preserve other characters",
            "article_heading_handling": "C5.1.18 heading is separated from body; text_raw retains it",
            "page_numbering": "pdf_page is one-based; printed_page is the visible footer label",
            "utility": "../../scripts/prepare_corpus.py",
            "boundary_method": "Explicit article starts and next-article endpoints, not every inline cross-reference",
            "pdf_warnings": "pypdf reported recoverable object-offset warnings; the PDF was not modified",
        },
        "quality": {
            "assistant_visual_check": "The original pinned snapshot was compared with Poppler renders on 2026-10-17; a rerun does not perform a new visual review",
            "reviewed_at_local_date": "2026-10-17",
            "human_source_validation": "not_recorded",
            "evaluation_gold_set": "not_accepted",
            "unresolved_cross_references": ["C5.7.8 g)", "C5.6.2", "C5.1.7 a)"],
            "text_only_limit": "Layout, colour semantics, and figures are not encoded in article text; retain the original PDF",
            "scope": "The five selected articles only; other downloaded PDF content is outside the corpus",
        },
        "status": {
            "source_snapshot_saved": True,
            "article_records_prepared": True,
            "retrieval_chunking_configured": False,
            "embeddings_generated": False,
            "search_index_built": False,
        },
    }
    records_text = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)
    (CORPUS / "articles.jsonl").write_text(records_text, encoding="utf-8", newline="\n")
    manifest["records_sha256"] = digest((CORPUS / "articles.jsonl").read_bytes())
    (CORPUS / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    # Check the deliverables rather than creating a separate test framework.
    saved_rows = [json.loads(line) for line in (CORPUS / "articles.jsonl").read_text(encoding="utf-8").splitlines()]
    assert len(saved_rows) == 5
    assert all(digest(row["text"].encode("utf-8")) == row["text_sha256"] for row in saved_rows)
    assert all(row["source_sha256"] == digest(PDF.read_bytes()) for row in saved_rows)
    print(json.dumps({"record_count": len(saved_rows), "article_ids": selected,
                      "source_sha256": source_hash, "records_sha256": manifest["records_sha256"]}, indent=2))


if __name__ == "__main__":
    main()
