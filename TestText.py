"""Level 3"""

from GetSections import get_section, get_pages


def testsectext(sec, startpage, stoppage):
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
