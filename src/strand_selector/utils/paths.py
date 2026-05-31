# utils/paths.py

from pathlib import Path


def get_results_dir(sample_name):

    results_dir = (
        Path("results")
        / sample_name
    )

    results_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    return results_dir
