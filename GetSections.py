"""Level 3."""

from OpenPages import get_pages


def get_section(filename, startpage=499, endpage=712):
    fulltext = get_pages(filename, startpage, endpage)
    print(fulltext)


get_section("Wurzburg Glosses")
