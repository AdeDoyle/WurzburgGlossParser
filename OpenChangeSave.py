"""Level 2."""

from OpenDocx import get_text
from SaveDocx import save_docx
import re


def opchsave(filename):
    """Opens a document, allows you to edit it somehow, saves a copy of the document."""
    # Open Document and get text
    text = get_text(filename)
    # Change Document somehow
    # Here instances of "...[a][/GLat]" are being changed to "...[/GLat][a]"
    glatpat = re.compile(r'\[\w\]\[/GLat\]')
    glatpatitir = glatpat.finditer(text)
    swaplist = []
    for i in glatpatitir:
        if i.group() not in swaplist:
            swaplist.append(i.group())
    for error in swaplist:
        letter = error[:3]
        fix = "[/GLat]" + letter
        textlist = text.split(error)
        text = fix.join(textlist)
    # Save a copy of the updated Document
    save_docx(text, filename)
    return "Completed!"


# print(opchsave("Wurzburg Glosses"))
