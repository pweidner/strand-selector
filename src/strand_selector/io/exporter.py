from pathlib import Path

import pandas as pd


def export_annotations(
    session,
    output_dir,
):

    rows = []

    for cell_id, label in session.annotations.items():

        rows.append(
            {
                "cell_id": cell_id,
                "label": label,
            }
        )

    output_file = (
        output_dir
        / "annotations.csv"
    )

    pd.DataFrame(rows).to_csv(
        output_file,
        index=False,
    )


def export_selected(
    session,
    output_dir,
):

    output_file = (
        output_dir
        / "selected_cells.txt"
    )

    with open(output_file, "w") as handle:

        for (
            cell_id,
            label,
        ) in session.annotations.items():

            if label == "selected":

                handle.write(
                    f"{cell_id}\n"
                )
