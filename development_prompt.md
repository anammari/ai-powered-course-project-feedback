**System Development Prompt for AI Coding Assistant**  

**Objective**: Develop a professional, fully functional AI-Powered Course Project Feedback Generator using Streamlit, integrating multiple LLM providers, adhering to strict marking criteria and feedback best practices.  

---

### **1. Core Requirements**  
- **Streamlit UI**:  
  - Intuitive, user-friendly interface with clear sections for LLM selection, marking criteria, comments, and feedback generation.  
  - Must include:  
    - Dropdown menu listing all available LLMs (Gemini 2.0 Flash, Gemini 2.5 Pro, Deepseek R1, Llama 4 Scout, Ollama Gemma 3, Ollama deepseek-r1 14B).  
    - Checkbox list of **all** marking items from `marking_criteria.md`, each with an adjacent text field for optional comments.  
    - Two large text boxes:  
      1. **Failing Criteria Feedback**: For comments on failed requirements.  
      2. **Learner-Requested Items Feedback**: For responses to learner-specific queries.  
    - "Generate Feedback" button to trigger LLM inference.  

- **LLM Integration**:  
  - Use the provided example scripts (`gemini_flash_inference.py`, `gemini_pro_inference.py`, etc.) as templates to implement inference functions for each LLM.  
  - Ensure compatibility with each LLM’s API/interface (e.g., Ollama vs. Gemini).  
  - Centralize LLM invocation logic for maintainability.  

- **Prompt Engineering**:  
  - Dynamically construct a system prompt containing:  
    - Instructions to generate structured, actionable feedback adhering to `feedback_examples.md` best practices.  
    - Full list of **checked marking items** (from UI) with associated user comments.  
    - Content from the two text boxes (if provided).  
    - Explicit directive to **omit failing/learner-requested feedback sections** if their respective text boxes are empty.  
    - Examples from `feedback_examples.md` to guide tone, structure, and specificity.  

- **Conditional Logic**:  
  - If the "Failing Criteria Feedback" text box is empty, exclude failure-related content from the LLM prompt.  
  - If the "Learner-Requested Items Feedback" text box is empty, exclude learner-specific responses.  

---

### **2. Technical Implementation Guidelines**  
#### **A. Streamlit UI Components**  
- **LLM Selection**:  
  ```python  
  selected_llm = st.selectbox("Choose LLM", ["Gemini 2.0 Flash", "Gemini 2.5 Pro", ...])  
  ```  
- **Marking Criteria Section**:  
  - Read `marking_criteria.md`, parse each item, and render as checkboxes with text inputs:  
  ```python  
  for item in marking_criteria:  
      checked = st.checkbox(item["description"])  
      if checked:  
          comment = st.text_input(f"Comment for {item['id']}", key=item["id"])  
  ```  
- **Additional Feedback Sections**:  
  ```python  
  failing_feedback = st.text_area("Failing Criteria Feedback (if applicable)")  
  learner_feedback = st.text_area("Learner-Requested Items Feedback (if applicable)")  
  ```  

#### **B. LLM Inference Logic**  
- Create a modular system with separate functions for each LLM (e.g., `run_gemini_flask()`, `run_deepseek()`).  
- Use the provided scripts to ensure correct API/config usage (e.g., Ollama’s local server vs. Gemini’s cloud API).  
- Handle errors gracefully (e.g., display user-friendly messages if an LLM fails to respond).  

#### **C. Prompt Construction**  
- Combine the following into a single structured prompt:  
  1. **Instructions**:  
     - "Generate professional, concise feedback for a course project. Follow these best practices:"  
     - Append contents of `feedback_examples.md`.  
  2. **Checked Criteria**: List all checked marking items and their comments.  
  3. **Additional Feedback**: Include failing/learner-requested content only if provided.  
  - Format the prompt to avoid markdown or ambiguous syntax.  

#### **D. Configuration & Dependencies**  
- Include a `requirements.txt` with:  
  ```  
  streamlit google-generativeai together ollama ...  
  ```  
- Provide clear instructions for setting up API keys/local LLM dependencies (e.g., Ollama server).  

---

### **3. Quality Assurance**  
- Ensure the generated feedback:  
  - Matches the tone and structure of `feedback_examples.md`.  
  - Explicitly addresses all checked marking items and user comments.  
  - Excludes sections for empty input fields.  
- Test all LLM integrations for correctness and speed.  
- Validate UI responsiveness across devices.  

---

### **4. Deliverables**  
1. A complete Streamlit app (`app.py`) with all UI components and LLM integrations.  
2. Supporting modules for LLM inference (e.g., `llm_inference.py`).  
3. Documentation (README.md) for installation, configuration, and usage.  
4. Error handling and loading states (e.g., `st.spinner()` during inference).  

---

**Note**: All secrets required to access remote LLMs are available in `secrets.env` and its usage is demonstrated in the provided LLM chat completion example scripts. 

**Final Note**: Prioritize clarity, maintainability, and adherence to the provided example scripts. Use functional programming patterns to avoid code duplication. The marker should be able to generate feedback in <15 seconds per LLM.