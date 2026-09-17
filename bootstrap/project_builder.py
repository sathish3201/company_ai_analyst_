from pathlib import Path


# ============================================================
# PROJECT STRUCTURE
# ============================================================

DIRECTORIES = [
    # Bootstrap
    "bootstrap",

    # Source
    "src/company_ai",
    "src/company_ai/app",
    "src/company_ai/config",
    "src/company_ai/core",
    "src/company_ai/contracts",
    "src/company_ai/models",
    "src/company_ai/llm",
    "src/company_ai/security",

    # Configuration
    "configs",
    "configs/environments",

    # Tests
    "tests",
    "tests/unit",
    "tests/integration",

    # Data
    "data",
    "data/raw",
    "data/processed",
    "data/temporary",

    # Knowledge
    "knowledge",
    "knowledge/documents",
    "knowledge/metadata",

    # Artifacts
    "artifacts",
    "artifacts/reports",
    "artifacts/visualizations",
    "artifacts/exports",

    # Logs
    "logs",
]


# Python packages that need __init__.py
PYTHON_PACKAGES = [
    "bootstrap",

    "src/company_ai",
    "src/company_ai/app",
    "src/company_ai/config",
    "src/company_ai/core",
    "src/company_ai/contracts",
    "src/company_ai/models",
    "src/company_ai/llm",
    "src/company_ai/security",
]


FILES = [
    # Application
    "src/company_ai/app/__init__.py",
    "src/company_ai/app/container.py",

    # Config
    "src/company_ai/config/__init__.py",
    "src/company_ai/config/settings.py",
    "src/company_ai/config/paths.py",
    "src/company_ai/config/security.py",
    "src/company_ai/config/logging.py",

    # Core
    "src/company_ai/core/__init__.py",
    "src/company_ai/core/exceptions.py",
    "src/company_ai/core/request.py",
    "src/company_ai/core/context.py",

    # Contracts
    "src/company_ai/contracts/__init__.py",
    "src/company_ai/contracts/llm.py",
    "src/company_ai/contracts/security.py",
    "src/company_ai/contracts/models.py",

    # Models
    "src/company_ai/models/__init__.py",
    "src/company_ai/models/llm.py",

    # LLM
    "src/company_ai/llm/__init__.py",
    "src/company_ai/llm/gateway.py",
    "src/company_ai/llm/litellm_gateway.py",
    "src/company_ai/llm/router.py",
    "src/company_ai/llm/model_registry.py",
    "src/company_ai/llm/fallback.py",
    "src/company_ai/llm/guardrails.py",

    # Security
    "src/company_ai/security/__init__.py",
    "src/company_ai/security/authorization.py",

    # Configuration files
    "configs/security.yaml",
    "configs/models.yaml",

    "configs/environments/development.yaml",
    "configs/environments/test.yaml",
    "configs/environments/production.yaml",

    # Tests
    "tests/unit/test_settings.py",
    "tests/unit/test_paths.py",
    "tests/unit/test_context.py",
    "tests/unit/test_security.py",
    "tests/unit/test_model_registry.py",
    "tests/unit/test_router.py",
    "tests/unit/test_fallback.py",

    "tests/integration/test_ollama.py",

    # Root files
    ".env",
    ".env.example",
    ".gitignore",
    "pyproject.toml",
    "README.md",
]


# ============================================================
# PROJECT BUILDER
# ============================================================

class ProjectBuilder:
    """
    Dynamically creates the Company AI Analyst
    project structure using pathlib.
    """

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root.resolve()

    # --------------------------------------------------------
    # Create directories
    # --------------------------------------------------------

    def create_directories(self) -> None:

        for directory in DIRECTORIES:

            path = self.project_root / directory

            path.mkdir(
                parents=True,
                exist_ok=True,
            )

    # --------------------------------------------------------
    # Create Python packages
    # --------------------------------------------------------

    def create_python_packages(self) -> None:

        for package in PYTHON_PACKAGES:

            package_path = (
                self.project_root / package
            )

            package_path.mkdir(
                parents=True,
                exist_ok=True,
            )

            init_file = (
                package_path / "__init__.py"
            )

            self.create_file(init_file)

    # --------------------------------------------------------
    # Create files
    # --------------------------------------------------------

    def create_files(self) -> None:

        for file_name in FILES:

            file_path = (
                self.project_root / file_name
            )

            self.create_file(file_path)

    # --------------------------------------------------------
    # Safe file creation
    # --------------------------------------------------------

    @staticmethod
    def create_file(path: Path) -> None:

        # Make sure parent directory exists
        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        # Never overwrite existing files
        if not path.exists():

            path.touch()

            print(
                f"[CREATED] {path}"
            )

        else:

            print(
                f"[EXISTS]  {path}"
            )

    # --------------------------------------------------------
    # Build entire project
    # --------------------------------------------------------

    def build(self) -> None:

        print("=" * 60)
        print("Company AI Analyst - Project Builder")
        print("=" * 60)

        print("\nCreating directories...")
        self.create_directories()

        print("\nCreating Python packages...")
        self.create_python_packages()

        print("\nCreating files...")
        self.create_files()

        print("\n" + "=" * 60)
        print("PROJECT CREATED SUCCESSFULLY")
        print("=" * 60)

        print(
            f"\nProject root:\n{self.project_root}"
        )


# ============================================================
# MAIN
# ============================================================

def main() -> None:

    # Current directory becomes project root
    project_root = Path.cwd()

    builder = ProjectBuilder(
        project_root=project_root
    )

    builder.build()


if __name__ == "__main__":
    main()