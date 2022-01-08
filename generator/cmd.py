import typer
from pathlib import Path
from generator.models.device_configuration import JsonSchemaForNetworkConfiguration
from generator.validation import validate_device_config
from generator.generate import generate_device_configuration
from generator.structure import load_repository_structure
from yaml import safe_load

app = typer.Typer()


@app.command()
def validate_config(config_path: Path = typer.Argument(..., exists=True)):
    validate_device_config(config_path)
    typer.echo(f'{config_path} is valid')


@app.command()
def generate_config(
    input: Path = typer.Argument(..., exists=True),
    output: str = typer.Argument(..., exists=True),
):
    validate_device_config(input)
    with open(input, 'r') as f:
        parsed = JsonSchemaForNetworkConfiguration.parse_obj(safe_load(f))
    config = generate_device_configuration(parsed)
    with open(output, 'w') as f:
        f.write('\n'.join(config))


@app.command()
def repository_structure(
    repository_path: Path = typer.Argument(..., exists=True),
    output: str = typer.Argument(..., exists=True),
):
    repository = load_repository_structure(repository_path)
    with open(output, 'w') as f:
        f.write(repository.json())
