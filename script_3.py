# Create a sample .env file template
env_content = '''# OpenRouter API Configuration
# Get your API key from: https://openrouter.ai/keys
OR_API_KEY=your_openrouter_api_key_here

# Example:
# OR_API_KEY=sk-or-v1-1234567890abcdef...
'''

with open(".env.example", "w") as f:
    f.write(env_content)

print("Created .env.example template")