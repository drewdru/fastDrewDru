import os
from pathlib import Path

import click
import massedit

from fastDrewDru.config import get_settings

project_name = "fastDrewDru"
settings = get_settings()


@click.group()
def cli():
    pass


@click.command()
@click.argument("microservice_name")
def initapp(microservice_name):
    try:
        Path(microservice_name).mkdir()
        with open(f"{microservice_name}/__init__.py", "w") as io_file:
            io_file.write("# Init your app.\n")
        with open(f"{microservice_name}/crud.py", "w") as io_file:
            io_file.write("# Create your CRUD methods here.\n")
        with open(f"{microservice_name}/schemas.py", "w") as io_file:
            io_file.write("# Create your pydantic schemas here.\n")
        with open(f"{microservice_name}/views.py", "w") as io_file:
            io_file.write("# Create your endpoints here.\n")
        Path(f"{microservice_name}/models").mkdir()
        with open(f"{microservice_name}/models/__init__.py", "w") as io_file:
            io_file.write(
                "__all__ = []\n"
                "# Don't modify the line above, or this line!\n"
                "import automodinit\n"
                "automodinit.automodinit(__name__, __file__, globals())\n"
                "del automodinit\n"
                "# Anything else you want can go after here, it won't get modified.\n"
            )
        with open(f"{microservice_name}/models/models.py", "w") as io_file:
            io_file.write("# Create your SqlAlchemy models here.\n")

        add_app_to_settings = f"""re.sub(r'APPS: List\\[str] = \\[', 'APPS: List[str] = ["{
            microservice_name
        }",', line)"""
        massedit.edit_files([f"./{project_name}/config.py"], [add_app_to_settings], dry_run=False)
        print(f"""{microservice_name} has been created and APPS in "config.py" has been updated.""")
    except FileExistsError:
        print(f"{microservice_name} alredy exist")


@click.command(
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    )
)
@click.pass_context
def migrations(ctx: click.Context, *args, **kwargs) -> None:
    os.system(f'alembic {" ".join(ctx.args)}')


cli.add_command(initapp)
cli.add_command(migrations)

if __name__ == "__main__":
    cli()
