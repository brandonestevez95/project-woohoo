import streamlit as st
from services.zotero_service import ZoteroService
from services.pdf_service import PDFService
import os
from pathlib import Path

def display_sources():
    st.title("Sources")
    
    # Initialize services
    zotero_service = ZoteroService()
    pdf_service = PDFService()
    
    # Create tabs for different source types
    source_tab, pdf_tab = st.tabs(["Zotero Library", "PDF Upload"])
    
    with source_tab:
        st.header("Zotero Library")
        if not zotero_service.is_configured():
            st.warning("Please configure your Zotero credentials in Settings first.")
            return
        
        # Get collections
        collections = zotero_service.get_collections()
        if collections:
            selected_collection = st.selectbox(
                "Select Collection",
                options=collections,
                format_func=lambda x: x['data']['name']
            )
            
            if selected_collection:
                # Get items in collection
                items = zotero_service.get_items_in_collection(selected_collection['key'])
                if items:
                    st.write(f"Found {len(items)} items in collection")
                    for item in items:
                        with st.expander(f"{item['data'].get('title', 'Untitled')}"):
                            st.write(f"**Type:** {item['data'].get('itemType', 'Unknown')}")
                            st.write(f"**Authors:** {', '.join([author.get('firstName', '') + ' ' + author.get('lastName', '') for author in item['data'].get('creators', [])])}")
                            if 'abstractNote' in item['data']:
                                st.write("**Abstract:**")
                                st.write(item['data']['abstractNote'])
                            
                            # Add citation button
                            if st.button(f"Add to Sources", key=f"add_{item['key']}"):
                                st.session_state.setdefault('selected_sources', []).append(item)
                                st.success("Added to selected sources!")
    
    with pdf_tab:
        st.header("Upload PDF")
        uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])
        
        if uploaded_file:
            # Save the uploaded file
            file_path = pdf_service.save_uploaded_file(uploaded_file)
            
            # Extract text and metadata
            text = pdf_service.extract_text(file_path)
            metadata = pdf_service.get_metadata(file_path)
            
            # Display metadata
            st.subheader("Document Information")
            st.write(f"**Title:** {metadata.get('title', 'Unknown')}")
            st.write(f"**Author:** {metadata.get('author', 'Unknown')}")
            st.write(f"**Pages:** {metadata.get('pages', 0)}")
            
            # Display preview
            with st.expander("Preview Content"):
                st.write(text[:1000] + "..." if len(text) > 1000 else text)
            
            # Add to sources
            if st.button("Add to Sources"):
                pdf_source = {
                    'type': 'pdf',
                    'path': file_path,
                    'metadata': metadata,
                    'text': text
                }
                st.session_state.setdefault('selected_sources', []).append(pdf_source)
                st.success("PDF added to selected sources!")
    
    # Display selected sources
    if 'selected_sources' in st.session_state and st.session_state['selected_sources']:
        st.header("Selected Sources")
        for idx, source in enumerate(st.session_state['selected_sources']):
            if isinstance(source, dict) and source.get('type') == 'pdf':
                with st.expander(f"PDF: {source['metadata'].get('title', 'Unknown')}"):
                    st.write(f"**Author:** {source['metadata'].get('author', 'Unknown')}")
                    st.write(f"**Pages:** {source['metadata'].get('pages', 0)}")
                    if st.button("Remove", key=f"remove_pdf_{idx}"):
                        st.session_state['selected_sources'].pop(idx)
                        st.rerun()
            else:
                with st.expander(f"Zotero: {source['data'].get('title', 'Untitled')}"):
                    st.write(f"**Type:** {source['data'].get('itemType', 'Unknown')}")
                    st.write(f"**Authors:** {', '.join([author.get('firstName', '') + ' ' + author.get('lastName', '') for author in source['data'].get('creators', [])])}")
                    if st.button("Remove", key=f"remove_zotero_{idx}"):
                        st.session_state['selected_sources'].pop(idx)
                        st.rerun()

if __name__ == "__main__":
    display_sources() 