import sys

from Text2SRT import *

def main(input_file_dir, output_file_name):
    '''
    Accepts the path of the input file and the name of the output file.
    If everything goes well then it converts the input file to an srt
    in the same location
    '''

    # Read the transcript and convert it to a list
    transcript_list = read_transcript_file(input_file_dir)

    # Convert the list of strings to a compatible list of dictionaries
    subtitles_list = [ {"text" : sub} for sub in transcript_list ]

    # Convert to a srt string
    subtitle_srt = timed_sub_list_2_srt(subtitles_list)

    # Save the text to a file
    save_srt_string_to_srt_file(subtitle_srt, output_file_name)

    
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
