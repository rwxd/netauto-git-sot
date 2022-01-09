import typer
from typing import List, Tuple
from eve.classifier import Classifier
from eve.searchpaths import get_searchpaths
from eve.structure import find_host_dir
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns

app = typer.Typer()
console = Console()


@app.command()
def device(device: str = typer.Argument(..., help='Device to get the scope for')):
    '''Get the scope of a device'''
    classifier = Classifier()
    host_path = find_host_dir(device)
    scope = classifier.scope(host_path)
    searchpaths = get_searchpaths(scope)

    scope_panel = '\n'.join(
        [
            f'[bold blue]{i[0]}[/bold blue]: {i[1]}'
            for i in get_key_strings_from_dict(scope)
        ]
    )
    console.print(Panel.fit(scope_panel, title='Scopes'))

    searchpaths_panel = '\n'.join([str(p) for p in searchpaths])
    console.print(
        Panel.fit(
            searchpaths_panel,
            title='Searchpaths',
            subtitle='[green]Paths are searched top down.[/green]',
        )
    )


def get_key_strings_from_dict(data: dict) -> List[Tuple[str, str]]:
    '''Get all key strings from a dict recursively.
    `{"a": {"b": {"c": "d"}}}` -> `[("c", "d")]`
    '''
    keys = []
    for k, v in data.items():
        if type(v) == dict:
            keys += get_key_strings_from_dict(v)
        if type(v) == list:
            for item in v:
                if type(item) == dict:
                    keys += get_key_strings_from_dict(item)
                if type(v) == str:
                    keys.append((k, v))
        if type(v) == str:
            keys.append((k, v))
    return keys
