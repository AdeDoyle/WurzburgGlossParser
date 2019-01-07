"""Level 1"""

from ClearTags import clear_tags
from GetSections import get_section
from OpenPages import get_pages
import re


def order_latlist_page(file):
    """Takes a single page of Latin text. Orders the text by removing any new lines where no new numbers are marked.
       Returns a list of ordered lines for the page."""
    latext = file
    # Make a list of all the strings on the page which start a line of latin text (eg. ['[f. 1a]', 'VII. ', '23. ']).
    latextlist = latext.split("\n")
    linestarts = []
    linestartpat = re.compile(r'((^\[f\. \d{1,2}[a-d]\])([IVX]{1,4}\. )?(\d{1,2}, )?(\d{1,2}\. )?)')
    for line in range(len(latextlist)):
        linestartitir = linestartpat.finditer(latextlist[line])
        for i in linestartitir:
            find = i.group()
            if find not in linestarts:
                linestarts.append(find)
    linestartpat = re.compile(r'((^[IVX]{1,4}\. )(\d{1,2}, )?(\d{1,2}\. )?)')
    for line in range(len(latextlist)):
        linestartitir = linestartpat.finditer(latextlist[line])
        for i in linestartitir:
            find = i.group()
            if find not in linestarts:
                linestarts.append(find)
    linestartpat = re.compile(r'(^(\d{1,2}, )?\d{1,2}\. )')
    for line in range(len(latextlist)):
        linestartitir = linestartpat.finditer(latextlist[line])
        for i in linestartitir:
            find = i.group()
            if find not in linestarts:
                linestarts.append(find)
    # Put the list in order as per the appearance of each of its items in the latin text on the page.
    orderedlinestarts = []
    for line in latextlist:
        for start in linestarts:
            startlen = len(start)
            if line[:startlen] == start:
                orderedlinestarts.append(start)
    # Reassemble page's lines with only accepted line-starts by replacing newlines with spacing between line-starts.
    # Find each line-start, and the upcoming one, combine every line from the line-start until the next into one line.
    lineslist = []
    firstprob = True
    for start in orderedlinestarts:
        startlen = len(start)
        thisstartlist = []
        if start != orderedlinestarts[-1]:
            # If this isn't the last line-start in the list...
            if firstprob:
                nextstart = orderedlinestarts[orderedlinestarts.index(start) + 1]
            else:
                nextstart = orderedlinestarts[orderedlinestarts.index(start) + 2]
            nslen = len(nextstart)
            if start == nextstart and firstprob:
                # On p. 647 and 697 there are repeating line numbers. Separate them into different lines.
                for line in latextlist:
                    if line == latextlist[0] or line == latextlist[1]:
                        thisstartlist.append(line)
                # remove all used lines from latextlist outside the for loop that uses the list.
                for copyline in thisstartlist:
                    if copyline in latextlist:
                        latextlist.remove(copyline)
                firstprob = False
            else:
                # If this is not a duplicate line-start number from a problem page...
                for line in latextlist:
                    if line[:nslen] != nextstart:
                        # if this isn't the start of what should be a new line...
                        thisstartlist.append(line)
                    else:
                        break
                # remove all used lines from latextlist outside the for loop that uses the list.
                for copyline in thisstartlist:
                    if copyline in latextlist:
                        latextlist.remove(copyline)
        else:
            # If this is the last line-start in the list...
            for line in latextlist:
                thisstartlist.append(line)
        lineslist.append(" ".join(thisstartlist))
    for i in range(len(orderedlinestarts)):
        checkline = lineslist[i]
        checkstart = orderedlinestarts[i]
        if checkline[:len(checkstart)] != checkstart:
            return ["Error: Line '" + checkline + "' does not begin with the expected marker: '" + checkstart + "'."]
    return lineslist


def order_latlist(file):
    """Takes multiple pages of latin text where pages are separated by a double space ("\n\n").
       Returns a list of ordered lines for the entire file."""
    pages = file.split("\n\n")
    orderedpageslist = []
    for page in pages:
        orderedglosses = order_latlist_page(page)
        orderedpageslist.append(orderedglosses)
    orderedpages = []
    for orderedpage in orderedpageslist:
        for orderedgloss in orderedpage:
            orderedpages.append(orderedgloss)
    return orderedpages


def order_latin(file):
    """Takes multiple pages of latin text where pages are separated by a double space ("\n\n").
       Returns a single string of ordered lines for the entire file."""
    latlist = order_latlist(file)
    linesstring = "\n".join(latlist)
    return linesstring


# latin = clear_tags("\n\n".join(get_section(get_pages("Wurzburg Glosses", 499, 712), "Lat")), "fol")
# latin = "\n\n".join(get_section(get_pages("Wurzburg Glosses", 499, 712), "Lat"))
# order_latlist_page(latin)
# print(order_latlist_page(latin))
# for i in order_latlist_page(latin):
#     print(i)
# print(order_latlist(latin))
# print(order_latin(latin))
