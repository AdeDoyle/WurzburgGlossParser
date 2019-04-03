from PrepareHandContent import compile_tokenised_glosslist
from CalculateBayes import bayes_tok


def auth_check_glosshand(gloss):
    """Assesses statistical liklihood that a gloss belongs to a particular hand
       Measures: Bayesian Token analysis"""
    # Creates a list of sublists, each sublist representing a hand.
    # Each sublist contains the probability of each token in the gloss occurring in each hand.
    tok_problist = [[], [], []]
    for token in gloss:
        if token != "*Latin*":
            for hand in range(3):
                handlist = tok_problist[hand]
                handlist.append(bayes_tok(token, hand + 1))
    for i in range(len(tok_problist)):
        hand_problist = tok_problist[i]
        multiplier = 1
        for prob in hand_problist:
            multiplier = multiplier * prob
        tok_problist[i] = multiplier
    most_probable_hand = 0
    highest_prob = 0
    for i in range(len(tok_problist)):
        if i == 0:
            highest_prob = tok_problist[i]
            most_probable_hand = i + 1
        elif tok_problist[i] > highest_prob:
            highest_prob = tok_problist[i]
            most_probable_hand = i + 1
    return most_probable_hand


def check_correct(gloss, hand):
    """Checks if a given gloss is in a given list"""
    glosshands = ["Wb. All Glosses", "Wb. Prima Manus", "Wb. Hand Two", "Wb. Hand Three"]
    if gloss in compile_tokenised_glosslist(glosshands[hand]):
        return "Correct"
    else:
        return "False"


def return_correction_list():
    """Calculates every gloss's most probable hand,
       checks to see if the gloss is actually from that hand,
       calculates how many glosses were assigned to the correct hand as a percentage"""
    allglosstoks = compile_tokenised_glosslist("Wb. All Glosses")
    all_corrections = []
    for gloss in allglosstoks:
        authguess = auth_check_glosshand(gloss)
        glosschecklist = [gloss, authguess, check_correct(gloss, authguess)]
        all_corrections.append(glosschecklist)
    correctcount = 0
    for i in all_corrections:
        print(i)
        if i[2] == "Correct":
            correctcount += 1
    percent_correct = (100 / len(all_corrections) * correctcount)
    return str(percent_correct) + "% correct"


# print(auth_check_glosshand(['.i.', 'díith', '.i.', '*Latin*', 'dernum']))


# allglosstoks = compile_tokenised_glosslist("Wb. All Glosses")


# for gloss in allglosstoks[:10]:
#     authguess = auth_check_glosshand(gloss)
#     print(str(authguess) + " - " + check_correct(gloss, authguess))

print(return_correction_list())
