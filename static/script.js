// ==========================================================
// ELEMENTS
// ==========================================================

const setupScreen = document.getElementById("setup-screen");
const interviewScreen = document.getElementById("interview-screen");
const resultScreen = document.getElementById("result-screen");

const roleInput = document.getElementById("role");
const skillsInput = document.getElementById("skills");

const startBtn = document.getElementById("start-btn");
const submitBtn = document.getElementById("submit-btn");
const submitText = document.getElementById("submit-text");

const questionText = document.getElementById("question-text");
const currentQuestion = document.getElementById("current-question");

const answerBox = document.getElementById("answer");
const characterCount = document.getElementById("character-count");

const progressBar = document.getElementById("progress-bar");

const loadingOverlay =
    document.getElementById("loading-overlay");

const loadingTitle =
    document.getElementById("loading-title");

const loadingDescription =
    document.getElementById("loading-description");

const errorMessage =
    document.getElementById("error-message");

const newInterviewBtn =
    document.getElementById("new-interview-btn");


// ==========================================================
// HELPER FUNCTIONS
// ==========================================================

function showLoading(title, description) {

    loadingTitle.textContent = title;
    loadingDescription.textContent = description;

    loadingOverlay.classList.remove("hidden");
}


function hideLoading() {

    loadingOverlay.classList.add("hidden");
}


function showError(message) {

    errorMessage.textContent = message;

    errorMessage.classList.remove("hidden");

    setTimeout(() => {

        errorMessage.classList.add("hidden");

    }, 4000);
}


function showScreen(screen) {

    setupScreen.classList.add("hidden");

    interviewScreen.classList.add("hidden");

    resultScreen.classList.add("hidden");

    screen.classList.remove("hidden");
}


function updateProgress(questionNumber) {

    currentQuestion.textContent =
        questionNumber;

    const percentage =
        (questionNumber / 5) * 100;

    progressBar.style.width =
        `${percentage}%`;
}


function updateCharacterCount() {

    const length =
        answerBox.value.length;

    characterCount.textContent =
        `${length} characters`;
}


// ==========================================================
// CANDIDATE SUBMISSION SUCCESS
// ==========================================================

function showSubmissionSuccess() {

    showScreen(resultScreen);


    const resultHeader =
        document.querySelector(".result-header");


    resultHeader.innerHTML = `

        <div class="hero-badge">

            <span>✓</span>

            INTERVIEW SUBMITTED

        </div>


        <h1>

            Thank you for

            <span>
                completing the interview.
            </span>

        </h1>


        <p>

            Your responses have been successfully
            submitted for review.

        </p>

    `;


    const scoreCard =
        document.querySelector(".score-card");


    scoreCard.innerHTML = `

        <div class="submission-icon">

            ✓

        </div>


        <div class="score-content">

            <p class="eyebrow">

                SUBMISSION RECEIVED

            </p>


            <h2>

                Your interview is under review

            </h2>


            <p>

                Your responses have been submitted
                successfully. The recruitment team
                will review your performance and
                contact you regarding the next round.

            </p>

        </div>

    `;


    const insightsGrid =
        document.querySelector(".insights-grid");


    insightsGrid.innerHTML = `

        <div class="insight-card">

            <div class="insight-title">

                <span class="insight-icon">
                    ✓
                </span>

                <h3>
                    Interview Complete
                </h3>

            </div>

            <ul>

                <li>
                    All 5 interview questions were
                    successfully submitted.
                </li>

            </ul>

        </div>


        <div class="insight-card">

            <div class="insight-title">

                <span class="insight-icon">
                    AI
                </span>

                <h3>
                    Evaluation
                </h3>

            </div>

            <ul>

                <li>
                    Your responses are being securely
                    evaluated by the assessment system.
                </li>

            </ul>

        </div>


        <div class="insight-card">

            <div class="insight-title">

                <span class="insight-icon">
                    →
                </span>

                <h3>
                    Next Round
                </h3>

            </div>

            <ul>

                <li>
                    Candidates selected for the next
                    round will be contacted by the
                    recruitment team.
                </li>

            </ul>

        </div>

    `;


    if (newInterviewBtn) {

        newInterviewBtn.style.display =
            "none";

    }
}


// ==========================================================
// CHARACTER COUNTER
// ==========================================================

answerBox.addEventListener(
    "input",
    updateCharacterCount
);


// ==========================================================
// START INTERVIEW
// ==========================================================

startBtn.addEventListener(
    "click",
    async () => {

        const role =
            roleInput.value.trim();

        const skills =
            skillsInput.value.trim();


        if (!role) {

            showError(
                "Please enter the target job role."
            );

            roleInput.focus();

            return;
        }


        if (!skills) {

            showError(
                "Please enter at least one skill."
            );

            skillsInput.focus();

            return;
        }


        showLoading(
            "Preparing your interview",
            "AI is generating 5 role-specific questions..."
        );


        startBtn.disabled = true;


        try {

            const response =
                await fetch(
                    "/start",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            role: role,
                            skills: skills
                        })
                    }
                );


            const data =
                await response.json();


            if (!response.ok || !data.success) {

                if (response.status === 401) {

                    window.location.href =
                        "/login";

                    return;
                }


                throw new Error(
                    data.message ||
                    "Could not start interview."
                );
            }


            questionText.textContent =
                data.question;


            updateProgress(
                data.question_number
            );


            answerBox.value = "";

            updateCharacterCount();


            showScreen(
                interviewScreen
            );


            setTimeout(() => {

                answerBox.focus();

            }, 100);

        }

        catch (error) {

            console.error(error);

            showError(
                error.message ||
                "Something went wrong."
            );

        }

        finally {

            hideLoading();

            startBtn.disabled = false;

        }

    }
);


// ==========================================================
// SUBMIT ANSWER
// ==========================================================

submitBtn.addEventListener(
    "click",
    async () => {

        const answer =
            answerBox.value.trim();


        if (!answer) {

            showError(
                "Please enter your answer before submitting."
            );

            answerBox.focus();

            return;
        }


        submitBtn.disabled = true;

        submitText.textContent =
            "Submitting...";


        try {

            const response =
                await fetch(
                    "/submit",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            answer: answer
                        })
                    }
                );


            const data =
                await response.json();


            if (!response.ok || !data.success) {

                if (response.status === 401) {

                    window.location.href =
                        "/login";

                    return;
                }


                throw new Error(
                    data.message ||
                    "Could not submit answer."
                );
            }


            // ==================================================
            // ALL 5 QUESTIONS COMPLETED
            // ==================================================

            if (data.completed) {

                submitText.textContent =
                    "Submitted";


                showLoading(
                    "Interview submitted",
                    "Your responses are being securely evaluated..."
                );


                setTimeout(() => {

                    hideLoading();

                    showSubmissionSuccess();

                }, 700);


                return;
            }


            // ==================================================
            // NEXT QUESTION
            // ==================================================

            if (!data.question) {

                throw new Error(
                    "The next interview question was not received."
                );
            }


            questionText.textContent =
                data.question;


            updateProgress(
                data.question_number
            );


            answerBox.value = "";

            updateCharacterCount();


            submitText.textContent =
                "Submit Answer";


            answerBox.focus();

        }

        catch (error) {

            console.error(error);

            showError(
                error.message ||
                "Something went wrong."
            );

        }

        finally {

            submitBtn.disabled = false;

            submitText.textContent =
                "Submit Answer";

        }

    }
);


// ==========================================================
// NEW INTERVIEW
// ==========================================================

newInterviewBtn.addEventListener(
    "click",
    async () => {

        try {

            const response =
                await fetch(
                    "/reset"
                );


            const data =
                await response.json();


            if (!response.ok || !data.success) {

                throw new Error(
                    "Could not reset the interview."
                );
            }

        }

        catch (error) {

            console.error(error);

            showError(
                error.message
            );

            return;
        }


        roleInput.value = "";

        skillsInput.value = "";

        answerBox.value = "";


        updateCharacterCount();

        updateProgress(1);


        showScreen(
            setupScreen
        );


        newInterviewBtn.style.display =
            "block";


        roleInput.focus();

    }
);


// ==========================================================
// KEYBOARD SHORTCUT
// ==========================================================
//
// Enter = new line
// Ctrl + Enter = submit answer
//
// This prevents a blank line from being treated as
// another answer. The candidate submits explicitly.
// ==========================================================

answerBox.addEventListener(
    "keydown",
    (event) => {

        if (
            event.key === "Enter" &&
            event.ctrlKey
        ) {

            event.preventDefault();

            submitBtn.click();

        }

    }
);


// ==========================================================
// INITIAL STATE
// ==========================================================

updateCharacterCount();

updateProgress(1);

showScreen(
    setupScreen
);