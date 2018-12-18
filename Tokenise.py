"""Level 2, 2, 1, 2"""

from RemoveNewlines import remove_newlines, get_pages, get_section, clear_tags, order_glosses, remove_brackets,\
    remove_glossnums
from RemoveLatin import rem_lat
from RemovePunctuation import rempunc_tok
from OpenDocx import get_text
from SaveXlsx import save_xlsx


def space_tokenise(string, puncfilter=False, puncexcept=[]):
    """Takes a string, a true/false value for filtering punctuation and a list of punctuation-filter exceptions.
       Replaces newlines with spaces, tokenises string based on word spacing.
       If filter punctuation is true, each token has """
    strunaltered = string
    stroneline = remove_newlines(strunaltered)
    strtoklist = stroneline.split(" ")
    if puncfilter:
        newtoklist = []
        for tok in strtoklist:
            tok = rempunc_tok(tok, puncexcept)
            newtoklist.append(tok)
        return newtoklist
    else:
        return strtoklist


def remove_duptoks(toklist):
    """Creates a list of unique tokens which occur in the full list of tokens"""
    uniquetoks = []
    for tok in toklist:
        if tok not in uniquetoks:
            uniquetoks.append(tok)
    return uniquetoks


# Defines a function which gets the first element in a list.
def takefirst(elem):
    return elem[0]


def top_toks(string, occurrences=0):
    """Takes a string, and optional minimum number of occurrences, tokenises the string, removes blank tokens or tokens
       with punctuation only, returns list of sublists of tokens and use-count for that token in the string"""
    strtoks = space_tokenise(string, True)
    unitoks = remove_duptoks(strtoks)
    tokinfolist = []
    # Creates a list of a token's count, and the token itself, and adds this list to tokinfolist.
    for tok in unitoks:
        if tok != "":
            tokcount = strtoks.count(tok)
            tokinfo = [tokcount, tok]
            tokinfolist.append(tokinfo)
    # Sorts tokinfolist into descending order.
    tokinfolist.sort(key=takefirst, reverse=True)
    toknum = 0
    orderedtoklist = []
    # Counts, then lists, in descending order, tokens with more than a set number of occurrences in the string.
    for i in tokinfolist:
        if i[0] >= occurrences:
            toknum += 1
            orderedtoklist.append([toknum, i[0], i[1]])
    return orderedtoklist


# glosses = remove_glossnums(remove_brackets(
#     order_glosses(clear_tags("\n".join(get_section(get_pages("Wurzburg Glosses", 499, 712), "SG"))))))
# glosses = remove_glossnums(remove_brackets(rem_lat(order_glosses(clear_tags(
#     "\n".join(get_section(get_pages("Wurzburg Glosses", 499, 712), "SG")), ["GLat", "ie", "vel"])), True)))
# glosses = remove_glossnums(remove_brackets(rem_lat(clear_tags(
#     get_text("Wb. Prima Manus"), ["GLat", "ie", "vel"]), True)))
# glosses = remove_glossnums(remove_brackets(rem_lat(clear_tags(
#     get_text("Wb. Hand Two"), ["GLat", "ie", "vel"]), True)))
# glosses = remove_glossnums(remove_brackets(rem_lat(clear_tags(
#     get_text("Wb. Hand Three"), ["GLat", "ie", "vel"]), True)))


# # Prints the most common tokens.
# for token in top_toks(glosses, 53):
#     print(str(token[0]) + ". " + token[2] + " - Count: " + str(token[1]))

# # Saves an excel document of the most common tokens.
# save_xlsx("Wb. Common Tokens", top_toks(glosses, 53))
