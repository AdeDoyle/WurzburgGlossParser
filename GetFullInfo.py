"""Level 3"""

from functools import lru_cache
from GetTagText import get_tagtext
from OpenPages import get_pages
from GetSections import get_section
from OrderGlosses import order_glosses, order_glosslist
from ClearTags import clear_tags, clear_spectags
from GetFolio import get_fol
from GetTrans import get_transpagesinfo
from OrderFootnotes import order_footlist, order_newlist, order_newglosslist, order_newtranslist
import re


@lru_cache(maxsize=1000)
def get_glinfo(file, startpage=499, stoppage=712):
    """Returns an infolist containing multiple sublists. The first sublist contains the headers for an info-table.
       Subsequent lists contain, respectively, for a set page range: Epistle, Page No., Folio, Gloss no. and Gloss Text
       (with [GLat][/GLat] tags converted to html italics tags) for every gloss in Wb."""
    curepist = "Unknown"
    infolist = [["Epistle", "Page", "Folio", "Gloss No.", "Gloss Full-Tags", "Gloss Text", "Gloss Footnotes",
                 "New Gloss Text", "Relevant Footnotes", "Adrian's Notes", "Gloss Translation", "New Translation"]]
    pagestrans = get_transpagesinfo(file, startpage, stoppage)
    for page in range(startpage, stoppage + 1):
        thispage = page
        pagetext = get_pages(file, thispage, thispage)
        # Gets all page Footnotes for the first time (for the gloss)
        footnotelist = order_footlist(file, page)
        # Gets all notes supplied by me
        notelist = order_newlist(file, page)
        newnotelist = list()
        notefol = False
        if notelist != ['']:
            for notenum, note in enumerate(notelist):
                # Separate folio-column tags from the text of site notes
                noteidpat = re.compile(r'\[/?f\. \d{1,2}[a-d]\]')
                noteiditer = noteidpat.findall(note)
                if noteiditer:
                    for folinfo in noteiditer:
                        note = "".join(note.split(folinfo))
                    folinfo = "".join(i for i in noteiditer[0] if i not in ["[", "]", "/"])
                    if notenum == 0:
                        notefol = folinfo
                    elif notefol != folinfo:
                        notefol = folinfo
                # Separate gloss numbers from the text of site notes
                notenumpat = re.compile(r'^\d{1,2}[a-z]?\. ')
                notenumiter = notenumpat.findall(note)
                if not notenumiter:
                    raise RuntimeError(f"Personal note found without link to gloss number.\nNote: {note}")
                elif len(notenumiter) > 1 or notenumiter[0] != note[:len(notenumiter[0])]:
                    raise RuntimeError(f"Multiple possible gloss numbers found for personal note.\nNote: {note}")
                elif notenumiter[0] == note[:len(notenumiter[0])]:
                    glossnum = notenumiter[0][:-2]
                    note = note[len(notenumiter[0]):].strip()
                newnotelist.append([notefol, glossnum, note])
        # Gets all new gloss readings supplied by me
        glosslist = order_newglosslist(file, page)
        newglosslist = list()
        glossfol = False
        if glosslist != ['']:
            for ng_num, newgloss in enumerate(glosslist):
                # Separate folio-column tags from the text of new gloss readings
                glossidpat = re.compile(r'\[/?f\. \d{1,2}[a-d]\]')
                glossiditer = glossidpat.findall(newgloss)
                if glossiditer:
                    for folinfo in glossiditer:
                        newgloss = "".join(newgloss.split(folinfo))
                    folinfo = "".join(i for i in glossiditer[0] if i not in ["[", "]", "/"])
                    if ng_num == 0:
                        glossfol = folinfo
                    elif glossfol != folinfo:
                        glossfol = folinfo
                # Separate gloss numbers from the text of new gloss readings
                glossnumpat = re.compile(r'^\d{1,2}[a-z]?\. ')
                glossnumiter = glossnumpat.findall(newgloss)
                if not glossnumiter:
                    raise RuntimeError(f"New gloss text found without link to gloss number.\nNote: {newgloss}")
                elif len(glossnumiter) > 1 or glossnumiter[0] != newgloss[:len(glossnumiter[0])]:
                    raise RuntimeError(f"Multiple possible gloss numbers found for new gloss text.\nNote: {newgloss}")
                elif glossnumiter[0] == newgloss[:len(glossnumiter[0])]:
                    glossnum = glossnumiter[0][:-2]
                    newgloss = newgloss[len(glossnumiter[0]):].strip()
                    # Remove or alter annotation tags that are likely to occur in the text of a new gloss reading
                    newgloss = "".join(newgloss.split("[ie]"))
                    newgloss = "".join(newgloss.split("[/ie]"))
                    newgloss = "".join(newgloss.split("[Con]"))
                    newgloss = "".join(newgloss.split("[/Con]"))
                    newgloss = "".join(newgloss.split("[Sup]"))
                    newgloss = "".join(newgloss.split("[/Sup]"))
                    newgloss = "<em>".join(newgloss.split("[GLat]"))
                    newgloss = "</em>".join(newgloss.split("[/GLat]"))
                newglosslist.append([glossfol, glossnum, newgloss])
        # Gets all new translations supplied by me
        translist = order_newtranslist(file, page)
        newtranslist = list()
        transfol = False
        if translist != ['']:
            for ng_num, newtrans in enumerate(translist):
                # Separate folio-column tags from the text of new gloss translation
                transidpat = re.compile(r'\[/?f\. \d{1,2}[a-d]\]')
                transiditer = transidpat.findall(newtrans)
                if transiditer:
                    for folinfo in transiditer:
                        newtrans = "".join(newtrans.split(folinfo))
                    folinfo = "".join(i for i in transiditer[0] if i not in ["[", "]", "/"])
                    if ng_num == 0:
                        transfol = folinfo
                    elif transfol != folinfo:
                        transfol = folinfo
                # Separate gloss numbers from the text of new gloss translations
                transnumpat = re.compile(r'^\d{1,2}[a-z]?\. ')
                transnumiter = transnumpat.findall(newtrans)
                if not transnumiter:
                    raise RuntimeError(f"New translation found without link to gloss number.\nNote: {newtrans}")
                elif len(transnumiter) > 1 or transnumiter[0] != newtrans[:len(transnumiter[0])]:
                    raise RuntimeError(f"Multiple possible gloss numbers found for new translation.\nNote: {newtrans}")
                elif transnumiter[0] == newtrans[:len(transnumiter[0])]:
                    glossnum = transnumiter[0][:-2]
                    newtrans = newtrans[len(transnumiter[0]):].strip()
                    # Alter annotation tags that are likely to occur in the text of a new gloss translation
                    newtrans = "<em>".join(newtrans.split("[GLat]"))
                    newtrans = "</em>".join(newtrans.split("[/GLat]"))
                newtranslist.append([transfol, glossnum, newtrans])
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
        # For each gloss on the current page, checks which folio it is in,
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
                footnotesgloss = glosstext[:]
                footnotepat = re.compile(r'\[/?[a-z]\]')
                fnpatitir = footnotepat.finditer(footnotesgloss)
                fnlist = []
                for j in fnpatitir:
                    fnlist.append(j.group())
                if not fnlist:
                    fnstring = ""
                    thisglosslist.extend([glossfulltags, basegloss, clear_tags(footnotesgloss), fnstring])
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
                    glossfnlist = []
                    for footnote in fnlist:
                        fnletter = footnote[-2]
                        # Collects footnotes relevant to this gloss and adds them to a list.
                        for fnote in footnotelist:
                            fnoteid = fnote[:1]
                            if fnletter == fnoteid:
                                glossfnlist.append(clear_tags(fnote[:1] + ":" + fnote[1:]))
                        fnsuperscript = "<sup>" + fnletter + "</sup>"
                        footnotesgloss = fnsuperscript.join(footnotesgloss.split(footnote))
                    thisglosslist.extend([glossfulltags, basegloss, clear_tags(footnotesgloss), glossfnlist])

                # Add new notes (site notes) to this gloss list
                if newnotelist:
                    for note in newnotelist:
                        folinfo = note[0]
                        glossnum = note[1]
                        notetext = note[2]
                        # if the current new note is for the current gloss
                        if folinfo == thisglosslist[2] and glossnum == thisglosslist[3]:
                            # if no empty string has been added (see else statement below) add the note text
                            if len(thisglosslist) == 8:
                                thisglosslist.extend([notetext])
                            # if empty string has been added (see else statement below), swap it for note text
                            elif len(thisglosslist) == 9:
                                if thisglosslist[8] == "":
                                    thisglosslist[8] = notetext
                        # if the current new note is not for the current gloss, add an empty string to thisglosslist
                        else:
                            anstring = ""
                            if len(thisglosslist) == 8:
                                thisglosslist.extend([anstring])
                elif not newnotelist:
                    anstring = ""
                    thisglosslist.extend([anstring])

                # Add new gloss readings to this gloss list
                if newglosslist:
                    for ngl in newglosslist:
                        folinfo = ngl[0]
                        glossnum = ngl[1]
                        ngltext = ngl[2]
                        # if the current new gloss text is for the current gloss
                        if folinfo == thisglosslist[2] and glossnum == thisglosslist[3]:
                            # if no empty string has been added (see else statement below) add the new gloss text
                            if len(thisglosslist) == 9:
                                thisglosslist = thisglosslist[:7] + [ngltext] + thisglosslist[7:]
                            # if empty string has been added (see else statement below), swap it for new gloss text
                            elif len(thisglosslist) == 10:
                                if thisglosslist[7] == "":
                                    thisglosslist[7] = ngltext
                        # if the current new gloss is not for the current gloss, add an empty string to thisglosslist
                        else:
                            ngstring = ""
                            if len(thisglosslist) == 9:
                                thisglosslist = thisglosslist[:7] + [ngstring] + thisglosslist[7:]
                elif not newglosslist:
                    ngstring = ""
                    thisglosslist = thisglosslist[:7] + [ngstring] + thisglosslist[7:]

                # Add new gloss translations to this gloss list
                if newtranslist:
                    for ntr in newtranslist:
                        folinfo = ntr[0]
                        glossnum = ntr[1]
                        ntrtext = ntr[2]
                        # if the current new translation text is for the current gloss
                        if folinfo == thisglosslist[2] and glossnum == thisglosslist[3]:
                            # if no empty string has been added (see else statement below) add the new translation text
                            if len(thisglosslist) == 10:
                                thisglosslist.extend([ntrtext])
                            # if empty string has been added (see else statement below), swap it for new translation
                            elif len(thisglosslist) == 11:
                                if thisglosslist[10] == "":
                                    thisglosslist[10] = ntrtext
                        # if the current new translation is not for the current gloss, add empty string to thisglosslist
                        else:
                            ntstring = ""
                            if len(thisglosslist) == 10:
                                thisglosslist.extend([ntstring])
                elif not newglosslist:
                    ntstring = ""
                    thisglosslist.extend([ntstring])

            infolist.append(thisglosslist)

    # add TPH translations to the info-lists where they are available
    for info_num, infoset in enumerate(infolist[1:]):  # exclude the first info-set containing the titles
        glossid = infoset[3]
        curpagetrans = pagestrans[0]
        curtransid = curpagetrans[0]
        curtrans = curpagetrans[1]
        # deal with the conjoined gloss on TPH p. 500 (1b10 + 1b11)
        # split the gloss id into the two numbers, use these to identify the two translations
        # conjoin the two translations and append them to the info-set for the conjoined gloss ids
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
            if "[GLat]" in joinedtrans:
                transtextlist = joinedtrans.split("[GLat]")
                joinedtrans = "<em>".join(transtextlist)
            if "[/GLat]" in joinedtrans:
                transtextlist = joinedtrans.split("[/GLat]")
                joinedtrans = "</em>".join(transtextlist)
            infolist[info_num + 1] = infoset[:-1] + [joinedtrans] + infoset[-1:]
        else:
            if glossid == curtransid:
                if "[GLat]" in curtrans:
                    transtextlist = curtrans.split("[GLat]")
                    curtrans = "<em>".join(transtextlist)
                if "[/GLat]" in curtrans:
                    transtextlist = curtrans.split("[/GLat]")
                    curtrans = "</em>".join(transtextlist)
                infolist[info_num + 1] = infoset[:-1] + [curtrans] + infoset[-1:]
                del pagestrans[0]
            # deal with page 587 where glosses 27, 28, and 29 share the one translation, numbered '27 – 29.'.
            elif " – " in curtransid:
                curtransidlist = curtransid.split(" – ")
                curtransidrange = [int(curtransidlist[0]), int(curtransidlist[1])]
                idstart = curtransidrange[0]
                idstop = curtransidrange[1]
                curtransidlist = []
                for i in range(idstart, idstop + 1):
                    curtransidlist.append(str(i))
                if glossid in curtransidlist:
                    if "[GLat]" in curtrans:

                        transtextlist = curtrans.split("[GLat]")
                        curtrans = "<em>".join(transtextlist)
                    if "[/GLat]" in curtrans:
                        transtextlist = curtrans.split("[/GLat]")
                        curtrans = "</em>".join(transtextlist)
                    infolist[info_num + 1] = infoset[:-1] + [curtrans] + infoset[-1:]
                if glossid == curtransidlist[-1]:
                    del pagestrans[0]
            # if no translation is given in TPH
            else:
                infolist[info_num + 1] = infoset[:-1] + [
                    "No translation available in <em>Thesaurus Palaeohibernicus</em>."
                ] + infoset[-1:]
    # Gets all page Footnotes for the second time (for the translation)
    curpage = None
    for infoset in infolist[1:]:  # exclude the first info-set containing the titles
        thistransfns = []
        # ensures page footnotes are only generated once per page, and not for every gloss
        if curpage:
            if curpage != infoset[1]:
                curpage = infoset[1]
                footnotelist = order_footlist(file, curpage)
        elif not curpage:
            curpage = infoset[1]
            footnotelist = order_footlist(file, curpage)
        trans = infoset[10]
        # finds which translations have footnotes, looks for the associated footnote i the list generated above
        if "<sup>" in trans:
            superscriptpat = re.compile(r'<sup>\w</sup>')
            superscriptpatitir = superscriptpat.finditer(trans)
            for i in superscriptpatitir:
                fnid = i.group()[5]
                for footnote in footnotelist:
                    if footnote[0] == fnid:
                        # if the footnote is found and not already in the footnote list for the gloss it is added
                        if infoset[8]:
                            if clear_tags(footnote[:1] + ":" + footnote[1:]) not in infoset[8]:
                                thistransfns.append(clear_tags(footnote[:1] + ":" + footnote[1:]))
                        else:
                            thistransfns.append(clear_tags(footnote[:1] + ":" + footnote[1:]))
        # all footnotes found for the gloss are combined
        # if there are translation footnotes
        if thistransfns:
            # if there are no gloss footnotes to add them to
            if not infoset[8]:
                infoset[8] = thistransfns
            # if there are gloss footnotes to add them to
            elif infoset[8]:
                for i in thistransfns:
                    infoset[8].append(i)
    return infolist


# if __name__ == "__main__":
#
#     for glossinfolist in get_glinfo("Wurzburg Glosses", 499, 509):
#         print(glossinfolist[7])
#     print(get_glinfo("Wurzburg Glosses", 499, 499))
#
#     for i in get_glinfo("Wurzburg Glosses", 624, 625):
#         print(i[:4] + i[8:])
#
#     get_glinfo("Wurzburg Glosses", 499, 712)
#     for i in get_glinfo("Wurzburg Glosses", 499, 579):
#         print(i)

