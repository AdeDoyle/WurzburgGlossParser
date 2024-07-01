
import os
import json


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


if __name__ == "__main__":

    with open(os.path.join(os.getcwd(), "Manual_tokenise_files", "OI_lexicon.json"), 'w', encoding="utf-8") as lex_file:
        json.dump(create_site_lex(), lex_file, indent=4, ensure_ascii=False)
