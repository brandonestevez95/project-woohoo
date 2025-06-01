import streamlit as st
from app.components.onboarding import OnboardingFlow
from app.utils.profile_manager import ProfileManager

# Configure Streamlit page
st.set_page_config(
    page_title="Project Woohoo",
    page_icon="🎙️",
    layout="wide"
)

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
            # Main content
            st.title(f"Welcome back, {profile['name']}! 👋")
            
            # Tabs for navigation
            tab1, tab2, tab3 = st.tabs(["Create Episode", "Library", "Settings"])
            
            with tab1:
                st.header("Create New Episode 🎙️")
                st.write("Let's create your first AI-powered podcast episode!")
                
                # Source selection
                st.subheader("Step 1: Add Sources")
                source_type = st.selectbox(
                    "Choose your source type",
                    ["Upload PDF", "Zotero Library"]
                )
                
                if source_type == "Upload PDF":
                    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
                    if uploaded_file:
                        st.success("PDF uploaded successfully!")
                        st.button("Process PDF", type="primary")
                else:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.text_input("Zotero Library ID")
                    with col2:
                        st.text_input("API Key", type="password")
                    if st.button("Connect to Zotero", type="primary"):
                        st.info("Connecting to Zotero...")
            
            with tab2:
                st.header("Your Episode Library 🎧")
                st.info("Your generated episodes will appear here. Create your first episode to get started!")
            
            with tab3:
                st.header("Settings ⚙️")
                
                # Profile settings
                st.subheader("Profile Settings")
                st.text_input("Name", value=profile['name'])
                st.selectbox(
                    "Language",
                    options=[("en", "English"), ("es", "Spanish"), ("fr", "French"), ("de", "German")],
                    format_func=lambda x: x[1],
                    index=0 if profile['language'] == 'en' else None
                )
                st.selectbox(
                    "Voice Style",
                    options=["default", "casual", "professional", "enthusiastic"],
                    index=["default", "casual", "professional", "enthusiastic"].index(profile['voice_preference'])
                )
                
                # Danger zone
                st.divider()
                st.subheader("Danger Zone")
                if st.button("Reset Profile", type="secondary"):
                    if st.checkbox("I understand this will delete my profile"):
                        st.session_state.pop("profile_id")
                        st.rerun()

if __name__ == "__main__":
    main() 