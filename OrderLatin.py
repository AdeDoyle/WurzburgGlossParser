"""Level 1"""

from ClearTags import clear_tags
from GetSections import get_section
from OpenPages import get_pages
import re


def order_latin(file):
    latext = file
    latitirs = []
    theselines = []
    linepat = re.compile(r'(\[/?f\. \d[a-d]\])?(Rom\. )?(Corintii .*)?(Scribens .*)?(Explicit .*)?(Incipit .*)?'
                         r'([IVX]{1,4}\. )?(\d{1,2}[a-z]?, )?\d{1,2}[a-z]?\. ')
    lineitir = linepat.finditer(latext)
    for i in lineitir:
        latitirs.append(i.start())
    for i in latitirs:
        if i == latitirs[0]:
            startpoint = i
        elif i == latitirs[-1]:
            endpoint = i
            thisline = latext[startpoint:endpoint]
            thisline = thisline.strip()
            if "\n" in thisline:
                thislinelist = thisline.split("\n")
                thisline = " ".join(thislinelist)
            theselines.append(thisline)
            startpoint = endpoint
            lastline = latext[startpoint:]
            lastline = lastline.strip()
            if "\n" in lastline:
                lastlinelist = lastline.split("\n")
                lastline = " ".join(lastlinelist)
            theselines.append(lastline)
        else:
            endpoint = i
            thisline = latext[startpoint:endpoint]
            thisline = thisline.strip()
            if "\n" in thisline:
                thislinelist = thisline.split("\n")
                thisline = " ".join(thislinelist)
            theselines.append(thisline)
            startpoint = endpoint
    linesstring = "\n".join(theselines)
    return linesstring


# glosses = clear_tags("\n\n".join(get_section(get_pages("Wurzburg Glosses", 499, 503), "Lat")))
# glosses = "\n\n".join(get_section(get_pages("Wurzburg Glosses", 499, 503), "Lat"))
# print(order_latin(glosses))
