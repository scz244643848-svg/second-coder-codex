# Package version 2026.10.26

Authors: Chunzhi Shi, Zhehan Zhu and W. Robert Reed.

Prepared on 26 October 2026 for a separate Zenodo software deposit. The authors confirmed the title, author order, affiliations, ORCIDs, maintainer and MIT license. The version-specific DOI is 10.5281/zenodo.23657589. A reserved DOI becomes publicly available when the Zenodo record is published.

## Changes from the 20261018 package

- Added a data-free startup panel check to verify the client can display controls and return a confirmation message before a long Stage 1 session. Technical readiness checks and recovery steps are described in a linked reference.
- Added qualified Stage 1 planning guidance: approximately 30–60 minutes, potentially longer. This is practical planning guidance, not a measured workload result or promise.
- Clarified that AI field coding is withheld from completed human coding, while estimate selection is reviewed and approved by the researcher.
- Explained that Stage 1 makes eligibility criteria and variable definitions explicit and that the final adjudicated codesheet is the data input for the researcher's analysis.
- Made the existing approval actions and periods requiring no researcher action easier to understand.
- Added a project navigation guide and a copyable resumption instruction without changing the existing state or receipt formats. Unsubmitted panel choices remain best-effort drafts.
- Added guidance for researchers who need to export a current-paper-only human codesheet from a master workbook.
- Removed a model-setting recommendation whose supporting discussion was absent from the user guide.
- Added author attribution, affiliations, ORCIDs, maintainer details, citation metadata and the full approved MIT license. Publication metadata has been finalized for the Zenodo deposit.

## Startup receipt filename correction

The startup compatibility helper uses a short hash prefix for message and receipt filenames, with collision handling. Full SHA-256 values remain in the records and are used for verification. This reduces Windows path-length failures without changing the confirmation payload or research workflow.

## Preserved behavior

The existing PDF preparation, evidence rendering, codesheet checking/merging, review panel, adjudication imports, finalization and output-packaging scripts are unchanged. The preserved original Stage 1 and Stage 3 reference skills are unchanged. The new helper only prepares and verifies the startup compatibility check; it cannot approve coding rules, estimates or adjudication decisions.

## Validation scope

The prior review exercised 15 synthetic checks of the existing helpers. This revision additionally checks the new helper and its panel behavior with synthetic messages, including unsupported/cancelled submission and a wrong-check rejection. Package integrity, references, syntax and skill metadata are checked before distribution. This is a limited update check, not a new extraction benchmark or a claim of a new first-time-user trial.

The startup filename correction passed 17 targeted checks, including a Windows deep-path case, collision handling, tamper rejection and repeated-submission handling. A live startup panel confirmation was also received and verified in the current client. The publication-preparation step changes only package metadata, licensing and documentation; the entire skill directory remains byte-for-byte identical to the checked path-fix package.
