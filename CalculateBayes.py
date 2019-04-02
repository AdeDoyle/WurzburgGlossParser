from PrepareHandContent import compile_tokenised_glosslist, combinelists, get_inditokcount, get_unitoks


def basic_bayes(p2g1, p1, p2):
    """Calculates the probability 1 (a scribe) given the probability of 2 (a word/bigram/contraction etc.)"""
    topline = p2g1 * p1
    bottomline = p2
    return topline / bottomline


def bayes_tok(tok, hand):
    """Takes a token, and a hand number.
       Uses Bayes theorem to calculate the probability of the given token being used by the given hand."""
    glosshands = ["Wb. All Glosses", "Wb. Prima Manus", "Wb. Hand Two", "Wb. Hand Three"]
    allglosstoks = compile_tokenised_glosslist(glosshands[0])
    allcurhand = compile_tokenised_glosslist(glosshands[hand])
    # probability of a given token
    # (number of times token is used by all scribes / total number of tokens used by all scribes)
    pw = get_inditokcount(tok, allglosstoks) / len(combinelists(allglosstoks))
    # probability of a given scribe
    # (total number of tokens used by a given scribe / total number of tokens used by all scribes)
    ps = len(combinelists(allcurhand)) / len(combinelists(allglosstoks))
    # probability of a given token given a scribe
    # (number of times a given token is used by given scribe / total number of tokens used by a given scribe)
    pwgs = get_inditokcount(tok, allcurhand) / len(combinelists(allcurhand))
    return basic_bayes(pwgs, ps, pw)


# Defines a function which gets the first element in a list.
def takefirst(elem):
    return elem[0]


# commontoks = []
# pmunitoks = get_unitoks(compile_tokenised_glosslist("Wb. Prima Manus"))
# h2unitoks = get_unitoks(compile_tokenised_glosslist("Wb. Hand Two"))
# h3unitoks = get_unitoks(compile_tokenised_glosslist("Wb. Hand Three"))
# # # Lists all tokens common to the three scribe lists (too few, not useful)
# # for token in pmunitoks:
# #     if token in h3unitoks:
# #         if token in h2unitoks:
# #             commontoks.append(token)
# # # Lists all tokens common to the three scribe lists
# for token in h2unitoks:
#     if token in pmunitoks or token in h3unitoks:
#         if token not in commontoks:
#             commontoks.append(token)
# for token in pmunitoks:
#     if token in h3unitoks:
#         if token not in commontoks:
#             commontoks.append(token)
# # Reverses the order of the tokens in the common tokens list
# comtokscounted = []
# allthetoks = combinelists(compile_tokenised_glosslist("Wb. All Glosses"))
# for i in commontoks:
#     tokcount = allthetoks.count(i)
#     tokcountlist = [tokcount, i]
#     comtokscounted.append(tokcountlist)
# comtokscounted.sort(key=takefirst, reverse=True)
# # for i in comtokscounted:
# #     print(i[1] + ": " + str(i[0]))


# # Test basic_bayes
# allwords = ["abacadaeaf", "abbbcbdbeb", "aabbccddee"]
# pl = (("".join(allwords)).count("a")) / (len("".join(allwords)))  # overall probability of a given letter
# pw = 1/(len(allwords))  # probability of a randomly chosen letter being from any of the three words
# plgw = (allwords[0].count("a")) / (len(allwords[0]))  # probability of a given letter given word 1
# print(basic_bayes(plgw, pw, pl))


# # Test bayes_setup
# for token in comtokscounted:
#     print(token[1] + ": " + str(token[0]))
#     print("H1 – " + str(bayes_tok(token[1], 1)))
#     print("H2 – " + str(bayes_tok(token[1], 2)))
#     print("H3 – " + str(bayes_tok(token[1], 3)) + "\n")
