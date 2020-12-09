
from CombineInfoLists import combine_infolists
from MakeJSON import make_json
from SaveJSON import save_json
import os
import json

pos_tags = ["ADJ", "ADP", "ADV", "AUX", "CCONJ", "DET", "INTJ", "NOUN", "NUM",
            "PART", "PRON", "PROPN", "PUNCT", "SCONJ", "SYM", "VERB", "X",
            "<Latin>", "<unknown>"]

if __name__ == "__main__":

    # Navigate to a directory containing a JSON file of the Wb. Glosses
    # If either the directory or the JSON file do not exist, create them

    maindir = os.getcwd()
    tokenise_dir = os.path.join(maindir, "Manual_Tokenise_Files")

    # Open the Manual Tokenisation folder
    try:
        os.chdir(tokenise_dir)
    except FileNotFoundError:
        os.mkdir("Manual_Tokenise_Files")
        os.chdir(tokenise_dir)

    # Create a JSON document in the Manual Tokenisation folder if it doesn't exist already
    dir_contents = os.listdir()
    if "Wb. Manual Tokenisation.json" not in dir_contents:
        os.chdir(maindir)
        wbglosslist = combine_infolists("Wurzburg Glosses", 499, 712)
        os.chdir(tokenise_dir)
        save_json(make_json(wbglosslist, True), "Wb. Manual Tokenisation")

    # Open the JSON file for use in the interface

    # Opening JSON file
    with open("Wb. Manual Tokenisation.json", 'r', encoding="utf-8") as wb_json:
        wb_data = json.load(wb_json)

    for epistle in wb_data:
        ep_name = epistle['epistle']
        folios = epistle['folios']
        for folio_data in folios:
            folio = folio_data['folio']
            glosses = folio_data['glosses']
            for gloss_data in glosses:
                number = gloss_data['glossNo']
                hand = gloss_data['glossHand']
                gloss = gloss_data['glossFullTags']
                tok_1 = gloss_data['glossTokens1']
                tok_2 = gloss_data['glossTokens2']
                token_list = [[i, "<Unknown>"] for i in gloss.split(" ")]
                if not tok_1 and not tok_2:
                    gloss_data["glossTokens1"] = token_list
                    gloss_data['glossTokens2'] = token_list
                    tok_1 = gloss_data['glossTokens1']
                    tok_2 = gloss_data['glossTokens2']
                print(tok_2)

    # Open the Interface
