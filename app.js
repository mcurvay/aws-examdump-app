// Application state
let questions = [];
let currentQuestion = null;
let selectedAnswer = null;
let questionAnswered = false;
let sessionStats = {
    correct: 0,
    wrong: 0,
    total: 0
};

// Question tracking for spaced repetition
let questionStats = {}; // {questionId: {correct: count, wrong: count, lastSeen: timestamp}}

// Initialize application
async function init() {
    // Load session stats from localStorage
    loadSessionStats();
    
    // Load question stats from localStorage
    loadQuestionStats();
    
    // Load questions
    try {
        const response = await fetch('questions.json');
        questions = await response.json();
        
        // Filter questions that have at least 2 options
        questions = questions.filter(q => Object.keys(q.options).length >= 2);
        
        console.log(`Loaded ${questions.length} questions`);
        
        // Initialize question stats for new questions
        questions.forEach(q => {
            if (!questionStats[q.id]) {
                questionStats[q.id] = {
                    correct: 0,
                    wrong: 0,
                    lastSeen: 0,
                    priority: 0 // Higher priority = show more often
                };
            }
        });
        
        // Start with first question
        nextQuestion();
    } catch (error) {
        console.error('Error loading questions:', error);
        document.getElementById('question-text').textContent = 
            'Sorular yüklenirken bir hata oluştu. Lütfen questions.json dosyasının mevcut olduğundan emin olun.';
    }
}

// Load session stats from localStorage
function loadSessionStats() {
    const saved = localStorage.getItem('sessionStats');
    if (saved) {
        sessionStats = JSON.parse(saved);
        updateStatsDisplay();
    }
}

// Save session stats to localStorage
function saveSessionStats() {
    localStorage.setItem('sessionStats', JSON.stringify(sessionStats));
}

// Load question stats from localStorage
function loadQuestionStats() {
    const saved = localStorage.getItem('questionStats');
    if (saved) {
        questionStats = JSON.parse(saved);
    }
}

// Save question stats to localStorage
function saveQuestionStats() {
    localStorage.setItem('questionStats', JSON.stringify(questionStats));
}

// Update stats display
function updateStatsDisplay() {
    document.getElementById('correct-count').textContent = sessionStats.correct;
    document.getElementById('wrong-count').textContent = sessionStats.wrong;
    document.getElementById('total-count').textContent = sessionStats.total;
}

// Reset session stats (doğru/yanlış sayılarını sıfırla)
function resetSessionStats() {
    // Kullanıcıya onay sor
    const confirmed = confirm(
        `Testi bitirmek ve istatistikleri sıfırlamak istediğinize emin misiniz?\n\n` +
        `Mevcut Durum:\n` +
        `✅ Doğru: ${sessionStats.correct}\n` +
        `❌ Yanlış: ${sessionStats.wrong}\n` +
        `📊 Toplam: ${sessionStats.total}\n\n` +
        `Not: Soru istatistikleri (hangi soruları yanlış yaptığınız) korunacak, sadece oturum sayıları sıfırlanacak.`
    );
    
    if (confirmed) {
        // Session stats'ı sıfırla
        sessionStats = {
            correct: 0,
            wrong: 0,
            total: 0
        };
        
        // localStorage'dan session stats'ı sil
        localStorage.removeItem('sessionStats');
        
        // Ekranı güncelle
        updateStatsDisplay();
        
        // Kullanıcıya bilgi ver
        alert('✅ Test tamamlandı ve istatistikler sıfırlandı!\n\nYeni bir test başlatabilirsiniz.');
        
        console.log('Session stats reset:', sessionStats);
    }
}

// Get next question using spaced repetition algorithm
function getNextQuestion() {
    if (questions.length === 0) return null;
    
    // Calculate priority for each question
    const now = Date.now();
    questions.forEach(q => {
        const stats = questionStats[q.id];
        if (!stats) {
            // Yeni sorular için varsayılan değerler
            questionStats[q.id] = {
                correct: 0,
                wrong: 0,
                lastSeen: 0,
                priority: 0
            };
            return;
        }
        
        // ÖNCELİK HESAPLAMA (Yanlış sorular daha yüksek öncelik alır):
        // 1. Yanlış cevap ağırlığı: Her yanlış cevap +20 puan (daha agresif)
        //    - 1 yanlış = 20 puan
        //    - 2 yanlış = 40 puan
        //    - 3 yanlış = 60 puan
        const wrongWeight = stats.wrong * 20;
        
        // 2. Doğru cevap ağırlığı: Her doğru cevap -3 puan (daha az etkili)
        //    - Çok doğru yapılan sorular daha az öncelik alır
        const correctWeight = -stats.correct * 3;
        
        // 3. Zaman ağırlığı: Uzun süredir görülmeyen sorular +5 puan
        //    - Son görülme zamanından bu yana geçen saat başına 1 puan (max 5)
        const timeSinceLastSeen = now - stats.lastSeen;
        const timeWeight = Math.min(timeSinceLastSeen / (1000 * 60 * 60), 5);
        
        // 4. Özel bonus: Yanlış yapılan ama henüz doğru yapılmayan sorular
        //    - Eğer yanlış > 0 ve correct = 0 ise ekstra +30 puan
        let bonus = 0;
        if (stats.wrong > 0 && stats.correct === 0) {
            bonus = 30; // Hiç doğru yapılmamış yanlış sorular çok yüksek öncelik
        }
        
        // Toplam öncelik = Yanlış ağırlığı + Doğru ağırlığı + Zaman ağırlığı + Bonus
        stats.priority = wrongWeight + correctWeight + timeWeight + bonus;
    });
    
    // Soruları önceliğe göre sırala (en yüksek öncelik önce)
    const sortedQuestions = [...questions].sort((a, b) => {
        const priorityA = questionStats[a.id]?.priority || 0;
        const priorityB = questionStats[b.id]?.priority || 0;
        return priorityB - priorityA; // Yüksek öncelik önce
    });
    
    // En yüksek öncelikli sorulardan seç (top %30 veya en az 15 soru)
    // Bu sayede yanlış yapılan sorular daha sık gelir
    const topCount = Math.max(15, Math.floor(sortedQuestions.length * 0.3));
    const topQuestions = sortedQuestions.slice(0, topCount);
    
    // En yüksek öncelikli sorulardan rastgele birini seç
    // Ama ilk %10'dan seçme şansı daha yüksek (yanlış sorular)
    const highPriorityCount = Math.max(5, Math.floor(topQuestions.length * 0.3));
    const highPriorityQuestions = topQuestions.slice(0, highPriorityCount);
    
    // %70 ihtimalle en yüksek öncelikli sorulardan, %30 ihtimalle diğerlerinden seç
    if (Math.random() < 0.7 && highPriorityQuestions.length > 0) {
        const randomIndex = Math.floor(Math.random() * highPriorityQuestions.length);
        return highPriorityQuestions[randomIndex];
    } else {
        const randomIndex = Math.floor(Math.random() * topQuestions.length);
        return topQuestions[randomIndex];
    }
}

// Display question
function displayQuestion(question) {
    currentQuestion = question;
    selectedAnswer = null;
    questionAnswered = false;
    
    // Update question number and progress
    const questionIndex = questions.findIndex(q => q.id === question.id) + 1;
    document.getElementById('question-number').textContent = `Soru #${question.id}`;
    document.getElementById('question-progress').textContent = 
        `${questionIndex} / ${questions.length}`;
    
    // Display question text
    document.getElementById('question-text').textContent = question.question;
    
    // Display domain information
    const domainBadge = document.getElementById('domain-badge');
    const domainName = document.getElementById('domain-name');
    if (question.domain) {
        domainName.textContent = question.domain;
        domainBadge.style.display = 'flex';
        
        // Add domain-specific class for styling
        domainBadge.className = 'domain-badge';
        const domainShort = question.domain_short || '';
        domainBadge.classList.add(`domain-${domainShort.toLowerCase()}`);
    } else {
        domainBadge.style.display = 'none';
    }
    
    // Display options
    const optionsContainer = document.getElementById('options-container');
    optionsContainer.innerHTML = '';
    
    // Sort options by letter (A, B, C, D, etc.)
    const optionLetters = Object.keys(question.options).sort();
    
    optionLetters.forEach(letter => {
        const optionDiv = document.createElement('div');
        optionDiv.className = 'option';
        optionDiv.id = `option-${letter}`;
        
        const radio = document.createElement('input');
        radio.type = 'radio';
        radio.name = 'answer';
        radio.value = letter;
        radio.id = `radio-${letter}`;
        radio.onclick = () => selectAnswer(letter);
        
        const label = document.createElement('label');
        label.htmlFor = `radio-${letter}`;
        label.textContent = `${letter}. ${question.options[letter]}`;
        
        optionDiv.appendChild(radio);
        optionDiv.appendChild(label);
        optionsContainer.appendChild(optionDiv);
    });
    
    // Hide feedback and solution
    document.getElementById('feedback-container').style.display = 'none';
    document.getElementById('solution-container').style.display = 'none';
    
    // Show check button, hide next button
    document.getElementById('check-button').style.display = 'inline-block';
    document.getElementById('next-button').style.display = 'none';
    
    // Update last seen timestamp
    if (questionStats[question.id]) {
        questionStats[question.id].lastSeen = Date.now();
        saveQuestionStats();
    }
}

// Select answer
function selectAnswer(letter) {
    if (questionAnswered) return;
    
    selectedAnswer = letter;
    
    // Update UI
    document.querySelectorAll('.option').forEach(opt => {
        opt.classList.remove('selected');
    });
    
    const selectedOption = document.getElementById(`option-${letter}`);
    if (selectedOption) {
        selectedOption.classList.add('selected');
    }
    
    // Enable check button
    document.getElementById('check-button').disabled = false;
}

// Check answer
function checkAnswer() {
    if (!currentQuestion || !selectedAnswer || questionAnswered) return;
    
    questionAnswered = true;
    const isCorrect = selectedAnswer === currentQuestion.correct_answer;
    
    // Update question stats
    if (questionStats[currentQuestion.id]) {
        if (isCorrect) {
            questionStats[currentQuestion.id].correct++;
        } else {
            questionStats[currentQuestion.id].wrong++;
        }
        saveQuestionStats();
    }
    
    // Update session stats
    if (isCorrect) {
        sessionStats.correct++;
    } else {
        sessionStats.wrong++;
    }
    sessionStats.total++;
    saveSessionStats();
    updateStatsDisplay();
    
    // Show feedback
    const feedbackContainer = document.getElementById('feedback-container');
    const feedbackMessage = document.getElementById('feedback-message');
    const solutionContainer = document.getElementById('solution-container');
    const solutionText = document.getElementById('solution-text');
    
    feedbackContainer.style.display = 'block';
    
    if (isCorrect) {
        feedbackMessage.textContent = '✓ Doğru!';
        feedbackMessage.className = 'feedback-message correct';
    } else {
        feedbackMessage.textContent = '✗ Yanlış!';
        feedbackMessage.className = 'feedback-message wrong';
    }
    
    // Highlight correct and wrong answers
    document.querySelectorAll('.option').forEach(opt => {
        opt.classList.remove('correct-answer', 'wrong-answer');
        const optionLetter = opt.id.replace('option-', '');
        
        if (optionLetter === currentQuestion.correct_answer) {
            opt.classList.add('correct-answer');
        } else if (optionLetter === selectedAnswer && !isCorrect) {
            opt.classList.add('wrong-answer');
        }
    });
    
    // Show solution if available
    if (currentQuestion.solution && currentQuestion.solution.trim()) {
        solutionContainer.style.display = 'block';
        solutionText.textContent = currentQuestion.solution;
    } else if (currentQuestion.answer_text && currentQuestion.answer_text.trim()) {
        solutionContainer.style.display = 'block';
        solutionText.textContent = `Doğru Cevap: ${currentQuestion.answer_text}`;
    }
    
    // Hide check button, show next button
    document.getElementById('check-button').style.display = 'none';
    document.getElementById('next-button').style.display = 'inline-block';
}

// Next question
function nextQuestion() {
    const nextQ = getNextQuestion();
    if (nextQ) {
        displayQuestion(nextQ);
    } else {
        // No more questions
        document.getElementById('question-text').textContent = 
            'Tüm sorular tamamlandı! Tebrikler!';
        document.getElementById('options-container').innerHTML = '';
        document.getElementById('feedback-container').style.display = 'none';
        document.getElementById('check-button').style.display = 'none';
        document.getElementById('next-button').style.display = 'none';
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', init);

