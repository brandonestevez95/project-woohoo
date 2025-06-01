import streamlit as st
from typing import Optional, Tuple
from ..utils.profile_manager import ProfileManager

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
        st.progress(st.session_state.onboarding_step / 4)
        
        if st.session_state.onboarding_step == 1:
            completed = self._show_welcome()
            if completed:
                st.session_state.onboarding_step = 2
                st.rerun()
                
        elif st.session_state.onboarding_step == 2:
            completed, profile_name = self._show_profile_setup()
            if completed:
                st.session_state.profile_name = profile_name
                st.session_state.onboarding_step = 3
                st.rerun()
                
        elif st.session_state.onboarding_step == 3:
            completed, (interests, arcs) = self._show_interests()
            if completed:
                st.session_state.interests = interests
                st.session_state.learning_arcs = arcs
                st.session_state.onboarding_step = 4
                st.rerun()
                
        elif st.session_state.onboarding_step == 4:
            completed, (language, voice) = self._show_preferences()
            if completed:
                # Create profile
                profile_id = self.profile_manager.create_profile(
                    name=st.session_state.profile_name,
                    interests=st.session_state.interests,
                    learning_arcs=st.session_state.learning_arcs,
                    language=language,
                    voice_preference=voice
                )
                
                # Clear onboarding state
                for key in ["onboarding_step", "profile_name", "interests", "learning_arcs"]:
                    if key in st.session_state:
                        del st.session_state[key]
                        
                return profile_id
                
        return None
    
    def _show_welcome(self) -> bool:
        """Show welcome screen."""
        st.header("Transform Your Learning Journey")
        st.write("""
        Project Woohoo turns academic content into engaging podcast episodes,
        helping you learn more effectively through audio content.
        
        Features:
        - 🎓 Personalized learning paths
        - 🎙️ AI-powered podcast generation
        - 📚 Integration with academic sources
        - 🌟 Track your progress
        """)
        
        return st.button("Get Started →")
    
    def _show_profile_setup(self) -> Tuple[bool, str]:
        """Show profile setup screen."""
        st.header("Create Your Profile")
        
        name = st.text_input("What should we call you?")
        if not name:
            st.info("Please enter your name to continue")
            return False, ""
            
        return st.button("Continue →"), name
    
    def _show_interests(self) -> Tuple[bool, Tuple[list, list]]:
        """Show interests and learning arcs selection."""
        st.header("Customize Your Experience")
        
        # Select interests
        st.subheader("What topics interest you?")
        interests = st.multiselect(
            "Select your interests",
            options=self.profile_manager.available_interests,
            default=["Academic Research", "Technology Trends"]
        )
        
        # Select learning arcs
        st.subheader("Choose Your Learning Paths")
        st.write("Learning paths help organize your podcast episodes into coherent educational journeys.")
        
        selected_arcs = []
        for arc in self.profile_manager.available_learning_arcs:
            col1, col2 = st.columns([1, 3])
            with col1:
                if st.checkbox(arc["name"], key=f"arc_{arc['id']}"):
                    selected_arcs.append(arc["id"])
            with col2:
                st.write(f"*{arc['description']}*")
                st.write(", ".join(arc["topics"]))
        
        if not interests or not selected_arcs:
            st.info("Please select at least one interest and learning path")
            return False, ([], [])
            
        return st.button("Continue →"), (interests, selected_arcs)
    
    def _show_preferences(self) -> Tuple[bool, Tuple[str, str]]:
        """Show language and voice preferences."""
        st.header("Set Your Preferences")
        
        # Language selection
        language = st.selectbox(
            "Preferred Language",
            options=[
                ("en", "English"),
                ("es", "Spanish"),
                ("fr", "French"),
                ("de", "German"),
                ("it", "Italian"),
                ("pt", "Portuguese"),
                ("ru", "Russian"),
                ("ja", "Japanese"),
                ("ko", "Korean"),
                ("zh", "Chinese")
            ],
            format_func=lambda x: x[1]
        )[0]
        
        # Voice preference
        voice = st.selectbox(
            "Voice Style",
            options=[
                "default",
                "casual",
                "professional",
                "enthusiastic"
            ]
        )
        
        completed = st.button("Complete Setup →")
        if completed:
            st.balloons()
            st.success("Profile created successfully!")
            
        return completed, (language, voice) 