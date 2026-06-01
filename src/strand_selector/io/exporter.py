from pathlib import Path

import pandas as pd


def export_annotations(
    session,
    pdf_loader,
    output_dir,
):

    rows = []

    for idx in range(
        len(pdf_loader.cell_pages)
    ):

        info = pdf_loader.get_cell_info(idx)

        cell_id = info["cell_id"]

        rows.append(
            {
                "cell_id": cell_id,
                "label": session.annotations.get(
                    cell_id,
                    ""
                ),
                "reads": info["reads"],
                "duplicate_rate": info[
                    "duplicate_rate"
                ],
            }
        )

    pd.DataFrame(rows).to_csv(
        output_dir / "annotations.csv",
        index=False,
    )

def export_selected(
    session,
    output_dir,
    sample_name,
):

    output_file = (
        output_dir
        / f"{sample_name}.txt"
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