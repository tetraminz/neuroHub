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
1. Import neurohub, call run_p300_pipeline().
2. nbclient-run the notebook(s).
3. pytest -q.
4. If tests fail → fix code, re-run (3 retries).
5. nbqa black, commit.

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
