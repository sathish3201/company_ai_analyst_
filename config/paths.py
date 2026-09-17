from pathlib import Path


class ProjectPaths:
    def __init__(self, root: Path | None = None):
        self.root = root or Path.cwd()

    @property
    def src(self) -> Path:
        return self.root / "src"

    @property
    def data(self) -> Path:
        return self.root / "data"

    @property
    def raw_data(self) -> Path:
        return self.data / "raw"

    @property
    def processed_data(self) -> Path:
        return self.data / "processed"

    @property
    def temporary_data(self) -> Path:
        return self.data / "temporary"

    @property
    def knowledge(self) -> Path:
        return self.root / "knowledge"

    @property
    def documents(self) -> Path:
        return self.knowledge / "documents"

    @property
    def artifacts(self) -> Path:
        return self.root / "artifacts"

    @property
    def reports(self) -> Path:
        return self.artifacts / "reports"

    @property
    def visualizations(self) -> Path:
        return self.artifacts / "visualizations"

    @property
    def exports(self) -> Path:
        return self.artifacts / "exports"

    @property
    def logs(self) -> Path:
        return self.root / "logs"

    def create_directories(self) -> None:
        directories = [
            self.raw_data,
            self.processed_data,
            self.temporary_data,
            self.documents,
            self.reports,
            self.visualizations,
            self.exports,
            self.logs,
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)