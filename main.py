from PyPDF2 import PdfReader
import pandas as pd
import pdfplumber
import os
import logging

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def clear_currency(value) -> float:
    if value:
        try:
            return float(value.replace(".", "").replace(",", ".").replace("€", "").strip())
        except ValueError:
            logger.warning(f"Failed to convert currency value: {value}")
            return 0.0
    return 0.0

def parse_invoice(pdf_path):
    if not os.path.exists(pdf_path):
        logger.error(f"File not found: {pdf_path}")
        return None
    
    invoice_info = {}
    try:
        with open(pdf_path, "rb") as file:
            reader = PdfReader(file)
            
            # Getting metadata
            metadata = reader.metadata
            invoice_info["author"] = metadata.author if metadata.author else "Unknown"
            invoice_info["title"] = metadata.title if metadata.title else "Unknown"
            invoice_info["creation_date"] = metadata.creation_date if metadata.creation_date else "Unknown"
            invoice_info["pages"] = len(reader.pages)
            
            # Extracting table from the first page
            with pdfplumber.open(pdf_path) as pdf:
                if len(pdf.pages) > 0:
                    table = pdf.pages[0].extract_table()
                    if table:
                        df = pd.DataFrame(table[1:], columns=table[0])
                        invoice_info["table_data"] = df
                        logger.info(f"Successfully extracted table with {len(df)} rows")
                    else:
                        logger.warning("No table found on the first page")
                else:
                    logger.warning("PDF file contains no pages")
            
            return invoice_info
    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")
        return None

if __name__ == "__main__":
    pdf_path = "sample-invoice.pdf"
    result = parse_invoice(pdf_path)
    
    if result:
        table_df = result["table_data"]
        total_rows = table_df.tail(3)
        table_df["quantity"] = pd.to_numeric(table_df["quantity"], errors="coerce").fillna(0).astype(int)
        tr_fee = table_df[table_df["Service Description"].str.contains("Transaction Fee|Basic Fee", na=False)]
        tr_fee_non_zero = tr_fee[tr_fee["quantity"] > 0]
        print(total_rows)
        am_without_vat_col = [col for col in total_rows.columns if "without VAT" in col][0]
        
        result["Total_with_VAT"] = clear_currency(total_rows[total_rows[am_without_vat_col].str.contains("incl. VAT", na=False)]["Total Amount"].iloc[0])
        result["VAT"] = clear_currency(total_rows[total_rows[am_without_vat_col].str.contains("VAT", na=False)]["Total Amount"].iloc[0])    
        result["Total_without_VAT"] = clear_currency(total_rows[total_rows[am_without_vat_col].str.contains("Total", na=False)]["Total Amount"].iloc[0])
        del result["table_data"]
    
        df = pd.DataFrame([result])
        df.to_csv("invoice_info.csv", index=False)
    else:
        print("Failed to process the invoice")



