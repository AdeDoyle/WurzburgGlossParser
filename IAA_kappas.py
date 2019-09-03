"""Level 1"""

from OpenDocx import get_text
import re
from sklearn.metrics import cohen_kappa_score
import os.path as op


def agreement(annotator_list):
    """Finds inter-annotator agreement on whether a space should follow a given letter
       Returns a binary list for each annotator as compared to other annotators"""
    alist = annotator_list
    purestring = "".join(alist[0].split(" "))
    # Ensure all strings are the same once spaces are removed
    for string in alist:
        if "".join(string.split(" ")) != purestring:
            print("Difference in Non-Space Characters")
    # Create a list to collect disagreement points for each annotator
    disagreelist = []
    for _ in alist:
        disagreelist.append([])
    # For each annotator, compare every character in their (test) string to a (pure) string with no spaces
    # Where the annotator adds a space, add the place number in the pure string to the annotator's disagreement list
    for i in range(len(alist)):
        teststring = alist[i]
        compstring = purestring
        place = 0
        # For each letter in the (pure) string with no spaces,
        # Compare it to the next character in the annotator's string to see if the annotator puts in a space
        # If the annotator puts in a space, add a placement marker to the annotator's disagreement list
        for j in range(len(compstring)):
            # If the two characters are the same in each string, move on to the next character
            if compstring[0] == teststring[0]:
                compstring = compstring[1:]
                teststring = teststring[1:]
            # If the two characters are different in each string, add the place to the annotator's disagreement list
            # Then move on to the next character
            elif compstring[0] != teststring[0]:
                if teststring[0] == " ":
                    disagreelist[i].append(place)
                    compstring = compstring[1:]
                    teststring = teststring[2:]
            place += 1
    # Get a single list of each place in the (pure) string with no spaces that annotators may include spaces
    alllist = list(set(x for l in disagreelist for x in l))
    # Create a binary list for each annotator
    bilists = []
    for _ in alist:
        bilists.append([])
    # For each sequential place each annotator could have a space, add a 1 or 0 to show which
    for annotator in range(len(disagreelist)):
        for disagreement in alllist:
            # If the annotator included a space at a given point, add a 1
            if disagreement in disagreelist[annotator]:
                bilists[annotator].append(1)
            # If the annotator did not include a space at a given point, add a 0
            else:
                bilists[annotator].append(0)
    # Add a space to the end of the string to show agreement on the final word's ending.
    for i in bilists:
        i.append(1)
    return bilists


# # Gets Kohen's Kappa of Annotators
# direct = "IAA Files"
# a0 = get_text(op.join(direct, "IAA_AD"))
# a1 = get_text(op.join(direct, "IAA_DW"))
# a2 = get_text(op.join(direct, "IAA_MH"))
# a3 = get_text(op.join(direct, "IAA_TF"))
# annolist = [a0, a1, a2, a3]
#
# for i in range(len(annolist)):
#     """Clean the text by removing new lines, stars, hyphens, gloss identifiers, and double spaces"""
#     annolist[i] = " ".join(annolist[i].split("\n"))
#     annolist[i] = "".join(annolist[i].split("*"))
#     annolist[i] = "".join(annolist[i].split("-"))
#     rempat = re.compile(r'\(\d\d?\w \d\d?\w?\) ')
#     rempatitir = rempat.finditer(annolist[i])
#     for j in rempatitir:
#         annolist[i] = "".join(annolist[i].split(j.group()))
#     while "  " in annolist[i]:
#         annolist[i] = " ".join(annolist[i].split("  "))
#
# biannos = agreement(annolist)
# print(cohen_kappa_score(biannos[0], biannos[1]))
# print(cohen_kappa_score(biannos[0], biannos[2]))
# print(cohen_kappa_score(biannos[0], biannos[3]))
# print(cohen_kappa_score(biannos[1], biannos[2]))
# print(cohen_kappa_score(biannos[1], biannos[3]))
# print(cohen_kappa_score(biannos[2], biannos[3]))
#
# # Get average agreement between Annotators
# binums = list()
# binums.append(cohen_kappa_score(biannos[0], biannos[1]))
# binums.append(cohen_kappa_score(biannos[0], biannos[2]))
# binums.append(cohen_kappa_score(biannos[0], biannos[3]))
# binums.append(cohen_kappa_score(biannos[1], biannos[2]))
# binums.append(cohen_kappa_score(biannos[1], biannos[3]))
# binums.append(cohen_kappa_score(biannos[2], biannos[3]))
# print(sum(binums) / len(binums))


# # Gets Cappa for Round 1 of Annotation
# direct = "IAA Files"
# a0 = get_text(op.join(direct, "IAA_T1_ADon"))
# a1 = get_text(op.join(direct, "IAA_T1_JBC"))
# a2 = get_text(op.join(direct, "IAA_T1_TF"))
# annolist = [a0, a1, a2]
#
# for i in range(len(annolist)):
#     """Clean the text by removing new lines, stars, hyphens, gloss identifiers, and double spaces"""
#     annolist[i] = " ".join(annolist[i].split("\n"))
#     annolist[i] = "".join(annolist[i].split("*"))
#     annolist[i] = "".join(annolist[i].split("-"))
#     rempat = re.compile(r'\(\d\d?\w \d\d?\w?\) ')
#     rempatitir = rempat.finditer(annolist[i])
#     for j in rempatitir:
#         annolist[i] = "".join(annolist[i].split(j.group()))
#     while "  " in annolist[i]:
#         annolist[i] = " ".join(annolist[i].split("  "))
#
# biannos = agreement(annolist)
# print(cohen_kappa_score(biannos[0], biannos[1]))
# print(cohen_kappa_score(biannos[0], biannos[2]))
# print(cohen_kappa_score(biannos[1], biannos[2]))
#
# # Get average agreement between Annotators Round 1
# binums = list()
# binums.append(cohen_kappa_score(biannos[0], biannos[1]))
# binums.append(cohen_kappa_score(biannos[0], biannos[2]))
# binums.append(cohen_kappa_score(biannos[1], biannos[2]))
# print(sum(binums) / len(binums))


# # Gets Kohen's Kappa of Annotators to compare against tokenizer
# direct = "IAA Files"
# t0 = get_text(op.join(direct, "IAA_TMod1"))
# a0 = get_text(op.join(direct, "IAA_AD"))
# a1 = get_text(op.join(direct, "IAA_DW"))
# a2 = get_text(op.join(direct, "IAA_MH"))
# a3 = get_text(op.join(direct, "IAA_TF"))
# annolist = [t0, a0, a1, a2, a3]
#
# for i in range(len(annolist)):
#     """Clean the text by removing new lines, stars, hyphens, gloss identifiers, and double spaces"""
#     annolist[i] = " ".join(annolist[i].split("\n"))
#     annolist[i] = "".join(annolist[i].split("*"))
#     annolist[i] = "".join(annolist[i].split("-"))
#     rempat = re.compile(r'\(\d\d?\w \d\d?\w?\) ')
#     rempatitir = rempat.finditer(annolist[i])
#     for j in rempatitir:
#         annolist[i] = "".join(annolist[i].split(j.group()))
#     while "  " in annolist[i]:
#         annolist[i] = " ".join(annolist[i].split("  "))
#
# biannos = agreement(annolist)
# print(cohen_kappa_score(biannos[0], biannos[1]))
# print(cohen_kappa_score(biannos[0], biannos[2]))
# print(cohen_kappa_score(biannos[0], biannos[3]))
# print(cohen_kappa_score(biannos[0], biannos[4]))
#
# # Get average agreement between Tokenizer Annotators
# binums = list()
# binums.append(cohen_kappa_score(biannos[0], biannos[1]))
# binums.append(cohen_kappa_score(biannos[0], biannos[2]))
# binums.append(cohen_kappa_score(biannos[0], biannos[3]))
# binums.append(cohen_kappa_score(biannos[0], biannos[4]))
# print(sum(binums) / len(binums))


# # Gets Kohen's Kappa of test strings
# a1 = "abcdefg hijklmnop qrstuv wxyz"
# a2 = "abcd efg hijk lmnop qrs tuv wx yz"
# a3 = "ab cd ef gh ij kl mn op qr st uv wx yz"
# annolist = [a1, a2, a3]
#
# biannos = agreement(annolist)
# print(cohen_kappa_score(biannos[0], biannos[1]))
# print(cohen_kappa_score(biannos[0], biannos[2]))
# print(cohen_kappa_score(biannos[1], biannos[2]))
#
# # Test Agreement function (three ways: 1. run, 2. print, 3. for-loop print)
# agreement(annolist)
# print(agreement(annolist))
# for i in agreement(annolist):
#     print(i)

