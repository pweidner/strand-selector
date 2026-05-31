import re

import fitz

from PySide6.QtGui import QPixmap


class PDFLoader:

    def __init__(self, pdf_path):

        self.doc = fitz.open(pdf_path)

        self.cell_pages = []

        self.sample_name = None

        self.scan_pages()
    
    def scan_pages(self):

        for page_idx in range(len(self.doc)):

            page = self.doc.load_page(page_idx)

            text = page.get_text()

            if self.sample_name is None:

                sample_name = self.extract_sample_name(
                    text
                )

            if sample_name:
                
                self.sample_name = sample_name

            if "Cell:" not in text:
                continue

            cell_id = self.extract_cell_id(text)

            if cell_id is None:
                continue

            self.cell_pages.append(
                {
                    "page_index": page_idx,
                    "cell_id": cell_id,
                    "text": text,
                }
            )

    def extract_cell_id(self, text):

        match = re.search(
            r"Cell:\s*(\S+)",
            text
        )

        if match:
            return match.group(1)

        return None

    def extract_reads(self, text):

        match = re.search(
            r"Total number of reads:\s*([\d,]+)",
            text
        )

        if match:
            return match.group(1)

        return "NA"

    def extract_duplicate_rate(self, text):

        match = re.search(
            r"Duplicate rate:\s*([\d.]+%)",
            text
        )

        if match:
            return match.group(1)

        return "NA"

    def get_cell_info(self, cell_idx):

        entry = self.cell_pages[cell_idx]

        return {
            "page_index": entry["page_index"],
            "cell_id": entry["cell_id"],
            "reads": self.extract_reads(entry["text"]),
            "duplicate_rate": self.extract_duplicate_rate(
                entry["text"]
            ),
        }

    def render_page(self, cell_idx):

        page_idx = self.cell_pages[cell_idx][
            "page_index"
        ]

        page = self.doc.load_page(page_idx)

        pix = page.get_pixmap(
            matrix=fitz.Matrix(3, 3)
        )

        image = QPixmap()

        image.loadFromData(
            pix.tobytes("png")
        )

        return image

    def extract_sample_name(self, text):

        for line in text.splitlines():

            line = line.strip()

            if line.startswith("Sample:"):

                sample = (
                    line
                    .replace("Sample:", "")
                    .strip()
                )

                if sample:
                    return sample

        return None
