import json
import boto3
import re
import codecs
from audioUtils import *

translate = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)



# Create a new phrase structure
def newPhrase():
	return { 'start_time': '', 'end_time': '', 'words' : [] }

# Format and return a string that contains the converted number of seconds into WebVTT format
def getTimeCode( seconds ):
	t_hund = int(seconds % 1 * 1000)
	t_seconds = int( seconds )
	t_secs = ((float( t_seconds) / 60) % 1) * 60
	t_mins = int( t_seconds / 60 )
	return str( "%02d:%02d:%02d.%03d" % (00, t_mins, int(t_secs), t_hund ))
	

	
def writeTranscriptToWebVTT( transcript, sourceLangCode, WebVTTFileName ):
	# Write the WebVTT file for the original language
	print( "==> Creating WebVTT from transcript")
	phrases = getPhrasesFromTranscript( transcript )
	writeWebVTT( phrases, WebVTTFileName, "A:middle L:90%" ) 
	
	
def writeTranslationToWebVTT( transcript, sourceLangCode, targetLangCode, WebVTTFileName ):
	# First get the translation
	print( "\n\n==> Translating from " + sourceLangCode + " to " + targetLangCode )
	translation = translateTranscript( transcript, sourceLangCode, targetLangCode )
	#print( "\n\n==> Translation: " + str(translation))
		
	# Now create phrases from the translation
	textToTranslate = unicode(translation["TranslatedText"])
	phrases = getPhrasesFromTranslation( textToTranslate, targetLangCode )
	writeWebVTT( phrases, WebVTTFileName, "A:middle L:90%" )
	
	
def getPhrasesFromTranslation( translation, targetLangCode ):

	# Now create phrases from the translation
	words = translation.split()
	
	#print( words ) #debug statement
	
	#set up some variables for the first pass
	phrase =  newPhrase()
	phrases = []
	nPhrase = True
	x = 0
	c = 0
	seconds = 0

	print "==> Creating phrases from translation..."

	for word in words:

		# if it is a new phrase, then get the start_time of the first item
		if nPhrase == True:
			phrase["start_time"] = getTimeCode( seconds )
			nPhrase = False
			c += 1
				
		# Append the word to the phrase...
		phrase["words"].append(word)
		x += 1
		
		
		# now add the phrase to the phrases, generate a new phrase, etc.
		if x == 10:
		
			# For Translations, we now need to calculate the end time for the phrase
			psecs = getSecondsFromTranslation( getPhraseText( phrase), targetLangCode, "phraseAudio" + str(c) + ".mp3" ) 
			seconds += psecs
			phrase["end_time"] = getTimeCode( seconds )
		
			#print c, phrase
			phrases.append(phrase)
			phrase = newPhrase()
			nPhrase = True
			#seconds += .001
			x = 0
			
		#if c == 30:
		#	break
			
	return phrases
	
	
def getPhrasesFromTranscript( transcript ):

	# This function is intended to be called with the JSON structure output from the Transcribe service.  However,
	# if you only have the translation of the transcript, then you should call getPhrasesFromTranslation instead

	# Now create phrases from the translation
	ts = json.loads( transcript )
	items = ts['results']['items']
	#print( items )
	
	#set up some variables for the first pass
	phrase =  newPhrase()
	phrases = []
	nPhrase = True
	x = 0
	c = 0

	print "==> Creating phrases from transcript..."

	for item in items:

		# if it is a new phrase, then get the start_time of the first item
		if nPhrase == True:
			if item["type"] == "pronunciation":
				phrase["start_time"] = getTimeCode( float(item["start_time"]) )
				nPhrase = False
			c+= 1
		else:	
			# get the end_time if the item is a pronuciation and store it
			# We need to determine if this pronunciation or puncuation here
			# Punctuation doesn't contain timing information, so we'll want
			# to set the end_time to whatever the last word in the phrase is.
			if item["type"] == "pronunciation":
				phrase["end_time"] = getTimeCode( float(item["end_time"]) )
				
		# in either case, append the word to the phrase...
		phrase["words"].append(item['alternatives'][0]["content"])
		x += 1
		
		# now add the phrase to the phrases, generate a new phrase, etc.
		if x == 10:
			#print c, phrase
			phrases.append(phrase)
			phrase = newPhrase()
			nPhrase = True
			x = 0
	
	# if there are any words in the final phrase add to phrases  
	if(len(phrase["words"]) > 0):
		phrases.append(phrase)	
			
	return phrases
	




def translateTranscript( transcript, sourceLangCode, targetLangCode ):
	# Get the translation in the target language.  We want to do this first so that the translation is in the full context
	# of what is said vs. 1 phrase at a time.  This really matters in some lanaguages

	# stringify the transcript
	ts = json.loads( transcript )

	# pull out the transcript text and put it in the txt variable
	txt = ts["results"]["transcripts"][0]["transcript"]
		
	# call Translate  with the text, source language code, and target language code.  The result is a JSON structure containing the 
	# translated text
	translation = translate.translate_text(Text=txt,SourceLanguageCode=sourceLangCode, TargetLanguageCode=targetLangCode)
	
	return translation
	
	

def writeWebVTT( phrases, filename, style ):
	print "==> Writing phrases to disk..."

	# open the files
	e = codecs.open(filename,"w+", "utf-8")
	x = 1
	
	# write the header of the webVTT file
	e.write( "WEBVTT\n\n")
	
	for phrase in phrases:

		# determine how many words are in the phrase
		length = len(phrase["words"])
		
		# write out the phrase number
		e.write( str(x) + "\n" )
		x += 1
		
		# write out the start and end time
		e.write( phrase["start_time"] + " --> " + phrase["end_time"] + " " + style + "\n" )
					
		# write out the full phase.  Use spacing if it is a word, or punctuation without spacing
		out = getPhraseText( phrase )

		# write out the WebVTT file
		e.write(out + "\n\n" )
		

		#print out
		
	e.close()
	


def getPhraseText( phrase ):

	length = len(phrase["words"])
		
	out = ""
	for i in range( 0, length ):
		if re.match( '[a-zA-Z0-9]', phrase["words"][i]):
			if i > 0:
				out += " " + phrase["words"][i]
			else:
				out += phrase["words"][i]
		else:
			out += phrase["words"][i]
			
	return out
	

			

	


	
	