"""Level 3"""
"""DISUSED!"""

from GetTagText import get_tagtext
from OpenPages import get_pages
from GetSections import get_section
from OrderGlosses import order_glosses, order_glosslist
from ClearTags import clear_tags
from GetFolio import get_fol
import re


def get_glinfobasic(file, startpage=499, stoppage=712):
    """Returns an infolist containing multiple sublists. The first sublist contains the headers for an info-table.
       Subsequent lists contain, respectively, for a set page range: Epistle, Page No., Folio, Gloss no. and tag-free
       Gloss Text for every gloss in Wb."""
    curepist = "Unknown"
    infolist = [["Epistle", "Page", "Folio", "Gloss No.", "Gloss Text"]]
    for page in range(startpage, stoppage + 1):
        thispage = page
        pagetext = get_pages(file, thispage, thispage)
        epfunc = get_tagtext(pagetext, "H2")
        if epfunc:
            curepist = epfunc[0]
        glosslist = order_glosslist(clear_tags("\n\n".join(get_section(pagetext, "SG"))))
        foliolist = []
        for folinfo in get_fol(order_glosses(clear_tags("\n\n".join(get_section(get_pages(
                file, thispage, thispage), "SG")), "fol"))):
            folio = folinfo[1]
            foliotext = folinfo[0]
            foliolist.append([folio, foliotext])
        for gloss in glosslist:
            thisglosslist = [curepist, thispage]
            glossfound = False
            for foltextlist in foliolist:
                if gloss in foltextlist[1]:
                    thisfolio = foltextlist[0]
                    thisglosslist.append(thisfolio)
                    glossfound = True
            if not glossfound:
                glossstub = gloss[:11]
                for foltextlist in foliolist:
                    if glossstub in foltextlist[1]:
                        thisfolio = foltextlist[0]
                        thisglosslist.append(thisfolio)
                        glossfound = True
            if not glossfound:
                thisglosslist.append("No Folio Information Found")
            glossnopat = re.compile(r'(\d{1,2}[a-z]?, )?\d{1,2}[a-z]?\. ')
            glosspatitir = glossnopat.finditer(gloss)
            for i in glosspatitir:
                thisglosslist.extend([(i.group())[:-2], gloss[gloss.find(i.group()) + len(i.group()):]])
            infolist.append(thisglosslist)
    return infolist


# for glossinfolist in get_glinfobasic("Wurzburg Glosses", 499, 509):
#     print(glossinfolist)
# print(get_glinfobasic("Wurzburg Glosses", 499, 499))
