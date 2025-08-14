# Create the requirements.txt file
requirements_content = """streamlit>=1.28.0
requests>=2.31.0
python-dotenv>=1.0.0
PyMuPDF>=1.23.0
json5>=0.9.0
"""

with open("requirements.txt", "w") as f:
    f.write(requirements_content)

print("Created requirements.txt")