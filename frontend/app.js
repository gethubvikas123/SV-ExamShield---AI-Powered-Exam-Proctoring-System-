// Configuration
const API_URL = 'http://localhost:8000';

// PROCTORING & CHEAT DETECTION SETTINGS
const MAX_VIOLATIONS_BEFORE_WARNING = 3;
const MAX_VIOLATIONS_BEFORE_TERMINATION = 5;
const ENABLE_AUTO_TERMINATION = true;
const ENABLE_TAB_SWITCH_DETECTION = true;
const ENABLE_KEYBOARD_BLOCKING = true;

// TIMER SETTINGS
const TIME_PER_QUESTION = 60; // seconds (1 minute per question)

// Global state
let currentUser = null;
let currentExam = null;
let questions = [];
let currentQuestionIndex = 0;
let userAnswers = {};
let violations = [];
let videoStream = null;
let proctoringInterval = null;
let timerInterval = null;
let examStartTime = null;
let violationCount = { high: 0, medium: 0, low: 0, total: 0, tabSwitch: 0 };
let cheatDetectionActive = false;
let ignoreNextBlur = false;
let requestedQuestionCount = 20;
let lastGeneratedSubject = null;

// NEW: Timer variables
let examTimeLimit = 0;
let examCountdownInterval = null;
let timeRemaining = 0;

// NEW: Prevent double submission
let submittingAnswers = new Set();
let lastSubmittedAnswer = null;
let lastSubmittedTime = 0;
let clickTimeout = null;
// Utility functions
function showPage(pageId) {
    document.querySelectorAll('[id$="Page"]').forEach(page => {
        page.classList.remove('active');
    });
    document.getElementById(pageId).classList.add('active');
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Input validation and sanitization
function validateAndSanitize(input) {
    if (!input || typeof input !== 'string') {
        return '';
    }
    return input.trim().replace(/\s+/g, ' ');
}

function validateForm(formData) {
    const errors = [];
    
    for (const [key, value] of Object.entries(formData)) {
        const sanitized = validateAndSanitize(value);
        
        if (!sanitized) {
            errors.push(`${key} cannot be empty`);
        }
        
        formData[key] = sanitized;
    }
    
    return { isValid: errors.length === 0, errors, data: formData };
}

function showRegister() {
    alertify.prompt('Register', 'Enter username, password (comma-separated)', 
        function(evt, value) {
            const parts = value.split(',').map(s => validateAndSanitize(s));
            
            if (parts.length < 2 || !parts[0] || !parts[1]) {
                alertify.error('Invalid format. Use: username, password');
                return;
            }
            
            register(parts[0], parts[1], parts[2] || '');
        }, 
        function() {
            alertify.error('Registration cancelled');
        }
    );
}

// Cheat Detection System
function startCheatDetection() {
    if (!ENABLE_TAB_SWITCH_DETECTION && !ENABLE_KEYBOARD_BLOCKING) {
        return;
    }
    
    cheatDetectionActive = true;
    ignoreNextBlur = true;
    
    alertify.alert(
        '⚠️ Anti-Cheating Measures Active',
        'The following are monitored during the exam:\n\n' +
        '• Tab switching\n' +
        '• Right-click disabled\n' +
        '• Copy/Paste blocked\n' +
        '• Developer tools blocked\n' +
        '• Face and object detection\n\n' +
        'Violations will be logged and may result in exam termination.',
        function() { ignoreNextBlur = false; }
    );
    
    if (ENABLE_TAB_SWITCH_DETECTION) {
        window.addEventListener('blur', handleTabSwitch);
        document.addEventListener('visibilitychange', handleVisibilityChange);
    }
    
    document.addEventListener('contextmenu', handleContextMenu);
    
    if (ENABLE_KEYBOARD_BLOCKING) {
        document.addEventListener('keydown', handleKeyboardShortcuts);
    }
    
    console.log('🔒 Cheat detection activated');
}

function handleTabSwitch() {
    if (!cheatDetectionActive) return;
    
    if (ignoreNextBlur) {
        ignoreNextBlur = false;
        return;
    }
    
    violationCount.tabSwitch++;
    violationCount.total++;
    
    const violation = {
        type: 'tab_switch',
        severity: 'high',
        message: `Tab switch detected (${violationCount.tabSwitch} times)`,
        timestamp: new Date().toLocaleTimeString()
    };
    
    addViolation(violation);
    logViolation(violation.type, violation.severity, violation.message);
    
    alertify.error('⚠️ Warning: Tab switching detected! Stay on exam page.');
    checkViolationLimit();
}

function handleVisibilityChange() {
    if (!cheatDetectionActive) return;
    if (document.hidden) {
        handleTabSwitch();
    }
}

function handleContextMenu(e) {
    e.preventDefault();
    alertify.warning('Right-click is disabled during the exam!');
    return false;
}

function handleKeyboardShortcuts(e) {
    const forbidden = [
        (e.ctrlKey && e.key === 'c'),
        (e.ctrlKey && e.key === 'v'),
        (e.ctrlKey && e.shiftKey && e.key.toLowerCase() === 'i'),
        (e.key === 'F12'),
        (e.ctrlKey && e.key === 'u'),
        (e.ctrlKey && e.shiftKey && e.key.toLowerCase() === 'j'),
        (e.ctrlKey && e.shiftKey && e.key.toLowerCase() === 'c'),
    ];
    
    if (forbidden.some(condition => condition)) {
        e.preventDefault();
        e.stopPropagation();
        alertify.error('⚠️ Cheating attempt detected! This action is blocked.');
        
        const violation = {
            type: 'keyboard_shortcut_blocked',
            severity: 'medium',
            message: `Blocked keyboard shortcut: ${e.key}`,
            timestamp: new Date().toLocaleTimeString()
        };
        
        addViolation(violation);
        logViolation(violation.type, violation.severity, violation.message);
        
        return false;
    }
}

function myFunction() {
  var x = document.getElementById("loginPassword");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}

function stopCheatDetection() {
    cheatDetectionActive = false;
    
    window.removeEventListener('blur', handleTabSwitch);
    document.removeEventListener('visibilitychange', handleVisibilityChange);
    document.removeEventListener('contextmenu', handleContextMenu);
    document.removeEventListener('keydown', handleKeyboardShortcuts);
    
    console.log('🔓 Cheat detection deactivated');
}

// API Functions
async function register(username, password, email) {
    try {
        const response = await fetch(`${API_URL}/api/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password, email })
        });
        
        if (response.ok) {
            alertify.success('Registration successful! Please login.');
        } else {
            const error = await response.json();
            alertify.error(error.detail || 'Registration failed');
        }
    } catch (error) {
        alertify.error('Registration error: ' + error.message);
    }
}

async function login(username, password) {
    const validation = validateForm({ username, password });
    
    if (!validation.isValid) {
        alertify.error(validation.errors.join(', '));
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/api/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(validation.data)
        });
        
        if (response.ok) {
            const data = await response.json();
            currentUser = data;
            alertify.success(`Welcome, ${data.username}!`);
            
            if (data.is_admin) {
                showPage('adminPage');
            } else {
                startExamSetup();
            }
        } else {
            alertify.error('Invalid credentials');
        }
    } catch (error) {
        alertify.error('Login error: ' + error.message);
    }
}

async function loadQuestions(limit = 20, subject = null) {
    try {
        // Backend se thode zyada questions mangwayenge taaki filter karne ke baad questions kam na padein
        let fetchLimit = 50; 
        let url = `${API_URL}/api/questions?limit=${fetchLimit}`;
        
        if (subject) {
            url += `&subject=${encodeURIComponent(subject)}`;
        }
        
        const response = await fetch(url);
        const data = await response.json();
        
        // FIX: Duplicates aur "Sample" questions ko filter karna
        let uniqueQuestions = [];
        let seenTexts = new Set();
        
        data.questions.forEach(q => {
            const textLower = q.question_text.toLowerCase();
            
            // Agar question mein "sample" nahi likha hai aur ye pehle nahi aaya hai
            if (!textLower.includes('sample') && !seenTexts.has(textLower)) {
                uniqueQuestions.push(q);
                seenTexts.add(textLower); // Duplicate check karne ke liye save kar liya
            }
        });
        
        // FIX: Questions ko Randomly Shuffle (mix) kar do taaki har baar order alag ho
        uniqueQuestions.sort(() => Math.random() - 0.5);
        
        // Jitne questions chahiye the, utne hi select karo
        questions = uniqueQuestions.slice(0, limit);
        
        if (questions.length === 0) {
            alertify.error('No valid unique questions found. Please go to Admin and generate more!');
            return false;
        }
        
        console.log(`✅ Loaded ${questions.length} unique questions`);
        return true;
    } catch (error) {
        alertify.error('Failed to load questions');
        return false;
    }
}

async function startExam() {
    try {
        const response = await fetch(
            `${API_URL}/api/exam/start?user_id=${currentUser.user_id}&exam_name=General%20Exam`,
            {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            }
        );
        
        if (response.ok) {
            const data = await response.json();
            currentExam = data;
            return true;
        } else {
            const error = await response.json();
            console.error('Exam start error:', error);
            alertify.error('Failed to start exam: ' + (error.detail || 'Unknown error'));
            return false;
        }
    } catch (error) {
        console.error('Exam start exception:', error);
        alertify.error('Failed to start exam: ' + error.message);
        return false;
    }
}

async function submitAnswer(questionId, answer) {
    try {
        const response = await fetch(`${API_URL}/api/exam/submit`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                exam_id: currentExam.exam_id,
                question_id: questionId,
                user_answer: answer
            })
        });
        
        if (response.ok) {
            console.log(`Answer submitted: Q${questionId} = ${answer}`);
            return true;
        } else {
            console.error('Failed to submit answer');
            return false;
        }
    } catch (error) {
        console.error('Failed to submit answer:', error);
        return false;
    }
}

async function submitAllAnswersAndFinish(reason) {
    alertify.message('Submitting your answers, please wait...');
    
    // Local memory se saare answers nikal kar ek-ek karke backend ko bhejo
    for (const [questionId, answer] of Object.entries(userAnswers)) {
        await submitAnswer(questionId, answer);
    }
    
    // Sab answers save hone ke baad finally exam ko complete karo
    finishExam(reason);
}


async function finishExam(reason = 'completed') {
    try {
        const response = await fetch(
            `${API_URL}/api/exam/finish?exam_id=${currentExam.exam_id}`,
            {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            }
        );
        
        if (response.ok) {
            const data = await response.json();
            if (reason === 'violations') {
                alertify.error('Exam terminated due to excessive violations!');
            }
            await showResults(data, reason);
        }
    } catch (error) {
        alertify.error('Failed to finish exam');
    }
}

async function analyzeFrame(imageBlob) {
    try {
        const formData = new FormData();
        formData.append('file', imageBlob, 'frame.jpg');
        
        const response = await fetch(`${API_URL}/api/proctor/analyze`, {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const data = await response.json();
            handleViolations(data);
        }
    } catch (error) {
        console.error('Proctoring analysis failed:', error);
    }
}

async function logViolation(type, severity, description) {
    try {
        const formData = new FormData();
        formData.append('exam_id', currentExam.exam_id);
        formData.append('violation_type', type);
        formData.append('severity', severity);
        formData.append('description', description);
        
        await fetch(`${API_URL}/api/proctor/violation`, {
            method: 'POST',
            body: formData
        });
    } catch (error) {
        console.error('Failed to log violation:', error);
    }
}

// Exam Setup and Management
async function startExamSetup() {
    const loaded = await loadQuestions(requestedQuestionCount, lastGeneratedSubject);
    if (!loaded) {
        showPage('adminPage');
        alertify.error('Please generate questions first!');
        return;
    }
    
    const started = await startExam();
    if (!started) return;
    
    showPage('examPage');
    
    initializeCamera();
    startProctoring();
    startCheatDetection();
    startTimer();
    displayQuestion();
    
    // NEW: Start exam countdown timer
    startExamTimer();
    
    alertify.success(`Exam started with ${questions.length} questions`);
}

function showExamPage() {
    currentUser = { user_id: 1, username: 'student', is_admin: false };
    startExamSetup();
}


function displayQuestion() {
    if (currentQuestionIndex >= questions.length) return;
    
    const question = questions[currentQuestionIndex];
    const container = document.getElementById('questionContainer');
    const savedAnswer = userAnswers[question.id];
    
    container.innerHTML = `
        <div class="question-card">
            <h5 class="mb-4">Question ${currentQuestionIndex + 1} of ${questions.length}</h5>
            <p class="lead">${question.question_text}</p>
            <div class="options-grid mt-4">
                <button class="option-btn ${savedAnswer === 'A' ? 'selected' : ''}" 
                        onclick="handleOptionClick('${question.id}', 'A', this)"
                        data-question="${question.id}" data-option="A">
                    <strong>A.</strong> ${question.option_a}
                </button>
                <button class="option-btn ${savedAnswer === 'B' ? 'selected' : ''}" 
                        onclick="handleOptionClick('${question.id}', 'B', this)"
                        data-question="${question.id}" data-option="B">
                    <strong>B.</strong> ${question.option_b}
                </button>
                <button class="option-btn ${savedAnswer === 'C' ? 'selected' : ''}" 
                        onclick="handleOptionClick('${question.id}', 'C', this)"
                        data-question="${question.id}" data-option="C">
                    <strong>C.</strong> ${question.option_c}
                </button>
                <button class="option-btn ${savedAnswer === 'D' ? 'selected' : ''}" 
                        onclick="handleOptionClick('${question.id}', 'D', this)"
                        data-question="${question.id}" data-option="D">
                    <strong>D.</strong> ${question.option_d}
                </button>
            </div>
        </div>
    `;
    
    updateProgress();
    updateNavigationButtons();
}

// NEW: Debounced option click handler
function handleOptionClick(questionId, answer, button) {
    // 1. UI Update: Sabhi options se 'selected' class hatao
    document.querySelectorAll('.option-btn').forEach(btn => {
        btn.classList.remove('selected');
    });
    
    // 2. UI Update: Jis button par click kiya hai, turant usko highlight karo
    button.classList.add('selected');

    // 3. Data Update: Answer ko local memory mein save karo
    userAnswers[questionId] = answer;

    // // 4. Double-click (spam) submission rokne ki logic
    // const submitKey = `${questionId}-${answer}`;
    // if (submittingAnswers.has(submitKey)) {
    //     return; // Agar already submit ho raha hai, toh wahi ruk jao
    // }
    // submittingAnswers.add(submitKey);

    // // 5. Backend (API) ko answer bhejo
    // submitAnswer(questionId, answer).finally(() => {
    //     // 500 milliseconds baad button ko wapas normal state mein allow karo
    //     setTimeout(() => {
    //         submittingAnswers.delete(submitKey);
    //     }, 500);
    // });
}

// Track last submission time

function nextQuestion() {
    if (currentQuestionIndex < questions.length - 1) {
        currentQuestionIndex++;
        displayQuestion();
    }
}

function previousQuestion() {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        displayQuestion();
    }
}

function updateProgress() {
    const answered = Object.keys(userAnswers).length;
    const total = questions.length;
    const percent = Math.round((answered / total) * 100);
    
    document.getElementById('currentQuestion').textContent = currentQuestionIndex + 1;
    document.getElementById('totalQuestions').textContent = total;
    document.getElementById('progressPercent').textContent = percent;
    document.getElementById('progressBar').style.width = percent + '%';
}

function updateNavigationButtons() {
    document.getElementById('prevBtn').disabled = currentQuestionIndex === 0;
    
    if (currentQuestionIndex === questions.length - 1) {
        document.getElementById('nextBtn').classList.add('hidden');
        document.getElementById('submitBtn').classList.remove('hidden');
    } else {
        document.getElementById('nextBtn').classList.remove('hidden');
        document.getElementById('submitBtn').classList.add('hidden');
    }
}

function submitExam() {
    alertify.confirm('Submit Exam', 
        'Are you sure you want to submit? You cannot change answers after submission.',
        function() {
            stopProctoring();
            stopCheatDetection();
            stopTimer();
            // FIX: Naya function call kiya gaya hai
            submitAllAnswersAndFinish('completed');
        },
        function() {
            alertify.message('Continue with your exam');
        }
    );
}

// Camera and Proctoring
async function initializeCamera() {
    try {
        videoStream = await navigator.mediaDevices.getUserMedia({ 
            video: { width: 640, height: 480 } 
        });
        
        const video = document.getElementById('videoFeed');
        video.srcObject = videoStream;
        
        alertify.success('Camera initialized');
    } catch (error) {
        alertify.error('Camera access denied!');
        console.error('Camera error:', error);
    }
}

function startProctoring() {
    proctoringInterval = setInterval(() => {
        captureAndAnalyze();
    }, 3000);
}

function stopProctoring() {
    if (proctoringInterval) {
        clearInterval(proctoringInterval);
    }
    
    if (videoStream) {
        videoStream.getTracks().forEach(track => track.stop());
    }
}

async function captureAndAnalyze() {
    const video = document.getElementById('videoFeed');
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');
    
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0);
    
    canvas.toBlob(async (blob) => {
        await analyzeFrame(blob);
    }, 'image/jpeg', 0.8);
}

function handleViolations(data) {
    if (data.violations && data.violations.length > 0) {
        data.violations.forEach(violation => {
            addViolation(violation);
            logViolation(violation.type, violation.severity, violation.message);
            
            violationCount.total++;
            if (violation.severity === 'high') {
                violationCount.high++;
                alertify.error(`⚠️ ${violation.message}`);
            } else if (violation.severity === 'medium') {
                violationCount.medium++;
                alertify.warning(`⚠️ ${violation.message}`);
            } else {
                violationCount.low++;
            }
            
            checkViolationLimit();
        });
    }
}

function checkViolationLimit() {
    if (violationCount.total === MAX_VIOLATIONS_BEFORE_WARNING) {
        alertify.alert(
            '⚠️ WARNING',
            `You have ${violationCount.total} violations. ${MAX_VIOLATIONS_BEFORE_TERMINATION - violationCount.total} more will terminate the exam!`,
            function() {}
        );
    }
    
    if (ENABLE_AUTO_TERMINATION && violationCount.total >= MAX_VIOLATIONS_BEFORE_TERMINATION) {
        alertify.error(`Exam terminated! ${violationCount.total} violations detected.`);
        
        stopProctoring();
        stopCheatDetection();
        stopTimer();
        
        setTimeout(() => {
            finishExam('violations');
        }, 2000);
    }
}

function addViolation(violation) {
    violations.push({
        ...violation,
        timestamp: new Date().toLocaleTimeString()
    });
    
    updateViolationsDisplay();
}

function updateViolationsDisplay() {
    const container = document.getElementById('violationsList');
    
    if (violations.length === 0) {
        container.innerHTML = '<p class="text-muted">No violations detected</p>';
        return;
    }
    
    const summary = `
        <div class="mb-3 p-2 bg-light rounded">
            <strong>Total Violations: ${violationCount.total}</strong><br>
            <small>
                High: ${violationCount.high} | 
                Medium: ${violationCount.medium} | 
                Low: ${violationCount.low} | 
                Tab Switch: ${violationCount.tabSwitch}
            </small>
            ${ENABLE_AUTO_TERMINATION ? `<br><small class="text-danger">Limit: ${MAX_VIOLATIONS_BEFORE_TERMINATION}</small>` : ''}
        </div>
    `;
    
    const violationsList = violations.slice(-10).reverse().map(v => `
        <div class="violation-item">
            <span class="violation-badge violation-${v.severity}">${v.severity.toUpperCase()}</span>
            <strong>${v.type}</strong><br>
            <small>${v.message} - ${v.timestamp}</small>
        </div>
    `).join('');
    
    container.innerHTML = summary + violationsList;
}

// Timer
// Timer - Countdown Mode (1 minute per question)

function startTimer() {
    examStartTime = Date.now();
    timerInterval = setInterval(updateTimer, 1000);
}

function stopTimer() {
    if (timerInterval) {
        clearInterval(timerInterval);
    }
    if (examCountdownInterval) {
        clearInterval(examCountdownInterval);
    }
}

function updateTimer() {
    const elapsed = Math.floor((Date.now() - examStartTime) / 1000);
    const minutes = Math.floor(elapsed / 60);
    const seconds = elapsed % 60;
    
    // This shows elapsed time (optional - you can remove if you only want countdown)
    // document.getElementById('timer').textContent = 
    //     `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}

// NEW: Exam Countdown Timer (1 minute per question)
function startExamTimer() {
    // Calculate total time: 1 minute per question
    examTimeLimit = questions.length * 60; // seconds
    timeRemaining = examTimeLimit;
    
    // Update display immediately
    updateExamTimer();
    
    // Start countdown
    examCountdownInterval = setInterval(() => {
        timeRemaining--;
        updateExamTimer();
        
        // Warning at 1 minute remaining
        if (timeRemaining === 60) {
            alertify.warning('⏰ Only 1 minute remaining!');
        }
        
        // Warning at 30 seconds remaining
        if (timeRemaining === 30) {
            alertify.error('⏰ Only 30 seconds remaining!');
        }
        
        // Time's up!
        if (timeRemaining <= 0) {
            clearInterval(examCountdownInterval);
            alertify.error('⏰ Time is up! Exam will be auto-submitted.');
            
            // Auto-submit exam
            setTimeout(() => {
                autoSubmitExam();
            }, 2000);
        }
    }, 1000);
}

function updateExamTimer() {
    const minutes = Math.floor(timeRemaining / 60);
    const seconds = timeRemaining % 60;
    
    const timerElement = document.getElementById('timer');
    timerElement.textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    
    // Change color based on time remaining
    if (timeRemaining <= 60) {
        timerElement.style.color = '#ef4444'; // Red
        timerElement.style.animation = 'pulse 1s infinite';
    } else if (timeRemaining <= 180) {
        timerElement.style.color = '#f59e0b'; // Orange
    } else {
        timerElement.style.color = '#818cf8'; // Normal blue
    }
}

// Auto-submit when time runs out
function autoSubmitExam() {
    stopProctoring();
    stopCheatDetection();
    stopTimer();
    // FIX: Naya function call kiya gaya hai
    submitAllAnswersAndFinish('time_expired');
}
// Results
async function showResults(examData, reason = 'completed') {
    showPage('resultsPage');
    
    // FIX: Time taken
    let timeFormatted = "00:00";
    if (examStartTime) {
        const elapsed = Math.floor((Date.now() - examStartTime) / 1000);
        const minutes = Math.floor(elapsed / 60);
        const seconds = elapsed % 60;
        timeFormatted = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    }

    document.getElementById('finalScore').textContent = Math.round(examData.score) + '%';
    document.getElementById('correctAnswers').textContent = 
        `${examData.correct} / ${examData.total}`;
    document.getElementById('totalViolations').textContent = violationCount.total;
    document.getElementById('timeTaken').textContent = timeFormatted;

    if (reason === 'violations') {
        alertify.alert(
            'Exam Terminated',
            `Exam was terminated due to ${violationCount.total} violations.`,
            function() {}
        );
    }
    
    try {
        const response = await fetch(`${API_URL}/api/exam/results/${currentExam.exam_id}`);
        const data = await response.json();
        
        const container = document.getElementById('detailedResults');
        container.innerHTML = data.answers.map((answer, index) => `
            <div class="question-card">
                <h6>Question ${index + 1}</h6>
                <p>${answer.question_text}</p>
                <p>
                    <strong>Your Answer:</strong> ${answer.user_answer || 'Not answered'} 
                    ${answer.is_correct ? 
                        '<span class="badge bg-success">Correct</span>' : 
                        '<span class="badge bg-danger">Incorrect</span>'}
                </p>
                <p><strong>Correct Answer:</strong> ${answer.correct_answer}</p>
            </div>
        `).join('');
    } catch (error) {
        console.error('Failed to load detailed results:', error);
    }
}

// Admin Functions
async function generateQuestions() {
    const subject = validateAndSanitize(document.getElementById('genSubject').value);
    const difficulty = document.getElementById('genDifficulty').value;
    const count = Math.min(parseInt(document.getElementById('genCount').value), 20);
    
    if (!subject) {
        alertify.error('Please select a subject');
        return;
    }
    
    if (count < 1) {
        alertify.error('Count must be at least 1');
        return;
    }
    
    if (count > 20) {
        alertify.warning('Maximum 20 questions allowed. Generating 20.');
    }
    
    // FIX: Store the requested count and subject for the exam
    requestedQuestionCount = count;
    lastGeneratedSubject = subject;
    
    alertify.message(`Generating ${count} questions...`);
    
    try {
        const response = await fetch(`${API_URL}/api/questions/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ subject, difficulty, count })
        });
        
        if (response.ok) {
            const data = await response.json();
            
            // Show generation method
            let method = data.source || 'pre-loaded';
            let icon = method === 'groq' ? '🤖' : method === 'hybrid' ? '🔄' : '📚';
            
            alertify.success(`${icon} Generated ${data.count} questions using ${method}!`);
            
            setTimeout(() => {
                loadAllQuestions();
            }, 500);
        } else {
            const error = await response.json();
            alertify.error(`Failed to generate questions: ${error.detail || 'Unknown error'}`);
        }
    } catch (error) {
        console.error('Error generating questions:', error);
        alertify.error('Failed to generate questions. Please try again.');
    }
}


async function addManualQuestion() {
    const question = {
        question_text: validateAndSanitize(document.getElementById('manQuestion').value),
        option_a: validateAndSanitize(document.getElementById('manOptA').value),
        option_b: validateAndSanitize(document.getElementById('manOptB').value),
        option_c: validateAndSanitize(document.getElementById('manOptC').value),
        option_d: validateAndSanitize(document.getElementById('manOptD').value),
        correct_answer: document.getElementById('manCorrect').value
    };
    
    const validation = validateForm(question);
    
    if (!validation.isValid) {
        alertify.error(validation.errors.join(', '));
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/api/questions`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(validation.data)
        });
        
        if (response.ok) {
            alertify.success('Question added successfully!');
            document.getElementById('manualQuestionForm').reset();
        } else {
            alertify.error('Failed to add question');
        }
    } catch (error) {
        alertify.error('Error: ' + error.message);
    }
}

async function loadAllQuestions() {
    try {
        const response = await fetch(`${API_URL}/api/questions/all`);
        const data = await response.json();
        
        const container = document.getElementById('allQuestionsList');
        
        if (data.questions.length === 0) {
            container.innerHTML = '<p class="text-muted">No questions. Generate some first!</p>';
            return;
        }
        
        // Group questions by subject
        const grouped = {};
        data.questions.forEach(q => {
            const key = `${q.subject || 'Other'}-${q.difficulty || 'N/A'}`;
            if (!grouped[key]) grouped[key] = [];
            grouped[key].push(q);
        });
        
        let html = '';
        for (const [key, qs] of Object.entries(grouped)) {
            const [subject, difficulty] = key.split('-');
            html += `<h6 class="mt-3">${subject} - ${difficulty} (${qs.length} questions)</h6>`;
        }
        
        html += `<hr><p><strong>Total: ${data.questions.length} questions</strong></p>`;
        
        html += data.questions.slice(0, 10).map((q, index) => `
            <div class="question-card">
                <h6>Q${index + 1} - ${q.subject || 'General'} (${q.difficulty || 'N/A'})</h6>
                <p><strong>Q:</strong> ${q.question_text}</p>
                <p><strong>A:</strong> ${q.option_a}</p>
                <p><strong>B:</strong> ${q.option_b}</p>
                <p><strong>C:</strong> ${q.option_c}</p>
                <p><strong>D:</strong> ${q.option_d}</p>
                <p><strong>Correct:</strong> <span class="badge bg-success">${q.correct_answer}</span></p>
            </div>
        `).join('');
        
        if (data.questions.length > 10) {
            html += `<p class="text-muted">Showing first 10 of ${data.questions.length} questions</p>`;
        }
        
        container.innerHTML = html;
    } catch (error) {
        alertify.error('Failed to load questions');
    }
}

// Event Listeners
document.getElementById('loginForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    login(username, password);
});

document.getElementById('generateForm').addEventListener('submit', (e) => {
    e.preventDefault();
    generateQuestions();
});

document.getElementById('manualQuestionForm').addEventListener('submit', (e) => {
    e.preventDefault();
    addManualQuestion();
});

// Configure Alertify
alertify.set('notifier', 'position', 'top-right');
alertify.set('notifier', 'delay', 3);

console.log('📚 Proctoring System Loaded');
console.log(`🔒 Cheat Detection: ${ENABLE_TAB_SWITCH_DETECTION ? 'Enabled' : 'Disabled'}`);
console.log(`⌨️ Keyboard Blocking: ${ENABLE_KEYBOARD_BLOCKING ? 'Enabled' : 'Disabled'}`);
console.log(`⚠️ Max Violations: ${MAX_VIOLATIONS_BEFORE_TERMINATION}`);
