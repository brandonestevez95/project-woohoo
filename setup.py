from setuptools import setup, find_packages

setup(
    name="operation_woohoo",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.24.0",
        "pandas>=1.5.0",
        "numpy>=1.24.0",
    ],
    python_requires=">=3.8",
    author="Brandon Estevez",
    description="AI-powered podcast generator",
    entry_points={
        "console_scripts": [
            "woohoo=app.main:main",
        ],
    },
) 