import textwrap


def dedent(text: str) -> str:
    return textwrap.dedent(text.lstrip('\n'))


def reindent(prefix: str, text: str) -> str:
    return textwrap.indent(dedent(text), prefix)
