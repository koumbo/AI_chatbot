import streamlit.components.v1 as components

def voice_input():
    return components.html(
        """
        <script>
        const streamlitInput = window.parent;
        let recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'en-US';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        function startRecognition() {
            recognition.start();
            document.getElementById('status').innerText = "🎤 Listening...";
        }

        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            document.getElementById('status').innerText = "✅ " + transcript;
            streamlitInput.postMessage(
                { type: 'STREAMLIT:SET_COMPONENT_VALUE', value: transcript },
                '*'
            );
        }

        recognition.onerror = function(event) {
            document.getElementById('status').innerText = "❌ Error: " + event.error;
        }

        </script>
        <button onclick="startRecognition()">🎙️ Speak</button>
        <p id="status">Click the mic and speak</p>
        """,
        height=180,
        key="voice"
    )
