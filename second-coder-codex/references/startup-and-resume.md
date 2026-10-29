# Startup readiness and resumption

Use this reference when starting or resuming a project. These are technical readiness and navigation steps, not new scientific approval rounds. Keep the existing extraction, comparison, decision and finalization routines.

## Choose and confirm the model

After the opening overview and establishment of the project folder, and before the extended Stage 1 coding-rule discussion, initiate model selection. Installation alone does not require choosing settings or starting a research project. This is an operational choice, not approval of scientific coding rules.

If a clear preference or confirmed choice has not already been supplied, prompt:

> Before we develop your coding rules, let's choose the model and reasoning setting for this project. Do you already have a preferred configuration, or would you like me to consult current official OpenAI guidance and recommend one?
>
> If you would like a recommendation, tell me whether to prioritize accuracy or balance accuracy with cost and processing time.

Adapt this prompt to information already provided; do not ask again for a known preference. If a recommendation is requested, consult current official OpenAI guidance, starting with [Models](https://learn.chatgpt.com/docs/models) and, where needed, [model selection](https://developers.openai.com/api/docs/guides/model-selection). Recommend a current reasoning model and a supported reasoning setting suitable for multi-step research, article text/table-image inspection and this client's tools. Explain the accuracy, cost and processing-time tradeoffs briefly. Describe this as a starting recommendation, not proof of superior extraction accuracy. Do not require the newest, most expensive model or the maximum reasoning setting, and do not infer equivalent effort from labels across model generations. If current guidance cannot be accessed, say so and help the researcher confirm an available choice without presenting remembered information as current guidance.

Use reliable session information about available models when exposed. Otherwise ask the researcher which relevant options they can select; do not assume account access from a public model list. Respect a suitable configuration the researcher has already chosen. If a proposed choice lacks a required capability, explain the specific issue and help identify an available alternative.

Explain how to select the model and reasoning setting in the actual Codex client. In the desktop interface this uses the model/reasoning controls; in the interactive CLI it uses `/model`. The researcher selects the settings and confirms the choice. Do not change global configuration or claim to have switched the active model merely because the researcher accepted a recommendation. If settings are not directly observable, ask for the displayed model name and reasoning setting and record them as researcher-confirmed rather than independently verified. Do not invent an underlying model snapshot, hidden configuration or a setting not shown by the client.

Save the model name, reasoning setting, confirmation date, and whether the settings were observed or researcher-confirmed in the existing project progress/run record. For a recommendation, also record the guidance links and date consulted. Link to that record from `PROJECT_GUIDE.md`; do not create a separate approval ledger or replace saved-state formats. Wait for selection/confirmation before the extended Stage 1 discussion, then continue the existing readiness and compatibility steps without another generic permission request.

For fresh per-paper coding or prompt-review agents, use the confirmed configuration where the actual host permits it. Check and record separately configured agent models/reasoning settings when exposed. If overrides or the resolved agent settings are unavailable, disclose that limit and record inherited/default or unknown settings accurately; do not claim uniform settings without evidence. Do not silently substitute a different model. If a different configuration is needed, explain it and obtain the researcher's choice before affected coding begins. Document subsequent changes and the affected stage/batch without overwriting earlier run records.

On resumption, reuse a recorded confirmed choice when the settings remain the same. Check reliable session metadata if exposed; ask only when a consequential change or missing setting cannot otherwise be established. For an older project without a model record, confirm settings before further research work; do not infer settings for already completed work or restart settled coding-rule approvals. If a model is retired or unavailable, explain the issue and help the researcher choose an available replacement. Never silently upgrade or rerun completed coding.

## First project start

After the opening overview, establish the intended project folder and complete model selection as described above. Confirm read access to designated inputs and a writable location for generated outputs. Do not read completed human coding to test access. Installation alone does not authorize starting a research project.

Locate Python 3.10+ and test whether `pymupdf` can be imported. Routine project-local setup is allowed within the user's authorization and environment permissions; explain any action that requires their involvement. Check whether fresh coding/prompt-review agents are available and disclose the existing fallback if not. No completed human data are needed for these checks.

Before an extended Stage 1 clarification session, verify that the client can display an inline panel and return its button action into the conversation. Use the small data-free check provided with the skill:

```text
python scripts/check_client.py prepare --output <project-folder>/compatibility-check
```

Use actual accessible paths. The helper creates `compatibility-check.html` and `check.json`. An unchanged prepared check can be reused; do not reset a completed check. Its `status` is initially `prepared`, not `passed`.

Display the generated HTML fragment through the host's in-conversation visualization mechanism. When available, follow the installed visualization skill's display contract. The expected content reference is:

```text
visualize{"path":"<absolute project path>/compatibility-check/compatibility-check.html"}
```

Explain: "Before we spend time developing your coding rules, please select Send compatibility confirmation below. This checks that the review panel can return a message to this chat. It contains no research data and approves no coding decisions. Complete the app's confirmation if it appears."

End the turn while waiting for that action. Do not click it for the researcher, invent its return message, or interpret file generation as a successful check. If the panel is absent or the button reports that submission is unavailable, explain the actual limitation and help the researcher choose a compatible client or explicitly agree an available alternative. Do not silently change the Stage 3 interface. Dependency inspection and organizing already designated materials can proceed independently; defer an extended Stage 1 session while the panel path is unresolved unless the researcher explicitly chooses to continue with that known limitation.

The return message contains JSON between `SECOND_CODER_COMPATIBILITY_CHECK` and `END_SECOND_CODER_COMPATIBILITY_CHECK`. Save the exact message as a text file in the project, then verify it:

```text
python scripts/check_client.py verify --check-dir <project-folder>/compatibility-check --message <saved-message.txt>
```

The helper checks the saved check ID, format and reported capabilities, preserves a receipt, and marks `check.json` as `passed`. Only then acknowledge the panel-to-chat check as passed. This is a capability check, not evidence of extraction accuracy, a guarantee of later persistence, or validation of every adjudication control. It sends no source files or research values. The presence of widget-state support is diagnostic; best-effort draft persistence is not a requirement for receiving confirmed decisions.

If sending is cancelled or fails, keep the same check available and allow a retry. A check passed in the current client/session need not be repeated for every batch. Recheck if the client changes, the capability fails, or the old result cannot be tied to the environment now being used. For a genuinely new check, prepare an unused folder such as `compatibility-check-02` and update the project guide; do not overwrite an earlier check or reuse its passed receipt as evidence about a changed client. Ask about a changed client only when that uncertainty matters.

## One project entry point

Create or update `PROJECT_GUIDE.md` in the project folder. Keep it short and link to:

- The existing progress/state record and current batch/paper status.
- The current approved prompt and blank template, with their versions.
- The existing run record containing the confirmed model/reasoning settings and any separately configured coding-agent settings.
- The existing rule-decision, estimate-approval and adjudication records.
- The current saved review session and confirmed receipt, when applicable.
- The latest final output folder and the exact next action or missing input.

Use relative links within the project where practical. This guide is an index, not another approval ledger. Keep the existing saved-state formats and authoritative decision records; do not migrate them or infer approval from a filename. Update the guide when the stage or pending action changes and before a requested pause. On normal completion link the final codesheet and state that the designated project is complete.

For an older project without this guide, locate existing state and designated source lists without opening reserved human codesheets or dumping directory contents that expose coding answers. Read and verify its saved approvals, then create the navigation guide. Ask only about a consequential gap that cannot be established from the records.

Provide this copyable resumption instruction when useful:

> Resume my second-coder project at [full project-folder path]. Read PROJECT_GUIDE.md and its linked progress, approval and decision records. Tell me the last completed step and the next action, preserve my previous decisions, and continue the authorized work.

Explain once that confirmed submissions are durable project records. Unsubmitted clicks are best-effort panel drafts; do not promise recovery after a lost panel. Reuse the saved review and confirmed records instead of rebuilding scope or reopening settled choices.

## Help with a current-paper human export

If a researcher needs help producing the Stage 3 input, ask which spreadsheet software they use and how the paper is identified. Guide them to filter their master workbook to the named paper, copy the original headers and every corresponding row into a separate CSV/XLSX, and verify that no other paper remains. Some spreadsheet copy operations include hidden rows, so tell them to copy visible rows only or verify the exported file before providing it. Reuse their original coding columns and preserve all human-coded estimates, including those absent from the AI-approved list. Do not open the full master workbook or other papers' human coding to provide this assistance.
