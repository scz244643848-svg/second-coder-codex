# A Second-Coder Codex Skill: Researcher-Guided Data Extraction for Meta-Analysis

Authors: Chunzhi Shi, Zhehan Zhu and W. Robert Reed. Package version: 2026.10.29. License: [MIT](LICENSE). See [release notes](RELEASE_NOTES.md), [licensing and citation](LICENSING.md) and the [Zenodo software record](https://doi.org/10.5281/zenodo.23657589).

## Introduction

This skill guides you through using AI as an independent second coder for a meta-analysis. Working entirely in Codex, it helps you develop and approve an extraction prompt, prepare the source PDFs, review eligible estimates, obtain independent AI coding, and resolve differences between the AI and human codesheets.

The first stage clarifies your coding instructions before extraction begins. Ambiguous definitions, conflicting instructions and missing rules can lead two competent coders to select different estimates or code the same estimate differently. Codex identifies these issues and incorporates your decisions into an extraction prompt. You explicitly approve that prompt before proceeding.

Next, Codex prepares the research PDFs and proposes eligible estimates for your review, paper by paper. You check each proposal against the source, look for omissions and approve the final list. Only then does Codex complete independent AI coding for the approved estimates. Finally, it compares the AI codesheet with your existing human codesheet and guides you through discrepancies using source evidence. Neither coder automatically takes precedence: you decide the final entries.

Here, independent AI coding means that the AI does not receive the completed human codesheet before its coding is saved. You first review and approve the eligible estimates that the AI will code. Estimate selection is therefore researcher-reviewed; this is not an unaided AI test of which estimates should be included.

Your involvement is essential throughout. This workflow supports research judgment and records its basis; it does not make the inclusion or adjudication decisions on your behalf. The final result is `Adjudicated_Codesheet.csv`, incorporating your confirmed decisions and ready to use as the data input for your meta-analysis, with any analysis-specific preparation you require. Supporting records show which estimates were approved, where the coding evidence came from and how differences were resolved.

## Before you start

Use this workflow for studies you have already selected for your meta-analysis and for which an independent human codesheet is available for later comparison. Decide which source version of each study belongs in your project before human coding. Supply the same designated versions for AI coding. Codex will not automatically search for a newer working paper, substitute a published version or repeat your study screening.

You supply your own research question, eligibility criteria, variable definitions and blank coding template. The skill does not prescribe a particular research topic, set of variables or statistical formula. You do not need to provide the whole paper collection at once: use representative papers for developing the rules, then designate batches of approximately five papers for extraction. A smaller batch is acceptable.

You may also provide all source papers in one folder at the start. On entering Stage 2A, Codex inventories the accessible papers and supplements, then asks which approximately five to use first unless you have already designated a batch or authorized an ordering. Providing all papers does not make them all the current batch, and you do not need to upload them again later. Keep human coding separate and provide it one paper at a time when requested in Stage 3.

For planning, allow approximately **30–60 minutes for Stage 1, potentially longer** if the materials are incomplete, ambiguous or inconsistent. This is practical planning guidance, not a formally measured completion-time estimate or a guarantee. Discussing the rules makes eligibility criteria and variable definitions explicit, including conventions that might otherwise remain unwritten.

**Estimate selection and final comparison can also require substantial researcher involvement.** Actual effort depends on the number and complexity of papers and estimates, the number of disagreements and your familiarity with the material. There is no fixed completion time or guaranteed efficiency gain.

Before an extended Stage 1 discussion, Codex checks local file access, available Python/PDF tools and the interactive panel capability. It displays a small compatibility check and asks you to send its test confirmation. This contains no research data and approves no scientific decisions. If the client cannot display the panel or send the confirmation, Codex explains the limitation before you invest further effort. See [startup and resumption](second-coder-codex/references/startup-and-resume.md).

## Choosing a model

Use a current reasoning model available in Codex that can inspect article text and table images and use the tools required by this workflow. Choose a model intended for complex, multi-step work, taking account of your budget and acceptable processing time.

Before starting, ask Codex to consult current official model guidance, recommend a model and reasoning setting, and explain the tradeoffs. Select the settings in Codex before proceeding.

## Install the skill and receive the introduction

A skill is a folder containing `SKILL.md` and its supporting files. If you received a ZIP, you can give Codex its accessible local path and ask it to extract and install the skill, or extract it yourself first. Install the complete `second-coder-codex` folder, including `references`, `scripts` and `assets`. The main package README is a user guide; the installable folder is the one containing `SKILL.md`.

The simplest method is to send Codex this instruction, replacing the bracketed text:

> Please read the second-coder-codex package at [full ZIP or extracted package path] and install the complete second-coder-codex skill folder in the supported personal skill location for this environment. Preserve any existing installation before updating it, resolve any ambiguous naming conflict with me, and verify what was installed and how I can invoke it. After installation, read the skill's researcher-guidance instructions and explain its purpose, each stage, what I need to provide and decide, and which parts may require substantial time. Then tell me what to prepare for Stage 1.

If file-access permission is needed, Codex should explain the required access. Research papers are not needed merely to install the skill. Successful file copying alone does not run the research workflow; the instruction above also requests the introduction.

For manual installation, current official guidance lists the personal local-skills location as `~/.agents/skills` (`%USERPROFILE%\.agents\skills` on Windows). Copy the complete folder so that `second-coder-codex/SKILL.md` is inside it. Ask Codex to verify the applicable location and discovery in your environment, especially if you already use another configured skills directory. Skills can be invoked explicitly; if an installed skill is not visible, have Codex check discovery and restart if needed. See the [official local-skill guidance](https://learn.chatgpt.com/docs/build-skills).

This is one integrated skill. The preserved Stage 1 and Stage 3 instruction files in `references` are supporting material, not additional skills that you need to install separately. Keep any backup outside active skill directories so Codex does not discover multiple copies with the same name.

## Start a project

Once installed, you can say:

> Use $second-coder-codex. I want to start using this skill for my meta-analysis. Please introduce the workflow and guide me through the materials needed for Stage 1.

If the interface uses a different skill selector, select `second-coder-codex` or name the skill in your request. If installation cannot yet be discovered, ask Codex to read and follow the extracted skill's full `SKILL.md` path as a fallback.

At first use, Codex should explain the whole workflow and your role, establish the project folder, prompt you to choose or confirm the model and reasoning setting, and check compatibility before requesting the remaining materials. If it has just given that introduction after installation, it should continue with the remaining startup steps instead of repeating it. Codex can consult current official guidance and recommend settings; you select and confirm them in Codex. It records your confirmed choice for the project and reuses it on resumption unless the settings have changed. At later transitions it explains only the current task, your next action and what follows. You do not need to repeatedly say “continue.”

## Prepare and provide materials

Organize your materials in a local folder and provide its full path, specifying which files Codex should read. You may also use the interface's drag-and-drop or attachment options. Codex will confirm which files it can access and identify anything missing. If relevant files have already been provided, it should reuse them rather than ask for another upload.

| Material | Purpose | Suggested format | When to provide it |
|---|---|---|---|
| Research question and eligibility protocol | Define the population, exposure/outcome, comparisons and eligible estimates | DOCX, PDF, Markdown or plain text | Stage 1 |
| Codebook, variable definitions and coding notes | Explain the meaning, permitted values and conventions for each field | DOCX, PDF, Markdown or plain text | Stage 1 |
| Blank coding template | Define output columns and order | CSV or XLSX; identify the worksheet if needed | Stage 1 |
| Representative papers and relevant supplements | Help clarify difficult cases while developing rules | Complete PDFs | Stage 1 |
| Current-batch papers and corresponding appendices/supplements | Supply evidence for estimate selection and AI coding | Complete PDFs; identify which supplement belongs to which paper | Stage 2A |
| Independently completed human coding for the current paper only | Provide the comparison input after AI coding is saved | Separate CSV or XLSX with all human-coded rows for that paper and the original coding columns | Stage 3, when that paper is requested |
| Existing adjudication records or approved lookup evidence, if applicable | Resume decisions and preserve their evidence | Existing readable files; identify their purpose | When resuming or at Stage 3 |

Materials do not need to be complete before you begin. Codex can inspect the designated accessible materials, identify gaps and clarify missing rules through conversation. A missing item that affects a specific decision must still be resolved or explicitly recorded before that affected work can be finalized.

Keep the blank template distinct from completed coding. **Do not provide human codesheets, GT or adjudicated datasets as evidence for Stage 1 or independent AI extraction.** If these files are already in the project folder, identify them as reserved for Stage 3; Codex must not read them early or pass them to coding agents. You can keep them in a separate folder to make this clear.

Existing filenames are acceptable. Tell Codex which file serves each role; it can create standardized working copies while preserving originals. If an XLSX has several worksheets, identify the intended sheet or let Codex clarify it before use. The working names used by the workflow are `Template_Codesheet.csv`, `AI_Codesheet.csv`, `Human_Codesheet.csv` and `Adjudicated_Codesheet.csv`; use batch folders to distinguish batches.

A sufficient starting message is:

> My project folder is [full path]. For Stage 1, read [protocol filename], [codebook filename], [blank template filename] and [representative paper filenames]. The human coding file is reserved for Stage 3. Please identify any materials or coding rules still needed.

## Workflow at a glance

| Stage | Codex's work | Your contribution | Result |
|---|---|---|---|
| 1: Develop the extraction prompt | Inspect rules, clarify ambiguities, draft and independently review the prompt | Supply definitions/materials, decide substantive rules and approve the prompt | Approved prompt, compatible blank template and rule-decision record |
| 2A: Prepare PDFs | Extract page-marked text, render relevant pages and check readability | Designate the batch and provide missing/unreadable sources if needed | Reading aids alongside complete original PDFs |
| 2B: Select eligible estimates | Check referenced supplements and propose estimates paper by paper | Check source evidence and omissions, approve each paper and the master list | Saved master approved estimate list |
| 2C: Independent AI coding | Assign per-paper workers, record evidence, check completeness and merge results | Resolve any newly found scope or rule issue; otherwise wait for the output | AI codesheet with `AI_reason`, mappings and pending issues |
| 3: Compare and adjudicate | Match estimates, present evidence for discrepancies, save decisions and validate final data | Provide human coding for the named current paper only, decide final values and authorize finalization | Adjudicated codesheet and supporting records in one organized folder |

## Stage 1: Develop and approve the extraction prompt

Codex reads only your designated sources. It asks focused questions about unclear eligibility rules, variable meanings, allowed values, calculations, evidence locations and missing versus zero values. Discuss one substantive decision at a time. You choose the research conventions; Codex records them so settled choices do not have to be repeatedly approved. The approved prompt makes the eligibility criteria and variable definitions transparent and preserves the decisions needed to interpret or reuse the coding instructions.

The extraction prompt must cover every template field and the approved estimate-selection process. Codex checks that the instructions and template agree. The AI export also includes the workflow's `AI_reason` audit column; this convention is explained in the output contract. Other changes to your template require agreement.

A fresh independent agent audits the draft when available. Codex corrects drafting mistakes and brings substantive proposed rule changes back to you. If an independent agent is unavailable, it must disclose that limitation. You are offered a review of the draft and an optional manual review by another LLM. If you choose an external review, supply the draft, relevant rules and blank template, then bring the reviewer's feedback back to Codex. Review suggestions do not automatically change or approve your rules.

Explicitly approve the completed prompt when satisfied. Skipping another review round is not itself approval. Codex saves the approved prompt, compatible template and decisions with their approval record. If you already have an approved project prompt, identify it and request its reuse; Codex should not silently substitute an unrelated or earlier prompt.

When presenting the draft, Codex gives a one-sentence reminder to check the eligibility scope, what each row represents, field definitions, calculations, and missing-value rules. This is part of the existing review, with no additional approval step.

## Stage 2A: Prepare the current batch

After prompt approval, designate approximately five papers and their relevant supplements if you have not already done so. Codex announces that it is beginning Stage 2A and that Stage 2B will follow. It does not ask whether to enable preparation.

Codex first organizes the files already provided for the batch and matches their supplements. It asks only about missing files or uncertain paper-supplement associations or batch membership; you do not need to refill an inventory or rename files. Representative papers used in Stage 1 can be reused when included in your batch designation.

Codex prepares full text marked with physical PDF page numbers, relevant page images and a conversion-quality report. Complete original PDFs remain accessible to both estimate selection and coding; extracted materials are reading aids. Codex checks suspected empty or garbled pages and can render further pages when formulas, notes or continued tables need inspection. Detected table pages do not define the full search scope.

The PDF helpers require Python 3.10+ and PyMuPDF. Codex checks available runtimes and handles routine project-local setup where permitted, explaining any action that needs your involvement. If a source cannot be prepared reliably, it identifies the problem and remedy rather than silently treating that paper as complete. Once the required material is readable, it announces and starts Stage 2B.

## Stage 2B: Review and approve eligible estimates

Codex reads each paper and its supplied supplements under the approved rules. Before requesting that paper's approval, it checks whether appendices or online supplements referenced in the text are actually available and correspond to the designated paper. If something relevant is missing, it points to the reference, identifies the missing item and explains its possible effect on eligible estimates or coding. Supply or identify that material so the affected review can continue. An unavailable supplement is not evidence that a result was never reported.

The proposed list identifies individual estimates with page, table/panel, row/column, specification and other distinguishing information. Where applicable, Codex groups entries by the paper's tables/panels, showing group counts and precise locations; estimates elsewhere are grouped by source section. It separates clear proposals from items needing your judgment and reports their counts separately. For the first paper, it briefly explains how the rows differ under your approved coding rules and prompts you to check omissions, duplicates and ineligible entries. It does not yet complete the codesheet or repeat this explanation for every paper.

Keep the source papers open while reviewing. Check that proposed estimates meet your criteria, remove ineligible entries and look for estimates that may have been overlooked. This can take substantial attention. Approve the list only when satisfied with its scope. If a potentially relevant appendix remains unavailable, the list cannot be presented as complete-paper screening. You may explicitly decide to defer the paper or proceed with a recorded limited-source scope; Codex must carry that limitation into later records.

For example:

> Approve the listed estimates except [identifier], which does not meet [criterion]. Also check [table, row and column] for a possible missing estimate. Show me the revised list before I approve it.

Codex records the revisions, obtains your explicit approval of the resulting list and moves to the next paper. Papers with zero approved estimates are also recorded. After all paper-level reviews, it combines the saved decisions into a master list with per-paper and total counts. Check that all approved entries are included, rejected/deferred entries are not silently included, and no estimate is duplicated. Confirm this assembled master list; Codex then begins coding automatically.

## Stage 2C: Obtain independent AI coding

Codex supplies each fresh per-paper worker with the approved prompt, blank template, approved estimate list, complete PDFs/supplements and reading aids. It schedules workers according to available capacity. Workers do not receive human coding, GT, prior adjudicated values or one another's coding results.

Each worker codes the approved estimates, connects relevant evidence across tables and text, and records important sources, calculations and uncertainty in the final `AI_reason` column. Codex checks one-to-one correspondence with the approved list, column structure, applicable coding rules and verifiable calculations, then merges the per-paper files. A row-count match alone is not sufficient.

Usually you need not act during coding. If a new eligibility issue or missing rule appears, Codex identifies exactly what needs your decision before finalizing affected results. Field uncertainties follow the approved missing-value convention and are carried forward for review. When AI coding is saved, Codex reports counts and pending issues, links the output, names the first paper for Stage 3 and asks for human coding for that paper only.

## Stage 3: Compare and decide the final values

Codex names the paper currently being adjudicated. Provide a separate CSV or Excel file containing only that paper's independently completed human coding, including all estimates you coded for it and the original coding columns. Do not limit the file to estimates on the AI-approved list; differences in coverage are part of the comparison. Do not provide the whole-project or multi-paper human codesheet, including data for later batches. If your human coding is stored in a master workbook, export a current-paper-only file before supplying it. If you need help, tell Codex the software you use and how papers are identified. It will guide you through filtering to the named paper, copying the header and all its rows into a new file, and checking that other papers are absent, while keeping the master workbook unread. Keep estimates absent from the AI-approved list; they are needed to check coverage. This keeps later papers' human answers out of the extraction workflow. Identify the worksheet if needed. Existing AI outputs, source files and rules are reused; you should not have to upload them again unless access is missing.

Codex first matches estimates by their source and specification and resolves missing, additional or ambiguously matched rows. It then compares the template fields. For substantive disagreements it shows the human value, AI value, original-source screenshot, precise locator, relevant approved rule and a recommendation. If images cannot be produced or displayed, it explains the limitation and gives an accurate source locator and short excerpt or labeled transcription. Calculated values include the relevant inputs and method.

After resolving coverage, Codex displays an interactive review panel directly in this conversation. All substantive discrepancies for the current paper appear together. Repeated discrepancies share one group only when the same field, alternatives, evidence and decision apply. Each group shows its scope and affected estimates. Expand the member list to separate an individual exception.

Choose **Use Human**, **Use AI**, **Other value** or **Defer**. Other value accepts a correction or an approved category; Defer leaves the item unresolved. Neither coder automatically takes precedence, and recommendations are not preselected. Verified equivalent wording and approved rounding equivalence are recorded as agreement, using the original comparison rules.

Select **View source** for a group to inspect the original screenshot, precise location, what to check, approved rule and recommendation. You can enlarge the image or view the full page. **Back to all groups** returns to the complete list without changing your choices. For a large review, some original images may be opened in this same chat through **Open this source image in chat**; the issue list and decisions stay together. This is an evidence request, not a confirmation.

When ready, select **Review decisions**, check the summary and click **Confirm and send to Codex**. Complete the app's confirmation if it appears. The selected decisions are sent into the same conversation, so you do not need to download, move or attach a file, or type a completion message. For coverage decisions, the button is **Confirm coverage and send to Codex**; Codex then prepares field review.

Codex validates the received submission against the saved review, records the choices for the exact estimates and fields, recalculates approved dependent values and runs the existing final checks before generating `Adjudicated_Codesheet.csv`. It confirms receipt in chat after validation. A panel status saying that submission was requested is not yet a receipt. If submission is cancelled or fails, the choices remain available and can be sent again. Deferred or unselected items block confirmation. The summary remains the existing consolidated review, not an additional approval round.

This edition requires a Codex client that supports in-conversation visualizations and their follow-up message action. It uses that host capability rather than a localhost server or a separately opened browser file. The skill cannot add the capability to a client that lacks it; Codex should identify that limitation and preserve the review for an agreed alternative. Generation and validation use the available Python runtime from PDF preparation, with no additional Python library for the panel helper.

Draft choices are retained in the panel and, where supported, in the host's widget state. That draft storage is best effort, not the project decision record. Keep the panel available until confirmation; a persistence problem is reported there. To return to it, scroll to the panel in this chat or ask Codex to show the saved review again. Imported confirmations are saved in the project. **Edit decisions** lets you amend choices; review and send the new confirmation before Codex applies it. Previous confirmations and outputs remain preserved.

After one paper's adjudication, Codex saves its decisions, names the next paper and requests that paper's human-coded file only. A file already supplied for that paper is reused. Once the batch's papers are adjudicated, their results are combined into the batch's final codesheet using the existing finalization process.

**The final comparison and adjudication may take substantial researcher time**, particularly when there are many estimates, unclear definitions or disagreements. Codex should state the exact decision it is waiting for rather than ask you to drive the workflow. It also checks important shared values against sources because agreement between coders does not prove correctness.

The decision summary provides the consolidated final review. You can review and confirm it or explicitly authorize finalization without another review round; numerical and structural validation still takes place. Accepted missing values and evidence limitations are recorded. Remaining unresolved decisions must not be silently described as finalized data.

## Final deliverables and where they are saved

Codex identifies the working project/batch location from your designated folder and tells you the actual saved paths. It preserves original inputs and stores generated work separately. After finalization it assembles one `Project_Outputs` folder in the agreed project location, using an unused destination if that name already exists. It provides a link/path to the folder and a direct link to the final codesheet. **Research output is delivered as a folder, not a ZIP.** The ZIP used to distribute this reusable skill is separate from project results.

| Folder | Contents |
|---|---|
| `01_Final_Data` | Final `Adjudicated_Codesheet.csv`, following your data template |
| `02_Protocol_and_Template` | Approved prompts, templates and coding-rule decisions |
| `03_Approved_Estimates` | Approved per-paper and master estimate lists |
| `04_AI_Coding` | Independent per-paper and master AI codesheets, including `AI_reason` |
| `05_Adjudication` | Human inputs, comparisons, decisions, mappings and issue records |
| `06_Source_Evidence` | Source screenshots, excerpts and calculation/lookup evidence |
| `07_PDF_Reading_Aids` | Prepared text, page images and conversion reports |
| `08_Validation_and_Run_Records` | Validation results, provenance and saved run state |
| `09_Superseded` | Clearly labeled drafts and replaced outputs |

Use batch and paper subfolders within these categories. The root README points to the data to use, `File_Index.csv` lists artifacts, and `SHA256SUMS.txt` supports integrity checking. Evidence links are relative to the delivered folder. Codex inventories the auxiliary outputs, verifies copies and organizes them automatically; you do not need to classify the files yourself.

## Continue, resume or process another batch

Codex maintains `PROJECT_GUIDE.md` in the project folder. It links to the existing progress record, approved prompt/template versions, decisions, current batch and saved review sessions, and identifies the next action. It is a navigation guide; the linked approval and decision records remain authoritative.

If the conversation stops, you can paste:

> Resume my second-coder project at [full project-folder path]. Read PROJECT_GUIDE.md and its linked progress, approval and decision records. Tell me the last completed step and the next action, preserve my previous decisions, and continue the authorized work.

Codex should reuse existing outputs and request only a missing input or unresolved decision. Confirmed submissions are saved in the project; panel choices that have not been submitted are only best-effort drafts and may need to be selected again. If an older project lacks `PROJECT_GUIDE.md`, Codex first locates its existing state without reading reserved human codesheets, verifies what can be established, then creates the guide without inventing approvals.

After each batch, Codex assesses whether mistakes reveal a defect in the coding rules. Ordinary transcription or calculation errors are corrected in the data; substantive rule changes require your explicit approval. Codex saves the revised prompt and identifies any earlier estimates or fields affected. The next batch uses the latest approved prompt. The skill does not require an automatic full-corpus second extraction.

At the handoff, Codex briefly identifies the completed batch, links the current approved prompt and states its version, explains any proposed changes or relevant paper-specific exceptions, and tells you the next action. An unchanged prompt does not need approval again. Codex proceeds with authorized work or identifies the exact input or decision it needs from you.

After finalizing and delivering a batch and completing that prompt review, Codex returns to Stage 2A for the next batch:

- If you have approved a batch plan or ordering, it names the next papers and begins preparation without asking you to select them again.
- If the remaining papers are already available but the next batch is not specified, it shows the remaining paper list and asks which approximately five to process. You may authorize an order for future batches at this point.
- If the next batch's papers or supplements are missing, it requests only those sources. Previously supplied files are reused.

Codex maintains completed, pending and deferred paper statuses in the existing progress record. Completed papers are not routinely selected again; deferred papers remain visible. The final batch may contain fewer than five papers. Each batch follows 2A -> 2B -> 2C -> Stage 3 using the approved prompt, without restarting Stage 1. When all designated papers are complete, Codex reports completion instead of asking for another batch. You may pause or stop the workflow at any time.

If Codex is waiting, it should state whether it needs a batch selection, particular source, clarification, estimate-list approval or adjudication decision, and explain what happens once you respond.

## Authors, maintenance and citation

- **Chunzhi Shi** (maintainer): Department of Economics and Finance, University of Canterbury, Christchurch, New Zealand; UCMeta, University of Canterbury, Christchurch, New Zealand. [ORCID: 0009-0003-0596-5119](https://orcid.org/0009-0003-0596-5119).
- **Zhehan Zhu**: School of Public Administration, Zhongnan University of Economics and Law, Wuhan, China. [ORCID: 0009-0007-5978-9375](https://orcid.org/0009-0007-5978-9375).
- **W. Robert Reed**: Department of Economics and Finance, University of Canterbury, Christchurch, New Zealand; UCMeta, University of Canterbury, Christchurch, New Zealand. [ORCID: 0000-0002-6459-8174](https://orcid.org/0000-0002-6459-8174).

If you use this workflow in research, please cite the version you used:

Shi, C., Zhu, Z., & Reed, W. R. (2026). *A Second-Coder Codex Skill: Researcher-Guided Data Extraction for Meta-Analysis* (Version 2026.10.29) [Computer software]. Zenodo. https://doi.org/10.5281/zenodo.23657589

Package version 2026.10.29 is a documentation and startup-guidance update to the existing Zenodo record, retaining DOI 10.5281/zenodo.23657589. No new Zenodo version or DOI is created for this update. Include the package version when citing the software. The earlier package is preserved in the [GitHub release v2026.10.26](https://github.com/scz244643848-svg/second-coder-codex/releases/tag/v2026.10.26). The [all-versions Zenodo DOI](https://doi.org/10.5281/zenodo.23657588) also remains unchanged.

Machine-readable citation metadata is provided in [CITATION.cff](CITATION.cff). The citation request does not alter the [MIT license](LICENSE).

The skill’s accuracy and time requirements have not been formally evaluated.
