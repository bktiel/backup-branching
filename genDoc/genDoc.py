from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import subprocess
from datetime import date

def generateMFR(reg,company,first,last,email,prefs):
    # where should editing text begin
    ROOT = (140, 490)
    PAGE2_Y_START = 699
    PAGE2_LIMIT = 28
    # how far is a newline
    Y_INTER = 15
    # values to print
    LENGTH = 20
    FIRST = "John"
    LAST = "Riemers"
    EMAIL = "johnathan.riemerspeters@westpoint.edu"
    COMPANY = "H"
    REG = "2"

    TEMPLATE = "original.pdf"
    OUTFILE = "destination.pdf"

    SIGNATURE_BLOCK_START = 0

    OFFICE_SYMBOL = (74, 670)

    # set up font
    pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))


    def writeFooter(page, ystart):
        global SIGNATURE_BLOCK_START
        contentString = f"3.   The point of contact for this memorandum is CDT {LAST.capitalize()}, {FIRST.capitalize()} at"
        Y_OFFSET = ystart
        X_OFFSET = OFFICE_SYMBOL[0]
        page.drawString(X_OFFSET, Y_OFFSET, contentString)
        contentString = f"{EMAIL}"
        X_OFFSET = OFFICE_SYMBOL[0]
        Y_OFFSET -= 15
        page.drawString(X_OFFSET, Y_OFFSET, contentString)
        # set signature block beneath this
        SIGNATURE_BLOCK_START = Y_OFFSET - 15
        X_OFFSET = 310
        Y_OFFSET -= 60
        contentString = f"{FIRST.upper()} {LAST.upper()}"
        page.drawString(X_OFFSET, Y_OFFSET, contentString)
        Y_OFFSET -= 15
        contentString = "CDT, USCC"
        page.drawString(X_OFFSET, Y_OFFSET, contentString)


    packet = io.BytesIO()
    # create a new PDF with Reportlab
    page1 = canvas.Canvas(packet, pagesize=letter)
    page1.setFont('Arial', 11)

    # write office symbol
    contentString = f"MACC-O-{REG}-{COMPANY}"
    page1.drawString(OFFICE_SYMBOL[0], OFFICE_SYMBOL[1], contentString)

    # write date
    contentString = date.today().strftime("%d %B %Y")
    page1.drawString(462, OFFICE_SYMBOL[1], contentString)

    packet2 = None
    if LENGTH > 20:
        packet2 = io.BytesIO()
        # if this big, need to set up another page
        page2 = canvas.Canvas(packet2, pagesize=letter)
        page2.setFont('Arial', 11)

        # write office symbol
        contentString = f"MACC-O-{REG}-{COMPANY}"
        page2.drawString(54, 748, contentString)

        # write contents (actual prefs)
        if LENGTH < PAGE2_LIMIT:
            # write contents
            for i in range(LENGTH):
                page1.drawString(ROOT[0], ROOT[1] - i * Y_INTER, "CYBER")
        else:
            for i in range(PAGE2_LIMIT):
                page1.drawString(ROOT[0], ROOT[1] - i * Y_INTER, "CYBER")
            # write remainder on second page
            for i in range(PAGE2_LIMIT, LENGTH):
                page2.drawString(ROOT[0], PAGE2_Y_START - (i - PAGE2_LIMIT) * Y_INTER, "CYBER")

        # write footer
        writeFooter(page2, (PAGE2_Y_START - ((LENGTH - PAGE2_LIMIT) * Y_INTER) - 5))

        # save
        page1.save()
        page2.save()

    else:
        # write contents
        for i in range(LENGTH):
            page1.drawString(ROOT[0], ROOT[1] - i * Y_INTER, "CYBER")
        # write footer
        writeFooter(page1, (ROOT[1] - (LENGTH * Y_INTER) - 5))
        page1.save()

    # move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open(TEMPLATE, "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # if needed extra page, need to add
    if LENGTH > 20:
        packet2.seek(0)
        second_page = PdfFileReader(packet2)
        page = existing_pdf.getPage(1)
        page.mergePage(second_page.getPage(0))
        output.addPage(page)
    # finally, write "output" to a real file
    # outputStream = open(OUTFILE, "wb")
    # output.write(outputStream)
    # outputStream.close()
    outputStream=io.BytesIO()
    output.write(outputStream)
    outputStream.seek(0)
    return outputStream

    # # make signature block
    # if LENGTH > 20:
    #     subprocess.run(['pyhanko', 'sign', 'addfields', '--field',
    #                     f"2/310,{SIGNATURE_BLOCK_START},450,{SIGNATURE_BLOCK_START - 35}/signature", 'destination.pdf',
    #                     'signme.pdf'])
    # else:
    #     subprocess.run(['pyhanko', 'sign', 'addfields', '--field',
    #                     f"1/310,{SIGNATURE_BLOCK_START},450,{SIGNATURE_BLOCK_START - 35}/signature", 'destination.pdf',
    #                     'signme.pdf'])