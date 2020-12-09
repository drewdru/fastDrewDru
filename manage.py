import os
from pathlib import Path

import click
import massedit
import uvicorn
from dotenv import load_dotenv

from fastdrewdru import config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
project_name = "fastdrewdru"


@click.group()
def cli():
    pass


@click.command()
@click.argument("microservice_name")
def createapp(microservice_name):
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
        with open(f"{microservice_name}/tests.py", "w") as io_file:
            io_file.write("# Create your tests here.\n")
        Path(f"{microservice_name}/models").mkdir()
        with open(f"{microservice_name}/models/__init__.py", "w") as io_file:
            io_file.write(
                "__all__ = []\n"
                "# Don't modify the line above, or this line!\n"
                "import automodinit\n"
                "automodinit.automodinit(__name__, __file__, globals())\n"
                "del automodinit\n"
                "# Anything else you want can go after here, "
                "it won't get modified.\n"
            )
        with open(f"{microservice_name}/models/models.py", "w") as io_file:
            io_file.write("# Create your SqlAlchemy models here.\n")

        add_app_to_settings = (
            "re.sub(r'APPS: List\\[str] = \\[',"
            f"""'APPS: List[str] = ["{microservice_name}",', line)"""
        )
        massedit.edit_files(
            [f"./{project_name}/config.py"], [add_app_to_settings], dry_run=False
        )
        print(
            f'{microservice_name} has been created and APPS in "config.py"',
            "has been updated.",
        )
    except FileExistsError:
        print(f"{microservice_name} alredy exist")


@click.command(
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
        allow_interspersed_args=True,
    )
)
@click.pass_context
@click.option("--prod/--no-prod", default=False)
@click.option("--docker/--no-docker", default=False)
def migrations(ctx: click.Context, prod: bool, docker: bool, *args, **kwargs) -> None:
    alembic_command = "alembic"
    if prod:
        alembic_command = "ENV=prod alembic"
    elif docker:
        alembic_command = "ENV=docker alembic"

    is_need_quotes = False
    for arg in ctx.args:
        if is_need_quotes:
            alembic_command = f'{alembic_command} "{arg}"'
            is_need_quotes = False
        else:
            alembic_command = f"{alembic_command} {arg}"
            if arg == "-m":
                is_need_quotes = True
    os.system(alembic_command)


@click.command()
@click.option("--prod/--no-prod", default=False)
@click.option("--docker/--no-docker", default=False)
def run(prod: bool, docker: bool) -> None:
    env_file = ".env"
    if prod:
        env_file = ".env.prod"
    if docker:
        env_file = ".env.docker"

    load_dotenv(env_file, override=True)
    settings = config.get_settings()
    # cli.add_command(uvicorn.main, name="uvicorn")
    if prod:
        uvicorn.run(
            "main:app",
            host=settings.HOST,
            port=settings.PORT,
            debug=settings.DEBUG,
            reload=True,
            env_file=env_file,
        )
    else:
        uvicorn.run(
            "main:app",
            host=settings.HOST,
            port=settings.PORT,
            debug=settings.DEBUG,
            env_file=env_file,
        )


@click.command(
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
        allow_interspersed_args=True,
    )
)
@click.pass_context
def test(ctx: click.Context, *args, **kwargs) -> None:
    ENV = "ENV=test"
    os.system(f"{ENV} alembic upgrade head")
    ctx_args = " ".join(ctx.args)
    exit_status = os.system(f"{ENV} pytest {ctx_args}")
    os.system(f"{ENV} alembic downgrade base")
    exit(exit_status)


cli.add_command(createapp)
cli.add_command(migrations)
cli.add_command(run)
cli.add_command(test)

if __name__ == "__main__":
    cli()
