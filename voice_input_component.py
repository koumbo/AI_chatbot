import streamlit.components.v1 as components

def voice_input():
    component = components.html(
        """
        <html>
        <body>
            <button onclick="startRecognition()">🎤 Speak</button>
            <p id="output" style="font-weight: bold;"></p>

            <script>
                const output = document.getElementById("output");

                function startRecognition() {
                    const recognition = new webkitSpeechRecognition() || new SpeechRecognition();
                    recognition.lang = 'en-US';
                    recognition.interimResults = false;
                    recognition.maxAlternatives = 1;

                    recognition.onresult = function(event) {
                        const text = event.results[0][0].transcript;
                        output.innerText = text;
                        window.parent.postMessage({type: 'STREAMLIT:SET_COMPONENT_VALUE', value: text}, '*');
                    };

                    recognition.onerror = function(event) {
                        output.innerText = "Error: " + event.error;
                    };

                    recognition.start();
                }
            </script>
        </body>
        </html>
        """,
        height=150,
    )
    return component
