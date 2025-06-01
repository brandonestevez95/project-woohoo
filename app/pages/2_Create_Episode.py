import streamlit as st
from app.services.zotero_service import ZoteroService
from app.services.pdf_service import PDFService
from app.services.generator import Generator
from pathlib import Path
import os

def show_create_episode():
    st.title("Create Episode 🎙️")
    
    # Initialize step if not exists
    if "create_step" not in st.session_state:
        st.session_state.create_step = 1
    
    # Progress bar
    progress = st.progress(st.session_state.create_step / 3)
    
    # Step indicators
    cols = st.columns(3)
    with cols[0]:
        st.button("1. Add Sources", 
                 type="primary" if st.session_state.create_step == 1 else "secondary",
                 on_click=lambda: setattr(st.session_state, 'create_step', 1))
    with cols[1]:
        st.button("2. Configure Episode",
                 type="primary" if st.session_state.create_step == 2 else "secondary",
                 disabled=not st.session_state.get('selected_sources', []),
                 on_click=lambda: setattr(st.session_state, 'create_step', 2))
    with cols[2]:
        st.button("3. Generate",
                 type="primary" if st.session_state.create_step == 3 else "secondary",
                 disabled=not st.session_state.get('episode_config', {}),
                 on_click=lambda: setattr(st.session_state, 'create_step', 3))
    
    st.divider()
    
    # Step 1: Add Sources
    if st.session_state.create_step == 1:
        # Initialize services
        pdf_service = PDFService()
        
        # Create tabs for different source types
        source_tab, pdf_tab = st.tabs(["Zotero Library", "PDF Upload"])
        
        with source_tab:
            st.subheader("Zotero Library")
            
            # Zotero Configuration
            with st.expander("Zotero Configuration", expanded=not st.session_state.get('zotero_configured', False)):
                st.write("""
                To connect your Zotero library, you'll need:
                1. Your Zotero Library ID (found in your library settings)
                2. Your Zotero API Key (generate one at https://www.zotero.org/settings/keys)
                
                **How to find your Library ID:**
                1. Go to zotero.org and log in
                2. Click on your username in the top right
                3. Your Library ID is the number in your profile URL
                """)
                
                library_id = st.text_input("Zotero Library ID")
                api_key = st.text_input("Zotero API Key", type="password")
                
                if st.button("Connect to Zotero"):
                    if library_id and api_key:
                        try:
                            zotero_service = ZoteroService(library_id=library_id, api_key=api_key)
                            if zotero_service.test_connection():
                                st.session_state.zotero_library_id = library_id
                                st.session_state.zotero_api_key = api_key
                                st.session_state.zotero_configured = True
                                st.success("Successfully connected to Zotero!")
                                st.rerun()
                            else:
                                st.error("Could not connect to Zotero. Please check your credentials.")
                        except Exception as e:
                            st.error(f"Error connecting to Zotero: {str(e)}")
                    else:
                        st.warning("Please provide both Library ID and API Key")
            
            # Show Zotero content if configured
            if st.session_state.get('zotero_configured', False):
                try:
                    zotero_service = ZoteroService(
                        library_id=st.session_state.zotero_library_id,
                        api_key=st.session_state.zotero_api_key
                    )
                    
                    collections = zotero_service.get_collections()
                    if collections:
                        selected_collection = st.selectbox(
                            "Select Collection",
                            options=collections,
                            format_func=lambda x: x['data']['name']
                        )
                        
                        if selected_collection:
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
                                        
                                        if st.button(f"Add to Sources", key=f"add_{item['key']}"):
                                            st.session_state.setdefault('selected_sources', []).append(item)
                                            st.success("Added to selected sources!")
                except Exception as e:
                    st.error(f"Error accessing Zotero: {str(e)}")
                    st.session_state.zotero_configured = False
        
        with pdf_tab:
            st.subheader("Upload PDF")
            
            # Create upload directory if it doesn't exist
            upload_dir = Path("uploads")
            upload_dir.mkdir(exist_ok=True)
            
            uploaded_file = st.file_uploader(
                "Choose a PDF file",
                type=['pdf'],
                help="Upload a PDF file to use as a source"
            )
            
            if uploaded_file:
                try:
                    # Save the uploaded file
                    file_path = upload_dir / uploaded_file.name
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getvalue())
                    
                    # Extract text and metadata
                    text = pdf_service.extract_text(str(file_path))
                    metadata = pdf_service.get_metadata(str(file_path))
                    
                    # Display metadata
                    st.subheader("Document Information")
                    st.write(f"**Title:** {metadata.get('title', uploaded_file.name)}")
                    st.write(f"**Author:** {metadata.get('author', 'Unknown')}")
                    st.write(f"**Pages:** {metadata.get('pages', 0)}")
                    
                    # Display preview
                    with st.expander("Preview Content"):
                        st.write(text[:1000] + "..." if len(text) > 1000 else text)
                    
                    if st.button("Add to Sources"):
                        pdf_source = {
                            'type': 'pdf',
                            'path': str(file_path),
                            'metadata': metadata,
                            'text': text
                        }
                        st.session_state.setdefault('selected_sources', []).append(pdf_source)
                        st.success("PDF added to selected sources!")
                        
                except Exception as e:
                    st.error(f"Error processing PDF: {str(e)}")
                    if file_path.exists():
                        file_path.unlink()
        
        # Display selected sources
        if st.session_state.get('selected_sources', []):
            st.divider()
            st.subheader("Selected Sources")
            for idx, source in enumerate(st.session_state['selected_sources']):
                if source.get('type') == 'pdf':
                    with st.expander(f"📄 {source['metadata'].get('title', 'Unknown')}"):
                        st.write(f"**Author:** {source['metadata'].get('author', 'Unknown')}")
                        st.write(f"**Pages:** {source['metadata'].get('pages', 0)}")
                        if st.button("Remove", key=f"remove_pdf_{idx}"):
                            st.session_state['selected_sources'].pop(idx)
                            st.rerun()
                else:
                    with st.expander(f"📚 {source['data'].get('title', 'Untitled')}"):
                        st.write(f"**Type:** {source['data'].get('itemType', 'Unknown')}")
                        st.write(f"**Authors:** {', '.join([author.get('firstName', '') + ' ' + author.get('lastName', '') for author in source['data'].get('creators', [])])}")
                        if st.button("Remove", key=f"remove_zotero_{idx}"):
                            st.session_state['selected_sources'].pop(idx)
                            st.rerun()
            
            # Next step button
            if st.button("Next: Configure Episode ➡️", type="primary"):
                st.session_state.create_step = 2
                st.rerun()
    
    # Step 2: Configure Episode
    elif st.session_state.create_step == 2:
        st.subheader("Episode Configuration")
        
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Episode Title", 
                placeholder="Enter a title for your episode",
                value=st.session_state.get('episode_config', {}).get('title', ''))
            
            tone = st.selectbox(
                "Tone",
                options=["journalistic", "casual", "professional", "enthusiastic"],
                help="Choose the tone of voice for your episode",
                index=["journalistic", "casual", "professional", "enthusiastic"].index(
                    st.session_state.get('episode_config', {}).get('tone', 'professional')
                )
            )
        
        with col2:
            duration = st.slider(
                "Target Duration (minutes)",
                min_value=5,
                max_value=30,
                value=st.session_state.get('episode_config', {}).get('duration', 15),
                help="Choose the target duration for your episode"
            )
            
            if "profile_id" in st.session_state:
                profile = st.session_state.get("profile", {})
                language = profile.get("language", "en")
            else:
                language = "en"
        
        # Save configuration
        if st.button("Save Configuration", type="primary"):
            if not title:
                st.error("Please enter an episode title.")
            else:
                st.session_state['episode_config'] = {
                    'title': title,
                    'tone': tone,
                    'duration': duration,
                    'language': language
                }
                st.success("Configuration saved!")
                st.session_state.create_step = 3
                st.rerun()
        
        # Back button
        if st.button("⬅️ Back to Sources"):
            st.session_state.create_step = 1
            st.rerun()
    
    # Step 3: Generate Episode
    elif st.session_state.create_step == 3:
        st.subheader("Generate Episode")
        
        # Show configuration summary
        config = st.session_state['episode_config']
        st.write("**Episode Title:** ", config['title'])
        st.write("**Tone:** ", config['tone'])
        st.write("**Duration:** ", f"{config['duration']} minutes")
        
        # Show selected sources
        st.write("**Selected Sources:**")
        for source in st.session_state['selected_sources']:
            if source.get('type') == 'pdf':
                st.write(f"📄 {source['metadata'].get('title', 'Unknown PDF')}")
            else:
                st.write(f"📚 {source['data'].get('title', 'Unknown Source')}")
        
        # Generate button
        if st.button("Generate Episode", type="primary"):
            with st.spinner("Generating your episode... This may take a few minutes."):
                try:
                    generator = Generator()
                    result = generator.generate_episode(
                        sources=st.session_state['selected_sources'],
                        title=config['title'],
                        tone=config['tone'],
                        duration_minutes=config['duration'],
                        language=config['language']
                    )
                    
                    if result:
                        st.success("Episode generated successfully!")
                        
                        # Display episode details
                        st.header("Episode Details")
                        st.subheader(result["title"])
                        st.write(result["summary"])
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.audio(result["audio_path"])
                        with col2:
                            st.download_button(
                                "Download Audio",
                                open(result["audio_path"], "rb"),
                                file_name=f"{config['title'].lower().replace(' ', '_')}.mp3",
                                mime="audio/mpeg"
                            )
                            st.download_button(
                                "Download Transcript",
                                open(result["transcript_path"], "r").read(),
                                file_name=f"{config['title'].lower().replace(' ', '_')}.txt",
                                mime="text/plain"
                            )
                    else:
                        st.error("Failed to generate episode. Please try again.")
                except Exception as e:
                    st.error(f"Error generating episode: {str(e)}")
        
        # Back button
        if st.button("⬅️ Back to Configuration"):
            st.session_state.create_step = 2
            st.rerun()
        
        # Start over button
        if st.button("Start Over"):
            st.session_state.pop('episode_config', None)
            st.session_state.pop('selected_sources', None)
            st.session_state.create_step = 1
            st.rerun()

if __name__ == "__main__":
    show_create_episode() 