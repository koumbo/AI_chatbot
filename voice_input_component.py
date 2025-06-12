import streamlit.components.v1 as components

def voice_input():
    return components.html(
        """
        <!DOCTYPE html>
        <html>
        <body>
            <button onclick="startRecognition()">🎙️ Speak</button>
            <p id="status">Waiting...</p>
            <script>
                const status = document.getElementById("status");

                function startRecognition() {
                    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
                    recognition.lang = 'en-US';
                    recognition.interimResults = false;
                    recognition.maxAlternatives = 1;

                    recognition.onresult = function(event) {
                        const transcript = event.results[0][0].transcript;
                        status.textContent = "✅ " + transcript;
                        window.parent.postMessage(
                            {type: 'STREAMLIT:SET_COMPONENT_VALUE', value: transcript},
                            '*'
                        );
                    };

                    recognition.onerror = function(event) {
                        status.textContent = "❌ Error: " + event.error;
                    };

                    recognition.start();
                    status.textContent = "🎤 Listening...";
                }
            </script>
        </body>
        </html>
        """,
        height=180
    )
