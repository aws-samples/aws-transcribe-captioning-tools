# AWS VOD Captioning using AWS Transcribe

> Add subtitles to video with AWS machine learning services. Inlcuding AWS Polly, AWS Transcribe, and AWS Translate.

## Overview
This repository contains code for VOD subtitle creation, described in the AWS blog post [“Create video subtitles with translation using machine learning”](https://aws.amazon.com/blogs/machine-learning/create-video-subtitles-with-translation-using-machine-learning/).

## Prerequisites

- Set up an AWS account. ([instructions](https://AWS.amazon.com/free/?sc_channel=PS&sc_campaign=acquisition_US&sc_publisher=google&sc_medium=cloud_computing_b&sc_content=AWS_account_bmm_control_q32016&sc_detail=%2BAWS%20%2Baccount&sc_category=cloud_computing&sc_segment=102882724242&sc_matchtype=b&sc_country=US&s_kwcid=AL!4422!3!102882724242!b!!g!!%2BAWS%20%2Baccount&ef_id=WS3s1AAAAJur-Oj2:20170825145941:s))
- Clone this repo.
- The other requirements are listed in this ([blog post](https://aws.amazon.com/blogs/machine-learning/create-video-subtitles-with-translation-using-machine-learning/))  
- Configure AWS CLI and a local credentials file. ([instructions](http://docs.AWS.amazon.com/cli/latest/userguide/cli-chap-welcome.html))  


## Getting Started

Head on over to this blog post to see the instructions to create captions with AWS Transcribe in the SRT format, create alternate language SRT files with AWS Translate, and use AWS Polly to create alternate language video files:
https://aws.amazon.com/blogs/machine-learning/create-video-subtitles-with-translation-using-machine-learning/




## More AWS Transcribe Tools for Video

If you just want to create an SRT or a VTT file, the tools directory contains Python code to convert AWS Transcribe JSON to an SRT or a VTT file. These files can be imported and used on web or desktop video players. 

```shell
python srt.py output_file_from_transcribe.json
```


| name | description | 
|-------|-------------|
|srt.py | Takes the JSON response from AWS Transcribe and converts to a captions.srt file |
|vtt.py | Takes the JSON response from AWS Transcribe and converts to a captions.vtt file |


## License Summary

This sample code is made available under a modified MIT license. See the LICENSE file.
