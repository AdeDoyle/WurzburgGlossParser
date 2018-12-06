"""Level 3"""

from GetSections import get_section, get_pages


def testsectext(sec, startpage, stoppage):
    """Takes a desired section and page range as input.
       Outputs a list of lists of page no. and page content."""
    pagesinfolist = []
    for page in range(startpage, stoppage + 1):
        pageinfolist = [str(page), "\n\n".join(get_section(get_pages("Wurzburg Glosses", page, page), sec))]
        pagesinfolist.append(pageinfolist)
    return pagesinfolist


# sections = testsectext("Lat", 499, 712)
# sections = testsectext("SG", 499, 712)
# sections = testsectext("Eng", 499, 712)
# sections = testsectext("FN", 499, 712)
# for pagelist in sections:
#     print(pagelist[0])
#     print(pagelist[1])
#     print("")
