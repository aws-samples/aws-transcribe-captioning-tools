REM ==================================================================================
REM Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.

REM Permission is hereby granted, free of charge, to any person obtaining a copy of this
REM software and associated documentation files (the "Software"), to deal in the Software
REM without restriction, including without limitation the rights to use, copy, modify,
REM merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
REM permit persons to whom the Software is furnished to do so.

REM THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
REM INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
REM PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
REM HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
REM OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
REM SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
REM ==================================================================================
REM
REM makevideo.bat
REM by: Rob Dachowski
REM For questions or feedback, please contact robdac@amazon.com
REM 
REM Purpose: This batchfile invokes the translatevideo.py file with parameters 
REM
REM Change Log:
REM          6/29/2018: Initial version
REM
REM ==================================================================================

cls
python translatevideo.py -region us-east-1 -inbucket robdac-aiml-test/ -infile AWS_reInvent_2017.mp4 -outbucket robdac-aiml-test/ -outfilename subtitledVideo -outfiletype mp4 -outlang es de
