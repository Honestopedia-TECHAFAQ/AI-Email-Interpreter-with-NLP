import streamlit as st
import pandas as pd
import re
import io
import base64

# Function to extract information from email content
def extract_email_info(email_content):
    # Basic regex to extract sender, product requested, quantity, model, and serial number.
    # Placeholder values for demonstration
    sender = re.findall(r'From: (.+)', email_content)
    product = re.findall(r'Product Requested: (.+)', email_content)
    quantity = re.findall(r'Quantity: (\d+)', email_content)
    model = re.findall(r'Model: (.+)', email_content)
    serial = re.findall(r'Serial: (.+)', email_content)

    return {
        "Sender": sender[0] if sender else "Not found",
        "Product Requested": product[0] if product else "Not found",
        "Quantity": int(quantity[0]) if quantity else 0,
        "Model": model[0] if model else "Not found",
        "Serial": serial[0] if serial else "Not found",
    }

# Streamlit app starts here
st.title("AI Email Interpreter for IT Parts")

# Sidebar options
st.sidebar.title("Options")
upload_choice = st.sidebar.radio("Choose an action:", ["Extract Data from Email", "Download Results"])

# Input section
if upload_choice == "Extract Data from Email":
    email_content = st.text_area("Paste the email content here:")
    
    if st.button("Extract Data"):
        if email_content:
            extracted_data = extract_email_info(email_content)
            st.success("Data extracted successfully!")
            st.json(extracted_data)

        else:
            st.warning("Please enter email content.")

elif upload_choice == "Download Results":
    # Logic for downloading results as CSV
    results_df = pd.DataFrame({
        "Sender": ["example@example.com"],
        "Product Requested": ["battery"],
        "Quantity": [1],
        "Model": ["XYZ-123"],
        "Serial": ["SN-456"]
    })
    
    # Download as CSV
    csv = results_df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # Convert to base64
    href = f'<a href="data:file/csv;base64,{b64}" download="results.csv">Download Results</a>'
    st.markdown(href, unsafe_allow_html=True)

# Note: No need for `st.run()` in Streamlit script; simply put your logic at the top level.
