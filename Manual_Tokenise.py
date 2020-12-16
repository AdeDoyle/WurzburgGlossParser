
from CombineInfoLists import combine_infolists
from MakeJSON import make_json
from SaveJSON import save_json
import os
import json
from ClearTags import clear_tags
from tkinter import *
from tkinter import ttk


class UI:

    def __init__(self, wb_data, pos_tags):

        self.wb_data = wb_data
        self.epistles = show_epistles(wb_data)
        self.pos_tags = pos_tags

        self.open_ep = self.epistles[0]
        self.open_fols = show_folcols(select_epistle(self.open_ep))
        self.open_folio = self.open_fols[0]
        self.open_glossnums = show_glossnums(select_folcol(select_epistle(self.open_ep), self.open_folio))
        self.open_glossnum = self.open_glossnums[0]
        self.open_glossid = self.open_folio + self.open_glossnum
        self.open_glossdata = select_glossnum(select_folcol(select_epistle(self.open_ep), self.open_folio),
                                              self.open_glossnum)
        self.open_hand = self.open_glossdata[0]
        self.open_gloss = set_spacing(self.open_glossdata[1])
        self.open_trans = set_spacing(self.open_glossdata[2])
        self.open_toks1 = self.open_glossdata[3]
        self.open_toks2 = self.open_glossdata[4]

        # Create the GUI
        self.root = Tk()
        self.root.title("Manual Tokenisation Window")
        self.root.geometry("900x900")

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
            "selected_gloss": set_spacing(selected_glossdata[1]),
            "selected_trans": set_spacing(selected_glossdata[2]),
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
            cur_toks2=self.selected_gloss_info["selected_toks2"],
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
            cur_toks2=self.selected_gloss_info["selected_toks2"],
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
            cur_toks2=self.selected_gloss_info["selected_toks2"],
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
            self.current_rendered_window["toks2_frame"].destroy()
            self.current_rendered_window["buttons_frame"].destroy()

            self.current_rendered_window["ep_drop"].destroy()
            self.current_rendered_window["fol_drop"].destroy()
            self.current_rendered_window["gloss_drop"].destroy()

            self.current_rendered_window["back_button"].destroy()
            self.current_rendered_window["next_button"].destroy()
            self.current_rendered_window["update_toks_button"].destroy()
            self.current_rendered_window["update_pos_button"].destroy()
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

        self.current_rendered_window["toks2_frame"] = LabelFrame(self.current_rendered_window["toks_frames"],
                                                                 padx=5, pady=5)
        self.current_rendered_window["toks2_frame"].grid(row=0, column=1, padx=5, pady=5, sticky="NW")

        self.current_rendered_window["buttons_frame"] = Frame(self.current_rendered_window["toks_frames"],
                                                              padx=5, pady=5)
        self.current_rendered_window["buttons_frame"].grid(row=0, column=2, padx=5, pady=5, sticky="NW")

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

        self.current_rendered_window["update_toks_button"] = Button(self.current_rendered_window["buttons_frame"],
                                                                    text="Update Tokens", command=self.update_tokens)
        self.current_rendered_window["update_toks_button"].grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.current_rendered_window["update_pos_button"] = Button(self.current_rendered_window["buttons_frame"],
                                                                   text="Update POS-tags", command=self.update_pos)
        self.current_rendered_window["update_pos_button"].grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.current_rendered_window["save_button"] = Button(self.current_rendered_window["buttons_frame"],
                                                             text="Save", command=self.save_tokens)
        self.current_rendered_window["save_button"].grid(row=2, column=0, padx=5, pady=5, sticky="w")

        # Create GUI text display boxes
        self.current_rendered_window["gloss_label"] = Label(self.current_rendered_window["text_frame"],
                                                            height=2, text=f"Gloss ({cur_glossid[3:]}) – {cur_hand}:",
                                                            font=("Helvetica", 16))

        self.current_rendered_window["gloss_text"] = Text(self.current_rendered_window["text_frame"],
                                                          width=80, height=5, font=("Courier", 12))
        self.current_rendered_window["gloss_text"].insert(1.0, cur_gloss)
        self.current_rendered_window["gloss_text"].config(state=DISABLED)

        self.current_rendered_window["trans_label"] = Label(self.current_rendered_window["text_frame"],
                                                            height=1, text="Translation:", font=("Helvetica", 16))

        self.current_rendered_window["trans_text"] = Text(self.current_rendered_window["text_frame"],
                                                          width=80, height=5, font=("Courier", 12))
        self.current_rendered_window["trans_text"].insert(1.0, cur_trans)
        self.current_rendered_window["trans_text"].config(state=DISABLED)

        self.current_rendered_window["gloss_label"].pack(anchor='w')
        self.current_rendered_window["gloss_text"].pack(pady=5, anchor='w')
        self.current_rendered_window["trans_label"].pack(anchor='w')
        self.current_rendered_window["trans_text"].pack(pady=5, anchor='w')

        # Create GUI text editing boxes
        self.current_rendered_window["tokenise_label_1"] = Label(self.current_rendered_window["text_frame"],
                                                                 height=2, text=f"Tokenise (1st Standard)",
                                                                 font=("Helvetica", 16))
        self.current_rendered_window["tokenise_text_1"] = Text(self.current_rendered_window["text_frame"], width=80,
                                                               height=5, borderwidth=1, relief="solid",
                                                               font=("Courier", 12))
        self.current_rendered_window["tokenise_text_1"].insert(1.0, set_spacing(" ".join([i[0] for i in cur_toks1])))

        self.current_rendered_window["tokenise_label_2"] = Label(self.current_rendered_window["text_frame"],
                                                                 height=1, text="Tokenise (2nd Standard)",
                                                                 font=("Helvetica", 16))
        self.current_rendered_window["tokenise_text_2"] = Text(self.current_rendered_window["text_frame"], width=80,
                                                               height=5, borderwidth=1, relief="solid",
                                                               font=("Courier", 12))
        self.current_rendered_window["tokenise_text_2"].insert(1.0, set_spacing(" ".join([i[0] for i in cur_toks2])))

        self.current_rendered_window["tokenise_label_1"].pack(anchor='w')
        self.current_rendered_window["tokenise_text_1"].pack(pady=5, anchor='w')
        self.current_rendered_window["tokenise_label_2"].pack(anchor='w')
        self.current_rendered_window["tokenise_text_2"].pack(pady=5, anchor='w')

        # Create lables for the tokens and POS tags (style 1)
        self.current_rendered_window["toks1_label"] = Label(self.current_rendered_window["toks1_frame"],
                                                            text="Tokens (1)", font=("Helvetica", 16))
        self.current_rendered_window["toks1_label"].grid(row=0, column=0, padx=5, pady=5)
        self.current_rendered_window["pos1_label"] = Label(self.current_rendered_window["toks1_frame"],
                                                           text="POS tags", font=("Helvetica", 16))
        self.current_rendered_window["pos1_label"].grid(row=0, column=1, padx=5, pady=5)

        # Create tokens and POS menus for the tokens and POS tags (style 1)
        self.cur_toks1 = cur_toks1
        for i, pos_token in enumerate(cur_toks1):
            token = pos_token[0]
            tag = pos_token[1]
            self.current_rendered_window[f"toks1_tok_{i}"] = Label(self.current_rendered_window["toks1_frame"],
                                                                   text=token, font=("Helvetica", 12))
            self.current_rendered_window[f"toks1_tok_{i}"].grid(row=i + 1, column=0, padx=5, pady=5, sticky='e')

            unknown_pos = StringVar()
            unknown_pos.set(tag)
            self.current_rendered_window[f"pos_drop1.{i}"] = OptionMenu(self.current_rendered_window["toks1_frame"],
                                                                        unknown_pos, *self.pos_tags)
            self.current_rendered_window[f"pos_drop1.{i}"].grid(row=i + 1, column=1, sticky='w')

        # Create lables for the tokens and POS tags (style 2)
        self.cur_toks2 = cur_toks2
        self.current_rendered_window["toks2_label"] = Label(self.current_rendered_window["toks2_frame"],
                                                            text="Tokens (2)", font=("Helvetica", 16))
        self.current_rendered_window["toks2_label"].grid(row=0, column=0, padx=5, pady=5)
        self.current_rendered_window["pos2_label"] = Label(self.current_rendered_window["toks2_frame"],
                                                           text="POS tags", font=("Helvetica", 16))
        self.current_rendered_window["pos2_label"].grid(row=0, column=1, padx=5, pady=5)

        # Create tokens and POS menus for the tokens and POS tags (style 1)
        for i, pos_token in enumerate(cur_toks2):
            token = pos_token[0]
            tag = pos_token[1]
            self.current_rendered_window[f"toks2_tok_{i}"] = Label(self.current_rendered_window["toks2_frame"],
                                                                   text=token, font=("Helvetica", 12))
            self.current_rendered_window[f"toks2_tok_{i}"].grid(row=i + 1, column=0, padx=5, pady=5, sticky='e')

            unknown_pos = StringVar()
            unknown_pos.set(tag)
            self.current_rendered_window[f"pos_drop2.{i}"] = OptionMenu(self.current_rendered_window["toks2_frame"],
                                                                        unknown_pos, *self.pos_tags)
            self.current_rendered_window[f"pos_drop2.{i}"].grid(row=i + 1, column=1, sticky='w')

    def update_tokens(self):
        string_1 = self.current_rendered_window["tokenise_text_1"].get(1.0, END)
        tokens_1 = self.cur_toks1

        string_2 = self.current_rendered_window["tokenise_text_2"].get(1.0, END)
        tokens_2 = self.cur_toks2

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
            cur_toks2=refresh_tokens(string_2, tokens_2),
        )

    def update_pos(self):
        pass

    def save_tokens(self):
        pass

    def last_gloss(self):
        self.save_tokens()

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
            cur_toks2=self.selected_gloss_info["selected_toks2"],
        )

    def next_gloss(self):
        self.save_tokens()

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
            cur_toks2=self.selected_gloss_info["selected_toks2"],
        )


def set_spacing(text):
    max_linelen = 80
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
    test_against = [[i, "<unknown>"] for i in string.split(" ")]
    if tokens == test_against:
        return tokens
    else:
        for i, tok_pos in enumerate(tokens):
            token = tok_pos[0]
            if [token, "<unknown>"] in test_against:
                match_place = test_against.index([token, "<unknown>"])
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

    pos_tags = ["ADJ", "ADP", "ADV", "AUX", "CCONJ", "DET", "INTJ", "NOUN", "NUM",
                "PART", "PRON", "PROPN", "PUNCT", "SCONJ", "SYM", "VERB", "X",
                "<Latin>", "<unknown>"]

    # Start the UI
    ui = UI(
        wb_data=wb_data,
        pos_tags=pos_tags
    )
    ui.start()
