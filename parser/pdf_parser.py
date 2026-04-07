import pdfplumber #extract text &table from pdf
import re  #python regular expression, used for pattern matching

def extract_transactions_from_pdf(file):
        transactions = []
        with pdfplumber.open(file) as pdf: #pdf is now representing all pages in the file
                for page in pdf.pages:  #loop thru each pages
                        table = page.extract_table()   #attempt to extract table

                        if table:
                                for row in table[1:]:  #loops thru all row except header row
                                        try: 
                                                date = row[0].strip() if row[0] else None   #remove xtra space(.strip)
                                                desc = row[1].strip() if row[1] else ""
                                                amount = row[2].replace(",","").strip() if row[2] else None #if amt is 1,500 then return 1500

                                                if date and amount:  #appends a dictonary
                                                        transactions.append({
                                                                "date" : date, 
                                                                "description" : desc,
                                                                "amount" : float(amount)
                                                        })
                                        except Exception as e: #if any error occurs(eg column is missing,contains unexpected data),ignores that row and moves on
                                                continue
                        else:#if no table exists
                            text = page.extract_text()  #extract raw text
                            if text:
                                lines = text.split("\n") #split text into lines
                                for line in lines: #loop thru each line to find transaction pattern
                                        match = re.match(r"(\d{2}/\d{2}/\d{4})\s+(.*?)\s+([\d,]+\.\d{2})", line)
                                        if match:
                                                date,desc,amount = match.groups()
                                                transactions.append({
                                                        "date" : date,
                                                        "description" : desc,
                                                        "amount" : float(amount.replace(",",""))

                                                      })
        return transactions

