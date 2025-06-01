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
        st.progress(st.session_state.onboarding_step / 3)
        
        if st.session_state.onboarding_step == 1:
            completed, name = self._show_welcome()
            if completed:
                st.session_state.name = name
                st.session_state.onboarding_step = 2
                st.rerun()
        
        elif st.session_state.onboarding_step == 2:
            completed, (interests, arcs) = self._show_interests()
            if completed:
                st.session_state.interests = interests
                st.session_state.learning_arcs = arcs
                st.session_state.onboarding_step = 3
                st.rerun()
        
        elif st.session_state.onboarding_step == 3:
            completed, (language, voice) = self._show_preferences()
            if completed:
                # Create profile
                profile_id = self.profile_manager.create_profile(
                    name=st.session_state.name,
                    interests=st.session_state.interests,
                    learning_arcs=st.session_state.learning_arcs,
                    language=language,
                    voice_preference=voice
                )
                
                if profile_id:
                    st.success("Profile created successfully! Redirecting to main interface...")
                    # Clean up ALL onboarding state
                    keys_to_remove = [
                        "onboarding_step",
                        "name",
                        "interests",
                        "learning_arcs"
                    ]
                    for key in keys_to_remove:
                        if key in st.session_state:
                            del st.session_state[key]
                    return profile_id
                else:
                    st.error("Failed to create profile. Please try again.")
        
        return None
    
    def _show_welcome(self) -> Tuple[bool, str]:
        """Show welcome screen and get name."""
        st.write("""
        Welcome to Project Woohoo, your AI-powered podcast generator! 🎙️
        
        Let's get you set up with a personalized learning experience. This will only take a few minutes.
        """)
        
        name = st.text_input("What should we call you?", 
            placeholder="Enter your name")
        
        if st.button("Continue", type="primary", disabled=not name):
            return True, name
        return False, ""
    
    def _show_interests(self) -> Tuple[bool, Tuple[list, list]]:
        """Show interests and learning paths selection."""
        st.subheader("Choose Your Interests & Learning Paths")
        
        # Select interests
        interests = st.multiselect(
            "Select your interests (choose at least 2)",
            options=self.profile_manager.available_interests,
            help="These topics will help us personalize your podcast content"
        )
        
        st.write("---")
        
        # Select learning paths
        st.write("Choose at least one learning path:")
        arcs = []
        for arc in self.profile_manager.available_learning_arcs:
            col1, col2 = st.columns([1, 3])
            with col1:
                if st.checkbox(arc["name"], key=f"arc_{arc['id']}"):
                    arcs.append(arc["id"])
            with col2:
                st.write(f"*{arc['description']}*")
                st.write(f"Difficulty: {arc['difficulty']}")
        
        if st.button("Continue", type="primary", disabled=not (len(interests) >= 2 and len(arcs) >= 1)):
            return True, (interests, arcs)
        return False, ([], [])
    
    def _show_preferences(self) -> Tuple[bool, Tuple[str, str]]:
        """Show language and voice preferences."""
        st.subheader("Almost Done!")
        
        language = st.selectbox(
            "Preferred Language",
            options=[
                ("en", "English"),
                ("es", "Spanish"),
                ("fr", "French"),
                ("de", "German")
            ],
            format_func=lambda x: x[1]
        )[0]
        
        voice = st.selectbox(
            "Voice Style",
            options=[
                "default",
                "casual",
                "professional",
                "enthusiastic"
            ]
        )
        
        if st.button("Complete Setup", type="primary"):
            return True, (language, voice)
        return False, ("en", "default") 