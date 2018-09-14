"""Level 1."""

from OpenPages import get_pages


def get_section(fulltext, section="No Section"):
    """Gets and returns just the text between a particular set of section tags"""
    return fulltext


glosses = get_pages("Wurzburg Glosses", 499, 499)
print(get_section(glosses))
