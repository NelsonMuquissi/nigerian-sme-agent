SME Invoice Automator
Overview
The SME Invoice Automator is an AI-powered tool designed to streamline invoicing for Nigerian Small and Medium Enterprises (SMEs). Built for the Agents Hackathon – Nigeria, it automates the creation of professional invoices, calculates taxes, generates PDFs, and optionally sends invoices via email. By leveraging AI, it enhances item descriptions, making invoices clear and professional, saving time, and reducing errors for Nigerian businesses.
Features

Automated Invoice Creation: Generates invoices with company details, customer information, and itemized lists (including quantities and prices).
Tax Calculation: Automatically calculates Nigeria's 7.5% VAT and provides subtotal and total amounts.
AI-Powered Descriptions: Uses the Grok API (xAI) to generate professional item descriptions for invoices.
PDF Generation: Creates formatted PDF invoices using the ReportLab library.
Email Automation (Optional): Sends invoices directly to customers via email (e.g., using Gmail SMTP).
Impact: Reduces manual invoicing time by up to 80%, minimizes errors, and enhances professionalism for SMEs.

Prerequisites

Python 3.x
Libraries: reportlab, requests, python-dotenv
Grok API Key (sign up at https://x.ai/api)
(Optional) Email account with SMTP settings for sending invoices

Installation

Clone this repository:git clone <https://github.com/NelsonMuquissi/nigerian-sme-agent.git>
cd sme_invoice_automator


Create and activate a virtual environment:python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows


Install dependencies:pip install reportlab requests python-dotenv


Create a .env file in the project root and add your Grok API key:



Usage

Run the script:python invoice_automator.py


The script generates a sample invoice PDF (invoice_[ID].pdf) based on predefined items.
Customize the script by editing the items list in invoice_automator.py:items = [
    ("Shirt", 5, 2000),  # Item name, quantity, price in Naira
    ("Trousers", 3, 3000)
]


(Optional) Enable email sending by uncommenting the send_invoice call and providing your email credentials (use an app-specific password for Gmail).

Output

A PDF invoice with:
Company name and address
Invoice ID and date
Customer name
Itemized list with AI-generated descriptions
Subtotal, VAT (7.5%), and total


(Optional) Email delivery to the customer with the PDF attached.

Impact for Nigerian SMEs

Time-Saving: Automates repetitive invoicing tasks, freeing up time for business owners.
Error Reduction: Ensures accurate VAT calculations and consistent formatting.
Professionalism: AI-generated descriptions make invoices polished and customer-friendly.
Scalability: Easily adapts to various SME needs, from retail to service-based businesses.

Demo

Run the script to generate a sample PDF invoice in the project directory.
Check the invoice_20250915112818.pdf file for the output.
(Optional) Record a video demo showing the script execution and PDF output.

Submission Details
This project was developed for the Agents Hackathon – Nigeria (submission deadline: September 15, 2025, 12:00 PM WAT). It addresses the hackathon's goal of automating business processes for Nigerian SMEs, delivering tangible value through AI-driven efficiency.
License
MIT License