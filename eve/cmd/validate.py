import typer
from eve.validation.schema import validate_schemas

app = typer.Typer()


@app.command(help='Validate the configuration files against the JSON schemas')
def schemas():
    validate_schemas()
    typer.echo(f'All schemes are valid')
