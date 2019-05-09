import pickle
from functools import lru_cache
from Tokenise import tokenise as tz
from nltk import edit_distance as ed


mod1 = "n3_1HLTokeniser.h5"
mod2 = "n3_2HLTokeniser.h5"
mod3 = "n10_2HLTokeniser.h5"
mod4 = "n3pad_2HLTokeniser.h5"
mod4_200 = "n3pad_2HLTokeniserV2.h5"
mod5 = "n5_1HLTokeniser.h5"
mod6 = "n5_2HLTokeniser.h5"

TBFmod1 = "n3_TBF1HLTokeniser.h5"
TBFmod2 = "n3_TBF2HLTokeniser.h5"
TBFmod3 = "n3_TBF4HLTokeniser.h5"
TBFmod4 = "n5_TBF1HLTokeniser.h5"
TBFmod5 = "n5_TBF2HLTokeniser.h5"
TBFmod6 = "n5_TBF4HLTokeniser.h5"
TBFmod7 = "n5_TBF3HLTokeniser.h5"
TBFmod8 = "n5_TBF2HLTokeniserV2.h5"


ogmods = [mod1, mod2, mod3, mod4, mod5, mod6]
tbfmods = [TBFmod1, TBFmod2, TBFmod3, TBFmod4, TBFmod5, TBFmod6, TBFmod7, TBFmod8]
allmods = ogmods + tbfmods


# print(get_text("Manually Tokenised Glosses"))
test_in = open("toktest.pkl", "rb")
test_set = pickle.load(test_in)
x_test, y_test = test_set[0], test_set[1]


def test_tzmod(mod):
    edit_dists = []
    count = 0
    remove = ["(", ")", "*", "-", "^"]
    for x_pos in range(len(x_test)):
        count += 1
        x = x_test[x_pos]
        y = y_test[x_pos]
        for rem in remove:
            if rem in y:
                y = "".join(y.split(rem))
        if "Latin" in y:
            y = "*Latin*".join(y.split("Latin"))
        e_dist = ed(y, tz(mod, x))
        edit_dists.append(e_dist)
        # print("Gloss {}/41: Edit Distance = {}".format(str(count), str(e_dist)))
    avg_edist = sum(edit_dists) / len(edit_dists)
    return avg_edist


modscores = []
for mod in allmods:
    print(mod)
    score = test_tzmod(mod)
    print(score)
    modscores.append(score)

best_score = min(modscores)
print("Best Model: {}".format(allmods[modscores.index(best_score)]))

