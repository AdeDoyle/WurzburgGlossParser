
from CombineInfoLists import combine_infolists
from MakeJSON import make_json, make_lex_json
from SaveJSON import save_json
from CoNLLU_to_JSON import c_to_j
from conllu import parse
import os
import json
import re
from decimal import Decimal
from ClearTags import clear_tags
from tkinter import *
from tkinter import ttk
from tkinter import font
from nltk import edit_distance
import unidecode
import platform


plt = platform.system()


class UI:

    def __init__(self, file_name, wb_data, lexicon, primary_lexicon):
        """Initialise the UI class
           Define several parameters within the UI"""

        self.file_name = file_name
        self.wb_data = wb_data
        self.epistles = show_epistles(wb_data)
        self.lexicon = lexicon
        self.primary_lexicon = primary_lexicon

        # Define possible POS-tags
        self.pos_tags = ["ADJ", "ADP", "ADV", "AUX", "CCONJ", "DET", "INTJ", "NOUN", "NUM",
                         "PART", "PRON", "PROPN", "PUNCT", "SCONJ", "SYM", "VERB", "X",
                         "<Latin>", "<Latin CCONJ>", "<Greek>", "<unknown>"]

        # Define possible morphological features
        self.adp_feats = {"AdpType": ["N/A", "Prep"],
                          "Definite": ["N/A", "Def", "Ind"],
                          "Gender": ["N/A", "Masc", "Masc,Neut", "Neut", "Fem"],
                          "Number": ["N/A", "Dual", "Sing", "Plur"],
                          "Person": ["N/A", "1",  "2", "3"],
                          "PronType": ["N/A", "Art", "Prs", "Prs,Rel", "Rel"]}
        self.pron_feats = {"Case": ["N/A", "Nom", "Acc", "Gen", "Dat"],
                           "Gender": ["N/A", "Masc", "Masc,Neut", "Neut", "Fem"],
                           "Mood": ["N/A", "Ind", "Sub"],
                           "Number": ["N/A", "Sing", "Plur"],
                           "Person": ["N/A", "1",  "2", "3"],
                           "Polarity": ["N/A", "Neg", "Pos"],
                           "Poss": ["N/A", "Yes"],
                           "PronClass": ["N/A", "A", "B", "C"],
                           "PronType": ["N/A", "Ana", "Emp", "Ind", "Int", "Prs"],
                           "Reflex": ["N/A", "Yes"]}
        self.max_linelen = 110

        self.open_ep = self.epistles[0]
        self.open_fols = show_folcols(select_epistle(self.open_ep))
        self.open_folio = self.open_fols[0]
        self.open_glossnums = show_glossnums(select_folcol(select_epistle(self.open_ep), self.open_folio))
        self.open_glossnum = self.open_glossnums[0]
        self.open_glossid = self.open_folio + self.open_glossnum
        self.open_glossdata = select_glossnum(select_folcol(select_epistle(self.open_ep), self.open_folio),
                                              self.open_glossnum)
        self.open_hand = self.open_glossdata[0]
        self.open_gloss = self.open_glossdata[1]
        self.open_trans = self.open_glossdata[2]
        self.open_toks = self.open_glossdata[3]
        spaceless_toks = [
            t if " " not in t[0] else [
                "_".join(t[0].split(" ")), t[1], t[2], t[3]
            ] for t in self.open_toks
        ]

        self.lex_toks = list()

        # Create the GUI
        self.root = Tk()
        self.root.title("Manual Tokenisation Window")
        self.root.geometry("1600x900")

        self.render_gloss(
            self.root,
            epistles=self.epistles,
            cur_ep=self.open_ep,
            cur_fols=self.open_fols,
            cur_folio=self.open_folio,
            cur_glossnums=self.open_glossnums,
            cur_glossnum=self.open_glossnum,
            cur_glossid=self.open_glossid,
            cur_hand=self.open_hand,
            cur_gloss=self.open_gloss,
            cur_trans=self.open_trans,
            cur_toks=spaceless_toks
        )

    def start(self):
        """Starts the program running, and runs functions when the program is ended"""
        # Runs the main loop of the program
        self.root.mainloop()
        # Runs functions when the program is closed
        self.clear_lexica()

        # Set arguments for CoNLL-U to JSON function
        conllu_dir = os.path.join(os.getcwd(), "conllu_files")
        wb_dir = os.path.join(conllu_dir, "Wb_Treebanks")
        wb_conllu = os.path.join(wb_dir, "combined_wb_files.conllu")
        with open(wb_conllu, "r", encoding="utf-8") as conllu_file_import:
            conllu_content = parse(conllu_file_import.read())

        json_dir = os.path.join(os.getcwd(), "Manual_Tokenise_Files")
        wb_json = os.path.join(json_dir, "Wb. Manual Tokenisation.json")
        with open(wb_json, "r", encoding="utf-8") as json_file_import:
            json_content = json.load(json_file_import)

        close_save_folder = os.path.join(os.getcwd(), "Manual_Tokenise_Files")

        # Combine any updates from manually annotated Wb. glosses CoNLL-U files before closing program
        c_to_j(
            conllu_content, json_content, output_filename="Wb. Manual Tokenisation.json", save_folder=close_save_folder
        )

    def create_gloss_info(self, selected_epistle, selected_folio, selected_glossnum):
        selected_glossdata = select_glossnum(
            select_folcol(
                select_epistle(selected_epistle), selected_folio),
            selected_glossnum
        )
        return {
            "selected_epistle": selected_epistle,
            "selected_fols": show_folcols(select_epistle(selected_epistle)),
            "selected_folio": selected_folio,
            "selected_glossnums": show_glossnums(select_folcol(select_epistle(selected_epistle), selected_folio)),
            "selected_glossnum": selected_glossnum,
            "selected_glossid": selected_folio + selected_glossnum,
            "selected_hand": selected_glossdata[0],
            "selected_gloss": selected_glossdata[1],
            "selected_trans": selected_glossdata[2],
            "selected_toks": selected_glossdata[3]
        }

    def change_gloss(self, event=None):
        self.remove_head_options()

        new_selected_glossnum = self.current_rendered_window["current_selected_gloss"].get()
        self.selected_gloss_info = self.create_gloss_info(
            selected_epistle=self.current_rendered_window["current_selected_epistle"].get(),
            selected_folio=self.current_rendered_window["current_selected_folio"].get(),
            selected_glossnum=new_selected_glossnum
        )

        spaceless_toks = [
            t if " " not in t[0] else [
                "_".join(t[0].split(" ")), t[1], t[2], t[3]
            ] for t in self.selected_gloss_info["selected_toks"]
        ]

        self.render_gloss(
            self.root,
            epistles=self.epistles,
            cur_ep=self.selected_gloss_info["selected_epistle"],
            cur_fols=self.selected_gloss_info["selected_fols"],
            cur_folio=self.selected_gloss_info["selected_folio"],
            cur_glossnums=self.selected_gloss_info["selected_glossnums"],
            cur_glossnum=self.selected_gloss_info["selected_glossnum"],
            cur_glossid=self.selected_gloss_info["selected_glossid"],
            cur_hand=self.selected_gloss_info["selected_hand"],
            cur_gloss=self.selected_gloss_info["selected_gloss"],
            cur_trans=self.selected_gloss_info["selected_trans"],
            cur_toks=spaceless_toks
        )

    def change_folio(self, event=None):
        self.remove_head_options()

        new_selected_folio = self.current_rendered_window["current_selected_folio"].get()
        cur_ep = self.current_rendered_window["current_selected_epistle"].get()
        cur_glossnums = show_glossnums(select_folcol(select_epistle(cur_ep), new_selected_folio))
        new_selected_glossnum = cur_glossnums[0]
        self.selected_gloss_info = self.create_gloss_info(
            selected_epistle=self.current_rendered_window["current_selected_epistle"].get(),
            selected_folio=new_selected_folio,
            selected_glossnum=new_selected_glossnum
        )

        spaceless_toks = [
            t if " " not in t[0] else [
                "_".join(t[0].split(" ")), t[1], t[2], t[3]
            ] for t in self.selected_gloss_info["selected_toks"]
        ]

        self.render_gloss(
            self.root,
            epistles=self.epistles,
            cur_ep=self.selected_gloss_info["selected_epistle"],
            cur_fols=self.selected_gloss_info["selected_fols"],
            cur_folio=self.selected_gloss_info["selected_folio"],
            cur_glossnums=self.selected_gloss_info["selected_glossnums"],
            cur_glossnum=self.selected_gloss_info["selected_glossnum"],
            cur_glossid=self.selected_gloss_info["selected_glossid"],
            cur_hand=self.selected_gloss_info["selected_hand"],
            cur_gloss=self.selected_gloss_info["selected_gloss"],
            cur_trans=self.selected_gloss_info["selected_trans"],
            cur_toks=spaceless_toks
        )

    def change_epistle(self, event=None):
        self.remove_head_options()

        new_selected_epistle = self.current_rendered_window["current_selected_epistle"].get()
        cur_fols = show_folcols(select_epistle(new_selected_epistle))
        new_selected_folio = cur_fols[0]
        cur_glossnums = show_glossnums(select_folcol(select_epistle(new_selected_epistle), new_selected_folio))
        new_selected_glossnum = cur_glossnums[0]
        self.selected_gloss_info = self.create_gloss_info(
            selected_epistle=new_selected_epistle,
            selected_folio=new_selected_folio,
            selected_glossnum=new_selected_glossnum
        )

        spaceless_toks = [
            t if " " not in t[0] else [
                "_".join(t[0].split(" ")), t[1], t[2], t[3]
            ] for t in self.selected_gloss_info["selected_toks"]
        ]

        self.render_gloss(
            self.root,
            epistles=self.epistles,
            cur_ep=self.selected_gloss_info["selected_epistle"],
            cur_fols=self.selected_gloss_info["selected_fols"],
            cur_folio=self.selected_gloss_info["selected_folio"],
            cur_glossnums=self.selected_gloss_info["selected_glossnums"],
            cur_glossnum=self.selected_gloss_info["selected_glossnum"],
            cur_glossid=self.selected_gloss_info["selected_glossid"],
            cur_hand=self.selected_gloss_info["selected_hand"],
            cur_gloss=self.selected_gloss_info["selected_gloss"],
            cur_trans=self.selected_gloss_info["selected_trans"],
            cur_toks=spaceless_toks
        )

    def mouse_wheel(self, event):
        if plt == "Windows":
            self.current_rendered_window["main_canvas"].yview_scroll(-1 * (event.delta // 120), "units")
        elif plt == "Darwin":
            self.current_rendered_window["main_canvas"].yview_scroll(-1 * event.delta, "units")

    def render_gloss(self, root, epistles, cur_ep, cur_fols, cur_folio, cur_glossnums, cur_glossnum, cur_glossid,
                     cur_hand, cur_gloss, cur_trans, cur_toks):

        # Create frames for all following widgets
        # Destroy currently rendered window
        if hasattr(self, "current_rendered_window"):

            self.current_rendered_window["main_frame"].destroy()
            self.current_rendered_window["main_canvas"].destroy()
            self.current_rendered_window["main_scrollbar"].destroy()
            self.current_rendered_window["horizontal_scrollbar"].destroy()
            self.current_rendered_window["secondary_frame"].destroy()

            self.current_rendered_window["nav_frame"].destroy()
            self.current_rendered_window["options_frame"].destroy()
            self.current_rendered_window["nav_buttons_frame"].destroy()
            self.current_rendered_window["text_frame"].destroy()
            self.current_rendered_window["toks_frames"].destroy()
            self.current_rendered_window["toks_frame"].destroy()
            for i in range(self.featureframe_count):
                self.current_rendered_window[f"feats_frame_{i}"].destroy()
            self.current_rendered_window["head_opts_frame"].destroy()
            self.current_rendered_window["buttons_frame"].destroy()

            self.current_rendered_window["ep_drop"].destroy()
            self.current_rendered_window["fol_drop"].destroy()
            self.current_rendered_window["gloss_drop"].destroy()

            self.current_rendered_window["back_button"].destroy()
            self.current_rendered_window["next_button"].destroy()
            self.current_rendered_window["update_button"].destroy()
            self.current_rendered_window["save_button"].destroy()

            self.current_rendered_window["gloss_label"].destroy()
            self.current_rendered_window["gloss_text"].destroy()
            self.current_rendered_window["trans_label"].destroy()
            self.current_rendered_window["trans_text"].destroy()

            self.current_rendered_window["tokenise_label"].destroy()
            self.current_rendered_window["tokenise_text"].destroy()

            self.current_rendered_window["toks_label"].destroy()
            self.current_rendered_window["pos_label"].destroy()

        # Define the type of data which will be in the drop-down menus
        self.current_rendered_window = {
            "current_selected_epistle": StringVar(),
            "current_selected_folio": StringVar(),
            "current_selected_gloss": StringVar()
        }

        self.current_rendered_window["current_selected_epistle"].set(cur_ep)
        self.current_rendered_window["current_selected_folio"].set(cur_folio)
        self.current_rendered_window["current_selected_gloss"].set(cur_glossnum)

        # Create a main frame with a canvas so that it's possible use a scroll bar
        self.current_rendered_window["main_frame"] = Frame(root)
        self.current_rendered_window["main_frame"].pack(fill=BOTH, expand=1)

        self.current_rendered_window["main_canvas"] = Canvas(self.current_rendered_window["main_frame"])

        self.current_rendered_window["main_scrollbar"] = ttk.Scrollbar(
            self.current_rendered_window["main_frame"],
            orient=VERTICAL, command=self.current_rendered_window["main_canvas"].yview
        )

        self.current_rendered_window["horizontal_scrollbar"] = ttk.Scrollbar(
            self.current_rendered_window["main_frame"],
            orient=HORIZONTAL, command=self.current_rendered_window["main_canvas"].xview
        )

        self.current_rendered_window["horizontal_scrollbar"].pack(side=BOTTOM, fill=X)
        self.current_rendered_window["main_canvas"].pack(side=LEFT, fill=BOTH, expand=1)
        self.current_rendered_window["main_scrollbar"].pack(side=RIGHT, fill=Y)

        self.current_rendered_window["main_canvas"].configure(
            yscrollcommand=self.current_rendered_window["main_scrollbar"].set,
            xscrollcommand=self.current_rendered_window["horizontal_scrollbar"].set
        )
        self.current_rendered_window["main_canvas"].bind(
            '<Configure>',
            lambda e: self.current_rendered_window["main_canvas"].configure(
                scrollregion=self.current_rendered_window["main_canvas"].bbox("all")
            )
        )

        self.current_rendered_window["secondary_frame"] = Frame(self.current_rendered_window["main_canvas"])
        self.current_rendered_window["main_canvas"].create_window(
            (0, 0),
            window=self.current_rendered_window["secondary_frame"],
            anchor="nw"
        )

        self.current_rendered_window["main_canvas"].bind("<MouseWheel>", self.mouse_wheel)
        self.current_rendered_window["secondary_frame"].bind("<MouseWheel>", self.mouse_wheel)

        # Create display frames for the window
        self.current_rendered_window["nav_frame"] = Frame(self.current_rendered_window["secondary_frame"],
                                                          padx=5, pady=5)
        self.current_rendered_window["nav_frame"].grid(row=0, column=0, padx=10, pady=10, sticky="W")
        self.current_rendered_window["nav_frame"].bind("<MouseWheel>", self.mouse_wheel)

        self.current_rendered_window["options_frame"] = Frame(self.current_rendered_window["nav_frame"],
                                                              padx=5, pady=5)
        self.current_rendered_window["options_frame"].grid(row=0, column=0, padx=5, pady=5, sticky="W")
        self.current_rendered_window["options_frame"].bind("<MouseWheel>", self.mouse_wheel)

        self.current_rendered_window["nav_buttons_frame"] = Frame(self.current_rendered_window["nav_frame"],
                                                                  padx=5, pady=5)
        self.current_rendered_window["nav_buttons_frame"].grid(row=0, column=1, padx=5, pady=5, sticky="W")
        self.current_rendered_window["nav_buttons_frame"].bind("<MouseWheel>", self.mouse_wheel)

        self.current_rendered_window["text_frame"] = Frame(self.current_rendered_window["secondary_frame"],
                                                           padx=5, pady=5)
        self.current_rendered_window["text_frame"].grid(row=1, column=0, padx=10, pady=10, sticky="W")
        self.current_rendered_window["text_frame"].bind("<MouseWheel>", self.mouse_wheel)

        self.current_rendered_window["toks_frames"] = Frame(self.current_rendered_window["secondary_frame"],
                                                            padx=5, pady=5)
        self.current_rendered_window["toks_frames"].grid(row=2, column=0, padx=10, pady=10, sticky="W")
        self.current_rendered_window["toks_frames"].bind("<MouseWheel>", self.mouse_wheel)

        self.current_rendered_window["toks_frame"] = LabelFrame(self.current_rendered_window["toks_frames"],
                                                                padx=5, pady=5)
        self.current_rendered_window["toks_frame"].grid(row=0, column=0, padx=5, pady=5, sticky="NW")
        self.current_rendered_window["toks_frame"].bind("<MouseWheel>", self.mouse_wheel)

        for i, _ in enumerate(cur_toks):
            self.current_rendered_window[f"feats_frame_{i}"] = Frame(self.current_rendered_window["toks_frame"])
            self.current_rendered_window[f"feats_frame_{i}"].grid(row=i + 1, column=4, padx=15, sticky='w')
            self.current_rendered_window[f"feats_frame_{i}"].bind("<MouseWheel>", self.mouse_wheel)

        self.current_rendered_window["head_opts_frame"] = LabelFrame(self.current_rendered_window["toks_frames"],
                                                                     padx=5, pady=5)
        self.current_rendered_window["head_opts_frame"].grid(row=0, column=1, padx=5, pady=5, sticky="NW")
        self.current_rendered_window["head_opts_frame"].bind("<MouseWheel>", self.mouse_wheel)

        self.current_rendered_window["buttons_frame"] = Frame(self.current_rendered_window["toks_frames"],
                                                              padx=5, pady=5)
        self.current_rendered_window["buttons_frame"].grid(row=0, column=4, padx=5, pady=5, sticky="NW")
        self.current_rendered_window["buttons_frame"].bind("<MouseWheel>", self.mouse_wheel)

        # Create top-bar dropdown menus
        self.current_rendered_window["ep_drop"] = OptionMenu(self.current_rendered_window["options_frame"],
                                                             self.current_rendered_window["current_selected_epistle"],
                                                             *epistles, command=self.change_epistle)
        self.current_rendered_window["ep_drop"].grid(row=0, column=0)
        self.current_rendered_window["ep_drop"].bind("<MouseWheel>", self.mouse_wheel)

        self.current_rendered_window["fol_drop"] = OptionMenu(self.current_rendered_window["options_frame"],
                                                              self.current_rendered_window["current_selected_folio"],
                                                              *cur_fols, command=self.change_folio)
        self.current_rendered_window["fol_drop"].grid(row=0, column=1)
        self.current_rendered_window["fol_drop"].bind("<MouseWheel>", self.mouse_wheel)

        self.current_rendered_window["gloss_drop"] = OptionMenu(self.current_rendered_window["options_frame"],
                                                                self.current_rendered_window["current_selected_gloss"],
                                                                *cur_glossnums, command=self.change_gloss)
        self.current_rendered_window["gloss_drop"].grid(row=0, column=2)
        self.current_rendered_window["gloss_drop"].bind("<MouseWheel>", self.mouse_wheel)

        # Create GUI buttons
        self.current_rendered_window["back_button"] = Button(self.current_rendered_window["nav_buttons_frame"],
                                                             text="Back", command=self.last_gloss)
        self.current_rendered_window["back_button"].grid(row=0, column=0, padx=5, pady=5)
        self.current_rendered_window["back_button"].bind("<MouseWheel>", self.mouse_wheel)

        self.current_rendered_window["next_button"] = Button(self.current_rendered_window["nav_buttons_frame"],
                                                             text="Next", command=self.next_gloss)
        self.current_rendered_window["next_button"].grid(row=0, column=1, padx=5, pady=5)
        self.current_rendered_window["next_button"].bind("<MouseWheel>", self.mouse_wheel)

        self.current_rendered_window["update_button"] = Button(self.current_rendered_window["buttons_frame"],
                                                               text="Update Tokens", command=self.update_tokens)
        self.current_rendered_window["update_button"].grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.current_rendered_window["update_button"].bind("<MouseWheel>", self.mouse_wheel)

        self.current_rendered_window["save_button"] = Button(self.current_rendered_window["buttons_frame"],
                                                             text="Save", command=self.save_tokens)
        self.current_rendered_window["save_button"].grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.current_rendered_window["save_button"].bind("<MouseWheel>", self.mouse_wheel)

        # Create GUI text display boxes
        self.current_rendered_window["gloss_label"] = Label(self.current_rendered_window["text_frame"],
                                                            height=2, text=f"Gloss ({cur_glossid[3:]}) – {cur_hand}:",
                                                            font=("Helvetica", 16))

        gloss_points = self.emp_points(cur_gloss)
        clean_gloss = gloss_points[0]
        gloss_emphs = gloss_points[1]
        self.current_rendered_window["gloss_text"] = Text(self.current_rendered_window["text_frame"],
                                                          width=self.max_linelen, height=5, font=("Courier", 12))
        self.current_rendered_window["gloss_text"].insert(1.0, clean_gloss)
        self.italicise_text(self.current_rendered_window["gloss_text"], gloss_emphs)
        self.current_rendered_window["gloss_text"].config(state=DISABLED)

        self.current_rendered_window["trans_label"] = Label(self.current_rendered_window["text_frame"],
                                                            height=1, text="Translation:", font=("Helvetica", 16))

        trans_points = self.emp_points(cur_trans)
        clean_trans = trans_points[0]
        trans_emphs = trans_points[1]
        self.current_rendered_window["trans_text"] = Text(self.current_rendered_window["text_frame"],
                                                          width=self.max_linelen, height=5, font=("Courier", 12))
        self.current_rendered_window["trans_text"].insert(1.0, clean_trans)
        self.italicise_text(self.current_rendered_window["trans_text"], trans_emphs)
        self.current_rendered_window["trans_text"].config(state=DISABLED)

        self.current_rendered_window["gloss_label"].pack(anchor='w')
        self.current_rendered_window["gloss_label"].bind("<MouseWheel>", self.mouse_wheel)
        self.current_rendered_window["gloss_text"].pack(pady=5, anchor='w')
        self.current_rendered_window["gloss_text"].bind("<MouseWheel>", self.mouse_wheel)
        self.current_rendered_window["trans_label"].pack(anchor='w')
        self.current_rendered_window["trans_label"].bind("<MouseWheel>", self.mouse_wheel)
        self.current_rendered_window["trans_text"].pack(pady=5, anchor='w')
        self.current_rendered_window["trans_text"].bind("<MouseWheel>", self.mouse_wheel)

        # Create GUI text labels and editing boxes
        self.current_rendered_window["tokenise_label"] = Label(self.current_rendered_window["text_frame"],
                                                               height=2, text=f"Tokenise Gloss",
                                                               font=("Helvetica", 16))
        self.current_rendered_window["tokenise_text"] = Text(self.current_rendered_window["text_frame"],
                                                             width=self.max_linelen, height=5, borderwidth=1,
                                                             relief="solid", font=("Courier", 12))
        self.current_rendered_window["tokenise_text"].insert(1.0, self.set_spacing(" ".join([i[0] for i in cur_toks])))

        self.current_rendered_window["tokenise_label"].pack(anchor='w')
        self.current_rendered_window["tokenise_label"].bind("<MouseWheel>", self.mouse_wheel)
        self.current_rendered_window["tokenise_text"].pack(pady=5, anchor='w')
        self.current_rendered_window["tokenise_text"].bind("<MouseWheel>", self.mouse_wheel)

        # Create labels for the tokens, POS tags and headwords
        self.current_rendered_window["toks_label"] = Label(self.current_rendered_window["toks_frame"],
                                                           text="Tokens", font=("Helvetica", 16))
        self.current_rendered_window["toks_label"].grid(row=0, column=0, padx=5, pady=5)
        self.current_rendered_window["toks_label"].bind("<MouseWheel>", self.mouse_wheel)

        self.current_rendered_window["head_label"] = Label(self.current_rendered_window["toks_frame"],
                                                           text="Headword", font=("Helvetica", 16))
        self.current_rendered_window["head_label"].grid(row=0, column=1, padx=5, pady=5)
        self.current_rendered_window["head_label"].bind("<MouseWheel>", self.mouse_wheel)

        self.current_rendered_window["pos_label"] = Label(self.current_rendered_window["toks_frame"],
                                                          text="POS", font=("Helvetica", 16))
        self.current_rendered_window["pos_label"].grid(row=0, column=2, padx=5, pady=5)
        self.current_rendered_window["pos_label"].bind("<MouseWheel>", self.mouse_wheel)

        self.current_rendered_window["feats_label"] = Label(self.current_rendered_window["toks_frame"],
                                                            text="Features", font=("Helvetica", 16))
        self.current_rendered_window["feats_label"].grid(row=0, column=4, padx=5, pady=5)
        self.current_rendered_window["feats_label"].bind("<MouseWheel>", self.mouse_wheel)

        # Create tokens, POS menus and headword entry boxes for the tokens and POS tags
        self.cur_toks = cur_toks
        self.featureframe_count = 0
        for i, pos_token in enumerate(cur_toks):
            lexicon = self.lexicon
            token = pos_token[0]
            tag = pos_token[1]
            head = pos_token[2]
            feats = pos_token[3]
            if feats:
                feats = {f.split("=")[0]: f.split("=")[1] for f in feats.split("|")}
            finds = " ".join(gloss_emphs)
            finds_list = " ".join(finds.split("\n")).split(" ")
            if token in finds_list and tag == "<unknown>":
                tag = "<Latin>"
                if head == "<unknown>":
                    head = "Latin *"
            if tag not in ["<Latin>", "<Greek>", "<unknown>"] and (head == "<unknown>" or head[-2:] == " *"):
                lex_toks = list()
                for level_1 in lexicon:
                    lex_pos = level_1.get("part_of_speech")
                    if lex_pos == tag:
                        lex_lemmata = level_1.get("lemmata")
                        for level_2 in lex_lemmata:
                            lex_lemma = level_2.get("lemma")
                            lex_tokens = level_2.get("tokens")
                            lex_toks = lex_toks + [[lex_token.get("token"), lex_lemma] for lex_token in lex_tokens]
                if lex_toks:
                    head_candidates = [i for i in lex_toks if i[0] == token]
                    if not head_candidates:
                        ed_dists = [edit_distance(token, i[0]) for i in lex_toks]
                        lex_toks = [i + [j] for i, j in zip(lex_toks, ed_dists)]
                        lowest_ed = min(ed_dists)
                        head_candidates = [i[:2] for i in lex_toks if i[2] == lowest_ed]
                    if len(head_candidates) > 1:
                        sec_ed_dists = [edit_distance(token, i[1]) for i in head_candidates]
                        head_match_dists = [i + [j] for i, j in zip(head_candidates, sec_ed_dists)]
                        sec_lowest_ed = min(sec_ed_dists)
                        head_candidates = [i[:2] for i in head_match_dists if i[2] == sec_lowest_ed]
                        if len(head_candidates) == 1:
                            head_candidate = head_candidates[0]
                        else:
                            third_ed_dists = [
                                edit_distance(unidecode.unidecode(token),
                                              unidecode.unidecode(i[0]))
                                for i in head_candidates
                            ]
                            third_lowest_ed = min(third_ed_dists)
                            head_candidate = head_candidates[third_ed_dists.index(third_lowest_ed)]
                    elif len(head_candidates) == 1:
                        head_candidate = head_candidates[0]
                    else:
                        raise RuntimeError(f"Could not find appropriate candidate in list:\n    {head_candidates}")
                    head = f"{head_candidate[1]} *"
            self.current_rendered_window[f"toks_tok_{i}"] = Label(self.current_rendered_window["toks_frame"],
                                                                  text=" ".join(token.split("_")),
                                                                  font=("Helvetica", 12))
            self.current_rendered_window[f"toks_tok_{i}"].grid(row=i + 1, column=0, padx=5, pady=5, sticky='ne')
            self.current_rendered_window[f"toks_tok_{i}"].bind("<MouseWheel>", self.mouse_wheel)

            self.current_rendered_window[f"head_word.{i}"] = Text(self.current_rendered_window["toks_frame"],
                                                                  height=1, width=12, font=("Helvetica", 12))
            self.current_rendered_window[f"head_word.{i}"].insert(1.0, head)
            self.current_rendered_window[f"head_word.{i}"].grid(row=i + 1, column=1, padx=5, pady=5, sticky='nw')
            self.current_rendered_window[f"head_word.{i}"].bind("<MouseWheel>", self.mouse_wheel)

            self.current_rendered_window[f"type_pos{i}"] = StringVar()
            self.current_rendered_window[f"type_pos{i}"].set(tag)
            self.current_rendered_window[f"pos_drop.{i}"] = OptionMenu(self.current_rendered_window["toks_frame"],
                                                                       self.current_rendered_window[f"type_pos{i}"],
                                                                       *self.pos_tags)
            self.current_rendered_window[f"pos_drop.{i}"].grid(row=i + 1, column=2, sticky='ne')
            self.current_rendered_window[f"pos_drop.{i}"].bind("<MouseWheel>", self.mouse_wheel)

            # Create feature dropdown menus for the tokens which can take them
            if tag == "ADP":
                possible_feats = self.adp_feats
            elif tag == "PRON":
                possible_feats = self.pron_feats
            else:
                possible_feats = dict()

            if possible_feats:
                self.current_rendered_window[f"feats_check.{i}_var"] = IntVar()
                if feats:
                    feats_list = list()
                    for num, pos_feat in enumerate(possible_feats):
                        for key in feats:
                            if pos_feat == key:
                                feats_list.append(f"{num + 1}.{feats.get(key)}")
                                break
                    feat_str = "; ".join(feats_list)
                else:
                    feat_str = ''

                self.current_rendered_window[f"feats.{i}_label"] = Label(
                    self.current_rendered_window[f"feats_frame_{i}"], text=feat_str, font=("Helvetica", 10)
                )
                self.current_rendered_window[f"feats.{i}_label"].grid(row=0, column=0, sticky='w')
                self.current_rendered_window[f"feats.{i}_label"].bind("<MouseWheel>", self.mouse_wheel)

                self.current_rendered_window[f"feats_check.{i}"] = Checkbutton(
                    self.current_rendered_window["toks_frame"],
                    text="Show:", font=("Helvetica", 10),
                    variable=self.current_rendered_window[f"feats_check.{i}_var"],
                    command=lambda chk=i: self.display_features(chk)
                )
                self.current_rendered_window[f"feats_check.{i}"].grid(row=i + 1, column=3, padx=5, pady=5, sticky='nw')
                self.current_rendered_window[f"feats_check.{i}"].bind("<MouseWheel>", self.mouse_wheel)

            self.current_rendered_window[f"suggest_head.{i}"] = Button(self.current_rendered_window["toks_frame"],
                                                                       text=" ? ",
                                                                       command=lambda but=i: self.suggest_head(but))
            self.current_rendered_window[f"suggest_head.{i}"].grid(row=i + 1, column=5, padx=5, pady=5, sticky='n')
            self.current_rendered_window[f"suggest_head.{i}"].bind("<MouseWheel>", self.mouse_wheel)

            self.featureframe_count = i

        # Display possibly matching headwords' list if one of the headword-search buttons has been pressed
        if self.lex_toks:
            lex_toks = self.lex_toks[0]
            token = self.lex_toks[1]
            tag = self.lex_toks[2]
            button_num = self.lex_toks[3]
            ed_dists = [edit_distance(token, i[0]) for i in lex_toks]
            lex_toks = [i + [j] for i, j in zip(lex_toks, ed_dists)]
            lex_toks.sort(key=lambda x: x[2])
            if len(lex_toks) > 50:
                lex_toks = lex_toks[:50]

            for i, option in enumerate(lex_toks):
                features = list()
                for level_1 in self.lexicon:
                    lex_pos = level_1.get("part_of_speech")
                    if lex_pos == tag:
                        lex_lemmata = level_1.get("lemmata")
                        for level_2 in lex_lemmata:
                            lex_lemma = level_2.get("lemma")
                            if lex_lemma == option[1]:
                                lex_tokens = level_2.get("tokens")
                                for level_3 in lex_tokens:
                                    lex_token = level_3.get("token")
                                    if lex_token == option[0]:
                                        lex_feat_sets = level_3.get("feature_sets")
                                        for level_4 in lex_feat_sets:
                                            lex_feature_set = level_4.get("features")
                                            if lex_feature_set:
                                                for level_5 in lex_feature_set:
                                                    features.append(";  ".join([f"{feat}={level_5.get(feat)}"
                                                                                for feat in level_5]))
                if len(features) > 1:
                    for j, feature in enumerate(features):
                        features[j] = f"{j + 1}. {feature}"
                features = "\n".join(features)

                self.current_rendered_window[f"tok_button{i}"] = Button(
                    self.current_rendered_window["head_opts_frame"],
                    text=option[0], width=15,
                    command=lambda headword=option[1]: self.select_head(headword, button_num)
                )
                self.current_rendered_window[f"tok_button{i}"].grid(row=2 + i, column=0, padx=5, pady=5, sticky="e")
                self.current_rendered_window[f"tok_button{i}"].bind("<MouseWheel>", self.mouse_wheel)

                self.current_rendered_window[f"head{i}"] = Label(self.current_rendered_window["head_opts_frame"],
                                                                 text=option[1], font=("Helvetica", 10))
                self.current_rendered_window[f"head{i}"].grid(row=2 + i, column=1, padx=5, pady=5)
                self.current_rendered_window[f"head{i}"].bind("<MouseWheel>", self.mouse_wheel)

                self.current_rendered_window[f"ed_dist{i}"] = Label(
                    self.current_rendered_window["head_opts_frame"],
                    text=option[2], font=("Helvetica", 10))
                self.current_rendered_window[f"ed_dist{i}"].grid(row=2 + i, column=2, padx=5, pady=5)
                self.current_rendered_window[f"ed_dist{i}"].bind("<MouseWheel>", self.mouse_wheel)

                self.current_rendered_window[f"feat_str{i}"] = Label(
                    self.current_rendered_window["head_opts_frame"],
                    text=features, font=("Helvetica", 10), justify=LEFT)
                self.current_rendered_window[f"feat_str{i}"].grid(row=2 + i, column=3, padx=5, pady=5, sticky="w")
                self.current_rendered_window[f"feat_str{i}"].bind("<MouseWheel>", self.mouse_wheel)

            self.current_rendered_window["killme"] = Button(self.current_rendered_window["head_opts_frame"],
                                                            text=" X ", command=self.remove_head_options)
            self.current_rendered_window["killme"].grid(row=0, column=4, padx=5, pady=5, sticky="NE")
            self.current_rendered_window["killme"].bind("<MouseWheel>", self.mouse_wheel)

            self.current_rendered_window["tok_label"] = Label(self.current_rendered_window["head_opts_frame"],
                                                              text="Token", font=("Helvetica", 12))
            self.current_rendered_window["tok_label"].grid(row=1, column=0, padx=5, pady=5)
            self.current_rendered_window["tok_label"].bind("<MouseWheel>", self.mouse_wheel)

            self.current_rendered_window["head_label"] = Label(self.current_rendered_window["head_opts_frame"],
                                                               text="Headword", font=("Helvetica", 12))
            self.current_rendered_window["head_label"].grid(row=1, column=1, padx=5, pady=5)
            self.current_rendered_window["head_label"].bind("<MouseWheel>", self.mouse_wheel)

            self.current_rendered_window["ed_label"] = Label(self.current_rendered_window["head_opts_frame"],
                                                             text="Edit Dist.", font=("Helvetica", 12))
            self.current_rendered_window["ed_label"].grid(row=1, column=2, padx=5, pady=5)
            self.current_rendered_window["ed_label"].bind("<MouseWheel>", self.mouse_wheel)

            self.current_rendered_window["featsets_label"] = Label(self.current_rendered_window["head_opts_frame"],
                                                                   text="Features", font=("Helvetica", 12))
            self.current_rendered_window["featsets_label"].grid(row=1, column=3, padx=5, pady=5)
            self.current_rendered_window["featsets_label"].bind("<MouseWheel>", self.mouse_wheel)

    def remove_head_options(self):
        self.current_rendered_window["head_opts_frame"].destroy()
        self.current_rendered_window["head_opts_frame"] = LabelFrame(self.current_rendered_window["toks_frames"],
                                                                     padx=5, pady=5)
        self.current_rendered_window["head_opts_frame"].grid(row=0, column=1, padx=5, pady=5, sticky="NW")
        self.current_rendered_window["head_opts_frame"].bind("<MouseWheel>", self.mouse_wheel)
        self.lex_toks = list()

    def select_head(self, head, button_num):
        self.current_rendered_window[f"head_word.{button_num}"].delete(1.0, END)
        self.current_rendered_window[f"head_word.{button_num}"].insert(1.0, head)
        self.remove_head_options()

    def suggest_head(self, button_num):
        self.current_rendered_window["head_opts_frame"].destroy()
        self.current_rendered_window["head_opts_frame"] = LabelFrame(self.current_rendered_window["toks_frames"],
                                                                     padx=5, pady=5)
        self.current_rendered_window["head_opts_frame"].grid(row=0, column=1, padx=5, pady=5, sticky="NW")
        self.current_rendered_window["head_opts_frame"].bind("<MouseWheel>", self.mouse_wheel)
        self.update_tokens()

        all_tokens = self.cur_toks
        updated_tokens = [self.current_rendered_window[f"toks_tok_{i}"].cget("text") for i in range(len(all_tokens))]
        token = updated_tokens[button_num]
        updated_pos = [self.current_rendered_window[f"type_pos{i}"].get() for i in range(len(all_tokens))]
        tag = updated_pos[button_num]

        lex_toks = list()
        for level_1 in self.lexicon:
            lex_pos = level_1.get("part_of_speech")
            if lex_pos == tag:
                lex_lemmata = level_1.get("lemmata")
                for level_2 in lex_lemmata:
                    lex_lemma = level_2.get("lemma")
                    lex_tokens = level_2.get("tokens")
                    lex_toks = lex_toks + [[lex_token.get("token"), lex_lemma] for lex_token in lex_tokens]
        self.lex_toks = [lex_toks, token, tag, button_num]

        self.selected_gloss_info = self.create_gloss_info(
            selected_epistle=self.current_rendered_window["current_selected_epistle"].get(),
            selected_folio=self.current_rendered_window["current_selected_folio"].get(),
            selected_glossnum=self.current_rendered_window["current_selected_gloss"].get()
        )

        self.render_gloss(
            self.root,
            epistles=self.epistles,
            cur_ep=self.selected_gloss_info["selected_epistle"],
            cur_fols=self.selected_gloss_info["selected_fols"],
            cur_folio=self.selected_gloss_info["selected_folio"],
            cur_glossnums=self.selected_gloss_info["selected_glossnums"],
            cur_glossnum=self.selected_gloss_info["selected_glossnum"],
            cur_glossid=self.selected_gloss_info["selected_glossid"],
            cur_hand=self.selected_gloss_info["selected_hand"],
            cur_gloss=self.selected_gloss_info["selected_gloss"],
            cur_trans=self.selected_gloss_info["selected_trans"],
            cur_toks=self.cur_toks
        )

    def display_features(self, tok_num):

        on_off = self.current_rendered_window[f"feats_check.{tok_num}_var"].get()
        feats = self.cur_toks[tok_num][3]
        if feats:
            feats = {f.split("=")[0]: f.split("=")[1] for f in feats.split("|")}
        else:
            feats = dict()
        tag = self.cur_toks[tok_num][1]
        if tag == "ADP":
            possible_feats = self.adp_feats
        elif tag == "PRON":
            possible_feats = self.pron_feats
        else:
            possible_feats = dict()

        if on_off == 0:
            feats = {
                self.current_rendered_window[
                    f"feats.{tok_num}_label{j}"
                ].cget('text'): self.current_rendered_window[
                    f"type_feats{tok_num}.{j}"
                ].get() for j, _ in enumerate(possible_feats)
                if self.current_rendered_window[f"type_feats{tok_num}.{j}"].get() != "N/A"
            }

            for j, _ in enumerate(possible_feats):
                self.current_rendered_window[f"feats.{tok_num}_label{j}"].destroy()
                self.current_rendered_window[f"feats_drop.{tok_num}.{j}"].destroy()

            feats_list = list()
            fullfeats_list = list()
            for j, pos_feat in enumerate(possible_feats):
                for key in feats:
                    if pos_feat == key:
                        feats_list.append(f"{j + 1}.{feats.get(key)}")
                        fullfeats_list.append(f"{key}={feats.get(key)}")
                        break
            feat_str = "; ".join(feats_list)
            fullfeat_str = "|".join(fullfeats_list)
            self.cur_toks[tok_num][3] = fullfeat_str
            self.current_rendered_window[f"feats.{tok_num}_label"] = Label(
                self.current_rendered_window[f"feats_frame_{tok_num}"], text=feat_str, font=("Helvetica", 10)
            )
            self.current_rendered_window[f"feats.{tok_num}_label"].grid(row=0, column=0, sticky='w')
            self.current_rendered_window[f"feats.{tok_num}_label"].bind("<MouseWheel>", self.mouse_wheel)

        elif on_off == 1:
            self.current_rendered_window[f"feats.{tok_num}_label"].destroy()

            fullfeats_list = list()
            for j, feat_type in enumerate(possible_feats):
                feat_vals = possible_feats.get(feat_type)
                if feats:
                    if feats.get(feat_type):
                        set_val = feats.get(feat_type)
                        fullfeats_list.append(f"{feat_type}={set_val}")
                    else:
                        set_val = "N/A"
                else:
                    set_val = "N/A"
                if set_val != "N/A" and set_val not in feat_vals:
                    raise RuntimeError(f"Unexpected feature value pre-set: "
                                       f"{feat_type}={set_val} for {tag} in {feat_vals}")

                self.current_rendered_window[f"feats.{tok_num}_label{j}"] = Label(
                    self.current_rendered_window[f"feats_frame_{tok_num}"], text=feat_type, font=("Helvetica", 10)
                )
                self.current_rendered_window[f"feats.{tok_num}_label{j}"].grid(row=j, column=0, sticky='w')
                self.current_rendered_window[f"feats.{tok_num}_label{j}"].bind("<MouseWheel>", self.mouse_wheel)

                self.current_rendered_window[f"type_feats{tok_num}.{j}"] = StringVar()
                self.current_rendered_window[f"type_feats{tok_num}.{j}"].set(set_val)
                self.current_rendered_window[f"feats_drop.{tok_num}.{j}"] = OptionMenu(
                    self.current_rendered_window[f"feats_frame_{tok_num}"],
                    self.current_rendered_window[f"type_feats{tok_num}.{j}"],
                    *feat_vals
                )
                self.current_rendered_window[f"feats_drop.{tok_num}.{j}"].grid(row=j, column=1, sticky='w')
                self.current_rendered_window[f"feats_drop.{tok_num}.{j}"].bind("<MouseWheel>", self.mouse_wheel)
            fullfeat_str = "|".join(fullfeats_list)
            self.cur_toks[tok_num][3] = fullfeat_str

    def update_tokens(self):
        """Update tokens after applying tokenisation, POS-tagging, etc., by clicking the update button"""
        string = self.current_rendered_window["tokenise_text"].get(1.0, END)
        tokens = self.cur_toks
        updated_pos = [self.current_rendered_window[f"type_pos{i}"].get() for i in range(len(tokens))]
        updated_feats = list()
        for i, pos_check in enumerate(updated_pos):
            new_pos = False
            if pos_check in ["ADP", "PRON"]:
                found_feats = list()
                try:
                    on_off = self.current_rendered_window[f"feats_check.{i}_var"].get()
                except KeyError:
                    on_off = 0
                    new_pos = True
                if new_pos:
                    found_feats = ['']
                elif pos_check == "ADP":
                    for j, feat_key in enumerate(self.adp_feats):
                        feat_val = "N/A"
                        if on_off == 0:
                            feat_str = self.current_rendered_window[f"feats.{i}_label"].cget("text")
                            if not feat_str:
                                found_feats = ['']
                                break
                            feat_list = feat_str.split("; ")
                            for numbered_feat in feat_list:
                                feat_numstring_split = numbered_feat.split(".")
                                feat_num = feat_numstring_split[0]
                                if int(feat_num) == j + 1:
                                    feat_val = feat_numstring_split[1]
                                    break
                        elif on_off == 1:
                            try:
                                feat_val = self.current_rendered_window[f"type_feats{i}.{j}"].get()
                            except KeyError:
                                feat_val = "N/A"
                        if feat_val != "N/A":
                            found_feats.append(f"{feat_key}={feat_val}")
                elif pos_check == "PRON":
                    for j, feat_key in enumerate(self.pron_feats):
                        feat_val = "N/A"
                        if on_off == 0:
                            feat_str = self.current_rendered_window[f"feats.{i}_label"].cget("text")
                            if not feat_str:
                                found_feats = ['']
                                break
                            feat_list = feat_str.split("; ")
                            for numbered_feat in feat_list:
                                feat_numstring_split = numbered_feat.split(".")
                                feat_num = feat_numstring_split[0]
                                if int(feat_num) == j + 1:
                                    feat_val = feat_numstring_split[1]
                                    break
                        elif on_off == 1:
                            try:
                                feat_val = self.current_rendered_window[f"type_feats{i}.{j}"].get()
                            except KeyError:
                                feat_val = "N/A"
                        if feat_val != "N/A":
                            found_feats.append(f"{feat_key}={feat_val}")
                if found_feats:
                    found_feats = "|".join(found_feats)
                    updated_feats.append(found_feats)
                else:
                    updated_feats.append(None)
            else:
                updated_feats.append(None)
        updated_head = [self.current_rendered_window[f"head_word.{i}"].get(1.0, END) for i in range(len(tokens))]
        if len(tokens) != len(updated_pos)\
                or len(tokens) != len(updated_feats)\
                or len(tokens) != len(updated_feats):
            raise RuntimeError("Different counts found for tokens before and after POS-tagging")
        if [i[1] for i in tokens] != updated_pos:
            tokens = [[i[0], j, i[2], i[3]] for i, j in zip(tokens, updated_pos)]
        if [i[2] for i in tokens] != updated_head:
            tokens = [[i[0], i[1], j.strip(), i[3]] for i, j in zip(tokens, updated_head)]
        if [i[3] for i in tokens] != updated_feats:
            tokens = [[i[0], i[1], i[2], j] if (i[2] not in [".i.", "⁊rl."]
                                                and i[1] not in ["<Latin>", "<Greek>", "<Latin CCONJ>", "<unknown>"])
                      else i for i, j in zip(tokens, updated_feats)]

        tokens = [i if i[1:3] not in [
            ['<Greek>', 'Latin *'], ['<Greek>', '<unknown>']
        ] else [i[0], i[1], 'Greek *', i[3]] for i in tokens]

        self.selected_gloss_info = self.create_gloss_info(
            selected_epistle=self.current_rendered_window["current_selected_epistle"].get(),
            selected_folio=self.current_rendered_window["current_selected_folio"].get(),
            selected_glossnum=self.current_rendered_window["current_selected_gloss"].get()
        )

        self.render_gloss(
            self.root,
            epistles=self.epistles,
            cur_ep=self.selected_gloss_info["selected_epistle"],
            cur_fols=self.selected_gloss_info["selected_fols"],
            cur_folio=self.selected_gloss_info["selected_folio"],
            cur_glossnums=self.selected_gloss_info["selected_glossnums"],
            cur_glossnum=self.selected_gloss_info["selected_glossnum"],
            cur_glossid=self.selected_gloss_info["selected_glossid"],
            cur_hand=self.selected_gloss_info["selected_hand"],
            cur_gloss=self.selected_gloss_info["selected_gloss"],
            cur_trans=self.selected_gloss_info["selected_trans"],
            cur_toks=refresh_tokens(string, tokens)
        )

    def save_tokens(self):
        """First, updates all tokens, so that no outstanding changes are remaining only on-screen.
           Next, updates the entry for this gloss in the Manual Tokenisation JSON file.
           Finally, updates working lexicon file with any new Irish lexical content"""

        self.update_tokens()

        # Check if a lexicon, potentially with eDIL lexeme IDs, already exists.
        # If so, create a simplified lexicon dictionary to use to find eDIL lexeme ID numbers
        try:
            try_path = os.path.join(os.getcwd(), "Manual_Tokenise_Files")
            if "Working_lexicon.json" in os.listdir(try_path):
                with open(os.path.join(try_path, "Working_lexicon.json"), 'r', encoding="utf-8") as lex_file_json:
                    lex_dict = json.load(lex_file_json)
                    lex_dict = {
                        pos.get("part_of_speech"): {
                            lem.get("lemma"): lem.get("eDIL_id") for lem in pos.get("lemmata")
                        } for pos in lex_dict
                    }
            else:
                lex_dict = None
        except FileNotFoundError:
            lex_dict = None

        file_name = self.file_name
        main_file = self.wb_data
        current_glossnum = self.current_rendered_window["current_selected_gloss"].get()
        current_folio = self.current_rendered_window["current_selected_folio"].get()
        current_epistle = self.current_rendered_window["current_selected_epistle"].get()

        # Remove Latin and Greek headword placeholders
        tokens = [[i, j, "", l] if k in ["Latin *", "Greek *"] else [i, j, k, l] for i, j, k, l in self.cur_toks]
        # Remove * from automatically supplied lemmata before saving them
        tokens = [[i, j, "".join(k.split(" *")), l] if " *" in k else [i, j, k, l] for i, j, k, l in tokens]
        # Replace underscore characters with space for tokens with internal spacing
        tokens = [t if "_" not in t[0] else [" ".join(t[0].split("_")), t[1], t[2], t[3]] for t in tokens]

        # Update Manual Tokenisation JSON file
        for epistle in main_file:
            ep_name = epistle['epistle']
            if ep_name == current_epistle:
                folios = epistle['folios']
                for folio_data in folios:
                    fol_num = folio_data['folio']
                    if fol_num == current_folio:
                        glosses = folio_data['glosses']
                        for gloss_data in glosses:
                            gloss_no = gloss_data['glossNo']
                            if gloss_no == current_glossnum:
                                gloss_data["glossTokens"] = tokens
                                break
        overwrite_json(os.path.join(os.getcwd(), "Manual_Tokenise_Files", file_name), main_file)

        # Update working lexicon file with any new Irish content
        working_file = self.lexicon
        for tok in tokens:
            tok_pos = tok[1]
            tok_head = tok[2]
            found_lex_id = None
            # Ensure the token is Irish
            if tok_pos not in ["<unknown>", "<Latin>", "<Latin CCONJ>", "<Greek>"] and tok_head[-2:] != " *":
                tok_form = tok[0]
                tok_feats = tok[3]
                if tok_feats:
                    tok_feats = [{i[0]: i[1] for i in [j.split("=") for j in tok_feats.split("|")]}]
                # Exclude common abbreviations
                if tok_form not in [".i.", "ɫ.", "ɫ"]:
                    all_filepos = [level_1.get("part_of_speech") for level_1 in working_file]
                    # If the POS-tag is a POS-tag that already occurs in the working lexicon
                    if tok_pos in all_filepos:
                        file_pos_data = working_file[all_filepos.index(tok_pos)].get("lemmata")
                        all_filelemmata = [level_2.get("lemma") for level_2 in file_pos_data]
                        pos_id_dict = {level_2.get("lemma"): level_2.get("eDIL_id") for level_2 in file_pos_data}
                        # If the lemma is a lemma that already occurs in the working lexicon
                        if tok_head in all_filelemmata:
                            found_lex_id = pos_id_dict.get(tok_head)
                            file_tok_data = file_pos_data[all_filelemmata.index(tok_head)].get("tokens")
                            all_filetoks = [level_3.get("token") for level_3 in file_tok_data]
                            # If the token is a token that already occurs in the working lexicon
                            if tok_form in all_filetoks:
                                file_featsets_data = file_tok_data[all_filetoks.index(tok_form)].get("feature_sets")
                                all_feats = [level_4.get("features") for level_4 in file_featsets_data]
                                # If the morpho-features DO NOT already occur in the working lexicon for this token
                                if tok_feats not in all_feats:
                                    # Add the new morphological features if other features already exist for this token
                                    if tok_feats:
                                        insert = {'feature_set': len(all_feats) + 1, 'features': tok_feats}
                                        file_featsets_data = file_featsets_data + [insert]
                                    else:
                                        # Create a new set of morphological features if necessary
                                        insert = {'feature_set': 1, 'features': tok_feats}
                                        for i in file_featsets_data:
                                            i['feature_set'] = i.get('feature_set') + 1
                                        file_featsets_data = [insert] + file_featsets_data
                                    # Cascade the newly added feature set up through the token, lemma and POS levels
                                    file_tok_data[all_filetoks.index(tok_form)] = {
                                        'token': tok_form, 'feature_sets': file_featsets_data
                                    }
                                    file_pos_data[all_filelemmata.index(tok_head)] = {
                                        'lemma': tok_head, 'eDIL_id': found_lex_id, 'tokens': file_tok_data
                                    }
                                    working_file[all_filepos.index(tok_pos)] = {
                                        'part_of_speech': tok_pos, 'lemmata': file_pos_data
                                    }
                            else:
                                # If the token IS NOT a token that already occurs in the working lexicon
                                # Find the correct position to insert it
                                filetoks_plus = sorted(list(set(
                                    [level_3.get("token") for level_3 in file_tok_data] + [tok_form]
                                )))
                                correct_position = filetoks_plus.index(tok_form)
                                # Insert it and any morphological feature sets in the correct position
                                insert = {'token': tok_form, 'feature_sets': [
                                    {'feature_set': 1, 'features': tok_feats}
                                ]}
                                file_tok_data = file_tok_data[:correct_position] + [
                                    insert
                                ] + file_tok_data[correct_position:]
                                # Cascade the newly added token up through the lemma and POS levels
                                file_pos_data[all_filelemmata.index(tok_head)] = {
                                    'lemma': tok_head, 'eDIL_id': found_lex_id, 'tokens': file_tok_data
                                }
                                working_file[all_filepos.index(tok_pos)] = {
                                    'part_of_speech': tok_pos, 'lemmata': file_pos_data
                                }
                        else:
                            # If the lemma IS NOT a lemma that already occurs in the working lexicon
                            # Find the correct position to insert it
                            filelemmata_plus = sorted(list(set(
                                [level_2.get("lemma") for level_2 in file_pos_data] + [tok_head]
                            )))
                            correct_position = filelemmata_plus.index(tok_head)
                            # Insert it, as well as any tokens and morphological feature sets in the correct position
                            insert = {'token': tok_form, 'feature_sets': [{'feature_set': 1, 'features': tok_feats}]}
                            insert = {'lemma': tok_head, 'eDIL_id': found_lex_id, 'tokens': [insert]}
                            file_pos_data = file_pos_data[:correct_position] + [
                                insert
                            ] + file_pos_data[correct_position:]
                            # Cascade the newly added lemma up to the POS level
                            working_file[all_filepos.index(tok_pos)] = {
                                'part_of_speech': tok_pos, 'lemmata': file_pos_data
                            }
                    else:
                        # If the POS-tag IS NOT a POS-tag that already occurs in the working lexicon
                        # Find the correct position to insert it at
                        filepos_plus = sorted(list(set(
                            [level_1.get("part_of_speech") for level_1 in working_file] + [tok_pos]
                        )))
                        correct_position = filepos_plus.index(tok_pos)
                        # Insert it, as well as any lemmata, tokens and morpho-feature sets in the correct position
                        insert = {'token': tok_form, 'feature_sets': [{'feature_set': 1, 'features': tok_feats}]}
                        insert = {'lemma': tok_head, 'eDIL_id': found_lex_id, 'tokens': [insert]}
                        insert = {'part_of_speech': tok_pos, 'lemmata': [insert]}
                        working_file = working_file[:correct_position] + [insert] + working_file[correct_position:]

        if lex_dict:
            for pos_data in working_file:
                curpos = pos_data.get("part_of_speech")
                lemmata = pos_data.get("lemmata")
                annotated_lemmata = lex_dict.get(curpos)
                for lemma_data in lemmata:
                    if annotated_lemmata.get(lemma_data.get("lemma")) and not lemma_data.get("eDIL_id"):
                        lemma_data["eDIL_id"] = annotated_lemmata.get(lemma_data.get("lemma"))

        with open(
                os.path.join(os.getcwd(), "Manual_tokenise_files", "Working_lexicon.json"
                             ), 'w', encoding="utf-8") as workfile:
            json.dump(working_file, workfile, indent=4, ensure_ascii=False)

        self.selected_gloss_info = self.create_gloss_info(
            selected_epistle=self.current_rendered_window["current_selected_epistle"].get(),
            selected_folio=self.current_rendered_window["current_selected_folio"].get(),
            selected_glossnum=self.current_rendered_window["current_selected_gloss"].get()
        )

        spaceless_toks = [
            t if " " not in t[0] else [
                "_".join(t[0].split(" ")), t[1], t[2], t[3]
            ] for t in self.selected_gloss_info["selected_toks"]
        ]

        self.render_gloss(
            self.root,
            epistles=self.epistles,
            cur_ep=self.selected_gloss_info["selected_epistle"],
            cur_fols=self.selected_gloss_info["selected_fols"],
            cur_folio=self.selected_gloss_info["selected_folio"],
            cur_glossnums=self.selected_gloss_info["selected_glossnums"],
            cur_glossnum=self.selected_gloss_info["selected_glossnum"],
            cur_glossid=self.selected_gloss_info["selected_glossid"],
            cur_hand=self.selected_gloss_info["selected_hand"],
            cur_gloss=self.selected_gloss_info["selected_gloss"],
            cur_trans=self.selected_gloss_info["selected_trans"],
            cur_toks=spaceless_toks
        )

    def last_gloss(self):
        """Displaying the previous gloss in the sequence of glosses"""
        self.remove_head_options()

        current_glossnum = self.current_rendered_window["current_selected_gloss"].get()
        current_folio = self.current_rendered_window["current_selected_folio"].get()
        current_epistle = self.current_rendered_window["current_selected_epistle"].get()

        current_glossnums = show_glossnums(select_folcol(select_epistle(current_epistle), current_folio))
        current_fols = show_folcols(select_epistle(current_epistle))
        epistles = self.epistles

        if current_glossnum != current_glossnums[0]:
            go_to_epistle = current_epistle
            go_to_folio = current_folio
            next_position = current_glossnums.index(current_glossnum) - 1
            go_to_gloss = current_glossnums[next_position]
        elif current_folio != current_fols[0]:
            go_to_epistle = current_epistle
            next_position = current_fols.index(current_folio) - 1
            go_to_folio = current_fols[next_position]
            next_glossnums = show_glossnums(select_folcol(select_epistle(go_to_epistle), go_to_folio))
            go_to_gloss = next_glossnums[-1]
        elif current_epistle != epistles[0]:
            next_position = epistles.index(current_epistle) - 1
            go_to_epistle = epistles[next_position]
            next_fols = show_folcols(select_epistle(go_to_epistle))
            go_to_folio = next_fols[-1]
            next_glossnums = show_glossnums(select_folcol(select_epistle(go_to_epistle), go_to_folio))
            go_to_gloss = next_glossnums[-1]
        else:
            go_to_gloss = current_glossnum
            go_to_folio = current_folio
            go_to_epistle = current_epistle

        self.selected_gloss_info = self.create_gloss_info(
            selected_epistle=go_to_epistle,
            selected_folio=go_to_folio,
            selected_glossnum=go_to_gloss
        )

        spaceless_toks = [
            t if " " not in t[0] else [
                "_".join(t[0].split(" ")), t[1], t[2], t[3]
            ] for t in self.selected_gloss_info["selected_toks"]
        ]

        self.render_gloss(
            self.root,
            epistles=self.epistles,
            cur_ep=self.selected_gloss_info["selected_epistle"],
            cur_fols=self.selected_gloss_info["selected_fols"],
            cur_folio=self.selected_gloss_info["selected_folio"],
            cur_glossnums=self.selected_gloss_info["selected_glossnums"],
            cur_glossnum=self.selected_gloss_info["selected_glossnum"],
            cur_glossid=self.selected_gloss_info["selected_glossid"],
            cur_hand=self.selected_gloss_info["selected_hand"],
            cur_gloss=self.selected_gloss_info["selected_gloss"],
            cur_trans=self.selected_gloss_info["selected_trans"],
            cur_toks=spaceless_toks
        )

    def next_gloss(self):
        """Display next gloss in sequence"""
        self.remove_head_options()

        current_glossnum = self.current_rendered_window["current_selected_gloss"].get()
        current_folio = self.current_rendered_window["current_selected_folio"].get()
        current_epistle = self.current_rendered_window["current_selected_epistle"].get()

        current_glossnums = show_glossnums(select_folcol(select_epistle(current_epistle), current_folio))
        current_fols = show_folcols(select_epistle(current_epistle))
        epistles = self.epistles

        if current_glossnum != current_glossnums[-1]:
            go_to_epistle = current_epistle
            go_to_folio = current_folio
            next_position = current_glossnums.index(current_glossnum) + 1
            go_to_gloss = current_glossnums[next_position]
        elif current_folio != current_fols[-1]:
            go_to_epistle = current_epistle
            next_position = current_fols.index(current_folio) + 1
            go_to_folio = current_fols[next_position]
            next_glossnums = show_glossnums(select_folcol(select_epistle(go_to_epistle), go_to_folio))
            go_to_gloss = next_glossnums[0]
        elif current_epistle != epistles[-1]:
            next_position = epistles.index(current_epistle) + 1
            go_to_epistle = epistles[next_position]
            next_fols = show_folcols(select_epistle(go_to_epistle))
            go_to_folio = next_fols[0]
            next_glossnums = show_glossnums(select_folcol(select_epistle(go_to_epistle), go_to_folio))
            go_to_gloss = next_glossnums[0]
        else:
            go_to_gloss = current_glossnum
            go_to_folio = current_folio
            go_to_epistle = current_epistle

        self.selected_gloss_info = self.create_gloss_info(
            selected_epistle=go_to_epistle,
            selected_folio=go_to_folio,
            selected_glossnum=go_to_gloss
        )

        spaceless_toks = [
            t if " " not in t[0] else [
                "_".join(t[0].split(" ")), t[1], t[2], t[3]
            ] for t in self.selected_gloss_info["selected_toks"]
        ]

        self.render_gloss(
            self.root,
            epistles=self.epistles,
            cur_ep=self.selected_gloss_info["selected_epistle"],
            cur_fols=self.selected_gloss_info["selected_fols"],
            cur_folio=self.selected_gloss_info["selected_folio"],
            cur_glossnums=self.selected_gloss_info["selected_glossnums"],
            cur_glossnum=self.selected_gloss_info["selected_glossnum"],
            cur_glossid=self.selected_gloss_info["selected_glossid"],
            cur_hand=self.selected_gloss_info["selected_hand"],
            cur_gloss=self.selected_gloss_info["selected_gloss"],
            cur_trans=self.selected_gloss_info["selected_trans"],
            cur_toks=spaceless_toks
        )

    def emp_points(self, text):
        """Identifies indices of tokens which should be italicised, removes emphasis tags"""
        suppat = re.compile(r'<sup>\w*</sup>')
        suppatiter = suppat.findall(text)
        if suppatiter:
            for suptag in suppatiter:
                text = "".join(text.split(suptag))
        text = " ".join(text.split("\n")).strip()
        text = self.set_spacing(text)
        finds = list()
        if "<em>et</em>" in text:
            text = "<em>&&</em>".join(text.split("<em>et</em>")).strip()
        if "<em>" in text:
            find_points = list()
            emcount = text.count("<em>")
            for _ in range(emcount):
                find_open = text.find("<em>")
                text = text[:find_open] + text[find_open + 4:]
                find_close = text.find("</em>")
                text = text[:find_close] + text[find_close + 5:]
                find_points.append([find_open, find_close])
            for points in find_points:
                finds.append(text[points[0]: points[1]])
        return [text, finds]

    def italicise_text(self, text_box, finds):
        """Italicises tokens at indices where emphasis tags occur in the annotated text"""
        italics_font = font.Font(text_box, text_box.cget("font"))
        italics_font.configure(weight="bold", slant="italic")

        text_box.tag_configure("italics", font=italics_font)

        text_in_box = text_box.get(1.0, END)

        used_points = list()
        find_points = list()
        for i, find in enumerate(finds):
            if find not in text_in_box:
                raise RuntimeError(f"Could not find text to italicise in textbox:\n    {find}\n    {text_in_box}")
            else:
                start_point = text_in_box.find(find)
                end_point = start_point + len(find)
                found_at = [start_point, end_point]
                if found_at in used_points:
                    while found_at in used_points:
                        reduced_text = text_in_box[end_point:]
                        start_point = end_point + reduced_text.find(find)
                        end_point = start_point + len(find)
                        found_at = [start_point, end_point]
                used_points.append(found_at)
                text_to_startpoint = text_in_box[:start_point]
                text_to_endpoint = text_in_box[:end_point]
                start_line = text_to_startpoint.count("\n") + 1
                end_line = text_to_endpoint.count("\n") + 1
                if "\n" in text_to_startpoint:
                    line_start_point = len(text_in_box[text_to_startpoint.rfind("\n") + 1: start_point])
                else:
                    line_start_point = start_point
                if "\n" in text_to_endpoint:
                    line_end_point = len(text_in_box[text_to_endpoint.rfind("\n") + 1: end_point])
                else:
                    line_end_point = end_point
                start_point = Decimal(f"{start_line}.{line_start_point}")
                end_point = Decimal(f"{end_line}.{line_end_point}")
                find_points.append([start_point, end_point])
        if "&&" in text_in_box:
            text_in_box = "et".join(text_in_box.split("&&"))
            text_box.delete(1.0, END)
            text_box.insert(1.0, text_in_box)
        for placed_find in find_points:
            start_point = placed_find[0]
            end_point = placed_find[1]
            text_box.tag_add("italics", start_point, end_point)

    def set_spacing(self, text):
        """Adds like breaks at the correct points so that line lengths do not exceed the maximum line-length allowed"""
        text = " ".join(text.split("\n")).strip()
        max_linelen = self.max_linelen
        text_cuts = list()
        if len(text) > max_linelen:
            first_cut = text[:max_linelen]
            last_spacepoint = first_cut.rfind(" ")
            text_cuts.append(first_cut[:last_spacepoint])
            remainder = text[last_spacepoint + 1:]
            if len(remainder) < max_linelen:
                text_cuts.append(remainder)
            else:
                while len(remainder) > max_linelen:
                    next_cut = remainder[:max_linelen]
                    last_spacepoint = next_cut.rfind(" ")
                    text_cuts.append(next_cut[:last_spacepoint])
                    remainder = remainder[last_spacepoint + 1:]
                    if len(remainder) <= max_linelen:
                        text_cuts.append(remainder)
            text = "\n".join(text_cuts)
        return text

    def check_lex_origin(self, check_list, orig_lex):
        """Look for a token (and its POS data) in the original (Sg. only) lexicon and return true if found"""

        # check if the check-list for a token has features or none
        if len(check_list) == 4:
            check_pos_tag, check_lemma, check_token, check_feat_vals = check_list[0], check_list[1], \
                                                                       check_list[2], check_list[3]
        elif len(check_list) == 3:
            check_pos_tag, check_lemma, check_token, check_feat_vals = check_list[0], check_list[1], \
                                                                       check_list[2], False
        else:
            raise RuntimeError("Unexpected check-list length")

        # look for the token in the original (Sg. only) lexicon for the token and return a true or false value
        check_found = False
        for pos_level in orig_lex:
            pos_tag = pos_level.get("part_of_speech")
            if pos_tag == check_pos_tag:
                lemmata_list = pos_level.get("lemmata")
                for lemmata_level in lemmata_list:
                    lemma = lemmata_level.get("lemma")
                    if lemma == check_lemma:
                        tokens_list = lemmata_level.get("tokens")
                        for tokens_level in tokens_list:
                            token = tokens_level.get("token")
                            if token == check_token:
                                if check_feat_vals:
                                    feat_sets_list = tokens_level.get("feature_sets")
                                    for feat_sets_level in feat_sets_list:
                                        features_list = feat_sets_level.get("features")
                                        if features_list:
                                            features_level = features_list[0]
                                            feat_keys = [i for i in features_level]
                                            feat_vals = [features_level.get(i) for i in features_level]
                                            feat_vals = "|".join(f"{i}={j}" for i, j in zip(feat_keys, feat_vals))
                                            if feat_vals == check_feat_vals:
                                                check_found = True
                                                return check_found
                                else:
                                    check_found = True
                                    return check_found
        return check_found

    def check_tokenised_file(self, checklist):
        """Look for a token (and its POS data) in the tokenised Wb. glosses file
           (Runs as the program is being closed)"""
        main_file = self.wb_data
        all_toks = list()
        for epistle in main_file:
            folios = epistle.get('folios')
            for folio_data in folios:
                glosses = folio_data.get('glosses')
                for gloss_data in glosses:
                    tokens = gloss_data.get(f"glossTokens")
                    tokens = [(i[1], i[2], i[0], i[3]) if [i[1], i[2]] not in [
                        ['<unknown>', '<unknown>'],
                        ['<Latin>', ''],
                        ['<Latin CCONJ>', 'et'],
                        ['<Greek>', '']
                    ] else () for i in tokens]
                    tokens = [i for i in tokens if i]
                    if tokens:
                        all_toks = all_toks + tokens
        all_toks = [i if i[3] else (i[0], i[1], i[2], '') for i in all_toks]
        all_toks = sorted(list(set(all_toks)))
        all_toks = [i if i[3] != '' else (i[0], i[1], i[2], None) for i in all_toks]
        all_toks = [[i[0], i[1], i[2].lower(), i[3]] for i in all_toks]
        results = [[i, True] if i in all_toks else [i, False] for i in checklist]
        return results

    def clear_lexica(self):
        """Check each lexicon for entries which do not occur in either Wb. or Sg. and removes them from the lexicon
           (Runs as the program is being closed)."""

        # create a list of tokens (and data) from a working lexicon which are not present in the original lexicon
        check_lex = list()
        for pos_level in self.lexicon:
            pos_tag = pos_level.get("part_of_speech")
            lemmata_list = pos_level.get("lemmata")
            for lemmata_level in lemmata_list:
                lemma = lemmata_level.get("lemma")
                tokens_list = lemmata_level.get("tokens")
                for tokens_level in tokens_list:
                    token = tokens_level.get("token")
                    feat_sets_list = tokens_level.get("feature_sets")
                    for feat_sets_level in feat_sets_list:
                        features_list = feat_sets_level.get("features")
                        if features_list:
                            features_level = features_list[0]
                            feat_keys = [i for i in features_level]
                            feat_vals = [features_level.get(i) for i in features_level]
                            feat_vals = "|".join(f"{i}={j}" for i, j in zip(feat_keys, feat_vals))
                            check = [pos_tag, lemma, token, feat_vals]
                            if not self.check_lex_origin(check, self.primary_lexicon):
                                check_lex.append(check)
                        else:
                            check = [pos_tag, lemma, token, None]
                            if not self.check_lex_origin(check, self.primary_lexicon):
                                check_lex.append(check)

        # check that all tokens found in the working lexicon which are not present in the original lexicon occur in
        # the manual tokenisation file for Wb.
        # if they do not occur, delete the entry from the working lexicon
        # reorder numbers for feature sets
        if check_lex:
            checked_lex = self.check_tokenised_file(check_lex)
            failed_lex = [i[0] for i in checked_lex if not i[1]]
            for failed_input in failed_lex:
                failed_pos = failed_input[0]
                failed_head = failed_input[1]
                failed_token = failed_input[2]
                failed_feats = failed_input[3]
                for pl, pos_level in enumerate(self.lexicon):
                    pos_tag = pos_level.get("part_of_speech")
                    if pos_tag == failed_pos:
                        lemmata_list = pos_level.get("lemmata")
                        for ll, lemmata_level in enumerate(lemmata_list):
                            lemma = lemmata_level.get("lemma")
                            if lemma == failed_head:
                                tokens_list = lemmata_level.get("tokens")
                                for tl, tokens_level in enumerate(tokens_list):
                                    token = tokens_level.get("token")
                                    if token == failed_token:
                                        feat_set_list = tokens_level.get("feature_sets")
                                        for fl, feat_set_level in enumerate(feat_set_list):
                                            features = feat_set_level.get("features")
                                            if features:
                                                features = "|".join(f"{i}={j}" for i, j in zip(
                                                    [i for i in features[0]], [features[0].get(i) for i in features[0]]
                                                ))
                                            if features == failed_feats:
                                                del feat_set_list[fl]
                                                if not feat_set_list:
                                                    del tokens_list[tl]
                                                if not tokens_list:
                                                    del lemmata_list[ll]
                                                if not lemmata_list:
                                                    del self.lexicon[pl]
                                                break

            # renumber all feature sets to ensure no numbers occur out of order
            for pl, pos_level in enumerate(self.lexicon):
                lemmata_list = pos_level.get("lemmata")
                for ll, lemmata_level in enumerate(lemmata_list):
                    tokens_list = lemmata_level.get("tokens")
                    for tl, tokens_level in enumerate(tokens_list):
                        feat_set_list = tokens_level.get("feature_sets")
                        set_count = 1
                        for fl, feat_set_level in enumerate(feat_set_list):
                            feat_set_level["feature_set"] = set_count
                            set_count += 1

            with open(
                    os.path.join(os.getcwd(), "Manual_tokenise_files", "Working_lexicon.json"), 'w', encoding="utf-8"
            ) as workfile:
                json.dump(self.lexicon, workfile, indent=4, ensure_ascii=False)


def refresh_tokens(string, tokens):
    """if new tokens have been created by adding spacing within the text-boxes
       return the new list of tokens, while keeping the data for tokens which are unchanged"""
    return_tokens = list()
    string = " ".join(string.split("\n")).strip()
    if "Pelagius:" in string:
        string = "Pelagius :".join(string.split("Pelagius:")).strip()
    if "Origenes:" in string:
        string = "Origenes :".join(string.split("Origenes:")).strip()
    if "Hieronymus:" in string:
        string = "Hieronymus :".join(string.split("Hieronymus:")).strip()
    if "Gregorius:" in string:
        string = "Gregorius :".join(string.split("Gregorius:")).strip()
    if "pænitentiam.:" in string:
        string = "pænitentiam. :".join(string.split("pænitentiam.:")).strip()
    if "perditio:" in string:
        string = "perditio :".join(string.split("perditio:")).strip()
    if "peccat:" in string:
        string = "peccat :".join(string.split("peccat:")).strip()
    if "non:" in string:
        string = "non :".join(string.split("non:")).strip()
    test_against = [[i, "<unknown>", "<unknown>", None] for i in string.split(" ")]
    if tokens == test_against:
        return tokens
    else:
        for i, tok_pos in enumerate(tokens):
            token = tok_pos[0]
            if [token, "<unknown>", "<unknown>", None] in test_against:
                match_place = test_against.index([token, "<unknown>", "<unknown>", None])
                removal = test_against[:match_place + 1]
                if len(removal) > 1:
                    return_tokens = return_tokens + removal[:-1]
                test_against = test_against[match_place + 1:]
                return_tokens.append(tok_pos)
        if test_against:
            return_tokens = return_tokens + test_against
        return return_tokens


def overwrite_json(file_path, file_object):
    """Save JSON file, overwrite old file by the same name if necessary"""
    with open(file_path, 'w', newline='', encoding="utf-8") as json_file:
        json.dump(file_object, json_file, indent=4, ensure_ascii=False)


def update_empty_toks(file_path, json_doc):
    """Go through all glosses looking for tokenisation fields that are empty
       replace any empty fields with tokens from the gloss and their POS tags
       update the .json file containing the data"""
    for epistle in json_doc:
        folios = epistle['folios']
        for folio_data in folios:
            glosses = folio_data['glosses']
            for gloss_data in glosses:
                gloss = gloss_data['glossFullTags']
                tok = gloss_data['glossTokens']
                if not tok:
                    token_list = [[i, "<unknown>", "<unknown>", None] if i != ".i."
                                  else [i, "ADV", ".i.", "Abbr=Yes"] for i in clear_tags(gloss).split(" ")]
                    token_list = [[i, "ADV", "⁊rl.", "Abbr=Yes"] if i in ["rl.", "⁊rl."]
                                  else [i, j, k, l] for i, j, k, l in token_list]
                    token_list = [[i, "<Latin CCONJ>", "et", "Foreign=Yes"] if i in ["et"]
                                  else [i, j, k, l] for i, j, k, l in token_list]
                    token_list = [[i, "CCONJ", "ocus", None] if i in ["⁊"]
                                  else [i, j, k, l] for i, j, k, l in token_list]
                    token_list = [[i, "CCONJ", "nó", None] if i in ["ɫ", "ɫ."]
                                  else [i, j, k, l] for i, j, k, l in token_list]
                    gloss_data["glossTokens"] = token_list
    overwrite_json(file_path, json_doc)
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
                toks = gloss['glossTokens']
                gloss_data = [hand, gloss_text, trans, toks]
    return gloss_data


def transfer_wb_toks(add_to_file, add_from_file):
    """add tokens to a lexicon from a manually tokenised .json document if they are not already in it"""

    # Check if a lexicon, potentially with eDIL lexeme IDs, already exists.
    # If so, create a simplified lexicon dictionary to use to find eDIL lexeme ID numbers
    try:
        try_path = os.path.join(os.getcwd(), "Manual_Tokenise_Files")
        if "Working_lexicon.json" in os.listdir(try_path):
            with open(os.path.join(try_path, "Working_lexicon.json"), 'r', encoding="utf-8") as lex_file_json:
                lex_dict = json.load(lex_file_json)
                lex_dict = {
                    pos.get("part_of_speech"): {
                        lem.get("lemma"): lem.get("eDIL_id") for lem in pos.get("lemmata")
                    } for pos in lex_dict
                }
        else:
            lex_dict = None
    except FileNotFoundError:
        lex_dict = None

    # Collect a list of token-data from a .json document from which tokens are to be added to lexica (Wb.)
    # If the token is Irish, add it to a list of Irish tokens
    # Remove duplicates from that list and sort its contents
    add_toks = list()
    for epistle in add_from_file:
        folios = epistle['folios']
        for folio_data in folios:
            glosses = folio_data['glosses']
            for gloss_data in glosses:
                tokens = gloss_data[f"glossTokens"]
                tokens = [(i[1], i[2], i[0].lower(), i[3]) if [i[1], i[2]] not in [
                    ['<unknown>', '<unknown>'],
                    ['<Latin>', ''],
                    ['<Latin CCONJ>', 'et'],
                    ['<Greek>', '']
                ] else () for i in tokens]
                tokens = [i for i in tokens if i]
                if tokens:
                    add_toks = add_toks + tokens
    add_toks = [i if i[3] else (i[0], i[1], i[2], '') for i in add_toks]
    add_toks = sorted(list(set(add_toks)))
    add_toks = [i if i[3] != '' else (i[0], i[1], i[2], None) for i in add_toks]
    add_toks = [[i[0], i[1], i[2], i[3]] for i in add_toks]

    # For each unique Irish token found in the add-from_file (Wb.) if it isn't already in the lexicon file, add it
    json_file = json.loads(add_to_file)
    for tok in add_toks:
        tok_pos = tok[0]
        tok_head = tok[1]
        found_lex_id = None
        # Ensure POS-tag is not a non-standard tag-type used on the Wb. website.
        if tok_pos not in ["<unknown>", "<Latin>", "<Latin CCONJ>", "<Greek>"] and tok_head[-2:] != " *":
            tok_form = tok[2]
            tok_feats = tok[3]
            if tok_feats:
                tok_feats = [{i[0]: i[1] for i in [j.split("=") for j in tok_feats.split("|")]}]
            all_filepos = [level_1.get("part_of_speech") for level_1 in json_file]
            # If the POS-tag is a POS-tag that already occurs in the working lexicon
            if tok_pos in all_filepos:
                file_pos_data = json_file[all_filepos.index(tok_pos)].get("lemmata")
                all_filelemmata = [level_2.get("lemma") for level_2 in file_pos_data]
                # If the lemma is a lemma that already occurs in the working lexicon
                if tok_head in all_filelemmata:
                    file_tok_data = file_pos_data[all_filelemmata.index(tok_head)].get("tokens")
                    all_filetoks = [level_3.get("token") for level_3 in file_tok_data]
                    # If the token is a token that already occurs in the working lexicon
                    if tok_form in all_filetoks:
                        file_featsets_data = file_tok_data[all_filetoks.index(tok_form)].get("feature_sets")
                        all_feats = [level_4.get("features") for level_4 in file_featsets_data]
                        # If the morphological features DO NOT already occur in the working lexicon for this token
                        if tok_feats not in all_feats:
                            # Add the new morphological features if other features already exist for this token
                            if tok_feats:
                                insert = {'feature_set': len(all_feats) + 1, 'features': tok_feats}
                                file_featsets_data = file_featsets_data + [insert]
                            else:
                                # Create a new set of morphological features if necessary
                                insert = {'feature_set': 1, 'features': tok_feats}
                                for i in file_featsets_data:
                                    i['feature_set'] = i.get('feature_set') + 1
                                file_featsets_data = [insert] + file_featsets_data
                            # Cascade the newly added feature set up through the token, lemma and POS levels
                            file_tok_data[all_filetoks.index(tok_form)] = {
                                'token': tok_form, 'feature_sets': file_featsets_data
                            }
                            file_pos_data[all_filelemmata.index(tok_head)] = {
                                'lemma': tok_head, 'eDIL_id': found_lex_id, 'tokens': file_tok_data
                            }
                            json_file[all_filepos.index(tok_pos)] = {
                                'part_of_speech': tok_pos, 'lemmata': file_pos_data
                            }
                    else:
                        # If the token IS NOT a token that already occurs in the working lexicon
                        # Find the correct position to insert it
                        filetoks_plus = sorted(list(set(
                            [level_3.get("token") for level_3 in file_tok_data] + [tok_form]
                        )))
                        correct_position = filetoks_plus.index(tok_form)
                        # Insert it and any morphological feature sets in the correct position
                        insert = {'token': tok_form, 'feature_sets': [{'feature_set': 1, 'features': tok_feats}]}
                        file_tok_data = file_tok_data[:correct_position] + [
                            insert
                        ] + file_tok_data[correct_position:]
                        # Cascade the newly added token up through the lemma and POS levels
                        file_pos_data[all_filelemmata.index(tok_head)] = {
                            'lemma': tok_head, 'eDIL_id': found_lex_id, 'tokens': file_tok_data
                        }
                        json_file[all_filepos.index(tok_pos)] = {
                            'part_of_speech': tok_pos, 'lemmata': file_pos_data
                        }
                else:
                    # If the lemma IS NOT a lemma that already occurs in the working lexicon
                    # Find the correct position to insert it
                    filelemmata_plus = sorted(list(set(
                        [level_2.get("lemma") for level_2 in file_pos_data] + [tok_head]
                    )))
                    correct_position = filelemmata_plus.index(tok_head)
                    # Insert it, as well as any tokens and morphological feature sets in the correct position
                    insert = {'token': tok_form, 'feature_sets': [{'feature_set': 1, 'features': tok_feats}]}
                    insert = {'lemma': tok_head, 'eDIL_id': found_lex_id, 'tokens': [insert]}
                    file_pos_data = file_pos_data[:correct_position] + [
                        insert
                    ] + file_pos_data[correct_position:]
                    # Cascade the newly added lemma up to the POS level
                    json_file[all_filepos.index(tok_pos)] = {
                        'part_of_speech': tok_pos, 'lemmata': file_pos_data
                    }
            else:
                # If the POS-tag IS NOT a POS-tag that already occurs in the working lexicon
                # Find the correct position to insert it at
                filepos_plus = sorted(list(set(
                    [level_1.get("part_of_speech") for level_1 in json_file] + [tok_pos]
                )))
                correct_position = filepos_plus.index(tok_pos)
                # Insert it, as well as any lemmata, tokens and morphological feature sets in the correct position
                insert = {'token': tok_form, 'feature_sets': [{'feature_set': 1, 'features': tok_feats}]}
                insert = {'lemma': tok_head, 'eDIL_id': None, 'tokens': [insert]}
                insert = {'part_of_speech': tok_pos, 'lemmata': [insert]}
                json_file = json_file[:correct_position] + [insert] + json_file[correct_position:]

    if lex_dict:
        for pos_data in json_file:
            curpos = pos_data.get("part_of_speech")
            lemmata = pos_data.get("lemmata")
            annotated_lemmata = lex_dict.get(curpos)
            for lemma_data in lemmata:
                lemma_data["eDIL_id"] = annotated_lemmata.get(lemma_data.get("lemma"))

    return json.dumps(json_file, indent=4, ensure_ascii=False)


def update_base_file(base_file):
    """update any data in the working manual tokenisation file if changes habe been made in the annotated text file
       (currently newNotes and glossHand can be updated, and any newly included glosses can be added)
       """
    updated_text_file = combine_infolists("Wurzburg Glosses", 499, 712)
    updated_text_file = json.loads(make_json(updated_text_file, True))
    # Check if there is any difference at all between the newly generated file and the file currently in use
    # Note: the newly generated file will have no tokenisation, hence, glossTokens1 and glossTokens2 will be empty
    # therefore, if the file currently in use has any tokens already added, there will be a difference here
    if updated_text_file != base_file:
        for i, level_0 in enumerate(updated_text_file):
            upd_folios = level_0.get('folios')
            folios = base_file[i].get('folios')
            # Check if there is any difference between the collected content of each epistle
            if upd_folios != folios:
                for j, level_1 in enumerate(upd_folios):
                    upd_glosses = level_1.get('glosses')
                    glosses = folios[j].get('glosses')
                    # Checks if there is any difference between the collected content of each column on each folio
                    if upd_glosses != glosses:
                        # If the length of the newly generated content is longer than that of the in-use file,
                        # which is unlikely given that it will not have any tokens or POS tag information,
                        # the gloss numbers are collected for each version and compared against each other
                        if len(upd_glosses) > len(glosses):
                            while len(upd_glosses) > len(glosses):
                                upd_glossnums = [upd_gloss_data.get("glossNo") for upd_gloss_data in upd_glosses]
                                glossnums = [gloss_data.get("glossNo") for gloss_data in glosses]
                                # For each gloss number which appears in the newly generated file but not in the file
                                # which is currently in use, it is assumed that a new gloss has been added
                                for k, upd_glossnumber in enumerate(upd_glossnums):
                                    if upd_glossnumber not in glossnums:
                                        # The list of glosses for the current column is split at the point of the
                                        # omission and the missing gloss's data is added in at the point of the split
                                        for upd_gloss_data in upd_glosses:
                                            if upd_gloss_data.get("glossNo") == upd_glossnumber:
                                                glosses = glosses[:k] + [upd_gloss_data] + glosses[k:]
                            folios[j]['glosses'] = glosses
                        for k, level_2 in enumerate(upd_glosses):
                            # Update the glossed Latin text if changes have been made
                            upd_latin = level_2.get('latin')
                            latin = glosses[k].get('latin')
                            if upd_latin != latin:
                                glosses[k]['latin'] = upd_latin
                            # Update the Latin lemma to which the gloss is attached if changes have been made
                            upd_lemma = level_2.get('lemma')
                            lemma = glosses[k].get('lemma')
                            if upd_lemma != lemma:
                                glosses[k]['lemma'] = upd_lemma
                            # Update the position of the Latin lemma if changes have been made
                            upd_lemPos = level_2.get('lemPos')
                            lemPos = glosses[k].get('lemPos')
                            if upd_lemPos != lemPos:
                                glosses[k]['lemPos'] = upd_lemPos
                            # Update the scribal hand if changes have been made
                            upd_glosshand = level_2.get('glossHand')
                            glosshand = glosses[k].get('glossHand')
                            if upd_glosshand != glosshand:
                                glosses[k]['glossHand'] = upd_glosshand
                            # Update the fully tagged gloss text if changes have been made
                            upd_glossFullTags = level_2.get('glossFullTags')
                            glossFullTags = glosses[k].get('glossFullTags')
                            if upd_glossFullTags != glossFullTags:
                                glosses[k]['glossFullTags'] = upd_glossFullTags
                            # Update the gloss text with all tags removed if changes have been made
                            upd_glossText = level_2.get('glossText')
                            glossText = glosses[k].get('glossText')
                            if upd_glossText != glossText:
                                glosses[k]['glossText'] = upd_glossText
                            # Update the new gloss readings if changes have been made
                            upd_newGloss = level_2.get('newGloss')
                            newGloss = glosses[k].get('newGloss')
                            if upd_newGloss != newGloss:
                                glosses[k]['newGloss'] = upd_newGloss
                            # Update the tagged new gloss readings if changes have been made
                            upd_newGlossTagged = level_2.get('taggedNewGloss')
                            taggedNewGloss = glosses[k].get('taggedNewGloss')
                            if upd_newGlossTagged != taggedNewGloss:
                                glosses[k]['taggedNewGloss'] = upd_newGlossTagged
                            # Update the gloss text with superscript footnote tags if changes have been made
                            upd_glossFNs = level_2.get('glossFNs')
                            glossFNs = glosses[k].get('glossFNs')
                            if upd_glossFNs != glossFNs:
                                glosses[k]['glossFNs'] = upd_glossFNs
                            # Update the English translation of the gloss if changes have been made
                            upd_glossTrans = level_2.get('glossTrans')
                            glossTrans = glosses[k].get('glossTrans')
                            if upd_glossTrans != glossTrans:
                                glosses[k]['glossTrans'] = upd_glossTrans
                            # Update the footnotes if changes have been made
                            upd_footnotes = level_2.get('footnotes')
                            footnotes = glosses[k].get('footnotes')
                            if upd_footnotes != footnotes:
                                glosses[k]['footnotes'] = upd_footnotes
                            # Update the site notes (new notes) if changes have been made
                            upd_newnote = level_2.get('newNotes')
                            newnote = glosses[k].get('newNotes')
                            if upd_newnote != newnote:
                                glosses[k]['newNotes'] = upd_newnote
                            # Update the new translations if changes have been made
                            upd_newtrans = level_2.get('newTrans')
                            newtrans = glosses[k].get('newTrans')
                            if upd_newtrans != newtrans:
                                glosses[k]['newTrans'] = upd_newtrans
                            # Update the new tokens if changes have been made
                            upd_toks = glosses[k].get('glossTokens')
                            upd_toks = [tagged_tok + [None] if len(tagged_tok) == 3
                                          else tagged_tok for tagged_tok in upd_toks]
                            upd_toks = [[".i.", "ADV", ".i.", "Abbr=Yes"]
                                          if [i, j, k, l] == [".i.", "ADV", ".i.", None]
                                          else [i, j, k, l] for i, j, k, l in upd_toks]
                            upd_toks = [[i, "ADV", "⁊rl.", "Abbr=Yes"]
                                          if [j, k, l] == ["ADV", "⁊rl.", None]
                                          else [i, j, k, l] for i, j, k, l in upd_toks]
                            upd_toks = [["et", "<Latin CCONJ>", "et", "Foreign=Yes"]
                                          if [i, j, k, l] == ["et", "<Latin CCONJ>", "et", None]
                                          else [i, j, k, l] for i, j, k, l in upd_toks]
                            glosses[k]['glossTokens'] = upd_toks

    overwrite_json(os.path.join(os.getcwd(), "Manual_Tokenise_Files", "Wb. Manual Tokenisation.json"), base_file)
    return base_file


if __name__ == "__main__":

    # Navigate to a directory containing a JSON file of the Wb. Glosses
    # If either the directory or the JSON file do not exist, create them

    maindir = os.getcwd()
    tokenise_dir = os.path.join(maindir, "Manual_Tokenise_Files")

    # Open the Manual Tokenisation folder
    try:
        os.listdir(tokenise_dir)
    except FileNotFoundError:
        os.mkdir("Manual_Tokenise_Files")

    # Create a JSON document of the Wb. Glosses in the Manual Tokenisation folder if it doesn't exist already
    dir_contents = os.listdir(tokenise_dir)
    if "Wb. Manual Tokenisation.json" not in dir_contents:
        wbglosslist = combine_infolists("Wurzburg Glosses", 499, 712)
        save_json(make_json(wbglosslist, True), "Wb. Manual Tokenisation", tokenise_dir)

    # Open the Wb. JSON file for use in the GUI
    man_tok_filepath = os.path.join(tokenise_dir, "Wb. Manual Tokenisation.json")
    with open(man_tok_filepath, 'r', encoding="utf-8") as wb_json:
        wb_data = json.load(wb_json)
        wb_data = update_base_file(wb_data)

    # Check if any of the tokenisation fields are empty
    empty_tokfields = False
    for epistle in wb_data:
        folios = epistle['folios']
        for folio_data in folios:
            glosses = folio_data['glosses']
            for gloss_data in glosses:
                tok = gloss_data['glossTokens']
                if not tok:
                    empty_tokfields = True
                    break
            if empty_tokfields:
                break
        if empty_tokfields:
            break
    # If any of the tokenisation fields, for any gloss, are empty (eg. if the JSON file has just been generated)
    # add lists of tokens and their POS tags, for each gloss, to the gloss's tokenisation fields
    if empty_tokfields:
        update_empty_toks(man_tok_filepath, wb_data)

    # Create a JSON document of the OI Lexicon in the Manual Tokenisation folder from the Sg. CoNNL_U file
    # if it doesn't exist already, otherwise, update it if necessary
    if "Lexicon.json" not in dir_contents:
        sg_conllu_file = "combined_sg_files.conllu"
        sg_filepath = os.path.join(maindir, "conllu_files", "Sg_Treebanks")
        sg_json = make_lex_json(os.path.join(sg_filepath, sg_conllu_file))
        save_json(sg_json, "Lexicon", tokenise_dir)
        # Open the first Lexicon JSON file for use in the GUI
        with open(os.path.join(tokenise_dir, "Lexicon.json"), 'r', encoding="utf-8") as lex_json:
            original_lexicon = json.load(lex_json)
    else:
        # Ensure that no changes have been made to the Sg. file that require the current lexicon to be amended
        # if any such changes have been made, replace the current lexicon
        with open(os.path.join(tokenise_dir, "Lexicon.json"), 'r', encoding="utf-8") as lex_json:
            original_lexicon = json.load(lex_json)
        sg_conllu_file = "combined_sg_files.conllu"
        sg_filepath = os.path.join(maindir, "conllu_files", "Sg_Treebanks")
        sg_json = make_lex_json(os.path.join(sg_filepath, sg_conllu_file))
        if original_lexicon != json.loads(sg_json):
            os.remove(os.path.join(tokenise_dir, "Lexicon.json"))
            save_json(sg_json, "Lexicon", tokenise_dir)
        # Open the first Lexicon JSON file for use in the GUI
        with open(os.path.join(tokenise_dir, "Lexicon.json"), 'r', encoding="utf-8") as lex_json:
            original_lexicon = json.load(lex_json)

    # Create a working copy of the OI Lexicon created above for use in the GUI if it doesn't already exist
    # This will be updated with new tokens and POS from Wb. which will not be saved to the original above
    if "Working_lexicon.json" not in dir_contents:
        sg_conllu_file = "combined_sg_files.conllu"
        sg_filepath = os.path.join(maindir, "conllu_files", "Sg_Treebanks")
        sg_json = make_lex_json(os.path.join(sg_filepath, sg_conllu_file))
        save_json(sg_json, "Working_lexicon", tokenise_dir)
        # Open the second Lexicon JSON file for use in the GUI
        with open(os.path.join(tokenise_dir, "Working_lexicon.json"), 'r', encoding="utf-8") as lex_working_json:
            working_lexicon = json.load(lex_working_json)
    # Check for any tokens, lemmata or parts-of-speech which don't occur in either the Sg. file of the Wb. file
    # if any exist, delete them.
    else:
        with open(os.path.join(tokenise_dir, "Working_lexicon.json"), 'r', encoding="utf-8") as lex_working_json:
            working_lexicon = json.load(lex_working_json)
        sg_conllu_file = "combined_sg_files.conllu"
        sg_filepath = os.path.join(maindir, "conllu_files", "Sg_Treebanks")
        sg_json = make_lex_json(os.path.join(sg_filepath, sg_conllu_file))
        sg_json = transfer_wb_toks(sg_json, wb_data)
        if working_lexicon != json.loads(sg_json):
            os.remove(os.path.join(tokenise_dir, "Working_lexicon.json"))
            save_json(sg_json, "Working_lexicon", tokenise_dir)
        # Open the second Lexicon JSON file for use in the GUI
        with open(os.path.join(tokenise_dir, "Working_lexicon.json"), 'r', encoding="utf-8") as lex_working_json:
            working_lexicon = json.load(lex_working_json)


    # Start the UI
    ui = UI(
        file_name="Wb. Manual Tokenisation.json",
        wb_data=wb_data,
        lexicon=working_lexicon,
        primary_lexicon=original_lexicon
    )
    ui.start()
