import click
from click.testing import CliRunner

@click.group()
def cli():
    pass


@cli.command()
@click.option("--count", prompt='count', help='greeting times')
@click.option("--name", default="anny", help="the person you greeting")
def greet(count, name, env):
    for _ in range(int(count)):
        print(f"Hello {name} {env}!")


@cli.command()
@click.option('--name', prompt='Your name', help='Name to goodbye.')
def goodbye(name):
    """Say goodbye."""
    click.echo(f"Goodbye, {name}!")




def test_greet():
    runner = CliRunner()
    result = runner.invoke(greet, ['--name', 'Alice', '--count', '2'])
    assert result.exit_code == 0
    assert result.output == 'Hello Alice!\nHello Alice!\n'

if __name__ == '__main__':
    greet()