import click


@click.group(short_help="pslandak CLI.")
def pslandak():
    """pslandak CLI.
    """
    pass


@pslandak.command()
@click.argument("name", default="pslandak")
def command(name):
    """Docs.
    """
    click.echo("Hello, {name}!".format(name=name))


def get_commands():
    return [pslandak]
