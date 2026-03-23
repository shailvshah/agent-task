import typer
import json
import yaml
from pathlib import Path
from pydantic import ValidationError
from rich import print as rprint

from .models import AgentTask

app = typer.Typer()

@app.command()
def init():
    """Scaffold a new agent.task file"""
    rprint("Scaffolding not yet implemented.")

@app.command()
def validate(file: str, is_json: bool = typer.Option(False, "--json")):
    """Validate an agent.task file against the strongly-typed extensible schema."""
    path = Path(file)
    if not path.exists():
        rprint(f"[bold red]Error:[/bold red] File not found: {file}")
        raise typer.Exit(code=1)
        
    try:
        with open(path, "r") as f:
            if path.suffix in [".yaml", ".yml", ".task"]:
                data = yaml.safe_load(f)
            else:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    f.seek(0)
                    data = yaml.safe_load(f)
                
        # The true validation backbone executes here
        task = AgentTask.model_validate(data)
        
        if is_json:
            # Produce byte-identical structured output
            out_dict = task.model_dump(by_alias=True, exclude_none=True)
            print(json.dumps(out_dict, sort_keys=True))
        else:
            rprint(f"[bold green]✓ Validated[/bold green] {file} [dim](Task ID: {task.meta.id})[/dim]")
            
    except ValidationError as e:
        if is_json:
            print(json.dumps({"error": "validation_error", "details": e.errors()}, sort_keys=True))
        else:
            rprint("[bold red]Validation Failed:[/bold red]")
            for err in e.errors():
                loc = " -> ".join(map(str, err["loc"]))
                rprint(f"  [yellow]{loc}[/yellow]: {err['msg']}")
        raise typer.Exit(code=1)
    except Exception as e:
        rprint(f"[bold red]Error processing file:[/bold red] {e}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
