"""Level 3"""

from OrderGlosses import order_glosses, get_section, get_pages, clear_tags
from RemoveLatin import rep_lat
from RemoveIrish import rep_Ir
from RemoveGlossnums import remove_glossnums
from Tokenise import space_tokenise, remove_duptoks, takefirst


def listCSToks(text, identifier, find="both"):
    """Tests which tokens occur most frequently on code-switching boundaries.
       Tokenises text entered, finds which tokens occur before and after a code-switch identifier token.
       Text entered should have target code-switch language instances replaced with this identifier token."""
    # correct for instances where identifier forms part of a token with another word
    textlist = text.split(identifier)
    insertid = " " + identifier + " "
    text = insertid.join(textlist)
    # correct for multiple spaces created by earlier step
    textlist = text.split("  ")
    text = " ".join(textlist)
    toklist = space_tokenise(text)
    nontoklist = [".", "", "[in", "marg.]"]
    beforelist = []
    afterlist = []
    for i in range(len(toklist)):
        # for every token in the text
        tok = toklist[i]
        if tok == identifier:
            if i == 0:
                # if the first token is the identifier, only look at the following token
                nexttok = toklist[i + 1]
                if nexttok not in nontoklist:
                    afterlist.append(nexttok)
            elif i == len(toklist) - 1:
                # if the last token is the identifier, only look at the preceeding token
                lasttok = toklist[i - 1]
                if lasttok not in nontoklist:
                    beforelist.append(lasttok)
            else:
                # if any other token is the identifier, look at both the word preceeding and following it
                nexttok = toklist[i + 1]
                lasttok = toklist[i - 1]
                if nexttok not in nontoklist:
                    afterlist.append(nexttok)
                if lasttok not in nontoklist:
                    beforelist.append(lasttok)
    if find == "both":
        return beforelist + afterlist
    elif find == "pre":
        return beforelist
    elif find == "post":
        return afterlist


def topCSToks(text, identifier, find="both", occurrences=0):
    """Takes a string/list, a code-switching identifier (list), a find-type, and optional minimum number of occurrences,
       tokenises the string, removes blank tokens, returns list of sublists of tokens and use-count for each token at a
       code-switch point within the string"""
    if isinstance(text, list):
        toklist = []
        for i in range(len(text)):
            thesetoks = listCSToks(text[i], identifier[i], find)
            for j in thesetoks:
                toklist.append(j)
    else:
        toklist = listCSToks(text, identifier, find)
    unitoks = remove_duptoks(toklist)
    tokinfolist = []
    # Creates a list of a token's count, and the token itself, and adds this list to tokinfolist.
    for tok in unitoks:
        if tok != "":
            tokcount = toklist.count(tok)
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


# glosses = remove_glossnums(clear_tags(rep_lat(order_glosses("\n\n".join(get_section(get_pages(
#     "Wurzburg Glosses", 499, 712), "SG"))), "[Latin]", False)))
# latin = clear_tags(rep_Ir(order_glosses("\n\n".join(get_section(get_pages(
#     "Wurzburg Glosses", 499, 712), "SG"))), "[Irish]"))

# # Print the most common Irish tokens used before and after a code switch.
# for token in topCSToks(glosses, "[Latin]", "pre", 5):
#     print(str(token[0]) + ". " + token[2] + " - Count: " + str(token[1]))
# print()
# for token in topCSToks(glosses, "[Latin]", "post", 5):
#     print(str(token[0]) + ". " + token[2] + " - Count: " + str(token[1]))
# print()
# for token in topCSToks(glosses, "[Latin]", "both", 5):
#     print(str(token[0]) + ". " + token[2] + " - Count: " + str(token[1]))

# # Print the most common Latin tokens used before and after a code switch.
# for token in topCSToks(latin, "[Irish]", "pre", 7):
#     print(str(token[0]) + ". " + token[2] + " - Count: " + str(token[1]))
# print()
# for token in topCSToks(latin, "[Irish]", "post", 7):
#     print(str(token[0]) + ". " + token[2] + " - Count: " + str(token[1]))
# print()
# for token in topCSToks(latin, "[Irish]", "both", 7):
#     print(str(token[0]) + ". " + token[2] + " - Count: " + str(token[1]))

# # Combine both Irish and Latin tokens and print the most common used before and after a code switch.
# for token in topCSToks([glosses, latin], ["[Latin]", "[Irish]"], "pre", 10):
#     print(str(token[0]) + ". " + token[2] + " - Count: " + str(token[1]))
# print()
# for token in topCSToks([glosses, latin], ["[Latin]", "[Irish]"], "post", 10):
#     print(str(token[0]) + ". " + token[2] + " - Count: " + str(token[1]))
# print()
# for token in topCSToks([glosses, latin], ["[Latin]", "[Irish]"], "both", 10):
#     print(str(token[0]) + ". " + token[2] + " - Count: " + str(token[1]))
