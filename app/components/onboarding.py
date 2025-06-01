import streamlit as st
from typing import Optional, Tuple
from app.utils.profile_manager import ProfileManager

class OnboardingFlow:
    def __init__(self):
        """Initialize onboarding flow."""
        self.profile_manager = ProfileManager()
        
    def show(self) -> Optional[str]:
        """Display onboarding flow and return profile ID if completed."""
        st.title("Welcome to Project Woohoo! 🎙️")
        
        # Initialize step if not exists
        if "onboarding_step" not in st.session_state:
            st.session_state.onboarding_step = 1
            
        # Show progress
        st.progress(st.session_state.onboarding_step / 2)
        
        if st.session_state.onboarding_step == 1:
            completed, name = self._show_welcome()
            if completed:
                st.session_state.name = name
                st.session_state.onboarding_step = 2
                st.rerun()
        
        elif st.session_state.onboarding_step == 2:
            completed, interests = self._show_interests()
            if completed:
                # Create profile with default settings
                profile_id = self.profile_manager.create_profile(
                    name=st.session_state.name,
                    interests=interests,
                    learning_arcs=["ai_basics"],  # Default to AI basics
                    language="en",
                    voice_preference="enthusiastic"
                )
                
                if profile_id:
                    st.success("Profile created! Let's create your first episode...")
                    # Clean up onboarding state
                    for key in ["onboarding_step", "name"]:
                        if key in st.session_state:
                            del st.session_state[key]
                    return profile_id
                else:
                    st.error("Failed to create profile. Please try again.")
        
        return None
    
    def _show_welcome(self) -> Tuple[bool, str]:
        """Show welcome screen and get name."""
        st.markdown("""
        ### Transform Your Learning with AI-Powered Podcasts! 🚀
        
        Project Woohoo turns any text into engaging podcast episodes, 
        helping you learn while you listen. Perfect for articles, 
        documents, or any content you want to digest on the go.
        """)
        
        name = st.text_input(
            "What's your name?",
            placeholder="Enter your name to get started"
        )
        
        if st.button("Continue →", type="primary", disabled=not name):
            return True, name
        return False, ""
    
    def _show_interests(self) -> Tuple[bool, list]:
        """Show interests selection."""
        st.subheader("What interests you? 🤔")
        st.write("Choose at least 2 topics that excite you:")
        
        interests = st.multiselect(
            "Your Interests",
            options=self.profile_manager.available_interests,
            help="These will help us personalize your learning experience"
        )
        
        if st.button("Start Learning →", type="primary", disabled=len(interests) < 2):
            return True, interests
        return False, [] 