from PrepareHandContent import compile_tokenised_glosslist, combinelists, get_inditokcount, get_unitoks


def basic_bayes(p2g1, p1, p2):
    """Calculates the probability 1 (a scribe) given the probability of 2 (a word/bigram/contraction etc.)"""
    topline = p2g1 * p1
    bottomline = p2
    return topline / bottomline


def bayes_tok(tok, allglosses, scribe_glosses):
    """Takes a word, a list of texts and the number of a given text within that list.
       Uses bayes theorum to estimate the probability of the of a given text given the word's occurrence."""
    # probability of a given token
    # (number of times token is used by all scribes / total number of tokens used by all scribes)
    pw = get_inditokcount(tok, allglosses) / len(combinelists(allglosses))
    # probability of a given scribe
    # (1 / number of scribes)
    ps = 1/3
    # probability of a given token given a scribe
    # (number of times token used by scribe / total number of tokens by scribe)
    pwgs = get_inditokcount(tok, scribe_glosses) / len(combinelists(scribe_glosses))
    return basic_bayes(pwgs, ps, pw)


glosshands = ["Wb. All Glosses", "Wb. Prima Manus", "Wb. Hand Two", "Wb. Hand Three"]

# # Lists of tokenised glosses
allglosstoks = compile_tokenised_glosslist(glosshands[0])
pmtoks = compile_tokenised_glosslist(glosshands[1])
h2toks = compile_tokenised_glosslist(glosshands[2])
h3toks = compile_tokenised_glosslist(glosshands[3])


# # Lists of unique tokens for each list of tokenised glosses
# allglossunitoks = get_unitoks(allglosstoks)
pmunitoks = get_unitoks(pmtoks)
h2unitoks = get_unitoks(h2toks)
h3unitoks = get_unitoks(h3toks)


commontoks = []
# # Lists all tokens common to the three scribe lists
# for token in pmunitoks:
#     if token in h3unitoks:
#         if token in h2unitoks:
#             commontoks.append(token)
# # Lists all tokens common to the three scribe lists
for token in h2unitoks:
    if token in pmunitoks or token in h3unitoks:
        commontoks.append(token)
for token in pmunitoks:
    if token in h3unitoks:
        commontoks.append(token)


# # Test basic_bayes
# allwords = ["abacadaeaf", "abbbcbdbeb", "aabbccddee"]
# pl = (("".join(allwords)).count("a")) / (len("".join(allwords)))  # overall probability of a given letter
# pw = 1/(len(allwords))  # probability of a randomly chosen letter being from any of the three words
# plgw = (allwords[0].count("a")) / (len(allwords[0]))  # probability of a given letter given word 1
# print(basic_bayes(plgw, pw, pl))


# Test bayes_tok
for token in commontoks:
    print(token + ": " + str(bayes_tok(token, allglosstoks, h3toks)))
