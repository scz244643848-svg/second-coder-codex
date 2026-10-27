---
name: extraction-prompt-development
description: Develop a researcher-approved extraction prompt from supplied codebooks, a blank codesheet, research protocols, and representative papers. Clarify eligibility and field definitions, obtain independent review, and guide optional external LLM feedback. Use for protocol development, not routine extraction or codesheet adjudication.
---

# Extraction prompt development

Help the researcher produce a standalone, versioned extraction prompt for their chosen extraction tool. This skill develops the prompt; it does not run NotebookLM or fill study codesheets. Keep conversation short, discuss one substantive decision at a time, and end each exchange with a clear next question or action. When awaiting external feedback, ask the researcher to return it rather than inventing progress.

## Start with a materials folder

Welcome the researcher and explain the outcome: review their materials, resolve unclear rules, and draft instructions for approval. Ask them to create a folder containing relevant codebooks, a blank codesheet, the research question and eligibility protocol, relevant papers, and additional coding notes. Ask for its path and the specific files to read. Do not say only 'send whatever you have'. Do not require every suggested document before starting.

Read only the designated materials. Ask to read a blank template if it has not yet been designated. Explain any access limitation and proceed with accessible materials. After inspection, ask targeted questions about gaps and unwritten conventions, rather than repeatedly asking 'what else should I know?'. Do not consult a previous extraction prompt unless the researcher requests it.

## Establish the extraction contract

Identify the research question, eligible exposure, outcome, comparison group, study restrictions, and unit of extraction. Clarify whether the researcher selects estimates, the extraction tool proposes them, or another selection workflow applies. Clarify batch versus one-paper processing, supplied appendices and supplements, source-search permissions, duplicates, and the approval boundary before field completion. Use the researcher's approved project rules; do not introduce eligibility criteria from unrelated projects.

Read the actual template column names and order. Develop an instruction for every field: meaning, allowed values, supporting evidence, calculation if applicable, missing versus zero, and uncertain/inapplicable handling. Resolve conflicting codebooks explicitly. Agree where stable candidate IDs and source locators will be recorded: use a suitable existing template field or a separate ID-to-row mapping when no suitable field exists. Do not assume a particular field name. Ask before adding or changing a field; when authorised, edit the blank template and verify the header without creating a completed codesheet.

Audit eligibility and definitions for ambiguity, contradictions, omitted cases, reference groups, interacting or nonlinear exposures, marginal/total effects, mediators, and estimator differences as relevant to the research design. Clarify signs, transformations, uncertainty recovery, degrees of freedom, precision, and external data sources/years/units when needed. Do not apply all these topics mechanically to unrelated projects. Use difficult supplied examples to test whether two coders could implement a rule consistently. Do not produce pilot codesheets unless separately requested.

Keep a working decision record as choices are settled. Distinguish researcher decisions from suggestions and unresolved issues. Settled choices persist; do not repeatedly reopen them without new evidence. If a source or reviewer conflicts with an approved choice, explain the conflict and ask only when a change is material.

## Draft and independently review

Draft the complete standalone prompt in the agreed location. It must explain source permissions, candidate selection and approval where applicable, output schema, every field, calculation inputs and formulas, missing-information rules, evidence locators, and completion checks. Match the actual template exactly. State the decision hierarchy so project-approved rules override conflicting reference materials. Prevent silent omission when a batch exceeds output limits.

Have a fresh independent agent check the draft before presenting it for researcher review. Give it the designated source materials, template, decision record, and draft; request a read-only audit of eligibility, all fields, contradictions, ambiguous instructions, and calculations. Correct drafting mistakes. Bring substantive proposed changes to the researcher one at a time. If agents are unavailable, disclose that independent review could not be performed; do not label a self-check independent.

Always offer the researcher a review of the draft. They may skip it. Never interpret skipping review as final approval.

## Offer external LLM review

After offering researcher review, always ask whether they want to take the draft to another LLM, such as Claude or Gemini. This is optional. If they accept, provide the saved prompt and identify the source files and template they should give the reviewer. Supply this adaptable instruction:

> Review this extraction prompt for ambiguities, contradictions, missing field instructions, and calculation errors. Its explicit project rules take precedence over the source documents where they differ. Prioritise problems that could change which estimates are selected or how fields are coded. Suggest specific corrections.

Explicitly ask the researcher to paste or provide the other LLM's output back here. Do not contact another service on their behalf merely because they accept manual external review. Wait for their feedback; no response does not mean the review occurred.

When feedback arrives, compare it with approved decisions and the designated sources. Separate valid drafting fixes, substantive changes requiring a decision, deliberate conventions to retain, and irrelevant comparisons with other protocols. Discuss one decision at a time, make accepted edits, and preserve rejected suggestions in the decision record. Do not adopt review advice automatically or claim that reviewer agreement establishes extraction accuracy. Offer another review when appropriate without making it mandatory.

## Approval and handoff

Ask explicitly whether the researcher wants to review again, obtain another external check, or approve the prompt. Once approved, mark the version and approval date; leave subsequent revisions for a new version. Preserve the approved rules and template together. Verify that files copied to a designated shared folder match the local deliverables. Do not claim saved files or installation that did not occur.

Provide a Stage 1 README covering the materials folder, starting the skill, the conversation, independent and optional external review, researcher approval, final deliverables, and the handoff to extraction. Use standardized output names Human_Codesheet.csv, AI_Codesheet.csv and Adjudicated_Codesheet.csv; the blank schema is Template_Codesheet.csv. Use batch folders to distinguish batches. If the researcher has not installed this skill, guide installation using the package README before routine use; direct reading is a fallback. Keep the reusable skill separate from a project's approved prompt and domain rules. Deliver the approved prompt, compatible blank template, decision record, skill, and README. Do not build Stage 2 or Stage 3 components during Stage 1 unless requested.
