import streamlit as st
from pathlib import Path
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="Project Woohoo",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "favorites" not in st.session_state:
    st.session_state.favorites = set()
if "current_page" not in st.session_state:
    st.session_state.current_page = "🧭 Home"

# Sidebar navigation
st.sidebar.title("Project Woohoo 🎙️")
pages = ["🧭 Home", "📚 Sources", "🧠 Generate", "🎧 Library", "⚙️ Settings"]
st.session_state.current_page = st.sidebar.radio("Navigation", pages)

# Main content area
def main():
    if st.session_state.current_page == "🧭 Home":
        st.title("Welcome to Project Woohoo! 🎙️")
        st.write("""
        Transform your academic sources into engaging podcast episodes using AI.
        
        Get started by:
        1. Adding your sources in the 📚 Sources section
        2. Generating new episodes in the 🧠 Generate section
        3. Managing your library in the 🎧 Library section
        """)
        
        # Quick stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Episodes", len(get_episodes()))
        with col2:
            st.metric("Favorites", len(st.session_state.favorites))
        with col3:
            st.metric("Sources", get_source_count())

    elif st.session_state.current_page == "📚 Sources":
        show_sources_page()
    elif st.session_state.current_page == "🧠 Generate":
        show_generate_page()
    elif st.session_state.current_page == "🎧 Library":
        show_library_page()
    elif st.session_state.current_page == "⚙️ Settings":
        show_settings_page()

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

def get_source_count():
    """Get count of available sources."""
    # TODO: Implement source counting from Zotero and local files
    return 0

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

def show_generate_page():
    st.title("Generate Episode 🧠")
    
    # Source selection
    st.multiselect("Select Sources (1-3)", ["Source 1", "Source 2", "Source 3"])
    
    # Generation settings
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Tone", ["Journalistic", "Youth", "Academic"])
        st.slider("Target Duration (minutes)", 5, 30, 15)
        st.selectbox("Voice", [
            "Male, enthusiastic",
            "Female, professional",
            "Male, deep",
            "Female, warm",
            "Male, narrative",
            "Female, clear",
            "Male, authoritative",
            "Female, engaging"
        ])
    with col2:
        st.text_input("Episode Title")
        st.text_area("Additional Notes")
        st.selectbox("Language", ["English", "Spanish", "French", "German"])
    
    if st.button("Generate Episode"):
        with st.spinner("Generating..."):
            # TODO: Implement generation pipeline
            pass

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

def show_settings_page():
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