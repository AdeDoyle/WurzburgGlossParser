
import os
from conllu import parse


def get_sent_id(sent):
    """Gets the sentence ID of a CoNLL-U sentence for use in sorting"""
    return int(sent.metadata.get("sent_id"))


def combine_conllu(folder=None, combo_file_name=None, save_place=None, combine_method="compound"):
    """Combines the contents of two .conllu files"""

    # Load .conllu files from the specified directory
    loaded_contents = list()
    if folder:
        folder_contents = [file for file in os.listdir(folder) if file[-7:] == ".conllu"]
        for content in folder_contents:
            if content != f"{combo_file_name}.conllu":
                with open(os.path.join(folder, content), "r", encoding="utf-8") as conllu_file_import:
                    text_file = conllu_file_import.read()
                loaded_contents.append(text_file)
    # If no directory is specified, look for .conllu files in the current directory
    else:
        folder_contents = [file for file in os.listdir(os.getcwd()) if file[-7:] == ".conllu"]
        for content in folder_contents:
            if content != f"{combo_file_name}.conllu":
                with open(os.path.join(os.getcwd(), content), "r", encoding="utf-8") as conllu_file_import:
                    text_file = conllu_file_import.read()
                loaded_contents.append(text_file)

    # If no filename is specified, name the file after the parent folder of the .conllu files being combined
    if combo_file_name:
        filename = f"{combo_file_name}.conllu"
    else:
        parentdir = os.path.split(os.getcwd())[-1]
        filename = f"{parentdir}_files_combined.conllu"

    # If no folder path is specified to save the combined .conllu file, save to the current directory instead
    if save_place:
        filename = os.path.join(save_place, filename)

    # Parse the conllu files
    content = [parse(conllu_file) for conllu_file in loaded_contents]

    # Combine all sentences into a single list
    content = [i for l in content for i in l]

    # If no combination method is specified, concatenate all files
    # If integration is specified, use sentence IDs from sentence metadata to order sentences in output file
    if combine_method == "integrate":
        content.sort(key=get_sent_id)
    elif combine_method != "compound":
        raise RuntimeError(f"Combination method must be either 'compound' or 'integrate'\nCombination method selected:"
                           f" '{combine_method}'.")

    sent_list = [sentence.serialize() for sentence in content]
    content = ""
    for i in sent_list:
        content += i

    with open(filename, 'w', encoding='utf-8') as doc:
        doc.write(content)


if __name__ == "__main__":

    curdir = os.getcwd()
    conllu_dir = os.path.join(curdir, "conllu_files")
    wb_dir = os.path.join(conllu_dir, "Wb_Treebanks")
    sg_dir = os.path.join(conllu_dir, "Sg_Treebanks")

    combine_conllu(wb_dir, "combined_wb_files", wb_dir, "integrate")
    combine_conllu(sg_dir, "combined_sg_files", sg_dir, "integrate")
