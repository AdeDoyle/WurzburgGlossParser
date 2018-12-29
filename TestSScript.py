# coding=utf8
"""Level 4"""

from TestText import testsectext
import re


def testlatgls(list):
    """Takes a list of lists of page number and latin text as input, finds all gloss markers within the text of
       each page, checks that each gloss number is of higher or equal (13, 14, 14a, etc.) value than the last."""
    noprobs = True
    abc = "abcdefghijklmnopqrstuvwxyz"
    for page in list:
        # identify page numbers, text, and gloss markers within the text of the page
        pageno = page[0]
        pagetext = page[1]
        glpat = re.compile(r'\[(\d{1,2}[a-z]?–)?\d{1,2}[a-z]?\]')
        glpatitir = glpat.finditer(pagetext)
        gllist = []
        for i in glpatitir:
            glossmark = i.group()
            # remove gloss marker brackets
            glplane = glossmark[1:-1]
            if "–" in glplane:
                # split the one instance of a double gloss marker into two separate gloss markers
                separatelist = glplane.split("–")
                for f in separatelist:
                    gllist.append(f)
            else:
                gllist.append(glplane)
        glnumlist = []
        for gl in gllist:
            # check for alphanumeric gloss markers and remove letters where they occur
            glnolet = gl
            for let in abc:
                if let in gl:
                    glnolet = gl[:-1]
            glnum = int(glnolet)
            # create a list of lists of int then str of each gloss number on the page
            glnumlist.append(glnum)
        lastno = 0
        for gl in glnumlist:
            # compare each number against the last to ensure it is equal or higher
            if gl < lastno and gl != 1:
                # if a gloss number is smaller than the last and isn't restarting at 1 (as with a new folio)
                noprobs = False
                print(pageno + " - " + str(lastno) + " preceding " + str(gl) + " (Preceding number higher)")
            # compare each number against the last to ensure it is only one digit higher
            if lastno:
                # if this is not the first gloss on the page (which will often be greater than 0 by more than 1)
                if gl > lastno + 1:
                    # if a gloss number is more than one higher than the last
                    noprobs = False
                    print(pageno + " - " + str(lastno) + " preceding " + str(gl) + " (Non-sequential)")
            lastno = gl
    if noprobs:
        return "All Gloss Markers Ordered Correctly."
    else:
        return "Problem! See log for details."


# latlist = testsectext("Lat", 499, 712)
# irlist = testsectext("SG", 499, 712)
# englist = testsectext("Eng", 499, 712)
# fnlist = testsectext("FN", 499, 712)

# print(testlatgls(latlist))
