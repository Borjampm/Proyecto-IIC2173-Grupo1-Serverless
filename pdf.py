from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, PageBreak, Spacer
from reportlab.lib.units import inch


def lambda_handler(event, context):
    context = 'Borja MPM'

    # Create a PDF document
    doc = SimpleDocTemplate("receipt.pdf", pagesize=letter)

    # Stocks bought data
    stocks_data = """
    Stocks Bought:
    AAPL - 10 shares at $150
    MSFT - 5 shares at $200
    GOOGL - 2 shares at $2500
    """

    # Create a list to hold the elements for the document
    elements = []

    # Add the stocks data as a preformatted text object
    from reportlab.platypus import Preformatted
    from reportlab.lib.styles import getSampleStyleSheet
    title = getSampleStyleSheet()['Title']
    body = getSampleStyleSheet()['Code']
    # elements.append(' ')

    # Add the context as a heading
    elements.append(Preformatted(context, title))

    # Add a spacer
    elements.append(Spacer(1, 12))
    elements.append(Preformatted(stocks_data, body))

    # Add a page break
    elements.append(PageBreak())

    # Build the PDF document, specifying the on_page function to add the header
    doc.build(elements)

lambda_handler('','')
