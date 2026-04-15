"""Test the build_constants stand-alone script."""
import pytest
from unittest.mock import patch
from click.testing import CliRunner
from typing import Any
from build_constants import get_template_data, write_constants_module

@pytest.fixture
def mock_template() -> str:
    """Mock test template."""
    return """
from enum import StrEnum

class USGSCollection(StrEnum):
    {% for item in collections %}
    {{ item.enum_member }} = "{{ item.value }}"
    {% endfor %}

"""

@pytest.fixture
def mock_schema() -> dict[str, Any]:
    """Mock test schema."""
    return {
        "paths": {
            "/collections/monitoring-locations/items": {"get": {}},
            "/collections/daily/items": {"get": {}},
            "/conformance": {"get": {}} 
        }
    }

def test_get_template_data(mock_schema):
    """Verify extraction of collections."""
    data = get_template_data(mock_schema)

    assert len(data) == 2
    assert data[0]["value"] == "daily"
    assert data[1]["enum_member"] == "MONITORING_LOCATIONS"

def test_cli_output_to_stdout(mock_schema, mock_template, tmp_path):
    """Verify CLI."""
    # Setup template file
    template_directory = tmp_path / "templates"
    template_directory.mkdir()
    template_name = "constants.py.j2"
    template_file = template_directory / template_name
    template_file.write_text(mock_template)

    # Patch and run CLI
    with patch("build_constants.get_schema") as mock_get_schema:
        mock_get_schema.return_value = mock_schema

        runner = CliRunner()
        result = runner.invoke(
            write_constants_module,
            [str(template_directory), "--name", template_name]
        )

        assert result.exit_code == 0
        assert "class USGSCollection" in result.output
        assert "daily" in result.output
        assert "MONITORING_LOCATIONS" in result.output

def test_cli_overwrite_error(mock_schema, mock_template, tmp_path):
    """Verify CLI."""
    # Setup template file
    template_directory = tmp_path / "templates"
    template_directory.mkdir()
    template_name = "constants.py.j2"
    template_file = template_directory / template_name
    template_file.write_text(mock_template)
    output_file = template_directory / "constant.py"
    output_file.touch()

    # Patch and run CLI
    with patch("build_constants.get_schema") as mock_get_schema:
        mock_get_schema.return_value = mock_schema

        runner = CliRunner()
        result = runner.invoke(
            write_constants_module,
            [
                str(template_directory),
                "--name",
                template_name,
                "--output",
                str(output_file)
                ]
        )

        assert result.exit_code == 1
        assert isinstance(result.exception, FileExistsError)

def test_cli_overwrite(mock_schema, mock_template, tmp_path):
    """Verify CLI."""
    # Setup template file
    template_directory = tmp_path / "templates"
    template_directory.mkdir()
    template_name = "constants.py.j2"
    template_file = template_directory / template_name
    template_file.write_text(mock_template)
    output_file = template_directory / "constant.py"
    output_file.touch()

    # Patch and run CLI
    with patch("build_constants.get_schema") as mock_get_schema:
        mock_get_schema.return_value = mock_schema

        runner = CliRunner()
        result = runner.invoke(
            write_constants_module,
            [
                str(template_directory),
                "--name",
                template_name,
                "--output",
                str(output_file),
                "--overwrite"
                ]
        )

        assert result.exit_code == 0
