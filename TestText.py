"""Level 3, 1"""

from GetSections import get_section, get_pages
import re


def testsectext(sec, startpage, stoppage):
    """Takes a desired section and page range as input.
       Outputs a list of lists of page no. and page content."""
    pagesinfolist = []
    for page in range(startpage, stoppage + 1):
        pageinfolist = [str(page), "\n\n".join(get_section(get_pages("Wurzburg Glosses", page, page), sec))]
        pagesinfolist.append(pageinfolist)
    return pagesinfolist


def testlatnums(text):
    """Searches for number patterns within a text which do not match expected numbering or superscript patterns"""
    numlist = []
    numpat = re.compile(r'\d[^.\]\da-z]')
    numpatitir = numpat.finditer(text)
    for i in numpatitir:
        find = i.group()
        if find not in numlist:
            numlist.append(find)
    numpat = re.compile(r'[^\[\]\d\s]\d\. ')
    numpatitir = numpat.finditer(text)
    for i in numpatitir:
        find = i.group()
        if find not in numlist:
            numlist.append(find)
    numpat = re.compile(r'\d\.[^\s]')
    numpatitir = numpat.finditer(text)
    for i in numpatitir:
        find = i.group()
        if find not in numlist:
            numlist.append(find)
    return numlist


# Select a section
# sections = testsectext("Lat", 499, 712)
# sections = testsectext("SG", 499, 712)
# sections = testsectext("Eng", 499, 712)
# sections = testsectext("FN", 499, 712)


# # Print an ordered list of all characters in a given section
# ordstr = ""
# for pagelist in sections:
#     ordstr += pagelist[1]
# print(sorted(list(set(ordstr))))


# # Print everything in a given section with page numbers above
# for pagelist in sections:
#     print(pagelist[0])
#     print(pagelist[1])
#     print("")


# # Find everything between given tags in a given
# sections_compiled = ""
# for pagelist in sections:
#     sections_compiled += "{}\n{}\n\n".format(pagelist[0], pagelist[1])
# secpat = re.compile(r'\[GLat\][\w \.\n:(\[\d\])(\[/\d\])(\[Con\])(\[/Con\])]*\[/GLat\]')
# secpatitir = secpat.finditer(sections_compiled)
# for i in secpatitir:
#     print(i.group() + "\n")


# # Calls the testlatnums function above then sorts and prints all potential/apparent failures
# lattext = "\n\n".join(get_section(get_pages("Wurzburg Glosses", 499, 712), "Lat"))
# for fail in sorted(list(set(testlatnums(lattext)))):
#     print(fail)
