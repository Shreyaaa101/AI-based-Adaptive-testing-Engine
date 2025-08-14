# AI-based-Adaptive-testing-Engine
AI-Driven Adaptive Testing Platform that adjusts question difficulty in real  time based on the candidate’s responses. By analyzing performance patterns, the system  ensures each test is personalized, relevant, and accurately measures.
A Python-based application that includes backend logic, scripts, and setup utilities.
This repository contains the full source code, configuration files, and dependencies to run the project.

📂 Project Structure
.
├── app.py              # Main application entry point
├── backend.py          # Backend logic and processing
├── script.py           # Utility or feature script
├── script_1.py ... script_7.py  # Additional functional scripts
├── setup.py            # Installation setup script
├── test_setup.py       # Test cases for setup validation
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (not for public sharing)
└── README.md           # Project documentation

🚀 Getting Started
1️⃣ Prerequisites

Python 3.10 or higher

pip (Python package manager)

2️⃣ Installation

Clone the repository and install dependencies:

pip install -r requirements.txt

3️⃣ Setup Environment Variables

Create a .env file in the project root (if not already present) and add the required variables:

API_KEY=your_api_key_here

4️⃣ Running the Application

Run the main application:

python app.py

Run backend:

python backend.py

🧪 Running Tests
python -m unittest test_setup.py

📦 Deployment

You can package and deploy the app using:

python setup.py install
