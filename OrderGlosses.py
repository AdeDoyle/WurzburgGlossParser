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
    folglosspat = re.compile(r'(\[/?f\. \d[a-d]\])?(\d{1,2}, )?\d{1,2}\. ')
    for i in folglosspat.finditer(glosstext):
        patfound = i[0]
        glosstext = glosstext[glosstext.find(patfound):]
        patlen = len(patfound)
        disctext = glosstext[patlen:]
        nextpat = folglosspat.search(disctext)
        if nextpat is None:
            thisgloss = glosstext
        else:
            nextpat = nextpat[0]
            thisgloss = glosstext[:glosstext.find(nextpat)]
        if "\n" in thisgloss:
            thisglosslist = thisgloss.split("\n")
            thisgloss = "".join(thisglosslist)
        thisgloss = thisgloss.strip()
        theseglosses.append(thisgloss)
    glossesstring = "\n".join(theseglosses)
    return glossesstring


# glosses = clear_tags("\n\n".join(get_section(get_pages("Wurzburg Glosses", 499, 509), "SG")))
# # Using the above variable for glosses with order_glosses instead of clearing the tags afterwards as below
# # deletes two glosses at the end of f. 1d and beginning of f. 2a.

# glosses = "\n\n".join(get_section(get_pages("Wurzburg Glosses", 499, 509), "SG"))
# print(order_glosses(glosses))
# print(clear_tags(order_glosses(glosses)))
