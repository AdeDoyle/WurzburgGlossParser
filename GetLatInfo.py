"""Level 3"""

from GetSections import get_section
from OpenPages import get_pages
from OrderLatin import order_latlist
from OrderGlosses import order_glosses, order_glosslist
from ClearTags import clear_tags
import re


def get_latpageinfo(file, page):
    """returns a list of gloss-lists for a specified page of TPH
       each gloss-list contains a gloss, the Latin text the gloss is on, and the specific Latin "lemma" or word that
       is marked in TPH to show the gloss as gloss-list[0], [1] and [2] respectively"""
    latininfolist = []
    latlines = order_latlist("\n\n".join(get_section(get_pages(file, page, page), "Lat")))
    eachgloss = order_glosslist(clear_tags("\n\n".join(get_section(get_pages(file, page, page), "SG"))))
    glosses = order_glosses(clear_tags("\n\n".join(get_section(get_pages(file, page, page), "SG"))))
    numpat = re.compile(r'(\d{1,2}[a-z]?, )?\d{1,2}[a-z]?\. ')
    glossitir = numpat.finditer(glosses)
    glossnums = []
    for i in glossitir:
        # gets gloss numbers from the Irish text, converts them to match tags in the Latin text, adds them to a list.
        glossnum = i.group()
        glossnum = glossnum[:-2]
        if ", " in glossnum:
            glossnum = "–".join(glossnum.split(", "))
        glossnums.append("[" + glossnum + "]")
    latpergloss = []
    lemmas = []
    for num in glossnums:
        # checks for expected gloss numbers in the latin text and, if found, adds the latin line and lemma to lists.
        for line in latlines:
            if num in line:
                latpergloss.append(line)
                linetext = line
                numpos = line.find(num)
                linetext = linetext[:numpos]
                lemma = linetext[linetext.rfind(" ") + 1:]
                lemmas.append(lemma)
    for i in range(len(glossnums)):
        # compiles a list of the gloss, the Latin line, and the lemma for the gloss within the Latin line.
        latininfolist.append([eachgloss[i], clear_tags(latpergloss[i]), clear_tags(lemmas[i])])
    return latininfolist


def get_latinfo(file, startpage, stoppage):
    """returns a list of gloss-lists for a specified page range within TPH
       each gloss-list contains a gloss, the Latin text the gloss is on, and the specific Latin "lemma" or word that
       is marked in TPH to show the gloss as gloss-list[0], [1] and [2] respectively"""
    infolist = []
    for page in range(startpage, stoppage + 1):
        curlist = get_latpageinfo(file, page)
        for list in curlist:
            infolist.append(list)
    return infolist


# for informationlist in (get_latpageinfo("Wurzburg Glosses", 499)):
#     print(informationlist)

# for informationlist in (get_latinfo("Wurzburg Glosses", 499, 712)):
#     print(informationlist)
