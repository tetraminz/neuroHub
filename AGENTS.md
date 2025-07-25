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
├── notebooks/
├── env/
├── data/
├── tests/
├── agent.md  # this file
├── environment.yaml
└── setup.sh
Use Python 3.11. Format with black -l 88 and isort (profile=black).
Default band-pass 0.1–30 Hz, down-sample 128 Hz, epoch −0.2…0.8 s.

Decomposition logic
1. Inspect prompt/context for dataset and parameters.
2. Create notebooks/p300_starter.ipynb skeleton with title and version.
3. Load or synthesize data.
4. Pre-process → epoch → baseline-correct.
5. Train LDA with 10-fold CV; require accuracy ≥ 0.60.
6. Visualise ERP and scalp map.
7. Self-check: run notebook headless with nbclient, then pytest.
8. Format with black and nbqa; save.
9. If any test fails, append error summary as a markdown cell, fix the notebook and re-run.

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
