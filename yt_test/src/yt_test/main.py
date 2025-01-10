#!/usr/bin/env python
import sys
import warnings

from crew import YtTest

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'video_url': 'https://youtu.be/zTbgNC42Ops?si=J-J3-0M8qX8lsQNt'
    }
    YtTest().crew().kickoff(inputs=inputs)

run()