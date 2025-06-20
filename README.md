# P300 EEG Analysis Starter Kit

This repository provides minimal building blocks to experiment with event-related potential (ERP) detection, focusing on the P300 component. It includes a conda environment specification, a bootstrap script and a simple smoke test.

## Setup

Run `setup.sh` to create the **p300-agent** environment and install the Jupyter kernel:

```bash
bash setup.sh
```

The script downloads **micromamba**, creates the conda environment based on `environment.yaml`, pulls optional Git LFS data and registers a `p300-agent` kernel for Jupyter.

## Data

The project expects a `data/` directory (see `AGENTS.md`) for small EEG assets
tracked with Git LFS. Real datasets are not bundled with the repository.

To initialise and use Git LFS:

```bash
git lfs install           # enable LFS support
git lfs pull              # fetch any available data
git lfs track "data/*.fif"
```

Place your own `.fif` recordings under `data/` and commit the resulting
`.gitattributes` so others can retrieve them via `git lfs pull`.

`notebooks/p300_starter.ipynb` uses synthetic data by default but can be adapted
to load real files from `data/`.

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
3. `git lfs pull` or add recordings under `data/`
4. `pytest -q`
5. `jupyter lab`
