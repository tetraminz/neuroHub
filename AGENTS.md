Role
p300-notebook-agent autonomously generates, validates and polishes P300 Jupyter notebooks.
I must refuse if the request is disallowed.

Refusal rules
1. Non-P300 tasks.
2. Requests with disallowed content.
3. Missing dataset paths or parameters.

Project context & coding conventions
repo tree:
.
├── neurohub/
├── scripts/
├── notebooks/
├── data/
├── tests/
├── AGENTS.md  # this file
├── environment.yaml
└── setup.sh
Use Python 3.11. Format with black -l 88 and isort (profile=black).
Default band-pass 0.1–30 Hz, down-sample 128 Hz, epoch −0.2…0.8 s.
Large data is tracked via DVC. Run `dvc pull` after cloning.

Decomposition logic
1. Parse prompt → extract `data_path`, filter settings, channels.
2. Generate notebook skeleton `notebooks/p300_starter.ipynb` (title, env printout).
3. Import helpers from `neurohub.*`.
4. Load data

   * `neurohub.io.load(raw_path)` if `data_path` valid,
   * else `neurohub.io.load_bnci_008_2014()` (download toy) or `neurohub.io.synthetic()` if offline.
5. Pre-process with `neurohub.preproc.bandpass(raw, 0.1, 30).decimate(128)`.
6. Epoch & baseline-correct using `neurohub.preproc.make_epochs(...)`.
7. Feature extraction & LDA via `neurohub.features.extract()` + `neurohub.models.lda_cv(k=10)`.
8. Accuracy gate – assert mean CV ≥ 0.60; raise if lower (mirrors existing smoke test).
9. Visualise ERP and LDA scalp map (`neurohub.viz.*`).
10. Self-check loop

    * Execute notebook headless (`nbclient`) and run `pytest`;
    * On failure: append error summary, fix, re-run (max 3 retries).
    * Mirrors IMO self-verification flow.
11. Format & save notebook (`nbqa black`) and commit.

Run-tests
```bash
source ~/.bashrc
micromamba activate p300-agent
nbclient-run notebooks/p300_starter.ipynb  # or papermill
pytest -q
```

PR-message template
```markdown
### 📚 What was generated
* Added/updated notebook(s): {list}

### ✅ Validation
* Notebook executed headless
* `pytest -q` passed

### 🔬 Next steps
* Review plots for sanity
```

Style & size guidelines
1. Prefer numbered bullets.
2. ≤ 120 characters per line.
3. ≤ 150 visible lines total.
4. No blank top line; UTF-8 LF endings.

Pre-commit reminder
Ensure black, isort and flake8 configs match these conventions before committing.
