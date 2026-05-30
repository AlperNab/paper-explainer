# Paper Explainer — Standalone Real GUI Implementation

This folder is now its own runnable project app. It does not depend on the root all-project dashboard at runtime.

## Run

```bash
./run_gui.sh
```

Windows:

```powershell
.\run_gui_windows.ps1
```

Default URL: `http://127.0.0.1:9143`

## What is inside this project folder

- `app/` — FastAPI backend for this project.
- `static/` — elegant browser GUI.
- `plugins/paper-explainer.json` — this project’s own feature/customization/input schema.
- `project_config.json` — readable copy of the same project-specific configuration.
- `data/` — local SQLite jobs, uploads, exports.
- `tests/` — verifies this project has a registered real local engine.

## Project-specific scope

- Domain: `Education / Research`
- Target user: `Domain operator, business owner, analyst, or team member who needs this workflow executed reliably.`
- Core job: Paper/DOI/PDF → understandable explanation
- Suite: `Medical & Research Suite`

## Deep features applied

- figure-aware summary
- methods critique
- limitations
- glossary
- citation context
- replication checklist
- related papers
- audience modes

## Customization controls

- `execution_mode` — Execution mode (select)
- `field` — field (text)
- `audience_level` — audience level (select)
- `output_depth` — output depth (text)
- `citation_style` — citation style (select)
- `focus_section` — focus section (text)
- `language` — language (select)
- `critique_strictness` — critique strictness (slider)
- `output_format` — output format (select)
- `privacy_mode` — privacy mode (select)
- `confidence_threshold` — Confidence threshold (slider)

## Input fields

- `paper` — Paper (text) required
- `doi` — DOI (text) required
- `pdf` — PDF (text) required
- `work_brief` — Work brief / source text / URL / instructions (textarea) required

## External data policy

The local deterministic core is real and executable. Live external systems are not simulated. If Shopify, ATS, ERP, OCR/STT, maps, SERP, market data, medical databases, tax/customs databases, or other live systems are required, this project reports the missing connector/API requirement instead of inventing data.

---

## Final UX/UI Layer

This project now uses the **Evidence & Safety Workbench** pattern.

**UX workflow:** Source intake → evidence extraction → safety review → study/learning output

**Domain components:**
- Evidence extraction table
- Citation manager
- Clinical safety warnings
- Study/learning map
- Human review checklist

**Quick actions:**
- Extract evidence
- Build citation list
- Check safety warnings
- Create study outputs

**No fake-data policy:** external/live actions require real connectors or API keys. Missing connectors are reported instead of simulated.
