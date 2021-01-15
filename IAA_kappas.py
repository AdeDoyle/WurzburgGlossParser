"""Level 1"""

from OpenDocx import get_text
from SaveDocx import save_docx
import re
from sklearn.metrics import cohen_kappa_score
import os.path as op


def find_agreement(annotator_list):
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


def compare_agreement(binary_agreements_list):
    """Takes a list of annotators' individual binary agreement on spacing points as compared to all other annotators.
       Compares each pair of annotators once and returns a list of tuples containing the numbers of each annotator and
       a Cohen's Kappa score for agreement between each two annotators."""
    comparrisons_list = list()
    compared_annotators = list()
    for i, first_annotator in enumerate(binary_agreements_list):
        for j, second_annotator in enumerate(binary_agreements_list):
            if i != j and f'{i} and {j}' not in compared_annotators and f'{j} and {i}' not in compared_annotators:
                comparrisons_list.append((i, j, cohen_kappa_score(first_annotator, second_annotator)))
                compared_annotators.append(f'{i} and {j}')
                compared_annotators.append(f'{j} and {i}')
    return comparrisons_list


# # Create a .docx file containing different annotators' glosses to compare
#
# direct = "IAA Files"
# direct_mod = "IAA Files Mod Irish"
# a0 = get_text(op.join(direct, "IAA_AD"))
# a1ng = get_text(op.join(direct, "IAA_T1_ADon"))
# a2 = get_text(op.join(direct, "IAA_DW"))
# a3 = get_text(op.join(direct, "IAA_JBC"))
# a3ng = get_text(op.join(direct, "IAA_T1_JBC"))
# a4 = get_text(op.join(direct, "IAA_MH"))
# a5 = get_text(op.join(direct, "IAA_TF"))
# a5ng = get_text(op.join(direct, "IAA_T1_TF"))
# a6ng = get_text(op.join(direct, "IAA_expert-41_BB"))
# a7ng = get_text(op.join(direct, "IAA_expert-41_FQ"))
# a8ng = get_text(op.join(direct, "IAA_expert-41_EL"))
# e0 = get_text(op.join(direct, "IAA_expert_BB"))
# e1 = get_text(op.join(direct, "IAA_expert_FQ"))
# e2 = get_text(op.join(direct, "IAA_expert_EL"))
# original = get_text(op.join(direct_mod, "Mod. Ir. Originals"))
# o0 = get_text(op.join(direct_mod, "IAA_CS"))
# o1 = get_text(op.join(direct_mod, "IAA_IG"))
# o2 = get_text(op.join(direct_mod, "IAA_KD"))
# s0 = get_text(op.join(direct_mod, "IAA_TF"))
# s1 = get_text(op.join(direct_mod, "IAA_JBC"))
# s2 = get_text(op.join(direct_mod, "IAA_OD"))
# # annolist = [a0, a1ng, a2, a3, a3ng, a4, a5, a5ng, a6ng, a7ng, a8ng]  # All annotations
# # annolist = [a1ng, a3ng, a5ng, a6ng, a7ng, a8ng]  # All annotators without guidelines
# # annolist = [a0, a2, a3, a4, a5]  # All annotators with guidelines
# # annolist = [e0, e1, e2]  # Expert annotations (includes 1 extra gloss)
# # annolist = [o0, o1, o2]  # Modern Irish, ordinary annotators
# # annolist = [s0, s1, s2]  # Modern Irish, student annotators
# # annolist = [original, o0, o1, o2]  # Modern Irish, ordinary annotators vs original
# # annolist = [original, s0, s1, s2]  # Modern Irish, student annotators vs original
# # annolist = [o0, o1, o2, s0, s1, s2]  # Modern Irish, all annotators
# # annolist = [original, s0, s1, s2, o0, o1, o2]  # Modern Irish, all annotators vs original
#
# allannoslist = list()
# for anno in annolist:
#     glosssplit = anno.split("\n")
#     annoglosslist = list()
#     for gl in glosssplit:
#         # glpat = re.compile(r'\(\d{1,2}[a-d] \d{1,2}[a-d]?\) ')
#         # glpatitir = glpat.finditer(gl)
#         # for i in glpatitir:
#         annoglosslist.append(gl)
#     allannoslist.append(annoglosslist)
# annocombo = list()
# for i in range(len(allannoslist[0])):
#     thiscombo = list()
#     for j in allannoslist:
#         thiscombo.append(j[i])
#     annocombo.append(thiscombo)
# outstring = ""
# for combo in annocombo:
#     count = 0
#     for var in combo:
#         count += 1
#         outstring = outstring + "{}: {}\n".format(str(count), var)
#     outstring = outstring + "\n"
# print(outstring)
# # save_docx(outstring, "Compare Annotators")


# # Gets Kohen's Kappa of Annotators
#
# direct = "IAA Files"
# direct_mod = "IAA Files Mod Irish"
# a0 = get_text(op.join(direct, "IAA_AD"))
# a1ng = get_text(op.join(direct, "IAA_T1_ADon"))
# a2 = get_text(op.join(direct, "IAA_DW"))
# a3 = get_text(op.join(direct, "IAA_JBC"))
# a3ng = get_text(op.join(direct, "IAA_T1_JBC"))
# a4 = get_text(op.join(direct, "IAA_MH"))
# a5 = get_text(op.join(direct, "IAA_TF"))
# a5ng = get_text(op.join(direct, "IAA_T1_TF"))
# a6ng = get_text(op.join(direct, "IAA_expert-41_BB"))
# a7ng = get_text(op.join(direct, "IAA_expert-41_FQ"))
# a8ng = get_text(op.join(direct, "IAA_expert-41_EL"))
# e0 = get_text(op.join(direct, "IAA_expert_BB"))
# e1 = get_text(op.join(direct, "IAA_expert_FQ"))
# e2 = get_text(op.join(direct, "IAA_expert_EL"))
# original = get_text(op.join(direct_mod, "Mod. Ir. Originals"))
# o0 = get_text(op.join(direct_mod, "IAA_CS"))
# o1 = get_text(op.join(direct_mod, "IAA_IG"))
# o2 = get_text(op.join(direct_mod, "IAA_KD"))
# s0 = get_text(op.join(direct_mod, "IAA_TF"))
# s1 = get_text(op.join(direct_mod, "IAA_JBC"))
# s2 = get_text(op.join(direct_mod, "IAA_OD"))
# # annolist = [a0, a2, a3, a4, a5]  # Non-expert annotators only (with guidelines)
# # annolist = [a2, a3, a4, a5]  # Non-expert annotators only, excluding Adrian (with guidelines)
# # annolist = [a0, a1ng, a3ng, a5ng]  # Non-expert annotators only (no guidelines)
# # annolist = [a1ng, a3ng, a5ng]  # Non-expert annotators only, excluding Adrian (no guidelines)
# # annolist = [a6ng, a7ng, a8ng]  # Expert annotators only (no guidelines)
# # annolist = [e0, e1, e2]  # Expert annotators only - 1 extra gloss (no guidelines)
# # annolist = [a0, a1ng, a3ng, a5ng, a6ng, a7ng, a8ng]  # All annotators (no guidelines)
# # annolist = [a1ng, a3ng, a5ng, a6ng, a7ng, a8ng]  # All annotators, excluding Adrian  (no guidelines)
# # annolist = [o0, o1, o2]  # Modern Irish, ordinary annotators
# # annolist = [s0, s1, s2]  # Modern Irish, student annotators
# # annolist = [original, o0, o1, o2]  # Modern Irish, ordinary annotators vs original
# # annolist = [original, s0, s1, s2]  # Modern Irish, student annotators vs original
# # annolist = [o0, o1, o2, s0, s1, s2]  # Modern Irish, all annotators
# # annolist = [original, s0, s1, s2, o0, o1, o2]  # Modern Irish, all annotators vs original
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
# biannos = find_agreement(annolist)
# if all(biannocheck == biannos[0] for biannocheck in biannos):
#     print("Perfect Agreement: all kappa scores = 1.0")
# else:
#     for kappa_score in compare_agreement(biannos):
#         print(f'{kappa_score[0]} and {kappa_score[1]}: {kappa_score[2]}')
#
# # Get average agreement between Annotators
#
# binums = [k[2] for k in compare_agreement(biannos)]
# print(sum(binums) / len(binums))


# # Gets Kohen's Kappa of Annotators to compare against tokenizer
# direct = "IAA Files"
# t0 = get_text(op.join(direct, "IAA_TMod1"))
# t1 = get_text(op.join(direct, "IAA_TMod2"))
# t2 = get_text(op.join(direct, "IAA_TMod3"))
# t3 = get_text(op.join(direct, "IAA_TMod4"))
# t4 = get_text(op.join(direct, "IAA_SgMod1"))
# t5 = get_text(op.join(direct, "IAA_SgMod2"))
#
# a0 = get_text(op.join(direct, "IAA_AD"))
# a1ng = get_text(op.join(direct, "IAA_T1_ADon"))
# a2 = get_text(op.join(direct, "IAA_DW"))
# a3 = get_text(op.join(direct, "IAA_JBC"))
# a3ng = get_text(op.join(direct, "IAA_T1_JBC"))
# a4 = get_text(op.join(direct, "IAA_MH"))
# a5 = get_text(op.join(direct, "IAA_TF"))
# a5ng = get_text(op.join(direct, "IAA_T1_TF"))
# a6ng = get_text(op.join(direct, "IAA_expert-41_BB"))
# a7ng = get_text(op.join(direct, "IAA_expert-41_FQ"))
# a8ng = get_text(op.join(direct, "IAA_expert-41_EL"))
# # annolist = [t0, a0, a2, a3, a4, a5]  # Non-expert annotators only (with guidelines) vs. model
# # annolist = [t0, a0, a1ng, a3ng, a5ng]  # Non-expert annotators only (no guidelines) vs. model
# # annolist = [t0, a6ng, a7ng, a8ng]  # Expert annotators only (no guidelines) vs. model
# # annolist = [t4, a0, a1ng, a3ng, a5ng, a6ng, a7ng, a8ng]  # All annotators (no guidelines) vs. model
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
# biannos = find_agreement(annolist)
# for kappa_score in compare_agreement(biannos)[:len(biannos)-1]:
#     print(f'{kappa_score[0]} and {kappa_score[1]}: {kappa_score[2]}')
#
# binums = [k[2] for k in compare_agreement(biannos)[:len(biannos)-1]]
# print(sum(binums) / len(binums))


# # Gets Kohen's Kappa of test strings
# a1 = "abcdefg hijklmnop qrstuv wxyz"
# a2 = "abcd efg hijk lmnop qrs tuv wx yz"
# a3 = "ab cd ef gh ij kl mn op qr st uv wx yz"
# annolist = [a1, a2, a3]
#
# biannos = find_agreement(annolist)
# print(cohen_kappa_score(biannos[0], biannos[1]))
# print(cohen_kappa_score(biannos[0], biannos[2]))
# print(cohen_kappa_score(biannos[1], biannos[2]))
#
# # Test Agreement function (three ways: 1. run, 2. print, 3. for-loop print)
# find_agreement(annolist)
# print(find_agreement(annolist))
# for i in find_agreement(annolist):
#     print(i)

