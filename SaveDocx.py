"""Level 1"""

from docx import Document


def save_docx(content, docname="New Doc"):
    doc = Document()
    doc.add_paragraph(content)
    doc.save(docname + ".docx")


# testdoc = """This is the title
#
# This is the secondary title
#
# Para 1 Line 1
# Para 1 Line 2
#
# Para 2 Line 1
# Para 2 Line 2"""
# save_docx(testdoc, "mydoc")
