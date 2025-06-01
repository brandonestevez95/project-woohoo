import streamlit as st
from pathlib import Path
import json
from dotenv import load_dotenv
from components.onboarding import OnboardingFlow
from utils.profile_manager import ProfileManager

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="Project Woohoo",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
with open('app/static/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Initialize managers
profile_manager = ProfileManager()

# Initialize session state
if "favorites" not in st.session_state:
    st.session_state.favorites = set()
if "current_page" not in st.session_state:
    st.session_state.current_page = "🧭 Home"
if "profile_id" not in st.session_state:
    st.session_state.profile_id = None

# Check for active profile
if not st.session_state.profile_id:
    onboarding = OnboardingFlow()
    profile_id = onboarding.show()
    if profile_id:
        st.session_state.profile_id = profile_id
        st.rerun()
else:
    # Load active profile
    profile = profile_manager.get_profile(st.session_state.profile_id)
    if not profile:
        st.session_state.profile_id = None
        st.rerun()
    
    # Sidebar navigation with custom styling
    with st.sidebar:
        st.markdown(
            f"""
            <div class="profile-header">
                <div class="profile-avatar">{profile['name'][0].upper()}</div>
                <div>
                    <h2>{profile['name']}</h2>
                    <p>{len(profile['learning_arcs'])} Learning Paths</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        pages = ["🧭 Home", "📚 Sources", "🧠 Generate", "🎧 Library", "📊 Progress", "⚙️ Settings"]
        st.session_state.current_page = st.radio("Navigation", pages)
        
        # Show learning progress in sidebar
        progress = profile_manager.get_learning_progress(st.session_state.profile_id)
        st.metric("Episodes Completed", progress["completed_episodes"])
        
        with st.expander("Learning Progress"):
            for arc, count in progress["arc_progress"].items():
                arc_info = next((a for a in profile_manager.available_learning_arcs if a["id"] == arc), None)
                if arc_info:
                    st.markdown(f"""
                        <div class="progress-item">
                            <div class="progress-label">{arc_info['name']}</div>
                            <div class="progress-count">{count} episodes</div>
                        </div>
                    """, unsafe_allow_html=True)
    
    # Main content area
    def main():
        if st.session_state.current_page == "🧭 Home":
            show_home_page(profile)
        elif st.session_state.current_page == "📚 Sources":
            show_sources_page()
        elif st.session_state.current_page == "🧠 Generate":
            show_generate_page(profile)
        elif st.session_state.current_page == "🎧 Library":
            show_library_page()
        elif st.session_state.current_page == "📊 Progress":
            show_progress_page(profile)
        elif st.session_state.current_page == "⚙️ Settings":
            show_settings_page(profile)

    def show_home_page(profile: dict):
        st.title("Your Learning Dashboard 🎓")
        
        # Quick stats with custom styling
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
                <div class="metric-card">
                    <div class="value">{}</div>
                    <div class="label">Total Episodes</div>
                </div>
            """.format(len(get_episodes())), unsafe_allow_html=True)
        with col2:
            st.markdown("""
                <div class="metric-card">
                    <div class="value">{}</div>
                    <div class="label">Favorites</div>
                </div>
            """.format(len(st.session_state.favorites)), unsafe_allow_html=True)
        with col3:
            st.markdown("""
                <div class="metric-card">
                    <div class="value">{}</div>
                    <div class="label">Active Learning Paths</div>
                </div>
            """.format(len(profile["learning_arcs"])), unsafe_allow_html=True)
        
        # Learning paths with enhanced styling
        st.header("Your Learning Journey")
        for arc_id in profile["learning_arcs"]:
            arc_info = next((a for a in profile_manager.available_learning_arcs if a["id"] == arc_id), None)
            if arc_info:
                with st.expander(f"{arc_info['name']} 📚"):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.markdown(f"*{arc_info['long_description']}*")
                        st.markdown("#### Topics")
                        topics_html = "".join([
                            f'<span class="topic-tag">{topic}</span>'
                            for topic in arc_info["topics"]
                        ])
                        st.markdown(f'<div class="topics">{topics_html}</div>', unsafe_allow_html=True)
                    with col2:
                        st.markdown("#### Recommended Sources")
                        for source in arc_info["recommended_sources"]:
                            st.markdown(f"- {source}")
                        st.markdown(f"**Difficulty:** {arc_info['difficulty']}")
                    
                    # Progress bar
                    progress = profile["progress"].get(arc_id, 0)
                    st.progress(min(progress / 10, 1.0))
                    st.write(f"Progress: {progress} episodes completed")
                    
                    # Action buttons
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        if st.button("Generate Episode", key=f"gen_{arc_id}"):
                            st.session_state.current_page = "🧠 Generate"
                            st.session_state.selected_arc = arc_id
                            st.rerun()
                    with col2:
                        st.markdown("""
                            <div class="difficulty-badge">
                                {}
                            </div>
                        """.format(arc_info["difficulty"]), unsafe_allow_html=True)
        
        # Suggested next steps
        st.header("Suggested Next Steps")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
                <div class="suggestion-card">
                    <h3>🎯 Complete Your Next Episode</h3>
                    <p>Generate a new episode in your active learning paths to maintain momentum.</p>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
                <div class="suggestion-card">
                    <h3>📚 Add More Sources</h3>
                    <p>Expand your knowledge base by connecting more academic sources.</p>
                </div>
            """, unsafe_allow_html=True)

    def show_generate_page(profile: dict):
        st.title("Generate Episode 🧠")
        
        # Pre-select learning arc if coming from dashboard
        selected_arc = None
        if hasattr(st.session_state, "selected_arc"):
            selected_arc = st.session_state.selected_arc
            del st.session_state.selected_arc
        
        # Source selection
        st.multiselect("Select Sources (1-3)", ["Source 1", "Source 2", "Source 3"])
        
        # Generation settings
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Tone", ["Journalistic", "Youth", "Academic"])
            st.slider("Target Duration (minutes)", 5, 30, 15)
            
            # Use profile preferences
            st.selectbox(
                "Language",
                options=[lang[0] for lang in [
                    ("en", "English"), ("es", "Spanish"), ("fr", "French"),
                    ("de", "German"), ("it", "Italian"), ("pt", "Portuguese"),
                    ("ru", "Russian"), ("ja", "Japanese"), ("ko", "Korean"),
                    ("zh", "Chinese")
                ]],
                index=0 if profile["language"] == "en" else None,
                format_func=lambda x: dict([
                    ("en", "English"), ("es", "Spanish"), ("fr", "French"),
                    ("de", "German"), ("it", "Italian"), ("pt", "Portuguese"),
                    ("ru", "Russian"), ("ja", "Japanese"), ("ko", "Korean"),
                    ("zh", "Chinese")
                ])[x]
            )
        with col2:
            st.text_input("Episode Title")
            st.text_area("Additional Notes")
            
            # Learning arc selection
            arc_options = [
                (arc["id"], arc["name"])
                for arc in profile_manager.available_learning_arcs
                if arc["id"] in profile["learning_arcs"]
            ]
            selected_arc = st.selectbox(
                "Learning Path",
                options=[arc[0] for arc in arc_options],
                format_func=lambda x: dict(arc_options)[x],
                index=arc_options.index((selected_arc, dict(arc_options)[selected_arc])) if selected_arc else 0
            )
        
        if st.button("Generate Episode"):
            with st.spinner("Generating..."):
                # TODO: Implement generation pipeline
                pass

    def show_progress_page(profile: dict):
        st.title("Learning Progress 📊")
        
        # Overall progress
        progress = profile_manager.get_learning_progress(profile["id"])
        st.header("Overview")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Episodes Completed", progress["completed_episodes"])
        with col2:
            st.metric("Active Learning Paths", len(profile["learning_arcs"]))
        
        # Progress by learning path
        st.header("Progress by Learning Path")
        for arc_id, count in progress["arc_progress"].items():
            arc_info = next((a for a in profile_manager.available_learning_arcs if a["id"] == arc_id), None)
            if arc_info:
                st.subheader(arc_info["name"])
                st.progress(min(count / 10, 1.0))  # Assume 10 episodes is completion
                st.write(f"{count} episodes completed")
                
                # Show completed episodes
                if profile["completed_episodes"]:
                    with st.expander("View Completed Episodes"):
                        for episode_id in profile["completed_episodes"]:
                            episode = get_episode(episode_id)
                            if episode:
                                st.write(f"- {episode['title']}")

    def get_episodes():
        """Get list of episodes from the index file."""
        index_path = Path("output/episode_index.json")
        if not index_path.exists():
            return []
        try:
            with open(index_path) as f:
                return json.load(f)
        except:
            return []
    
    def get_episode(episode_id: str):
        """Get specific episode by ID."""
        episodes = get_episodes()
        return next((ep for ep in episodes if ep["id"] == episode_id), None)

    def show_sources_page():
        st.title("Sources 📚")
        
        # Source type selection
        source_type = st.selectbox(
            "Select Source Type",
            ["Zotero Library", "RSS Feed", "Upload File"]
        )
        
        if source_type == "Zotero Library":
            st.text_input("Zotero Library ID")
            st.text_input("Zotero API Key (optional)")
            st.button("Connect Library")
            
        elif source_type == "RSS Feed":
            st.text_input("RSS Feed URL")
            st.button("Add Feed")
            
        elif source_type == "Upload File":
            st.file_uploader("Upload .bib or .csv file", type=["bib", "csv"])

    def show_library_page():
        st.title("Episode Library 🎧")
        
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            st.multiselect("Filter by Tags", ["AI", "Science", "History"])
        with col2:
            st.checkbox("Show Favorites Only")
        
        # Episode list
        episodes = get_episodes()
        for episode in episodes:
            with st.expander(episode["title"]):
                st.audio(episode["audio_path"])
                st.download_button("Download Audio", episode["audio_path"])
                st.download_button("Download Transcript", episode["transcript_path"])
                if episode["id"] in st.session_state.favorites:
                    if st.button("⭐ Unfavorite", key=f"unfav_{episode['id']}"):
                        st.session_state.favorites.remove(episode["id"])
                else:
                    if st.button("☆ Favorite", key=f"fav_{episode['id']}"):
                        st.session_state.favorites.add(episode["id"])

    def show_settings_page(profile: dict):
        st.title("Settings ⚙️")
        
        # Voice Settings
        st.subheader("Voice Settings")
        st.selectbox("Default Voice", [
            "Male, enthusiastic (v2/en_speaker_1)",
            "Female, professional (v2/en_speaker_2)",
            "Male, deep (v2/en_speaker_3)",
            "Female, warm (v2/en_speaker_4)",
            "Male, narrative (v2/en_speaker_5)",
            "Female, clear (v2/en_speaker_6)",
            "Male, authoritative (v2/en_speaker_7)",
            "Female, engaging (v2/en_speaker_8)"
        ])
        st.selectbox("Default Language", ["English", "Spanish", "French", "German"])
        
        # Storage Settings
        st.subheader("Storage Settings")
        st.number_input("Max Episodes to Keep", min_value=10, value=50)
        if st.button("Clear Cache"):
            # TODO: Implement cache clearing
            pass

    if __name__ == "__main__":
        main() 