"""Level 4"""

from OpenPages import get_pages
from GetSections import get_section
from OrderGlosses import order_glosses
from ClearTags import clear_tags
from GetLatInfo import get_latpageinfo
from GetFolio import get_fol
import re


def get_allinfo(file, startpage, stoppage=None):
    """Returns an infolist containing multiple sub-lists. The first sublist contains the headers for an info-table.
       Subsequent lists contain, respectively, for a set page range: page no., folio, gloss no., gloss text, Latin
       lemma, verse, and Latin text."""
    if stoppage is None:
        stoppage = startpage
    infolist = [["Page", "Folio", "Gloss No.", "Gloss Text", "Lemma", "Verse", "Glossed Latin"]]
    for page in range(startpage, stoppage + 1):
        thispage = page
        foliolist = []
        for folinfo in get_fol(order_glosses(clear_tags("\n\n".join(get_section(get_pages(
                file, thispage, thispage), "SG")), "fol"))):
            folio = folinfo[1]
            foliotext = folinfo[0]
            foliolist.append([folio, foliotext])
        for sublist in get_latpageinfo(file, page):
            glosslistplus = [thispage]
            thisgloss = sublist[0]
            glossfound = False
            for foltextlist in foliolist:
                if thisgloss in foltextlist[1]:
                    thisfolio = foltextlist[0]
                    glosslistplus.append(thisfolio)
                    glossfound = True
            if not glossfound:
                glossstub = thisgloss[:11]
                for foltextlist in foliolist:
                    if glossstub in foltextlist[1]:
                        thisfolio = foltextlist[0]
                        glosslistplus.append(thisfolio)
            glossnopat = re.compile(r'(\d{1,2}[a-z]?, )?\d{1,2}[a-z]?\. ')
            glosspatitir = glossnopat.finditer(thisgloss)
            glosslist = []
            for i in glosspatitir:
                glosslist.extend([i.group(), thisgloss[thisgloss.find(i.group()) + len(i.group()):]])
            glossno = glosslist[0]
            glosstext = glosslist[1]
            lemma = sublist[2]
            latin = sublist[1]
            latnopat = re.compile(r'00\. (Rom\. )?([IVX]{1,4}\. )?(\d{1,2}[a-z]?, )?(\d{1,2}[a-z]?\. )?')
            latpatitir = latnopat.finditer("00. " + latin)
            for i in latpatitir:
                if i.group() == "00. ":
                    latno = "0"
                else:
                    latno = (i.group())[4:-2]
                    latin = latin[len(latno) + 2:]
            glosslistplus.extend([glossno[:glossno.rfind(".")], glosstext, lemma, latno, latin])
            infolist.append(glosslistplus)
    latnofixlist = []
    for info in infolist:
        latnofixlist.append(info[5])
    numsearch = "".join(latnofixlist)
    romnumlist = []
    numeralpat = re.compile(r'[IVX]{1,4}\. ')
    numpatitir = numeralpat.finditer(numsearch)
    for numfind in numpatitir:
        if numfind.group() not in romnumlist:
            romnumlist.append(numfind.group())
    curline = "0"
    poscount = 0
    curnum = ""
    for item in latnofixlist:
        if "Rom. " in item:
            latnofixlist[poscount] = item[5:]
            item = latnofixlist[poscount]
        if item != "0":
            curline = item
        elif item == "0":
            latnofixlist[poscount] = curline
            item = latnofixlist[poscount]
        for romnum in romnumlist:
            if romnum in item:
                if item.find(romnum) == 0:
                    curnum = romnum
        if curnum not in item:
            latnofixlist[poscount] = curnum + item
        poscount += 1
    fixcount = 0
    for wronglist in infolist:
        wronglist[5] = latnofixlist[fixcount]
        fixcount += 1
    return infolist


# for inf in get_allinfo("Wurzburg Glosses", 499, 509):
#     print(inf)
# print(get_allinfo("Wurzburg Glosses", 499, 509))
