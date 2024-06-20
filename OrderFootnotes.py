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
    """Prints new site-notes for a selected page as a single string"""
    newnotes = "\n\n".join(get_section(get_pages(file, page, page), "AN"))
    return newnotes


@lru_cache(maxsize=250)
def order_newlist(file, page):
    """Returns new site-notes for a selected page as a list"""
    newnotes = order_newnotes(file, page)
    newlist = newnotes.split("\n")
    return newlist


@lru_cache(maxsize=250)
def order_newglosses(file, page):
    """Prints alternative gloss readings for a selected page as a single string"""
    newglosses = "\n\n".join(get_section(get_pages(file, page, page), "NG"))
    return newglosses


@lru_cache(maxsize=250)
def order_newglosslist(file, page):
    """Returns alternative gloss readings for a selected page as a list"""
    newglosses = order_newglosses(file, page)
    newglosslist = newglosses.split("\n")
    return newglosslist


@lru_cache(maxsize=250)
def order_newtrans(file, page):
    """Prints new translations for a selected page as a single string"""
    newtrans = "\n\n".join(get_section(get_pages(file, page, page), "NT"))
    return newtrans


@lru_cache(maxsize=250)
def order_newtranslist(file, page):
    """Returns new translations for a selected page as a list"""
    newtrans = order_newtrans(file, page)
    newtranslist = newtrans.split("\n")
    return newtranslist


# if __name__ == "__main__":
#
#     print(order_footnotes("Wurzburg Glosses", 500))
#     print(order_footlist("Wurzburg Glosses", 500))
#     for i in order_footlist("Wurzburg Glosses", 500):
#         print(i)
#
#     print(order_newnotes("Wurzburg Glosses", 625))
#     print(order_newlist("Wurzburg Glosses", 625))
#     for i in order_newlist("Wurzburg Glosses", 625):
#         print(i)
#
#     print(order_newglosses("Wurzburg Glosses", 568))
#     print(order_newglosslist("Wurzburg Glosses", 568))
#     for i in order_newglosslist("Wurzburg Glosses", 568):
#         print(i)
#
#     print(order_newtrans("Wurzburg Glosses", 568))
#     print(order_newtranslist("Wurzburg Glosses", 568))
#     for i in order_newtranslist("Wurzburg Glosses", 568):
#         print(i)
