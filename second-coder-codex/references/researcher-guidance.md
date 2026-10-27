# Researcher orientation and stage guidance

Use this reference on first use, when introducing the workflow after installation, and when a stage transition needs clarification. It strengthens communication around the existing workflow; it does not replace the original Stage 1 procedure or add approval rounds.

## First introduction

Give one coherent overview before asking for materials. Cover the following in English, adapting to already supplied information. A compact table is useful; do not recite every detailed requirement in every message.

> This skill helps you use AI as an independent second coder for a meta-analysis. We will develop your coding instructions, prepare the source PDFs, review eligible estimates, obtain independent AI coding, and compare it with your human codesheet. You approve the rules and estimate lists and decide the final values. The AI does not see your completed human coding before its output is saved; because you approve the estimates first, selection is researcher-reviewed. The final adjudicated codesheet is the data input for your meta-analysis.

| Stage | What Codex does | What you provide or decide |
|---|---|---|
| 1: Develop the prompt | Review designated rules and the blank template, clarify ambiguities, draft and independently review the prompt | Provide the research question, eligibility criteria, codebook, blank template and representative papers; settle substantive rules and explicitly approve the prompt |
| 2A: Prepare PDFs | Prepare page-marked text and relevant images and check readability, keeping complete originals accessible | Identify the current batch, about five papers and corresponding supplements; supply missing/unreadable sources if needed |
| 2B: Select estimates | Check appendix availability and propose eligible estimates paper by paper | Check the original papers for eligibility and omissions; approve each paper's list and the combined master list |
| 2C: AI coding | Use fresh per-paper agents where available, record reasons, validate and merge coding | Usually no action; decide any newly discovered eligibility or rule issue before affected results are finalized |
| 3: Compare and adjudicate | Match human and AI estimates, show all current-paper discrepancies in an interactive panel in this conversation with source evidence, save confirmed choices and validate final data | Provide human-coded data only for the named paper currently being adjudicated; inspect evidence, click Human / AI / Other value / Defer, and confirm the summary |

Explain that the result is `Adjudicated_Codesheet.csv`, incorporating the researcher’s confirmed decisions and available for analysis, plus supporting records in one organized folder. After establishing the project folder, follow [startup and resumption](startup-and-resume.md) to verify readiness and the panel-to-chat path before an extended Stage 1 discussion. Codex announces and carries out the next authorized step; the researcher does not have to manage stage order or repeatedly say “continue.” Approval gates still require an explicit decision.

Include this qualitative reminder:

> For planning, allow approximately 30–60 minutes for Stage 1, potentially longer when materials are incomplete, ambiguous or inconsistent. This is practical planning guidance, not a measured completion time or a promise. The questioning also makes your eligibility criteria and variable definitions explicit. Estimate selection and final comparison can require substantial additional attention, depending on the papers, estimates, disagreements and your familiarity with the material. I will tell you exactly when I need information or a decision from you.

Use the qualified Stage 1 planning allowance above; do not promise completion within it, infer a fixed duration for later stages, or make unsupported accuracy/speed claims. Do not mechanically teach familiar research concepts or add examples to every question. Use a short example only when it helps a specific action.

## Materials and the immediate next action

After the overview, request only the current stage's inputs. Explain their purpose and suitable formats. Reuse designated accessible files. A blank template can be CSV or XLSX; preserve column order and inspect the intended sheet. Existing names need not be changed by the researcher; Codex can create standardized working copies without altering originals.

| When | Inputs to request | Purpose and suggested formats |
|---|---|---|
| Stage 1 | Research question, eligibility protocol, codebook/variable definitions, blank template, representative papers and relevant notes/supplements | Rules/notes: DOCX, PDF, Markdown or plain text; template: CSV/XLSX; papers: complete PDF. These define what to extract and how; representative examples expose ambiguities |
| Stage 2A | Designated current-batch papers and corresponding supplements | Complete PDFs for reading preparation. The approved prompt/template are already available and should be reused |
| Stage 2B | Only a specifically missing appendix/supplement or required clarification | Complete the source coverage and eligibility decision; no human codesheet or GT |
| Stage 2C | Usually no additional files | Workers use the approved materials; raise substantive scope/rule questions only as needed |
| Stage 3 | A separate human-coded file for the paper currently being adjudicated, relevant sheet/tab if needed, and any additional designated comparison evidence | CSV/XLSX containing only that paper, with all its human-coded estimates and original columns; no whole-project or multi-paper GT. Reuse source PDFs, AI files, approved rules and prior decisions |

Recommended Stage 1 closing request:

> To begin Stage 1, please provide your research question and eligibility criteria, codebook or variable definitions, blank coding template, and a few representative papers with any relevant supplements or notes. Organize your materials in a local folder and provide its full path, specifying which files I should read. You may also use the interface's drag-and-drop or attachment options. I will confirm which files I can access and identify anything missing. You do not need every document ready before we start. Please keep completed human codesheets, GT and adjudicated datasets separate until Stage 3.

If the user supplied some of these already, replace the generic list with what is actually missing. Do not read unidentified files to fill gaps without establishing their designation. During an installation-only request, explain what to prepare next; do not start inspecting research data without a start request or designated materials. If the user asked to install and begin, proceed with accessible designated inputs in the same turn.

## Guidance at transitions

When presenting the Stage 1 draft for researcher review, add one sentence: “Please check the eligibility scope, what each row represents, field definitions, calculations, and missing-value rules.” Keep this within the existing review and approval step; do not add a separate checklist approval, repeat a full review tutorial, or provide multiple reply examples by default.

Keep the pattern: completed action, next action, current researcher task (if any). At the first relevant occurrence, briefly explain what an approval means: prompt approval freezes the rules; estimate approval fixes the list for AI field coding; confirmation sends the listed adjudication decisions into the project record. No response is not approval. During technical preparation/coding, say when no researcher action is needed. These explanations belong within existing transitions, not new approval rounds. Use the exact 2A-to-2B progression in `stage2.md`; no extra confirmation to start technical preparation. Remind the researcher briefly at 2B that checking omissions and source evidence takes attention, and at Stage 3 that resolving disagreements can take time. Do not repeat the full opening table.

When pausing, name the decision and the affected work, for example: “I am waiting for your approval of this paper's revised estimate list. Once approved, I will save it and review the next paper.” For a missing supplement, identify the paper's reference, missing item and likely impact; use the source-completeness procedure in `stage2.md` rather than claiming approval is ready.

For resumed projects, begin with `PROJECT_GUIDE.md` and its linked existing records, following startup and resumption. Read saved approvals, pending items and the designated source list. State the last completed step and the specific next unresolved item. Preserve prior choices; do not restart Stage 1 or repeat the entire orientation unless requested.

At the Stage 3 handoff, follow `grouped-review.md`: generate or reuse the in-conversation panel and display it in the same chat. Explain: "Review the evidence and choose Human, AI, Other value or Defer. A group choice applies only to its listed estimates and field; you can separate an exception. View source opens the original evidence. Select Review decisions below the group list, then Confirm and send to Codex on the summary. I will receive your choices here, verify them and generate the adjudicated codesheet." For coverage, use Confirm coverage and send to Codex and explain that field review follows. If the app asks for confirmation of the follow-up message, the researcher completes that prompt.

End the turn after displaying the actual panel; the researcher interaction starts the next turn through the host. Do not require a download, file attachment, saved-location question, separate browser or "Done" message. On the marked confirmation message, validate and import the exact submission, acknowledge receipt and continue recording, checking and output work. A draft state or source-image request is not approval. If the researcher asks for evidence, show the requested actual image in chat while preserving the existing choices. If inline display or direct submission is unavailable, explain the actual capability limit and preserve the review; do not silently substitute another edition.

At the end-of-batch prompt review, give a concise handoff based on saved approvals. Name the completed batch, link the current approved prompt and state its version, and report whether any rule changes are needed. If none are needed, say that the same approved version continues without asking for approval again. If changes are needed, briefly explain the proposed change, reason and affected earlier work, and request only the substantive approval required by the existing workflow; label proposals as unapproved. Mention any recorded paper-specific exception relevant to continuation and its scope without turning it into a general rule. State the concrete next action and what, if anything, the researcher must supply. Carry out authorized work in the same turn; if waiting, name the missing input or decision and what follows. Keep this brief: do not repeat the full prompt, reopen settled choices without a specific conflict, or add an approval round.

After a batch is finalized and delivered and its prompt review is complete, return to 2A using the batch-selection branches in `stage2.md`. Announce and use an approved next batch; otherwise ask for a selection from available remaining papers or request missing sources. Do not request reuploads or repeated approval of an existing batch order. Stop when the designated project is complete or the researcher asks to pause.
