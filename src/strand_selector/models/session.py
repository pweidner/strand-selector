from dataclasses import dataclass, field


@dataclass
class Session:
    pdf_path: str

    page_indices: list[int]

    output_dir: str

    current_index: int = 0

    annotations: dict[str, str] = field(
        default_factory=dict
    )

    @property
    def total_cells(self):
        return len(self.page_indices)

    @property
    def current_page(self):
        return self.page_indices[self.current_index]
