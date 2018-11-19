"""Level 2, 2, 1, 2"""

from RemoveNewlines import remove_newlines, get_pages, get_section, clear_tags, order_glosses, remove_brackets,\
    remove_glossnums
from SaveXlsx import save_xlsx


def space_tokenise(string):
    """Takes a string, replaces newlines with spaces, tokenises string based on word spacing"""
    strunaltered = string
    stroneline = remove_newlines(strunaltered)
    strtoklist = stroneline.split(" ")
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
    """Takes a string, and optional minimum number of occurrences, tokenises the string,
       returns list of sublists of tokens and use-count for that token in the string"""
    strtoks = space_tokenise(string)
    unitoks = remove_duptoks(strtoks)
    tokinfolist = []
    # Creates a list of a token's count, and the token itself, and adds this list to tokinfolist.
    for tok in unitoks:
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
# for token in top_toks(glosses, 69):
#     print(str(token[0]) + ". " + token[2] + " - Count: " + str(token[1]))

# # Saves an excel document of the most common tokens.
# save_xlsx("Wb. Common Tokens", top_toks(glosses, 69))
