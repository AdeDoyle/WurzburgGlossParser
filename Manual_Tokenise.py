
from CombineInfoLists import combine_infolists
from MakeJSON import make_json
from SaveJSON import save_json
import os
import json
from ClearTags import clear_tags
from tkinter import *
from tkinter import font


pos_tags = ["ADJ", "ADP", "ADV", "AUX", "CCONJ", "DET", "INTJ", "NOUN", "NUM",
            "PART", "PRON", "PROPN", "PUNCT", "SCONJ", "SYM", "VERB", "X",
            "<Latin>", "<unknown>"]


def italicise(ital_text):
    italics_font = font.Font(ital_text, ital_text.cget("font"))
    italics_font.configure(slant="italic")
    ital_text.tag_configure("italic", font=italics_font)
    current_tags = ital_text.tag_names("sel.first")


def update_json(file_name, file_object):
    """Save JSON file, overwrite old file by the same name if necessary"""
    with open(file_name, 'w', encoding="utf-8") as json_file:
        json.dump(file_object, json_file, indent=4, ensure_ascii=False)


def update_empty_toks(file_name, json_doc):
    """Go through all glosses looking for tokenisation fields that are empty
       replace any empty fields with tokens from the gloss and their POS tags
       update the .json file containing the data"""
    for epistle in json_doc:
        folios = epistle['folios']
        for folio_data in folios:
            glosses = folio_data['glosses']
            for gloss_data in glosses:
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
    update_json(file_name, json_doc)
    return f'{json_doc} updated: Tokenisation fields generated for empty strings.'


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
                gloss_text = gloss['glossText']
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

    # Check if any of the tokenisation fields are empty
    empty_tokfields = False
    for epistle in wb_data:
        folios = epistle['folios']
        for folio_data in folios:
            glosses = folio_data['glosses']
            for gloss_data in glosses:
                tok_1 = gloss_data['glossTokens1']
                tok_2 = gloss_data['glossTokens2']
                if not tok_1 or not tok_2:
                    empty_tokfields = True
                    break
            if empty_tokfields:
                break
        if empty_tokfields:
            break
    # If any of the tokenisation fields, for any gloss, are empty (eg. if the JSON file has just been generated)
    # add lists of tokens and their POS tags, for each gloss, to the gloss's tokenisation fields
    if empty_tokfields:
        update_empty_toks("Wb. Manual Tokenisation.json", wb_data)

    # Select the first gloss, from the first folio, from the first epistle as the starting gloss
    epistles = show_epistles(wb_data)
    open_ep = epistles[0]
    open_folio = show_folcols(select_epistle(open_ep))[0]
    open_glossnum = show_glossnums(select_folcol(select_epistle(open_ep), open_folio))[0]
    open_glossdata = select_glossnum(select_folcol(select_epistle(open_ep), open_folio), open_glossnum)
    open_hand = open_glossdata[0]
    open_gloss = open_glossdata[1]
    open_trans = open_glossdata[2]
    open_toks1 = open_glossdata[3]
    open_toks2 = open_glossdata[4]
    open_glossid = open_folio + open_glossnum

    cur_glossid = open_glossid
    cur_hand = open_hand
    cur_gloss = open_gloss
    cur_trans = open_trans
    cur_toks1 = open_toks1
    cur_toks2 = open_toks2

    # Create the GUI
    root = Tk()
    root.title("Manual Tokenisation Window")
    root.geometry("1200x500")

    # Create GUI text labels (to show the gloss hand, the original gloss text, and the gloss translation)
    gloss_label = Label(root, width=80, height=2, text=f"Gloss ({cur_glossid[3:]}) – {cur_hand}:", font=("Helvetica", 16))
    gloss_text = Label(root, width=80, height=3, text=open_gloss, font=("Courier", 16))
    trans_label = Label(root, width=80, height=1, text="Translation:", font=("Helvetica", 16))
    trans_text = Label(root, width=80, height=3, text=open_trans, font=("Courier", 16))
    gloss_label.grid(row=1, column=1)
    gloss_text.grid(row=2, column=1)
    trans_label.grid(row=3, column=1)
    trans_text.grid(row=4, column=1)

    # Create GUI text-boxes (to edit the tokenisation fields by inserting or removing spaces)
    tokenise_text_1 = Text(root, width=80, height=3, borderwidth=1, relief="solid", font=("Courier", 16))
    tokenise_text_2 = Text(root, width=80, height=3, borderwidth=1, relief="solid", font=("Courier", 16))
    tokenise_text_1.grid(row=5, column=1)
    tokenise_text_2.grid(row=6, column=1)

    # Create GUI buttons
    back_button = Button(root, text="Back", command=last_gloss)
    back_button.grid(row=7, column=0, pady=20)
    save_button = Button(root, text="Save", command=save_tokens)
    save_button.grid(row=7, column=1, pady=20)
    next_button = Button(root, text="Next", command=next_gloss)
    next_button.grid(row=7, column=2, pady=20)

    # Run the GUI
    root.mainloop()
