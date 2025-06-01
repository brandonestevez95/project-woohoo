import os
import sys
import subprocess
from pathlib import Path

def run_app():
    # Get the directory containing our script
    if getattr(sys, 'frozen', False):
        # If we're running as a bundled exe, use sys._MEIPASS
        bundle_dir = Path(sys._MEIPASS)
    else:
        # If we're running from a normal Python environment
        bundle_dir = Path(__file__).parent

    # Set up environment
    os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    os.environ['STREAMLIT_SERVER_PORT'] = '8501'
    
    # Ensure output directory exists
    output_dir = bundle_dir / 'output'
    output_dir.mkdir(exist_ok=True)

    # Run Streamlit
    streamlit_path = str(bundle_dir / 'app' / 'main.py')
    subprocess.run([sys.executable, '-m', 'streamlit', 'run', streamlit_path])

if __name__ == '__main__':
    run_app() 