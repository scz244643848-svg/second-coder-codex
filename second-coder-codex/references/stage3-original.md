---
name: codesheet-adjudication
description: Compare human and AI research codesheets, guide researcher decisions on discrepancies, and produce an audited adjudicated codesheet using the project's approved extraction protocol and template.
---

# Codesheet adjudication

Stage 3 follows researcher-led eligibility selection and AI extraction. The researcher chooses final entries; neither input automatically takes precedence. Use the project's current approved extraction prompt, codebooks, template and recorded amendments. Use only the researcher's approved eligibility criteria, field definitions and calculation rules.

## Begin and resume

Welcome the researcher and explain the result: a final codesheet with an auditable decision record. Ask for the folder containing Human_Codesheet.csv, AI_Codesheet.csv, source PDFs and supplied supplements, the approved extraction prompt, codebooks, Template_Codesheet.csv, AI_approved_estimates (the saved Stage 2 Master approved estimate list), any AI_coding_notes saved in Stage 2, and existing adjudication decisions or external lookup evidence. Identify files by inspecting the folder, then clarify only missing or ambiguous inputs. Never imply that files were inspected before reading them.

For a resumed session, read existing decisions and unresolved issues before asking anything. Preserve earlier authorizations and choices. Always end an interactive step with a concrete next question or action. During autonomous work, explain that the researcher need not do anything until the next decision. Actually perform announced checks before ending the turn.

Preserve original inputs. Save comparison outputs and decisions separately in the researcher's nominated Stage 3 folder. Use standardized names Human_Codesheet.csv, AI_Codesheet.csv and Adjudicated_Codesheet.csv, with Template_Codesheet.csv for the blank schema. Guide a researcher who has not installed the skill to the package README; obtain authorization for installation separately from adjudication. Do not operate NotebookLM as part of adjudication.

## Establish comparison conventions

Use prior agreed conventions if available; otherwise propose and ask about consequential choices, one issue at a time:

- Follow the template's field names and order; preserve extra input audit fields separately.
- Treat numerical differences agreeing at the coarser reported precision as rounding-equivalent. Retain additional precision only when source-supported. Do not apply this tolerance to counts, identifiers or categories.
- Treat equivalent wording as agreement; a missing versus a populated value requires an evidence-based decision. Follow the approved protocol's conventions for missing, uncertain and inapplicable values; preserve genuine zero separately from missing.
- Resolve estimate coverage and eligibility before field values. Keep every eligible distinct specification, even if its published coefficient and SE equal another specification. Deduplicate only repeated reporting of the same estimate.

Record any project-specific amendment explicitly. Do not repeatedly ask the researcher to reapprove established rules.

## Compare and adjudicate

Parse both inputs and verify headers and rows. Match estimates using article identity, source table, specification, outcome, sample and subgroup; never use equal coefficient/SE alone as a match. Resolve identifier conflicts from source evidence. Record unmatched rows without silently dropping them. If a row absent from one input is retained, identify that absence in the mapping; do not pretend a metadata donor is its matching estimate.

Produce a systematic comparison covering all template fields. Group repeated paper-level discrepancies when one decision applies to multiple estimates. Separate actual disagreements from wording/rounding equivalence and values derived from previously approved inputs. Check important shared values against source evidence too: two agreeing coders can share an error.

For each substantive discrepancy, give the human value, AI value, source locator, relevant approved rule and recommendation, then ask the researcher to choose the final entry. Keep questions short. If evidence is missing, offer an unresolved value using the approved protocol's missing-value convention, or ask for researcher-supplied evidence. An explicit choice to trust a comparator is valid: retain it and record that it was researcher-accepted rather than independently verified. Do not generalize that choice into automatic precedence for other fields.

Update the decision record immediately after each answer, including affected estimates, field, final value and reason. Keep the original values in supporting comparison records. Do not silently apply new eligibility criteria while resolving numeric fields.

## Calculations and external information

Use the approved project formulas and inputs. Distinguish reported statistics from derived values and keep different definitions of sample size or degrees of freedom separate where the protocol requires it. Record calculation inputs and any researcher-approved approximations. Recalculate derived values after their inputs change, retaining full calculation precision and following approved export rounding. Apply only approved sign and transformation conventions.

When an approved protocol requires external fields, follow its specified sources, lookup dates, reference years, units and completeness rules. Keep source records, raw inputs and calculations. Resolve unspecified consequential conventions with the researcher before lookup or calculation. Do not substitute remembered values, unsupported zeros or unapproved sources. If access is blocked, provide a concrete manual lookup request; distinguish researcher-provided values from independent verification.

## Finalize

Save a draft with the exact template schema and stable estimate IDs in supporting records. Offer consolidated review; the researcher may skip it and authorize finalization. This waives another review round, not numerical validation.

Before final export, verify row coverage, specification uniqueness, template order, category invariants, missing/zero handling, approved corrections and independent numerical recalculation. Explain any remaining evidence limitations already accepted by the researcher. Do not describe approved missing values as unresolved adjudication.

Deliver the final codesheet, estimate mapping, comparison/change audit, decision record and necessary lookup/calculation evidence. Keep draft and final clearly distinct. Provide a Stage 3 README with the input checklist, invocation example, review workflow and final-output explanation. Copy to the nominated folder and verify the saved files; do not claim a copy succeeded without checking it.
