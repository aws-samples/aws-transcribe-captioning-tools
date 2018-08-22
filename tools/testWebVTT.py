import argparse
from transcribeUtils import *
from webvttUtils import *
import requests
from videoUtils import *
from audioUtils import *

# Get the command line arguments and parse them
parser = argparse.ArgumentParser( prog='testWebVTT.py', description='Process a video found in the input file, process it, and write tit out to the output file')
parser.add_argument('-region', required=True, help="The AWS region containing the S3 buckets" )
parser.add_argument('-inbucket', required=True, help='The S3 bucket containing the input file')
parser.add_argument('-infile', required=True, help='The input file to process')
parser.add_argument('-outbucket', required=True, help='The S3 bucket containing the input file')
parser.add_argument('-outfilename', required=True, help='The file name without the extension')
parser.add_argument('-outfiletype', required=True, help='The output file type.  E.g. mp4, mov')
parser.add_argument('-outlang', required=True, nargs='+', help='The language codes for the desired output.  E.g. en = English, de = German')		
parser.add_argument('-TranscriptJob', required=True, help='The URI resulting from the transcript job')
args = parser.parse_args()


job = getTranscriptionJobStatus( args.TranscriptJob )
#print( job )


# Now get the transcript JSON from AWS Transcribe
transcript = getTranscript( str(job["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]) ) 
#print( "\n==> Transcript: \n" + transcript)

# Create the WebVTT File for the original transcript and write it out.  
writeTranscriptToWebVTT( transcript, 'en', "subtitles-en.vtt")
#createVideo( args.infile, "subtitles-en.vtt", args.outfilename + "-en." + args.outfiletype, "audio-en.mp3", True)


# Now write out the translation to the transcript for each of the target languages
for lang in args.outlang:
	writeTranslationToWebVTT(transcript, 'en', lang, "subtitles-" + lang + ".vtt" ) 	
	
	#Now that we have the subtitle files, let's create the audio track
	#createAudioTrackFromTranslation( args.region, transcript, 'en', lang, "audio-" + lang + ".mp3" )
	
	# Finally, create the composited video
	#createVideo( args.infile, "subtitles-" + lang + ".WebVTT", args.outfilename + "-" + lang + "." + args.outfiletype, "audio-" + lang + ".mp3", False)


