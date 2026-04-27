"""Tests for the build_clients stand-alone script."""
import pytest
from unittest.mock import patch
from click.testing import CliRunner
from typing import Any
from pathlib import Path
from build_clients import write_clients_module

@pytest.fixture
def mock_client_template() -> str:
    """Mock client template that mimics the production Jinja2 structure."""
    return """
class {{ collections[0].class_name }}(BaseClient):
    \"\"\"{{ collections[0].description }}\"\"\"
    _endpoint = USGSCollection.{{ collections[0].enum_member }}

    def get(self, 
        {% for p in collections[0].parameters %}
        {{ p.python_name }}: {{ p.type_hint }} = {{ p.default }},
        {% endfor %}
    ):
        query = {
            {% for p in collections[0].parameters %}
            "{{ p.name }}": {{ p.python_name }},
            {% endfor %}
        }
        return self._get_json_responses(queries=[query])

"""

@pytest.fixture
def complex_schema() -> dict[str, Any]:
    """Mock schema with parameters that require sanitization and type mapping."""
    return {
        "paths": {
            "/collections/monitoring-locations/items": {
                "get": {
                    "description": "Test description",
                    "parameters": [
                        {
                            "name": "bbox-crs",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "string", "default": "EPSG:4326"}
                        },
                        {
                            "name": "limit",
                            "in": "query",
                            "required": True,
                            "schema": {"type": "integer", "default": 10}
                        }
                    ]
                }
            }
        }
    }

@pytest.fixture
def multi_type_schema() -> dict[str, Any]:
    """Schema with various types."""
    return {
        "paths": {
            "/collections/types/items": {
                "get": {
                    "parameters": [
                        {"name": "str_param", "in": "query",
                         "schema": {"type": "string", "default": "value"}},
                        {"name": "int_param", "in": "query",
                         "schema": {"type": "integer", "default": 42}},
                        {"name": "bool_param", "in": "query",
                         "schema": {"type": "boolean", "default": False}},
                        {"name": "none_param", "in": "query",
                         "schema": {"type": "string"}} # No default
                    ]
                }
            }
        }
    }

def test_client_generation_parameter_mapping(complex_schema, mock_client_template, tmp_path):
    """Verify that kebab-case OGC parameters are mapped to snake_case Python identifiers."""
    # Setup template
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    template_file = template_dir / "clients.py.j2"
    template_file.write_text(mock_client_template)

    with patch("build_clients.get_schema") as mock_get:
        mock_get.return_value = complex_schema

        runner = CliRunner()
        result = runner.invoke(
            write_clients_module,
            [str(template_dir), "--name", "clients.py.j2"]
        )

        assert result.exit_code == 0
        assert "bbox_crs: Optional[str] = \"EPSG:4326\"" in result.output
        assert "\"bbox-crs\": bbox_crs" in result.output

def test_client_generation_type_hints(complex_schema, mock_client_template, tmp_path):
    """Verify JSON type to Python type hint mapping."""
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    (template_dir / "clients.py.j2").write_text(mock_client_template)

    with patch("build_clients.get_schema") as mock_get:
        mock_get.return_value = complex_schema

        runner = CliRunner()
        result = runner.invoke(
            write_clients_module,
            [str(template_dir), "--name", "clients.py.j2"]
        )

        # Verify integer mapping
        assert "limit: int = 10" in result.output

def test_build_clients_file_output(complex_schema, mock_client_template, tmp_path):
    """Verify the script writes to a specific file path."""
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    (template_dir / "clients.py.j2").write_text(mock_client_template)
    output_path = tmp_path / "output_clients.py"

    with patch("build_clients.get_schema") as mock_get:
        mock_get.return_value = complex_schema

        runner = CliRunner()
        runner.invoke(
            write_clients_module,
            [str(template_dir), "--name", "clients.py.j2", "--output", str(output_path)]
        )

        assert output_path.exists()
        assert "class MonitoringLocationsClient" in output_path.read_text()

def test_repr_logic_across_types(multi_type_schema, mock_client_template, tmp_path):
    """Verify different Python literals in the generated code."""
    # Setup template
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    template_file = template_dir / "clients.py.j2"
    template_file.write_text(mock_client_template)

    with patch("build_clients.get_schema") as mock_get:
        mock_get.return_value = multi_type_schema

        runner = CliRunner()
        result = runner.invoke(
            write_clients_module,
            [str(template_dir), "--name", "clients.py.j2"]
        )

        assert 'str_param: Optional[str] = "value"' in result.output
        assert "int_param: Optional[int] = 42" in result.output
        assert "bool_param: Optional[bool] = False" in result.output
        assert "none_param: Optional[str] = None" in result.output
