import docx


def get_text(filename):
    """Opens the document containing the glosses and returns the full text"""
    file = docx.Document(filename + ".docx")
    lines = []
    for para in file.paragraphs:
        lines.append(para.text)
    return '\n'.join(lines)


# print(get_text("Wurzburg Glosses"))
