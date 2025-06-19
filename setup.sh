#!/usr/bin/env bash
set -euo pipefail

MAMBA_ROOT="${HOME}/mambaforge"

if ! command -v micromamba &> /dev/null; then
echo "🔧 Installing micromamba..."
curl -sSL https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xvj -C /tmp
mkdir -p "${MAMBA_ROOT}"
/tmp/bin/micromamba shell init -s bash -p "${MAMBA_ROOT}" >/dev/null
source "${HOME}/.bashrc"
fi

echo "📦 Creating conda environment..."
micromamba env remove -n p300-agent -y || true
micromamba create -y -f environment.yaml

micromamba activate p300-agent

echo "🎧 Pulling (small) LFS EEG assets..."
git lfs install --skip-repo
git lfs pull || true # benign if no LFS pointers present

echo "🔗 Registering Jupyter kernel..."
python -m ipykernel install --user --name p300-agent --display-name "Python (p300-agent)"

echo "✅ Environment ready."