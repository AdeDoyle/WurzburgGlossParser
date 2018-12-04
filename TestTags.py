"""Level 1"""

from OrderGlosses import order_glosses
from GetSections import get_section
from OpenPages import get_pages


def check_tagset(text, tag):
    """Takes a text and a given tag from an open-close set.
       Checks for the correct amount of each tag in the text.
       Ensures that open and close tags occur in the correct sequence throughout text."""
    intext = text
    optag = "[" + tag + "]"
    cltag = "[/" + tag + "]"
    cltlen = len(cltag)
    opcount = intext.count(optag)
    clcount = intext.count(cltag)
    if opcount != 0 and clcount != 0:
        if opcount != clcount:
            print("Error: Tag-set unbalanced\nOpen-tag count = {}\nClose-tag count = {}".format(opcount, clcount))
            returnstate = "Tag-set broken!"
        elif opcount == clcount:
            eqstatement = "There are {} of each tag".format(opcount)
            print(eqstatement)
            returnstate = "All tags correct!"
        examinetext = intext
        curplace = 0
        for i in range(opcount):
            oplace = examinetext.find(optag)
            cplace = examinetext.find(cltag)
            if cplace < oplace:
                errorstate = "Error: Tag-set number {} is broken.".format(str(i + 1))
                errorline = "Line: " + examinetext[:oplace]
                print(errorstate + "\n" + errorline)
                returnstate = "Tag-set broken!"
                break
            elif oplace < cplace:
                curplace += len(examinetext[cplace + cltlen:])
                examinetext = examinetext[cplace + cltlen:]
        return returnstate


# testtext = order_glosses("\n\n".join(get_section(get_pages("Wurzburg Glosses", 499, 712), "SG")))
# print(check_tagset(testtext, "GLat"))
