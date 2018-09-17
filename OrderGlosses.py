"""Level 1"""

from ClearTags import clear_tags
from GetSections import get_section
from OpenPages import get_pages
import re


def order_glosses(file):
    """Finds each gloss by its number (and folio info where applicable)
       and returns a string with each gloss on a new line"""
    glosstext = file
    theseglosses = []

    glossitirs = []

    folglosspat = re.compile(r'(\[/?f\. \d[a-d]\])?(\d{1,2}, )?\d{1,2}\. ')
    glossitir = folglosspat.finditer(glosstext)
    for i in glossitir:
        glossitirs.append(i.start())
    for i in glossitirs:
        if i == glossitirs[0]:
            startpoint = i
        elif i == glossitirs[-1]:
            endpoint = i
            thisgloss = glosstext[startpoint:endpoint]
            thisgloss = thisgloss.strip()
            if "\n" in thisgloss:
                thisglosslist = thisgloss.split("\n")
                thisgloss = " ".join(thisglosslist)
            theseglosses.append(thisgloss)
            startpoint = endpoint
            lastgloss = glosstext[startpoint:]
            lastgloss = lastgloss.strip()
            if "\n" in lastgloss:
                lastglosslist = lastgloss.split("\n")
                lastgloss = " ".join(lastglosslist)
            theseglosses.append(lastgloss)
        else:
            endpoint = i
            thisgloss = glosstext[startpoint:endpoint]
            thisgloss = thisgloss.strip()
            if "\n" in thisgloss:
                thisglosslist = thisgloss.split("\n")
                thisgloss = " ".join(thisglosslist)
            theseglosses.append(thisgloss)
            startpoint = endpoint
    glossesstring = "\n".join(theseglosses)
    return glossesstring


# glosses = clear_tags("\n\n".join(get_section(get_pages("Wurzburg Glosses", 499, 509), "SG")))
# glosses = "\n\n".join(get_section(get_pages("Wurzburg Glosses", 499, 712), "SG"))
# print(order_glosses(glosses))
