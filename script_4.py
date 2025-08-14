# Create a comprehensive README.md file
readme_content = '''# 🧠 AI-Driven Adaptive Testing Platform

A sophisticated Streamlit-based application that creates personalized adaptive tests from PDF study materials using AI. The platform dynamically adjusts question difficulty based on user performance and provides detailed learning analytics.

## ✨ Features

### 📄 PDF Processing
- Upload PDF study materials
- Extract text using PyMuPDF (handles various PDF formats)
- Intelligent error handling for corrupted or image-based PDFs
- Support for multi-page documents

### 🤖 AI Question Generation
- Generates 20 multiple-choice questions using OpenRouter API
- Questions span difficulty levels from 0.1 (easiest) to 0.9 (hardest)
- Uses GPT-4o-mini for cost-effective question generation
- Validates question format and content quality

### 🎯 Adaptive Testing Algorithm
- **Dynamic Difficulty Adjustment**: Questions get harder or easier based on performance
- **Intelligent Question Selection**: Picks optimal next question from pre-generated set
- **Performance-Based Scoring**: Harder questions yield more points (multiplier system)
- **Real-Time Adaptation**: Adjusts user ability and difficulty after each answer

### 📊 Live Metrics & Analytics
- **Real-Time Tracking**: Current difficulty, ability score, accuracy
- **Performance Insights**: Time per question, points earned, multiplier effects
- **Progress Monitoring**: Questions attempted, score progression
- **Learning Journey Visualization**: Charts showing difficulty and ability evolution

### 📈 Comprehensive Results
- **Detailed Performance Summary**: Total points, accuracy, ability progression
- **Time Analysis**: Fastest/slowest response times, average difficulty faced
- **Learning Recommendations**: Identifies topics needing improvement
- **Visual Progress Charts**: Shows learning journey and performance trends

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- OpenRouter API key ([Get one here](https://openrouter.ai/keys))

### Installation

1. **Clone or download the project files**
   ```bash
   # Ensure you have these files:
   # - app.py (main Streamlit application)
   # - backend.py (core logic and API handling)
   # - requirements.txt (dependencies)
   # - .env.example (API key template)
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your OpenRouter API key:
   OR_API_KEY=your_actual_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to that URL manually

## 📋 How to Use

### Step 1: Upload PDF
1. Click "Choose a PDF file" and select your study material
2. Ensure the PDF contains readable text (not just images)
3. Click "Process PDF & Generate Questions"
4. Wait for text extraction and question generation (usually 30-60 seconds)

### Step 2: Take the Adaptive Test
1. Answer questions one by one
2. Monitor your real-time metrics (difficulty, ability, score)
3. Notice how questions adapt to your performance:
   - **Correct + Fast (< 10s)**: Significant difficulty increase
   - **Correct + Slow (≥ 10s)**: Moderate difficulty increase  
   - **Incorrect**: Difficulty decrease, easier next question
4. Each question shows topic, difficulty level, and point multiplier

### Step 3: View Results & Analytics
1. **Performance Summary**: Total score, accuracy, questions completed
2. **Time Analysis**: Response time patterns and trends
3. **Learning Insights**: Topics needing improvement
4. **Progress Visualization**: Charts showing your learning journey
5. **Action Options**: Restart test or upload new material

## 🔧 Technical Architecture

### File Structure
```
├── app.py              # Main Streamlit application
├── backend.py          # Core logic (PDF processing, API calls, adaptive engine)
├── requirements.txt    # Python dependencies
├── .env.example       # API key template
└── .env               # Your actual API key (create this)
```

### Core Components

#### `PDFProcessor` Class
- Text extraction from uploaded PDFs
- Error handling for various PDF issues
- Support for multi-page documents

#### `OpenRouterAPI` Class  
- Handles all API communication with OpenRouter
- Question generation with specific JSON schema
- Response validation and error handling

#### `AdaptiveTestEngine` Class
- **Question Selection Algorithm**: Finds best-matching unused question based on current difficulty
- **Performance Processing**: Updates user ability and difficulty after each answer
- **Scoring System**: Dynamic point calculation with difficulty multipliers
- **Analytics Generation**: Comprehensive test results and insights

### Adaptive Algorithm Details

The system uses a sophisticated adaptive algorithm:

1. **Initialization**: Starts with medium difficulty (0.5) and ability (0.5)
2. **Question Selection**: Finds unused question closest to target difficulty
3. **Performance Analysis**:
   - Correct + Fast (< 10s): Ability +0.1, Difficulty +0.05
   - Correct + Slow: Ability +0.05, Difficulty +0.05  
   - Incorrect: Ability -0.08, Difficulty -0.1
4. **Scoring**: Points = Base Points × (1 + (Difficulty - 0.5))
5. **Bounds**: Ability and difficulty clamped between 0.1 and 0.9

## 🛠️ Customization Options

### Modifying Question Generation
Edit the prompt in `backend.py` → `OpenRouterAPI.generate_questions()`:
- Change question types (multiple choice, true/false, etc.)
- Adjust difficulty distribution
- Modify question topics or focus areas

### Adjusting Adaptive Algorithm
Modify parameters in `backend.py` → `AdaptiveTestEngine.process_answer()`:
- **Ability Updates**: Change increment/decrement values
- **Time Thresholds**: Adjust fast/slow response cutoffs
- **Scoring Multipliers**: Modify point calculation formula
- **Question Selection**: Adjust difficulty tolerance ranges

### UI Customization
Edit styling in `app.py`:
- **CSS Styles**: Modify the custom CSS section
- **Layout**: Adjust column layouts and component arrangements
- **Metrics Display**: Add/remove performance indicators
- **Color Schemes**: Update container backgrounds and borders

## 🔍 Troubleshooting

### Common Issues

**API Key Errors**
```
Error: OR_API_KEY not found in environment variables
```
- Solution: Create `.env` file with `OR_API_KEY=your_key_here`
- Restart the application after adding the key

**PDF Processing Errors**  
```
Error: No text could be extracted from the PDF
```
- PDF might be image-based or corrupted
- Try a different PDF with readable text
- Ensure PDF is not password-protected

**Question Generation Failures**
```
Error: Invalid JSON response from API
```
- Check your API key balance and permissions
- Ensure stable internet connection
- Try with shorter PDF content

**Memory Issues**
- For large PDFs, only first 1000 words are used
- Close other browser tabs if experiencing slowdowns
- Restart the application if session state becomes corrupted

### Performance Tips

- **PDF Size**: Optimal PDF size is 1-10 pages with clear text
- **Internet**: Stable connection required for API calls
- **Browser**: Use Chrome/Firefox for best Streamlit compatibility
- **Session State**: Refresh page if application state seems stuck

## 🔐 Security Notes

- API keys are loaded from `.env` file (never commit this file)
- All processing happens locally except for question generation
- No user data is stored permanently
- Session data clears when browser is closed

## 📊 API Usage & Costs

- Uses OpenRouter's GPT-4o-mini model for cost efficiency
- Approximate cost: $0.01-0.05 per test (20 questions)
- Only calls API once per PDF upload (not per question)
- Questions are pre-generated and stored in session

## 🤝 Contributing

To extend or modify the application:

1. **Add New Question Types**: Modify the generation prompt and UI components
2. **Enhanced Analytics**: Add more sophisticated performance metrics  
3. **Different AI Models**: Change the model in `OpenRouterAPI` class
4. **Database Integration**: Add persistence for user progress tracking
5. **Multiple File Formats**: Extend `PDFProcessor` for DOC, TXT files

## 📄 License

This project is provided as-is for educational and personal use. Make sure to comply with OpenRouter's API terms of service.

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify all files are present and properly configured
3. Ensure your OpenRouter API key is valid and has sufficient credits
4. Check that all dependencies are correctly installed

---

**Happy Learning! 🎓**
'''

with open("README.md", "w") as f:
    f.write(readme_content)

print("Created comprehensive README.md")