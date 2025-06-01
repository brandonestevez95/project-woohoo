import streamlit as st
from app.components.onboarding import OnboardingFlow
from app.utils.profile_manager import ProfileManager
from app.utils.pdf_processor import PDFProcessor

# Configure Streamlit page
st.set_page_config(
    page_title="Project Woohoo",
    page_icon="🎙️",
    layout="wide"
)

def show_first_episode(profile):
    st.title(f"Welcome to Project Woohoo, {profile['name']}! 🎙️")
    
    st.markdown("""
    ### How Project Woohoo Works 🚀
    
    1. **Choose Your Content**: Upload a PDF or paste text you want to learn about
    2. **AI Magic**: Our AI transforms your content into an engaging podcast
    3. **Listen & Learn**: Get personalized episodes based on your interests
    
    Let's create your first episode!
    """)
    
    with st.expander("✨ Pro Tips", expanded=True):
        st.markdown("""
        - Start with a short article or document (2-3 pages)
        - Choose topics aligned with your interests
        - Listen to the generated episode and provide feedback
        """)
    
    st.divider()
    
    # Initialize PDF processor
    pdf_processor = PDFProcessor()
    
    # Simple upload section
    uploaded_file = st.file_uploader("Upload your first document (PDF)", type=["pdf"])
    if uploaded_file:
        st.success("Document uploaded successfully!")
        
        # Process the PDF
        with st.spinner("Analyzing your document..."):
            doc_info = pdf_processor.process_uploaded_file(uploaded_file)
            
            if doc_info:
                # Show document info
                st.subheader("📄 Document Overview")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Pages", doc_info["metadata"]["num_pages"])
                with col2:
                    st.metric("Sections", len(doc_info["sections"]))
                with col3:
                    size_mb = round(doc_info["metadata"]["file_size"] / (1024 * 1024), 2)
                    st.metric("Size", f"{size_mb} MB")
                
                # Show sections
                st.subheader("📚 Document Structure")
                for section in doc_info["sections"]:
                    if section["title"]:
                        with st.expander(f"📝 {section['title']}", expanded=False):
                            st.write(section["content"][:500] + "..." if len(section["content"]) > 500 else section["content"])
                
                # Generate episode button
                if st.button("Generate My First Episode", type="primary"):
                    with st.spinner("Creating your personalized episode..."):
                        # Show preview of transformation
                        st.subheader("🎯 Preview of Podcast Transformation")
                        
                        # Example preview tabs
                        preview_tab1, preview_tab2 = st.tabs(["Original Text", "Podcast Style"])
                        
                        with preview_tab1:
                            # Show first 1000 characters of original text
                            st.markdown("### Original Academic Text")
                            st.markdown(doc_info["full_text"][:1000] + "...")
                        
                        with preview_tab2:
                            # Show example of how it would be transformed
                            st.markdown("### Transformed for Podcast")
                            st.markdown("""
                            🎙️ *Welcome to today's episode! Today, we're diving into an fascinating study about developing intercultural competence in agricultural education.*
                            
                            In our increasingly diverse world, preparing teachers to connect with students from all backgrounds is crucial. This study tackles this challenge head-on, exploring how we can better equip future agricultural education teachers with the skills they need.
                            
                            Let's break down what the researchers discovered:
                            
                            1. First, they found that focused training in diversity and cultural awareness makes a real difference
                            2. The study used a mixed-methods approach, combining both numbers and real experiences
                            3. Most importantly, they uncovered specific strategies that work...
                            
                            *[This is a preview of how the content would be transformed into engaging podcast format]*
                            """)
                        
                        st.balloons()
                        st.success("Your first episode is ready!")
                        
                        # Show next steps
                        st.info("""
                        🎉 **Coming Soon:**
                        - AI-powered content transformation
                        - Text-to-speech conversion
                        - Interactive episode player
                        """)

def main():
    # Initialize profile manager
    profile_manager = ProfileManager()

    # Check for active profile
    if "profile_id" not in st.session_state:
        onboarding = OnboardingFlow()
        profile_id = onboarding.show()
        if profile_id:
            st.session_state.profile_id = profile_id
            st.rerun()
    else:
        # Load active profile
        profile = profile_manager.get_profile(st.session_state.profile_id)
        if not profile:
            st.session_state.pop("profile_id")
            st.rerun()
        else:
            show_first_episode(profile)

if __name__ == "__main__":
    main() 