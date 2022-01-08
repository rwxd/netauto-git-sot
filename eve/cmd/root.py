import typer
from pathlib import Path
import eve.cmd.validate
import eve.cmd.build

app = typer.Typer()
app.add_typer(eve.cmd.validate.app, name='validate')
app.add_typer(eve.cmd.build.app, name='build')


@app.command()
def build(limit: Path = typer.Option(False, help='File or directory to limit build')):
    pass


# @app.command()
# def generate_config(
#     input: Path = typer.Argument(..., exists=True),
#     output: str = typer.Argument(..., exists=True),
# ):
#     validate_device_config(input)
#     with open(input, 'r') as f:
#         parsed = JsonSchemaForNetworkConfiguration.parse_obj(safe_load(f))
#     config = generate_device_configuration(parsed)
#     with open(output, 'w') as f:
#         f.write('\n'.join(config))


# @app.command()
# def repository_structure(
#     repository_path: Path = typer.Argument(..., exists=True),
#     output: str = typer.Argument(..., exists=True),
# ):
#     repository = load_repository_structure(repository_path)
#     with open(output, 'w') as f:
#         f.write(repository.json())
