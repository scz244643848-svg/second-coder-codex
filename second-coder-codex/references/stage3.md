# Stage 3 integration

Follow the preserved professor adjudication workflow in `stage3-original.md`, with these agreed integration conventions:

- Paper-by-paper adjudication through a grouped review panel in the same conversation. Show all discrepancies for the current paper together, with separate groups wherever evidence, field or decision scope differs. Codex guides each next action. Only the interaction changes; the underlying comparison, eligibility, calculation and finalization workflow remains the same.
- Request human data after independent AI output is frozen, one paper at a time. Name the paper currently being adjudicated and ask for a separate CSV/XLSX containing all its human-coded rows and the original coding columns. Do not ask the researcher to restrict these rows to the AI-approved list; coverage disagreements must remain visible. Do not request or accept whole-project or multi-paper GT as the comparison input. If such a file is supplied or encountered, leave other papers' coding values unread, stop broader inspection and request a current-paper-only export; do not dump or summarize the full sheet. Never assume a sheet or header without inspecting the permitted current-paper input.
- `AI_reason` is an authorized audit field. Read it as evidence/explanation, not a comparison variable. Compare all original template fields. Final `Adjudicated_Codesheet.csv` uses the data template; preserve AI reasons in the original AI output and audit records.
- Resolve unmatched/ambiguous estimates and eligibility before field disagreements. IDs and row numbers alone cannot establish correspondence. Equal coefficients do not establish identity. Record AI-only/human-only records and the researcher's coverage decisions.
- Show human value, AI value, source locator, approved rule and recommendation for substantive disagreements. The researcher decides. Group repeated issues only where the same evidence and decision actually apply. Check important shared values too; agreement is not proof of truth.
- Follow the source-evidence display requirements below before asking for each substantive decision. A descriptive choice between AI and human values without source evidence is insufficient.
- Keep clicks as unconfirmed panel drafts, with best-effort host widget-state persistence. After the researcher reviews the summary and clicks Confirm and send to Codex, the host sends the exact decisions into this conversation. Save that message payload and validate/import it through `review_inline.py`; only a successful import establishes project receipt. Apply choices to the listed estimate-field pairs and retain the original values, final value, rationale, approval and source evidence. Recompute derived values when their inputs change. Draft state and a generic completion message are not approval.
- Retain uncertain issues until resolved or the researcher explicitly accepts an approved missing value. Do not silently mark an unresolved draft final.
- Offer consolidated final review/finalization following the original workflow. Validate actual coverage, schema, invariants and numerical calculations; save estimate mapping, comparison/change audit, decisions, and final dataset. Preserve originals.
- After batch completion assess prompt defects, propose only necessary approved revisions, and identify affected earlier records. No compulsory full-corpus second extraction.
- After finalization, follow [output organization](output-packaging.md) to deliver a categorized folder containing the final data and all generated auxiliary artifacts, including the evidence images used in the conversation.

Opening guidance (insert the actual paper title): "Independent AI coding for this batch has been saved. We will begin adjudication with [paper title]. Please provide a separate CSV or Excel file containing only this paper's human-coded data, including all estimates you coded for it. Do not provide the whole-project or multi-paper human codesheet. I will match the estimates and show all substantive differences together in a panel in this chat, with source evidence. Choose Human, AI, Other value or Defer, review the summary, then select Confirm and send to Codex. I will receive your decisions here and continue the checks and adjudicated codesheet."


Adapt that request to existing designated current-paper inputs: accept CSV/XLSX and identify the relevant worksheet when necessary. Reuse the saved AI output, source PDFs, approved rules and decisions rather than asking for them again. Briefly explain that source-based comparison and adjudication can require substantial researcher time, depending on the number and complexity of differences. State what the researcher must do now: provide the current paper's human-coded file if missing, or inspect the evidence, choose values in the review panel and confirm the summary. Do not predict fixed completion times or treat human data as automatically correct. When waiting, identify the exact material or confirmation needed. After receiving the marked confirmation, validate and import its exact decisions and continue the authorized recording, validation and output work without another generic approval request.

After adjudicating a paper, save its decisions, name the next paper in the batch and request only that paper's human-coded file. Reuse an already supplied current-paper-only file instead of requesting it again. Keep per-paper human inputs distinguishable in the existing batch records. After all papers are adjudicated, produce the batch's combined final codesheet through the existing finalization and delivery workflow, then follow the next-batch transition in `stage2.md`.

## Source evidence at the point of decision

For each substantive disagreement, unresolved item, or eligibility/coverage decision requiring researcher judgment:

1. Identify the paper, estimate/specification, field and both values. State whether the AI value was reported, calculated or inferred. Do not invent a source for the human coder's value; say when its basis is unknown.
2. Open the complete original PDF or supplied supplement and locate the relevant evidence. Reuse a Stage 2A page image only after verifying its source hash, page and readability. Render missing evidence from the original using available PDF tools or `scripts/render_evidence.py`. A source screenshot must preserve original page pixels; do not recreate the table as an image or manufacture a screenshot from AI text.
3. Display the actual source screenshot in the selected group's evidence view, with enlargement and the full page available. Preserve choices when returning to the complete group list. Keep the all-group list complete; do not drop issues to fit images in the panel. The helper embeds original images up to the inline size limit and offers a source-image request for the remaining originals, which Codex must visibly show in the same conversation. This does not approve or change values. Merely saving an image or inspecting it privately is not showing it to the researcher. Include enough context to see the table title, panel, headers, row labels and notes. Use a wider or second image when needed and multiple pages when evidence spans locations. If actual display is unavailable, provide the textual fallback below and state that limitation.
4. Label each image with the source filename, one-based PDF page, printed page if visible, table/panel/row/column or section/paragraph. Tell the researcher exactly what to look at and connect the visible text/numbers to the differing codes. A page number alone or “see Table 4” is insufficient.
5. Give the relevant approved rule, a concise explanation of the discrepancy, and a recommendation grounded in the evidence. For calculations show the source inputs and calculation separately from the screenshot. Ask for the final value only after this evidence is presented.

One evidence display can support a grouped decision when exactly the same evidence/rule applies; list all affected estimates and fields. Do not request a separate approval merely to create a screenshot. Inspect rendered images for legibility and correct source/page before presenting them.

The helper renders a full source page and optional context-preserving crop:

`python scripts/render_evidence.py --source paper.pdf --page 18 --output evidence/paper-01/issue-003 --dpi 180`

Use a new issue/evidence folder for each render. `--clip x0 y0 x1 y1` optionally renders a detail in PDF page coordinates while retaining the full-page image; use it only after inspecting the layout. Source hash, page, resolution, crop and image hashes are saved in `evidence.json`. The helper creates files; the agent still must inspect and visibly present them. An equivalent renderer is acceptable.

## When screenshots cannot be produced or displayed

Briefly explain the actual limitation. Provide all of the following that the source permits:

- Exact source file and a clickable link, physical PDF page plus printed page if known, table/panel/row/column or section and paragraph.
- A short verbatim source excerpt, or an accurately transcribed small table fragment with its row and column labels. Clearly label it as text/transcription, not a screenshot. Do not substitute the AI's paraphrase for a quotation.
- Human value, AI value, the particular source text/number supporting the AI value, any separate source supporting an alternative, and the approved rule/calculation connecting evidence to the proposed final value.
- What remains uncertain. If the source itself cannot be read, say evidence is unavailable and request the specific page/material or leave the decision unresolved; never invent a quote or source locator.

Example presentation structure (fill with actual evidence, not illustrative invented values):

> **Paper / estimate / field:** [identity and field]. **Human:** [value]. **AI:** [value].
>
> **Source:** [file link], PDF p. [physical page], Table [number], panel [label], row [label], column [label].
>
> [Display screenshot and link, or explain the limitation and provide a short labeled excerpt/transcription.]
>
> **What to check:** [specific visible wording/number and how it relates to the discrepancy].
>
> **Rule and recommendation:** [approved rule, calculation if any, proposed value and remaining uncertainty].
>
> Please choose the final value or leave this item unresolved.

Save relative evidence links with each discrepancy/decision record. Preserve the original AI reason and both input values even if adjudication changes them. During packaging, make these links resolve to `06_Source_Evidence` within the delivered folder; do not leave the researcher with links that only work on the author's machine.

## Grouped review and direct confirmation

Read [grouped review implementation](grouped-review.md) and use its panel builder and confirmed-message importer. Show every substantive current-paper field discrepancy together after coverage is settled. A shared group is allowed only for the same field, Human/AI alternatives, source evidence and decision scope. Display the scope and count, expose all members and allow individual exceptions. Similar wording alone does not justify grouping.

Follow the [mandatory in-conversation handoff](grouped-review.md#mandatory-in-conversation-handoff) as soon as the review is ready. Display the actual generated panel in this conversation, not a code preview, standalone file link or localhost page. Reuse existing review state without resetting confirmed choices. The panel's source view keeps the selected issue's choices, evidence and explanation together; Back to all groups returns to the full list. Source requests must preserve choices and never be interpreted as decision confirmation.

Use the readable design: prominent values, bold Other value and Defer controls, Human/AI alternatives, original source images, enlargement, precise locators, rules and recommendations. No recommendation is preselected. Other value supports approved corrections and missing tokens. Defer remains unresolved and blocks confirmation. Retain the existing textual fallback when evidence is unavailable.

The researcher sequence is evidence -> click choices -> Review decisions -> Confirm and send to Codex. The panel calls the host's follow-up action with a compact, explicit group-default-and-exception record bound to the saved snapshot. No download, external browser, location search or completion message is part of this edition. Widget state is only a draft; it cannot replace the actual confirmation. Do not claim receipt until the importer verifies and records the message. A cancelled or failed action can be retried. The summary remains the existing consolidated review; an explicit request to skip another review round retains its original meaning, with specific decision authority and validation still required.

After receiving and importing confirmation, apply only those estimate-field choices, preserve originals, recompute approved dependent calculations and complete the original finalization checks. Produce the same per-paper result, batch master, audit records and categorized folder. Source-only requests and repeated confirmations do not create new scientific decisions. No persistent service or background watcher is needed. If the host lacks inline display or the follow-up action, preserve the review, explain the verified limitation and agree an available interface before proceeding.
