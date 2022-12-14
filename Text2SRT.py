import os
import re
from datetime import datetime, timedelta

def timedelta_2_str(timedlt: timedelta, timedlt_format: str = "%H:%M:%S") -> str:
    '''
    Easily convert a datetime.timedelta to a string
    '''
    time_base = datetime.min
    timedlt_str = datetime.strftime(time_base+timedlt, timedlt_format)
    return timedlt_str


def timed_sub_list_2_srt(subtitles: list[dict]) -> str:
    '''
    Accepts a list of the format:
    [
        {
            "timings" : ( <start timedelta> , <end timedelta> ),
            "text" : " <some text> "
        },
        ...
    ]
    
    And converts it into an srt file formatted string.
    '''

    timing_str_format = "%H:%M:%S,%f"

    default_timing = (timedelta(seconds=0), timedelta(seconds=1))
    def __get_timings_of_subtitle(sub_index: int):
        '''
        An overengineered way to always return a subtitle's timings.
        If there is no timing information it generates it (almost certainly an incorrect one) and 
        modifies the original input subtitle list so that it remains consistent throughout the
        execution of the function
        '''
        
        nonlocal subtitles
        
        if "timings" not in subtitles[sub_index].keys():
            # There is no timing for this subtitle
            if sub_index > 0:
                # There is a previous subtitle
                previous_timings = subtitles[sub_index-1]["timings"]
                
                # Add a second to the previous' start and end
                modified_timings = (
                    previous_timings[0] + timedelta(seconds=1),
                    previous_timings[1] + timedelta(seconds=1)
                )

                # update the original input list
                subtitles[sub_index]["timings"] = modified_timings
            else:
                # This is the first subtitle. Just add the default timing
                subtitles[sub_index]["timings"] = default_timing
        
        return subtitles[sub_index]["timings"]
    

    srt_file_text = ""
    for sub_index, sub in enumerate(subtitles):
        timings: tuple[timedelta] = sub.get("timings", __get_timings_of_subtitle(sub_index))
        text = sub.get("text", None)
        
        # Convert the timedeltas to strings.
        # Chop off the last 3 digits.
        # According to this https://stackoverflow.com/a/11040248 it is better than rounding
        start_time_text = timedelta_2_str(timings[0], timing_str_format)[:-3]
        end_time_text = timedelta_2_str(timings[1], timing_str_format)[:-3]
        
        current_sub_text = f"{sub_index+1}\n{start_time_text} --> {end_time_text}\n{text}\n\n"

        srt_file_text += current_sub_text


    return srt_file_text


def read_transcript_file(input_file_dir: str) -> list[str]:
    '''
    Reads a .txt file and returns its contents as a list
    '''

    if not os.path.isfile(input_file_dir):
        raise ValueError(f"Couldn't find file '{input_file_dir}'")
    
    with open(input_file_dir, 'r') as input_file:
        contents = input_file.read()
    
    contents = re.split('\n{2,}', contents)
    
    return contents


def save_srt_string_to_srt_file(srt_text: str, output_file_dir: str) -> None:
    '''
    It saves the srt formatted text to an .srt file
    '''

    with open(output_file_dir, 'w') as output_file:
        output_file.write(srt_text)
