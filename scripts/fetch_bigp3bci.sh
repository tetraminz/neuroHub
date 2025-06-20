#!/usr/bin/env bash
set -euo pipefail

# Fetch a single EDF file from the PhysioNet BIGP3 BCI dataset.
# Requires an active PhysioNet account or token for private datasets.

BASE_URL="https://physionet.org/files/bigp3bci/1.0.0"
FILE="S001R01.edf"
DEST="data/${FILE}"

mkdir -p data

# Download EDF sample
wget -O "${DEST}" "${BASE_URL}/${FILE}?download=1"

# Download MD5 checksum list and verify
wget -O - "${BASE_URL}/MD5SUMS" | grep "${FILE}" > "${DEST}.md5"
md5sum -c "${DEST}.md5"
rm "${DEST}.md5"

echo "Sample stored at ${DEST}"
