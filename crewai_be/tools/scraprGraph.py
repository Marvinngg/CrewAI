import json
import os
from scrapegraphai.graphs import SpeechGraph   #版本和 python-dotenv 冲突，后续解决
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()
@tool("search,scrape and summarize website content")
def generate_audio_summary(prompt, source):
    """Useful to search,scrape and summarize a website content"""
    graph_config = {
        "llm": {
            "api_key": os.environ["OPENAI_API_KEY"],
            "model": "gpt-3.5-turbo",
        },
        "tts_model": {
            "api_key": os.environ["OPENAI_API_KEY"],
            "model": "tts-1",
            "voice": "alloy"
        },
        "output_path": "audio_summary.mp3",
    }

    speech_graph = SpeechGraph(
        prompt=prompt,
        source=source,
        config=graph_config,
    )

    result = speech_graph.run()
    return result
