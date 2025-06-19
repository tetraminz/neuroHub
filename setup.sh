#!/usr/bin/env bash
set -euo pipefail

# Where we keep micromamba + all envs/caches
MAMBA_ROOT="${HOME}/micromamba"
export MAMBA_ROOT_PREFIX="${MAMBA_ROOT}"

# ----------------------------------------------------------------------
# 1.  Grab the latest static micromamba
# ----------------------------------------------------------------------
if ! command -v micromamba &>/dev/null; then
  echo "🔧  Installing micromamba …"
  curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest \
      | tar -xJ -C /tmp bin/micromamba
  export PATH="/tmp/bin:$PATH"
fi

# ----------------------------------------------------------------------
# 2.  One-shot shell hook (no need to touch ~/.bashrc)
# ----------------------------------------------------------------------
eval "$(micromamba shell hook --shell=bash)"

# OPTIONAL — persist hooks for future *interactive* sessions
# micromamba shell init --shell=bash -r "${MAMBA_ROOT}"

# ----------------------------------------------------------------------
# 3.  Create or recreate the project env from environment.yaml
# ----------------------------------------------------------------------
echo "📦  Creating conda environment …"
micromamba create -y -n p300-agent -f environment.yaml

micromamba activate p300-agent

# ----------------------------------------------------------------------
# 4.  (Optional) pull small LFS demo data, register ipykernel
# ----------------------------------------------------------------------
echo "🎧  Pulling LFS EEG assets (if any) …"
git lfs install --skip-repo
git lfs pull || true

echo "🔗  Registering Jupyter kernel …"
python -m ipykernel install --user --name p300-agent \
       --display-name "Python (p300-agent)"

echo "✅  Environment ready."
