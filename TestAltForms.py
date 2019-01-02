"""Level 3"""

from ClearTags import clear_tags
from GetSections import get_section
from OpenPages import get_pages
from Tokenise import space_tokenise, remove_duptoks
import re


def testalts(teststring, text):
    """Takes a string and a full text as input, iterates a regex wildcard through the string, tokenises the text and
       compares each token to each regex generated, returns a list containing each variation of the string found within
       the text."""
    foundlist = []
    textlist = remove_duptoks(space_tokenise(text, True))
    for char in range(len(teststring)):
        stringstart = teststring[:char]
        stringendpoint = len(stringstart) + 1
        stringend = teststring[stringendpoint:]
        stringpat = re.compile(stringstart + r'([\w\s]){0,2}' + stringend)
        stringpatitir = stringpat.finditer(text)
        for i in stringpatitir:
            find = i.group()
            find = find.strip()
            if find not in foundlist:
                if find in textlist:
                    # check if a find has a perfect match in the tokenised text
                    foundlist.append(find)
                elif " " in find:
                    # check if there's an internal space in the find, if so it can't have a matching token
                    foundlist.append(find)
                else:
                    # check if the find has no perfectly matching token, but makes up part of a token
                    for token in textlist:
                        if find in token:
                            if token not in foundlist:
                                foundlist.append(token)
    return foundlist


# testglosses = "pri ma manu, primaa Prima manus, prirna manu, príma Manus, primâ, Primasius"
# for altform in testalts("prima", testglosses):
#     print(altform)

# glosses = clear_tags("\n\n".join(get_section(get_pages("Wurzburg Glosses", 499, 712), "FN")))
# for altform in testalts("prima", glosses):
#     print(altform)
