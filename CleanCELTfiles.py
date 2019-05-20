from OpenDocx import get_text
from SaveDocx import save_docx
import re
from os import listdir
import os.path as op


raw_dir = "CELT_Texts_Raw"
clean_dir = "CELT_Texts_Clean"
thisfile = op.join(raw_dir, "TBF")


def cleantext_CELT(filename):
    """Opens docx file of text as copied from CELT,
       removes line numbers and punctuation,
       saves the updated document."""
    # Open Document and get text
    text = get_text(filename)
    linelist = text.split("\n")
    # Here lines are stripped of white space at the end
    textlist = []
    for line in linelist:
        line = line.strip()
        textlist.append(line)
    text = "\n".join(textlist)
    # Here irregular intrusions into texts are removed
    removes = ["[LU1]", "[LU2]", "\nf. L.", 'L. f.', '.r.', '.C.', '.u.', ' m.', " c.", " e.", " R.", " U.", ".ix.",
               ".x.", ".xx.", ".xxx.", ".u."]
    for rem in removes:
        text = "".join(text.split(rem))
    # Here punctuated items are replaced so that they are not changed when punctuation is removed
    rep_list = [".i.", ".l.", "rl."]
    for replacer in rep_list:
        rep_str = "***".join(replacer.split("."))
        text = rep_str.join(text.split(replacer))
    # Here hyphenated items are replaced appropriately
    post_hyph = ["h-", "m-", "n-", "l-", "t-", "s-", "c-", "r-"]
    for hyph_item in post_hyph:
        hyphpat = re.compile(r'[ ‘\n]' + hyph_item)
        hyphpatitir = hyphpat.finditer(text)
        for hyphpatitem in hyphpatitir:
            thishyphitem = hyphpatitem.group()
            hyph_gone = "".join(thishyphitem.split("-"))
            text = hyph_gone.join(text.split(thishyphitem))
    text = " ".join(text.split("-"))
    # Here apostrophes are removed where they represent a split word
    apostlist = ["'s", "'S", "m' ", "d' ", "th' ", "t' ", "T' "]
    for apost in apostlist:
        apost_gone = "".join(apost.split("'"))
        text = apost_gone.join(text.split(apost))
    # Here line numbers are removed
    remnumlist = []
    linopat = re.compile(r'\n\d{1,4}\] ?')
    linopatitir = linopat.finditer(text)
    for i in linopatitir:
        num = i.group()
        remnumlist.append(num)
    for i in remnumlist[::-1]:
        text = "\n".join(text.split(i))
    # Here page numbers are removed
    pnumlist = []
    pnopat = re.compile(r'p\.\d{1,3}')
    pnopatitir = pnopat.finditer(text)
    for i in pnopatitir:
        pnum = i.group()
        pnumlist.append(pnum)
    for i in pnumlist[::-1]:
        text = "".join(text.split(i))
    # Here folio information is removed
    follist = []
    folpat = re.compile(r'-?{.+}')
    folpatitir = folpat.finditer(text)
    for j in folpatitir:
        fol = j.group()
        follist.append(fol)
    for j in follist:
        text = "".join(text.split(j))
    # Here & and 'et' are replaced with ⁊
    text = "⁊".join(text.split("&"))
    text = " ⁊ ".join(text.split(" et "))
    # Here punctuation is removed
    punclist = ['!', ',', '.', ':', ';', '?', "'", '‘', '’', '[', ']', '(', ')', '|', '/', '—']
    for punc in punclist:
        text = "".join(text.split(punc))
    # Here punctuated items are reinserted into the text where they were replaced
    reinst_list = ["***i***", "***l***", "rl***"]
    for reinstater in reinst_list:
        reinst_str = ".".join(reinstater.split("***"))
        text = reinst_str.join(text.split(reinstater))
    # Here double spacing and triple line spacing are removed
    while "\n\n\n" in text:
        text = "\n\n".join(text.split("\n\n\n"))
    while "  " in text:
        text = " ".join(text.split("  "))
    while "\n " in text:
        text = "\n".join(text.split("\n "))
    # Here text is stripped and lower-cased
    text = text.lower()
    text = text.strip()
    # Save a copy of the updated Document
    save_docx(text, op.join(clean_dir, filename[len(raw_dir) + 1:] + "_cleaned"))
    return "Complete!"


# print(cleantext_CELT(thisfile))

# all_raw_files = [f for f in listdir(raw_dir) if op.isfile(op.join(raw_dir, f))]
# for rf in all_raw_files:
#     rf = "".join(rf.split(".docx"))
#     if rf != ".DS_Store":
#         rf = op.join(raw_dir, rf)
#         print(cleantext_CELT(rf))

