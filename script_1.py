# Create backend.py with all core logic
backend_content = '''import fitz  # PyMuPDF
import requests
import json
import time
import os
from dotenv import load_dotenv
from typing import Dict, List, Any, Optional, Tuple
import math
import random

# Load environment variables
load_dotenv()

class PDFProcessor:
    """Handle PDF text extraction using PyMuPDF"""
    
    @staticmethod
    def extract_text_from_pdf(pdf_file) -> Tuple[str, str]:
        """
        Extract text from uploaded PDF file
        Returns: (extracted_text, error_message)
        """
        try:
            # Read the PDF file
            pdf_bytes = pdf_file.read()
            
            # Check if file is empty
            if len(pdf_bytes) == 0:
                return "", "Error: The uploaded file is empty."
            
            # Open PDF document
            pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
            
            # Check if PDF has pages
            if pdf_document.page_count == 0:
                return "", "Error: The PDF file appears to be corrupted or has no pages."
            
            extracted_text = ""
            
            # Extract text from all pages
            for page_num in range(pdf_document.page_count):
                page = pdf_document.load_page(page_num)
                page_text = page.get_text()
                extracted_text += page_text + "\\n"
            
            # Close the document
            pdf_document.close()
            
            # Check if any text was extracted
            if not extracted_text.strip():
                return "", "Error: No text could be extracted from the PDF. The file might be image-based or corrupted."
            
            return extracted_text.strip(), ""
            
        except Exception as e:
            return "", f"Error processing PDF: {str(e)}"

class OpenRouterAPI:
    """Handle OpenRouter API calls for question generation"""
    
    def __init__(self):
        self.api_key = os.getenv('OR_API_KEY')
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        
        if not self.api_key:
            raise ValueError("OR_API_KEY not found in environment variables. Please add it to your .env file.")
    
    def generate_questions(self, text_content: str) -> Tuple[List[Dict], str]:
        """
        Generate 20 multiple-choice questions from text content
        Returns: (questions_list, error_message)
        """
        try:
            # Use only first 1000 words to avoid token limits
            words = text_content.split()[:1000]
            limited_text = " ".join(words)
            
            prompt = f"""Based on the following text, generate exactly 20 multiple-choice questions in JSON format. Each question should test understanding of the material at different difficulty levels (0.1 to 0.9).

Text: {limited_text}

Generate questions with the following JSON schema:
{{
    "questions": [
        {{
            "question": "Question text here",
            "options": {{
                "A": "Option A text",
                "B": "Option B text", 
                "C": "Option C text",
                "D": "Option D text"
            }},
            "correct_answer": "A",
            "difficulty": 0.5,
            "explanation": "Brief explanation of the correct answer",
            "topic": "Main topic/concept being tested"
        }}
    ]
}}

Make sure to vary the difficulty levels from 0.1 (easiest) to 0.9 (hardest). Return only valid JSON, no markdown formatting."""

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "openai/gpt-4o-mini",  # Using a cost-effective model
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            response = requests.post(self.base_url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            
            response_data = response.json()
            content = response_data["choices"][0]["message"]["content"]
            
            # Parse JSON response
            questions_data = json.loads(content)
            
            if "questions" not in questions_data:
                return [], "Error: Invalid response format from API"
            
            questions = questions_data["questions"]
            
            if len(questions) != 20:
                return [], f"Error: Expected 20 questions, got {len(questions)}"
            
            # Validate question format
            for i, q in enumerate(questions):
                required_fields = ["question", "options", "correct_answer", "difficulty", "explanation", "topic"]
                for field in required_fields:
                    if field not in q:
                        return [], f"Error: Question {i+1} missing required field: {field}"
                
                if q["correct_answer"] not in q["options"]:
                    return [], f"Error: Question {i+1} has invalid correct_answer"
            
            return questions, ""
            
        except json.JSONDecodeError as e:
            return [], f"Error: Invalid JSON response from API - {str(e)}"
        except requests.exceptions.RequestException as e:
            return [], f"Error: API request failed - {str(e)}"
        except Exception as e:
            return [], f"Error generating questions: {str(e)}"

class AdaptiveTestEngine:
    """Core logic for adaptive testing algorithm"""
    
    def __init__(self, questions: List[Dict]):
        self.questions = questions
        self.user_ability = 0.5  # Start with medium ability
        self.current_difficulty = 0.5  # Start with medium difficulty
        self.questions_attempted = 0
        self.correct_answers = 0
        self.total_points = 0
        self.question_history = []
        self.used_questions = set()
        
        # Sort questions by difficulty for easier selection
        self.questions_by_difficulty = sorted(questions, key=lambda x: x["difficulty"])
    
    def get_next_question(self) -> Optional[Dict]:
        """
        Select the next question based on current ability and difficulty
        Returns the best matching question that hasn't been used
        """
        if len(self.used_questions) >= len(self.questions):
            return None  # All questions used
        
        # Find unused questions within reasonable difficulty range
        target_difficulty = self.current_difficulty
        tolerance = 0.2  # Allow some flexibility
        
        candidate_questions = []
        for i, q in enumerate(self.questions):
            if i not in self.used_questions:
                diff = abs(q["difficulty"] - target_difficulty)
                if diff <= tolerance:
                    candidate_questions.append((i, q, diff))
        
        # If no questions in range, expand tolerance
        if not candidate_questions:
            tolerance = 0.4
            for i, q in enumerate(self.questions):
                if i not in self.used_questions:
                    diff = abs(q["difficulty"] - target_difficulty)
                    if diff <= tolerance:
                        candidate_questions.append((i, q, diff))
        
        # If still no questions, take any unused question
        if not candidate_questions:
            for i, q in enumerate(self.questions):
                if i not in self.used_questions:
                    candidate_questions.append((i, q, abs(q["difficulty"] - target_difficulty)))
        
        if not candidate_questions:
            return None
        
        # Select the question with difficulty closest to target
        best_question = min(candidate_questions, key=lambda x: x[2])
        question_index, question, _ = best_question
        
        self.used_questions.add(question_index)
        return question
    
    def process_answer(self, is_correct: bool, time_taken: float, question_difficulty: float) -> Dict:
        """
        Process user's answer and update ability/difficulty
        Returns metrics for the current question
        """
        self.questions_attempted += 1
        
        # Calculate multiplier based on difficulty
        multiplier = 1 + (question_difficulty - 0.5)
        
        # Calculate points earned
        base_points = 10
        if is_correct:
            self.correct_answers += 1
            points_earned = int(base_points * multiplier)
            self.total_points += points_earned
            
            # Update ability based on performance
            if time_taken < 10:  # Quick correct answer
                ability_increase = 0.1
            else:  # Slow but correct
                ability_increase = 0.05
            
            self.user_ability = min(0.9, self.user_ability + ability_increase)
            self.current_difficulty = min(0.9, self.current_difficulty + 0.05)
            
        else:
            points_earned = 0
            # Decrease ability and difficulty for wrong answer
            self.user_ability = max(0.1, self.user_ability - 0.08)
            self.current_difficulty = max(0.1, self.current_difficulty - 0.1)
        
        # Store question history
        question_result = {
            "question_num": self.questions_attempted,
            "is_correct": is_correct,
            "time_taken": time_taken,
            "difficulty": question_difficulty,
            "points_earned": points_earned,
            "multiplier": multiplier,
            "ability_after": self.user_ability
        }
        
        self.question_history.append(question_result)
        
        return {
            "is_correct": is_correct,
            "points_earned": points_earned,
            "time_taken": time_taken,
            "multiplier": multiplier,
            "current_difficulty": self.current_difficulty,
            "user_ability": self.user_ability,
            "questions_attempted": self.questions_attempted,
            "total_points": self.total_points
        }
    
    def get_final_results(self) -> Dict:
        """
        Calculate and return final test results
        """
        if self.questions_attempted == 0:
            return {}
        
        accuracy = (self.correct_answers / self.questions_attempted) * 100
        
        # Calculate average difficulty
        avg_difficulty = sum(q["difficulty"] for q in self.question_history) / len(self.question_history)
        
        # Find fastest and slowest times
        times = [q["time_taken"] for q in self.question_history]
        fastest_time = min(times) if times else 0
        slowest_time = max(times) if times else 0
        
        # Get incorrect topics for improvement suggestions
        incorrect_topics = []
        for i, result in enumerate(self.question_history):
            if not result["is_correct"] and i < len(self.questions):
                # Find the corresponding question
                for q in self.questions:
                    if abs(q["difficulty"] - result["difficulty"]) < 0.01:  # Match by difficulty
                        incorrect_topics.append(q.get("topic", "Unknown topic"))
                        break
        
        return {
            "total_points": self.total_points,
            "questions_attempted": self.questions_attempted,
            "correct_answers": self.correct_answers,
            "accuracy": accuracy,
            "avg_difficulty": avg_difficulty,
            "fastest_time": fastest_time,
            "slowest_time": slowest_time,
            "final_ability": self.user_ability,
            "incorrect_topics": list(set(incorrect_topics)),  # Remove duplicates
            "question_history": self.question_history
        }
    
    def reset(self):
        """Reset the test engine for a new test"""
        self.user_ability = 0.5
        self.current_difficulty = 0.5
        self.questions_attempted = 0
        self.correct_answers = 0
        self.total_points = 0
        self.question_history = []
        self.used_questions = set()
'''

with open("backend.py", "w") as f:
    f.write(backend_content)

print("Created backend.py")