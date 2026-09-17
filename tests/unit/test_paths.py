from pathlib import Path

from company_ai.config.paths import ProjectPaths


def test_project_paths_are_path_objects():
    paths = ProjectPaths()

    assert isinstance(paths.root, Path)
    assert isinstance(paths.data, Path)
    assert isinstance(paths.logs, Path)


def test_create_directories(tmp_path):

    paths = ProjectPaths(root=tmp_path)

    paths.create_directories()

    assert paths.data.exists()
    assert paths.raw_data.exists()
    assert paths.processed_data.exists()
    assert paths.temporary_data.exists()
    assert paths.logs.exists()
    assert paths.artifacts.exists()