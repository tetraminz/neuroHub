from pathlib import Path

import nbformat
from nbclient import NotebookClient


def test_p300_starter_notebook_runs(tmp_path):
    nb_path = Path("notebooks/p300_starter.ipynb")
    nb = nbformat.read(nb_path, as_version=4)
    client = NotebookClient(nb, timeout=600, kernel_name="python3")
    client.execute()

    for cell in nb.cells:
        for output in cell.get("outputs", []):
            if output.output_type == "stream" and "LDA mean accuracy:" in output.text:
                acc_str = output.text.split("accuracy:")[1].split("±")[0]
                mean_acc = float(acc_str.strip())
                assert mean_acc >= 0.60
                return
    assert False, "Accuracy output not found"
