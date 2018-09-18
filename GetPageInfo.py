"""Level 3"""

from OpenPages import get_pages


def get_pageinfo(file, startpage=499, stoppage=712):
    """Opens the text of the Glosses from the document and returns a page-list of page-no-lists where the page number is
       at page-no-list[0] and the page text is at page-no-list[1] for a selected range of pages"""
    pagelist = []
    for page in range(startpage, stoppage):
        pageno = page
        pagetext = get_pages(file, page, page)
        pagelist.append([pageno, pagetext])
    return pagelist


# glosses = (get_pageinfo("Wurzburg Glosses", 499, 509))
# for i in glosses:
#     print(str(i[0]) + ":\n" + i[1] + "\n")
