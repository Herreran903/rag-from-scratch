"""Compare source-article units with LangChain recursive text splitting.

This local exercise uses no models, embeddings, vector store, or remote tracing.
Character offsets refer to normalized corpus text, not the PDF byte stream.
"""

import argparse
from copy import deepcopy
import hashlib
from importlib.metadata import version
import json
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


ROOT = Path(__file__).resolve().parent.parent
STRATEGIES = {
    "article": None,
    "recursive_180_40": {"chunk_size": 180, "chunk_overlap": 40},
    "recursive_100_20": {"chunk_size": 100, "chunk_overlap": 20},
}


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def load_documents(corpus):
    manifest = json.loads((corpus / "manifest.json").read_text(encoding="utf-8"))
    data = (corpus / manifest["records_file"]).read_bytes()
    if sha256(data) != manifest["records_sha256"]:
        raise ValueError("Corpus file does not match its recorded fingerprint")
    records = [json.loads(line) for line in data.decode("utf-8").splitlines()]
    if len(records) != manifest["record_count"]:
        raise ValueError("Unexpected number of article records")
    documents = []
    for row in records:
        if sha256(row["text"].encode("utf-8")) != row["text_sha256"]:
            raise ValueError(f"Text fingerprint mismatch: {row['record_id']}")
        if row["source_sha256"] != manifest["source_sha256"]:
            raise ValueError(f"Source fingerprint mismatch: {row['record_id']}")
        metadata = {key: deepcopy(row[key]) for key in (
            "corpus_id", "document_id", "logical_document_id", "season",
            "section", "issue", "document_date", "article_id",
            "article_heading", "parent_heading", "pdf_page", "printed_page",
            "source_url", "source_sha256",
        )}
        metadata["parent_record_id"] = row["record_id"]
        metadata["parent_text_sha256"] = row["text_sha256"]
        metadata["parent_unresolved_cross_references"] = deepcopy(row["unresolved_cross_references"])
        documents.append(Document(page_content=row["text"], metadata=metadata))
    ids = [doc.metadata["parent_record_id"] for doc in documents]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate parent record identifiers")
    return documents, manifest


def make_chunks(documents, strategy, config):
    splitter = None if config is None else RecursiveCharacterTextSplitter(
        **config,
        length_function=len,
        add_start_index=True,
        separators=["\n\n", "\n", ". ", " ", ""],
        keep_separator=True,
    )
    chunks = []
    for parent in documents:
        children = [Document(page_content=parent.page_content,
                             metadata={**deepcopy(parent.metadata), "start_index": 0})]
        if splitter is not None:
            children = splitter.split_documents([parent])
        covered = [False] * len(parent.page_content)
        for number, child in enumerate(children, start=1):
            start = child.metadata["start_index"]
            end = start + len(child.page_content)
            if not child.page_content or start < 0 or parent.page_content[start:end] != child.page_content:
                raise ValueError("A chunk cannot be located exactly in its source article")
            if config and len(child.page_content) > config["chunk_size"]:
                raise ValueError("A recursive chunk exceeds its configured character limit")
            if any(child.metadata[key] != value for key, value in parent.metadata.items()):
                raise ValueError("Source metadata changed during splitting")
            covered[start:end] = [True] * (end - start)
            chunks.append({
                "chunk_id": f"{parent.metadata['parent_record_id']}:{strategy}:{number:03d}",
                "strategy": strategy,
                "text": child.page_content,
                "metadata": {**child.metadata, "end_index_exclusive": end},
            })
        if any(not flag and not char.isspace() for flag, char in zip(covered, parent.page_content)):
            raise ValueError("Splitting dropped non-whitespace source characters")
    return chunks


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8", newline="\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus-dir", type=Path, default=ROOT / "outputs" / "corpus")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "outputs" / "langchain-chunking")
    args = parser.parse_args()
    documents, manifest = load_documents(args.corpus_dir)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary = {
        "corpus_id": manifest["corpus_id"],
        "source_sha256": manifest["source_sha256"],
        "records_sha256": manifest["records_sha256"],
        "packages": {name: version(name) for name in ("langchain-core", "langchain-text-splitters")},
        "input_documents": len(documents),
        "length_unit": "Python Unicode characters measured by len; not tokens or bytes",
        "offset_basis": "Normalized parent article text; end offsets are exclusive",
        "separators": ["\n\n", "\n", ". ", " ", ""],
        "strategies": {},
        "checks": ["corpus and text fingerprints", "metadata preservation",
                   "exact source offsets", "non-whitespace source coverage", "recursive size bounds"],
        "scope": "Mechanical chunk inspection only; no retrieval or answer-quality evaluation",
    }
    for name, config in STRATEGIES.items():
        chunks = make_chunks(documents, name, config)
        content = "".join(json.dumps(chunk, ensure_ascii=False) + "\n" for chunk in chunks)
        filename = f"{name}.jsonl"
        (args.output_dir / filename).write_text(content, encoding="utf-8", newline="\n")
        counts = {doc.metadata["article_id"]: 0 for doc in documents}
        for chunk in chunks:
            counts[chunk["metadata"]["article_id"]] += 1
        summary["strategies"][name] = {
            "config": config,
            "chunks_file": filename,
            "chunks_sha256": sha256(content.encode("utf-8")),
            "chunk_count": len(chunks),
            "max_chunk_characters": max(len(chunk["text"]) for chunk in chunks),
            "chunks_per_article": counts,
        }
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
