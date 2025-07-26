# P300 EEG Analysis Starter Kit

This repository provides minimal building blocks to experiment with event-related potential (ERP) detection, focusing on the P300 component. It includes a conda environment specification, a bootstrap script and a simple smoke test.

## Setup

Run `setup.sh` to create the **p300-agent** environment and install the Jupyter kernel.
After activation run `pip install -e .` to link the `neurohub` package:

```bash
bash setup.sh
micromamba activate p300-agent
pip install -e .
```

The script downloads **micromamba**, creates the conda environment based on `environment.yaml` and registers a `p300-agent` kernel for Jupyter.
The environment includes MNE, scikit-learn, click and DVC for data versioning.

## Data

The project expects a `data/` directory (see `AGENTS.md`) for small EEG assets.
Real datasets are not bundled with the repository.

Place your own `.fif` recordings under `data/` if you wish to work with real data.

`notebooks/p300_starter.ipynb` loads a toy dataset by default. Pass a path under
`data/` to analyse your own files. Synthetic examples run only when explicitly
requested.

## Project layout

```
neurohub/   # reusable pipeline functions
scripts/    # CLI wrappers
notebooks/  # demos importing from neurohub
data/       # DVC-tracked recordings
tests/      # unit and smoke tests
```

Retrieve large assets with:

```bash
dvc pull
```

## Running tests

Activate the environment and execute the smoke tests with `pytest -q`:

```bash
source ~/.bashrc
micromamba activate p300-agent
pytest -q
```

Alternatively you can run a single command without activating:

```bash
micromamba run -n p300-agent pytest -q
```

## Launching Jupyter

To explore or execute notebooks, start Jupyter Lab using the environment kernel:

```bash
micromamba activate p300-agent
jupyter lab
```

Choose the **Python (p300-agent)** kernel when opening notebooks.

## Basic workflow

1. `bash setup.sh`
2. `micromamba activate p300-agent`
3. `pip install -e .` once
4. Add recordings under `data/` (optional)
5. `pytest -q`
6. Run `python scripts/run_pipeline.py --data PATH` for the CLI demo
7. `jupyter lab`

## Pre-commit hooks

Enable [pre-commit](https://pre-commit.com/) to automatically format and lint
files before each commit. Install the tool once the environment is ready:

```bash
micromamba run -n p300-agent pip install pre-commit
pre-commit install
```

Run `pre-commit run --all-files` to check the entire repository.

## Using BigP3BCI data

The repository contains metadata for the **bigP3BCI** dataset but not the full
recordings. The dataset is licensed under the [CC BY 4.0 license](data/bigp3bci-an-open-diverse-and-machine-learning-ready-p300-based-brain-computer-interface-dataset-1.0.0/LICENSE.txt) and can be quite large,
so store it outside of Git when working with the complete release.

Files follow a multi-level directory structure:

```
StudyA/subject/session/phase/paradigm
```

The study folder may be `StudyA`, `StudyB`, `StudyC` and so on. Each contains
subject IDs (for example `A_01`) which in turn contain session folders such as
`SE001`. Inside a session you will find the `Train` and `Test` phases, and each
phase stores one or more paradigm folders (for example `CB`).

The dataset README describes the path template as:

```
Study#/<subject>/SE<session>/<Train|Test>/...
```

An example file path therefore looks like:

```
StudyA/A_01/SE001/Train/CB/A_01_SE001_CB_Train01.edf
```

Set the environment variable `NEURO_DATA_ROOT` to the folder containing the
`bigP3BCI-data` directory. If unset, the code defaults to `~/neuro-data`.
