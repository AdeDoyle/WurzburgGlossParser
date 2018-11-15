"""Level 3"""

from GetTagText import get_tagtext
from OpenPages import get_pages
from GetSections import get_section
from OrderGlosses import order_glosses, order_glosslist
from ClearTags import clear_tags, clear_spectags
from GetFolio import get_fol
import re


def get_glinfo(file, startpage=499, stoppage=712):
    """Returns an infolist containing multiple sublists. The first sublist contains the headers for an info-table.
       Subsequent lists contain, respectively, for a set page range: Epistle, Page No., Folio, Gloss no. and Gloss Text
       (with [GLat][/GLat] tags converted to html italics tags) for every gloss in Wb."""
    curepist = "Unknown"
    infolist = [["Epistle", "Page", "Folio", "Gloss No.", "Gloss Text", "Gloss Footnotes"]]
    for page in range(startpage, stoppage + 1):
        thispage = page
        pagetext = get_pages(file, thispage, thispage)
        # Checks for a new epistle on the current page.
        epfunc = get_tagtext(pagetext, "H2")
        if epfunc:
            curepist = epfunc[0]
        # Identifies individual glosses on the current page, and adds them to a gloss-list.
        glosslist = order_glosslist(clear_tags("\n\n".join(get_section(pagetext, "SG")), ["GLat", "let"]))
        foliolist = []
        # Creates a list of folios and related gloss text for the current page.
        for folinfo in get_fol(order_glosses(clear_tags("\n\n".join(get_section(get_pages(
                file, thispage, thispage), "SG")), ["GLat", "fol", "let"]))):
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
            # Adds gloss number and gloss texts to list.
            for i in glosspatitir:
                glosstext = gloss[gloss.find(i.group()) + len(i.group()):]
                # Replaces Latin tags with html emphasis tags.
                if "[GLat]" in glosstext:
                    glosstextlist = glosstext.split("[GLat]")
                    glosstext = "<em>".join(glosstextlist)
                if "[/GLat]" in glosstext:
                    glosstextlist = glosstext.split("[/GLat]")
                    glosstext = "</em>".join(glosstextlist)
                basegloss = clear_spectags(glosstext, "let")
                footnotesgloss = clear_tags(glosstext, "let")
                footnotepat = re.compile(r'\[/?[a-z]\]')
                fnpatitir = footnotepat.finditer(footnotesgloss)
                fnlist = []
                for i in fnpatitir:
                    fnlist.append(i.group())
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
                thisglosslist.extend([(i.group())[:-2], basegloss, footnotesgloss])
            infolist.append(thisglosslist)
    return infolist


# for glossinfolist in get_glinfo("Wurzburg Glosses", 499, 509):
#     print(glossinfolist)
# print(get_glinfo("Wurzburg Glosses", 499, 499))
