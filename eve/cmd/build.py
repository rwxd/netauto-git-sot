import typer
from pathlib import Path
from typing import List
import pytest
from eve.classifier import Classifier
from eve.jerakia import Jerakia
from eve.logging import logger
from eve.structure import get_hosts, get_system
from eve.builder.plugin import PytestPlugin

app = typer.Typer()


@app.command()
def configurations(
    limit: List[Path] = typer.Option(
        None,
        help='Path to limit building the configuration, can be specified multiple times',
    ),
    templates: Path = typer.Option(
        Path("templates"), help='Path to the templates directory'
    ),
    output: Path = typer.Option(Path("out"), help="Path for the output files"),
    cache: bool = typer.Option(False, help='Enable caching'),
    diff: bool = typer.Option(False, help='Produce diff'),
    skip_checks: bool = typer.Option(False),
    data: Path = typer.Option(Path("data"), help="Path to the data directory"),
    silent: bool = typer.Option(False),
    debug: bool = typer.Option(False),
):
    '''Build the device-specific configurations'''
    host_paths = get_hosts()

    if not limit:
        logger.info('No limit specified')
        targets = host_paths
    else:
        targets = []
        for item in limit:
            logger.info(f'Limit: {item}')
            for host in host_paths:
                if str(item) in str(host):
                    targets.append(host)

    logger.info(f'{len(targets)} hosts to build')

    classifier = Classifier()
    jerakia = Jerakia(classifier=classifier, datapath=data)

    process = pytest.main(
        args=['-p', 'no:cacheprovider'],
        plugins=[
            PytestPlugin(
                templates=templates,
                cache=cache,
                output=output,
                skip_checks=skip_checks,
                silent=silent,
                diff=diff,
                debug=debug,
                devices=host_paths,
                targets=targets,
                jerakia=jerakia,
                classifier=classifier,
            )
        ],
    )
    if process != 0:
        exit(1)

    # host_paths = get_hosts()
    # for path in host_paths:
    #     logger.info(path.name)
    #     searchpaths = get_searchpaths_for_host(path)
    #     for searchpath in searchpaths:
    #         logger.info(searchpath.name)
