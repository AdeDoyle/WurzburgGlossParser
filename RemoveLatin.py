"""Level 1"""

from RemoveNewlines import remove_newlines
from OrderGlosses import order_glosses, get_section, get_pages, clear_tags


def rep_lat(glosstext, strong=False):
    """Takes glosses as input. Replaces all Latin text with ellipsis."""
    workingtext = glosstext
    ellip = "…"
    latinsts = workingtext.count("[GLat]")
    if "[GLat]" in workingtext:
        if latinsts != workingtext.count("[/GLat]"):
            return "Error: Uneven number of open and close tags for Gloss Latin."
        else:
            for i in range(latinsts):
                workingtext = workingtext[:workingtext.find("[GLat]")] + ellip +\
                              workingtext[workingtext.find("[/GLat]") + 7:]
    if strong:
        ieinsts = workingtext.count("[ie]")
        velinsts = workingtext.count("[vel]")
        etcinsts = workingtext.count("[etc]")
        if "[ie]" in workingtext:
            if ieinsts != workingtext.count("[/ie]"):
                return "Error: Uneven number of open and close tags for .i."
            else:
                for j in range(ieinsts):
                    workingtext = workingtext[:workingtext.find("[ie]")] + ellip + \
                                  workingtext[workingtext.find("[/ie]") + 5:]
        if "[vel]" in workingtext:
            if velinsts != workingtext.count("[/vel]"):
                return "Error: Uneven number of open and close tags for ɫ."
            else:
                for k in range(velinsts):
                    workingtext = workingtext[:workingtext.find("[vel]")] + ellip + \
                                  workingtext[workingtext.find("[/vel]") + 6:]
        if "[etc]" in workingtext:
            if etcinsts != workingtext.count("[/etc]"):
                return "Error: Uneven number of open and close tags for rl."
            else:
                for l in range(etcinsts):
                    workingtext = workingtext[:workingtext.find("[etc]")] + ellip + \
                                  workingtext[workingtext.find("[/etc]") + 6:]
    if ellip in workingtext:
        workingtext = "[GLat]…[/GLat]".join(workingtext.split(ellip))
    return workingtext


def rem_lat(glosstext, strong=False):
    """Takes glosses as input. Removes all Latin text and resultant double spacing."""
    workingtext = glosstext
    latinsts = workingtext.count("[GLat]")
    if "[GLat]" in workingtext:
        if latinsts != workingtext.count("[/GLat]"):
            return "Error: Uneven number of open and close tags for Gloss Latin!"
        else:
            for i in range(latinsts):
                workingtext = workingtext[:workingtext.find("[GLat]")] + workingtext[workingtext.find("[/GLat]") + 7:]
    if strong:
        ieinsts = workingtext.count("[ie]")
        velinsts = workingtext.count("[vel]")
        etcinsts = workingtext.count("[etc]")
        if "[ie]" in workingtext:
            if ieinsts != workingtext.count("[/ie]"):
                return "Error: Uneven number of open and close tags for .i."
            else:
                for j in range(ieinsts):
                    workingtext = workingtext[:workingtext.find("[ie]")] + workingtext[workingtext.find("[/ie]") + 5:]
        if "[vel]" in workingtext:
            if velinsts != workingtext.count("[/vel]"):
                return "Error: Uneven number of open and close tags for ɫ."
            else:
                for k in range(velinsts):
                    workingtext = workingtext[:workingtext.find("[vel]")] + workingtext[workingtext.find("[/vel]") + 6:]
        if "[etc]" in workingtext:
            if etcinsts != workingtext.count("[/etc]"):
                return "Error: Uneven number of open and close tags for rl."
            else:
                for l in range(etcinsts):
                    workingtext = workingtext[:workingtext.find("[etc]")] + workingtext[workingtext.find("[/etc]") + 6:]
    if "  " in workingtext:
        while "  " in workingtext:
            workingtext = " ".join(workingtext.split("  "))
    return workingtext


# glosses = order_glosses("\n\n".join(get_section(get_pages("Wurzburg Glosses", 499, 712), "SG")))
# glosses = "this is [GLat]some[/GLat] text [ie].i.[/ie] [GLat]that[/GLat] I made up on the     spot"
# print(rep_lat(glosses, True))
# print(remove_newlines(rem_lat(glosses, False)))
