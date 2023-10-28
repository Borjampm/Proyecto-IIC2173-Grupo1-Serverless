import io
import boto3
from fpdf.fpdf import FPDF

def lambda_handler(event, context):
    # Create a PDF document
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Hello, this is a PDF created with FPDF", ln=True, align='C')

    # Save the PDF to a file
    pdf_content = pdf.output(dest='S').encode('latin1')

    # Upload the PDF to an S3 bucket
    bucket_name = "e1-arquisis"
    s3_object_key = "sample.pdf"

    s3 = boto3.client("s3")

    try:
        s3.put_object(Bucket=bucket_name, Key=s3_object_key, Body=pdf_content)
        return f"PDF uploaded to S3 bucket: {bucket_name}, object key: {s3_object_key}"
    except Exception as e:
        return f"Error: {str(e)}"