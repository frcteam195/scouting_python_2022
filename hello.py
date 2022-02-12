
from unicodedata import name
import click
@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='The person you Love',
              help='The person to love.')

def hello(count, name):
    for x in range(count):
        if name == "Harish":
            click.echo("I love Harish!")
        elif name == "Joe":
            click.echo("I love Joe but also Harish")

if __name__ == '__main__':
        hello()


