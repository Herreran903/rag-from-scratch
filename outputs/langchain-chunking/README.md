# First LangChain Exercise: Documents and Chunking

## Purpose

Introduce two components of the LangChain ecosystem using the existing five-article corpus:

- `langchain_core.documents.Document`: pairs source text with a metadata dictionary.
- `langchain_text_splitters.RecursiveCharacterTextSplitter`: divides text using ordered separators and a size limit.

This exercise prepares and inspects passages. It does not train a model, generate embeddings, search documents, or evaluate answer quality.

## Run locally

The learner authorised installing `langchain-core`, `langchain-text-splitters`, and their dependencies in this project's ignored `.venv` on 2026-10-18. This updates the initial restriction against installing packages for this specific exercise. No system-wide installation is required.

```bash
# Windows, using Python 3.12:
py -3.12 -m venv .venv
./.venv/Scripts/python.exe -m pip install -r requirements-langchain.lock.txt
./.venv/Scripts/python.exe examples/01_langchain_chunking.py

# Linux or macOS, after creating an environment with the same dependencies:
./.venv/bin/python examples/01_langchain_chunking.py
```

[Direct dependencies](../../requirements-langchain.txt) are pinned separately from the [tested environment](../../requirements-langchain.lock.txt), which also records transitive dependencies. The latter was resolved on Windows with Python 3.12; other platforms may require a compatible resolution. Corpus preparation has its own `requirements.txt`; `pypdf` is not needed to run this exercise against the existing JSONL.

The script reads `outputs/corpus/articles.jsonl`, checks its recorded fingerprints, creates `Document` objects, and writes the comparison artifacts alongside this guide. It can run without the locally stored source PDF.

## Comparison

| Strategy | Maximum size | Target overlap | Purpose |
|---|---|---|---|
| `article` | One complete source article | None | Preserve the original article boundary as a baseline. |
| `recursive_180_40` | 180 characters | 40 characters | Inspect moderate splitting of these short articles. |
| `recursive_100_20` | 100 characters | 20 characters | Deliberately expose the effects of small fragments. |

Sizes are measured using Python's `len`, not a model tokenizer. Overlap is a target, not a guarantee of exactly that many shared characters. The separator order is paragraphs, newlines, sentence boundaries, spaces, and finally individual characters. Our corpus has already collapsed whitespace, so its original paragraph breaks are not available to the splitter.

These are small illustrative settings, not tuned production recommendations. Splitting stays inside each parent article; the splitter does not discover links between articles or resolve regulatory exceptions.

## Observed run: 2026-10-18

Versions: `langchain-core==1.6.12`, `langchain-text-splitters==1.1.3`.

| Strategy | Total chunks | Largest chunk in characters | Chunks for C5.1.18 |
|---|---:|---:|---:|
| Article | 5 | 511 | 1 |
| Recursive 180 / 40 | 8 | 180 | 1 |
| Recursive 100 / 20 | 15 | 99 | 2 |

In the 100 / 20 run, C5.1.18 is split into intervals `[0, 93)` and `[74, 113)`. The first contains the exception qualifier but stops before the ambient-temperature phrase. The second contains the latter phrase without the exception qualifier. This demonstrates a context-separation risk if only one fragment is retrieved; it is not an observed model-answer failure because no model was run.

The actual shared span in this example is 19 characters, illustrating that the configured overlap is a target. Source metadata and complete character coverage pass their checks even though an individual chunk can lack interpretive context.

For this tiny corpus, whole articles are a sensible first retrieval baseline: the largest is only 511 characters, and C5.1.18 remains intact. This does not establish a general optimum or resolve cross-article dependencies. The 180 / 40 setting also retains C5.1.18 here, but splits the longer valve article into four pieces.

## Outputs and checks

- `article.jsonl`, `recursive_180_40.jsonl`, and `recursive_100_20.jsonl`: chunk text, strategy, unique identifier, and inherited source metadata.
- `summary.json`: installed package versions, source fingerprints, settings, and mechanical counts.

Every chunk has an exact character interval in its normalized parent text: `start_index` is inclusive and `end_index_exclusive` is exclusive. These offsets do not identify byte positions or coordinates in the PDF.

The script verifies source fingerprints, inherited metadata, exact text offsets, recursive size bounds, and coverage of all non-whitespace parent characters. Passing these checks establishes mechanical consistency, not semantic completeness. A second run with socket connections disabled reproduced all four generated artifacts byte-for-byte; `pip check` also passed.

`parent_unresolved_cross_references` describes dependencies of the complete source article. It does not claim that every child chunk contains each reference. Retaining this metadata also does not make the missing target articles available.

## Where the other tools fit

| Tool | Role | Place in this project |
|---|---|---|
| LangChain components and integrations | Common interfaces for documents, models, retrieval, and tools. | Documents and splitting first; retrieval and model adapters later. |
| LangGraph | Stateful orchestration of deterministic and agent-driven steps. | Consider when the project needs explicit branching, persistence, or repeated searches. |
| LangSmith | Tracing and evaluation tooling. | Optional later observability; no hosted tracing is configured here. |
| Vector storage | Store embeddings and retrieve similar records with filters. | Select after learning embeddings and defining a retrieval comparison. |

LangSmith's SDK may be installed as a transitive dependency of LangChain Core. Installing the SDK does not mean this exercise configures a hosted tracing service or sends documents to it. The example constructs documents and splits text locally; it contains no model or tracing calls.

## Official references

- [LangChain overview](https://docs.langchain.com/oss/python/langchain/overview).
- [Recursive text splitter](https://docs.langchain.com/oss/python/integrations/splitters/recursive_text_splitter).
- [LangGraph overview and ecosystem roles](https://docs.langchain.com/oss/python/langgraph/overview).

The next step is to inspect the resulting fragments and choose a baseline for simple retrieval. No learner quiz is required to continue.
