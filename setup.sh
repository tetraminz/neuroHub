#!/usr/bin/env bash
set -euo pipefail

MAMBA_ROOT="${HOME}/micromamba"
export MAMBA_ROOT_PREFIX="${MAMBA_ROOT}"

# ----------------------------------------------------------------------
# 1.  Install micromamba (static binary)
# ----------------------------------------------------------------------
if ! command -v micromamba &>/dev/null; then
  echo "🔧  Installing micromamba …"
  curl -L \
    https://github.com/mamba-org/micromamba-releases/releases/latest/download/micromamba-linux-64 \
    -o /tmp/micromamba
  chmod +x /tmp/micromamba
  export PATH="/tmp:$PATH"
fi

# ----------------------------------------------------------------------
# 2.  One-shot shell hook (no ~/.bashrc needed)
# ----------------------------------------------------------------------
eval "$(micromamba shell hook --shell=bash)"

# ----------------------------------------------------------------------
# 3.  Create / recreate the env
# ----------------------------------------------------------------------
echo "📦  Creating conda environment …"
micromamba create -y -n p300-agent -f environment.yaml

micromamba activate p300-agent

# ----------------------------------------------------------------------
# 4.  Optional data + kernel
# ----------------------------------------------------------------------
echo "🎧  Pulling LFS EEG assets (if any) …"
git lfs install --skip-repo
git lfs pull || true

echo "🔗  Registering Jupyter kernel …"
python -m ipykernel install --user --name p300-agent \
       --display-name "Python (p300-agent)"

echo "✅  Environment ready."
