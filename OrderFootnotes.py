"""Level 3"""

from functools import lru_cache
from GetSections import get_section
from OpenPages import get_pages


@lru_cache(maxsize=250)
def order_footnotes(file, page):
    """Prints footnotes for a selected page as a single string"""
    footnotes = "\n\n".join(get_section(get_pages(file, page, page), "FN"))
    return footnotes


@lru_cache(maxsize=250)
def order_footlist(file, page):
    """Returns footnotes for a selected page as a list"""
    footnotes = order_footnotes(file, page)
    footlist = footnotes.split("\n")
    return footlist


@lru_cache(maxsize=250)
def order_newnotes(file, page):
    """Prints footnotes for a selected page as a single string"""
    newnotes = "\n\n".join(get_section(get_pages(file, page, page), "AN"))
    return newnotes


@lru_cache(maxsize=250)
def order_newlist(file, page):
    """Returns footnotes for a selected page as a list"""
    newnotes = order_newnotes(file, page)
    newlist = newnotes.split("\n")
    return newlist


# print(order_footnotes("Wurzburg Glosses", 500))
# print(order_footlist("Wurzburg Glosses", 500))
# for i in order_footlist("Wurzburg Glosses", 500):
#     print(i)

# print(order_newnotes("Wurzburg Glosses", 705))
# print(order_newlist("Wurzburg Glosses", 705))
# for i in order_newlist("Wurzburg Glosses", 705):
#     print(i)
