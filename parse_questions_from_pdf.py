#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parse questions from PDF and answers from TXT, then combine them
"""

import re
import json
import sys

try:
    import pdfplumber
    PDF_LIB = 'pdfplumber'
except ImportError:
    try:
        import PyPDF2
        PDF_LIB = 'PyPDF2'
    except ImportError:
        print("PDF kütüphanesi bulunamadı. Lütfen şunlardan birini yükleyin:")
        print("  pip install pdfplumber")
        print("  veya")
        print("  pip install PyPDF2")
        sys.exit(1)

def extract_text_from_pdf(pdf_path):
    """PDF'den metni çıkar"""
    text = ""
    
    if PDF_LIB == 'pdfplumber':
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    else:  # PyPDF2
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
    
    return text

def parse_questions_from_pdf(pdf_text):
    """PDF metninden soruları parse et"""
    questions = []
    
    # Soru pattern'i: "Question #1", "Question #2", vb.
    # Şık pattern'i: "A.", "B.", "C.", "D."
    
    # Tüm metni satırlara böl
    lines = pdf_text.split('\n')
    
    current_question = None
    current_option = None
    in_question = False
    in_options = False
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Soru başlangıcı: "Question #1" veya "Question #1 Topic"
        q_match = re.search(r'Question\s+#(\d+)', line, re.IGNORECASE)
        if q_match:
            # Önceki soruyu kaydet
            if current_question and len(current_question['options']) >= 2:
                questions.append(current_question)
            
            # Yeni soru başlat
            q_num = int(q_match.group(1))
            # Soru metni bu satırda veya sonraki satırlarda olabilir
            question_text = line
            # "Question #X" kısmını çıkar
            question_text = re.sub(r'Question\s+#\d+.*?Topic\s+\d+\s*', '', question_text, flags=re.IGNORECASE).strip()
            
            current_question = {
                'id': q_num,
                'question': question_text,
                'options': {},
                'correct_answer': None,
                'answer_text': '',
                'solution': ''
            }
            in_question = True
            in_options = False
            current_option = None
        
        elif current_question:
            # Şık kontrolü: "A.", "B.", "C.", "D." ile başlayan satırlar
            option_match = re.match(r'^([A-F])\.\s*(.+)', line)
            if option_match:
                letter = option_match.group(1).upper()
                option_text = option_match.group(2).strip()
                
                # Şık metni çok kısa ise, sonraki satırları da al
                j = i + 1
                while j < len(lines):
                    next_line = lines[j].strip()
                    # Yeni şık, yeni soru veya boş satır varsa dur
                    if (not next_line or 
                        re.match(r'^([A-F])\.', next_line) or 
                        re.search(r'Question\s+#\d+', next_line, re.IGNORECASE)):
                        break
                    # Şık metnine ekle
                    option_text += " " + next_line
                    j += 1
                
                current_question['options'][letter] = option_text
                in_options = True
                in_question = False
                current_option = letter
                i = j - 1  # j'yi i'ye atla (while döngüsü i'yi artıracak)
            
            # Soru metni devam ediyor (şık başlamadan önce)
            elif in_question and not in_options:
                # Yeni soru veya şık başlamadıysa, soru metnine ekle
                if not re.match(r'^([A-F])\.', line) and not re.search(r'Question\s+#\d+', line, re.IGNORECASE):
                    if line:  # Boş satır değilse
                        if current_question['question']:
                            current_question['question'] += " " + line
                        else:
                            current_question['question'] = line
        
        i += 1
    
    # Son soruyu ekle
    if current_question and len(current_question['options']) >= 2:
        questions.append(current_question)
    
    # Soru metinlerini temizle
    for q in questions:
        if q['question']:
            q['question'] = ' '.join(q['question'].split())
        # Şık metinlerini temizle
        for letter in q['options']:
            q['options'][letter] = ' '.join(q['options'][letter].split())
    
    return questions

def parse_answers_from_txt(txt_path):
    """TXT dosyasından cevapları parse et"""
    with open(txt_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    answers = {}
    
    # Soru numarası ve cevap pattern'i
    question_blocks = re.split(r'-{20,}', content)
    
    for block in question_blocks:
        block = block.strip()
        if not block:
            continue
        
        # Soru numarası bul
        q_match = re.match(r'^(\d+)\]', block)
        if not q_match:
            continue
        
        q_num = int(q_match.group(1))
        
        # Cevap satırını bul
        ans_match = re.search(r'ans[-:]?\s*([^\n]+)', block, re.IGNORECASE)
        if ans_match:
            answer_text = ans_match.group(1).strip()
        else:
            # "ans-" ile başlayan satırı bul
            lines = block.split('\n')
            answer_text = ""
            for line in lines:
                if line.strip().startswith('ans-') or line.strip().startswith('ans '):
                    answer_text = line[4:].strip()
                    break
        
        # Çözüm metnini bul
        solution_start = block.find('ans-') if 'ans-' in block.lower() else block.find('ans ')
        if solution_start == -1:
            solution_start = block.find(answer_text) if answer_text else len(block)
        
        solution_text = block[solution_start + len(answer_text):].strip()
        # Separator'ları temizle
        solution_text = re.sub(r'-+$', '', solution_text, flags=re.MULTILINE).strip()
        
        # Doğru cevap harfini bul
        correct_answer = None
        
        # Cevap metninde harf ara
        answer_upper = answer_text.upper()
        for letter in ['A', 'B', 'C', 'D', 'E', 'F']:
            if (f' {letter}.' in answer_text or 
                f'Option {letter}' in answer_text or 
                f'answer {letter}' in answer_upper or
                answer_text.strip().startswith(letter + '.') or
                answer_text.strip().startswith(letter + ' ')):
                correct_answer = letter
                break
        
        # Çözüm metninde de ara
        if not correct_answer and solution_text:
            sol_match = re.search(r'(?:Correct answer|Option|answer)\s+([A-Z])', solution_text, re.IGNORECASE)
            if sol_match:
                correct_answer = sol_match.group(1)
        
        answers[q_num] = {
            'correct_answer': correct_answer,
            'answer_text': answer_text,
            'solution': solution_text
        }
    
    return answers

def combine_questions_and_answers(questions, answers):
    """Soruları ve cevapları birleştir"""
    combined = []
    
    for q in questions:
        q_id = q['id']
        if q_id in answers:
            q['correct_answer'] = answers[q_id]['correct_answer']
            q['answer_text'] = answers[q_id]['answer_text']
            q['solution'] = answers[q_id]['solution']
        
        # En az 2 şık ve doğru cevap olmalı
        if len(q['options']) >= 2 and q['correct_answer']:
            combined.append(q)
    
    return combined

def main():
    pdf_path = 'AWS Certified Solutions Architect Associate SAA-C03.pdf'
    txt_path = 'AWS SAA-03 Solution.txt'
    output_file = 'questions.json'
    
    print(f"PDF'den sorular parse ediliyor: {pdf_path}")
    try:
        pdf_text = extract_text_from_pdf(pdf_path)
        print(f"PDF metni çıkarıldı ({len(pdf_text)} karakter)")
        
        questions = parse_questions_from_pdf(pdf_text)
        print(f"PDF'den {len(questions)} soru bulundu")
        
        # İlk birkaç soruyu göster
        if questions:
            print(f"\nİlk 3 soru örneği:")
            for q in questions[:3]:
                print(f"  Soru #{q['id']}: {len(q['options'])} şık - {list(q['options'].keys())}")
    except Exception as e:
        print(f"PDF parse hatası: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print(f"\nTXT'den cevaplar parse ediliyor: {txt_path}")
    try:
        answers = parse_answers_from_txt(txt_path)
        print(f"TXT'den {len(answers)} cevap bulundu")
    except Exception as e:
        print(f"TXT parse hatası: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print(f"\nSorular ve cevaplar birleştiriliyor...")
    combined = combine_questions_and_answers(questions, answers)
    
    print(f"\nToplam {len(combined)} geçerli soru oluşturuldu")
    
    # JSON'a kaydet
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(combined, f, ensure_ascii=False, indent=2)
    
    print(f"Sonuçlar {output_file} dosyasına kaydedildi")
    
    # Örnek göster
    if combined:
        sample = combined[0]
        print(f"\nÖrnek soru:")
        print(f"ID: {sample['id']}")
        print(f"Soru: {sample['question'][:100]}...")
        print(f"Şıklar: {list(sample['options'].keys())}")
        print(f"Doğru cevap: {sample['correct_answer']}")

if __name__ == '__main__':
    main()
