import gradio as gr
# Import the Speech-to-Text client library
from google.cloud import speech

# Instantiates a client
client = speech.SpeechClient()


def transcribe_speech(file):
    with open(file.name, 'rb') as f:
        content = f.read()

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="en-US",
        model="phone_call",
        audio_channel_count=2,
        enable_word_confidence=True,
        enable_word_time_offsets=True,
    )

    # Detects speech in the audio file
    operation = client.long_running_recognize(config=config, audio=audio)

    response = operation.result(timeout=90)

    ret = ""
    for result in response.results:
        ret += result.alternatives[0].transcript

    return ret


demo = gr.Interface(fn=transcribe_speech, inputs="file",
                    outputs="text", allow_flagging='never')

demo.launch(server_name="0.0.0.0", server_port=8080)
