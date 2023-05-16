import click
from tapita import Cover


@click.command()
@click.option("-t", "--title", metavar="<title>", help="Book title")
@click.option(
    "-s", "--subtitle", metavar="<subtitle>", help="Book subtitle", default=None
)
@click.option("-a", "--author", metavar="<author>", help="Book author", default=None)
@click.option("-o", "--output", metavar="<filename>", help="Output file (- for stdout)")
def cover(title, author, output, subtitle):
    cover = Cover(title, subtitle, author)
    cover.cover_image.save(output)


if __name__ == "__main__":
    cover()
