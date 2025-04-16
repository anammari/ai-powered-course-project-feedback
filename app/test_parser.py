import re

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
                print(f"Found section: {current_section}")
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
                print(f"  Found part: {current_id} - {current_title}")
                pass_criteria = []
                fail_criteria = []
                continue
            
            # Check for pass criteria
            pass_match = re.match(r'- \[\s?\]\s*\*\*Pass\*\*:\s*(.*)', line)
            if pass_match and current_part is not None:
                pass_text = pass_match.group(1).strip()
                pass_criteria.append(pass_text)
                print(f"    Found pass criteria: {pass_text[:30]}...")
                continue
            
            # Check for fail criteria
            fail_match = re.match(r'- \[\s?\]\s*\*\*Fail\*\*:\s*(.*)', line)
            if fail_match and current_part is not None:
                fail_text = fail_match.group(1).strip()
                fail_criteria.append(fail_text)
                print(f"    Found fail criteria: {fail_text[:30]}...")
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
        
        print(f"\nTotal criteria items found: {len(criteria)}")
        return criteria
        
    except Exception as e:
        print(f"Error parsing marking criteria: {str(e)}")
        return []

if __name__ == "__main__":
    criteria = parse_marking_criteria()
    
    # Print a summary of what was found
    for item in criteria:
        print(f"\n{item['id']}: {item['title']}")
        print(f"  Section: {item['section']}")
        print(f"  Pass criteria: {len(item['pass_criteria'])}")
        print(f"  Fail criteria: {len(item['fail_criteria'])}")