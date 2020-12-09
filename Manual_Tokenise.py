
from CombineInfoLists import combine_infolists
from MakeJSON import make_json
from SaveJSON import save_json
import os
import json
from ClearTags import clear_tags
from tkinter import *


pos_tags = ["ADJ", "ADP", "ADV", "AUX", "CCONJ", "DET", "INTJ", "NOUN", "NUM",
            "PART", "PRON", "PROPN", "PUNCT", "SCONJ", "SYM", "VERB", "X",
            "<Latin>", "<unknown>"]


def show_epistles(json_file):
    """return all the epistle names in a JSON document"""
    epistle_list = [i['epistle'] for i in json_file]
    return epistle_list


def select_epistle(ep_name):
    """for a selected epistle, return all the folios with gloss content for that epistle"""
    epistle_list = show_epistles(wb_data)
    folios_data = None
    if ep_name in epistle_list:
        for epistle in wb_data:
            ep = epistle['epistle']
            if ep == ep_name:
                folios_data = epistle['folios']
    return folios_data


def show_folcols(folios_data):
    """return all folios numbers and column letters containing glosses"""
    folio_names = [i["folio"] for i in folios_data]
    return folio_names


def select_folcol(folios_data, folio_name):
    """for a given epistle name and folio-column combination,
       return all data for glosses contained in that column of that folio"""
    folios_names = show_folcols(folios_data)
    glosses = None
    if folio_name in folios_names:
        for folio_column in folios_data:
            fol_col = folio_column["folio"]
            if fol_col == folio_name:
                glosses = folio_column["glosses"]
    return glosses


def show_glossnums(glosses):
    """return all gloss numbers"""
    gloss_nums = [i["glossNo"] for i in glosses]
    return gloss_nums


def select_glossnum(glosses, glossnum):
    """for a given folio-column combination and gloss number
       return all data related to that gloss which can be edited in the GUI"""
    glossnum = str(glossnum)
    gloss_nums = show_glossnums(glosses)
    gloss_data = None
    if glossnum in gloss_nums:
        for gloss in glosses:
            gl_num = gloss["glossNo"]
            if gl_num == glossnum:
                hand = gloss['glossHand']
                gloss_text = gloss['glossFullTags']
                trans = gloss['glossTrans']
                toks1 = gloss['glossTokens1']
                toks2 = gloss['glossTokens1']
                gloss_data = [hand, gloss_text, trans, toks1, toks2]
    return gloss_data


def update_toklists():
    pass


def save_tokens():
    pass


def next_gloss():
    save_tokens()
    pass


def last_gloss():
    save_tokens()
    pass


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

    # Open the JSON file for use in the GUI
    with open("Wb. Manual Tokenisation.json", 'r', encoding="utf-8") as wb_json:
        wb_data = json.load(wb_json)

    # If the tokenised fields are empty (the JSON file has just been generated) lists of tokens and POS to them
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
                token_list = [[i, "<unknown>"] for i in clear_tags(gloss).split(" ")]
                if not tok_1 and not tok_2:
                    tok_1 = token_list
                    tok_2 = token_list
                    gloss_data["glossTokens1"] = tok_1
                    gloss_data['glossTokens2'] = tok_2
                elif not tok_1:
                    tok_1 = token_list
                    gloss_data["glossTokens1"] = tok_1
                elif not tok_2:
                    tok_2 = token_list
                    gloss_data['glossTokens2'] = tok_2

    # Save the updated JSON file
    with open("Wb. Manual Tokenisation.json", 'w', encoding="utf-8") as wb_json:
        json.dump(wb_data, wb_json, indent=4, ensure_ascii=False)

    # Create the GUI
    root = Tk()
    root.title("Manual Tokenisation Window")
    root.geometry("1200x500")

    # Create GUI text displays (to show the gloss hand, the original gloss text, and the gloss translation)

    # Create GUI text-boxes (to edit the tokenisation fields by inserting or removing spaces)
    tokenise_text_1 = Text(root, width=80, height=3, font=("Courier", 16))
    tokenise_text_2 = Text(root, width=80, height=3, font=("Courier", 16))
    tokenise_text_1.pack(pady=20)
    tokenise_text_2.pack(pady=20)

    # Create GUI buttons
    save_button = Button(root, text="Save", command=save_tokens)
    save_button.pack(pady=20)
    next_button = Button(root, text="Next", command=next_gloss)
    next_button.pack(pady=21)
    back_button = Button(root, text="Back", command=last_gloss)
    back_button.pack(pady=22)

    # Run the GUI
    root.mainloop()
