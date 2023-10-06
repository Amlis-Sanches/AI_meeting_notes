#import section
import openai
from pydub import AudioSegment
from docx import Document

#get your API key to run the code but save it outside of your git rapository. 
api_key_file = r"C:\Users\natha\Documents\Coding\MeetingMinutesKey.txt"  # Path to the text file containing the API key

def get_api_key(api_key_file):
    with open(api_key_file, 'r') as file:
        api_key = file.read().strip()
    return api_key

# Initialize the API with the retrieved key
openai.api_key = get_api_key(api_key_file)

# Load the audio file
audio_file = AudioSegment.from_file(r"C:\Users\natha\Documents\Coding\AI_meeting_notes\EarningsCall.wav")

# Load your WAV file
audio = AudioSegment.from_wav("EarningsCall.wav")

# Convert to MP3
audio.export("EarningsCall.mp3", format="mp3")

# Get the duration in milliseconds
duration_ms = len(audio_file)

def trim_audio(input_file, output_file, start_time, end_time):
    audio = AudioSegment.from_file(input_file)
    trimmed_audio = audio[start_time:end_time]
    trimmed_audio.export(output_file, format="wav")

# Usage example
output_file = "trimmed_audio.wav"
start_time = 0  # Start time in milliseconds
end_time = duration_ms/2   # End time in milliseconds

input_file_path = r"C:\Users\natha\Documents\Coding\AI_meeting_notes\EarningsCall.wav"
trim_audio(input_file_path, output_file, start_time, end_time)

audio_file_path = r"C:\Users\natha\Documents\Coding\AI_meeting_notes\trimmed_audio.mp3"
#use the Whisper model to take the audio and transcribe the file
def transcribe_audio(audio_file_path):
    with open(audio_file_path, 'rb') as audio_file:
        transcription = openai.Audio.transcribe("whisper-1",audio_file)
    return transcription['text']

#Summarizing and analyzing the transcript with GPT-4

#you can do this all in one function but it is found that splitting up the functions allow for higher quality. 
# Here we take the raw text and pass it through each function. 

def meeting_minutes(transcription):
    abstract_summary = abstract_summary_extraction(transcription)
    key_points = key_points_extraction(transcription)
    action_items = action_item_extraction(transcription)
    sentiment = sentiment_analysis(transcription)
    return {
        'abstract_summary': abstract_summary,
        'key_points': key_points,
        'action_items': action_items,
        'sentiment': sentiment
    }

#--Summary extraction
#take the text and summarizes it into a concise abstract paragraph.
def abstract_summary_extraction(transcription):
    response = openai.Completion.create(
        model="text-davinci-003",
        temperature=0,
        prompt="You are a highly skilled AI trained in language comprehension and summarization. "
            "I would like you to read the following text and summarize it into a concise abstract paragraph. "
            "Aim to retain the most important points, providing a coherent and readable summary that could help a person "
            "understand the main points of the discussion without needing to read the entire text. Please avoid unnecessary "
            "details or tangential points.\n\n" + transcription
    )
    return response['choices'][0]['text']



#--Extract Key Points
def key_points_extraction(transcription):
    response = openai.Completion.create(
        model="text-davinci-003",
        temperature=0,
        prompt="You are a proficient AI with a specialty in distilling information into key points." 
            "Based on the following text, identify and list the main points that were discussed or brought up." 
            "These should be the most important ideas, findings, or topics that are crucial to the essence of the discussion." 
            "Your goal is to provide a list that someone could read to quickly understand what was talked about.\n\n" + transcription
    )
    return response['choices'][0]['text']

#--Action Item Extraction
def action_item_extraction(transcription):
    response = openai.Completion.create(
        model="text-davinci-003",
        temperature=0,
        prompt="You are an AI expert in analyzing conversations and extracting action items."
            "Please review the text and identify any tasks, assignments, or actions that were agreed upon or mentioned as needing to be done." 
            "These could be tasks assigned to specific individuals, or general actions that the group has decided to take." 
            "Please list these action items clearly and concisely. \n\n" + transcription
    )
    return response['choices'][0]['text']

#--Sentiment Analysis
def sentiment_analysis(transcription):
    response = openai.Completion.create(
        model="text-davinci-003",
        temperature=0,
        prompt="As an AI with expertise in language and emotion analysis, your task is to analyze the sentiment of the following text."
            "Please consider the overall tone of the discussion, the emotion conveyed by the language used, and the context in which words and phrases are used." 
            "Indicate whether the sentiment is generally positive, negative, or neutral, and provide brief explanations for your analysis where possible.\n\n" + transcription
    )
    return response['choices'][0]['text']


#--Exporting Meeting Minutes
def save_as_docx(minutes, filename):
    doc = Document()
    for key, value in minutes.items():
        # Replace underscores with spaces and capitalize each word for the heading
        heading = ' '.join(word.capitalize() for word in key.split('_'))
        doc.add_heading(heading, level=1)
        doc.add_paragraph(value)
        # Add a line break between sections
        doc.add_paragraph()
    doc.save(filename)

audio_file_path = "EarningsCall.mp3"
transcription = transcribe_audio(audio_file_path)
minutes = meeting_minutes(transcription)
print(minutes)

save_as_docx(minutes, 'meeting_minutes.docx')