# RAG from Scratch

An independent learning project for understanding Retrieval-Augmented Generation (RAG) from first principles, one small step at a time.

## Current scope

Define the scope and learning approach before implementing a RAG system. No dependencies will be installed, models downloaded, or paid APIs called at this stage. Implementation choices will be agreed on together.

The selected domain is the **FIA 2026 Formula 1 Technical Regulations**, connecting this project with the learner's previous exchange-program work. Start with engine specifications, then consider wider power-unit requirements and aerodynamics.

Working question: **How can a RAG assistant retrieve the relevant technical requirements, definitions, conditions, and exceptions from the correct regulation edition and answer with verifiable sources?**

This directory is the project root. This project is independent of the Whisper project at `C:\Users\herre\OneDrive\Documentos\simulst-from-scratch`.

## Gradual learning path

1. **Documents:** Choose a small collection and understand how to read and preserve its text and metadata.
2. **Chunking:** Split documents into useful passages while retaining source references.
3. **Search:** Build intuition with simple keyword search and inspect its limitations.
4. **Embeddings:** Understand vector representations and similarity before selecting any model.
5. **Retrieval:** Select relevant passages and examine retrieval quality.
6. **Generation with sources:** Use retrieved context to answer questions with traceable citations and acknowledge missing evidence.
7. **Evaluation:** Create a small question set and assess retrieval, answer accuracy, and source support.

## Working conventions

- Use English for files, code names, and commands.
- Explain each step in Spanish before implementing it.
- Agree on scope before adding implementation or dependencies.
- Use `work/` for scratch files and `outputs/` for deliverables.

## Next step

Inspect the prepared [minimal corpus](outputs/corpus/README.md): an official PDF snapshot, source manifest, and five article records with provenance. Next, discuss retrieval fragmentation and contextual dependencies using these records before implementing basic search. Learn through practical construction and analysis, rather than question-by-question oral exercises.

The [draft reference answers](outputs/reference-candidates.md) remain development candidates with incomplete human review. Treat dataset curation as a separate workstream. Local corpus preparation is complete; retrieval, embeddings, and generation remain unimplemented. No dependencies have been installed.

## Process documentation

See the [process log](outputs/process-log.md) for scope decisions, source provenance, the LLM-assisted evaluation-data method, candidate questions, and pending verification. The candidates are not yet a validated gold set.
