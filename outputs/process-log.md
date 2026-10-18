# Process Log: FIA Technical Regulations RAG

## 2026-10-17 — Scope and evaluation design

### Purpose and working method

Learn RAG gradually through small, inspectable exercises. Explain each step in Spanish before implementation; keep project files, code names, and commands in English. This project is independent of the Whisper project.

At this stage, the work consists of discussion, source inspection through web browsing, and documentation. No RAG system has been implemented, no local corpus has been ingested, no dependencies have been installed, no models have been downloaded, and no paid API calls have been initiated for the project.

### How the scope was selected

1. Prepared this chat directory as the project root and created the initial README.
2. Reviewed earlier portfolio planning. That planning proposed an evaluated support assistant on AWS, followed by optional agent extensions. It was background rather than a fixed architecture for this project.
3. Discussed research on evidence retrieval, conversational ambiguity, unanswerable questions, conflicting sources, temporal relevance, and evaluation.
4. Expanded the discussion to document fragmentation, revisions, incremental indexing, stale chunks, update visibility, and embedding-model migrations.
5. The learner proposed FIA documentation to connect the project with previous Formula 1 work during an exchange program, then clarified that the work concerned the 2026 technical regulations.
6. Considered engine and aerodynamics topics. The assistant proposed engine specifications as the first small exercise, and the learner agreed to proceed.
7. Identified the question-proposal step as LLM-assisted synthetic evaluation-data generation. The learner requested that this method and the process be documented.

### Selected scope

- **Domain:** FIA 2026 Formula 1 Technical Regulations.
- **Initial topic:** engine specifications within Article C5, Power Unit.
- **Initial reading subset:** C5.1.1-C5.1.4 and C5.1.18.
- **Possible later topics:** broader power-unit requirements, aerodynamics, and comparisons between regulation editions.
- **Working research question:** How can a RAG assistant retrieve the relevant technical requirements, definitions, conditions, and exceptions from the correct edition and answer with verifiable sources?

This is a learning project connected with current research problems. An original research contribution has not been established.

LangChain, a vector database, and AWS are learning options discussed for later stages. No library, database, embedding model, cloud service, or deployment architecture has been selected or configured.

### Source provenance

- [Official FIA regulation catalogue](https://www.fia.com/regulations/category/110).
- [Selected official PDF: 2026 Section C, Issue 20](https://www.fia.com/system/files/documents/fia_2026_f1_regulations_-_section_c_technical_-_iss_20_-_2026-08-05.pdf).
- The PDF cover identifies **Issue 20**, status **PUBLISHED**, document date **5 August 2026**, and WMSC approval date **3 August 2026**.
- The catalogue displayed a publication date of **1 October 2026**. Catalogue publication, PDF document date, and approval date must remain distinct.
- Initial source inspection date: **17 October 2026**.
- Initial passages appear on printed pages **C61-C62** (PDF viewer pages 61-62 in this edition).

The selected edition is the reference for this exercise, not a claim that it governs every historical event or future query. No local source snapshot or checksum has yet been recorded.

### Method: LLM-assisted evaluation-data generation

The assistant inspected the selected source through web tools and proposed questions in the conversation. The five questions were originally presented in Spanish; the English versions below are their documentation translations. This was an interactive proposal process, not an executed Ragas pipeline or a batch-generation script.

The intended workflow is:

**Official source -> LLM-generated candidates -> human verification against the source -> accepted reference set.**

Generated questions and answers are candidates, not automatically ground truth. At present, only question candidates have been proposed: reference answers, complete evidence annotations, and human acceptance are pending. No validated gold set exists yet.

For each accepted example, record:

- Question and language.
- Reference answer or required answer points, including units, tolerances, and conditions.
- Supporting passages anchored to the original document, articles, and pages.
- Document identity and edition.
- Expected behavior: answer, request clarification, or report insufficient evidence.
- The corpus scope under which answerability is assessed.
- Review status, corrections, and acceptance rationale.

Original-document evidence anchors should remain usable when chunking changes. Future chunk identifiers can be added without replacing these anchors.

The exact chat model identifier, sampling settings, and a standalone generation prompt were not recorded. These should be captured for future reproducible generation runs.

### Initial question candidates

All rows are **proposed; human verification pending**. The article column is a proposed evidence location, not a completed annotation.

| ID | Candidate question | Proposed evidence | Intended behavior |
|---|---|---|---|
| Q001 | What type of engine is permitted? | C5.1.1 | Answer from the selected edition. |
| Q002 | What engine cubic capacity and tolerance are specified? | C5.1.2 | Preserve the value, units, and tolerance. |
| Q003 | How many cylinders are required, and how must they be arranged? | C5.1.3 | Include the applicable configuration requirements. |
| Q004 | What valve requirements are specified? | C5.1.4 | Cover the requirements in this article; follow cross-references if needed. |
| Q005 | Under what conditions are numerical values in Article C5 interpreted? | C5.1.18 | Preserve the qualifier and default interpretation conditions. |
| Q006 | What is the engine speed limit? | Not established by the initial subset; inspect C5.14 and related provisions later. | Report insufficient evidence from this subset or seek additional passages if broader retrieval is allowed. |

Q006 is deliberately outside the initial reading subset. It must **not** be labelled unanswerable from the complete regulation merely because the subset is insufficient. Reassess its label when the corpus expands. References needed by other questions may likewise require expanding the subset or narrowing the question.

These examples are learning/development cases. They are not a held-out test set and do not establish broad system quality.

### Evaluation safeguards discussed

- Check generated labels directly against the official source rather than trusting model fluency.
- Distinguish generating evaluation examples from using an LLM as a judge of system outputs.
- A second automated judgement does not establish correctness by itself.
- Include varied questions as the set grows; source-generated questions can be too easy or too close to document wording.
- Keep some independently reviewed cases separate from iterative development when meaningful comparisons begin.
- Distinguish source disagreements from changes across editions, scope differences, and rule/exception relationships.
- Distinguish explaining a requirement from checking whether a physical design complies; the latter may require geometry, measurements, or calculations beyond the text.

### Technical topics deferred to later exercises

Preserve definitions, exceptions, headings, tables, and cross-references during fragmentation. Compare retrieval strategies using the same reviewed examples. Track document revisions and the processing configuration. When updating an index, account for removed chunks, changed chunk boundaries, embedding compatibility, query visibility, and caches. These are learning questions, not implemented capabilities.

### Method references

- [Ragas: Testset Generation](https://docs.ragas.io/en/latest/concepts/test_data_generation/) — synthetic evaluation-data generation tooling; not installed or executed here.
- [Can we Evaluate RAGs with Synthetic Data? (2025)](https://arxiv.org/abs/2508.11758) — examines whether synthetic evaluation preserves comparisons with human-labelled benchmarks; cautions against assuming equivalence across generator comparisons.
- [FreshStack (2025)](https://arxiv.org/abs/2504.13128) — realistic technical-document retrieval evaluation.
- [MTRAG-UN (2026)](https://arxiv.org/abs/2602.23184) — conversational, ambiguous, and unanswerable-query evaluation.
- [DRAGged into Conflicts (2025)](https://arxiv.org/abs/2506.08500) — different source-conflict types and expected response behaviors.

These references motivated the discussion; their results are not experimental results from this project.

### Next step and completion criterion

Read the selected passages together, draft answers to Q001-Q005, and verify their evidence. Confirm Q006's insufficient-evidence behavior under the explicitly limited subset. Correct or narrow ambiguous questions before accepting them.

The first exercise is complete when each candidate has a documented review outcome and each accepted example has a reference answer or behavior, source edition, and verifiable evidence. Search implementation follows this exercise.

## 2026-10-17 — Draft reference answers and source checks

After the learner asked to continue, the assistant reopened the official PDF and inspected its extracted text for the scoped articles. Created [reference-candidates.md](reference-candidates.md) with draft answers, evidence anchors, expected behaviors, and case-specific review criteria.

### Curation decisions

- Made Q001-Q003 and Q005 more explicit about their article or requested attributes. Case IDs remain unchanged.
- Narrowed Q004 from general valve requirements to per-cylinder intake and exhaust valve counts. The broader question includes additional construction requirements and cross-references and is deferred.
- Marked Q002's interval representation as an arithmetic derivation rather than a verbatim source statement.
- Preserved Q005's exception qualifier rather than treating the default as unconditional.
- Assessed Q006 only against the selected articles, retaining `insufficient_evidence_in_subset`. No answerability claim about the complete regulation was established.

### Status and next action

The candidate table earlier in this log records the initial proposals; the new reference-candidates document records their refined wording and draft answers. These stages are intentionally retained for traceability.

Assistant source checking has been performed; human review, acceptance, and any independent validation remain pending. The source check and answer drafting were performed by the same assistant. No validated gold set or system performance results are claimed.

Next, review the cases with the learner against the official source, record any corrections and explicit case decisions, and then begin discussing how to preserve these evidence units during fragmentation. No code, local ingestion, dependencies, model downloads, or paid API calls were added in this step.

## 2026-10-17 — Learner reasoning review of Q002

The assistant presented a hypothetical displacement above the specified upper bound and asked the learner to explain why it would not satisfy the scoped requirement. The learner correctly identified the absence of a positive tolerance and explained the positive excess. The assistant clarified that the unit is volume (cubic centimetres), rather than length (centimetres).

Recorded outcome: Q002's asymmetric-tolerance reasoning exercise was completed correctly. This is evidence of learner interpretation, not confirmation of independent PDF inspection, final case acceptance, or validation of the other candidates. Updated the case record accordingly. The remaining cases are still pending learner review; no complete gold set has been accepted.

## 2026-10-17 — Learner reasoning review of Q005

The assistant asked what error would result from losing the exception qualifier in C5.1.18 during fragmentation. The learner recognised that the default has exceptions, but attributed the possible differences to directions or changes by the FIA.

The assistant clarified the distinction between a default with an expressly specified exception and a power to amend or override requirements. The scoped qualifier does not, by itself, establish the latter. A claimed exception needs supporting evidence in an applicable provision.

Recorded outcome: exception recognition with a corrected explanation of its basis. This introduces a retrieval requirement: preserve qualifiers and retrieve the provision supporting a claimed exception rather than inventing one. No actual exception was identified, and no final gold-set acceptance was recorded.

## 2026-10-17 — Learning-method correction

After a further question-by-question exercise was proposed for Q006, the learner explained that this format was not useful: they already understand the need for trustworthy information and domain-approved datasets. Their intended learning objective is practical RAG construction and the associated engineering decisions.

The assistant acknowledged that the oral exercises had diverted the learning process. Continue through small concrete artifacts and direct explanations, rather than asking the learner to demonstrate basic evidence-handling principles. Record dataset-review outcomes only when actually obtained; do not infer case approval from this general discussion. Q006 has not received a learner case review.

The learner described a real-world need for a dataset aligned with the policies being evaluated and validated by the responsible department. In this project, reference questions, answers, and evidence serve evaluation; they are not automatically model-training data. A basic RAG can use an external document corpus and evaluation examples without fine-tuning. Domain approval remains a distinct dataset-governance activity; no external department has reviewed this project's candidates.

The next practical topic is preparation of a minimal versioned corpus with source and article metadata, followed by fragmentation and retrieval. The earlier statement that search implementation follows accepted reference cases describes the initial plan; it is superseded by this gradual practical approach, with candidate-set curation tracked separately. The current change updates documentation only and does not install dependencies, ingest a corpus, invoke paid APIs, or implement a RAG system.

## 2026-10-17 — First local source corpus

Following the learner's agreement to the proposed corpus-preparation step, saved an unmodified official PDF under `corpus/sources/` and prepared the [corpus guide](corpus/README.md), [manifest](corpus/manifest.json), and [article records](corpus/articles.jsonl). Earlier statements that no local snapshot existed describe the prior stage and are superseded by this entry.

### Source identity and extraction

- Source SHA-256: `cf0b919eef5eecc27497fb6de012f8d27e200f6dbd34d62b7e5385f7274ff652`.
- Download size: 5,825,714 bytes; 254 PDF pages.
- The cover identifies Section C, Issue 20, document date 2026-08-05, and approval date 2026-08-03. Actual retrieval time and selected HTTP response headers are in the manifest.
- Extracted C5.1.1-C5.1.4 and C5.1.18 into five distinct records, preserving full article bodies and source locators. These are source units, not a selected retrieval chunking policy.
- Preserved raw extracted text alongside text normalized only for typographical ligatures and whitespace. Numeric signs and original cross-references were retained.
- Stored three unresolved references from C5.1.4: C5.7.8 g), C5.6.2, and C5.1.7 a). Did not expand the corpus to include them.

### Tooling and verification

Used the PDF skill and the existing bundled Python/pypdf and Poppler rendering tools. The initial console extraction hit an encoding error; rerunning in UTF-8 resolved it. The parser also reported recoverable PDF object-offset warnings. Selected text was compared visually against Poppler-rendered pages C61-C62; the original file was not repaired or rewritten. No OCR was needed for these pages.

Saved the one-off preparation utility at `work/prepare_corpus.py` and extraction/rendering intermediates at `work/pdf-review/`. Verified five records, distinct identifiers, valid JSON, the source fingerprint, and the per-record text fingerprints. The manifest also records the JSONL checksum and extractor version. This establishes byte-level traceability and extraction checks, not independent domain validation or broad source completeness.

No new dependencies, model downloads, paid API calls, embeddings, vector store, retrieval index, or generation system were added. Evaluation candidate acceptance is unchanged. The next step is to inspect fragmentation choices and contextual dependencies using the prepared source records.

## 2026-10-18 — Public repository preparation

The learner requested a public GitHub repository. On resuming publication work, the assistant found an existing initial commit on `main` in a private `Herreran903/rag-from-scratch` repository. The public-visibility request remains the publication instruction.

Prepared a public-facing README, removed machine-specific personal paths from the documentation, added ignore rules for temporary files and credentials, and promoted the preparation utility to `scripts/prepare_corpus.py`. The public utility supports read-only integrity checking, optional checksum-pinned source download, and an isolated output directory. It does not depend on the original chat's scratch files and does not install packages or call models.

Recorded `pypdf==6.10.0` in `requirements.txt` without installing it. Added explicit LF rules for text artifacts so corpus byte fingerprints remain stable across checkouts. The local PDF is retained; the current tracked tree excludes it. The initial private commit already contained that snapshot, which remains in history because this preparation does not rewrite published commits. The source note identifies its official origin and third-party rights.

The publication scope is the learning project, preparation utility, source records, evaluation candidates, and process documentation. Temporary rendering files and other local work are excluded. Retrieval and generation implementation remain future steps.

Publication validation passed: read-only corpus integrity checking in the working directory and in an isolated export of the staged tree without the PDF; local reconstruction reproduced all five JSONL records byte-for-byte; a fresh official download in an isolated directory matched the pinned fingerprint and produced the same records. The staged diff passed whitespace checks. No packages were installed for these checks. The publication target is the public `main` branch of [Herreran903/rag-from-scratch](https://github.com/Herreran903/rag-from-scratch).

## 2026-10-18 — First LangChain exercise

The learner requested work with LangChain and related tools. The assistant checked official documentation and found that the libraries were not installed in the available checked runtimes. Because the initial instruction prohibited installations, the assistant asked whether this stage could install LangChain Core and text splitters in a project-local environment. The learner explicitly authorised installation in `.venv` and execution of the exercise.

Created an ignored `.venv` with Python 3.12.10 and installed `langchain-core==1.6.12`, `langchain-text-splitters==1.1.3`, and their required transitive dependencies. No system-wide packages or models were installed. The LangSmith SDK is a transitive dependency, but no hosted tracing, account, or API calls were configured for the exercise. Recorded direct dependencies and the full installed dependency set in separate requirement files. The initial no-installation instruction is superseded only for this authorised step; model downloads and paid API calls remain outside scope.

Added `examples/01_langchain_chunking.py`. It converts the existing source records into LangChain `Document` objects, preserves source and article metadata, and compares whole articles with recursive splitting at 180 characters / 40 target overlap and 100 characters / 20 target overlap. Character offsets refer to the normalized parent text. Unresolved-reference metadata is explicitly labelled as belonging to the parent article, not necessarily each child chunk.

The run produced 5, 8, and 15 chunks respectively. All source/text fingerprint, metadata, exact-offset, size-bound, and non-whitespace coverage checks passed. `pip check` reported no broken requirements. C5.1.18 split into two pieces under the smallest configuration: one retains the exception qualifier without the ambient-temperature phrase, and the other retains that phrase without its qualifier. This is an inspected context-separation risk, not a measured answer error.

Saved results and a concise ecosystem guide in [the chunking exercise](langchain-chunking/README.md). LangGraph, hosted observability, vector storage, embeddings, and generation remain future steps. Whole articles are the proposed initial retrieval baseline for this tiny corpus; this is a scoped engineering choice rather than a universal chunk-size recommendation.

Repeated the example in a separate scratch output directory with socket connections disabled. All three chunk JSONL files and the summary matched the first run byte-for-byte. This confirms that the exercised document/splitting path ran locally without external connections. No learner quiz or additional domain-validation claim was introduced.

## 2026-10-18 — Existing local Ollama model smoke test

The learner proposed using their existing local Ollama installation for experiments. The assistant checked the local CLI, installed-model endpoint, and running-model endpoint. Ollama 0.40.6 was available locally with no model loaded at inspection time. Selected the already-installed `qwen2.5:14b` completion model, approximately 9 GB on disk with Q4_K_M quantization, for a bounded generation exercise. The full installed-model inventory and personal machine paths were not added to project outputs.

Added `examples/02_ollama_grounded_generation.py`, reusing LangChain Core's `ChatPromptTemplate` and the standard-library HTTP client. It accepts only an already-listed local model, rejects cloud model markers, and calls the fixed loopback `/api/chat` endpoint. It never pulls weights. Both requests supply all five source articles explicitly, so this is a generation smoke test, not an automatic retrieval pipeline.

Ran Q002 and Q006 with temperature 0, seed 42, context setting 2048, generation budget 192, and a structured-output schema. Q002 preserved the displacement and asymmetric tolerance and cited C5.1.2. Q006 reported insufficient evidence in the provided subset, with no citations or numerical limit. Both responses completed normally and passed structural checks; the assistant inspected their content against the intended cases. No independent human validation, accepted-gold-set result, or general reliability score is claimed.

Wall times were 45.354 seconds for the first call and 0.728 seconds for the second. The first included approximately 25.1 seconds of model loading, so these are smoke-run observations rather than comparable latency benchmarks. Saved prompts, schema, generation settings, exact model digest, source fingerprints, versions, and outputs in [the Ollama smoke-test artifacts](ollama-smoke-test/README.md).

No new Python dependencies, model downloads, hosted tracing, or paid API calls were introduced. The existing models remain managed by Ollama; the requests set a one-minute keep-alive rather than changing global service configuration. Automatic retrieval remains the next pipeline step.
