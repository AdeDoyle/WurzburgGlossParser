# coding=utf8
"""Level 4"""

from GetSections import get_section, get_pages
from GetPageInfo import get_pageinfo
from OrderFootnotes import order_footlist
from OrderGlosses import order_glosslist
import re
from ClearTags import clear_spectags
from SaveDocx import save_docx


def scribe_split(glossfile, startpage=499, stoppage=712):
    """Takes the text of the glosses, identifies page number, gloss text and footnotes,
       Separates the three scribal hands first by identifying prima manus footnotes throughout whole text
       then by breaking the remaining glosses of f.32d from f.33a"""
    # get a list of pages and page numbers from the file, and isolate the irish gloss text ... and footnotes
    pagesinfolist = get_pageinfo(glossfile, startpage, stoppage)
    pagesdir = []
    for page in pagesinfolist:
        pageno = page[0]
        irish = get_section(get_pages(glossfile, pageno, pageno), "SG")
        irish = irish[0]
        pagedir = [pageno, irish]
        pagesdir.append(pagedir)
    # get the individual glosses per page, check if they have a 'prima manus' footnote, if so, put in PM list
    allglosses = ['All Glosses']
    primanlist = ['Prima Manus']
    handiilist = ['Hand Two']
    handiiilist = ['Hand Three']
    # glosscount = 0
    # pmcount = 0
    # htwocount = 0
    # hthreecount = 0
    # adds all glosses to a single list
    for page in pagesdir:
        glosslist = order_glosslist(page[1])
        for curgloss in glosslist:
            allglosses.append(curgloss)
            # glosscount += 1
    # adds prima manus glosses to a proma manus list
    for page in pagesdir:
        glosslist = order_glosslist(page[1])
        footnotes = order_footlist(glossfile, page[0])
        for curgloss in glosslist:
            # find footnote markers in each individual gloss
            glossfnpat = re.compile(r'\[[a-z]\]')
            glossfnitir = glossfnpat.finditer(curgloss)
            for i in glossfnitir:
                let = i.group()
                let = let[1:-1]
                for fn in footnotes:
                    # Find footnote associated with gloss, then if it indicates a prima manu add gloss to prima list
                    if fn[0] == let:
                        if "prima" in fn:
                            if curgloss not in primanlist:
                                primanlist.append(curgloss)
                                # pmcount += 1
    # adds remaining glosses to separate lists for hands 2 and 3
    handtwo = True
    for page in pagesdir:
        glosslist = order_glosslist(page[1])
        for curgloss in glosslist:
            # iterate through the remaining glosses, remove prima glosses, divide rest into hand 2 or hand 3 list
            if "[f. 33a]" in curgloss:
                handtwo = False
            if handtwo:
                if curgloss not in primanlist:
                    handiilist.append(curgloss)
                    # htwocount += 1
            else:
                if curgloss not in primanlist:
                    handiiilist.append(curgloss)
                    # hthreecount += 1
    handlists = [allglosses, primanlist, handiilist, handiiilist]
    # print("Full Count: %d\nH1: %d\nH2: %d\nH3: %d" % (glosscount, pmcount, htwocount, hthreecount))
    return handlists


# glosses = "Wurzburg Glosses"

# print(scribe_split(glosses, 499, 712))
# for i in scribe_split(glosses, 499, 712):
#     print(i)

# for scribe in scribe_split(glosses, 499, 712):
#     contentlist = scribe[1:]
#     content = "\n".join(contentlist)
#     clearcont = clear_spectags(content, "fol")
#     save_docx(clearcont, "Wb. " + scribe[0])
