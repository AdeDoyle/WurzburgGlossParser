"""Level 3"""

from GetSections import get_section
from OpenPages import get_pages
from ClearTags import clear_spectags
import re


def get_transpageinfo(file, page):
    """Returns a list of translation lists for each page
       Each translation list contains a glossno [0] and a gloss translation [1]"""
    english = clear_spectags("\n\n".join(get_section(get_pages(file, page, page), "Eng")), "fol")
    englishnums = []
    englishlines = []
    engpat = re.compile(r'\d{1,2}[a-z]?\. ')
    engpatitir = engpat.finditer(english)
    # find the numbers in the english text, add them to a list
    for i in engpatitir:
        englishnums.append(i.group())
    # using the numbers as markers, identify the strings associated with the numbers, add them to a list
    for i in range(len(englishnums)):
        numlen = len(englishnums[i])
        # if the current number isn't the last number, the string is from this number to the next number
        if i != len(englishnums) - 1:
            if englishnums[i + 1] not in englishnums[i]:
                line = english[english.find(englishnums[i]) + numlen: english.find(englishnums[i + 1])]
            # account for situations where the next number is in the current number
            # eg. "1. " is in "21. " on page 503
            else:
                scrap = english
                firstspot = scrap.find(englishnums[i + 1])
                scrap = scrap[firstspot + len(englishnums[i + 1]):]
                secondspot = scrap.find(englishnums[i + 1]) + len(englishnums[i + 1])
                line = english[english.find(englishnums[i]) + numlen: secondspot]
            english = english[numlen:]
            english = english[english.find(englishnums[i + 1]):]
        # if the current number is the last number, the string is from this number to the end
        else:
            line = english[english.find(englishnums[i]) + numlen:]
        line = line.split("\n")
        line = " ".join(line)
        line = line.strip()
        englishlines.append(line)
    translist = []
    # remove full stop and space from end of number
    for i in range(len(englishnums)):
        thistransnum = englishnums[i]
        englishnums[i] = thistransnum[:thistransnum.rfind(".")]
    # add number and trans to list, then lest to translist
    for i in range(len(englishnums)):
        thislist = [englishnums[i], englishlines[i]]
        translist.append(thislist)
    return translist


# for informationlist in (get_transpageinfo("Wurzburg Glosses", 503)):
#         print(informationlist)

# for leath in range(499, 712):
#     for informationlist in (get_transpageinfo("Wurzburg Glosses", leath)):
#         print(str(leath) + " " + informationlist[0] + " " + informationlist[1])
