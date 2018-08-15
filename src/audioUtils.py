# ==================================================================================
# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.

# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ==================================================================================
#
# audioUtils.py
# by: Rob Dachowski
# For questions or feedback, please contact robdac@amazon.com
# 
# Purpose: The program provides a number of utility audio functions used to create 
#          transcribed, translated, and subtitled videos using Amazon Transcribe,
#          Amazon Translate, Amazon Polly, and MoviePy
#
# Change Log:
#          6/29/2018: Initial version
#
# ==================================================================================


import boto3
import os
import json
import contextlib
from moviepy.editor import *
from moviepy import editor
from contextlib import closing

# ==================================================================================
# Function: writeAudio
# Purpose: writes the bytes associates with the stream to a binary file
# Parameters: 
#                 output_file - the name + extension of the ouptut file (e.g. "abc.mp3")
#                 stream - the stream of bytes to write to the output_file
# ==================================================================================
def writeAudio( output_file, stream ):

	bytes = stream.read()
	
	print "\t==> Writing ", len(bytes), "bytes to audio file: ", output_file
	try:
		# Open a file for writing the output as a binary stream
		with open(output_file, "wb") as file:
			file.write(bytes)
		
		if file.closed:
				print "\t==>", output_file, " is closed"
		else:
				print "\t==>", output_file, " is NOT closed"
	except IOError as error:
		# Could not write to file, exit gracefully
		print(error)
		sys.exit(-1)

# ==================================================================================
# Function: createAudioTrackFromTranslation
# Purpose: Using the provided transcript, get a translation from Amazon Translate, then use Amazon Polly to synthesize speech
# Prrameters: 
#                 region - the aws region in which to run the service
#                 transcript - the Amazon Transcribe JSON structure to translate
#                 sourceLangCode - the language code for the original content (e.g. English = "EN")
#                 targetLangCode - the language code for the translated content (e.g. Spanich = "ES")
#                 audioFileName - the name (including extension) of the target audio file (e.g. "abc.mp3")
# ==================================================================================
def createAudioTrackFromTranslation( region, transcript, sourceLangCode, targetLangCode, audioFileName ):
	print( "\n==> createAudioTrackFromTranslation " )
	
	# Set up the polly and translate services
	client = boto3.client('polly')
	translate = boto3.client(service_name='translate', region_name=region, use_ssl=True)

	#get the transcript text
	temp = json.loads( transcript)
	transcript_txt = temp["results"]["transcripts"][0]["transcript"]
	
	voiceId = getVoiceId( targetLangCode )
	
	# Now translate it.
	translated_txt = unicode((translate.translate_text(Text=transcript_txt, SourceLanguageCode=sourceLangCode, TargetLanguageCode=targetLangCode))["TranslatedText"])[:2999]

	# Use the translated text to create the synthesized speech
	response = client.synthesize_speech( OutputFormat="mp3", SampleRate="22050", Text=translated_txt, VoiceId=voiceId)
	
	if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
		print( "\t==> Successfully called Polly for speech synthesis")
		writeAudioStream( response, audioFileName )
	else:
		print( "\t==> Error calling Polly for speech synthesis")

	
# ==================================================================================
# Function: writeAudioStream
# Purpose: Utility to write an audio file from the response from the Amazon Polly API
# Prrameters: 
#                 response - the Amazaon Polly JSON response  
#                 audioFileName - the name (including extension) of the target audio file (e.g. "abc.mp3")
# ==================================================================================
def writeAudioStream( response, audioFileName ):
	# Take the resulting stream and write it to an mp3 file
	if "AudioStream" in response:
		with closing(response["AudioStream"]) as stream:
			output = audioFileName
			writeAudio( output, stream )



# ==================================================================================
# Function: getVoiceId
# Purpose: Utility to return the name of the voice to use given a language code.  Note: this is only populated with the
#          VoiceIds used for this example.   Refer to the Amazon Polly API documentation for other voiceId names
# Prrameters: 
#                 targetLangCode - the language code used for the target Amazon Polly output 
# ==================================================================================
def getVoiceId( targetLangCode ):

	# Feel free to add others as desired
	if targetLangCode == "es":
		voiceId = "Penelope"
	elif targetLangCode == "de":
		voiceId = "Marlene"
		
	return voiceId
	
	
# ==================================================================================
# Function: getSecondsFromTranslation
# Purpose: Utility to determine how long in seconds it will take for a particular phrase of translated text to be spoken
# Prrameters: 
#                 textToSynthesize - the raw text to be synthesized   
#                 targetLangCode - the language code used for the target Amazon Polly output 
#                 audioFileName - the name (including extension) of the target audio file (e.g. "abc.mp3")
# ==================================================================================
def getSecondsFromTranslation( textToSynthesize, targetLangCode, audioFileName ):

	# Set up the polly and translate services
	client = boto3.client('polly')
	translate = boto3.client(service_name='translate', region_name="us-east-1", use_ssl=True)
	
	# Use the translated text to create the synthesized speech
	response = client.synthesize_speech( OutputFormat="mp3", SampleRate="22050", Text=textToSynthesize, VoiceId=getVoiceId( targetLangCode ) )
	
	# write the stream out to disk so that we can load it into an AudioClip
	writeAudioStream( response, audioFileName )
	
	# Load the temporary audio clip into an AudioFileClip
	audio = AudioFileClip( audioFileName)
		
	# return the duration
	return audio.duration
	
	
	