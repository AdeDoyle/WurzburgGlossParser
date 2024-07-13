
import os
import json
from lexicon_functions import create_site_lex, create_lex_lookup


def update_gloss_ids(update_site_lex=True):
    """Opens tagged glosses and requests, presents users with headwords with missing lemma IDs
       Users can then input the required ID for each headword as necessary, and these are saved to the lexicon"""

    man_tok_filepath = os.path.join(os.getcwd(), "Manual_Tokenise_Files")
    with open(os.path.join(man_tok_filepath, "Wb. Manual Tokenisation.json"), 'r', encoding="utf-8") as wb_json:
        wb_data = json.load(wb_json)
    with open(os.path.join(man_tok_filepath, "Working_lexicon.json"), 'r', encoding="utf-8") as wb_lex:
        lex_data = json.load(wb_lex)
    simp_lex = create_site_lex(False)

    # Iterate through individual glosses, if they're annotated check if headwords have eDIL IDs.
    for ep_num, ep_level in enumerate(wb_data):
        folios = ep_level.get("folios")
        for fol_num, folio in enumerate(folios):
            fol_col = folio.get("folio")
            glosses = folio.get("glosses")
            for gloss_num, gloss in enumerate(glosses):
                gloss_id = f"{fol_col}{gloss.get('glossNo')}"
                # Test each goss to see if it's been annotated yet, and ignore it if it hasn't
                gl_annotated = True
                tok_data = gloss.get("glossTokens")
                test_anno = [
                    tok for tok in tok_data if [tok[1], tok[2]] in [
                        ["<unknown>", "<unknown>"],
                        ["ADV", ".i."],
                        ["ADV", "⁊rl."],
                        ["CCONJ", "nó"],
                        ["<Greek>", ""],
                        ["<Latin>", ""],
                        ["<Latin CCONJ>", "et"]
                    ]
                ]
                if test_anno == tok_data:
                    gl_annotated = False
                if gl_annotated:
                    if gloss.get("newGloss"):
                        gloss_text = gloss.get("newGloss")
                    else:
                        gloss_text = gloss.get("glossText")
                    if gloss.get("glossTrans") != "No translation available in <em>Thesaurus Palaeohibernicus</em>.":
                        gloss_trans = gloss.get("glossTrans")
                    else:
                        gloss_trans = "No translation available."
                    if gloss.get("newTrans"):
                        gloss_trans = gloss.get("newTrans")
                    # Check that each annotated token has a headword
                    for tok_num, token in enumerate(tok_data):
                        if [token[1], token[2]] not in [
                            ["<unknown>", "<unknown>"],
                            ["ADV", "⁊rl."],
                            ["<Greek>", ""],
                            ["<Latin>", ""],
                            ["<Latin CCONJ>", "et"]
                        ] and token[1] != "PUNCT":
                            t_IDd = simp_lex.get(token[1]).get(token[2])
                            # Request user input for annotated tokens with lemmata which haven't yet been linked
                            # to a headword in eDIL via an ID number
                            if not t_IDd:
                                print()
                                print(gloss_id, f"\n    {gloss_text}\n    {gloss_trans}")
                                print(f"    {token[:3] + [tok_num]}")
                                user_tok_id = input("\nInput lemma ID: ")
                                # Allow users to mark a lemma as not having any eDIL headword ID
                                if user_tok_id in ["none", "None", "null", "Null", "false", "False",
                                                   "no", "No", "NO", "no!", "No!", "NO!"]:
                                    user_tok_id = "None"
                                # Allow users to quit the program without inputting any ID for the current lemma
                                elif user_tok_id in ["exit", "exit!", "Exit", "Exit!", "EXIT", "EXIT!"]:
                                    return
                                # Allow users to input multiple relevant eDIL headword IDs if necessary,
                                # List must start with primary ID (as per lemma and/or POS-tag)
                                elif user_tok_id in ["lst", "list", "list!", "List", "List!", "LIST", "LIST!"]:
                                    user_tok_id = list()
                                    user_prim_id = input("    Input lemma primary ID: ")
                                    if user_prim_id in ["exit", "exit!", "Exit", "Exit!", "EXIT", "EXIT!"]:
                                        return
                                    else:
                                        try:
                                            user_prim_id = int(user_prim_id)
                                            user_tok_id.append(user_prim_id)
                                        except ValueError:
                                            raise RuntimeError("In a lemma ID list, the primary lemma ID must be a "
                                                               "number (int). Alternatively, type 'exit' to quit.")
                                    while True:
                                        next_rel_id = input("    Input another relevant ID: ")
                                        if next_rel_id in ["exit", "exit!", "Exit", "Exit!", "EXIT", "EXIT!"]:
                                            break
                                        else:
                                            try:
                                                next_rel_id = int(next_rel_id)
                                                user_tok_id.append(next_rel_id)
                                            except ValueError:
                                                print("In a lemma ID list, lemma IDs must be a number (int). "
                                                      "Alternatively, type 'exit' to close the list.")
                                    if not user_tok_id:
                                        raise RuntimeError(f"Expected user input to be a list containing numbers (int)."
                                                           f"\nInstead got: {user_tok_id}")
                                    elif not isinstance(user_tok_id, list):
                                        raise RuntimeError(f"Expected user input to be a list containing numbers (int)."
                                                           f"\nInstead got: {user_tok_id}")
                                    elif len(user_tok_id) == 1:
                                        user_tok_id = user_tok_id[0]
                                # Expect that any other input will be a simple integer correlating with an eDIL ID
                                else:
                                    try:
                                        user_tok_id = int(user_tok_id)
                                    except ValueError:
                                        raise RuntimeError("Lemma ID must be a number (int), list of numbers, or Null. "
                                                           "Alternatively, type 'exit' to quit.")

                                # Update Manual Tokenisation JSON file with user input for each token
                                for pos in lex_data:
                                    if pos.get("part_of_speech") == token[1]:
                                        lem_data = pos.get("lemmata")
                                        for lem in lem_data:
                                            if lem.get("lemma") == token[2]:
                                                lem["eDIL_id"] = user_tok_id
                                                break
                                        break
                                with open(
                                        os.path.join(
                                            os.getcwd(), "Manual_Tokenise_Files", "Working_lexicon.json"
                                        ), 'w', encoding="utf-8"
                                ) as json_update:
                                    json.dump(lex_data, json_update, indent=4, ensure_ascii=False)
                                # Recreate the simplified lexicon so changes in the working lexicon are reflected here
                                simp_lex = create_site_lex(False)

    # Update the website lexicon files
    with open(os.path.join(os.getcwd(), "Manual_tokenise_files", "OI_lexicon.json"), 'w', encoding="utf-8") as lex_file:
        json.dump(create_site_lex(), lex_file, indent=4, ensure_ascii=False)

    with open(os.path.join(os.getcwd(), "Manual_tokenise_files", "lex_lookup.json"), 'w', encoding="utf-8") as lex_file:
        json.dump(create_lex_lookup(), lex_file, indent=4, ensure_ascii=False)


if __name__ == "__main__":

    update_gloss_ids()

