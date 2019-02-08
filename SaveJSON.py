"""Level 1"""

from CombineInfoLists import combine_infolists
from MakeJSON import make_json
import os


def save_json(content, docname="glosses"):
    """Saves content as text in a .json document file. If a file already exists in the directory with the selected
       filename, the name is edited by adding a number to the end of it before saving. This prevents files with the same
       name from being overwritten"""
    newdocname = docname
    docnamelen = len(docname)
    curdir = os.getcwd()
    exists = os.path.isfile(curdir + "/" + docname + ".json")
    if exists:
        doccount = 0
        while exists:
            newdocname = docname[:docnamelen] + str(doccount)
            exists = os.path.isfile(curdir + "/" + newdocname + ".json")
            doccount += 1
    docname = newdocname
    with open(docname + '.json', 'w', encoding='utf-8') as doc:
        doc.write(content)


# testglosslist = [["Rom", "499", "f. 1a", "1", "foo", "foo", "foo"], ["Rom", "499", "f. 1a", "2", "fee", "fee", "fee"],
#                  ["Rom", "500", "f. 1a", "3", "faa", "faa", "faa"], ["Rom", "500", "f. 1b", "4", "fii", "fii", "fii"],
#                  ["Rom", "501", "f. 1b", "5", "fuu", "fuu", "fuu"], ["Rom", "502", "f. 1b", "6", "roo", "roo", "roo"],
#                  ["Rom", "502", "f. 1b", "7", "ree", "ree", "ree"], ["Rom", "502", "f. 1b", "1", "raa", "raa", "raa"],
#                  ["Rom", "503", "f. 1c", "2", "rii", "rii", "rii"], ["Rom", "503", "f. 1c", "3", "ruu", "ruu", "ruu"],
#                  ["Rom", "504", "f. 1c", "4", "poo", "poo", "poo"], ["Cor", "504", "f. 1c", "5", "pee", "pee", "pee"],
#                  ["Cor", "505", "f. 1d", "1", "paa", "paa", "paa"], ["Cor", "505", "f. 1d", "2", "pii", "pii", "pii"],
#                  ["Phl", "506", "f. 2a", "1", "puu", "puu", "puu"], ["Phl", "506", "f. 2a", "2", "fum", "fum", "fum"]]
# save_json(make_json(testglosslist))

# wbglosslist = combine_infolists("Wurzburg Glosses", 499, 712)
# save_json(make_json(wbglosslist, True))
