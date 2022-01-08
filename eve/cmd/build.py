import typer
from pathlib import Path
from eve.logging import logger

app = typer.Typer()


@app.command()
def configurations(
    limit: Path = typer.Option(None, help='Path to limit building the configuraiton')
):
    if not limit:
        logger.info('No limit specified')
    else:
        logger.debug(f'Limit: {limit}')
