"""Level 1"""

from OrderGlosses import order_glosses, get_section, get_pages, clear_tags


def rep_Ir(glosstext, repchar="…"):
    """Takes glosses as input. Replaces all Irish text text with ellipsis (or other selected replace-character."""
    oplat = "[GLat]"
    clat = "[/GLat]"
    latlist = []
    if glosstext.find(oplat) != 0:
        latlist.append("")
        glosstext = glosstext[glosstext.find(oplat):]
    while oplat in glosstext:
        lat = glosstext[:glosstext.find(clat) + 7]
        latlist.append(lat)
        glosstext = glosstext[glosstext.find(clat) + 7:]
        if oplat in glosstext:
            glosstext = glosstext[glosstext.find(oplat):]
        else:
            if glosstext:
                latlist.append("")
    repchar = " " + repchar + " "
    latintext = repchar.join(latlist)
    latintext = latintext.strip()
    return latintext


# glosses = order_glosses("\n\n".join(get_section(get_pages("Wurzburg Glosses", 499, 712), "SG")))
# glosses = clear_tags(order_glosses("\n\n".join(get_section(get_pages("Wurzburg Glosses", 499, 712), "SG"))), "GLat")
# print(rep_Ir(glosses))
