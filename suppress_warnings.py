
import os
import sys
import warnings

# Aggressive warning suppression
def ignore_warnings(message="", category=Warning, filename="", lineno=-1, file=None, line=None):
    return True

warnings.showwarning = ignore_warnings
warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"

# Specifically handle pkg_resources warnings
try:
    import pkg_resources
    pkg_resources.working_set  # Access it once to trigger the warning
except:
    pass
