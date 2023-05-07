"""Streamlit app to explain code using text-to-speech."""

import streamlit as st
from explainer import get_code_explanation, get_code_language
from streamlit.runtime.uploaded_file_manager import UploadedFile
from text2speech import convert_text_to_mp3, list_available_names


def display_header() -> None:
    """Display the header of the app."""
    st.title("Code Explainer")
    st.text("Just upload your code or copy and paste in the field below")
    st.warning("Warning: uploaded files have precendence on copied and pasted code.")


def display_code_input_widget() -> tuple[UploadedFile | None, str]:
    """Display the widgets to upload a file or copy/paste the code."""
    file = st.file_uploader("Upload your script here.")
    text = st.text_area("or copy and paste your code here (press Ctrl + Enter to send)")

    if not (text or file):
        st.error("Bring your code with one of the options from above.")

    return file, text


def get_content_from_uploaded_file(file: UploadedFile) -> str:
    """Return the content of the uploaded file."""
    return file.getvalue().decode("utf8")


def get_code() -> str:
    """Renders widgets and return the code to explain."""
    uploaded_script, pasted_code = display_code_input_widget()

    if uploaded_script:
        return get_content_from_uploaded_file(uploaded_script)
    return pasted_code or ""


def select_voice_widget() -> str:
    """Streamlit widget to choose a voice."""
    voices = list_available_names()
    selected_voice = st.selectbox(
        "Could you please choose one of our available voices to explain?", voices
    )
    if not selected_voice:
        selected_voice = voices[0]
    return selected_voice


def main() -> None:
    display_header()

    selected_voice = select_voice_widget()

    if code_to_explain := get_code():
        with st.spinner(text="Let me think for a while..."):
            language = get_code_language(code=code_to_explain)
            explanation = get_code_explanation(code=code_to_explain)

        with st.spinner(text="Give me a little bit more time, this code is complex..."):
            convert_text_to_mp3(
                message=language, voice_name=selected_voice, mp3_filename="language.mp3"
            )
        with st.spinner(
            text=(
                "I've got the language! "
                "I'm thinking about how to explain to you in a few words now..."
            )
        ):
            convert_text_to_mp3(
                message=explanation,
                voice_name=selected_voice,
                mp3_filename="explanation.mp3",
            )

        st.success("Uhg, that was hard! But here is your explanation")
        st.warning("Remember to turn on your audio!")

        st.markdown(f"**Language:** {language}")
        st.audio("language.mp3")

        st.markdown(f"**Explanation:** {explanation}")
        st.audio("explanation.mp3")


if __name__ == "__main__":
    main()
