from pathlib import Path


class ProjectPaths:
    def __init__(self, root: Path | None = None) -> None:
        self.root = (
            root.resolve()
            if root is not None
            else Path(__file__).resolve().parents[3]
        )

    @property
    def src(self) -> Path:
        return self.root / "src"

    @property
    def tests(self) -> Path:
        return self.root / "tests"

    @property
    def configs(self) -> Path:
        return self.root / "configs"

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
    def metadata(self) -> Path:
        return self.knowledge / "metadata"

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
            self.data,
            self.raw_data,
            self.processed_data,
            self.temporary_data,
            self.knowledge,
            self.documents,
            self.metadata,
            self.artifacts,
            self.reports,
            self.visualizations,
            self.exports,
            self.logs,
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)