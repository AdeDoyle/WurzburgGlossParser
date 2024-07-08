
import os
import json
import unidecode


def check_lex_dups():
    """Check for duplicate headwords under a single POS-tag in the working lexicon"""

    dup_list = list()

    try:
        try_path = os.path.join(os.getcwd(), "Manual_Tokenise_Files")
        if "Working_lexicon.json" in os.listdir(try_path):
            with open(os.path.join(try_path, "Working_lexicon.json"), 'r', encoding="utf-8") as lex_file_json:
                lex_dict = json.load(lex_file_json)

                lex_dict = {
                    pos.get("part_of_speech"): [
                        lem.get("lemma") for lem in pos.get("lemmata")
                    ] for pos in lex_dict
                }

                for pos in lex_dict:
                    pos_lems = lex_dict.get(pos)
                    for lem in pos_lems:
                        if pos_lems.count(lem) != 1:
                            duple = (pos, lem, pos_lems.count(lem))
                            if duple not in dup_list:
                                dup_list.append(duple)

        else:
            raise RuntimeError("Could not find lexicon in directory")
    except FileNotFoundError:
        raise RuntimeError("Could not find directory containing lexicon")

    return dup_list


def create_site_lex(replace_none_string=True):
    """Returns a JSON lookup dictionary for all headwords.
       It assumes that no duplicate headwords occur within any given POS group."""

    if check_lex_dups():
        raise RuntimeError(f"Duplicate headwords found in working Lexicon:\n    {check_lex_dups()}")
    else:
        try:
            try_path = os.path.join(os.getcwd(), "Manual_Tokenise_Files")
            if "Working_lexicon.json" in os.listdir(try_path):
                with open(os.path.join(try_path, "Working_lexicon.json"), 'r', encoding="utf-8") as lex_file_json:
                    lex_dict = json.load(lex_file_json)
                    # Where tokens have no headword in eDIL they are tagged with the string "None"
                    # By default this is replaced with a null value for use on the Wb. website
                    if replace_none_string:
                        lex_dict = {
                            pos.get("part_of_speech"): {
                                lem.get("lemma"): lem.get("eDIL_id") if lem.get("eDIL_id") != "None" else None
                                for lem in pos.get("lemmata")
                            } for pos in lex_dict
                        }
                    # If specified, the "None" string can be kept (as is necessary for functions in update_lexIDs.py)
                    else:
                        lex_dict = {
                            pos.get("part_of_speech"): {
                                lem.get("lemma"): lem.get("eDIL_id") for lem in pos.get("lemmata")
                            } for pos in lex_dict
                        }
            else:
                raise RuntimeError("Could not find lexicon in directory")
        except FileNotFoundError:
            raise RuntimeError("Could not find directory containing lexicon")

    return lex_dict


def create_lex_lookup():
    """
    Creates an alphabetised lookup table for use on the Wb. website.
    Table contains a list of lemmata  which are currently in use in annotated glosses,
    and an ordered list of all glosses in which each lemma occurs throughout the Wb. corpus.
    """

    simp_lex = create_site_lex()
    simp_lex = [[pos, simp_lex.get(pos)] for pos in simp_lex]
    simp_lex = [[[tok, pos_group[1].get(tok), pos_group[0]] for tok in pos_group[1]] for pos_group in simp_lex]
    lex_lookup = [i for j in simp_lex for i in j if i[1]]
    lex_lookup.sort(key=lambda x: (unidecode.unidecode(x[0]), x[2]))
    while lex_lookup[0][0][0] != "a":
        moving = lex_lookup[0]
        lex_lookup = lex_lookup[1:] + [moving]

    try:
        try_path = os.path.join(os.getcwd(), "Manual_Tokenise_Files")
        if "Wb. Manual Tokenisation.json" in os.listdir(try_path):
            with open(os.path.join(try_path, "Wb. Manual Tokenisation.json"), 'r', encoding="utf-8") as glosses_json:
                ep_data = json.load(glosses_json)
        else:
            raise RuntimeError("Could not find Manual Tokenisation file in directory")
    except FileNotFoundError:
        raise RuntimeError("Could not find directory containing Manual Tokenisation file")

    for i, item in enumerate(lex_lookup):
        item_glosses = list()
        item_forms = list()
        item_check = [item[0], item[2]]
        for epistle in ep_data:
            folio_data = epistle.get("folios")
            for folio in folio_data:
                fol_num = folio.get("folio")
                gloss_data = folio.get("glosses")
                for gloss in gloss_data:
                    gloss_no = gloss.get("glossNo")
                    tokens = gloss.get("glossTokens")
                    for token in tokens:
                        tok_check = [token[2], token[1]]
                        if tok_check[0] and tok_check not in [
                            ['<unknown>', '<unknown>'],
                            ['et', '<Latin CCONJ>']
                        ]:
                            if item_check == tok_check:
                                gloss_id = fol_num[3:] + gloss_no
                                if gloss_id not in item_glosses:
                                    item_glosses.append(gloss_id)
                                if [token[0], gloss_id] not in item_forms:
                                    item_forms.append([token[0], gloss_id])
        item_forms.sort(key=lambda x: x[0])
        form_glosses = [[f[0], [i[1] for i in item_forms if i[0] == f[0]]] for f in item_forms]
        unique_forms = list()
        [unique_forms.append(i) for i in form_glosses if i not in unique_forms]
        lex_lookup[i].append(item_glosses)
        lex_lookup[i].append(unique_forms)
    lex_lookup = [i for i in lex_lookup if [i[3], i[4]] != [[], []]]

    return lex_lookup


if __name__ == "__main__":

    with open(os.path.join(os.getcwd(), "Manual_tokenise_files", "OI_lexicon.json"), 'w', encoding="utf-8") as lex_file:
        json.dump(create_site_lex(), lex_file, indent=4, ensure_ascii=False)

    with open(os.path.join(os.getcwd(), "Manual_tokenise_files", "lex_lookup.json"), 'w', encoding="utf-8") as lex_file:
        json.dump(create_lex_lookup(), lex_file, indent=4, ensure_ascii=False)

