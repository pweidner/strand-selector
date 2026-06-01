import sys

from strand_selector.app import run_app

from strand_selector.io.pdf_loader import PDFLoader
from strand_selector.models.session import Session


def main():

    if len(sys.argv) != 2:

        print(
            "Usage:\n"
            "strand-selector counts.pdf"
        )
        sys.exit(1)

    pdf_path = sys.argv[1]

    print(
        f"Loading PDF: {pdf_path}"
    )

    print(
        "Scanning pages and extracting metadata..."
    )

    pdf_loader = PDFLoader(pdf_path)
    
    from strand_selector.utils.paths import (
        get_results_dir
    )

    output_dir = get_results_dir(
        pdf_loader.sample_name
    )

    print(
        f"Detected "
        f"{len(pdf_loader.cell_pages)} "
        f"cell pages"
    )

    print(
        f"Sample: {pdf_loader.sample_name}"
    )

    print(
        f"Results: {output_dir}"
    )

    session = Session(
        pdf_path=pdf_path,
        page_indices=list(
            range(
                len(
                    pdf_loader.cell_pages
                )
            )
        ),
        output_dir=output_dir,
    )
    run_app(
        session,
        pdf_loader,
    )


if __name__ == "__main__":
    main()
