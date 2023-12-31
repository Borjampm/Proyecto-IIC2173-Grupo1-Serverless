import boto3
from fpdf.fpdf import FPDF
import uuid
import time
import json


def lambda_handler(event, context):
    # Check if it's an HTTP OPTIONS (preflight) request
    if event["httpMethod"] == "OPTIONS":
        # Handle the CORS preflight request
        headers = {
            "Access-Control-Allow-Origin": "*",  # Or specify your allowed origins
            "Access-Control-Allow-Methods": "POST",
            "Access-Control-Allow-Headers": "Content-Type",
        }
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps("CORS preflight request successful"),
        }

    if event["httpMethod"] == "POST":
        # Parse the request body
        request_body = json.loads(event["body"])
        print(request_body, "request body")

        # Access the data sent in the POST request
        group = request_body.get("group")
        user = request_body.get("user")
        company = request_body.get("companyId")
        quantity = request_body.get("quantity")
        price = request_body.get("price")
        totalAmount = request_body.get("totalAmount")
        date = request_body.get("date")
        userId = request_body.get("userId")

        text = f"Comprobate de compra\nVendedor: grupo {group}"
        text += f"Comprador: {user}"

        text2 = f"Detalles de la compra --> Empresa: {company} | Quantity: {quantity} | Price: {price} | Total Amount: {totalAmount}"
        # Create a PDF document
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(
            200, 10, txt=text, ln=True, align='C')
        pdf.cell(
            200, 10, txt=text2, ln=True, align='C')

        # Save the PDF to a file
        pdf_content = pdf.output(dest='S').encode('latin1')

        # Upload the PDF to an S3 bucket
        bucket_name = "e1-arquisis"
        s3_object_key = f"pdf/pdf_{userId}_{totalAmount}.pdf"

        s3 = boto3.client("s3")

        try:
            s3.put_object(Bucket=bucket_name,
                          Key=s3_object_key, Body=pdf_content)
            url = s3.generate_presigned_url(
                ClientMethod='get_object',
                Params={
                    'Bucket': "e1-arquisis",
                    'Key': s3_object_key
                },
                ExpiresIn=24 * 3600
            )
            headers = {
                "Access-Control-Allow-Origin": "*",  # This allows requests from any origin
                "Content-Type": "application/json"
            }
            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps({"url": url})
            }
        except Exception as e:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": str(e)})
            }
