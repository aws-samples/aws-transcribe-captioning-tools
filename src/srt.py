import sys

from srtUtils import *

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, "r") as f:
      data = writeTranscriptToSRT(f.read(), 'en', output_file )