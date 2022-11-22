from PyPDF2 import PdfFileReader, PdfFileWriter, PageObject
import os
def get_pages_all_pdfs(path):
    files = list(filter(lambda a: a.endswith(".pdf"),  os.listdir(path)))
    allPages = []
    for file in files:
        f = open(f"{path}\\{file}", 'rb')
        pdf = PdfFileReader(f)
        for page in pdf.pages:
            allPages.append(page)
    return allPages

def reorder(pages, blockSize):
    out = []
    if(len(pages) % blockSize * 4 != 0):
        raise Exception(f"{len(pages)} non è divisibile per {blockSize * 4} (DimensioneBlocco * 4)")
    for pagei in range(0, len(pages), blockSize * 4):
        for i in range(0, blockSize * 2):
            if(i % 2 == 0):
                out.append(pages[pagei + (blockSize * 4 - i - 1)])
                out.append(pages[pagei + (i)])
            else:
                out.append(pages[pagei + (i)])
                out.append(pages[pagei + (blockSize * 4 - i - 1)])
    return out

def generate(pages, blockSize, internalMargin, externalMargin):
    if(len(pages) % blockSize * 4 != 0):
        raise Exception(f"{len(pages)} non è divisibile per {blockSize * 4} (DimensioneBlocco * 4)")
    writer = PdfFileWriter()
    for pagei in range(0, len(pages), 2):
        page1 = pages[pagei]
        page2 = pages[pagei + 1]
        newPage = PageObject.createBlankPage(None, float(page1.mediaBox.getWidth()) + float(page2.mediaBox.getWidth()) + (internalMargin * 2) + (externalMargin * 2), max(float(page1.mediaBox.getHeight()), float(page2.mediaBox.getHeight())))
        newPage.mergeScaledTranslatedPage(page1, 1, externalMargin, 0, False)
        w = float(page1.mediaBox.getWidth()) + externalMargin + (internalMargin * 2)
        newPage.mergeScaledTranslatedPage(page2, 1, w, 0, False)
        writer.addPage(newPage)
    return writer


print("Path della cartella che contiene i PDF")
path = input()

print("Da quanti fogli è compsto un blocchetto?")
blockSize = int(input())

print("Di quanti mm il margine esterno? Se premi invio e basta è 0")
x = input()
externalMargin = int(x if x != None and x != "" else "0")

print("Di quanti mm il margine interno? Se premi invio e basta è 0")
x = input()
internalMargin = int(x if x != None and x != "" else "0")

pages = get_pages_all_pdfs(path)
pages = reorder(pages, blockSize)
writ = generate(pages, blockSize, internalMargin, externalMargin)
with(open(f'{path}\\FileFinale.pdf', 'wb')) as f:
    writ.write(f)