# Final output organization

After final adjudication, proactively organize the final data and every generated auxiliary artifact into one structured output folder. Do not compress it into a ZIP. This is the researcher's project output folder, distinct from the installable skill folder. Do not present an undifferentiated collection of files. Preserve working files and original inputs; stage copies for delivery rather than moving/deleting the project.

Use this structure, adding batch and paper subfolders where applicable. Omit categories with no artifacts instead of creating misleading empty outputs.

```text
Project_Outputs/
  README.md
  File_Index.csv
  SHA256SUMS.txt
  01_Final_Data/
    batch-01/Adjudicated_Codesheet.csv
  02_Protocol_and_Template/
    approved_prompt_versions/
    templates/
    coding_rule_decisions/
  03_Approved_Estimates/
    batch-01/master/
    batch-01/per-paper/
  04_AI_Coding/
    batch-01/master/
    batch-01/per-paper/
  05_Adjudication/
    batch-01/human_input/
    batch-01/comparisons/
    batch-01/decisions/
    batch-01/pending_issues/
    batch-01/mappings/
  06_Source_Evidence/
    batch-01/paper-01/issue-001/
  07_PDF_Reading_Aids/
    batch-01/paper-01/
  08_Validation_and_Run_Records/
    batch-01/
  09_Superseded/
    batch-01/
```

Only researcher-finalized codesheets belong in `01_Final_Data`. Put drafts and superseded data in `09_Superseded`; label them clearly. Keep independent AI codesheets, including `AI_reason`, in `04_AI_Coding`. Store evidence screenshots, textual fallbacks, screenshot metadata and any lookup/calculation evidence in `06_Source_Evidence`; store bulk Stage 2A texts/images and conversion reports in `07_PDF_Reading_Aids`. Keep in-conversation panel fragments, review data, received confirmation messages, saved choices and receipts with decisions in `05_Adjudication`; put application/finalization check records in `08_Validation_and_Run_Records`. Use the existing evidence-link portability procedure for their audit copies, and exclude disposable local connection metadata as described in `grouped-review.md`. Classify unmatched generated artifacts by their actual function; do not silently discard them. Multi-batch final data can include a verified project master plus batch datasets; do not combine batches without checking schema/version compatibility and duplicate coverage.

The root README must identify the exact final codesheet(s) to use, explain each populated folder, state scope/batch counts and final/draft status, summarize accepted evidence limitations and unresolved items where applicable, and link to the approved protocol. Keep this README focused on using the results; omit skill release/version history and descriptions of changes between releases. Preserve prompt versions and approval history in protocol and audit records. Use relative paths/links. The index lists every packaged artifact with its type, description, size and hash. Include source manifests with original PDF paths/hashes. Source PDFs need not be recopied unless requested or already designated as part of the deliverable; preserve all source screenshots actually used for adjudication. Do not sweep unrelated papers or human datasets into the output folder.

## Build and verify

1. Inventory the generated output roots and classify all files. Include final and auxiliary deliverables. Explicitly exclude only disposable caches, dependency/runtime files, unrelated files or redundant compressed copies, with reasons in the packaging manifest. Do not exclude an auxiliary research output merely because it is large or inconvenient. Preserve historical results in `09_Superseded`.
2. Prepare copies with folder-relative links between decision records and their evidence. Keep immutable original records; label any reformatted portable copy. Check those links in the completed output folder. The packaging helper cannot rewrite prose links automatically.
3. Create `package_manifest.json` with `package_name`, `status` (`final` or `draft`), `summary`, `artifact_roots`, `files`, and optional `excluded` and `notes`. Each `files` entry has `source`, `destination` (starting with a category folder above), and `description`. Each `excluded` entry has `source` and `reason`. Paths to source files/roots are relative to the manifest location or absolute. `artifact_roots` are the designated generated output directories, not the whole workspace. Every file in them must be either packaged or explicitly excluded. For example:

```json
{
  "package_name": "Project_Outputs",
  "status": "final",
  "summary": "Batch 01: five papers, all adjudication decisions finalized.",
  "artifact_roots": ["project-output"],
  "files": [
    {"source": "project-output/Adjudicated_Codesheet.csv", "destination": "01_Final_Data/batch-01/Adjudicated_Codesheet.csv", "description": "Final researcher-approved codesheet"},
    {"source": "project-output/decisions.csv", "destination": "05_Adjudication/batch-01/decisions/decisions.csv", "description": "Researcher decisions with evidence links"}
  ],
  "excluded": [],
  "notes": ["Finalization and the approved protocol are recorded in the decision log."]
}
```

4. Run `python scripts/package_outputs.py --manifest package_manifest.json --output Project_Outputs`. The output is a directory, not an archive. Choose an unused destination outside inventoried artifact roots. The helper rejects uncategorized paths, missing files, collisions, unaccounted generated files and overwrites; copies artifacts into category subfolders; generates the README/index/hash list; and verifies copied file hashes before publishing the complete folder. It preserves original file bytes and working files. It does not establish that a researcher's decisions are complete; confirm that before setting `status` to `final`.
5. Inspect the output directory tree, verify final codesheet contents match the finalized working artifact, and check relative evidence links inside the delivered folder. Then provide a link/path to that folder and a direct link to the final codesheet. Do not create a ZIP. In a draft package, state what is outstanding and do not place draft data in `01_Final_Data`.

A resumed or later batch uses the same organization. A new delivery must not overwrite an existing output folder. Folder organization is an automatic finalization action; do not ask the researcher to classify files or say “continue.”
