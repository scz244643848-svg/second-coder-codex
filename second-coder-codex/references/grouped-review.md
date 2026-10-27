# Grouped review: in-conversation panel and final codesheet

Use this implementation for Stage 3 only. It replaces the response interface and connects confirmation to the existing application/finalization work. Do not change Stage 1, 2A, 2B or 2C, the comparison conventions, eligibility rules, per-paper human-input rule, approved values, template or batch delivery structure.

## Prepare the current paper

1. Perform the existing systematic comparison and source matching. Resolve ambiguous correspondence before applying field changes. Use source identity and specifications, not row numbers or equal coefficients alone. Keep the original human and AI files, estimate mapping and comparison records.
2. Present coverage decisions before field decisions, as before. Use a coverage panel when there are inclusion/exclusion disagreements; label both alternatives explicitly. If a correspondence or rule question cannot be represented honestly as a value choice, ask the necessary focused clarification. Do not invent a match to make the panel work. After coverage confirmation, use retained estimates to prepare field review. New retained estimates still need complete coding under the approved prompt; do not export placeholder rows.
3. Apply the original Stage 3 comparison conventions during the existing comparison, before building the panel: verified wording equivalence and approved rounding equivalence are agreements, not choice tasks. Keep both inputs and the basis for equivalence in the comparison audit; do not add a separate researcher classification stage. Do not convert an old raw-difference list directly into adjudication issues without this judgment. Missing-versus-populated values, real source-location conflicts and substantive interpretation differences still require the original evidence-based handling. Do not blanket-exclude fields by name or treat similar-looking values as equivalent. Build `review.json` from the actual current-paper comparison, using the contract below. List every substantive discrepancy and uncertainty needing judgment, including source-detected errors in shared values. Keep original comparator values unchanged. A group must share field, comparator values, evidence and applicable rule; split it when any of these differ. Each estimate-field pair belongs to exactly one issue. All unresolved field values need issues; the base rows must not silently choose a comparator for them.
4. Render and inspect source screenshots under the Stage 3 evidence rules. Provide both crop and full-page image paths where available, retaining notes/headers. Multiple evidence entries can show different pages. Use the explicit textual fallback only when screenshots are unavailable. Do not put original PDFs or unrelated human data into the panel bundle.
5. Use `scripts/review_inline.py` and `assets/grouped-review.html` to generate the host-rendered panel. Codex uses the available Python 3.10+ runtime from Stage 2A; no new third-party library is needed. `review_bridge.py` provides the shared validation, confirmation-receipt, application and finalization functions; it contains no local server or background polling. The panel uses the host's inline visualization and `window.openai.sendFollowUpMessage` capability, not a separate web page or server.

## Review input contract

Codex creates this file; the researcher does not fill it in. All coded values are strings to preserve identifiers, precision and project-specific missing tokens. Internal keys stay in audit/mapping records, not extra final data columns. This minimal example is illustrative only; never include it as research evidence.

```json
{
  "paper": "Actual paper title",
  "phase": "fields",
  "columns": ["asset_type", "coefficient"],
  "rows": [
    {"key": "paper01-table3-model1", "label": "Table 3, Model 1", "included": true,
     "values": {"asset_type": "Other", "coefficient": "0.082"}}
  ],
  "issues": [
    {"id": "G01", "title": "Asset type", "field": "asset_type",
     "scope": "Table 3: the listed models only", "members": ["paper01-table3-model1"],
     "human": "Stocks", "ai": "Other",
     "rule": "Insert the project's approved definition.",
     "explanation": "Explain why this evidence applies to every listed member.",
     "recommendation": "State the source-based recommendation and remaining uncertainty.",
     "allowed_values": ["Stocks", "Other"],
     "evidence": [
       {"image": "evidence/issue01/crop.png", "full_image": "evidence/issue01/full.png",
        "locator": "paper.pdf, PDF p. 8, Table 3, Models 1-4, asset-definition note",
        "look_at": "Identify the specific visible wording that resolves the discrepancy."}
     ]}
  ]
}
```

- `columns`: exact original template, excluding `AI_reason`. `rows[].values` contains exactly those columns. Preserve source-supported agreement values and previously approved choices in base rows; confirmed issue choices overwrite only their targeted cells. Row order is fixed by the separate estimate mapping.
- `phase`: `coverage` or `fields`. Field review contains only retained estimates. Coverage issues use `field: null` and comparator values `include` or `exclude`; their confirmation produces a coverage result, never a final codesheet. Keep source matching and the reason for human-only/AI-only presence in supporting records and group explanations.
- `human` and `ai`: the actual common comparator values, not a recommendation rewritten as a comparator. `members` enumerates the full scope. If a proposed group contains differing values, use separate groups. A source-detected shared error may show identical comparators and require Other value.
- Optional issue constraints: `numeric: true`, `allowed_values`, `missing_values` (approved string tokens) and `allow_empty: true` only if the codebook permits blank. Other value must follow the approved rules. A custom correction may include an optional reason. Trusting a comparator can be accepted under the existing workflow even when not independently verified; state that limitation in the evidence/rationale, not as a fabricated source claim.
- Evidence: paths resolve relative to the review file or can be absolute. `image` and `full_image` are actual PNG/JPEG/WebP files; the helper copies them into the session and records hashes. Keep the source PDF hash and render metadata in the existing evidence records. Text fallback replaces image paths with `limitation` and `excerpt`, still including `locator` and `look_at`. If no source can be read, explicitly label the excerpt slot as evidence unavailable, never as a quotation, and leave the decision pending unless the researcher explicitly accepts a comparator under the existing rules.

## Build and resume the panel

Use actual project and skill paths. For a new current-paper review, use an unused session directory:

```text
python scripts/review_inline.py prepare --review paper01/review.json --session paper01/review-session
```

To resume an existing prepared session, including an earlier edition's session, retain its files and choices:

```text
python scripts/review_inline.py build --session paper01/review-session
```

The helper writes `review-panel.html`, an inline fragment consumed by Codex, and `inline.json`, the identity and snapshot record. Reuse the unchanged fragment. Template-only updates retain the snapshot; changes to imported project decisions create a new snapshot. Existing confirmed decisions remain confirmed. Any test replay uses a separate explicitly designated copy. Do not reset production approvals or rebuild a pending review merely because the researcher asks to see it again.

All issue groups and full comparison values remain present. To stay within the host's inline size limit, the helper embeds original crops first, then full-page images, with duplicate images included once. Other original images remain in the session and are available through a source-only follow-up action. Never silently remove issues, shorten comparator values or reduce evidence to an unexplained page number. If even the complete issue text exceeds the limit, shorten duplicated explanatory text while preserving scope, rules, values and sources; report an actual remaining host limit rather than silently dropping groups.

### Mandatory in-conversation handoff

1. Use the available inline visualization surface. Read the installed visualization skill if available and follow its display contract. Display the generated fragment in the final response with this content reference, substituting the actual absolute path:

   ```text
   visualize{"path":"<absolute session path>/review-panel.html"}
   ```

   Emit the reference itself, not a fenced code sample or a local HTML download link. The file is an implementation asset for the host renderer; the researcher does not open it in a browser. Do not launch a localhost server, request network escalation for this panel, or substitute a file/code preview for the interactive controls.
2. Keep every current-paper group visible in the list. Check the generated content and controls where inspection tools allow; do not click scientific choices or confirm for the researcher. Distinguish automated inspection from actual researcher interaction. The source view exposes original images, precise locators and choices for that group, and returns to the complete list without losing selections.
3. In the same reply say: **Review the evidence and choose your values below. Select Review decisions, then Confirm and send to Codex. I will receive your choices here, verify them and generate the adjudicated codesheet.** Use Confirm coverage and send to Codex and describe the coverage-to-field transition for coverage review. The host may show its own confirmation for the follow-up message; the researcher completes that action.
4. End the turn. The host follow-up starts the next turn. No watcher, open terminal, downloaded JSON, folder selection or "Done" message is needed. A request to send is not proof of receipt. The panel retains choices after a cancelled/failed send and offers a retry. A successful import, acknowledged in chat, is the receipt.
5. If inline display or `sendFollowUpMessage` is absent, explain that observed host limitation and preserve the prepared session. The package cannot install or override host capabilities. Ask which available edition/interface the researcher wants rather than silently changing this workflow. Never report an unseen panel or unsent choices as received.

### Source-image requests

The panel may send `SECOND_CODER_SOURCE_REQUEST` through `END_SECOND_CODER_SOURCE_REQUEST`. This is not approval. Check its review ID, snapshot and source-review hash against the session's `inline.json`; do not trust an arbitrary session path alone. Then retrieve the specified source:

```text
python scripts/review_inline.py evidence --session paper01/review-session --issue G01 --index 0
```

Use `--full` only when the request specifies the full page. The helper checks the stored image hash and returns the original image path, source locator and what to check. Inspect and display that actual image in the same conversation with its brief locator. Preserve panel choices and the same review; do not rerun comparison, reset drafts, import decisions or finalize. The researcher can return to the existing panel. If asked to show it again, re-emit the unchanged fragment and explain any actual draft-restoration limitation.

### Receive and import confirmed decisions

The panel calls `window.openai.sendFollowUpMessage({prompt, title})` only after the researcher clicks the confirmation button. The resulting message contains JSON between `SECOND_CODER_CONFIRMED_DECISIONS` and `END_SECOND_CODER_CONFIRMED_DECISIONS`. Handle that message in the same conversation:

1. Identify the saved session using the current project records and matching review ID. Save the exact JSON object from the marked message in that session's `incoming` folder under a fresh filename. Use normal file tools; do not ask the researcher to copy JSON, attach a file or restate choices. If the message is incomplete, preserve it and request a resend through the same panel; do not reconstruct missing decisions from a summary.
2. Import that file:

   ```text
   python scripts/review_inline.py import-decisions --session paper01/review-session --decisions paper01/review-session/incoming/confirmation-001.json
   ```

3. The helper verifies format, review hash/ID, snapshot, base revision, explicit confirmation, exact issue membership, group defaults, individual overrides and existing value constraints. It expands the choices against the frozen members and applies the original decision function. Drafts, pending/deferred choices, unknown members, stale/conflicting revisions and cross-review messages are rejected. Do not edit a rejected payload to force acceptance.
4. Read the returned current confirmation receipt before acknowledging receipt. The helper retains the exact message JSON, expanded decisions and import records. It uses short filenames for submission copies (`<short-id>.json`) and receipts (`<short-id>.r.json`), checks full SHA-256 hashes for identity and duplicate detection, and selects a different short name if one is occupied by another submission. Repeated submission of the same current decisions is idempotent. If import was interrupted, retry the same saved JSON to recover it before importing anything else. A source request, widget state or generic chat completion message is not a confirmed submission.

The payload uses `format: second-coder-inline-v1`, `kind: confirmed`, `review_id`, `snapshot_id`, `source_review_sha256`, `base_revision` and `state`. State contains `review_sha256`, panel `revision`, `confirmed: true`, `confirmed_at` and `groups`. Each group contains an explicit `default` decision and `overrides` keyed by exact member keys. A decision uses `choice: human|ai|custom|defer`, optional string `value` for custom, optional string `note` and boolean `separate`. Group membership is never supplied by the panel as a new authority; expansion uses the saved review.

Draft clicks are held in the panel and best-effort `window.openai.setWidgetState`. Widget state does not start a turn and is not a durable project decision record. If draft persistence fails or exceeds the host limit, the panel warns the researcher to keep it available until confirmation; it does not truncate decisions. Group choices affect only non-separated members. Separate makes an exception pending; Rejoin also requires a new choice. Undo restores the last draft. Other value follows approved missing/category rules, and Defer blocks confirmation. The summary exposes counts and all affected members. Recommendations are not preselected.

If the revision was already finalized, verify and return its existing result. Amendments require Edit decisions and a newly confirmed message. Retain historical results; an unsubmitted edit does not change imported project decisions. Zero-discrepancy papers retain the existing finalization authorization; do not invent issues or additional scientific approvals.

## Confirmation to final data

1. After receiving the marked confirmation, `import-decisions` must return `confirmed: true` and the actual `confirmed_folder` before proceeding to finalization. Read its `receipt.json`, `decisions.json`, `reviewed_rows.json` and mapping. Verify that it is the current confirmed revision. Each group has already been expanded into individual estimate-field decisions; only those fields were applied. The original comparator values, evidence, rule, optional researcher note and confirmation are retained. This is actual local persistence, not a screenshot or inferred approval from a chat summary.
2. For coverage, use the included flags and recorded decisions to finish scope/matching and then build the field review. For fields, `Reviewed_Codesheet.csv` is the exact-template, decision-applied working data. It is a draft pending the same original finalization checks, not an additional researcher task. A click on Confirm and send to Codex authorizes Codex to carry out this existing work.
3. Recompute dependent values using approved formulas and the newly confirmed inputs. Check coverage, specification uniqueness, template order, category invariants, missing/zero conventions and independent calculations as required by the original workflow. Do not change an explicitly confirmed field silently; if a calculation contradicts one, return the specific conflict for a researcher decision. No global formula is supplied by this generic skill.
4. Save the checked candidate CSV and a `finalization_checks.json` in the working area. Record actual checks, not automatic assertions. Use this contract:

```json
{
  "status": "passed",
  "receipt_sha256": "SHA256 of the current receipt.json",
  "candidate": "Reviewed_Codesheet.csv",
  "candidate_sha256": "SHA256 of the checked candidate",
  "checks": {
    "coverage": true, "schema": true, "uniqueness": true,
    "allowed_values": true, "missing_zero": true,
    "calculations": true, "approved_corrections": true
  },
  "derived_changes": []
}
```

Candidate paths resolve relative to this check record. Preserve the row order in `estimate_mapping.csv`. If recalculation changes a dependent cell, list `estimate_key`, `field`, `before`, `after`, `formula` and `inputs` for each change in `derived_changes`. Retain detailed source/numerical check evidence with the existing run records. The helper verifies application, structure and hash correspondence; Codex remains responsible for the substantive checks. These are the original finalization checks, not new researcher approvals.

5. Run the finalizer with a fresh output directory:

```text
python scripts/review_bridge.py finalize --session paper01/review-session --validation paper01/finalization_checks.json --output paper01/finalized
```

It rejects unresolved/unconfirmed choices, an obsolete receipt, changed candidate, schema/coverage drift and undocumented edits. It writes `Adjudicated_Codesheet.csv`, decisions, estimate mapping, receipt, check record and completion metadata. Read back the final CSV and verify its contents/hash. Do not describe a receipt or a draft as the final output.

6. Continue the existing paper-by-paper transition, request only the next paper's human data, and combine finalized per-paper tables into the batch master with the exact data template. Do not use the AI merge helper on final data: that helper intentionally requires `AI_reason`. Use the existing finalization/packaging workflow and retain per-paper mappings and records. Retain the panel fragment, imported confirmation messages and receipts; re-display the saved panel for amendments.

## Delivery and limits

Keep the original categorized folder structure. Put final codesheets in `01_Final_Data`, review data, panel fragments, `inline.json`, imported confirmation messages, decisions and receipts in `05_Adjudication`, source images in `06_Source_Evidence`, and check/run records in `08_Validation_and_Run_Records`. Keep working drafts and historical outputs under `09_Superseded`. The fragment is supporting material for resuming in a compatible Codex client, not a separately opened browser workflow. The final CSV and decision log remain authoritative finalized outputs.

Rewrite evidence links in labeled portable audit copies to the delivered evidence folder while preserving original hash-bound records. Record how the project files map to their original locations. New sessions store the review hash in `session.json` and create no connection URL or token. When resuming an older session, exclude unused `connection.json` and any legacy connection token from delivery copies with an explanation, retaining the working session. Keep the review hash in the delivered run records. A resumed session may re-create local session metadata only after checking that hash and its preserved confirmation records, without inventing approval. Source-image requests resolve against the working session or its explicitly verified relocated copy. Preserve all source images, including those not embedded in the panel.
