"""Level 3"""

from GetSections import get_section
from OpenPages import get_pages


def order_footnotes(file, page):
    """Prints footnotes for a selected page as a single string"""
    footnotes = "\n\n".join(get_section(get_pages(file, page, page), "FN"))
    return footnotes


def order_footlist(file, page):
    """Returns footnotes for a selected page as a list"""
    footnotes = order_footnotes(file, page)
    footlist = footnotes.split("\n")
    return footlist


# print(order_footnotes("Wurzburg Glosses", 500))
# print(order_footlist("Wurzburg Glosses", 500))
# for i in order_footlist("Wurzburg Glosses", 500):
#     print(i)