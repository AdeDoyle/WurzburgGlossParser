
import os
import re
import json
from conllu import parse


def c_to_j(conllu_file, json_file, output_filename=None, save_folder=None):
    """Adds token information from manually parsed a CoNLL-U file to the Wb. website's JSON format"""

    if not output_filename:
        output_filename = "Wb. Manual Tokenisation - update.json"
    if save_folder:
        output_filename = os.path.join(save_folder, output_filename)
    else:
        save_folder = os.path.join(os.getcwd(), "Manual_Tokenise_Files")
        output_filename = os.path.join(save_folder, output_filename)

    # Creates a list containing relevant data for each gloss: [[folio-column, gloss-number, token-data] ...]
    glosses = list()
    for gloss in conllu_file:

        # Get and split gloss references into parts to sort the glosses
        meta = gloss.metadata
        id = meta.get("reference")
        id_pat = re.compile(r"\d{1,2}[abcd]")
        id_pat_iter = id_pat.findall(id)
        folcol = f"f. {id_pat_iter[0]}"
        gl_id = id[len(folcol) - 3:]

        # Gets token data for each gloss, compiles it into a list of tuples: [(token, pos-tag, headword, features) ...]
        tokens = [tok.get("form") for tok in gloss]
        pos = [tok.get("upos") for tok in gloss]
        head = [tok.get("lemma") for tok in gloss]
        feats = ["|".join([f"{key}={feat_dict.get(key)}" for key in feat_dict]) if feat_dict else None for feat_dict in
                 [tok.get("feats") for tok in gloss]]
        tok_data = list(zip(tokens, pos, head, feats))
        tok_data = [[i[0], i[1], i[2], i[3]] for i in tok_data]
        tok_data = [t if t != ['et', 'CCONJ', '_', 'Foreign=Yes']
                    else ['et', '<Latin CCONJ>', 'et', 'Foreign=Yes'] for t in tok_data]
        tok_data = [t if t[2:] != ['_', 'Foreign=Yes']
                    else [t[0], '<Latin>', '', None] for t in tok_data]

        gloss_list = [folcol, gl_id, tok_data]
        glosses.append(gloss_list)

    for tagged_gloss in glosses:
        tagged_fol = tagged_gloss[0]
        tagged_glno = tagged_gloss[1]
        tagged_toks = tagged_gloss[2]
        for _, ep in enumerate(json_file):
            folios = ep.get("folios")
            for _, fol in enumerate(folios):
                fol_col = fol.get("folio")
                if fol_col == tagged_fol:
                    glosses = fol.get("glosses")
                    for _, gloss_data in enumerate(glosses):
                        gloss_num = gloss_data.get("glossNo")
                        if gloss_num == tagged_glno:
                            gloss_data["glossTokens"] = tagged_toks

    with open(output_filename, 'w', newline='', encoding="utf-8") as new_json_file:
        json.dump(json_file, new_json_file, indent=4, ensure_ascii=False)

    return "\nDone"


if __name__ == "__main__":

    curdir = os.getcwd()

    conllu_dir = os.path.join(curdir, "conllu_files")
    wb_dir = os.path.join(conllu_dir, "Wb_Treebanks")
    wb_conllu = os.path.join(wb_dir, "combined_wb_files.conllu")

    with open(wb_conllu, "r", encoding="utf-8") as conllu_file_import:
        conllu_content = parse(conllu_file_import.read())

    json_dir = os.path.join(curdir, "Manual_Tokenise_Files")
    wb_json = os.path.join(json_dir, "Wb. Manual Tokenisation.json")

    with open(wb_json, "r", encoding="utf-8") as json_file_import:
        json_content = json.load(json_file_import)

    print(c_to_j(conllu_content, json_content))
