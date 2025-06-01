import streamlit as st
import json
from utils.profile_manager import ProfileManager

def show_settings():
    st.title("Settings ⚙️")
    
    if "profile_id" not in st.session_state:
        st.warning("Please complete the onboarding process first.")
        return
        
    profile_manager = ProfileManager()
    profile = profile_manager.get_profile(st.session_state.profile_id)
    
    if not profile:
        st.error("Could not load profile. Please try logging in again.")
        return
    
    # Profile card
    st.markdown("""
        <div class="profile-header" style="margin-bottom: 2rem;">
            <div class="profile-avatar">{}</div>
            <div>
                <h2>{}</h2>
                <p>Member since {}</p>
            </div>
        </div>
    """.format(
        profile["name"][0].upper(),
        profile["name"],
        "today"  # TODO: Format date
    ), unsafe_allow_html=True)
    
    # Profile Settings
    with st.expander("Profile Settings", expanded=True):
        st.markdown('<div class="settings-section">', unsafe_allow_html=True)
        st.subheader("Basic Information")
        new_name = st.text_input("Name", value=profile["name"])
        
        # Interests
        st.subheader("Interests")
        new_interests = st.multiselect(
            "Select your interests",
            options=profile_manager.available_interests,
            default=profile["interests"]
        )
        
        # Learning Paths
        st.subheader("Learning Paths")
        st.write("Select the learning paths you want to follow:")
        
        new_arcs = []
        for arc in profile_manager.available_learning_arcs:
            col1, col2 = st.columns([1, 3])
            with col1:
                if st.checkbox(
                    arc["name"],
                    value=arc["id"] in profile["learning_arcs"],
                    key=f"arc_{arc['id']}"
                ):
                    new_arcs.append(arc["id"])
            with col2:
                st.markdown(f"""
                    <div class="arc-description">
                        <p><em>{arc['description']}</em></p>
                        <div class="arc-meta">
                            <span class="difficulty-badge">{arc['difficulty']}</span>
                            <span class="topics-count">{len(arc['topics'])} topics</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
        if st.button("Save Profile Changes", type="primary"):
            updates = {
                "name": new_name,
                "interests": new_interests,
                "learning_arcs": new_arcs
            }
            if profile_manager.update_profile(profile["id"], updates):
                st.success("Profile updated successfully!")
                st.rerun()
            else:
                st.error("Failed to update profile.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Language & Voice Settings
    with st.expander("Language & Voice Settings"):
        st.markdown('<div class="settings-section">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            # Language selection
            current_lang = profile["language"]
            new_lang = st.selectbox(
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
                index=next(
                    (i for i, (code, _) in enumerate([
                        ("en", "English"), ("es", "Spanish"), ("fr", "French"),
                        ("de", "German"), ("it", "Italian"), ("pt", "Portuguese"),
                        ("ru", "Russian"), ("ja", "Japanese"), ("ko", "Korean"),
                        ("zh", "Chinese")
                    ]) if code == current_lang),
                    0
                ),
                format_func=lambda x: x[1]
            )
        
        with col2:
            # Voice preference
            new_voice = st.selectbox(
                "Voice Style",
                options=[
                    "default",
                    "casual",
                    "professional",
                    "enthusiastic"
                ],
                index=["default", "casual", "professional", "enthusiastic"].index(
                    profile["voice_preference"]
                )
            )
        
        if st.button("Save Language & Voice Settings", type="primary"):
            updates = {
                "language": new_lang[0],
                "voice_preference": new_voice
            }
            if profile_manager.update_profile(profile["id"], updates):
                st.success("Settings updated successfully!")
                st.rerun()
            else:
                st.error("Failed to update settings.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Storage Settings
    with st.expander("Storage Settings"):
        st.markdown('<div class="settings-section">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.number_input(
                "Max Episodes to Keep",
                min_value=10,
                value=50,
                help="Maximum number of episodes to store locally"
            )
        with col2:
            if st.button("Clear Cache", type="secondary"):
                # TODO: Implement cache clearing
                st.info("Cache clearing not implemented yet")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Account Management
    with st.expander("Account Management"):
        st.markdown('<div class="settings-section danger-zone">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
                <div class="account-info">
                    <p><strong>Profile ID:</strong> {}</p>
                    <p><strong>Created:</strong> {}</p>
                    <p><strong>Last Updated:</strong> {}</p>
                </div>
            """.format(
                profile["id"],
                "today",  # TODO: Format date
                "today"  # TODO: Format date
            ), unsafe_allow_html=True)
        
        with col2:
            st.download_button(
                "Export Profile Data",
                data=json.dumps(profile, indent=2),
                file_name="profile_export.json",
                mime="application/json"
            )
            
            if st.button("Reset Profile", type="secondary"):
                st.warning("⚠️ This action cannot be undone!")
                if st.checkbox("I understand this will delete all my progress"):
                    st.session_state.profile_id = None
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    show_settings() 