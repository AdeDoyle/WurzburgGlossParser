"""Level 2"""

from OpenDocx import get_text
from OrderGlosses import order_glosslist
from RemoveLatin import rep_lat
from ClearTags import clear_tags
from RemoveBrackets import remove_brackets
import re


def openhandlists(file):
    """Gets the text from a gloss-hand file"""
    filetext = get_text(file)
    return filetext


def splitglosses(file):
    """Splits the glosses from a gloss-hand file into a gloss list"""
    filetext = openhandlists(file)
    glosslist = order_glosslist(filetext)
    return glosslist


def cleangloss(gloss):
    """Takes a gloss, replaces Latin with a place-marker, removes tags, removes brackets and non-gloss bracket content,
       then removes gloss numbers and all unnecessary punctuation"""
    cleanedgloss = remove_brackets(clear_tags(rep_lat(gloss, "*Latin*")))
    # Removes gloss numbers
    numpat = re.compile(r'(\d{1,2}[a-z]?, )?\d{1,2}[a-z]?\. ')
    numpatitir = numpat.finditer(cleanedgloss)
    for i in numpatitir:
        if i.group() in cleanedgloss:
            glosssplit = cleanedgloss.split(i.group())
            cleanedgloss = "".join(glosssplit)
    # Removes all known, undesired punctuation except full stops
    for punct in [",", " . ", ":", ";", ".........", ".......", "......", ".....", "....", "...", "  "]:
        if punct in cleanedgloss:
            while punct in cleanedgloss:
                glosssplit = cleanedgloss.split(punct)
                cleanedgloss = " ".join(glosssplit)
    # Removes most unrequired full stops
    stoppat = re.compile(r'[^ilɫró]\.[^\w]')
    stoppatitir = stoppat.finditer(cleanedgloss)
    for i in stoppatitir:
        if i.group() in cleanedgloss:
            glosssplit = cleanedgloss.split(i.group())
            cleanedgloss = "".join(glosssplit)
    # Replaces doubled Latin markers with just one
    if "*Latin* *Latin*" in cleanedgloss:
        while "*Latin* *Latin*" in cleanedgloss:
            glosssplit = cleanedgloss.split("*Latin* *Latin*")
            cleanedgloss = "*Latin*".join(glosssplit)
    # Removes full stops at the end of glosses as long as they're not part of "rl.", ".i." or "ɫ."
    if cleanedgloss[-1] == ".":
        patfound = False
        endpat = re.compile(r'(rl|\.i|ɫ)\.')
        endpatitir = endpat.finditer(cleanedgloss)
        for i in endpatitir:
            ilen = len(i.group())
            if i.group() == cleanedgloss[-ilen:]:
                patfound = True
        if not patfound:
            cleanedgloss = cleanedgloss[:-1]
    cleanedgloss = cleanedgloss.strip()
    return cleanedgloss


def tokenisegloss(gloss):
    glosstoks = gloss.split(" ")
    return glosstoks


def compile_tokenised_glosslist(file):
    """Takes a file, removes glosses which contain no Irish tokens,
       counts faults experienced along the way,
       returns a tokenised list of lists (glosses and their tokens) for each acceptable gloss"""
    tokenised_handlist = []
    # removes glosses just comprised of non-Old-Irish tokens
    faultlist = [".i.", "rl.", "ɫ.", "*Latin*", ""]
    faultcount = 0
    for gloss in splitglosses(file):
        if cleangloss(gloss) not in faultlist:
            glossfault = True
            for glosstok in tokenisegloss(cleangloss(gloss)):
                if glosstok not in faultlist:
                    glossfault = False
                    break
            if glossfault:
                faultcount += 1
            else:
                tokenised_handlist.append(tokenisegloss(cleangloss(gloss)))
        else:
            faultcount += 1
    # print(faultcount)
    return tokenised_handlist


# glosshands = ["Wb. All Glosses", "Wb. Prima Manus", "Wb. Hand Two", "Wb. Hand Three"]
# allglosstoks = compile_tokenised_glosslist(glosshands[0])
# pmtoks = compile_tokenised_glosslist(glosshands[1])
# h2toks = compile_tokenised_glosslist(glosshands[2])
# h3toks = compile_tokenised_glosslist(glosshands[3])

# print(len(allglosstoks))
# print(len(pmtoks))
# print(len(h2toks))
# print(len(h3toks))

# print(openhandlists(glosshands[0]))

# for gloss in splitglosses(glosshands[0]):
#     print(gloss)

# for gloss in splitglosses(glosshands[0]):
#     print(cleangloss(gloss))

# for tok_gloss in compile_tokenised_glosslist(glosshands[0]):
#     print(tok_gloss)
