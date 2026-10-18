# RAG from Scratch: FIA F1 Technical Regulations

A gradual, practical learning project for Retrieval-Augmented Generation (RAG), using the **2026 FIA Formula 1 Technical Regulations**. The initial topic is engine specifications; power-unit requirements and aerodynamics are possible extensions.

**Working question:** How can a RAG assistant retrieve the relevant requirements, definitions, conditions, and exceptions from the correct regulation edition and answer with verifiable sources?

## Current status

This project currently contains a small versioned corpus, preparation code, a local LangChain document-and-chunking exercise, an Ollama generation smoke test with explicitly supplied evidence, evaluation candidates, and a documented learning process. Automatic retrieval, embeddings, and vector storage are not implemented. No model-training results or general answer-quality benchmark are claimed.

The corpus contains five articles from Section C, Issue 20, dated 5 August 2026: C5.1.1-C5.1.4 and C5.1.18. Each record preserves source provenance, page locators, text fingerprints, and unresolved cross-references.

## Start here

| Material | Purpose |
|---|---|
| [Corpus guide](outputs/corpus/README.md) | Files, record fields, preparation checks, and limitations. |
| [Source manifest](outputs/corpus/manifest.json) | Edition, source URL, dates, extraction method, and checksums. |
| [Article records](outputs/corpus/articles.jsonl) | Five source units, one JSON record per line. |
| [Reference candidates](outputs/reference-candidates.md) | Draft answers, source anchors, and review criteria; not an accepted gold set. |
| [Process log](outputs/process-log.md) | Decisions, revisions, and the LLM-assisted evaluation-data method. |
| [Preparation utility](scripts/prepare_corpus.py) | Download, verify, and reproduce the small source corpus. |
| [First LangChain exercise](outputs/langchain-chunking/README.md) | Document metadata, three chunking strategies, and an observed context-separation risk. |
| [Chunking example](examples/01_langchain_chunking.py) | Runnable local exercise using LangChain Core and text splitters. |
| [Local Ollama test](outputs/ollama-smoke-test/README.md) | Two generation cases using an existing local model and supplied evidence. |

## Reproduce corpus preparation

The recorded preparation environment used Python 3.12 and `pypdf==6.10.0`, listed in [requirements.txt](requirements.txt). Make that dependency available in your chosen environment before running the utility. The utility does not install packages.

```bash
# Verify the checked-in JSONL and manifest without downloading the PDF.
python scripts/prepare_corpus.py --check

# Download the official PDF if missing, verify its checksum, and rebuild records.
python scripts/prepare_corpus.py --download

# Rebuild from a source PDF that is already stored locally.
python scripts/prepare_corpus.py
```

The original PDF and temporary files are excluded from Git. A changed source download is rejected if it does not match the pinned fingerprint. Extraction does not replace visual or domain review; regenerated outputs do not claim a new human review.

## Gradual learning path

1. **Documents:** preserve source text, structure, metadata, and versions.
2. **Chunking:** compare article boundaries and smaller passages while retaining context.
3. **Search:** establish a simple keyword baseline and inspect failures.
4. **Embeddings:** understand vector representations and similarity.
5. **Retrieval:** compare evidence selection, filters, and vector storage.
6. **Generation with sources:** answer from retrieved evidence and handle missing information.
7. **Evaluation:** measure retrieval, answer correctness, source support, and update behavior.

LangChain Core and text splitters are used for the first chunking exercise; its prompt abstraction is reused in the [local Ollama test](outputs/ollama-smoke-test/README.md). Ollama is a working local generation option. Vector storage, other model providers, and AWS remain later choices; LangGraph and hosted tracing are not configured. The next step is a simple retrieval baseline, starting with whole articles for this small corpus, before connecting automatic evidence selection to generation.

## Working conventions

- Use English for files, code names, and commands; discuss learning steps in Spanish.
- Explain each step before implementation and progress through small practical artifacts.
- Keep scratch files in the ignored `work/` directory and inspectable learning artifacts in `outputs/`.
- Track evaluation-data curation separately from implementation. LLM-generated candidates require verification; they are not automatically ground truth.

This is an independent educational project. FIA and Formula 1 source materials retain their respective rights; this project is not affiliated with or endorsed by either organisation. See the [source note](outputs/corpus/sources/README.md).
