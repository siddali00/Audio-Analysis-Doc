import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Define the backend endpoint
# BACKEND_API_URL = "http://127.0.0.1:8080/speech_analysis"  # Replace with your backend URL if hosted elsewhere

BACKEND_API_URL = os.getenv('BACKEND_API_URL')

# Streamlit app
st.title("Audio Analysis App")
st.markdown("""
Upload your audio file and (optionally) provide a CSV link to get a summary and an updated Google Sheet link.
""")

# Upload audio file
audio_file = st.file_uploader("Upload your audio file (MP3, OGG, or WAV)", type=["mp3", "ogg", "wav"])

# Select language
language = st.selectbox("Select the target language", options=["en", "ar"])

email_link = st.text_input("Provide the Google Sheet link for emails of relevant personnel.")
# Optional CSV link
csv_link = st.text_input("Provide the Google Sheet link (optional)")

# Submit button
if st.button("Analyze Audio"):
    if not audio_file:
        st.error("Please upload an audio file.")
    else:
        # Prepare the payload
        files = {"file": audio_file.getvalue()}
        data = {"language": language}
        if email_link:
            data["email"] =email_link
        if csv_link:
            data["csv"] = csv_link

        st.info("Processing your request... This may take some time.")

        # Send the request to the backend
        try:
            response = requests.post(
                BACKEND_API_URL,
                files={"file": (audio_file.name, audio_file, audio_file.type)},
                data=data
            )

            # Process the response
            if response.status_code == 200:
                result = response.json()
                st.success("Analysis Complete!")
                
                # Display the results
                st.markdown("### Summary")
                st.write(result.get("summary", "No summary provided"))

                st.markdown("### Google Sheet URL")
                sheet_url = result.get("google_sheet_url", "No URL provided")
                st.write(f"[View Google Sheet]({sheet_url})")
                st.markdown("### Docs URL")
                doc_url = result.get("google_doc_url", "No URL provided")
                st.write(f"[View Google Doc]({doc_url})")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
