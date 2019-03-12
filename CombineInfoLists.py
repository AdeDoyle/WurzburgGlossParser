"""Level 4"""

from GetAllInfo import get_allinfo
from GetFullInfo import get_glinfo
from ClearTags import clear_tags
from RemoveGlossnums import remove_glossnums


def combine_infolists(file, startpage=499, stoppage=712):
    """Gets both the Gloss Info list and Latin Info list and combines them."""
    glossinfo = get_glinfo(file, startpage, stoppage)
    del glossinfo[0]
    latinfo = get_allinfo(file, startpage, stoppage)
    del latinfo[0]
    combolist = [["Epistle", "Page", "Folio", "Verse", "Latin", "Lemma", "Lemma Position", "Gloss No.",
                  "Gloss Full-Tags", "Gloss Text", "Gloss Footnotes", "Relevant Footnotes", "Gloss Translation"]]
    if len(glossinfo) == len(latinfo):
        for i in range(len(glossinfo)):
            gloss = glossinfo[i]
            lat = latinfo[i]
            glist = gloss[:3]
            if clear_tags(gloss[4]) == lat[3]:
                # Ensures the gloss from one list matches the same gloss in the other list before combining contents.
                glist.extend(lat[6:])
                glist.extend(lat[4:6])
                glist.extend(gloss[3:])
                combolist.append(glist)
            else:
                print("Error 2.\n%s\n%s" % (clear_tags(gloss[4]), remove_glossnums(lat[0])))
    else:
        print("Error 1: Glosses: %s, Latin: %s" % (len(glossinfo), len(latinfo)))
    return combolist


# for combo in combine_infolists("Wurzburg Glosses", 499, 500):
#     print(combo)
