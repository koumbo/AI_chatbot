import streamlit.components.v1 as components

def voice_io(prompt_to_speak=""):
    return components.html(
        f"""
        <!DOCTYPE html>
        <html>
        <body>
            <button onclick="startRecognition()">🎙️ Speak</button>
            <p id="status">🕒 Waiting...</p>

            <script>
                const status = document.getElementById("status");

                function speak(text) {{
                    const utterance = new SpeechSynthesisUtterance(text);
                    utterance.lang = 'en-US';
                    speechSynthesis.speak(utterance);
                }}

                if ("{prompt_to_speak}" !== "") {{
                    speak("{prompt_to_speak}");
                }}

                function startRecognition() {{
                    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
                    recognition.lang = 'en-US';
                    recognition.interimResults = false;
                    recognition.maxAlternatives = 1;

                    recognition.onresult = function(event) {{
                        const transcript = event.results[0][0].transcript;
                        status.innerText = "✅ " + transcript;

                        // Send to Streamlit
                        window.parent.postMessage({{
                            type: 'STREAMLIT:SET_COMPONENT_VALUE',
                            value: transcript
                        }}, '*');
                    }};

                    recognition.onerror = function(event) {{
                        status.innerText = "❌ Error: " + event.error;
                    }};

                    recognition.start();
                    status.innerText = "🎤 Listening...";
                }}
            </script>
        </body>
        </html>
        """,
        height=220
    )
