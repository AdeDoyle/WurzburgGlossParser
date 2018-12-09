"""Lervel 1, 1, 1, 2"""

from Tokenise import space_tokenise, remove_glossnums, remove_brackets, rem_lat, order_glosses, clear_tags,\
    get_section, get_pages
from OpenDocx import get_text
from matplotlib import pyplot as plt


def find_divs(toklist):
    """Finds possible divisors and divisions for the total number of tokens in the list
       returns a divisions list of division lists, each containing the divisor, and associated division size"""
    t = len(toklist)
    divslist = []
    for i in range(t):
        j = i + 1
        if t % j == 0:
            k = t / j
            divlist = [int(j), int(k)]
            divslist.append(divlist)
    return divslist


def occur_count(toklist, tok, division=0):
    """Divides a list of tokens into sub-lists, returns a list of counts of a given token in each list"""
    if not division:
        division = len(toklist)
    toklists = [toklist[x:x + division] for x in range(0, len(toklist), division)]
    tokcounts = [tok]
    for l in toklists:
        tokcounts.append(l.count(tok))
    return tokcounts


def plot_occur(occurrences):
    """Takes a list of occurrences,
       plots the length of the list on the x axis and the highest number in the list on the y axis"""
    allnos = len(occurrences) - 1
    x = [i + 1 for i in range(allnos)]
    y = occurrences[1:]
    plt.plot(x, y)
    plt.title("Occurrences of token in Glosses")
    plt.xlabel("Glosses (140 Divisions)")
    plt.ylabel("Token Occurrences")
    plt.show()
    return "Process Completed."


def multiplot_occur(occurrenceslist):
    """Takes a list of occurrences,
       plots the length of the list on the x axis and the highest number in the list on the y axis"""
    # ensures all lists are the same length and defines the range of x by that length
    lengths = [len(i) for i in occurrenceslist]
    allnos = lengths[0] - 1
    for length in lengths:
        if length != allnos + 1:
            return "Error: lists of occurrences are of different lengths!"
    x = [i + 1 for i in range(allnos)]
    # plots each token's occurrence list from occurrenceslist
    tokslist = []
    for occurrences in occurrenceslist:
        tok = occurrences[0]
        tokslist.append(tok)
        y = occurrences[1:]
        plt.plot(x, y)
    plt.title("Occurrences of Tokens in Wb. Glosses")
    plt.xlabel("Glosses (Beginning to End)")
    plt.ylabel("Token Occurrences")
    plt.legend(tokslist)
    plt.show()
    return "Process completed."


# glosses = remove_glossnums(remove_brackets(rem_lat(order_glosses(clear_tags(
#     "\n".join(get_section(get_pages("Wurzburg Glosses", 499, 712), "SG")), ["GLat", "ie", "vel"])), True)))
# glosses = remove_glossnums(remove_brackets(rem_lat(clear_tags(
#     get_text("Wb. Prima Manus"), ["GLat", "ie", "vel"]), True)))
# glosses = remove_glossnums(remove_brackets(rem_lat(clear_tags(
#     get_text("Wb. Hand Two"), ["GLat", "ie", "vel"]), True)))
# glosses = remove_glossnums(remove_brackets(rem_lat(clear_tags(
#     get_text("Wb. Hand Three"), ["GLat", "ie", "vel"]), True)))

# glosstoks = space_tokenise(glosses.strip())

# # input the desired tokens to be plotted and size of each division
# t1 = occur_count(glosstoks, "ni", 1633)
# t2 = occur_count(glosstoks, "ní", 1633)
# t3 = occur_count(glosstoks, "dano", 1633)
# t4 = occur_count(glosstoks, "dáno", 1633)


# # prints all divisors and division sizes for the tokenised text's list
# for i in find_divs(glosstoks):
#     print(str(i[0]) + " - " + str(i[1]))

# # prints the list of occurrence counts for each division of the text
# print(occur_count(glosstoks, "ní", 1633))

# # plots one token's frequency distribution throughout the text
# print(plot_occur(t1))

# # plots the frequency distributions throughout the text of multiple tokens
# print(multiplot_occur([t1, t2]))
# print(multiplot_occur([t1, t2, t3, t4]))
