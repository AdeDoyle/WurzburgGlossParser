
import os
import json
from lexicon_functions import create_site_lex


def update_gloss_ids():
    """Opens tagged glosses and requests, presents users with headwords with missing lemma IDs
       Users can then input the required ID for each headword as necessary, and these are saved to the lexicon"""

    man_tok_filepath = os.path.join(os.getcwd(), "Manual_Tokenise_Files")
    with open(os.path.join(man_tok_filepath, "Wb. Manual Tokenisation.json"), 'r', encoding="utf-8") as wb_json:
        wb_data = json.load(wb_json)
    with open(os.path.join(man_tok_filepath, "Working_lexicon.json"), 'r', encoding="utf-8") as wb_lex:
        lex_data = json.load(wb_lex)
    simp_lex = create_site_lex()

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
                            if not t_IDd:
                                print()
                                print(gloss_id, gloss_text)
                                print(f"    {token[:3] + [tok_num]}")
                                user_tok_id = input("        Input lemma ID: ")
                                if user_tok_id in ["none", "None", "null", "Null", "false", "False",
                                                   "no", "No", "NO", "no!", "No!", "NO!"]:
                                    user_tok_id = "None"
                                elif user_tok_id in ["exit", "exit!", "Exit", "Exit!"]:
                                    return
                                else:
                                    try:
                                        user_tok_id = int(user_tok_id)
                                    except ValueError:
                                        raise RuntimeError("Lemma ID must be a number (int) or Null")

                                # Update Manual Tokenisation JSON file with user-supplied eDIL lemma ID for each token
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


if __name__ == "__main__":

    update_gloss_ids()

