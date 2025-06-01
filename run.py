import streamlit.web.cli as stcli
import sys
from pathlib import Path

if __name__ == "__main__":
    root_path = Path(__file__).parent
    sys.path.append(str(root_path))
    
    sys.argv = ["streamlit", "run", "app/main.py"]
    sys.exit(stcli.main()) 