import os
import requests
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import datetime

# Carregar variáveis de ambiente
load_dotenv()
GROK_API_KEY = os.getenv('GROK_API_KEY')

class SMEInvoiceAutomator:
    def __init__(self, company_name, company_address, vat_rate=0.075):
        self.company_name = company_name
        self.company_address = company_address
        self.vat_rate = vat_rate  # VAT padrão na Nigéria é 7.5%

    def generate_description(self, item_name):
        """Usa Grok API para gerar uma descrição profissional do item."""
        url = "https://api.x.ai/v1/chat/completions"  # Endpoint da API Grok
        headers = {
            "Authorization": f"Bearer {GROK_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "grok-beta",
            "messages": [
                {"role": "system", "content": "Você é um assistente que gera descrições profissionais para itens em faturas de SMEs nigerianas."},
                {"role": "user", "content": f"Gere uma descrição curta e profissional para o item: {item_name}"}
            ]
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content'].strip()
        else:
            return f"Descrição padrão para {item_name}"  # Fallback se API falhar

    def create_invoice(self, customer_name, customer_email, items):
        """Gera a fatura com cálculos e PDF."""
        invoice_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        total = 0
        invoice_data = {
            "id": invoice_id,
            "date": datetime.date.today().strftime("%d/%m/%Y"),
            "items": [],
            "subtotal": 0,
            "vat": 0,
            "total": 0
        }

        for item in items:
            name, qty, price = item
            desc = self.generate_description(name)
            subtotal = qty * price
            total += subtotal
            invoice_data["items"].append({"name": name, "desc": desc, "qty": qty, "price": price, "subtotal": subtotal})

        invoice_data["subtotal"] = total
        invoice_data["vat"] = total * self.vat_rate
        invoice_data["total"] = total + invoice_data["vat"]

        # Gerar PDF
        pdf_filename = f"invoice_{invoice_id}.pdf"
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        c.drawString(100, 750, self.company_name)
        c.drawString(100, 735, self.company_address)
        c.drawString(100, 700, f"Fatura ID: {invoice_id}")
        c.drawString(100, 685, f"Data: {invoice_data['date']}")
        c.drawString(100, 670, f"Cliente: {customer_name}")

        y = 650
        for item in invoice_data["items"]:
            c.drawString(100, y, f"{item['name']} - {item['desc']}")
            c.drawString(400, y, f"Qtd: {item['qty']} | Preço: ₦{item['price']} | Subtotal: ₦{item['subtotal']}")
            y -= 20

        c.drawString(100, y-20, f"Subtotal: ₦{invoice_data['subtotal']}")
        c.drawString(100, y-40, f"VAT (7.5%): ₦{invoice_data['vat']}")
        c.drawString(100, y-60, f"Total: ₦{invoice_data['total']}")
        c.save()

        return pdf_filename, invoice_data

    def send_invoice(self, customer_email, pdf_filename, sender_email, sender_password):
        """Envia a fatura por e-mail (opcional)."""
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = customer_email
        msg['Subject'] = "Sua Fatura da Empresa"

        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(pdf_filename, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={pdf_filename}')
        msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, customer_email, msg.as_string())
        server.quit()

# Exemplo de uso
if __name__ == "__main__":
    agent = SMEInvoiceAutomator("Minha SME Nigeriana Ltd", "Endereço em Lagos, Nigéria")
    items = [
        ("Camisa", 5, 2000),
        ("Calça", 3, 3000)
    ]
    pdf, data = agent.create_invoice("Cliente Exemplo", "cliente@email.com", items)
    print(f"Fatura gerada: {pdf}")
    # Para enviar: agent.send_invoice("cliente@email.com", pdf, "meu@gmail.com", "minha-senha-app")