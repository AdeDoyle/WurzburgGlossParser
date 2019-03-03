"""Level 3"""

from GetTagText import get_tagtext
from OpenPages import get_pages
from GetSections import get_section
from OrderGlosses import order_glosses, order_glosslist
from ClearTags import clear_tags, clear_spectags
from GetFolio import get_fol
from GetTrans import get_transpagesinfo
import re


def get_glinfo(file, startpage=499, stoppage=712):
    """Returns an infolist containing multiple sublists. The first sublist contains the headers for an info-table.
       Subsequent lists contain, respectively, for a set page range: Epistle, Page No., Folio, Gloss no. and Gloss Text
       (with [GLat][/GLat] tags converted to html italics tags) for every gloss in Wb."""
    curepist = "Unknown"
    infolist = [["Epistle", "Page", "Folio", "Gloss No.", "Gloss Full-Tags", "Gloss Text", "Gloss Footnotes",
                 "Gloss Translation"]]
    pagestrans = get_transpagesinfo(file, startpage, stoppage)
    for page in range(startpage, stoppage + 1):
        thispage = page
        pagetext = get_pages(file, thispage, thispage)
        # Checks for a new epistle on the current page.
        epfunc = get_tagtext(pagetext, "H2")
        if epfunc:
            curepist = epfunc[0]
        # Identifies individual glosses on the current page, and adds them to a gloss-list.
        glosslist = order_glosslist(clear_spectags("\n\n".join(get_section(pagetext, "SG")), "fol"))
        foliolist = []
        # Creates a list of folios and related gloss text for the current page.
        for folinfo in get_fol(order_glosses("\n\n".join(get_section(get_pages(
                file, thispage, thispage), "SG")))):
            folio = folinfo[1]
            foliotext = folinfo[0]
            foliolist.append([folio, foliotext])
        # Creates a list with the current epistle name and page,
        # Checks for each gloss on the current page which folio it is in,
        # Adds folio information to the list.
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
            # Identifies gloss numbers and removes them from the gloss text.
            glossnopat = re.compile(r'(\d{1,2}[a-z]?, )?\d{1,2}[a-z]?\. ')
            glosspatitir = glossnopat.finditer(gloss)
            for i in glosspatitir:
                # Adds gloss number to list.
                thisglosslist.append(i.group()[:-2])
                # Identifies foundational gloss including all markup tags.
                glossfulltags = gloss[gloss.find(i.group()) + len(i.group()):]
                # Creates a display copy of the gloss text, replacing Latin tags with html emphasis tags.
                glosstext = glossfulltags
                if "[GLat]" in glosstext:
                    glosstextlist = glosstext.split("[GLat]")
                    glosstext = "<em>".join(glosstextlist)
                if "[/GLat]" in glosstext:
                    glosstextlist = glosstext.split("[/GLat]")
                    glosstext = "</em>".join(glosstextlist)
                # Creates 2 copies of display gloss text, one primary, one retaining footnotes in superscript tags.
                basegloss = clear_tags(glosstext)
                footnotesgloss = clear_tags(glosstext, "let")
                footnotepat = re.compile(r'\[/?[a-z]\]')
                fnpatitir = footnotepat.finditer(footnotesgloss)
                fnlist = []
                for j in fnpatitir:
                    fnlist.append(j.group())
                if fnlist:
                    for fntag in fnlist:
                        if "[/" in fntag:
                            endtag = fntag
                            begintag = "".join(endtag.split("/"))
                            footnotesgloss = "".join(footnotesgloss.split(begintag))
                            tagplace = footnotesgloss.find(endtag)
                            footnotesgloss = footnotesgloss[:tagplace] + "<sup>" +\
                                             footnotesgloss[tagplace + 2: tagplace + 3] + "</sup>" +\
                                             footnotesgloss[tagplace + 4:]
                            if begintag in fnlist:
                                del fnlist[fnlist.index(begintag)]
                    for footnote in fnlist:
                        fnletter = footnote[-2]
                        fnsuperscript = "<sup>" + fnletter + "</sup>"
                        footnotesgloss = fnsuperscript.join(footnotesgloss.split(footnote))
                thisglosslist.extend([glossfulltags, basegloss, footnotesgloss])
            infolist.append(thisglosslist)
    # add translations to the end of the infolists where they are available
    for infoset in infolist:
        # exclude the first infoset containing the titles
        if infoset != infolist[0]:
            glossid = infoset[3]
            curpagetrans = pagestrans[0]
            curtransid = curpagetrans[0]
            curtrans = curpagetrans[1]
            # deal with the conjoined gloss on TPH p. 500 (1b10 + 1b11)
            # split the gloss id into the two numbers, use these to identify the two translations
            # conjoin the two translations and append them to the infoset for the conjoined gloss ids
            if ", " in glossid:
                glossidlist = glossid.split(", ")
                splittranslations = []
                for newid in glossidlist:
                    if newid == curtransid:
                        splittranslations.append(curtrans)
                        del pagestrans[0]
                        curpagetrans = pagestrans[0]
                        curtransid = curpagetrans[0]
                        curtrans = curpagetrans[1]
                joinedtrans = " i.e. ".join(splittranslations)
                infoset.append(joinedtrans)
            else:
                if glossid == curtransid:
                    infoset.append(curtrans)
                    del pagestrans[0]
                # if no translation is given in TPH
                else:
                    infoset.append("No translation available.")
    return infolist


# for glossinfolist in get_glinfo("Wurzburg Glosses", 499, 509):
#     print(glossinfolist)
# print(get_glinfo("Wurzburg Glosses", 499, 499))
