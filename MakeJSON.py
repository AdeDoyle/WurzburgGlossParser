"""Level 1"""

from CombineInfoLists import combine_infolists


def make_json(glosslist, headers=False):
    """Takes a list of sublists, each sublist containing a gloss and related information, returns a json package for
       each gloss"""
    jsonformat0 = """[x]"""
    jsonformat1 = """{
    "epistle": "[x]",
    "folios": [y]
}"""
    jsonformat2 = """{
        "folio": "[x]",
        "glosses": [y]
    }"""
    jsonformat3 = """{
            "tphPage": "[a]",
            "glossNo": "[b]",
            "latLine": "[c]",
            "latin": "[d]",
            "lemma": "[e]",
            "glossFullTags": "[g]",
            "glossText": "[x]",
            "glossFNs": "[y]"
        }"""
    if headers:
        glosslist = glosslist[1:]
    #  This gets level 3
    jsonglosslist1 = []
    for gloss in glosslist:
        jsonblank = jsonformat3
        e = gloss[0]
        p = gloss[1]
        f = gloss[2]
        ll = gloss[3]
        la = gloss[4]
        le = gloss[5]
        gn = gloss[6]
        g = gloss[7]
        gt = gloss[8]
        gfn = gloss[9]
        jsonblank = jsonblank[:jsonblank.find("[a]")] + str(p) + jsonblank[jsonblank.find("[a]") + 3:]
        jsonblank = jsonblank[:jsonblank.find("[b]")] + gn + jsonblank[jsonblank.find("[b]") + 3:]
        jsonblank = jsonblank[:jsonblank.find("[c]")] + ll + jsonblank[jsonblank.find("[c]") + 3:]
        jsonblank = jsonblank[:jsonblank.find("[d]")] + la + jsonblank[jsonblank.find("[d]") + 3:]
        jsonblank = jsonblank[:jsonblank.find("[e]")] + le + jsonblank[jsonblank.find("[e]") + 3:]
        jsonblank = jsonblank[:jsonblank.find("[g]")] + g + jsonblank[jsonblank.find("[g]") + 3:]
        jsonblank = jsonblank[:jsonblank.find("[x]")] + gt + jsonblank[jsonblank.find("[x]") + 3:]
        jsonblank = jsonblank[:jsonblank.find("[y]")] + gfn + jsonblank[jsonblank.find("[y]") + 3:]
        jsonblanklist = [e, f, jsonblank]
        jsonglosslist1.append(jsonblanklist)
    jsonglosslist2 = []
    curep = "unknown"
    curfol = "unknown"
    for gloss in jsonglosslist1:
        lastep = curep
        lastfol = curfol
        curep = gloss[0]
        curfol = gloss[1]
        curgloss = gloss[2]
        if gloss != jsonglosslist1[-1]:
            if lastep == "unknown" and lastfol == "unknown":
                epfollist = [curgloss]
            elif curep == lastep and curfol == lastfol:
                epfollist.append(curgloss)
            else:
                epfolstr = ",\n        ".join(epfollist)
                jsonglosslist2.append([lastep, lastfol, epfolstr])
                epfollist = [curgloss]
        else:
            if curep == lastep and curfol == lastfol:
                epfollist.append(curgloss)
                epfolstr = ",\n        ".join(epfollist)
                jsonglosslist2.append([lastep, lastfol, epfolstr])
            else:
                epfolstr = ",\n        ".join(epfollist)
                jsonglosslist2.append([lastep, lastfol, epfolstr])
                jsonglosslist2.append([curep, curfol, curgloss])
    #  This gets level 2
    jsonfollist1 = []
    for gloss in jsonglosslist2:
        jsonblank = jsonformat2
        e = gloss[0]
        f = gloss[1]
        jsoninsert = gloss[2]
        jsonblank = jsonblank[:jsonblank.find("[x]")] + f + jsonblank[jsonblank.find("[x]") + 3:]
        jsonblank = jsonblank[:jsonblank.find("y]")] + jsoninsert + jsonblank[jsonblank.find("y]") + 1:]
        jsonblanklist = [e, jsonblank]
        jsonfollist1.append(jsonblanklist)
    jsonfollist2 = []
    curep = "unknown"
    for fol in jsonfollist1:
        lastep = curep
        curep = fol[0]
        curfol = fol[1]
        if fol != jsonfollist1[-1]:
            if lastep == "unknown":
                eplist = [curfol]
            elif curep == lastep:
                eplist.append(curfol)
            else:
                epstr = ",\n    ".join(eplist)
                jsonfollist2.append([lastep, epstr])
                eplist = [curfol]
        else:
            if curep == lastep:
                eplist.append(curfol)
                epstr = ",\n    ".join(eplist)
                jsonfollist2.append([lastep, epstr])
            else:
                epstr = ",\n    ".join(eplist)
                jsonfollist2.append([lastep, epstr])
                jsonfollist2.append([curep, curfol])
    #  This gets level 1
    jsoneplist = []
    for fol in jsonfollist2:
        jsonblank = jsonformat1
        e = fol[0]
        jsonfol = fol[1]
        jsonblank = jsonblank[:jsonblank.find("[x]")] + e + jsonblank[jsonblank.find("[x]") + 3:]
        jsonblank = jsonblank[:jsonblank.find("y]")] + jsonfol + jsonblank[jsonblank.find("y]") + 1:]
        jsoneplist.append(jsonblank)
    #  This gets level 0
    jsonepstr = ",\n".join(jsoneplist)
    jsonoutput = jsonformat0[:jsonformat0.find("x]")] + jsonepstr + jsonformat0[jsonformat0.find("x]") + 1:]
    return jsonoutput


# wbglosslist = combine_infolists("Wurzburg Glosses", 499, 509)
# print(make_json(wbglosslist, True))
