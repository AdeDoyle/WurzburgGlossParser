
from CombineInfoLists import combine_infolists
from MakeJSON import make_json, make_lex_json
from SaveJSON import save_json
import os
import json
from decimal import Decimal
from ClearTags import clear_tags
from tkinter import *
from tkinter import ttk
from tkinter import font
from nltk import edit_distance
import unidecode


class UI:

    def __init__(self, file_name, wb_data, lexica):

        self.file_name = file_name
        self.wb_data = wb_data
        self.epistles = show_epistles(wb_data)
        self.lexicon_1 = lexica[0]
        self.lexicon_2 = lexica[1]
        self.pos_tags = ["ADJ", "ADP", "ADV", "AUX", "CCONJ", "DET", "INTJ", "NOUN", "NUM",
                         "PART", "PRON", "PROPN", "PUNCT", "SCONJ", "SYM", "VERB", "X",
                         "<Latin>", "<Latin CCONJ>", "<unknown>"]
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
        self.open_toks1 = self.open_glossdata[3]
        self.open_toks2 = self.open_glossdata[4]

        # Create the GUI
        self.root = Tk()
        self.root.title("Manual Tokenisation Window")
        self.root.geometry("1200x800")

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
            cur_toks1=self.open_toks1,
            cur_toks2=self.open_toks2
        )

    def start(self):
        self.root.mainloop()

    def create_gloss_info(self, selected_epistle, selected_folio, selected_glossnum):
        selected_glossdata = select_glossnum(select_folcol(select_epistle(selected_epistle),
                                                           selected_folio), selected_glossnum)
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
            "selected_toks1": selected_glossdata[3],
            "selected_toks2": selected_glossdata[4]
        }

    def change_gloss(self, event=None):

        new_selected_glossnum = self.current_rendered_window["current_selected_gloss"].get()
        self.selected_gloss_info = self.create_gloss_info(
            selected_epistle=self.current_rendered_window["current_selected_epistle"].get(),
            selected_folio=self.current_rendered_window["current_selected_folio"].get(),
            selected_glossnum=new_selected_glossnum
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
            cur_toks1=self.selected_gloss_info["selected_toks1"],
            cur_toks2=self.selected_gloss_info["selected_toks2"]
        )

    def change_folio(self, event=None):

        new_selected_folio = self.current_rendered_window["current_selected_folio"].get()
        cur_ep = self.current_rendered_window["current_selected_epistle"].get()
        cur_glossnums = show_glossnums(select_folcol(select_epistle(cur_ep), new_selected_folio))
        new_selected_glossnum = cur_glossnums[0]
        self.selected_gloss_info = self.create_gloss_info(
            selected_epistle=self.current_rendered_window["current_selected_epistle"].get(),
            selected_folio=new_selected_folio,
            selected_glossnum=new_selected_glossnum
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
            cur_toks1=self.selected_gloss_info["selected_toks1"],
            cur_toks2=self.selected_gloss_info["selected_toks2"]
        )

    def change_epistle(self, event=None):

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
            cur_toks1=self.selected_gloss_info["selected_toks1"],
            cur_toks2=self.selected_gloss_info["selected_toks2"]
        )

    def render_gloss(self, root, epistles, cur_ep, cur_fols, cur_folio, cur_glossnums, cur_glossnum, cur_glossid,
                     cur_hand, cur_gloss, cur_trans, cur_toks1, cur_toks2):

        # Create frames for all following widgets
        if hasattr(self, "current_rendered_window"):

            self.current_rendered_window["main_frame"].destroy()
            self.current_rendered_window["main_canvas"].destroy()
            self.current_rendered_window["main_scrollbar"].destroy()
            self.current_rendered_window["secondary_frame"].destroy()

            self.current_rendered_window["nav_frame"].destroy()
            self.current_rendered_window["options_frame"].destroy()
            self.current_rendered_window["nav_buttons_frame"].destroy()
            self.current_rendered_window["text_frame"].destroy()
            self.current_rendered_window["toks_frames"].destroy()
            self.current_rendered_window["toks1_frame"].destroy()
            self.current_rendered_window["head_opts_1_frame"].destroy()
            self.current_rendered_window["toks2_frame"].destroy()
            self.current_rendered_window["head_opts_2_frame"].destroy()
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

            self.current_rendered_window["tokenise_label_1"].destroy()
            self.current_rendered_window["tokenise_text_1"].destroy()
            self.current_rendered_window["tokenise_label_2"].destroy()
            self.current_rendered_window["tokenise_text_2"].destroy()

            self.current_rendered_window["toks1_label"].destroy()
            self.current_rendered_window["pos1_label"].destroy()
            self.current_rendered_window["toks2_label"].destroy()
            self.current_rendered_window["pos2_label"].destroy()

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
        self.current_rendered_window["main_canvas"].pack(side=LEFT, fill=BOTH, expand=1)

        self.current_rendered_window["main_scrollbar"] = ttk.Scrollbar(
            self.current_rendered_window["main_frame"],
            orient=VERTICAL, command=self.current_rendered_window["main_canvas"].yview
        )
        self.current_rendered_window["main_scrollbar"].pack(side=RIGHT, fill=Y)

        self.current_rendered_window["main_canvas"].configure(
            yscrollcommand=self.current_rendered_window["main_scrollbar"].set
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

        # Create display frames for the window
        self.current_rendered_window["nav_frame"] = Frame(self.current_rendered_window["secondary_frame"],
                                                          padx=5, pady=5)
        self.current_rendered_window["nav_frame"].grid(row=0, column=0, padx=10, pady=10, sticky="W")

        self.current_rendered_window["options_frame"] = Frame(self.current_rendered_window["nav_frame"],
                                                              padx=5, pady=5)
        self.current_rendered_window["options_frame"].grid(row=0, column=0, padx=5, pady=5, sticky="W")

        self.current_rendered_window["nav_buttons_frame"] = Frame(self.current_rendered_window["nav_frame"],
                                                                  padx=5, pady=5)
        self.current_rendered_window["nav_buttons_frame"].grid(row=0, column=1, padx=5, pady=5, sticky="W")

        self.current_rendered_window["text_frame"] = Frame(self.current_rendered_window["secondary_frame"],
                                                           padx=5, pady=5)
        self.current_rendered_window["text_frame"].grid(row=1, column=0, padx=10, pady=10, sticky="W")

        self.current_rendered_window["toks_frames"] = Frame(self.current_rendered_window["secondary_frame"],
                                                            padx=5, pady=5)
        self.current_rendered_window["toks_frames"].grid(row=2, column=0, padx=10, pady=10, sticky="W")

        self.current_rendered_window["toks1_frame"] = LabelFrame(self.current_rendered_window["toks_frames"],
                                                                 padx=5, pady=5)
        self.current_rendered_window["toks1_frame"].grid(row=0, column=0, padx=5, pady=5, sticky="NW")

        self.current_rendered_window["head_opts_1_frame"] = LabelFrame(self.current_rendered_window["toks_frames"],
                                                                       padx=5, pady=5)
        self.current_rendered_window["head_opts_1_frame"].grid(row=0, column=1, padx=5, pady=5, sticky="NW")

        self.current_rendered_window["toks2_frame"] = LabelFrame(self.current_rendered_window["toks_frames"],
                                                                 padx=5, pady=5)
        self.current_rendered_window["toks2_frame"].grid(row=0, column=2, padx=5, pady=5, sticky="NW")

        self.current_rendered_window["head_opts_2_frame"] = LabelFrame(self.current_rendered_window["toks_frames"],
                                                                       padx=5, pady=5)
        self.current_rendered_window["head_opts_2_frame"].grid(row=0, column=3, padx=5, pady=5, sticky="NW")

        self.current_rendered_window["buttons_frame"] = Frame(self.current_rendered_window["toks_frames"],
                                                              padx=5, pady=5)
        self.current_rendered_window["buttons_frame"].grid(row=0, column=4, padx=5, pady=5, sticky="NW")

        # Create top-bar dropdown menus
        self.current_rendered_window["ep_drop"] = OptionMenu(self.current_rendered_window["options_frame"],
                                                             self.current_rendered_window["current_selected_epistle"],
                                                             *epistles, command=self.change_epistle)
        self.current_rendered_window["ep_drop"].grid(row=0, column=0)

        self.current_rendered_window["fol_drop"] = OptionMenu(self.current_rendered_window["options_frame"],
                                                              self.current_rendered_window["current_selected_folio"],
                                                              *cur_fols, command=self.change_folio)
        self.current_rendered_window["fol_drop"].grid(row=0, column=1)

        self.current_rendered_window["gloss_drop"] = OptionMenu(self.current_rendered_window["options_frame"],
                                                                self.current_rendered_window["current_selected_gloss"],
                                                                *cur_glossnums, command=self.change_gloss)
        self.current_rendered_window["gloss_drop"].grid(row=0, column=2)

        # Create GUI buttons
        self.current_rendered_window["back_button"] = Button(self.current_rendered_window["nav_buttons_frame"],
                                                             text="Back", command=self.last_gloss)
        self.current_rendered_window["back_button"].grid(row=0, column=0, padx=5, pady=5)

        self.current_rendered_window["next_button"] = Button(self.current_rendered_window["nav_buttons_frame"],
                                                             text="Next", command=self.next_gloss)
        self.current_rendered_window["next_button"].grid(row=0, column=1, padx=5, pady=5)

        self.current_rendered_window["update_button"] = Button(self.current_rendered_window["buttons_frame"],
                                                               text="Update Tokens", command=self.update_tokens)
        self.current_rendered_window["update_button"].grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.current_rendered_window["save_button"] = Button(self.current_rendered_window["buttons_frame"],
                                                             text="Save", command=self.save_tokens)
        self.current_rendered_window["save_button"].grid(row=1, column=0, padx=5, pady=5, sticky="w")

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
        self.current_rendered_window["gloss_text"].pack(pady=5, anchor='w')
        self.current_rendered_window["trans_label"].pack(anchor='w')
        self.current_rendered_window["trans_text"].pack(pady=5, anchor='w')

        # Create GUI text labels and editing boxes
        self.current_rendered_window["tokenise_label_1"] = Label(self.current_rendered_window["text_frame"],
                                                                 height=2, text=f"Tokenise (1st Standard)",
                                                                 font=("Helvetica", 16))
        self.current_rendered_window["tokenise_text_1"] = Text(self.current_rendered_window["text_frame"],
                                                               width=self.max_linelen, height=5, borderwidth=1,
                                                               relief="solid", font=("Courier", 12))
        self.current_rendered_window["tokenise_text_1"].insert(1.0,
                                                               self.set_spacing(" ".join([i[0] for i in cur_toks1])))

        self.current_rendered_window["tokenise_label_2"] = Label(self.current_rendered_window["text_frame"],
                                                                 height=1, text="Tokenise (2nd Standard)",
                                                                 font=("Helvetica", 16))
        self.current_rendered_window["tokenise_text_2"] = Text(self.current_rendered_window["text_frame"],
                                                               width=self.max_linelen, height=5, borderwidth=1,
                                                               relief="solid", font=("Courier", 12))
        self.current_rendered_window["tokenise_text_2"].insert(1.0,
                                                               self.set_spacing(" ".join([i[0] for i in cur_toks2])))

        self.current_rendered_window["tokenise_label_1"].pack(anchor='w')
        self.current_rendered_window["tokenise_text_1"].pack(pady=5, anchor='w')
        self.current_rendered_window["tokenise_label_2"].pack(anchor='w')
        self.current_rendered_window["tokenise_text_2"].pack(pady=5, anchor='w')

        # Create lables for the tokens, POS tags and headwords (style 1)
        self.current_rendered_window["toks1_label"] = Label(self.current_rendered_window["toks1_frame"],
                                                            text="Tokens (1)", font=("Helvetica", 16))
        self.current_rendered_window["toks1_label"].grid(row=0, column=0, padx=5, pady=5)

        self.current_rendered_window["pos1_label"] = Label(self.current_rendered_window["toks1_frame"],
                                                           text="POS", font=("Helvetica", 16))
        self.current_rendered_window["pos1_label"].grid(row=0, column=1, padx=5, pady=5)

        self.current_rendered_window["head1_label"] = Label(self.current_rendered_window["toks1_frame"],
                                                            text="Headword", font=("Helvetica", 16))
        self.current_rendered_window["head1_label"].grid(row=0, column=2, padx=5, pady=5)

        # Create tokens, POS menus and headword entry boxes for the tokens and POS tags (style 1)
        self.cur_toks1 = cur_toks1
        for i, pos_token in enumerate(cur_toks1):
            lexicon1 = self.lexicon_1
            token = pos_token[0]
            tag = pos_token[1]
            head = pos_token[2]
            finds = " ".join(gloss_emphs)
            finds_list = " ".join(finds.split("\n")).split(" ")
            if token in finds_list and tag == "<unknown>":
                tag = "<Latin>"
                if head == "<unknown>":
                    head = "Latin ?"
            if tag not in ["<Latin>", "<unknown>"] and (head == "<unknown>" or head[-2:] == " ?"):
                lex_toks = list()
                for level_1 in lexicon1:
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
                    head = f"{head_candidate[1]} ?"
            self.current_rendered_window[f"toks1_tok_{i}"] = Label(self.current_rendered_window["toks1_frame"],
                                                                   text=token, font=("Helvetica", 12))
            self.current_rendered_window[f"toks1_tok_{i}"].grid(row=i + 1, column=0, padx=5, pady=5, sticky='e')

            self.current_rendered_window[f"type1_pos{i}"] = StringVar()
            self.current_rendered_window[f"type1_pos{i}"].set(tag)
            self.current_rendered_window[f"pos_drop1.{i}"] = OptionMenu(self.current_rendered_window["toks1_frame"],
                                                                        self.current_rendered_window[f"type1_pos{i}"],
                                                                        *self.pos_tags)
            self.current_rendered_window[f"pos_drop1.{i}"].grid(row=i + 1, column=1, sticky='w')

            self.current_rendered_window[f"head_word1.{i}"] = Text(self.current_rendered_window["toks1_frame"],
                                                                   height=1, width=12, font=("Helvetica", 12))
            self.current_rendered_window[f"head_word1.{i}"].insert(1.0, head)
            self.current_rendered_window[f"head_word1.{i}"].grid(row=i + 1, column=2, sticky='w')

            self.current_rendered_window[f"suggest_head1.{i}"] = Button(self.current_rendered_window["toks1_frame"],
                                                                        text=" ? ",
                                                                        command=lambda but=i: self.suggest_head_1(but))
            self.current_rendered_window[f"suggest_head1.{i}"].grid(row=i + 1, column=3, padx=5, pady=5)

        # Create lables for the tokens, POS tags and headwords (style 2)
        self.current_rendered_window["toks2_label"] = Label(self.current_rendered_window["toks2_frame"],
                                                            text="Tokens (2)", font=("Helvetica", 16))
        self.current_rendered_window["toks2_label"].grid(row=0, column=0, padx=5, pady=5)

        self.current_rendered_window["pos2_label"] = Label(self.current_rendered_window["toks2_frame"],
                                                           text="POS", font=("Helvetica", 16))
        self.current_rendered_window["pos2_label"].grid(row=0, column=1, padx=5, pady=5)

        self.current_rendered_window["head2_label"] = Label(self.current_rendered_window["toks2_frame"],
                                                            text="Headword", font=("Helvetica", 16))
        self.current_rendered_window["head2_label"].grid(row=0, column=2, padx=5, pady=5)

        # Create tokens, POS menus and headword entry boxes for the tokens and POS tags (style 2)
        self.cur_toks2 = cur_toks2
        for i, pos_token in enumerate(cur_toks2):
            lexicon2 = self.lexicon_2
            token = pos_token[0]
            tag = pos_token[1]
            head = pos_token[2]
            finds = " ".join(gloss_emphs)
            finds_list = " ".join(finds.split("\n")).split(" ")
            if token in finds_list and tag == "<unknown>":
                tag = "<Latin>"
                if head == "<unknown>":
                    head = "Latin ?"
            if tag not in ["<Latin>", "<unknown>"] and (head == "<unknown>" or head[-2:] == " ?"):
                lex_toks = list()
                for level_1 in lexicon2:
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
                    head = f"{head_candidate[1]} ?"
            self.current_rendered_window[f"toks2_tok_{i}"] = Label(self.current_rendered_window["toks2_frame"],
                                                                   text=token, font=("Helvetica", 12))
            self.current_rendered_window[f"toks2_tok_{i}"].grid(row=i + 1, column=0, padx=5, pady=5, sticky='e')

            self.current_rendered_window[f"type2_pos{i}"] = StringVar()
            self.current_rendered_window[f"type2_pos{i}"].set(tag)
            self.current_rendered_window[f"pos_drop2.{i}"] = OptionMenu(self.current_rendered_window["toks2_frame"],
                                                                        self.current_rendered_window[f"type2_pos{i}"],
                                                                        *self.pos_tags)
            self.current_rendered_window[f"pos_drop2.{i}"].grid(row=i + 1, column=1, sticky='w')

            self.current_rendered_window[f"head_word2.{i}"] = Text(self.current_rendered_window["toks2_frame"],
                                                                   height=1, width=12, font=("Helvetica", 12))
            self.current_rendered_window[f"head_word2.{i}"].insert(1.0, head)
            self.current_rendered_window[f"head_word2.{i}"].grid(row=i + 1, column=2, sticky='w')

            self.current_rendered_window[f"suggest_head2.{i}"] = Button(self.current_rendered_window["toks2_frame"],
                                                                        text=" ? ",
                                                                        command=lambda but=i: self.suggest_head_2(but))
            self.current_rendered_window[f"suggest_head2.{i}"].grid(row=i + 1, column=3, padx=5, pady=5)

    def remove_head_options1(self):
        self.current_rendered_window["head_opts_1_frame"].destroy()
        self.current_rendered_window["head_opts_1_frame"] = LabelFrame(self.current_rendered_window["toks_frames"],
                                                                       padx=5, pady=5)
        self.current_rendered_window["head_opts_1_frame"].grid(row=0, column=1, padx=5, pady=5, sticky="NW")

    def remove_head_options2(self):
        self.current_rendered_window["head_opts_2_frame"].destroy()
        self.current_rendered_window["head_opts_2_frame"] = LabelFrame(self.current_rendered_window["toks_frames"],
                                                                       padx=5, pady=5)
        self.current_rendered_window["head_opts_2_frame"].grid(row=0, column=3, padx=5, pady=5, sticky="NW")

    def select_head_1(self, head, button_num):
        self.current_rendered_window[f"head_word1.{button_num}"].delete(1.0, END)
        self.current_rendered_window[f"head_word1.{button_num}"].insert(1.0, head)
        self.remove_head_options1()

    def select_head_2(self, head, button_num):
        self.current_rendered_window[f"head_word2.{button_num}"].delete(1.0, END)
        self.current_rendered_window[f"head_word2.{button_num}"].insert(1.0, head)
        self.remove_head_options2()

    def suggest_head_1(self, button_num):
        self.remove_head_options1()

        all_tokens = self.cur_toks1
        updated_tokens = [self.current_rendered_window[f"toks1_tok_{i}"].cget("text") for i in range(len(all_tokens))]
        token = updated_tokens[button_num]
        updated_pos = [self.current_rendered_window[f"type1_pos{i}"].get() for i in range(len(all_tokens))]
        tag = updated_pos[button_num]

        lex_toks = list()
        for level_1 in self.lexicon_1:
            lex_pos = level_1.get("part_of_speech")
            if lex_pos == tag:
                lex_lemmata = level_1.get("lemmata")
                for level_2 in lex_lemmata:
                    lex_lemma = level_2.get("lemma")
                    lex_tokens = level_2.get("tokens")
                    lex_toks = lex_toks + [[lex_token.get("token"), lex_lemma] for lex_token in lex_tokens]
        if lex_toks:
            ed_dists = [edit_distance(token, i[0]) for i in lex_toks]
            lex_toks = [i + [j] for i, j in zip(lex_toks, ed_dists)]
            lex_toks.sort(key=lambda x: x[2])
            if len(lex_toks) > 50:
                lex_toks = lex_toks[:50]

            for i, option in enumerate(lex_toks):
                features = list()
                for level_1 in self.lexicon_1:
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
                                            for level_5 in lex_feature_set:
                                                features.append(";  ".join([f"{feat}={level_5.get(feat)}"
                                                                           for feat in level_5]))
                if len(features) > 1:
                    for j, feature in enumerate(features):
                        features[j] = f"{j + 1}. {feature}"
                features = "\n".join(features)

                self.current_rendered_window[f"tok_button{i}"] = Button(
                    self.current_rendered_window["head_opts_1_frame"],
                    text=option[0], width=15,
                    command=lambda head=option[1]: self.select_head_1(head, button_num)
                )
                self.current_rendered_window[f"tok_button{i}"].grid(row=2 + i, column=0, padx=5, pady=5, sticky="e")

                self.current_rendered_window[f"head{i}"] = Label(self.current_rendered_window["head_opts_1_frame"],
                                                                 text=option[1], font=("Helvetica", 10))
                self.current_rendered_window[f"head{i}"].grid(row=2 + i, column=1, padx=5, pady=5)

                self.current_rendered_window[f"ed_dist{i}"] = Label(self.current_rendered_window["head_opts_1_frame"],
                                                                    text=option[2], font=("Helvetica", 10))
                self.current_rendered_window[f"ed_dist{i}"].grid(row=2 + i, column=2, padx=5, pady=5)

                self.current_rendered_window[f"feat_str{i}"] = Label(self.current_rendered_window["head_opts_1_frame"],
                                                                     text=features,
                                                                     font=("Helvetica", 10), justify=LEFT)
                self.current_rendered_window[f"feat_str{i}"].grid(row=2 + i, column=3, padx=5, pady=5, sticky="w")

        self.current_rendered_window["killme1"] = Button(self.current_rendered_window["head_opts_1_frame"],
                                                         text=" X ", command=self.remove_head_options1)
        self.current_rendered_window["killme1"].grid(row=0, column=4, padx=5, pady=5, sticky="NE")

        self.current_rendered_window["tok_label"] = Label(self.current_rendered_window["head_opts_1_frame"],
                                                          text="Token", font=("Helvetica", 12))
        self.current_rendered_window["tok_label"].grid(row=1, column=0, padx=5, pady=5)

        self.current_rendered_window["head_label"] = Label(self.current_rendered_window["head_opts_1_frame"],
                                                           text="Headword", font=("Helvetica", 12))
        self.current_rendered_window["head_label"].grid(row=1, column=1, padx=5, pady=5)

        self.current_rendered_window["ed_label"] = Label(self.current_rendered_window["head_opts_1_frame"],
                                                         text="Edit Dist.", font=("Helvetica", 12))
        self.current_rendered_window["ed_label"].grid(row=1, column=2, padx=5, pady=5)

        self.current_rendered_window["featsets_label"] = Label(self.current_rendered_window["head_opts_1_frame"],
                                                               text="Features", font=("Helvetica", 12))
        self.current_rendered_window["featsets_label"].grid(row=1, column=3, padx=5, pady=5)

    def suggest_head_2(self, button_num):
        self.remove_head_options2()

        all_tokens = self.cur_toks2
        updated_tokens = [self.current_rendered_window[f"toks2_tok_{i}"].cget("text") for i in range(len(all_tokens))]
        token = updated_tokens[button_num]
        updated_pos = [self.current_rendered_window[f"type2_pos{i}"].get() for i in range(len(all_tokens))]
        tag = updated_pos[button_num]

        lex_toks = list()
        for level_1 in self.lexicon_2:
            lex_pos = level_1.get("part_of_speech")
            if lex_pos == tag:
                lex_lemmata = level_1.get("lemmata")
                for level_2 in lex_lemmata:
                    lex_lemma = level_2.get("lemma")
                    lex_tokens = level_2.get("tokens")
                    lex_toks = lex_toks + [[lex_token.get("token"), lex_lemma] for lex_token in lex_tokens]
        if lex_toks:
            ed_dists = [edit_distance(token, i[0]) for i in lex_toks]
            lex_toks = [i + [j] for i, j in zip(lex_toks, ed_dists)]
            lex_toks.sort(key=lambda x: x[2])
            if len(lex_toks) > 50:
                lex_toks = lex_toks[:50]

            for i, option in enumerate(lex_toks):
                features = list()
                for level_1 in self.lexicon_2:
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
                                            for level_5 in lex_feature_set:
                                                features.append(";  ".join([f"{feat}={level_5.get(feat)}"
                                                                           for feat in level_5]))
                if len(features) > 1:
                    for j, feature in enumerate(features):
                        features[j] = f"{j + 1}. {feature}"
                features = "\n".join(features)

                self.current_rendered_window[f"tok_button{i}"] = Button(
                    self.current_rendered_window["head_opts_2_frame"],
                    text=option[0], width=15,
                    command=lambda head=option[1]: self.select_head_2(head, button_num)
                )
                self.current_rendered_window[f"tok_button{i}"].grid(row=2 + i, column=0, padx=5, pady=5, sticky="e")

                self.current_rendered_window[f"head{i}"] = Label(self.current_rendered_window["head_opts_2_frame"],
                                                                 text=option[1], font=("Helvetica", 10))
                self.current_rendered_window[f"head{i}"].grid(row=2 + i, column=1, padx=5, pady=5)

                self.current_rendered_window[f"ed_dist{i}"] = Label(self.current_rendered_window["head_opts_2_frame"],
                                                                    text=option[2], font=("Helvetica", 10))
                self.current_rendered_window[f"ed_dist{i}"].grid(row=2 + i, column=2, padx=5, pady=5)

                self.current_rendered_window[f"feat_str{i}"] = Label(self.current_rendered_window["head_opts_2_frame"],
                                                                     text=features,
                                                                     font=("Helvetica", 10), justify=LEFT)
                self.current_rendered_window[f"feat_str{i}"].grid(row=2 + i, column=3, padx=5, pady=5, sticky="w")

        self.current_rendered_window["killme2"] = Button(self.current_rendered_window["head_opts_2_frame"],
                                                         text=" X ", command=self.remove_head_options2)
        self.current_rendered_window["killme2"].grid(row=0, column=4, padx=5, pady=5, sticky="NE")

        self.current_rendered_window["tok_label"] = Label(self.current_rendered_window["head_opts_2_frame"],
                                                          text="Similar Token", font=("Helvetica", 12))
        self.current_rendered_window["tok_label"].grid(row=1, column=0, padx=5, pady=5)

        self.current_rendered_window["head_label"] = Label(self.current_rendered_window["head_opts_2_frame"],
                                                           text="Headword", font=("Helvetica", 12))
        self.current_rendered_window["head_label"].grid(row=1, column=1, padx=5, pady=5)

        self.current_rendered_window["ed_label"] = Label(self.current_rendered_window["head_opts_2_frame"],
                                                         text="Edit Dist.", font=("Helvetica", 12))
        self.current_rendered_window["ed_label"].grid(row=1, column=2, padx=5, pady=5)

        self.current_rendered_window["featsets_label"] = Label(self.current_rendered_window["head_opts_2_frame"],
                                                               text="Features", font=("Helvetica", 12))
        self.current_rendered_window["featsets_label"].grid(row=1, column=3, padx=5, pady=5)

    def update_tokens(self):
        string_1 = self.current_rendered_window["tokenise_text_1"].get(1.0, END)
        tokens_1 = self.cur_toks1
        updated_pos1 = [self.current_rendered_window[f"type1_pos{i}"].get() for i in range(len(tokens_1))]
        updated_head1 = [self.current_rendered_window[f"head_word1.{i}"].get(1.0, END) for i in range(len(tokens_1))]
        if len(tokens_1) != len(updated_pos1):
            raise RuntimeError("Different counts found for tokens before and after POS-tagging")
        if [i[1] for i in tokens_1] != updated_pos1:
            tokens_1 = [[i[0], j, i[2]] for i, j in zip(tokens_1, updated_pos1)]
        if [i[2] for i in tokens_1] != updated_head1:
            tokens_1 = [[i[0], i[1], j.strip()] for i, j in zip(tokens_1, updated_head1)]

        string_2 = self.current_rendered_window["tokenise_text_2"].get(1.0, END)
        tokens_2 = self.cur_toks2
        updated_pos2 = [self.current_rendered_window[f"type2_pos{i}"].get() for i in range(len(tokens_2))]
        updated_head2 = [self.current_rendered_window[f"head_word2.{i}"].get(1.0, END) for i in range(len(tokens_2))]
        if len(tokens_2) != len(updated_pos2):
            raise RuntimeError("Different counts found for tokens before and after POS-tagging")
        if [i[1] for i in tokens_2] != updated_pos2:
            tokens_2 = [[i[0], j, i[2]] for i, j in zip(tokens_2, updated_pos2)]
        if [i[2] for i in tokens_2] != updated_head2:
            tokens_2 = [[i[0], i[1], j.strip()] for i, j in zip(tokens_2, updated_head2)]

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
            cur_toks1=refresh_tokens(string_1, tokens_1),
            cur_toks2=refresh_tokens(string_2, tokens_2)
        )

    def save_tokens(self):
        self.update_tokens()

        file_name = self.file_name
        main_file = self.wb_data
        current_glossnum = self.current_rendered_window["current_selected_gloss"].get()
        current_folio = self.current_rendered_window["current_selected_folio"].get()
        current_epistle = self.current_rendered_window["current_selected_epistle"].get()
        tokens_1 = self.cur_toks1
        tokens_2 = self.cur_toks2

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
                                gloss_data["glossTokens1"] = tokens_1
                                gloss_data['glossTokens2'] = tokens_2
                                break
        update_json(file_name, main_file)

        working_file1 = self.lexicon_1
        for tok1 in tokens_1:
            tok1_pos = tok1[1]
            tok1_head = tok1[2]
            if tok1_pos not in ["<unknown>", "<Latin>", "<Latin CCONJ>"] and tok1_head[-2:] != " ?":
                tok1_form = tok1[0]
                if tok1_form not in [".i."]:
                    all_filepos = [level_1.get("part_of_speech") for level_1 in working_file1]
                    if tok1_pos in all_filepos:
                        file_pos_data = working_file1[all_filepos.index(tok1_pos)].get("lemmata")
                        all_filelemmata = [level_2.get("lemma") for level_2 in file_pos_data]
                        if tok1_head in all_filelemmata:
                            file_tok_data = file_pos_data[all_filelemmata.index(tok1_head)].get("tokens")
                            all_filetoks = [level_3.get("token") for level_3 in file_tok_data]
                            if tok1_form not in all_filetoks:
                                filetoks_plus = sorted(list(set(
                                    [level_3.get("token") for level_3 in file_tok_data] + [tok1_form]
                                )))
                                correct_position = filetoks_plus.index(tok1_form)
                                insert = {'token': tok1_form, 'feature_sets': [{'feature_set': 1, 'features': []}]}
                                file_tok_data = file_tok_data[:correct_position] + [
                                    insert
                                ] + file_tok_data[correct_position:]
                                file_pos_data[all_filelemmata.index(tok1_head)] = {
                                    'lemma': tok1_head, 'tokens': file_tok_data
                                }
                                working_file1[all_filepos.index(tok1_pos)] = {
                                    'part_of_speech': tok1_pos, 'lemmata': file_pos_data
                                }
                        else:
                            filelemmata_plus = sorted(list(set(
                                [level_2.get("lemma") for level_2 in file_pos_data] + [tok1_head]
                            )))
                            correct_position = filelemmata_plus.index(tok1_head)
                            insert = {'token': tok1_form, 'feature_sets': [{'feature_set': 1, 'features': []}]}
                            insert = {'lemma': tok1_head, 'tokens': [insert]}
                            file_pos_data = file_pos_data[:correct_position] + [
                                insert
                            ] + file_pos_data[correct_position:]
                            working_file1[all_filepos.index(tok1_pos)] = {
                                'part_of_speech': tok1_pos, 'lemmata': file_pos_data
                            }
                    else:
                        filepos_plus = sorted(list(set(
                            [level_1.get("part_of_speech") for level_1 in working_file1] + [tok1_pos]
                        )))
                        correct_position = filepos_plus.index(tok1_pos)
                        insert = {'token': tok1_form, 'feature_sets': [{'feature_set': 1, 'features': []}]}
                        insert = {'lemma': tok1_head, 'tokens': [insert]}
                        insert = {'part_of_speech': tok1_pos, 'lemmata': [insert]}
                        working_file1 = working_file1[:correct_position] + [insert] + working_file1[correct_position:]
        with open("Working_lexicon_file_1.json", 'w', encoding="utf-8") as workfile1:
            json.dump(working_file1, workfile1, indent=4, ensure_ascii=False)

        working_file2 = self.lexicon_2
        for tok2 in tokens_2:
            tok2_pos = tok2[1]
            tok2_head = tok2[2]
            if tok2_pos not in ["<unknown>", "<Latin>", "<Latin CCONJ>"] and tok2_head[-2:] != " ?":
                tok2_form = tok2[0]
                if tok2_form not in [".i."]:
                    all_filepos = [level_1.get("part_of_speech") for level_1 in working_file2]
                    if tok2_pos in all_filepos:
                        file_pos_data = working_file2[all_filepos.index(tok2_pos)].get("lemmata")
                        all_filelemmata = [level_2.get("lemma") for level_2 in file_pos_data]
                        if tok2_head in all_filelemmata:
                            file_tok_data = file_pos_data[all_filelemmata.index(tok2_head)].get("tokens")
                            all_filetoks = [level_3.get("token") for level_3 in file_tok_data]
                            if tok2_form not in all_filetoks:
                                filetoks_plus = sorted(list(set(
                                    [level_3.get("token") for level_3 in file_tok_data] + [tok2_form]
                                )))
                                correct_position = filetoks_plus.index(tok2_form)
                                insert = {'token': tok2_form, 'feature_sets': [{'feature_set': 1, 'features': []}]}
                                file_tok_data = file_tok_data[:correct_position] + [
                                    insert
                                ] + file_tok_data[correct_position:]
                                file_pos_data[all_filelemmata.index(tok2_head)] = {
                                    'lemma': tok2_head, 'tokens': file_tok_data
                                }
                                working_file2[all_filepos.index(tok2_pos)] = {
                                    'part_of_speech': tok2_pos, 'lemmata': file_pos_data
                                }
                        else:
                            filelemmata_plus = sorted(list(set(
                                [level_2.get("lemma") for level_2 in file_pos_data] + [tok2_head]
                            )))
                            correct_position = filelemmata_plus.index(tok2_head)
                            insert = {'token': tok2_form, 'feature_sets': [{'feature_set': 1, 'features': []}]}
                            insert = {'lemma': tok2_head, 'tokens': [insert]}
                            file_pos_data = file_pos_data[:correct_position] + [
                                insert
                            ] + file_pos_data[correct_position:]
                            working_file2[all_filepos.index(tok2_pos)] = {
                                'part_of_speech': tok2_pos, 'lemmata': file_pos_data
                            }
                    else:
                        filepos_plus = sorted(list(set(
                            [level_1.get("part_of_speech") for level_1 in working_file2] + [tok2_pos]
                        )))
                        correct_position = filepos_plus.index(tok2_pos)
                        insert = {'token': tok2_form, 'feature_sets': [{'feature_set': 1, 'features': []}]}
                        insert = {'lemma': tok2_head, 'tokens': [insert]}
                        insert = {'part_of_speech': tok2_pos, 'lemmata': [insert]}
                        working_file2 = working_file2[:correct_position] + [insert] + working_file2[correct_position:]
        with open("Working_lexicon_file_2.json", 'w', encoding="utf-8") as workfile2:
            json.dump(working_file2, workfile2, indent=4, ensure_ascii=False)

    def last_gloss(self):

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
            cur_toks1=self.selected_gloss_info["selected_toks1"],
            cur_toks2=self.selected_gloss_info["selected_toks2"]
        )

    def next_gloss(self):

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
            cur_toks1=self.selected_gloss_info["selected_toks1"],
            cur_toks2=self.selected_gloss_info["selected_toks2"]
        )

    def emp_points(self, text):
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
                    if len(remainder) < max_linelen:
                        text_cuts.append(remainder)
            text = "\n".join(text_cuts)
        return text


def refresh_tokens(string, tokens):
    return_tokens = list()
    string = " ".join(string.split("\n")).strip()
    test_against = [[i, "<unknown>", "<unknown>"] for i in string.split(" ")]
    if tokens == test_against:
        return tokens
    else:
        for i, tok_pos in enumerate(tokens):
            token = tok_pos[0]
            if [token, "<unknown>", "<unknown>"] in test_against:
                match_place = test_against.index([token, "<unknown>", "<unknown>"])
                removal = test_against[:match_place + 1]
                if len(removal) > 1:
                    return_tokens = return_tokens + removal[:-1]
                test_against = test_against[match_place + 1:]
                return_tokens.append(tok_pos)
        if test_against:
            return_tokens = return_tokens + test_against
        return return_tokens


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
                token_list = [[i, "<unknown>", "<unknown>"] if i != ".i."
                              else [i, "ADV", ".i."] for i in clear_tags(gloss).split(" ")]
                token_list = [[i, "<Latin CCONJ>", "et"] if i in ["et"] else [i, j, k] for i, j, k in token_list]
                token_list = [[i, "CCONJ", "ocus"] if i in ["⁊"] else [i, j, k] for i, j, k in token_list]
                token_list = [[i, "CCONJ", "nó"] if i in ["ɫ", "ɫ."] else [i, j, k] for i, j, k in token_list]
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
                toks2 = gloss['glossTokens2']
                gloss_data = [hand, gloss_text, trans, toks1, toks2]
    return gloss_data


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

    # Create a JSON document of the Wb. Glosses in the Manual Tokenisation folder if it doesn't exist already
    dir_contents = os.listdir()
    if "Wb. Manual Tokenisation.json" not in dir_contents:
        os.chdir(maindir)
        wbglosslist = combine_infolists("Wurzburg Glosses", 499, 712)
        os.chdir(tokenise_dir)
        save_json(make_json(wbglosslist, True), "Wb. Manual Tokenisation")

    # Open the Wb. JSON file for use in the GUI
    with open("Wb. Manual Tokenisation.json", 'r', encoding="utf-8") as wb_json:
        wb_data = json.load(wb_json)

    # Create 2 JSON documents of OI Lexica in the Manual Tokenisation folder from the two Sg. CoNNL_U files,
    # one for each tokenisation type, if they doesn't exist already

    # Lexicon 1 = combined-tokens style
    dir_contents = os.listdir()
    if "Lexicon_1.json" not in dir_contents:
        os.chdir(maindir)
        sg_json1 = make_lex_json("sga_dipsgg-ud-test_combined_POS.conllu")
        os.chdir(tokenise_dir)
        save_json(sg_json1, "Lexicon_1")

    # Lexicon 2 = separated-tokens style
    if "Lexicon_2.json" not in dir_contents:
        os.chdir(maindir)
        sg_json2 = make_lex_json("sga_dipsgg-ud-test_split_POS.conllu")
        os.chdir(tokenise_dir)
        save_json(sg_json2, "Lexicon_2")

    # Create a working copy of each of the OI Lexica created above for use in the GUI, if they doesn't exist already
    # These will be updated with new tokens and POS from Wb. which will not be saved to in the originals above

    # Lexicon 1 = combined-tokens style
    dir_contents = os.listdir()
    if "Working_lexicon_file_1.json" not in dir_contents:
        os.chdir(maindir)
        sg_json1 = make_lex_json("sga_dipsgg-ud-test_combined_POS.conllu")
        os.chdir(tokenise_dir)
        save_json(sg_json1, "Working_lexicon_file_1")

    # Open the first Lexicon JSON file for use in the GUI
    with open("Working_lexicon_file_1.json", 'r', encoding="utf-8") as lex1_working_json:
        working_lexicon_1 = json.load(lex1_working_json)

    # Lexicon 2 = separated-tokens style
    if "Working_lexicon_file_2.json" not in dir_contents:
        os.chdir(maindir)
        sg_json2 = make_lex_json("sga_dipsgg-ud-test_split_POS.conllu")
        os.chdir(tokenise_dir)
        save_json(sg_json2, "Working_lexicon_file_2")

    # Open the second Lexicon JSON file for use in the GUI
    with open("Working_lexicon_file_2.json", 'r', encoding="utf-8") as lex2_working_json:
        working_lexicon_2 = json.load(lex2_working_json)

    working_lexica = [working_lexicon_1, working_lexicon_2]

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


    # Start the UI
    ui = UI(
        file_name="Wb. Manual Tokenisation.json",
        wb_data=wb_data,
        lexica=working_lexica
    )
    ui.start()
