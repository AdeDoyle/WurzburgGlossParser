"""Level 2"""

from GetTagText import get_tagtext
import re


def rep_mstags(text, footnotes):
    """Finds all open/close footnotes in a gloss or line of Latin, checks if there is a footnote with an associated
       manuscript replacement tagged and, if so, replaces it returning the gloss/Latin with all replacements made."""
    textstring = text
    tagsintext = []
    taggedtextlist = []
    tagtextpat = re.compile(r'\[/[a-z]\]')
    tagtextitir = tagtextpat.finditer(textstring)
    for tagfound in tagtextitir:
        closetag = tagfound.group()
        opentag = "[" + closetag[2:]
        tag = opentag[1:-1]
        tagsintext.append(tag)
        tagtextlist = get_tagtext(textstring, tag)
        for taggedtext in tagtextlist:
            tagstring = opentag + taggedtext + closetag
            taggedtextlist.append(tagstring)
    for tag in tagsintext:
        tagplace = tagsintext.index(tag)
        replacetext = taggedtextlist[tagplace]
        for footnote in footnotes:
            if footnote[:2] == tag + " ":
                if "[/Rep]" in footnote:
                    replacementlist = get_tagtext(footnote, "Rep")
                    repstring = "[Rep]" + replacementlist[0] + "[/Rep]"
                    textstringlist = textstring.split(replacetext)
                    textstring = repstring.join(textstringlist)
    return textstring


def rep_legtags(text, footnotes):
    """Finds all open/close footnotes in a gloss or line of Latin, checks if there is a footnote with an associated
       suggested reading tagged and, if so, replaces it returning the gloss/Latin with all replacements made."""
    textstring = text
    tagsintext = []
    taggedtextlist = []
    tagtextpat = re.compile(r'\[/[a-z]\]')
    tagtextitir = tagtextpat.finditer(textstring)
    for tagfound in tagtextitir:
        closetag = tagfound.group()
        opentag = "[" + closetag[2:]
        tag = opentag[1:-1]
        tagsintext.append(tag)
        tagtextlist = get_tagtext(textstring, tag)
        for taggedtext in tagtextlist:
            tagstring = opentag + taggedtext + closetag
            taggedtextlist.append(tagstring)
    for tag in tagsintext:
        tagplace = tagsintext.index(tag)
        replacetext = taggedtextlist[tagplace]
        for footnote in footnotes:
            if footnote[:2] == tag + " ":
                if "[/LRep]" in footnote:
                    replacementlist = get_tagtext(footnote, "LRep")
                    repstring = "[LRep]" + replacementlist[0] + "[/LRep]"
                    textstringlist = textstring.split(replacetext)
                    textstring = repstring.join(textstringlist)
    return textstring


# testgloss = "This is [a]a[/a] nice [b]glos[/b] used [c]for[/c] testing."
# testFN = ["a MS. [Rep]the[/Rep]\n", "b leg. [LRep]gloss[/LRep]\n", "c MS. [Rep]when[/Rep]\n", "d MS. [Rep]by[/Rep]\n"]
# print(rep_mstags(testgloss, testFN))
# print(rep_legtags(testgloss, testFN))
# print(rep_mstags(rep_legtags(testgloss, testFN), testFN))
