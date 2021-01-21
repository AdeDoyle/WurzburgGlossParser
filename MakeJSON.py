"""Level 1"""

import re
from CombineInfoLists import combine_infolists
from conllu import parse, TokenList
import json


def make_json(glosslist, headers=False):
    """Takes a list of sublists, each sublist containing a gloss and related information, returns a json package for
       each gloss"""
    # Create a high level blank of the JSON document to hold all data
    jsonformat0 = """[x]"""
    # Create a high-mid level blank to be reused in the JSON document each time a new epistle begins
    jsonformat1 = """{
    "epistle": "[x]",
    "folios": [y]
}"""
    # Create a low-mid level blank to be reused in the JSON document each time a new folio begins
    jsonformat2 = """{
        "folio": "[x]",
        "glosses": [y]
    }"""
    # Create a low level blank to be reused in the JSON document for each new gloss
    jsonformat3 = """{
            "tphPage": "[p]",
            "glossNo": "[gn]",
            "latLine": "[v]",
            "latin": "[la]",
            "lemma": "[le]",
            "lemPos": "[lp]",
            "glossFullTags": "[g]",
            "glossHand": "[h]",
            "glossText": "[gt]",
            "glossTokens1": "",
            "glossTokens2": "",
            "glossFNs": "[gfn]",
            "footnotes": "[fn]",
            "newNotes": "[nn]",
            "glossTrans": "[tr]"
        }"""
    if headers:
        glosslist = glosslist[1:]
    # Identify all low level data for each gloss from the combined information list of glosses
    jsonglosslist1 = []
    foliohandswap = False
    for gloss in glosslist:
        jsonblank = jsonformat3
        e = gloss[0]
        p = gloss[1]
        f = gloss[2]
        v = gloss[3]
        la = gloss[4]
        le = gloss[5]
        lp = gloss[6]
        gn = gloss[7]
        g = gloss[8]
        gt = gloss[9]
        gfn = gloss[10]
        fn = gloss[11]
        an = gloss[12]
        gtr = gloss[13]
        h = "Hand Two"
        if f == "f. 33a":
            foliohandswap = True
        if foliohandswap:
            h = "Hand Three"
        if fn:
            for i in fn:
                if "prima" in i:
                    h = "Hand One (Prima Manus)"
                    # print(i)
        mixed_hand_list = ["8d3", "8d13", "11b3", "17b4", "17d15", "21d6", "24b8"]
        if an:
            if "a prima manu" in an or "prima manus" in an:
                if f[3:] + gn in mixed_hand_list:
                    if foliohandswap:
                        h = "Hand Three"
                    else:
                        h = "Hand Two"
                    h = f"Hand One (Prima Manus) and {h}"
                elif "not <em>a prima manu</em>" in an:
                    if foliohandswap:
                        h = "Hand Three"
                    else:
                        h = "Hand Two"
                else:
                    h = "Hand One (Prima Manus)"
        # Replace the marker for each datum in the low level JSON blank with appropriate data for the gloss
        jsonblank = jsonblank[:jsonblank.find("[p]")] + str(p) + jsonblank[jsonblank.find("[p]") + 3:]
        jsonblank = jsonblank[:jsonblank.find("[gn]")] + gn + jsonblank[jsonblank.find("[gn]") + 4:]
        jsonblank = jsonblank[:jsonblank.find("[v]")] + v + jsonblank[jsonblank.find("[v]") + 3:]
        jsonblank = jsonblank[:jsonblank.find("[la]")] + la + jsonblank[jsonblank.find("[la]") + 4:]
        jsonblank = jsonblank[:jsonblank.find("[le]")] + le + jsonblank[jsonblank.find("[le]") + 4:]
        jsonblank = jsonblank[:jsonblank.find("[lp]")] + str(lp) + jsonblank[jsonblank.find("[lp]") + 4:]
        jsonblank = jsonblank[:jsonblank.find("[g]")] + g + jsonblank[jsonblank.find("[g]") + 3:]
        jsonblank = jsonblank[:jsonblank.rfind("[h]")] + h + jsonblank[jsonblank.rfind("[h]") + 3:]
        jsonblank = jsonblank[:jsonblank.find("[gt]")] + gt + jsonblank[jsonblank.find("[gt]") + 4:]
        jsonblank = jsonblank[:jsonblank.find("[gfn]")] + gfn + jsonblank[jsonblank.find("[gfn]") + 5:]
        if not fn:
            jsonblank = jsonblank[:jsonblank.find("[fn]") - 1] + "null" + jsonblank[jsonblank.find("[fn]") + 5:]
        elif fn:
            if isinstance(fn, list):
                fncombine = '",\n                "'.join(fn)
                fn = '[\n                "' + fncombine + '"\n            ]'
                if "***" in fn:
                    starpat = re.compile(r' \*\*\*.*\*\*\*')
                    starpatitir = starpat.finditer(fn)
                    for starfind in starpatitir:
                        fnlist = fn.split(starfind.group())
                        fn = "".join(fnlist)
                jsonblank = jsonblank[:jsonblank.find("[fn]") - 1] + fn + jsonblank[jsonblank.find("[fn]") + 5:]
        if not an:
            jsonblank = jsonblank[:jsonblank.find("[nn]") - 1] + "null" + jsonblank[jsonblank.find("[nn]") + 5:]
        elif an:
            jsonblank = jsonblank[:jsonblank.find("[nn]")] + an + jsonblank[jsonblank.find("[nn]") + 4:]
        jsonblank = jsonblank[:jsonblank.find("[tr]")] + gtr + jsonblank[jsonblank.find("[tr]") + 4:]
        jsonblanklist = [e, f, jsonblank]
        jsonglosslist1.append(jsonblanklist)
    # Identify all low-mid level data for each new folio from the combined information list of glosses
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


def make_lex_json(conllu_file):
    with open(conllu_file, "r", encoding="utf-8") as conllu_file_import:
        text_file = conllu_file_import.read()
    sentences = parse(text_file)
    all_words = list()
    for sentence in sentences:
        words = [(i.get("lemma"), i.get("form").lower(), i.get("upos"), i.get("feats")) for i in sentence]
        words = [i if i[3] else tuple([j for j in i[:3]] + ["_"]) for i in words]
        words = [i if i[3] == "_"
                 else tuple([j for j in i[:3]] + ["|".join([f"{k}={i[3].get(k)}" for k in i[3]])]) for i in words]
        all_words = all_words + words
    all_words = sorted(list(set([i for i in all_words if i[0] not in ['_', 'False']])))
    all_POS = sorted(list(set([i[2] for i in all_words])))
    json_file = [{
        "part_of_speech": pos,
        "lemmata": [i for i in all_words if i[2] == pos]
    } for pos in all_POS]
    for pos_data in json_file:
        relevant_lem_data = pos_data.get("lemmata")
        relevant_lemmata = sorted(list(set([i[0] for i in relevant_lem_data])))
        pos_data["lemmata"] = [{
            "lemma": lemma,
            "tokens": [j for j in relevant_lem_data if j[0] == lemma]
        } for lemma in relevant_lemmata]
        for lemmata_data in pos_data.get("lemmata"):
            relevant_tok_data = lemmata_data.get("tokens")
            relevant_tokens = sorted(list(set([k[1] for k in relevant_tok_data])))
            lemmata_data["tokens"] = [{
                "token": token,
                "feature_sets": [l[3].split("|") for l in relevant_tok_data if l[1] == token]
            } for token in relevant_tokens]
            for token_data in lemmata_data.get("tokens"):
                relevant_features_data = token_data.get("feature_sets")
                token_data["feature_sets"] = [{
                    "feature_set": m + 1,
                    "features": n
                } if n != ['_'] else {
                    "feature_set": m + 1,
                    "features": None
                } for m, n in enumerate(relevant_features_data)]
                for feature_data in token_data.get("feature_sets"):
                    relative_features = feature_data.get("features")
                    if relative_features:
                        feature_data["features"] = [{
                            o.split("=")[0]: o.split("=")[1]for o in relative_features
                        }]
    json_file = json.dumps(json_file, indent=4, ensure_ascii=False)
    return json_file


if __name__ == "__main__":

    wbglosslist = combine_infolists("Wurzburg Glosses", 499, 509)
    print(make_json(wbglosslist, True))
    # wbglosslist = combine_infolists("Wurzburg Glosses", 704, 705)
    # print(make_json(wbglosslist, True))

    # make_lex_json("sga_dipsgg-ud-test_split_POS.conllu")
    print(make_lex_json("sga_dipsgg-ud-test_split_POS.conllu"))
    # # make_lex_json("sga_dipsgg-ud-test_combined_POS.conllu")
    # print(make_lex_json("sga_dipsgg-ud-test_combined_POS.conllu"))
