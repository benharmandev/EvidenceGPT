import streamlit as st
from subprocess import run
import utils

# Define the main function to run the Streamlit app
def main():
    # Set the page title
    st.set_page_config(page_title="PDF Source Viewer")

    # Set the page header
    st.header("PDF Source Viewer")

    # Create a file uploader for PDF files
    uploaded_files = st.file_uploader("Upload PDF Files", type="pdf", accept_multiple_files=True)

    # Add an "Add Sources" button
    add_sources_button = st.button("Add Sources")

    if add_sources_button:
        utils.create_source_objects(uploaded_files)
        print(utils.sources)
        print(utils.summarize_sources(utils.sources))

        for source in utils.sources:
            # Create a card for each source using expander
            with st.expander(f"Source: {source.filename}"):
                # Display filename (not editable)
                st.markdown(f"**Filename:** {source.filename}")

                # Display other source information in editable fields
                title = st.text_input("Title", value=source.title)
                author = st.text_input("Author", value=source.author)
                date = st.text_input("Date", value=source.date)
                description = st.text_area("Description", value=source.description)
                publisher = st.text_input("Publisher", value=source.publisher)

                # Update the source object with the new values
                source.title = title
                source.author = author
                source.date = date
                source.description = description
                source.publisher = publisher

if __name__ == "__main__":
    main()
