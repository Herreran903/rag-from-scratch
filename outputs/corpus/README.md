# Minimal FIA 2026 Engine Corpus

Prepared on 2026-10-17. This is the first local data-preparation artifact for the RAG learning project. It contains source records, not generated reference answers or a search index.

## Files

| File | Purpose |
|---|---|
| [Original PDF](sources/fia-f1-2026-section-c-issue-20.pdf) | Unmodified snapshot downloaded from the official FIA source. |
| [manifest.json](manifest.json) | Source URL, retrieval time, edition dates, checksums, extraction method, and corpus boundaries. |
| [articles.jsonl](articles.jsonl) | Five article records; each line is an independent JSON object. |

The original PDF contains the complete document. The current text corpus consists only of C5.1.1, C5.1.2, C5.1.3, C5.1.4, and C5.1.18. Other PDF content is not automatically included in future retrieval.

## What a record contains

| Field | Meaning |
|---|---|
| `document_id` | Identity of this particular edition. |
| `logical_document_id` | Document family shared by later or earlier editions. |
| `article_id` | Original article locator. |
| `issue`, `document_date` | Source edition information. |
| `pdf_page`, `printed_page` | One-based viewer page and visible footer label. |
| `text_raw` | Extracted article text before normalization, including any article heading. |
| `text` | Body text after limited normalization; not a summary. |
| `source_sha256` | Fingerprint of the downloaded PDF bytes. |
| `text_sha256` | Fingerprint of the normalized text bytes. |
| `unresolved_cross_references` | References whose target articles are outside this subset. |

Example metadata: `article_id = C5.1.2`, `issue = 20`, `pdf_page = 61`, `printed_page = C61`. The metadata lets a retrieved passage lead back to the source edition and location.

A checksum detects byte differences; it does not establish factual correctness, authenticity on its own, or the significance of a change. Reformatting a PDF can change its checksum without changing a requirement.

## Preparation and checks

1. Downloaded the source PDF and recorded the URL, UTC retrieval time, and selected HTTP response headers.
2. Checked the cover identity, document dates, and page count using the existing bundled `pypdf` package.
3. Extracted the five agreed article bodies using explicit article boundaries. Inline cross-references were retained as content rather than treated as new boundaries.
4. Expanded typographical ligatures and collapsed whitespace. Numerical signs, symbols, wording, and cross-references were retained. The title of C5.1.18 is stored separately from its normalized body and remains in `text_raw`.
5. Rendered the relevant pages with the existing bundled Poppler tool and visually compared all selected article text with pages C61-C62.
6. Reopened the JSONL, checked five distinct record IDs, and verified source and text checksums.

The one-off preparation utility is saved in the project's `work/` directory as `prepare_corpus.py`. It is preparation code, not an implemented RAG pipeline. No dependencies were installed and no model was called.

## Limitations and next step

C5.1.4 contains three cross-references outside this subset. They are retained and marked unresolved; their target provisions have not been silently added or interpreted. The article body is preserved in full even though the initial valve-count evaluation question is narrower.

Raw extraction is not a perfect reconstruction of the PDF. The parser reported recoverable object-offset warnings; the selected text was checked against rendered pages. Text records do not preserve layout, colour semantics, or figures, so the original PDF remains necessary for source review.

These records follow the source's article boundaries. A retrieval chunking policy has not yet been selected. The next exercise will compare what happens when an article is treated as a retrieval unit and when its contextual dependencies need to accompany it. No embeddings, vector database, search index, or model-generated answers have been created.
