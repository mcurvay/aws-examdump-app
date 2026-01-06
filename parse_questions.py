#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parse questions from AWS SAA-03 Solution.txt and convert to JSON format
"""

import re
import json

def parse_questions(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    questions = []
    current_question = None
    current_block = []
    in_solution = False
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Check if this is a new question (starts with number])
        q_match = re.match(r'^(\d+)\]', line)
        if q_match:
            # Save previous question if exists
            if current_question:
                questions.append(current_question)
            
            # Start new question
            q_num = int(q_match.group(1))
            question_text = line[len(q_match.group(0)):].strip()
            current_block = [question_text]
            in_solution = False
            current_question = {
                'id': q_num,
                'question': question_text,
                'options': {},
                'correct_answer': None,
                'answer_text': '',
                'solution': ''
            }
        elif current_question:
            # Check for separator line
            if re.match(r'^-+$', line):
                # End of question block
                if current_question['solution']:
                    # Already have solution, this is just separator
                    pass
                i += 1
                continue
            
            # Check for answer line
            if line.startswith('ans-') or line.startswith('ans '):
                in_solution = True
                answer_text = line[4:].strip() if line.startswith('ans-') else line[4:].strip()
                current_question['answer_text'] = answer_text
                
                # Try to extract answer letter from answer text
                # Look for patterns like "A.", "Option A", "answer A", etc.
                answer_upper = answer_text.upper()
                for letter in ['A', 'B', 'C', 'D', 'E', 'F']:
                    if (f' {letter}.' in answer_text or 
                        f'Option {letter}' in answer_text or 
                        f'answer {letter}' in answer_upper or
                        answer_text.strip().startswith(letter + '.') or
                        answer_text.strip().startswith(letter + ' ')):
                        if letter in current_question['options']:
                            current_question['correct_answer'] = letter
                            break
                
                # If answer text starts with a letter, use it
                if not current_question['correct_answer']:
                    first_char = answer_text.strip()[0] if answer_text.strip() else ''
                    if first_char in ['A', 'B', 'C', 'D', 'E', 'F'] and first_char in current_question['options']:
                        current_question['correct_answer'] = first_char
            elif in_solution:
                # Collect solution text
                if current_question['solution']:
                    current_question['solution'] += '\n' + line
                else:
                    current_question['solution'] = line
            else:
                # Check if this is an option line (A., B., C., D., etc.)
                option_match = re.match(r'^([A-Z])\.\s*(.+)', line)
                if option_match:
                    letter = option_match.group(1)
                    option_text = option_match.group(2).strip()
                    current_question['options'][letter] = option_text
                    
                    # Check if answer text matches this option
                    if not current_question['correct_answer']:
                        answer_lower = current_question['answer_text'].lower()
                        option_lower = option_text.lower()
                        # Check if answer contains option text or vice versa
                        if (option_lower[:30] in answer_lower or 
                            answer_lower[:30] in option_lower or
                            any(word in answer_lower for word in option_text.split()[:3] if len(word) > 4)):
                            current_question['correct_answer'] = letter
                else:
                    # Continue question text
                    if not current_question['options']:
                        # Still in question text
                        if current_question['question']:
                            current_question['question'] += ' ' + line
                        else:
                            current_question['question'] = line
                    elif line and not line.startswith('Correct answer') and not line.startswith('Option'):
                        # Might be additional context or solution starting
                        # Check if it looks like solution (contains explanation words)
                        solution_keywords = ['because', 'allows', 'provides', 'enables', 'solution', 'requirement']
                        if any(keyword in line.lower() for keyword in solution_keywords):
                            in_solution = True
                            current_question['solution'] = line
        
        i += 1
    
    # Add last question
    if current_question:
        questions.append(current_question)
    
    # Post-process: Try to find correct answer from solution text if not found
    for q in questions:
        if not q['correct_answer'] and q['solution']:
            # Look for "Correct answer A", "Option A", etc. in solution
            sol_match = re.search(r'(?:Correct answer|Option|answer)\s+([A-Z])', q['solution'], re.IGNORECASE)
            if sol_match:
                letter = sol_match.group(1)
                if letter in q['options']:
                    q['correct_answer'] = letter
        
        # Clean up question text
        if q['question']:
            q['question'] = ' '.join(q['question'].split())
        
        # If still no correct answer, try matching answer text with options
        if not q['correct_answer'] and q['answer_text'] and q['options']:
            answer_words = set(q['answer_text'].lower().split())
            best_match = None
            best_score = 0
            for letter, opt_text in q['options'].items():
                opt_words = set(opt_text.lower().split())
                common = len(answer_words & opt_words)
                if common > best_score and common > 2:
                    best_score = common
                    best_match = letter
            if best_match:
                q['correct_answer'] = best_match
    
    return questions

def main():
    input_file = 'AWS SAA-03 Solution.txt'
    output_file = 'questions.json'
    
    print(f"Parsing questions from {input_file}...")
    questions = parse_questions(input_file)
    
    # Filter out questions without options or correct answer
    valid_questions = [q for q in questions if q['options'] and q['correct_answer']]
    
    print(f"Found {len(questions)} total questions")
    print(f"Found {len(valid_questions)} valid questions with options and correct answer")
    
    # Save to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(valid_questions, f, ensure_ascii=False, indent=2)
    
    print(f"Saved {len(valid_questions)} questions to {output_file}")
    
    # Print sample
    if valid_questions:
        print("\nSample question:")
        sample = valid_questions[0]
        print(f"ID: {sample['id']}")
        print(f"Question: {sample['question'][:100]}...")
        print(f"Options: {list(sample['options'].keys())}")
        print(f"Correct: {sample['correct_answer']}")

if __name__ == '__main__':
    main()
