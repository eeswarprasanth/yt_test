import streamlit as st
from crew import YtTest

st.title("🎬 YouTube Video Analyzer with CrewAI")

# User inputs
video_url = st.text_input("Enter YouTube Video URL")
question = st.text_input("Enter your question about the video")

if st.button("Analyze Video"):
    if not video_url:
        st.warning("Please enter a YouTube video URL.")
    else:
        st.write("🚀 Running CrewAI Agents...")

        # Run the crew with user inputs
        inputs = {'video_url': video_url, 'question': question}
        result = YtTest().crew().kickoff(inputs=inputs)

        def format_text(text):
            """Formats text by adding line breaks and bullet points where needed."""
            text = text.replace("  ", "\n")  # Ensure proper line breaks
            formatted_text = []
            for line in text.split("\n"):
                if line.strip().startswith(("*", "-")):  # Handle bullet points
                    formatted_text.append(f"- {line.strip().lstrip('*-').strip()}")
                elif line.strip()[0:2].isdigit():  # Handle numbered points
                    formatted_text.append(f"{line.strip()}")
                else:
                    formatted_text.append(line.strip())
            return "\n".join(formatted_text)

        # Display Transcript
        st.subheader("📜 Transcript")
        try:
            with open("transcript.txt", "r") as f:
                transcript_text = f.read()
                st.text_area("Extracted Transcript", transcript_text, height=300)
        except FileNotFoundError:
            st.warning("Transcript file not found.")

        # Display Summary
        st.subheader("📄 Summary")
        try:
            with open("summary.txt", "r") as f:
                summary_text = f.read()
                formatted_summary = format_text(summary_text)
                st.text_area("Generated Summary", formatted_summary, height=250)
        except FileNotFoundError:
            st.warning("No summary available.")

        # Display Q&A Response
        st.subheader("❓ Q&A Response")
        try:
            with open("answer.txt", "r") as f:
                qa_response = f.read()
                formatted_qa = format_text(qa_response)
                st.text_area("AI Response", formatted_qa, height=250)
        except FileNotFoundError:
            st.warning("No Q&A response available.")
