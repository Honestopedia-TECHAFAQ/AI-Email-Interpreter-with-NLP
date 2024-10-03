import base64
import streamlit as st
import pandas as pd
import spacy
from word2number import w2n
import io

# Attempt to load the SpaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    st.error("SpaCy model 'en_core_web_sm' not found. Please ensure it's installed.")
    nlp = None  # Set nlp to None if model is not found

# Streamlit app starts here
st.title("AI Email Interpreter for IT Parts")

# Sidebar options
st.sidebar.title("Options")
upload_choice = st.sidebar.radio("Choose an action:", ["Extract Data from Email", "Download Results"])

# Input section
if upload_choice == "Extract Data from Email":
    email_content = st.text_area("Paste the email content here:")
    
    if st.button("Extract Data"):
        if nlp is not None:
            doc = nlp(email_content)
            extracted_data = {
                "Sender": "example@example.com",  # Placeholder
                "Product Requested": "battery",    # Placeholder
                "Quantity": 1,                     # Placeholder
                "Model": "XYZ-123",                # Placeholder
                "Serial": "SN-456",                # Placeholder
            }
            st.success("Data extracted successfully!")
            st.json(extracted_data)
        else:
            st.warning("NLP processing is not available without the SpaCy model.")

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

# Run the app
if __name__ == "__main__":
    st.run()
