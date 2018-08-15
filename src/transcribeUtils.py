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
# transcribeUtils.py
# by: Rob Dachowski
# For questions or feedback, please contact robdac@amazon.com
# 
# Purpose: The program provides a number of utility functions for leveraging the Amazon Transcribe API
#
# Change Log:
#          6/29/2018: Initial version
#
# ==================================================================================

import boto3
import uuid
import requests

# ==================================================================================
# Function: createTranscribeJob
# Purpose: Function to format the input parameters and invoke the Amazon Transcribe service
# Parameters: 
#                 region - the AWS region in which to run AWS services (e.g. "us-east-1")
#                 bucket - the Amazon S3 bucket name (e.g. "mybucket/") found in region that contains the media file for processing.   
#                 mediaFile - the content to process (e.g. "myvideo.mp4")
#
# ==================================================================================
def createTranscribeJob( region, bucket, mediaFile ):

	# Set up the Transcribe client 
	transcribe = boto3.client('transcribe')
	
	# Set up the full uri for the bucket and media file
	mediaUri = "https://" + "s3-" + region + ".amazonaws.com/" + bucket + mediaFile 
	
	print( "Creating Job: " + "transcribe" + mediaFile + " for " + mediaUri )
	
	# Use the uuid functionality to generate a unique job name.  Otherwise, the Transcribe service will return an error
	response = transcribe.start_transcription_job( TranscriptionJobName="transcribe_" + uuid.uuid4().hex + "_" + mediaFile , \
		LanguageCode = "en-US", \
		MediaFormat = "mp4", \
		Media = { "MediaFileUri" : mediaUri }, \
		Settings = { "VocabularyName" : "MyVocabulary" } \
		)
	
	# return the response structure found in the Transcribe Documentation
	return response
	
	
# ==================================================================================
# Function: getTranscriptionJobStatus
# Purpose: Helper function to return the status of a job running the Amazon Transcribe service
# Parameters: 
#                 jobName - the unique jobName used to start the Amazon Transcribe job
# ==================================================================================
def getTranscriptionJobStatus( jobName ):
	transcribe = boto3.client('transcribe')
	
	response = transcribe.get_transcription_job( TranscriptionJobName=jobName )
	return response
	
	
# ==================================================================================
# Function: getTranscript
# Purpose: Helper function to return the transcript based on the signed URI in S3 as produced by the Transcript job
# Parameters: 
#                 transcriptURI - the signed S3 URI for the Transcribe output
# ==================================================================================
def getTranscript( transcriptURI ):
	# Get the resulting Transcription Job and store the JSON response in transcript
	result = requests.get( transcriptURI )

	return result.text

	