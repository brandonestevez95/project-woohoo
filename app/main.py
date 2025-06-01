import streamlit as st
from app.components.onboarding import OnboardingFlow
from app.utils.profile_manager import ProfileManager

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
    
    # Simple upload section
    uploaded_file = st.file_uploader("Upload your first document (PDF)", type=["pdf"])
    if uploaded_file:
        st.success("Document uploaded successfully!")
        if st.button("Generate My First Episode", type="primary"):
            with st.spinner("Creating your personalized episode..."):
                st.balloons()
                st.success("Your first episode is ready!")

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