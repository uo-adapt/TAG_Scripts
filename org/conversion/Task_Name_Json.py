# This python script adds 'TaskName: "rest"' to the end of the resting state json files 
# If you want to use this for other tasks or multiple runs (I think) you must change 
# line 54 f.endswith('rest_bold.json') to whatever your specif task name is
 
import os
import json
import re
from pprint import pprint

# Change these to your own paths/times/etc.
bidsdir = os.path.join(os.sep, 'projects', 'adapt_lab', 'shared', 'SHARP', 'bids_data')

# Change these to whatever your task names are. You must make sure that the amount of variables here match the amount of if stamements in the write_to_json() function. 

def main():
    subjectdirs = get_subjectdirs()
    for subjectdir in subjectdirs:
        timepoints = get_timepoints(subjectdir)
        for timepoint in timepoints:
            func_dir_path = os.path.join(bidsdir, subjectdir, timepoint, 'func')
            if os.path.isdir(func_dir_path):
                func_jsons = get_func_jsons(func_dir_path)
                write_to_json(func_jsons, func_dir_path)
            else:
                continue


def get_subjectdirs() -> list:
    """
    Returns subject directory names (not full path) based on the bidsdir (bids_data directory).
    @rtype:  list
    @return: list of bidsdir directories that start with the prefix sub
    """
    bidsdir_contents = os.listdir(bidsdir)
    has_sub_prefix = [subdir for subdir in bidsdir_contents if subdir.startswith('sub-')]
    subjectdirs = [subdir for subdir in has_sub_prefix if os.path.isdir(os.path.join(bidsdir, subdir))]
    subjectdirs.sort()
    return subjectdirs


def get_timepoints(subject: str) -> list:
    """
    Returns a list of ses-wave directory names in a participant's directory.
    @type subject:  string
    @param subject: subject folder name
    @rtype:  list
    @return: list of ses-wave folders in the subject directory
    """
    subject_fullpath = os.path.join(bidsdir, subject)
    subjectdir_contents = os.listdir(subject_fullpath)
    return [f for f in subjectdir_contents if not f.startswith('.')]

def get_func_jsons(func_dir_path):
    func_jsons = [f for f in os.listdir(func_dir_path) if f.endswith('bold.json')]
    return func_jsons

def write_to_json(func_jsons:list, func_dir_path:str):
    for func_json in func_jsons:
        if func_json.endswith('_bold.json'):
            json_path = os.path.join(func_dir_path, func_json)
            with open(json_path) as target_json:
                json_file = json.load(target_json)
                json_file['TaskName'] = re.search('task-(.+?)_bold.json', func_json).group(1)
            with open(json_path, 'w') as target_json:
                json.dump(json_file, target_json, indent=4)

main()
