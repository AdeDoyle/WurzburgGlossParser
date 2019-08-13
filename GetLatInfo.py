"""Level 3"""

from functools import lru_cache
from GetSections import get_section
from OpenPages import get_pages
from OrderLatin import order_latlist
from OrderGlosses import order_glosses, order_glosslist
from ClearTags import clear_tags
import re


@lru_cache(maxsize=1000)
def get_latpageinfo(file, page):
    """returns a list of gloss-lists for a specified page of TPH
       each gloss-list contains a gloss[0], the Latin verse[1], the lemma[2], and the lemma position[3]"""
    latininfolist = []
    latlines = order_latlist("\n\n".join(get_section(get_pages(file, page, page), "Lat")))
    eachgloss = order_glosslist(clear_tags("\n\n".join(get_section(get_pages(file, page, page), "SG"))))
    glosses = order_glosses(clear_tags("\n\n".join(get_section(get_pages(file, page, page), "SG"))))
    numpat = re.compile(r'(\d{1,2}[a-z]?, )?\d{1,2}[a-z]?\. ')
    glossitir = numpat.finditer(glosses)
    glossnums = []
    for i in glossitir:
        # Gets gloss numbers from the Irish text, converts them to match tags in the Latin text, adds them to a list.
        glossnum = i.group()
        glossnum = glossnum[:-2]
        if ", " in glossnum:
            glossnum = "–".join(glossnum.split(", "))
        glossnums.append("[" + glossnum + "]")
    latpergloss = []
    lemmata = []
    positions = []
    usednums = []
    backlist = []
    # Creates a reversed version of latlines to be searched instead on pages where there are duplicate glossnos.
    # This prevents two glosses with the same number interacting with each other's Latin lines.
    for line in latlines:
        backlist.append(line)
    backlist.reverse()
    # Checks for expected gloss numbers in the latin text and, if found, adds the latin line and lemma to lists.
    for num in glossnums:
        if num not in usednums:
            # If this is the first instance of this glossno on this page.
            usednums.append(num)
            found = False
            while not found:
                for line in latlines:
                    if num in line:
                        latpergloss.append(line)
                        linetext = line
                        numpos = line.find(num)
                        linetext = linetext[:numpos]
                        lemma = linetext[linetext.rfind(" ") + 1:]
                        if "[" in lemma:
                            lemma = clear_tags(lemma)
                        lemmata.append(lemma)
                        notagtext = clear_tags(linetext, ["let"])
                        remnumpat = re.compile(
                            r'(\[NV\]|((Rom\. )?([IVX]{1,4}\. )?(\d{1,2}[a-z]?, )?(\d{1,2}[a-z]?\. )?))')
                        thisglossremnum = ""  # has to be put here for pages which begin mid-Latin-line
                        for remnum in remnumpat.finditer(notagtext):
                            if remnum.group() != "":
                                thisglossremnum = remnum.group()
                        remlen = len(thisglossremnum)
                        notagtext = notagtext[remlen:]
                        fnpat = re.compile(r'\[/?[a-d]\]')
                        fnpatitir = fnpat.finditer(notagtext)
                        fns = []
                        for fn in fnpatitir:
                            fns.append(fn.group())
                        if fns:
                            for marker in fns:
                                if "[/" in marker:
                                    notagtext = "".join(notagtext.split(marker[0] + marker[-2:]))
                                    supscr = "</em><sup>{}</sup><em>".format(marker[2:3])
                                    notagtext = supscr.join(notagtext.split(marker))
                            for marker in fns:
                                if marker in notagtext:
                                    supscr = "</em><sup>{}</sup><em>".format(marker[1:2])
                                    notagtext = supscr.join(notagtext.split(marker))
                        lempos = notagtext.rfind(lemma)
                        positions.append(lempos)
                        found = True
                        break
        elif num in usednums:
            # If this is not the first instance of this glossno on this page.
            found = False
            while not found:
                for line in backlist:
                    if num in line:
                        latpergloss.append(line)
                        linetext = line
                        numpos = line.find(num)
                        linetext = linetext[:numpos]
                        lemma = linetext[linetext.rfind(" ") + 1:]
                        if "[" in lemma:
                            lemma = clear_tags(lemma)
                        lemmata.append(lemma)
                        notagtext = clear_tags(linetext, ["let"])
                        remnumpat = re.compile(
                            r'(\[NV\]|((Rom\. )?([IVX]{1,4}\. )?(\d{1,2}[a-z]?, )?(\d{1,2}[a-z]?\. )?))')
                        thisglossremnum = ""  # has to be put here for pages which begin mid-Latin-line
                        for remnum in remnumpat.finditer(notagtext):
                            if remnum.group() != "":
                                thisglossremnum = remnum.group()
                        remlen = len(thisglossremnum)
                        notagtext = notagtext[remlen:]
                        fnpat = re.compile(r'\[/?[a-d]\]')
                        fnpatitir = fnpat.finditer(notagtext)
                        fns = []
                        for fn in fnpatitir:
                            fns.append(fn.group())
                        if fns:
                            for marker in fns:
                                if "[/" in marker:
                                    notagtext = "".join(notagtext.split(marker[0] + marker[-2:]))
                                    supscr = "</em><sup>{}</sup><em>".format(marker[2:3])
                                    notagtext = supscr.join(notagtext.split(marker))
                            for marker in fns:
                                if marker in notagtext:
                                    supscr = "</em><sup>{}</sup><em>".format(marker[1:2])
                                    notagtext = supscr.join(notagtext.split(marker))
                        lempos = notagtext.rfind(lemma)
                        positions.append(lempos)
                        found = True
                        break
    for i in range(len(glossnums)):
        # Compiles a list of the gloss, the Latin line, and the lemma for the gloss within the Latin line.
        thislatperglos = latpergloss[i]
        fnpat = re.compile(r'\[/?[a-d]\]')
        fnpatitir = fnpat.finditer(thislatperglos)
        fns = []
        for fn in fnpatitir:
            fns.append(fn.group())
        if fns:
            for marker in fns:
                if "[/" in marker:
                    thislatperglos = "".join(thislatperglos.split(marker[0] + marker[-2:]))
                    supscr = "</em><sup>{}</sup><em>".format(marker[2:3])
                    thislatperglos = supscr.join(thislatperglos.split(marker))
            for marker in fns:
                if marker in thislatperglos:
                    supscr = "</em><sup>{}</sup><em>".format(marker[1:2])
                    thislatperglos = supscr.join(thislatperglos.split(marker))
        latininfolist.append([eachgloss[i], clear_tags(thislatperglos, ["NV"]), clear_tags(lemmata[i]), positions[i]])
    return latininfolist


@lru_cache(maxsize=1000)
def get_latinfo(file, startpage, stoppage):
    """returns a list of gloss-lists for a specified page range within TPH
       each gloss-list contains a gloss[0], the Latin verse[1], the lemma[2], and the lemma position[3]"""
    infolist = []
    for page in range(startpage, stoppage + 1):
        curlist = get_latpageinfo(file, page)
        for list in curlist:
            infolist.append(list)
    return infolist


# for informationlist in (get_latpageinfo("Wurzburg Glosses", 499)):
#     print(informationlist[3])

# for informationlist in (get_latinfo("Wurzburg Glosses", 499, 712)):
#     print(informationlist)
