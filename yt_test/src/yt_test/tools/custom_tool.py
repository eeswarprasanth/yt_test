from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, VideoUnavailable, NoTranscriptFound
import re
from crewai.tools import tool

@tool("YouTube Transcript Extractor")
def youtube_transcript_extractor(video_url: str) -> str:
    """
    Extracts the transcript from a YouTube video.

    Args:
        video_url (str): The URL of the YouTube video.

    Returns:
        str: The transcript of the video or an error message if transcript extraction fails.
    """
    try:
        # Extract video ID from the URL
        if "youtu.be" in video_url:
            video_id = video_url.split("/")[-1].split("?")[0]
        elif "youtube.com" in video_url and "v=" in video_url:
            video_id = video_url.split("v=")[1].split("&")[0]
        else:
            raise ValueError("Invalid YouTube URL. Ensure it contains a video ID.")
        
        # Validate video ID (optional, ensuring it's not empty or malformed)
        if not re.match(r'^[a-zA-Z0-9_-]{11}$', video_id):
            raise ValueError("Invalid video ID extracted from the URL.")
        
        # Fetch transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Combine transcript text
        full_transcript = "\n".join([entry['text'] for entry in transcript])
        
        return full_transcript
    
    except TranscriptsDisabled:
        return "Transcripts are disabled for this video."
    except VideoUnavailable:
        return "The video is unavailable. Please check the URL."
    except NoTranscriptFound:
        return "No transcript found for this video in the requested language."
    except Exception as e:
        return f"An error occurred: {str(e)}"
