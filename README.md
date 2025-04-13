# AI-Powered Course Project Feedback Generator

A professional, fully functional AI-Powered Course Project Feedback Generator built with Streamlit, integrating multiple LLM providers. This tool helps educators provide consistent, high-quality feedback on student projects according to structured marking criteria.

## Features

- **Intuitive Streamlit UI** with clear sections for LLM selection, marking criteria, comments, and feedback generation
- **Multiple LLM Integration** supporting:
  - Gemini 2.0 Flash
  - Gemini 2.5 Pro
  - Deepseek R1 (via Together API)
  - Llama 4 Scout (via KlusterAI)
  - Ollama Gemma 3
  - Ollama Deepseek R1
- **Dynamic Prompt Engineering** for generating structured, actionable feedback
- **Flexible Feedback Options** including failing criteria feedback and learner-requested items

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/ai-powered-course-project-feedback.git
cd ai-powered-course-project-feedback
```

2. Set up a Python virtual environment (Python 3.8+ recommended):
```bash
# Using pyenv
pyenv virtualenv 3.11 feedback_env
pyenv activate feedback_env

# Or using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install streamlit google-generativeai together huggingface-hub openai ollama python-dotenv
```

4. Configure API keys in `secrets.env`:
```
GEMINI_API_KEY=your_gemini_api_key
KLUSTERAI_API_KEY=your_klusterai_api_key
TOGETHER_API_KEY=your_together_api_key
HF_TOKEN=your_huggingface_token
```

5. For Ollama models, ensure Ollama is installed and running locally:
```bash
# Install Ollama: https://ollama.com/download
# Pull required models
ollama pull gemma3:12b
ollama pull deepseek-r1:14b
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your browser and navigate to `http://localhost:8501`

3. Use the interface to:
   - Select an LLM provider from the dropdown
   - Check the marking criteria that have been met
   - Add optional comments for each criterion
   - Provide feedback for failing criteria (if applicable)
   - Include responses to learner-specific queries (if applicable)
   - Click "Generate Feedback" to create the feedback

4. Review the generated feedback and download it if desired

## Files Structure

- `app.py` - Main Streamlit application
- `llm_inference.py` - Module containing functions for each LLM provider
- `marking_criteria.md` - Structured marking criteria
- `feedback_examples.md` - Examples of effective feedback patterns
- `secrets.env` - Environment file for API keys

## Notes

- Each LLM has different characteristics and may generate slightly different feedback
- Generation time varies by model, typically less than 15 seconds per LLM
- Error handling is included for each LLM to ensure graceful degradation

## License

[MIT License](LICENSE)
