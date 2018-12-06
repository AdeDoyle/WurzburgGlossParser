"""Level 1"""

from ClearTags import clear_tags
from GetSections import get_section
from OpenPages import get_pages
import re


def order_latlist_page(file):
    """Takes a single page of Latin text. Orders the text by removing any new lines where no new numbers are marked.
    Returns a list of ordered lines for the page."""
    latext = file
    latitirs = []
    theselines = []
    brokenlinepat = re.compile(r'(\[/?f\. \d[a-d]\])?\D.+(\n)?(.*\n)?(\d{1,2}[a-z]?, )?\d{1,2}[a-z]?\. ')
    brokenlineitir = brokenlinepat.finditer(latext)
    for i in brokenlineitir:
        brokelattext = i.group()
        if latext.find(brokelattext) == 0:
            brokelattext = brokelattext[:brokelattext.rfind("\n")]
            brokelattext = " ".join(brokelattext.split("\n"))
            theselines.append(brokelattext)
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
    if theselines[1] in theselines[0]:
        del theselines[0]
    elif theselines[0] in theselines[1]:
        del theselines[0]
    return theselines


def order_latlist(file):
    """Takes multiple pages of latin text where pages are separated by a double space ("\n\n").
       Returns a list of ordered lines for the entire file."""
    pages = file.split("\n\n")
    orderedpageslist = []
    for page in pages:
        orderedglosses = order_latlist_page(page)
        orderedpageslist.append(orderedglosses)
    orderedpages = []
    for orderedpage in orderedpageslist:
        for orderedgloss in orderedpage:
            orderedpages.append(orderedgloss)
    return orderedpages


def order_latin(file):
    """Takes multiple pages of latin text where pages are separated by a double space ("\n\n").
       Returns a single string of ordered lines for the entire file."""
    latlist = order_latlist(file)
    linesstring = "\n".join(latlist)
    return linesstring


# latin = clear_tags("\n\n".join(get_section(get_pages("Wurzburg Glosses", 499, 509), "Lat")))
# latin = "\n\n".join(get_section(get_pages("Wurzburg Glosses", 499, 509), "Lat"))
# print(order_latlist(latin))
# print(order_latin(latin))
