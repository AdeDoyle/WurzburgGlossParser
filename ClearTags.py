"""Level 1"""

from OpenPages import get_pages


def clear_tags(file, exceptions=[]):
    """Clears all tags out of the text except those listed as exceptions, replacing them with original TPH markers where
       they were originally identified by use of various bracket types"""
    filetext = file
    taglist = ["H1", "H2", "Lat", "SG", "Eng", "FN", "GLat", "fol", "num", "let", "Rep", "ie", "vel", "Com",
               "Con", "Sup", "Res", "STOP", "Nam", "MRep", "LRep"]
    for tag in taglist:
        if tag not in exceptions:
            if tag == "fol":
                for i in range(1, 34 + 1):
                    for l in ["a", "b", "c", "d"]:
                        opentag = "[f. " + str(i) + l + "]"
                        closetag = "[/f. " + str(i) + l + "]"
                        if opentag in filetext:
                            filetextlist = filetext.split(opentag)
                            filetext = "".join(filetextlist)
                        if closetag in filetext:
                            filetextlist = filetext.split(closetag)
                            filetext = "".join(filetextlist)
            elif tag == "num":
                for i in range(99):
                    opentag = "[" + str(i) + "]"
                    closetag = "[/" + str(i) + "]"
                    if opentag in filetext:
                        filetextlist = filetext.split(opentag)
                        filetext = "".join(filetextlist)
                    if closetag in filetext:
                        filetextlist = filetext.split(closetag)
                        filetext = "".join(filetextlist)
                    for j in range(99):
                        opentag = "[" + str(i) + "–" + str(j) + "]"
                        closetag = "[/" + str(i) + "–" + str(j) + "]"
                        if opentag in filetext:
                            filetextlist = filetext.split(opentag)
                            filetext = "".join(filetextlist)
                        if closetag in filetext:
                            filetextlist = filetext.split(closetag)
                            filetext = "".join(filetextlist)
            elif tag == "let":
                for l in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
                          "t", "u", "v", "w", "x", "y", "z"]:
                    opentag = "[" + l + "]"
                    closetag = "[/" + l + "]"
                    if opentag in filetext:
                        filetextlist = filetext.split(opentag)
                        filetext = "".join(filetextlist)
                    if closetag in filetext:
                        filetextlist = filetext.split(closetag)
                        filetext = "".join(filetextlist)
            elif tag == "Com":
                opentag = "[" + tag + "]"
                closetag = "[/" + tag + "]"
                if opentag in filetext:
                    filetextlist = filetext.split(opentag)
                    filetext = "[".join(filetextlist)
                if closetag in filetext:
                    filetextlist = filetext.split(closetag)
                    filetext = "]".join(filetextlist)
            elif tag == "Sup":
                opentag = "[" + tag + "]"
                closetag = "[/" + tag + "]"
                if opentag in filetext:
                    filetextlist = filetext.split(opentag)
                    filetext = "[".join(filetextlist)
                if closetag in filetext:
                    filetextlist = filetext.split(closetag)
                    filetext = "]".join(filetextlist)
            elif tag == "Res":
                opentag = "[" + tag + "]"
                closetag = "[/" + tag + "]"
                if opentag in filetext:
                    filetextlist = filetext.split(opentag)
                    filetext = "(".join(filetextlist)
                if closetag in filetext:
                    filetextlist = filetext.split(closetag)
                    filetext = ")".join(filetextlist)
            else:
                opentag = "[" + tag + "]"
                closetag = "[/" + tag + "]"
                if opentag in filetext:
                    filetextlist = filetext.split(opentag)
                    filetext = "".join(filetextlist)
                if closetag in filetext:
                    filetextlist = filetext.split(closetag)
                    filetext = "".join(filetextlist)
    return filetext


def clear_spectags(file, taglist=[]):
    """Clears only the specified tag or tags from the text using the clear_tags function"""
    alltags = ["H1", "H2", "Lat", "SG", "Eng", "FN", "GLat", "fol", "num", "let", "Rep", "ie", "vel", "Com", "Con",
               "Sup", "Res", "STOP", "Nam", "MRep", "LRep"]
    excepted = []
    for exception in alltags:
        if exception not in taglist:
            excepted.append(exception)
    untaggedtext = clear_tags(file, excepted)
    return untaggedtext


# glosses = get_pages("Wurzburg Glosses", 499, 509)

# print(clear_tags(glosses, ["Lat", "SG", "Eng", "FN"]))
# print(clear_tags(glosses))

# print(clear_spectags(glosses, ["Lat", "SG", "Eng", "FN"]))
# print(clear_spectags(glosses))
