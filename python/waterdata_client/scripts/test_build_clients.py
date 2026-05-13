"""Tests for the build_clients stand-alone script."""
import pytest
from unittest.mock import patch
from click.testing import CliRunner
from typing import Any
from build_clients import write_clients_module

@pytest.fixture
def mock_client_template() -> str:
    """Mock client template that mimics the production Jinja2 structure."""
    return """
class {{ item.class_name }}(BaseClient):
    \"\"\"{{ item.description }}\"\"\"
    _endpoint = USGSCollection.{{ item.enum_member }}

    def get(self, 
        {% for p in item.parameters %}
        {{ p.python_name }}: {{ p.type_hint }} = {{ p.default }},
        {% endfor %}
    ):
        query = {
            {% for p in item.parameters %}
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
    init_template_file = template_dir / "clients_init.py.j2"
    template_file.write_text(mock_client_template)
    init_template_file.touch()

    # Setup output directory
    output_dir = tmp_path / "generated_clients"

    with patch("build_clients.get_schema") as mock_get:
        mock_get.return_value = complex_schema

        runner = CliRunner()
        result = runner.invoke(
            write_clients_module,
            [str(template_dir), "--name", "clients.py.j2", "--output", str(output_dir)]
        )

        generated_path = output_dir / "monitoring_locations.py"
        generated_content = generated_path.read_text()

        assert result.exit_code == 0
        assert "bbox_crs: Optional[str] = \"EPSG:4326\"" in generated_content
        assert "\"bbox-crs\": bbox_crs" in generated_content

def test_client_generation_type_hints(complex_schema, mock_client_template, tmp_path):
    """Verify JSON type to Python type hint mapping."""
    # Setup template
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    template_file = template_dir / "clients.py.j2"
    init_template_file = template_dir / "clients_init.py.j2"
    template_file.write_text(mock_client_template)
    init_template_file.touch()

    # Setup output directory
    output_dir = tmp_path / "generated_clients"

    with patch("build_clients.get_schema") as mock_get:
        mock_get.return_value = complex_schema

        runner = CliRunner()
        result = runner.invoke(
            write_clients_module,
            [str(template_dir), "--name", "clients.py.j2", "--output", str(output_dir)]
        )

        generated_path = output_dir / "monitoring_locations.py"
        generated_content = generated_path.read_text()

        # Verify integer mapping
        assert result.exit_code == 0
        assert "limit: int = 10" in generated_content

def test_build_clients_file_output(complex_schema, mock_client_template, tmp_path):
    """Verify the script writes to a specific file path."""
    # Setup template
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    template_file = template_dir / "clients.py.j2"
    init_template_file = template_dir / "clients_init.py.j2"
    template_file.write_text(mock_client_template)
    init_template_file.touch()

    # Setup output directory
    output_dir = tmp_path / "generated_clients"

    with patch("build_clients.get_schema") as mock_get:
        mock_get.return_value = complex_schema

        runner = CliRunner()
        result = runner.invoke(
            write_clients_module,
            [str(template_dir), "--name", "clients.py.j2", "--output", str(output_dir)]
        )

        generated_path = output_dir / "monitoring_locations.py"
        generated_content = generated_path.read_text()

        assert result.exit_code == 0
        assert output_dir.exists()
        assert "class MonitoringLocationsClient" in generated_content

def test_repr_logic_across_types(multi_type_schema, mock_client_template, tmp_path):
    """Verify different Python literals in the generated code."""
    # Setup template
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    template_file = template_dir / "clients.py.j2"
    init_template_file = template_dir / "clients_init.py.j2"
    template_file.write_text(mock_client_template)
    init_template_file.touch()

    # Setup output directory
    output_dir = tmp_path / "generated_clients"

    with patch("build_clients.get_schema") as mock_get:
        mock_get.return_value = multi_type_schema

        runner = CliRunner()
        result = runner.invoke(
            write_clients_module,
            [str(template_dir), "--name", "clients.py.j2", "--output", str(output_dir)]
        )

        generated_path = output_dir / "types.py"
        generated_content = generated_path.read_text()

        assert result.exit_code == 0
        assert 'str_param: Optional[str] = "value"' in generated_content
        assert "int_param: Optional[int] = 42" in generated_content
        assert "bool_param: Optional[bool] = False" in generated_content
        assert "none_param: Optional[str] = None" in generated_content
