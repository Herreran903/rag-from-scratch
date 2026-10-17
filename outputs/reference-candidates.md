# Reference Candidates: Engine Specifications

## Scope and review status

Prepared on 2026-10-17 through assistant inspection of the official PDF's extracted text. This is a development exercise, not an implemented retrieval experiment.

**Source checks:** completed by the assistant for all cases. **Learner review:** Q002 reasoning exercise completed correctly; Q005 exception recognition recorded with an assistant clarification; the remaining cases are pending. These are draft reference answers, not an accepted gold set. The authoring assistant also performed the source check, so this is not independent validation.

## Source and evidence scope

- Document ID: `fia-f1-2026-section-c-issue-20`.
- Edition: Section C, Issue 20; document date: 2026-08-05.
- [Official FIA PDF](https://www.fia.com/system/files/documents/fia_2026_f1_regulations_-_section_c_technical_-_iss_20_-_2026-08-05.pdf).
- Exercise evidence scope: C5.1.1-C5.1.4 and C5.1.18 only.
- Printed pages C61-C62; PDF viewer pages 61-62 (one-based).

The linked PDF contains much more than this subset. Having access to a whole PDF does not make all of it part of this exercise's evidence scope. A local source snapshot, checksum, and article records are now available in the [minimal corpus](corpus/README.md). No search index has been built.

Answers below are paraphrases. Article anchors identify the supporting original passages; no verbatim passage collection is reproduced here.

## Q001

**Question:** What type of engine does C5.1.1 permit?

**Draft reference answer:** A four-stroke engine using reciprocating pistons is required.

**Evidence:** C5.1.1, printed page C61, PDF page 61.

**Expected behavior:** Answer from the scoped evidence.

**Review checks:** Preserve both the operating cycle and piston type. Do not add requirements from general engine knowledge.

## Q002

**Question:** What engine cubic capacity and tolerance does C5.1.2 specify?

**Draft reference answer:** Nominal displacement is 1600 cm3, with +0/-10 cm3 tolerance, corresponding to 1590-1600 cm3 inclusive.

**Evidence:** C5.1.2, printed page C61, PDF page 61. The interval is an assistant-derived arithmetic restatement of the specified value and tolerance.

**Expected behavior:** Answer with units and the asymmetric tolerance.

**Review checks:** An equivalent interval is acceptable; an answer giving only the nominal capacity is incomplete for this question. A symmetric tolerance is incorrect. Full treatment of measurement conventions is outside this case.

**Learner review, 2026-10-17:** The learner correctly explained that the tolerance permits no positive deviation and that the proposed value exceeds the upper bound. The assistant clarified the volume unit as cubic centimetres (cm3), rather than centimetres. Outcome: correct interpretation of the asymmetric tolerance. Independent inspection of the PDF by the learner was not explicitly reported; this records the reasoning exercise, not an independent source audit or final gold-set acceptance.

## Q003

**Question:** What cylinder count, arrangement, and cylinder geometry does C5.1.3 require?

**Draft reference answer:** Six equal-displacement cylinders must form a V with a 90-degree bank angle; each cylinder's normal cross-section must be circular.

**Evidence:** C5.1.3, printed page C61, PDF page 61.

**Expected behavior:** Include all the requested characteristics.

**Review checks:** The question explicitly names geometry so that its scope matches the draft answer. A statement such as "V6" alone does not cover all requested points.

## Q004

**Question:** How many intake and exhaust valves must each cylinder have under C5.1.4?

**Draft reference answer:** Each cylinder needs two inlet valves and two outlet valves.

**Evidence:** The valve-count statement in C5.1.4, printed page C61, PDF page 61.

**Expected behavior:** State the count for each valve function and make the per-cylinder basis clear.

**Review checks:** Giving only a total does not fully answer this question. This case does not assess the article's other construction or sealing requirements.

**Curation decision:** Narrowed the original candidate, "What valve requirements are specified?" The original was too broad for a first exercise because the rest of C5.1.4 includes additional requirements and cross-references. This is a documented question revision, not a claim that those requirements are irrelevant.

## Q005

**Question:** What default interpretation does C5.1.18 establish for numerical values in Article C5?

**Draft reference answer:** Unless another provision specifies otherwise, C5 numerical values represent static values at ambient temperature.

**Evidence:** C5.1.18, printed page C62, PDF page 62.

**Expected behavior:** Preserve the default, its scope, and the possibility of an explicit exception.

**Review checks:** Dropping the exception qualifier changes the meaning. Do not invent a numerical ambient temperature or an unstated measurement procedure.

**Learner review, 2026-10-17:** The learner correctly identified that the default is not unconditional, but described exceptions as possible changes directed by the FIA. The assistant clarified that this qualifier alone does not establish discretionary authority or an amendment procedure: a different interpretation must be supported by an applicable provision specifying otherwise. Outcome: exception recognition recorded; the authority-based explanation required correction. No specific exception or amendment power was established in this exercise.

## Q006

**Question:** What is the engine speed limit?

**Draft reference behavior:** State that the selected subset does not provide enough evidence to determine the limit. If broader retrieval is permitted in a later exercise, request or retrieve the relevant additional provisions.

**Evidence scope:** The five selected articles contain no engine-speed-limit requirement.

**Expected label:** `insufficient_evidence_in_subset`.

**Review checks:** Do not supply a limit from model memory. Do not claim that the full regulation lacks an answer. Reassess the label whenever the evidence scope changes. C5.14 is a candidate for later inspection, not a verified answer in this exercise.

## What this exercise establishes

Each draft now has an explicit question scope, source anchor, intended behavior, and checks for omissions or unsupported additions. Q002 distinguishes a sourced requirement from arithmetic interpretation; Q004 illustrates question refinement; Q006 illustrates corpus-dependent answerability.

These checks are proposed review criteria, not scores obtained from a running system. There are no retrieval metrics, model-answer comparisons, or human acceptance results yet.

## Human review record

Q002 has a recorded learner reasoning review, assessed as correct by the assistant. Q005 has an initial learner review with an assistant clarification about the basis for an exception. Q001, Q003, Q004, and Q006 remain pending learner review. Final case acceptance has not been recorded. Review each case against the linked source and record acceptance, a correction, or rejection with its rationale. Keep the case IDs when editing wording so the process remains traceable.

Once reviewed, these cases can serve as a small development reference set. Broader quality claims will require more varied cases and separate evaluation data.
