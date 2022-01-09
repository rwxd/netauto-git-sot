from os import scandir
import typer
from pathlib import Path
import eve.cmd.validate
import eve.cmd.build
import eve.cmd.scope

app = typer.Typer()


app.add_typer(
    eve.cmd.validate.app, name='validate', help='Validate files & configurations'
)
app.add_typer(eve.cmd.build.app, name='build', help='Build from files')
app.add_typer(eve.cmd.scope.app, name='scope', help='Get scopes')


@app.callback(invoke_without_command=True)
def main():
    pass
