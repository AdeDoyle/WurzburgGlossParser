from OpenDocx import get_text
from SaveDocx import save_docx
import re


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
    # Here line numbers are removed
    remnumlist = []
    linopat = re.compile(r'\d{1,3}\] ')
    linopatitir = linopat.finditer(text)
    for i in linopatitir:
        num = i.group()
        remnumlist.append(num)
    for i in remnumlist[::-1]:
        text = "".join(text.split(i))
    # Here page numbers are removed
    pnumlist = []
    pnopat = re.compile(r'p\.\d{1,2}')
    pnopatitir = pnopat.finditer(text)
    for i in pnopatitir:
        pnum = i.group()
        pnumlist.append(pnum)
    for i in pnumlist[::-1]:
        text = "".join(text.split(i))
    # Here & are replaced with ⁊
    text = "⁊".join(text.split("&"))
    # Here punctuation is removed
    punclist = ['!', "'", ',', '-', '.', ':', ';', '?', '‘', '’']
    for punc in punclist:
        text = "".join(text.split(punc))
    # Here double spacing and triple line spacing are removed
    while "\n\n\n" in text:
        text = "\n\n".join(text.split("\n\n\n"))
    while "  " in text:
        text = " ".join(text.split("  "))
    # Here text is stripped and lower-cased
    text = text.lower()
    text = text.strip()
    # Save a copy of the updated Document
    save_docx(text, filename + "_cleaned")
    return "Complete!"


# print(cleantext_CELT("TBF"))
