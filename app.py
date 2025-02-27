import streamlit as st
import PyPDF2
from io import BytesIO
from PyPDF2 import PageObject  # For PyPDF2 v2.x
from PyPDF2 import Transformation  # For PyPDF2 v3.x

def add_margin_to_pdf(pdf_stream, left, right, top, bottom):
    input_pdf = PyPDF2.PdfReader(pdf_stream)
    output_pdf = PyPDF2.PdfWriter()
    
    for page_num in range(len(input_pdf.pages)):
        page = input_pdf.pages[page_num]
        orig_width = float(page.mediabox.width)
        orig_height = float(page.mediabox.height)
        
        new_width = orig_width + left + right
        new_height = orig_height + top + bottom
        
        # Create a new blank page with new dimensions
        new_page = PageObject.create_blank_page(width=new_width, height=new_height)
        
        # Move original content to fit within new margins
        transformation = Transformation().translate(tx=left, ty=bottom)
        page.add_transformation(transformation)
        
        # Merge the original page onto the new blank page
        new_page.merge_page(page)
        output_pdf.add_page(new_page)
    
    output_stream = BytesIO()
    output_pdf.write(output_stream)
    output_stream.seek(0)
    return output_stream

# Streamlit UI
#st.title("PDF Margin Editor")


st.markdown("<h1 style='text-align: center;'>PDF Margin Editor</h1>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    left_margin = st.number_input("Left Margin (pts)", min_value=0, value=10)
    right_margin = st.number_input("Right Margin (pts)", min_value=0, value=10)
    top_margin = st.number_input("Top Margin (pts)", min_value=0, value=10)
    bottom_margin = st.number_input("Bottom Margin (pts)", min_value=0, value=10)
    
    if st.button("Apply Margins"):
        new_pdf = add_margin_to_pdf(uploaded_file, left_margin, right_margin, top_margin, bottom_margin)
        st.success("Margins updated successfully!")
        st.download_button(label="Download Modified PDF", data=new_pdf, file_name="modified.pdf", mime="application/pdf")
