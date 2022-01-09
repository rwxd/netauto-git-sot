import typer
from eve.validation.schema import validate_schemas
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def schemas():
    '''Validate the configuration files against the JSON schemas'''
    if validate_schemas():
        console.print(f'[green]All schemas are valid[/green]')
    else:
        exit(1)
