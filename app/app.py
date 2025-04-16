import streamlit as st
import os
from dotenv import load_dotenv
import re
import sys
import time
import json

# Load environment variables
load_dotenv('secrets.env')

# Suppress logging warnings
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"

# Debug flag (set to False for production)
DEBUG = False

# Import LLM module
from llm_inference import (
    run_gemini_flash, 
    run_gemini_pro, 
    run_deepseek_r1_together, 
    run_llama4_scout_klusterai, 
    run_ollama_gemma3, 
    run_ollama_deepseek,
    run_ollama_llama
)

# Debug helper function
def debug_log(message, data=None):
    if DEBUG:
        debug_container = st.container()
        with debug_container:
            st.warning("Debug Info:")
            st.write(message)
            if data is not None:
                if isinstance(data, list) or isinstance(data, dict):
                    st.json(data)
                else:
                    st.write(data)

# Parse marking criteria from the markdown file
def parse_marking_criteria(file_path="marking_criteria.md"):
    criteria = []
    
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        current_section = None
        current_part = None
        current_id = None
        current_title = None
        pass_criteria = []
        fail_criteria = []
        
        for line in lines:
            # Strip any trailing whitespace
            line = line.rstrip()
            
            # Check for section header
            section_match = re.match(r'### \*\*Part (\d+)\*\*', line)
            if section_match:
                current_section = f"Part {section_match.group(1)}"
                continue
            
            # Check for part header
            part_match = re.match(r'#### \*\*Part (\d+)\.(\d+):\*\* (.*)', line)
            if part_match:
                # If we were processing a previous part, add it to the criteria list
                if current_part is not None:
                    criteria.append({
                        "id": current_id,
                        "section": current_section,
                        "title": current_title,
                        "pass_criteria": pass_criteria,
                        "fail_criteria": fail_criteria,
                        "description": current_title
                    })
                
                # Start a new part
                section_num = part_match.group(1)
                part_num = part_match.group(2)
                current_part = f"{section_num}.{part_num}"
                current_id = f"Part {current_part}"
                current_title = part_match.group(3).strip()
                # Update current section just in case it wasn't set properly
                current_section = f"Part {section_num}"
                pass_criteria = []
                fail_criteria = []
                continue
            
            # Check for pass criteria
            pass_match = re.match(r'- \[\s?\]\s*\*\*Pass\*\*:\s*(.*)', line)
            if pass_match and current_part is not None:
                pass_criteria.append(pass_match.group(1).strip())
                continue
            
            # Check for fail criteria
            fail_match = re.match(r'- \[\s?\]\s*\*\*Fail\*\*:\s*(.*)', line)
            if fail_match and current_part is not None:
                fail_criteria.append(fail_match.group(1).strip())
                continue
        
        # Add the last part if there is one
        if current_part is not None:
            criteria.append({
                "id": current_id,
                "section": current_section,
                "title": current_title,
                "pass_criteria": pass_criteria,
                "fail_criteria": fail_criteria,
                "description": current_title
            })
        
        return criteria
        
    except Exception as e:
        if DEBUG:
            print(f"Error parsing marking criteria: {str(e)}")
        return []

# Load feedback examples for prompt construction
def load_feedback_examples(file_path="feedback_examples.md"):
    with open(file_path, 'r') as file:
        return file.read()

# Construct the prompt for the LLM
def construct_prompt(selected_criteria, failing_feedback, learner_feedback, feedback_examples):
    prompt = (
        "You are an expert course project marker. Generate professional, concise feedback for a course project, following these best practices:\n\n"
        + feedback_examples + "\n\n"
    )
    
    # General feedback section
    prompt += (
        "---\n"
        "Paragraph 1: General Feedback (Strengths and Areas for Improvement)\n"
        "Summarize the strengths and areas for improvement based on the selected marking criteria and comments below. Combine strengths and improvements in a single paragraph. Do not include any final thoughts or use lists.\n"
    )
    if selected_criteria:
        prompt += "Checked Marking Criteria and Comments:\n"
        for part_item in selected_criteria:
            part_id = part_item["id"]
            part_title = part_item["title"]
            prompt += f"- {part_id}: {part_title}\n"
            if "selected_criteria" in part_item and part_item["selected_criteria"]:
                for criteria_item in part_item["selected_criteria"]:
                    criteria_type = criteria_item["type"]
                    criteria_text = criteria_item["criteria"]
                    criteria_comment = criteria_item["comment"] if criteria_item["comment"] else ""
                    type_indicator = "Pass" if criteria_type == "pass" else "Fail"
                    prompt += f"    - {type_indicator}: {criteria_text}"
                    if criteria_comment:
                        prompt += f" | Comment: {criteria_comment}"
                    prompt += "\n"
    else:
        prompt += "No marking criteria selected.\n"
    
    # Failing criteria feedback section
    if failing_feedback:
        prompt += (
            "---\n"
            "Paragraph 2: Failing Criteria Feedback\n"
            "If the following text is not empty, generate a second paragraph explaining why the submission failed these items, focusing only on the failed criteria. Do not use lists.\n"
            f"Failing Criteria Feedback:\n{failing_feedback}\n"
        )
    else:
        prompt += (
            "---\n"
            "Paragraph 2: Failing Criteria Feedback\n"
            "No failing criteria feedback provided. Omit this paragraph.\n"
        )
    
    # Learner-requested feedback section
    if learner_feedback:
        prompt += (
            "---\n"
            "Paragraph 3: Learner-Requested Items Feedback\n"
            "If the following text is not empty, generate a third paragraph with advice or responses to the learner's specific requests. Do not use lists.\n"
            f"Learner-Requested Items Feedback:\n{learner_feedback}\n"
        )
    else:
        prompt += (
            "---\n"
            "Paragraph 3: Learner-Requested Items Feedback\n"
            "No learner-requested feedback provided. Omit this paragraph.\n"
        )
    
    prompt += (
        "---\n"
        "Output only the paragraphs as described above, in order. If a paragraph is to be omitted, do not mention it. Each paragraph should be clearly separated. Do not use lists or headings.\n"
    )
    return prompt

# Main app
def main():
    st.set_page_config(
        page_title="AI-Powered Course Project Feedback Generator",
        page_icon="📝",
        layout="wide"
    )
    
    st.title("AI-Powered Course Project Feedback Generator")
    
    # Load marking criteria
    marking_criteria = parse_marking_criteria()
    
    # Debug the marking criteria
    if DEBUG:
        debug_log("Parsed Marking Criteria", marking_criteria)
    
    # Load feedback examples
    feedback_examples = load_feedback_examples()
    
    # Sidebar for LLM selection
    with st.sidebar:
        st.header("Settings")
        selected_llm = st.selectbox(
            "Choose LLM", 
            [
                "Gemini 2.0 Flash",
                "Gemini 2.5 Pro",
                "Deepseek R1 (Together)",
                "Llama 4 Scout (KlusterAI)",
                "Ollama Gemma 3",
                "Ollama Deepseek R1",
                "Ollama Llama 3.2"
            ]
        )
        
        # Generate button in sidebar
        generate_button = st.button("Generate Feedback", type="primary", use_container_width=True)

    # --- Unified full-width layout ---
    st.header("Marking Criteria")
    st.markdown("Select the criteria that have been met and add optional comments.")
    
    # Selected criteria storage
    if "selected_criteria" not in st.session_state:
        st.session_state.selected_criteria = []
    
    # Sort marking criteria by ID for consistent ordering
    marking_criteria.sort(key=lambda x: x["id"])
    
    # Display criteria directly as a flat list
    for item in marking_criteria:
        with st.container():
            # Show item ID and title
            st.markdown(f"**{item['id']}:** {item['description']}")
            
            # Initialize criteria selection if not in session state
            if f"selected_criteria_{item['id']}" not in st.session_state:
                st.session_state[f"selected_criteria_{item['id']}"] = []
            
            # Show pass criteria with checkboxes and comment fields
            if item.get('pass_criteria', []):
                st.markdown("**Pass Criteria:**")
                for i, criteria in enumerate(item.get('pass_criteria', [])):
                    criteria_id = f"{item['id']}_pass_{i}"
                    c1, c2 = st.columns([1, 10])
                    with c1:
                        checked = st.checkbox("", key=f"check_{criteria_id}")
                    with c2:
                        st.markdown(f"✅ {criteria}")
                    if checked:
                        comment = st.text_area(
                            f"Comment for '{criteria[:40]}...'", 
                            placeholder="Add your feedback comments here...",
                            height=68,
                            key=f"comment_{criteria_id}"
                        )
                        criteria_data = {
                            "id": criteria_id,
                            "parent_id": item["id"],
                            "type": "pass",
                            "criteria": criteria,
                            "comment": comment
                        }
                        existing_idx = next((i for i, x in enumerate(st.session_state[f"selected_criteria_{item['id']}"]) 
                                             if x["id"] == criteria_id), None)
                        if existing_idx is not None:
                            st.session_state[f"selected_criteria_{item['id']}"][existing_idx] = criteria_data
                        else:
                            st.session_state[f"selected_criteria_{item['id']}"].append(criteria_data)
                    else:
                        st.session_state[f"selected_criteria_{item['id']}"] = [
                            x for x in st.session_state[f"selected_criteria_{item['id']}"] if x["id"] != criteria_id
                        ]
            # Show fail criteria with checkboxes and comment fields
            if item.get('fail_criteria', []):
                st.markdown("**Fail Criteria:**")
                for i, criteria in enumerate(item.get('fail_criteria', [])):
                    criteria_id = f"{item['id']}_fail_{i}"
                    c1, c2 = st.columns([1, 10])
                    with c1:
                        checked = st.checkbox("", key=f"check_{criteria_id}")
                    with c2:
                        st.markdown(f"❌ {criteria}")
                    if checked:
                        comment = st.text_area(
                            f"Comment for '{criteria[:40]}...'", 
                            placeholder="Add your feedback comments here...",
                            height=68,
                            key=f"comment_{criteria_id}"
                        )
                        criteria_data = {
                            "id": criteria_id,
                            "parent_id": item["id"],
                            "type": "fail",
                            "criteria": criteria,
                            "comment": comment
                        }
                        existing_idx = next((i for i, x in enumerate(st.session_state[f"selected_criteria_{item['id']}"])
                                             if x["id"] == criteria_id), None)
                        if existing_idx is not None:
                            st.session_state[f"selected_criteria_{item['id']}"][existing_idx] = criteria_data
                        else:
                            st.session_state[f"selected_criteria_{item['id']}"].append(criteria_data)
                    else:
                        st.session_state[f"selected_criteria_{item['id']}"] = [
                            x for x in st.session_state[f"selected_criteria_{item['id']}"] if x["id"] != criteria_id
                        ]
            # Update the primary selected_criteria collection for the prompt
            if st.session_state[f"selected_criteria_{item['id']}"]:
                existing_item = next((x for x in st.session_state.selected_criteria if x["id"] == item["id"]), None)
                if existing_item:
                    existing_item["selected_criteria"] = st.session_state[f"selected_criteria_{item['id']}"]
                else:
                    st.session_state.selected_criteria.append({
                        "id": item["id"],
                        "title": item["description"],
                        "selected_criteria": st.session_state[f"selected_criteria_{item['id']}"]
                    })
            else:
                st.session_state.selected_criteria = [
                    x for x in st.session_state.selected_criteria if x["id"] != item["id"]
                ]
            st.markdown("---")

    # --- Additional Feedback Section ---
    st.header("Additional Feedback")
    failing_feedback = st.text_area(
        "Failing Criteria Feedback (if applicable)",
        height=150,
        help="Provide specific feedback for criteria that were not met."
    )
    learner_feedback = st.text_area(
        "Learner-Requested Items Feedback (if applicable)",
        height=150,
        help="Provide feedback for specific questions or concerns raised by the learner."
    )
    st.markdown("---")

    # --- Generated Feedback Section ---
    st.header("Generated Feedback")
    if generate_button:
        if not st.session_state.selected_criteria:
            st.error("Please select at least one marking criteria.")
        else:
            prompt = construct_prompt(
                st.session_state.selected_criteria,
                failing_feedback,
                learner_feedback,
                feedback_examples
            )
            if DEBUG:
                debug_log("Generated Prompt", prompt)
            with st.spinner(f"Generating feedback using {selected_llm}..."):
                start_time = time.time()
                if selected_llm == "Gemini 2.0 Flash":
                    feedback = run_gemini_flash(prompt)
                elif selected_llm == "Gemini 2.5 Pro":
                    feedback = run_gemini_pro(prompt)
                elif selected_llm == "Deepseek R1 (Together)":
                    feedback = run_deepseek_r1_together(prompt)
                elif selected_llm == "Llama 4 Scout (KlusterAI)":
                    feedback = run_llama4_scout_klusterai(prompt)
                elif selected_llm == "Ollama Gemma 3":
                    feedback = run_ollama_gemma3(prompt)
                elif selected_llm == "Ollama Deepseek R1":
                    feedback = run_ollama_deepseek(prompt)
                elif selected_llm == "Ollama Llama 3.2":
                    feedback = run_ollama_llama(prompt)
                else:
                    feedback = "Error: Selected LLM not implemented"
                end_time = time.time()
            st.markdown(feedback)
            st.caption(f"Generated in {end_time - start_time:.2f} seconds")
            st.download_button(
                label="Download Feedback",
                data=feedback,
                file_name="course_project_feedback.md",
                mime="text/markdown"
            )

if __name__ == "__main__":
    main()