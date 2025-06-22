#!/usr/bin/env bash
set -euo pipefail

# Fetch a single EDF file from the PhysioNet BIGP3 BCI dataset.
# Requires an active PhysioNet account or token for private datasets.

# Version as hosted on PhysioNet (adjust if newer)
BASE_URL="https://physionet.org/files/bigp3bci/1.0.1"
FILE="S001R01.edf"
DEST="data/${FILE}"

mkdir -p data

# Download EDF sample; try files/ then content/ paths
if ! wget -qO "${DEST}" "${BASE_URL}/${FILE}?download=1"; then
    echo "Trying alternate URL ..." >&2
    ALT="https://physionet.org/content/bigp3bci/1.0.1/${FILE}?download=1"
    wget -O "${DEST}" "${ALT}"
fi

# Download MD5 checksum list and verify if available
if wget -qO - "${BASE_URL}/MD5SUMS" | grep "${FILE}" >"${DEST}.md5"; then
    md5sum -c "${DEST}.md5"
    rm "${DEST}.md5"
else
    echo "Warning: checksum file not found; skipping verification." >&2
fi

echo "Sample stored at ${DEST}"
