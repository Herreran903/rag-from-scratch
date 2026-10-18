# Local Ollama Grounded-Generation Smoke Test

## Purpose

Try generation using an already-installed local model and the five FIA corpus articles. This checks the generation component with explicitly supplied context. It does not retrieve evidence automatically and is not an end-to-end RAG evaluation.

The chosen starting model is `qwen2.5:14b`, a locally installed quantized completion model. No model weights are downloaded by the example. The exact model digest, Ollama version, options, source fingerprints, and outputs are recorded in `results.json` after a successful run.

## Components

| Component | Responsibility |
|---|---|
| Corpus JSONL | Source text and article/page provenance. |
| LangChain `ChatPromptTemplate` | Construct the system and user messages with explicit context and question variables. |
| Local Ollama `/api/chat` | Run the installed model and return a structured response. |
| Python standard-library HTTP client | Send requests only to the fixed loopback endpoint. |

The example reuses the existing LangChain Core dependency. It does not require `langchain-ollama`, an additional client SDK, cloud credentials, or a vector database. A provider adapter such as `ChatOllama` can be introduced separately when that integration is useful to the learning exercise.

## Run

Start the existing Ollama service and use the project's current environment:

```bash
./.venv/Scripts/python.exe examples/02_ollama_grounded_generation.py

# Another model must already be installed locally:
./.venv/Scripts/python.exe examples/02_ollama_grounded_generation.py --model qwen2.5:14b
```

The script verifies the selected model against `/api/tags`, rejects cloud model markers, and never calls a model-pull endpoint. Its fixed inference destination is `http://127.0.0.1:11434`. All five article texts are supplied in both cases; this is an explicit context choice, not an automatic search result.

## Cases and interpretation

- **Q002:** ask for displacement and tolerance. Inspect whether the output retains the asymmetric tolerance and cites supporting evidence.
- **Q006:** ask for the engine-speed limit. Inspect whether the model recognises insufficient evidence within these five articles, without claiming that the entire regulation lacks an answer.

Outputs use `answer`, `citations`, and `insufficient_evidence`. A JSON schema constrains structure and allowable article identifiers; it does not prove that the answer is true or that a citation supports a claim. The script checks structural consistency, completion, and source fingerprints. Content review remains a separate activity.

Settings are temperature 0, seed 42, a 2048-token context configuration, and a 192-token generation budget. These are bounded smoke-test settings, not tuned quality recommendations or a promise of identical generations on different runtimes. Timing values include machine-specific conditions; the first case may include cold loading. After requests, the model is kept alive for one minute.

Two examples are insufficient to establish reliable behaviour, compare models, or accept an evaluation gold set. No automated quality score is claimed.

## Observed run: 2026-10-18

Ollama version: `0.40.6`. Model: `qwen2.5:14b`, digest beginning `7cdf5a0187d5`, with Q4_K_M quantization. The complete digest is in [results.json](results.json).

| Case | Observed response behaviour | Wall time |
|---|---|---:|
| Q002 | Preserved the displacement and asymmetric tolerance, citing C5.1.2; did not mark evidence insufficient. | 45.354 s |
| Q006 | Stated that the provided subset was insufficient, with no citations or remembered limit. | 0.728 s |

Assistant inspection found both behaviours consistent with the intended smoke-test cases. This is not independent human validation or acceptance of the candidate set. Both responses completed normally and passed the structural checks.

The first request included approximately 25.1 seconds of model loading. The two timing values are not directly comparable measures of question difficulty or general model speed. No other model was benchmarked, and no new model or Python dependency was installed for this step.

## Official references

- [Ollama chat API](https://docs.ollama.com/api/chat).
- [Ollama installed-model API](https://docs.ollama.com/api/tags).

The next pipeline step remains a simple retriever that selects evidence before this generation component receives it.
