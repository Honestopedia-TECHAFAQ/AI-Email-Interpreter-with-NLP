import streamlit as st
import pandas as pd
import spacy
from word2number import w2n
from io import StringIO

nlp = spacy.load("en_core_web_sm")

def extract_email_data(email_content):
    doc = nlp(email_content)
    sender_email, sender_name, product_requested, quantity_requested, product_model, product_serial = None, None, None, None, None, None
    for ent in doc.ents:
        if ent.label_ == "EMAIL":
            sender_email = ent.text
        elif ent.label_ == "PERSON":
            sender_name = ent.text
    for token in doc:
        if token.text.lower() in ["battery", "lcd", "hard drive"]:
            product_requested = token.text
        if token.text.lower().startswith("cz"):
            product_model = token.text
        if token.text.isnumeric() and len(token.text) >= 5:
            product_serial = token.text
        try:
            if token.text.isdigit() or token.like_num:
                quantity_requested = w2n.word_to_num(token.text)
        except:
            pass

    return {
        "Sender Email": sender_email,
        "Sender Name": sender_name,
        "Product Requested": product_requested,
        "Quantity Requested": quantity_requested,
        "Product Model": product_model,
        "Product Serial": product_serial,
        "Part Number": get_part_number(product_model, product_serial),
    }
def get_part_number(model, serial):
    if model and serial:
        return f"PART-{model}-{serial[-4:]}"
    elif model:
        return f"PART-{model}-GEN"
    else:
        return None
def draft_email_response(data):
    if data["Sender Name"] and data["Product Requested"] and data["Part Number"]:
        return f"Hello {data['Sender Name']},\n\nThe part number for the requested {data['Product Requested']} (Model: {data['Product Model']}) is {data['Part Number']}.\n\nThanks,\nSupport Team"
    else:
        return "Unable to generate response due to missing data."
st.set_page_config(layout="wide", page_title="AI Email Interpreter")
with st.sidebar:
    st.title("AI Email Interpreter")
    st.markdown("**Options:**")
    task_option = st.selectbox("Select Task", ["Extract Data from Email", "Summary Dashboard"])
    st.markdown("---")
    st.write("**Customization:**")
    enable_error_log = st.checkbox("Show Error Log")
    st.markdown("---")
    st.info("Developed By Afaq Ahmad")
st.title("AI-Powered Email Interpreter")
st.markdown("This tool extracts parts information from emails and interacts with HPE Partsurfer to get accurate part numbers.")

if task_option == "Extract Data from Email":
    st.subheader("Step 1: Extract Data from Email Content")
    email_content = st.text_area("Paste the email content here", height=200)
    
    if st.button("Extract Data"):
        if email_content:
            try:
                extracted_data = extract_email_data(email_content)
                st.success("Data extracted successfully!")
                st.json(extracted_data)
                response = draft_email_response(extracted_data)
                st.subheader("Drafted Email Response")
                st.text_area("Automated Response", response, height=150)
                df = pd.DataFrame([extracted_data])
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(label="Download Extracted Data as CSV", data=csv, file_name="extracted_data.csv", mime="text/csv")
                
            except Exception as e:
                st.error(f"An error occurred while extracting data: {e}")
        else:
            st.warning("Please enter the email content.")
elif task_option == "Summary Dashboard":
    st.subheader("Step 2: Summary Dashboard")
    uploaded_file = st.file_uploader("Upload CSV file with Extracted Data for Dashboard", type="csv")
    
    if uploaded_file:
        try:
            results_df = pd.read_csv(uploaded_file)
            if not results_df.empty:
                st.success("Data loaded successfully for summary dashboard!")
                product_counts = results_df["Product Requested"].value_counts()
                st.bar_chart(product_counts)

        except Exception as e:
            st.error(f"An error occurred while loading data for dashboard: {e}")
if enable_error_log:
    st.sidebar.error("Error log is not implemented yet.")
