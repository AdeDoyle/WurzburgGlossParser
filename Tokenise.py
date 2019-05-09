"""Level 1, 2, 2, 1, 2"""

from functools import lru_cache
from keras.models import load_model
import pickle
import re
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from RemoveNewlines import remove_newlines, get_pages, get_section, clear_tags, order_glosses, remove_brackets,\
    remove_glossnums
from RemoveLatin import rem_lat
from RemovePunctuation import rempunc_tok
from OpenDocx import get_text
from SaveXlsx import save_xlsx


@lru_cache(maxsize=500)
def tokenise(model, intext):
    """Takes a trained language model and a text, returns the text tokenised as per the language model"""
    mod = load_model(model)
    buffer = 0
    buffpat = re.compile(r'n\d{1,2}(pad)?_')
    buffpatitir = buffpat.finditer(model)
    for buff in buffpatitir:
        if "pad" in buff.group():
            padbuff = buff.group()
            buff = "".join(padbuff.split("pad"))
            buffer = int(buff[1:-1])
        else:
            buffer = int(buff.group()[1:-1])
    buffer_text = buffer * "$"
    text = buffer_text + intext
    mapping = pickle.load(open('char_mapping.pkl', 'rb'))
    reverse = {i: c for c, i in mapping.items()}
    letters = [i for i in intext]
    outlist = []
    for i in range(len(text) - buffer):
        let = text[buffer]
        text_chunk = text[:buffer]
        outlist_text = "".join(outlist)
        # if there are enough letters in the outlist to make predictions from
        # take the chunk of letters to predict from from the outlist
        if buffer <= len(outlist):
            text_chunk = outlist_text[-buffer:]
        # if there aren't enough letters in the outlist to make predictions from yet
        # combine what's in the outlist with what's in the text
        else:
            text_chunk = text_chunk[:buffer - (len(outlist))] + outlist_text
        # if the letter were trying to predict isn't a space in the text
        # predict a character
        if let != " ":
            encoded = [mapping[char] for char in text_chunk]
            encoded = pad_sequences([encoded], maxlen=buffer, truncating='pre')
            encoded = to_categorical(encoded, num_classes=len(mapping))
            pred = mod.predict_classes(encoded, verbose=0)[0]
            # if the prediction is not a space
            # just add the letter we were trying to predict to the outlist
            if pred != 1:
                outlist.append(let)
            # if the prediction is a space
            # add a space to the outlist followed by the letter that was in the text
            else:
                outlist.append(" " + let)
        # if the letter we're trying to predict is a space in the text
        # just append a space to the outlist
        else:
            outlist.append(" ")
        text = text[1:]
    outtext = "".join(outlist)
    # outtext = " ".join(outtext.split("  "))
    return outtext


def space_tokenise(string, puncfilter=False, puncexcept=[]):
    """Takes a string, a true/false value for filtering punctuation and a list of punctuation-filter exceptions.
       Replaces newlines with spaces, tokenises string based on word spacing.
       If filter punctuation is true, each token has """
    strunaltered = string
    stroneline = remove_newlines(strunaltered)
    strtoklist = stroneline.split(" ")
    if puncfilter:
        newtoklist = []
        for tok in strtoklist:
            tok = rempunc_tok(tok, puncexcept)
            newtoklist.append(tok)
        return newtoklist
    else:
        return strtoklist


def remove_duptoks(toklist):
    """Creates a list of unique tokens which occur in the full list of tokens"""
    uniquetoks = []
    for tok in toklist:
        if tok not in uniquetoks:
            uniquetoks.append(tok)
    return uniquetoks


# Defines a function which gets the first element in a list.
def takefirst(elem):
    return elem[0]


def top_toks(string, occurrences=0):
    """Takes a string, and optional minimum number of occurrences, tokenises the string, removes blank tokens or tokens
       with punctuation only, returns list of sublists of tokens and use-count for that token in the string"""
    strtoks = space_tokenise(string, True)
    unitoks = remove_duptoks(strtoks)
    tokinfolist = []
    # Creates a list of a token's count, and the token itself, and adds this list to tokinfolist.
    for tok in unitoks:
        if tok != "":
            tokcount = strtoks.count(tok)
            tokinfo = [tokcount, tok]
            tokinfolist.append(tokinfo)
    # Sorts tokinfolist into descending order.
    tokinfolist.sort(key=takefirst, reverse=True)
    toknum = 0
    orderedtoklist = []
    # Counts, then lists, in descending order, tokens with more than a set number of occurrences in the string.
    for i in tokinfolist:
        if i[0] >= occurrences:
            toknum += 1
            orderedtoklist.append([toknum, i[0], i[1]])
    return orderedtoklist


# mod1 = "n3_1HLTokeniser.h5"
# mod2 = "n3_2HLTokeniser.h5"
# mod3 = "n10_2HLTokeniser.h5"
# mod4 = "n3pad_2HLTokeniser.h5"
# mod4_200 = "n3pad_2HLTokeniserV2.h5"
# mod5 = "n5_1HLTokeniser.h5"
# mod6 = "n5_2HLTokeniser.h5"
#
# TBFmod1 = "n3_TBF1HLTokeniser.h5"
# TBFmod2 = "n3_TBF2HLTokeniser.h5"
# TBFmod3 = "n3_TBF4HLTokeniser.h5"
# TBFmod4 = "n5_TBF1HLTokeniser.h5"
# TBFmod5 = "n5_TBF2HLTokeniser.h5"
# TBFmod6 = "n5_TBF4HLTokeniser.h5"
# TBFmod7 = "n5_TBF3HLTokeniser.h5"
# TBFmod8 = "n5_TBF2HLTokeniserV2.h5"
# TBFmod9 = "n5_TBF3HLTokeniserV2.h5"
# TBFmod10 = "n5_TBF1HLTokeniserV2.h5"
# TBFmod11 = "n7_TBF1HLTokeniser.h5"
# TBFmod12 = "n3_TBF1HLTokeniserV2.h5"


# print(tokenise(mod1, ".i. biuusa ocirbáig darfarcennsi frimaccidóndu"))
# print(tokenise(mod2, ".i. biuusa ocirbáig darfarcennsi frimaccidóndu"))
# print(tokenise(mod3, ".i. biuusa ocirbáig darfarcennsi frimaccidóndu"))
# print(tokenise(mod4, ".i. biuusa ocirbáig darfarcennsi frimaccidóndu"))
# print(tokenise(mod4_200, ".i. biuusa ocirbáig darfarcennsi frimaccidóndu"))
# print(tokenise(mod5, ".i. biuusa ocirbáig darfarcennsi frimaccidóndu"))
# print(tokenise(mod6, ".i. biuusa ocirbáig darfarcennsi frimaccidóndu"))
# print()
# print(tokenise(TBFmod1, ".i. biuusa ocirbáig darfarcennsi frimaccidóndu"))
# print(tokenise(TBFmod2, ".i. biuusa ocirbáig darfarcennsi frimaccidóndu"))
# print(tokenise(TBFmod3, ".i. biuusa ocirbáig darfarcennsi frimaccidóndu"))
# print(tokenise(TBFmod4, ".i. biuusa ocirbáig darfarcennsi frimaccidóndu"))
# print(tokenise(TBFmod5, ".i. biuusa ocirbáig darfarcennsi frimaccidóndu"))
# print(tokenise(TBFmod6, ".i. biuusa ocirbáig darfarcennsi frimaccidóndu"))
# print(tokenise(TBFmod7, ".i. biuusa ocirbáig darfarcennsi frimaccidóndu"))
# print(tokenise(TBFmod8, ".i. biuusa ocirbáig darfarcennsi frimaccidóndu"))
# print(tokenise(TBFmod9, ".i. biuusa ocirbáig darfarcennsi frimaccidóndu"))
# print(tokenise(TBFmod10, ".i. biuusa ocirbáig darfarcennsi frimaccidóndu"))
# print(tokenise(TBFmod11, ".i. biuusa ocirbáig darfarcennsi frimaccidóndu"))
# print(tokenise(TBFmod12, ".i. biuusa ocirbáig darfarcennsi frimaccidóndu"))
# print()


# testlists = pickle.load(open('toktest.pkl', 'rb'))
# x_test = testlists[0]
# y_test = testlists[1]
# for text_no in range(len(x_test)):
#     print(x_test[text_no])
#     print(tokenise(mod1, x_test[text_no]))
#     print(y_test[text_no] + "\n")


# glosses = remove_glossnums(remove_brackets(
#     order_glosses(clear_tags("\n".join(get_section(get_pages("Wurzburg Glosses", 499, 712), "SG"))))))
# glosses = remove_glossnums(remove_brackets(rem_lat(order_glosses(clear_tags(
#     "\n".join(get_section(get_pages("Wurzburg Glosses", 499, 712), "SG")), ["GLat", "ie", "vel"])), True)))
# glosses = remove_glossnums(remove_brackets(rem_lat(clear_tags(
#     get_text("Wb. Prima Manus"), ["GLat", "ie", "vel"]), True)))
# glosses = remove_glossnums(remove_brackets(rem_lat(clear_tags(
#     get_text("Wb. Hand Two"), ["GLat", "ie", "vel"]), True)))
# glosses = remove_glossnums(remove_brackets(rem_lat(clear_tags(
#     get_text("Wb. Hand Three"), ["GLat", "ie", "vel"]), True)))


# # Prints the most common tokens.
# for token in top_toks(glosses, 53):
#     print(str(token[0]) + ". " + token[2] + " - Count: " + str(token[1]))

# # Saves an excel document of the most common tokens.
# save_xlsx("Wb. Common Tokens", top_toks(glosses, 53))
