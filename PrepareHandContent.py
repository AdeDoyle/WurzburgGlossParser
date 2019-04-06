"""Level 2, 2, 2, 1, 1, 1, 2, 2, 1"""

from OpenDocx import get_text
from OrderGlosses import order_glosslist
from RemoveLatin import rep_lat
from ClearTags import clear_tags
from RemoveBrackets import remove_brackets
import re
from Tokenise import remove_duptoks


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
        # Remainder (below) necessary to ensure only full stop is removed, and not all of i.group()
        isplit = (i.group().strip()).split(".")
        # Ensure no space is removed after "*"
        if "*" in isplit:
            remainder = " ".join(isplit)
        else:
            remainder = ("".join(isplit))
        if i.group() in cleanedgloss:
            glosssplit = cleanedgloss.split(i.group())
            cleanedgloss = remainder.join(glosssplit)
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
    if cleanedgloss[:3] != ".i.":
        if cleanedgloss[0] == ".":
            cleanedgloss = cleanedgloss[1:]
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


def combinelists(listlist):
    """Combines lists of lists into a single list of the
       contents of all the lists in the list-of-lists entered"""
    outlist = []
    for i in range(len(listlist)):
        singlelist = listlist[i]
        for j in range(len(singlelist)):
            outlist.append(singlelist[j])
    return outlist


def get_unitoks(glosslist):
    """Returns a list of unique tokens in a list of tokenised glosses"""
    return remove_duptoks(combinelists(glosslist))


def get_unitokscount(glosslist):
    """Returns a count of all unique tokens in a list of tokenised glosses"""
    unitoks = remove_duptoks(combinelists(glosslist))
    tokcount = len(unitoks)
    return tokcount


def get_inditokcount(tok, glosslist):
    """Returns a count of a single token's number of occurrences in a list of tokenised glosses"""
    alltoks = combinelists(glosslist)
    if tok in alltoks:
        return alltoks.count(tok)
    elif tok not in alltoks:
        return 0


# glosshands = ["Wb. All Glosses", "Wb. Prima Manus", "Wb. Hand Two", "Wb. Hand Three"]
# allglosstoks = compile_tokenised_glosslist(glosshands[0])
# pmtoks = compile_tokenised_glosslist(glosshands[1])
# h2toks = compile_tokenised_glosslist(glosshands[2])
# h3toks = compile_tokenised_glosslist(glosshands[3])


# print(openhandlists(glosshands[0]))

# for gloss in splitglosses(glosshands[0]):
#     print(gloss)

# for gloss in splitglosses(glosshands[0]):
#     print(cleangloss(gloss))

# for tok_gloss in compile_tokenised_glosslist(glosshands[0]):
#     print(tok_gloss)

# for unitok in get_unitoks(pmtoks):
#     print(unitok)

# print(get_unitokscount(pmtoks))

# for tok in remove_duptoks(combinelists(pmtoks)):
#     print(tok + ": " + str(get_inditokcount(tok, pmtoks)))

# # Count how many glosses are in each gloss-list
# print(len(allglosstoks))
# print(len(pmtoks))
# print(len(h2toks))
# print(len(h3toks))

# # Count how many unique tokens are in each gloss-list
# print(len(remove_duptoks(combinelists(allglosstoks))))
# print(len(remove_duptoks(combinelists(pmtoks))))
# print(len(remove_duptoks(combinelists(h2toks))))
# print(len(remove_duptoks(combinelists(h3toks))))

# # Count how many tokens are in each gloss-list
# print(len(combinelists(allglosstoks)))
# print(len(combinelists(pmtoks)))
# print(len(combinelists(h2toks)))
# print(len(combinelists(h3toks)))
