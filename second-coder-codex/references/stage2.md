# Stage 2 procedures

## Batch selection and continuation

At the first Stage 2A entry, inventory the accessible research papers and supplements in the researcher's designated folder, including a collection supplied earlier during Stage 1. Use filenames and limited source inspection to identify papers, supplements and version ambiguities; do not read human coding/GT or perform full-corpus PDF conversion or estimate screening merely to choose a batch. Show a concise selectable paper list when selection is needed. Having all papers available does not designate all of them as the current batch.

Use the existing project progress record to keep batch membership and completed, pending and deferred paper statuses. Do not ask the researcher to maintain a separate inventory. Select approximately five main papers per batch, or the researcher's designated size; corresponding supplements do not count as separate papers, and a smaller final batch is acceptable.

At initial selection and each return to 2A:

- If the current/next batch or a batch order has already been approved, name its papers and begin 2A without requesting the same selection again.
- If papers are available but the next batch is unspecified, list the remaining unprocessed papers and ask which approximately five to use. The researcher may instead authorize an ordering, such as filename order, for later batches; do not impose an unapproved order.
- If the next batch's sources are unavailable, request only those papers and their relevant supplements. Reuse available files and ask only about missing sources or ambiguous associations.

After the current batch's Stage 3 finalization, output delivery and existing prompt review, save its completed status and follow these same branches for the next batch. Continue 2A -> 2B -> 2C -> Stage 3 using the latest approved prompt; do not restart Stage 1 or ask for previously supplied files. Keep completed papers out of routine next-batch selection. Keep deferred papers visible with their pending issue rather than silently completing or dropping them. If no pending or deferred papers remain in the designated project, report completion instead of requesting another five. Pause when the researcher asks to pause or stop.

## 2A — required PDF preparation

Stage 2A is fixed. After Stage 1 approval, proactively say: “Your extraction prompt is approved. I will now begin Stage 2A: preparing and checking the PDF reading materials for this batch. Once preparation is complete, I will move directly to Stage 2B, where I will propose eligible estimates for your review, paper by paper.” If the batch PDFs or supplements have not yet been designated, request only those missing inputs and then start preparation. Do not ask whether to use or skip 2A, including when resuming a project with a saved `skip_2a` preference.

First organize the already supplied, designated papers and supplements into the batch source list. Reuse clear paper-supplement associations and batch designations; ask only about missing sources or uncertain supplement ownership or batch membership. A representative paper from Stage 1 belongs to this batch only if the designation includes it. Do not require the researcher to refill a material inventory, rename files, or reconfirm an unambiguous mapping.

After the required materials are readable, say: “Stage 2A is complete. I will now begin Stage 2B and prepare the proposed eligible estimate list for the first paper.” Then actually start that work; do not stop after the announcement or ask the researcher to say “continue.” Disclose any remaining preparation limitation accurately rather than claiming successful completion.

Find available bundled or system Python and verify PyMuPDF; do not assume all Codex environments include either. Use a project-local environment if dependency installation is needed, respecting execution permissions. Do not require the researcher to manage routine commands or change global configuration. A missing dependency is a preparation blocker, not proof that a PDF is unreadable.

Use `scripts/prepare_pdfs.py` with a designated JSON manifest and output folder. Python 3.10+ and PyMuPDF are required. The manifest is `{"papers":[{"paper_id":"paper-01","pdf":"/absolute/main.pdf","supplements":["/absolute/appendix.pdf"]}]}`. IDs are internal, unique, safe folder names; do not add them to data columns. Only manifest-listed PDFs are processed. Source hashes keep cached aids tied to their originals.

Example: `python scripts/prepare_pdfs.py --manifest batch_sources.json --output reading_aids`

Outputs contain per-source page-marked full text, table-related text, table/successor and suspicious-page PNGs, and a quality report. PDF page numbers are one-based physical pages. Keep printed page labels distinct. Automated table keywords locate possible rendering targets; they do not define eligibility or prove completeness. Read the full text and inspect necessary source pages, including appendices, narrative estimates, equations, headers and notes.

Generated aids initially have `prepared_unchecked` status. Inspect flagged pages and representative complex tables; record the actual source checks and change project paper status to `readable`, `needs_attention`, or `blocked`. Empty extracted text may indicate scans; images can still be readable. Render additional pages with `--render-pages 2,5-7` and `--source /absolute/main.pdf --output reading_aids`. Supplementary rendering never replaces full text. OCR or other local reading tools are optional remedies after checking the page, not mandatory blanket processing.

Preserve originals. Changed PDFs create new hash-scoped aids; do not overwrite approved source versions. A failed source is explicitly reported, and other sources continue. No batch-wide ready status until required sources are readable. If preparation fails, attempt a proportionate repair or an equivalent local text/rendering method and record it. Do not silently bypass required 2A by switching to direct-only reading. If preparation remains blocked, pause the affected paper and report the specific cause and remedy; other papers may continue preparation. A researcher can explicitly authorize an exception, which must be recorded as incomplete 2A for that paper.

Complete original PDFs and supplements must be accessible to eligibility and coding agents, even with successful conversion. Reading aids never replace original sources.

## 2B — propose and approve estimates

On entering 2B, briefly explain the researcher's task: check each proposal against the complete sources, look for omissions, and approve the paper's list. Say that this review can require substantial attention depending on the paper and estimate count. Do not give a time estimate or repeat the full workflow overview.

### Check referenced appendices and supplements before approval

While reading each paper, check references to Appendix, Online Appendix, Supplementary Material and equivalent labels. Determine whether each relevant referenced item is embedded in the main PDF or present in the supplied files. Verify article identity, designated version and referenced table/section labels where possible; a similarly named attachment or same-author paper is not enough. This is a source-completeness check within the selected study, not a new study-screening or paper-version-selection stage.

Record a short source check with the paper's review: referenced material, citation location in the main paper, matched supplied file/pages, availability and any possible impact on eligible estimates or coding definitions. Reuse the existing review/approval notes; a new complex ledger is unnecessary. If no separate supplement is referenced, say what was checked rather than inventing a missing-file requirement or claiming unreferenced material cannot exist.

When an item is missing or its match is uncertain, show the exact reference location (physical PDF page and table/section), name the specific item, explain its possible effect on scope/coding, and ask the researcher to supply or identify it. Search/retrieval is allowed only under the project's approved source-search permissions; do not replace the designated paper with a newer or different version. Keep human coding/GT unread until Stage 3.

Complete this check before asking for approval of the paper's estimate list. Do not treat an unavailable supplement as evidence that an estimate or field was not reported. Do not mark complete screening or source completeness while a potentially relevant item is unresolved. Available-source candidates may remain provisional, and preparation of unaffected papers may continue. If the researcher explicitly decides to proceed with limited sources or defer a paper, record the scope limitation, the decision and its effect on the master list; do not silently exclude unseen estimates or describe the result as complete-paper coverage. This decision is part of the existing eligibility review, not an additional approval round.

When material arrives, verify its match, prepare it through 2A, and resume the affected review. Revise the saved list and obtain its explicit approval; if approval had already occurred, explain and reopen only the affected scope. At master confirmation, carry forward any accepted source limitations or deferred papers.

A deferred paper is not a zero-eligible-estimate paper. Preserve its deferred status separately and obtain an explicit decision about the revised current-batch scope before proceeding with a partial batch. Do not mark the deferred paper's screening complete or silently count unseen estimates as excluded.

### Review and approve the paper's list

Review one paper at a time against the approved prompt. Do not fill the entire codesheet yet. Identify each proposed estimate uniquely using source file, PDF page, table/panel, row/column, model/specification and relevant sample/outcome/subgroup. Give an eligibility rationale and separately flag ambiguous candidates. Stable internal keys and later row mapping belong in auxiliary records, not extra template columns.

Provide an exact enumerable list. Follow the paper's table/panel structure where applicable, showing proposed counts per group and precise source locators; use suitable source sections for estimates outside tables. Keep ambiguous candidates separate from clear proposals and state their counts separately. Grouping is for navigation, not a new definition of an estimate: apply the approved Stage 1 rules. “All estimates in Table 4” is insufficient. For a large list, save the full file and show a readable summary/link; do not truncate or invent completeness. Include a short account of result tables, appendices and narrative sections reviewed to help detect omissions; clearly excluded estimates need not each be listed.

At the first paper's list, briefly explain how its rows are distinguished under the approved rules, using the actual source/specification labels. Do not repeat this explanation for later papers unless a new ambiguity arises or the researcher asks.

Ask: “Please review the proposed estimates against the paper for omissions, duplicates, and ineligible entries. You may request changes or approve the list. Once approved, I will save the decisions and proceed to the next paper.”

Apply edits, resolve material eligibility questions, and obtain explicit approval of the revised version. Zero-estimate papers also need confirmation. Preserve change history; rejected candidates must not reappear in an approved merge. Save each approved list, version/hash, count, prompt version and approval evidence. Then immediately begin the next paper.

Merge from the saved approved files, not conversational memory. Check key uniqueness and all papers' inclusion, including zero counts. Present per-paper counts and total with the complete `AI_approved_estimates.csv`. Ask for explicit final master confirmation; it checks the assembled inventory, rather than repeating all decisions. Begin coding automatically upon approval.

For script checks use an auxiliary mapping with columns `estimate_key,paper_id,codesheet_row` (one-based data row, excluding header). The approved list must have `estimate_key,paper_id`; it may include locator and selection metadata. Coding agents produce a mapping for each per-paper output; the coordinator adjusts row numbers when merging. Match source/specification identity too: keys alone are not evidence of a valid match.

## 2C — independent coding and export

Announce that independent per-paper coding is starting. Each fresh worker reads the complete paper PDF, supplements, Stage 2A reading aids, the approved list and frozen prompt/template. Supply explicit paths and scope; prohibit GT and other workers' results. Workers write separate paper folders; only the coordinator writes master files. Keep the prompt/template/source hashes in the run record. Queue remaining papers as slots become available. If a worker fails, retain its partial output and resume/retry that paper without duplicating estimates; do not merge partial output as complete.

Code precisely the approved estimates. Use full-paper reasoning to connect tables and narrative, verifying that sample/model/specification information actually applies to each estimate. Same-paper location alone does not establish applicability. No required entity hierarchy, scoped ledger, or resolver. Follow project-specific signs, missing values, categories, external-source permissions and calculation rules.

Append `AI_reason` to the exact template header/order. Make reasons field-specific where needed: `Sample period: Section 3, PDF p. 10. Coefficient/t: Table 4, panel A, row X, column 2, PDF p. 18. SE = abs(b/t), inputs ... . Field Y unresolved because ...`. Include essential numeric inputs and permitted approximation assumptions. Never use a generic reason that obscures multiple unsupported choices. Quote only short necessary source fragments.

Field uncertainty: follow the approved missing convention and add an actionable entry to `pending_issues.csv` identifying paper, estimate, field, issue, locator and current disposition. Known source absence may be an approved missing value rather than unresolved. Eligibility rediscovery: report to coordinator; researcher decides, updated list approval is saved, and coding/mapping is reconciled. Rule changes require version approval and impact review. Workers cannot silently reinterpret approved scope.

Validate each paper against its list; check exact columns plus `AI_reason`, categories/invariants, duplicated specifications, completeness and formula inputs/results. Counts alone are insufficient. Repair technical errors autonomously; ask only for substantive researcher decisions. Each row must have meaningful `AI_reason`; a pending row can be exported for Stage 3 but cannot be described as fully resolved.

Merge per-paper codesheets with `scripts/merge_codesheets.py --manifest coding_files.json --template Template_Codesheet.csv --output new-master-version-folder`, not copied chat text. Its manifest is `{"papers":[{"codesheet":"paper-01/AI_Codesheet.csv","approved":"paper-01/approved.csv","mapping":"paper-01/mapping.csv"}]}`. Include every batch paper, including zero-estimate files with headers. All approved-list headers must match. It adjusts mapping row numbers, checks master coverage, and refuses to overwrite existing master CSVs. Separately reconcile the merged scope with the frozen master approved list, including zero-paper counts, and preserve per-paper files. `scripts/check_codesheet.py` checks header and one-to-one mapping with the approved list, not semantic accuracy or all project calculations; perform those separately. Export `AI_Codesheet.csv`, `AI_approved_estimates.csv`, `AI_estimate_mapping.csv`, `pending_issues.csv`, and a short validation report recording actual checks and limitations.

Freeze independent outputs before requesting GT. State counts and remaining issues, link files, and name the first paper to adjudicate in Stage 3. Request only that paper's complete human-coded rows in a separate CSV/XLSX, not the batch or whole-project human codesheet; follow the per-paper intake in `stage3.md`.
