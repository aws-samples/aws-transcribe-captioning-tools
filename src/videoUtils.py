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
# videoUtils.py
# by: Rob Dachowski
# For questions or feedback, please contact robdac@amazon.com
# 
# Purpose: This code drives the MoviePy functions needed to create the subtitled video
#
# Change Log:
#          6/29/2018: Initial version
#
# ==================================================================================

from moviepy.editor import *
from moviepy import editor
from moviepy.video.tools.subtitles import SubtitlesClip
from time import gmtime, strftime
from audioUtils import *


# ==================================================================================
# Function: annotate
# Purpose: This function creates a TextClip based on the provided text and composites the subtitle onto the provided clip.
#          Defaults are used for txt_color, fontsize, and font.   You can override them as desired
# Parameters: 
#                 clip - the clip to composite the text on 
#                 txt - the block of text to composite on the clip
#                 txt_color - the color of the text on the screen
#                 font_size - the size of the font to display
#                 font - the font to use for the text
#
# ==================================================================================
def annotate(clip, txt, txt_color='white', fontsize=24, font='Arial-Bold'):
    # Writes a text at the bottom of the clip  'Xolonium-Bold'
    txtclip = editor.TextClip(txt, fontsize=fontsize, font=font, color=txt_color).on_color(color=[0,0,0])
    cvc = editor.CompositeVideoClip([clip, txtclip.set_pos(('center', 50))])
    return cvc.set_duration(clip.duration)
	
# ==================================================================================
# Function: createVideo
# Purpose: This function drives the MoviePy code needed to put all of the pieces together and create a new subtitled video  
# Parameters: 
#                 originalClipName - the flename of the orignal conent (e.g. "originalVideo.mp4")
#                 subtitlesFileName - the filename of the SRT file (e.g. "mySRT.srt")
#                 outputFileName - the filename of the output video file (e.g. "outputFileName.mp4")
#                 alternateAudioFileName - the filename of an MP3 file that should be used to replace the audio track
#                 useOriginalAudio - boolean value as to whether or not we should leave the orignal audio in place or overlay it
#
# ==================================================================================
def createVideo( originalClipName, subtitlesFileName, outputFileName, alternateAudioFileName, useOriginalAudio=True ):
	# This function is used to put all of the pieces together.   
	# Note that if we need to use an alternate audio track, the last parm should = False
	
	print( "\n==> createVideo " )

	# Load the original clip
	print "\t" + strftime("%H:%M:%S", gmtime()), "Reading video clip: " + originalClipName 
	clip = VideoFileClip(originalClipName)
	print "\t\t==> Original clip duration: " + str(clip.duration)

	if useOriginalAudio == False:
		print strftime( "\t" + "%H:%M:%S", gmtime()), "Reading alternate audio track: " + alternateAudioFileName
		audio = AudioFileClip(alternateAudioFileName)
		audio = audio.subclip( 0, clip.duration )
		audio.set_duration(clip.duration)
		print "\t\t==> Audio duration: " + str(audio.duration)
		clip = clip.set_audio( audio )
	else:
		print strftime( "\t" + "%H:%M:%S", gmtime()), "Using original audio track..."
		
	# Create a lambda function that will be used to generate the subtitles for each sequence in the SRT
	generator = lambda txt: TextClip(txt, font='Arial-Bold', fontsize=24, color='white')

	# read in the subtitles files
	print "\t" + strftime("%H:%M:%S", gmtime()), "Reading subtitle file: " + subtitlesFileName 
	subs = SubtitlesClip(subtitlesFileName, generator)
	print "\t\t==> Subtitles duration before: " + str(subs.duration)
	subs = subs.subclip( 0, clip.duration - .001)
	subs.set_duration( clip.duration - .001 )
	print "\t\t==> Subtitles duration after: " + str(subs.duration)
	print "\t" + strftime("%H:%M:%S", gmtime()), "Reading subtitle file complete: " + subtitlesFileName 


	print "\t" + strftime( "%H:%M:%S", gmtime()), "Creating Subtitles Track..."
	annotated_clips = [annotate(clip.subclip(from_t, to_t), txt) for (from_t, to_t), txt in subs]



	print "\t" + strftime( "%H:%M:%S", gmtime()), "Creating composited video: " + outputFileName
	# Overlay the text clip on the first video clip
	final = concatenate_videoclips( annotated_clips )

	print "\t" + strftime( "%H:%M:%S", gmtime()), "Writing video file: " + outputFileName 
	final.write_videofile(outputFileName)