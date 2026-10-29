# Stage 1: Develop and approve an extraction prompt

Stage 1 turns your research materials into clear, consistent extraction instructions. Codex explores ambiguities with you, drafts a prompt, arranges independent review, and helps you approve the final version. It does not operate NotebookLM or create completed study codesheets.

## Install and start

**Install `second-coder-codex` before starting**, following the main package README. The skill folder is `second-coder-codex`. Use a Codex environment that passes the package’s startup compatibility check. This package does not establish comparative model performance or prescribe a particular model setting.

In a new Codex chat, paste:

> Use $second-coder-codex. Welcome me and guide me from the beginning, including setting up a folder for my extraction-prompt materials. Please ask me what files to read and then help resolve ambiguities one question at a time.

If Codex cannot discover the installed skill, ask it to verify installation. As a fallback, ask it to read and follow the full path to the extracted `second-coder-codex/SKILL.md`.

## Prepare the materials folder

Create a folder containing relevant codebooks, a blank `Template_Codesheet.csv`, the research question and eligibility protocol, representative papers, and existing coding notes. Tell Codex the folder address and exactly which files to read. Incomplete materials are acceptable; Codex will identify gaps. Keep completed `Human_Codesheet.csv` separate from the blank template.

Supply the materials relevant to your own research question and coding requirements.

## Resolve the rules and review the prompt

Codex reads the designated materials and asks focused questions about eligibility, definitions, calculations, missing versus zero values, evidence locators and permitted external lookups. You decide substantive choices. The prompt must define every template field. Changes to the template require your agreement.

Codex records decisions so they need not be repeated. The approved prompt makes eligibility criteria and variable definitions explicit, including previously unwritten conventions. For planning, allow approximately 30–60 minutes for this stage, potentially longer; this is practical planning guidance, not a formally measured completion time or guarantee. The workflow used here recommends batches of five papers: eligibility reviewed paper by paper, a Master approved estimate list compiled only after every paper is reviewed, then coding for the whole approved set. See Stage 2 for the exact sequence.

A fresh independent agent checks the draft before researcher review when that capability is available. Codex must disclose if independent review cannot be performed. Codex always offers you draft review; you can accept or skip it. Skipping review is not automatically final approval.

Codex also asks whether you want optional manual review by Claude, Gemini or another LLM. If you accept, give that reviewer the prompt, relevant protocol/codebooks and blank template. **Paste the reviewer's output back into Codex.** Codex evaluates the feedback against your decisions and discusses substantive changes with you. External feedback does not automatically change or approve the prompt.

## Approve and proceed

Explicitly approve the extraction prompt when satisfied. Save its version and date with the compatible template and decision record. For later changes, preserve the old version and create a new one. Keep the prompt version used for each batch; if a change affects an earlier batch, decide whether that batch needs review or recoding.

Stage 1 produces an approved extraction prompt, blank template, decision record and project instructions. Then follow [Stage 2 procedures](stage2.md) in `second-coder-codex/references/stage2.md`. Use your own approved extraction prompt and compatible Template_Codesheet.csv. These define the eligibility criteria, fields and calculations for your project.
