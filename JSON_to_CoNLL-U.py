
import os
import json
from ClearTags import clear_tags


def j_to_c(json_file_path, output_filename=None, save_folder=None):
    """Takes the JSON file format specific to the Wb. website and converts its contents to CoNLL-U format"""

    with open(json_file_path, "r", encoding="utf-8") as json_file_import:
        json_file = json.load(json_file_import)

    conllu_text = ""

    gloss_counter = 0

    for _, ep in enumerate(json_file):
        folios = ep.get("folios")
        for _, fol in enumerate(folios):
            fol_col = fol.get("folio")
            fol_glosses = fol.get("glosses")
            for _, gloss_data in enumerate(fol_glosses):

                # Get data from JSON file for individual gloss
                gloss_counter += 1
                gloss_num = gloss_data.get("glossNo")
                gloss_id = fol_col + gloss_num
                hand = gloss_data.get("glossHand")
                gloss = clear_tags(gloss_data.get("glossFullTags"), keep_editorial=False)
                gloss = gloss.strip()
                new_gloss = gloss_data.get("newGloss")
                if new_gloss:
                    new_gloss = clear_tags(new_gloss, keep_editorial=False)
                    new_gloss = new_gloss.strip()
                translation = clear_tags(gloss_data.get("glossTrans"), keep_editorial=False)
                translation = translation.strip()
                new_trans = gloss_data.get("newTrans")
                if new_trans:
                    new_trans = clear_tags(new_trans, keep_editorial=False)
                    new_trans = new_trans.strip()
                    translation = new_trans
                tokens = gloss_data.get("glossTokens")

                # Remove html styling tags from text
                for tag in ["<em>", "</em>"]:
                    if new_gloss:
                        if tag in new_gloss:
                            new_gloss = "".join(new_gloss.split(tag))
                    if tag in translation:
                        translation = "".join(translation.split(tag))
                if new_gloss:
                    while "<sup>" in new_gloss:
                        startpoint = new_gloss.find("<sup>")
                        endpoint = new_gloss.find("</sup>") + len("</sup>")
                        new_gloss = new_gloss[:startpoint] + new_gloss[endpoint:]
                        new_gloss = " ".join(new_gloss.split("  "))
                while "<sup>" in translation:
                    startpoint = translation.find("<sup>")
                    endpoint = translation.find("</sup>") + len("</sup>")
                    translation = translation[:startpoint] + translation[endpoint:]
                    translation = " ".join(translation.split("  "))

                # Identify glosses which have not been annotated, and recreate tokens from text
                unannotated = False
                for t in tokens:
                    if t[1] == "<unknown>" or t[2] == "<unknown>":
                        unannotated = True
                if unannotated:
                    tokens = [[tok, "_", "_", None] for tok in gloss.split(" ")]

                # Replace null morphological features in tokens with _ character
                tokens = [t if t[3] else [t[0], t[1], t[2], "_"] for t in tokens]
                # Replace null lemmata (for Latin tokens) with _ character
                tokens = [t if t[2] else [t[0], t[1], "_", t[3]] for t in tokens]
                # Replace non-standard UD tags (for Latin/Greek tokens) with standard alternatives
                tokens = [t if t[1] != "<Latin CCONJ>" else [t[0], "CCONJ", t[2], t[3]] for t in tokens]
                tokens = [t if t[1] != "<Latin>" else [t[0], "X", t[2], "Foreign=Yes"] for t in tokens]
                tokens = [t if t[1] != "<Greek>" else [t[0], "X", t[2], "Foreign=Yes"] for t in tokens]

                # Remove any brackets from tokens
                for b in ["[", "]", "(", ")"]:
                    tokens = [t if b not in t[0] else ["".join(t[0].split(b)), t[1], t[2], t[3]] for t in tokens]

                # Solve any issues caused by distinctions between tokens and the text of glosses
                if "".join(["".join(t[0].split(" ")) for t in tokens]) != "".join(gloss.split(" ")):
                    if new_gloss:
                        if "".join(["".join(t[0].split(" ")) for t in tokens]) == "".join(new_gloss.split(" ")):
                            gloss = new_gloss
                        else:
                            print(f"Tokens: {tokens}")
                            print(f"New Gloss: {new_gloss}")
                            raise RuntimeError("Unresolvable differences between tokens and new-gloss.")
                    else:
                        raise RuntimeError("Unresolvable differences between tokens and gloss.")

                # Create CoNLL-U text for gloss
                conllu_gloss = (f"# sent_id = {gloss_counter}\n"
                                f"# reference = {gloss_id}\n"
                                f"# scribe = {hand}\n"
                                f"# text = {gloss}\n"
                                f"# translation = {translation}\n")
                for toknum, tok in enumerate(tokens):
                    conllu_gloss += f"{toknum + 1}	{tok[0]}	{tok[2]}	{tok[1]}	_	{tok[3]}	_	_	_	_\n"
                conllu_text += conllu_gloss + "\n"

    if not output_filename:
        output_filename = "Wb. Manual Tokenisation.conllu"
    if not save_folder:
        save_folder = "Manual_Tokenise_Files"

    save_dir = os.path.join(os.getcwd(), save_folder, output_filename)
    with open(save_dir, "w", encoding="utf-8") as conllu_file_export:
        conllu_file_export.write(conllu_text)

    return "\nDone"


if __name__ == "__main__":

    json_dir = os.path.join(os.getcwd(), "Manual_Tokenise_Files", "Wb. Manual Tokenisation.json")
    print(j_to_c(json_dir))
