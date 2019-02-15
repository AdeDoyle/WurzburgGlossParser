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
        # Collect folio information, one page at a time
        foliolist = []
        for folinfo in get_fol(order_glosses(clear_tags("\n\n".join(get_section(get_pages(
                file, thispage, thispage), "SG")), "fol"))):
            folio = folinfo[1]
            foliotext = folinfo[0]
            foliolist.append([folio, foliotext])
        # Gets gloss, glossed latin, and lemma for all glosses, one page at a time
        for sublist in get_latpageinfo(file, page):
            glosslistplus = [thispage]
            thisgloss = sublist[0]
            glossfound = False
            # For each folio on the page compares gloss from Latin list to the gloss in the folio list
            # If found, folio is identified for gloss
            for foltextlist in foliolist:
                if thisgloss in foltextlist[1]:
                    thisfolio = foltextlist[0]
                    glosslistplus.append(thisfolio)
                    glossfound = True
            # If gloss not found still, compares first ten characters of gloss from Latin list to gloss in folio list
            # Only seems to affect f.2a 21 ([f. 2b]) marker bisects gloss in TPH
            if not glossfound:
                glossstub = thisgloss[:11]
                for foltextlist in foliolist:
                    if glossstub in foltextlist[1]:
                        thisfolio = foltextlist[0]
                        glosslistplus.append(thisfolio)
            # Gets each gloss on this page by finding its number
            # Returns gloss number and then the gloss in a list for each gloss
            # Adds each list to a gloss list for the page
            glossnopat = re.compile(r'(\d{1,2}[a-z]?, )?\d{1,2}[a-z]?\. ')
            glosspatitir = glossnopat.finditer(thisgloss)
            glosslist = []
            for i in glosspatitir:
                glosslist.extend([i.group(), thisgloss[thisgloss.find(i.group()) + len(i.group()):]])
            # Identifies glossno, glosstext, latin text, and latin lemma from their lists (all already found)
            glossno = glosslist[0]
            glosstext = glosslist[1]
            lemma = sublist[2]
            latin = sublist[1]
            # Identifies Latin Verse Numbers and Latin text for that verse
            # Adds '00. ' to the start of every latin line in the page's Latin list (for folios that start with no no.)
            # 'Rom. ' is removed later (Why include 'Rom. '?)
            versenopat = re.compile(r'00\. (Rom\. )?([IVX]{1,4}\. )?(\d{1,2}[a-z]?, )?(\d{1,2}[a-z]?\. )?')
            latpatitir = versenopat.finditer("00. " + latin)
            for i in latpatitir:
                if i.group() == "00. ":
                    verseno = "0"
                else:
                    verseno = (i.group())[4:-2]
                    latin = latin[len(verseno) + 2:]
            # Adds glossno, glosstext, lemma, verseno, and Latin text to glosslistplus
            # Now glosslistplus is: pageno, folio, glossno, glosstext, lemma, verseno, and Latin text
            # Adds glosslistplus to infolist (which is returned once fixed)
            glosslistplus.extend([glossno[:glossno.rfind(".")], glosstext, lemma, verseno, latin])
            infolist.append(glosslistplus)
    # Fixes versenos in infolist (combines numberless verses, adds chapter to verses with verseno only)
    # Adds all versenos from infolist to versenofixlist
    versenofixlist = []
    for info in infolist:
        versenofixlist.append(info[5])
    # Joins all versenos together
    numsearch = "".join(versenofixlist)
    romnumlist = []
    # Finds all chapter numerals throughout all the verse info, adds these to romnumlist
    numeralpat = re.compile(r'[IVX]{1,4}\. ')
    numpatitir = numeralpat.finditer(numsearch)
    for numfind in numpatitir:
        if numfind.group() not in romnumlist:
            romnumlist.append(numfind.group())
    # Goes through every verseno in the versenofixlist
    curverse = "0"
    poscount = 0
    curnum = ""
    for item in versenofixlist:
        # Removes 'Rom. ' from the numeral
        if "Rom. " in item:
            versenofixlist[poscount] = item[5:]
            item = versenofixlist[poscount]
        if item != "0":
            curverse = item
        # Replaces no-number verses with the number of the previous verse
        elif item == "0":
            versenofixlist[poscount] = curverse
            item = versenofixlist[poscount]
        # Updates the current (previous) verse to the roman numeral of the current verse
        for romnum in romnumlist:
            if romnum in item:
                if item.find(romnum) == 0:
                    curnum = romnum
        # Combines chapter numerals to verse numbers that don't have them already
        if curnum not in item:
            versenofixlist[poscount] = curnum + item
        poscount += 1
    fixcount = 0
    # The versenos in infolist are updated with the corrected forms from versenofixlist
    for wronglist in infolist:
        wronglist[5] = versenofixlist[fixcount]
        fixcount += 1
    return infolist


# for inf in get_allinfo("Wurzburg Glosses", 499, 509):
#     print(inf)
# print(get_allinfo("Wurzburg Glosses", 499, 509))
