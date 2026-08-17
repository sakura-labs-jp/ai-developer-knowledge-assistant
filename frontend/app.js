const API_URL = "http://127.0.0.1:8000/chat";

const chatMessages =
    document.getElementById("chatMessages");

const questionInput =
    document.getElementById("questionInput");

const sendButton =
    document.getElementById("sendButton");

const welcome =
    document.getElementById("welcome");


/* =========================================================
   Send Question
   ========================================================= */

async function sendQuestion() {

    const question =
        questionInput.value.trim();

    if (!question) {
        return;
    }


    if (welcome) {
        welcome.style.display = "none";
    }


    addUserMessage(question);


    questionInput.value = "";
    questionInput.style.height = "auto";

    sendButton.disabled = true;


    const loadingMessage =
        addLoadingMessage();


    try {

        const response =
            await fetch(API_URL, {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    message: question
                })

            });


        if (!response.ok) {

            throw new Error(
                `API request failed: ${response.status}`
            );

        }


        const data =
            await response.json();

        loadingMessage.remove();

        addAssistantMessage(
            data.answer,
            data.source
        );


    } catch (error) {

        console.error(error);

        loadingMessage.remove();


        addErrorMessage(
            "Unable to connect to the Knowledge Assistant."
        );


    } finally {

        sendButton.disabled = false;

        questionInput.focus();

    }

}


/* =========================================================
   User Message
   ========================================================= */

function addUserMessage(message) {

    const element =
        document.createElement("div");


    element.className =
        "message user";


    element.innerHTML = `

        <div class="avatar">
            You
        </div>

        <div class="message-content">

            <div class="message-name">
                You
            </div>

            <div class="message-bubble">
                ${escapeHtml(message)}
            </div>

        </div>

    `;


    chatMessages.appendChild(element);

    scrollToBottom();

}


/* =========================================================
   Assistant Message
   ========================================================= */

function addAssistantMessage(message, source) {

    const element =
        document.createElement("div");

    element.className =
        "message assistant";

    const results =
        extractKeyResults(message);

    const formattedAnswer =
        formatAnswer(message);

    element.innerHTML = `

        <div class="avatar">
            AI
        </div>

        <div class="message-content">

            <div class="message-name">
                Knowledge Copilot
            </div>

            <div class="message-bubble">

                <div class="answer-header">

                    <div class="answer-check">
                        ✓
                    </div>

                    Relevant knowledge found

                </div>

                ${
                    results.length > 0
                    ? createResultsHtml(results)
                    : ""
                }

                <div class="section-label">
                    💡 Knowledge Answer
                </div>

                <div class="answer-text">
                    ${formattedAnswer}
                </div>

                ${createKnowledgeSourceHtml(source)}

            </div>

        </div>

    `;

    chatMessages.appendChild(element);

    scrollToBottom();
}


/* =========================================================
   Key Result Extraction
   ========================================================= */

function extractKeyResults(text) {

    const results = [];


    const patterns = [

        {
            regex: /約?\s*100\s*GB/i,
            value: "100 GB",
            label: "Data volume"
        },

        {
            regex: /約?\s*4,?600\s*(カラム|列)/i,
            value: "4,600",
            label: "Columns"
        },

        {
            regex: /約?\s*30\s*分/,
            value: "~30 min",
            label: "Processing time"
        },

        {
            regex: /96\s*%/,
            value: "96%",
            label: "Success rate"
        },

        {
            regex: /2,?200\s*(カラム|列)/i,
            value: "2,200",
            label: "Normalized fields"
        }

    ];


    patterns.forEach(
        pattern => {

            if (
                pattern.regex.test(text)
            ) {

                results.push({

                    value: pattern.value,

                    label: pattern.label

                });

            }

        }
    );


    return results.slice(0, 3);

}


/* =========================================================
   Key Result HTML
   ========================================================= */

function createResultsHtml(results) {

    return `

        <div class="key-result-section">

            <div class="section-label">
                📊 Key Results
            </div>


            <div class="key-results">

                ${results.map(result => `

                    <div class="result-card">

                        <div class="result-value">
                            ${result.value}
                        </div>

                        <div class="result-label">
                            ${result.label}
                        </div>

                    </div>

                `).join("")}

            </div>

        </div>

    `;

}


/* =========================================================
   Loading
   ========================================================= */

function addLoadingMessage() {

    const element =
        document.createElement("div");


    element.className =
        "message assistant";


    element.innerHTML = `

        <div class="avatar">
            AI
        </div>

        <div class="message-content">

            <div class="message-name">
                Knowledge Copilot
            </div>

            <div class="message-bubble">

                <div class="loading-status">
                    🔍 Searching engineering knowledge...
                </div>

                <div class="loading">

                    <span></span>
                    <span></span>
                    <span></span>

                </div>

            </div>

        </div>

    `;


    chatMessages.appendChild(element);

    scrollToBottom();


    return element;

}


/* =========================================================
   Error
   ========================================================= */

function addErrorMessage(message) {

    const element =
        document.createElement("div");


    element.className =
        "message assistant";


    element.innerHTML = `

        <div class="avatar">
            AI
        </div>

        <div class="message-content">

            <div class="message-name">
                Knowledge Copilot
            </div>

            <div class="message-bubble">

                <div class="error">
                    ${escapeHtml(message)}
                </div>

            </div>

        </div>

    `;


    chatMessages.appendChild(element);

    scrollToBottom();

}


/* =========================================================
   Markdown-like Formatting
   ========================================================= */

function formatAnswer(text) {

    let html =
        escapeHtml(text);


    /*
     * Heading:
     * ### Title
     */

    html =
        html.replace(
            /^###\s+(.+)$/gm,
            '<h3 class="answer-heading">$1</h3>'
        );


    /*
     * Bold:
     * **text**
     */

    html =
        html.replace(
            /\*\*(.+?)\*\*/g,
            '<strong>$1</strong>'
        );


    /*
     * Horizontal separators:
     * ---
     */

    html =
        html.replace(
            /^---$/gm,
            '<hr class="answer-divider">'
        );


    /*
     * Bullet:
     * - text
     * * text
     */

    html =
        html.replace(
            /^[*-]\s+(.+)$/gm,
            '<div class="answer-bullet"><span>•</span><div>$1</div></div>'
        );


    /*
     * Numbered items:
     * 1. text
     */

    html =
        html.replace(
            /^(\d+)\.\s+(.+)$/gm,
            '<div class="answer-step"><span class="step-number">$1</span><div>$2</div></div>'
        );


    /*
     * Paragraph / line break
     */

    html =
        html.replace(
            /\n{2,}/g,
            '</p><p>'
        );


    html =
        html.replace(
            /\n/g,
            '<br>'
        );


    return `<p>${html}</p>`;

}


/* =========================================================
   Suggestion Buttons
   ========================================================= */

document
    .querySelectorAll(".suggestion")
    .forEach(button => {

        button.addEventListener(
            "click",
            () => {

                questionInput.value =
                    button.dataset.question;

                sendQuestion();

            }
        );

    });


/* =========================================================
   Enter Key
   ========================================================= */

questionInput.addEventListener(
    "keydown",
    event => {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendQuestion();

        }

    }
);


/* =========================================================
   Send Button
   ========================================================= */

sendButton.addEventListener(
    "click",
    sendQuestion
);


/* =========================================================
   Auto Resize
   ========================================================= */

questionInput.addEventListener(
    "input",
    function () {

        this.style.height = "auto";

        this.style.height =
            `${Math.min(this.scrollHeight, 120)}px`;

    }
);


/* =========================================================
   Scroll
   ========================================================= */

function scrollToBottom() {

    chatMessages.scrollTo({

        top: chatMessages.scrollHeight,

        behavior: "smooth"

    });

}


/* =========================================================
   HTML Escape
   ========================================================= */

function escapeHtml(text) {

    const div =
        document.createElement("div");

    div.textContent = text;

    return div.innerHTML;

}

function createKnowledgeSourceHtml(source) {

    if (!source) {

        return `
            <div class="knowledge-card">

                <div class="knowledge-title">
                    📚 Knowledge Used
                </div>

                <div class="knowledge-name">
                    No relevant knowledge source
                </div>

            </div>
        `;
    }

    const similarityPercent =
        Math.round(source.similarity * 100);

    return `

        <div class="knowledge-card">

            <div class="knowledge-title">
                📚 Knowledge Used
            </div>

            <div class="knowledge-name">
                ${escapeHtml(source.title)}
            </div>

            <div class="knowledge-meta">

                <span>
                    ${escapeHtml(source.category)}
                </span>

                <span class="meta-divider">
                    •
                </span>

                <span>
                    ${escapeHtml(source.technology)}
                </span>

            </div>

            <div class="knowledge-match">

                <span class="match-value">
                    ${similarityPercent}%
                </span>

                Knowledge Match

            </div>

            <div class="knowledge-status">
                ✓ Retrieved from registered engineering knowledge
            </div>

        </div>

    `;
}