import aiofiles
import os
import uuid
import urllib
import mistune
from pathlib import Path

async def write_to_file(filename: str, text: str) -> None:
    """Asynchronously write text to a file in UTF-8 encoding."""
    text_utf8 = text.encode('utf-8', errors='replace').decode('utf-8')
    async with aiofiles.open(filename, "w", encoding='utf-8') as file:
        await file.write(text_utf8)

async def write_text_to_md(text: str, path: str) -> str:
    """Writes text to a Markdown file and returns the file path."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    file_path = path / f"{uuid.uuid4().hex}.md"
    await write_to_file(file_path, text)
    print(f"Markdown report written to {file_path}")
    return str(file_path)
import base64
import streamlit as st
def display_pdf(file_path):
    """Embed a PDF in Streamlit using an HTML iframe."""
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
async def write_md_to_pdf(text: str, path: str) -> str:
    """Converts Markdown text to a PDF file and returns the file path."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    file_path = path / f"{uuid.uuid4().hex}.pdf"
    if ".md" in text:
        md_file_path = Path(text)
        if not md_file_path.exists() or not md_file_path.is_file():
            return(f"Markdown file {md_file_path} does not exist.")
        with open(md_file_path, 'r') as f:
            md_content = f.read()
    else:
        md_content = text
    try:
        from md2pdf.core import md2pdf
        css_path = Path("pdf_styles.css")
        md2pdf(file_path, md_content=md_content, css_file_path=css_path if css_path.exists() else None)
        print(f"PDF report written to {file_path}")
    except Exception as e:
        print(f"Error converting Markdown to PDF: {e})")
    return f"PDF report written and saved in {file_path}."

async def write_md_to_word(text: str, path: str) -> str:
    """Converts Markdown text to a DOCX file and returns the file path."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    file_path = path / f"{uuid.uuid4().hex}.docx"
    try:
        from htmldocx import HtmlToDocx
        from docx import Document
        html = mistune.create_markdown()(text)
        doc = Document()
        HtmlToDocx().add_html_to_document(html, doc)
        doc.save(file_path)
        print(f"DOCX report written to {file_path}")
    except Exception as e:
        print(f"Error converting Markdown to DOCX: {e}")
        return ""
    return urllib.parse.quote(str(file_path))
