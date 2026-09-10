const input = document.getElementById("userInput");
const sendButton = document.getElementById("sendButton");

sendButton.addEventListener("click", sendMessage);

input.addEventListener("keydown", function (event) {

    if (event.key === "Enter" && !event.shiftKey) {

        event.preventDefault();

        sendMessage();
    }
});


async function sendMessage() {

    const message = input.value.trim();

    if (!message) {
        return;
    }


    sendButton.disabled = true;

    sendButton.textContent = "Thinking...";


    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })
        });


        const data = await response.json();


        if (data.error) {

            alert(data.error);

            return;
        }


        // ==========================================
        // FINAL ANSWER
        // ==========================================

        const finalBox = document.getElementById("finalAnswer");

        if (finalBox) {

            finalBox.innerText = data.final;
        }


        // ==========================================
        // INDIVIDUAL AGENTS
        // ==========================================

        updateAgent(
            "chatgptResponse",
            data.agents.ChatGPT
        );

        updateAgent(
            "claudeResponse",
            data.agents.Claude
        );

        updateAgent(
            "geminiResponse",
            data.agents.Gemini
        );

        updateAgent(
            "kimiResponse",
            data.agents.Kimi
        );


    } catch (error) {

        console.error(error);

        alert(
            "Something went wrong: " +
            error.message
        );

    } finally {

        sendButton.disabled = false;

        sendButton.textContent = "Send";
    }
}


function updateAgent(elementId, response) {

    const element = document.getElementById(elementId);

    if (!element) {
        return;
    }

    element.innerText = response;
}