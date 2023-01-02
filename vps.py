#!/bin/python3
#https://github.com/andrea-varesio/vsco-profile-saver
#version = 20230102.01

'''Download all media files from your VSCO account'''

import argparse
import asyncio
import datetime
import json
import os
import pathlib
import sys
import time

import requests

cwd = os.path.dirname(os.path.realpath(__file__))

def show_license():
    '''Show License'''

    print('\n**************************************************')
    print('"vsco-profile-saver": Download all media files from your VSCO account')
    print('Copyright (C) 2023 Andrea Varesio (https://www.andreavaresio.com/).')
    print('This program comes with ABSOLUTELY NO WARRANTY')
    print('This is free software, and you are welcome to redistribute it under certain conditions')
    print('Full license available at https://github.com/andrea-varesio/vsco-profile-saver')
    print('**************************************************\n\n')

def parse_arguments():
    '''Parse arguments'''

    arg = argparse.ArgumentParser(description='Download all media files from your VSCO account')
    input_group = arg.add_mutually_exclusive_group()
    verbosity = arg.add_mutually_exclusive_group()

    arg.add_argument('-l', '--license', help='show license and exit', action='store_true')
    input_group.add_argument('-i', '--input', help='path to input images.json', type=str)
    input_group.add_argument('-r', '--resume', help='resume last session', action='store_true')
    input_group.add_argument('-R', '--resume-file', help='resume specified session', type=str)
    arg.add_argument('-o', '--output-dir', help='path to output dir (Default: $HOME)', type=str)
    verbosity.add_argument('-v', '--verbose', help='increase verbosity', action='store_true')
    verbosity.add_argument('-q', '--quiet', help='disable all verbosity', action='store_true')

    return arg.parse_args()

def quiet(text):
    '''Print text if not quiet'''

    args = parse_arguments()

    if not args.quiet:
        print(text)

def verbose(text):
    '''Print text if verbose'''

    args = parse_arguments()

    if args.verbose:
        print(text)

def check_args():
    '''Check if required arguments have been passed'''

    args = parse_arguments()

    if args.license:
        show_license()
        sys.exit(0)

    if not (args.input or args.resume or args.resume_file):
        quiet('[ERROR] Missing required argument: INPUT')
        quiet('Specify an input file [-i], or a resume action [-r | -R]')
        quiet(f'Type "{os.path.realpath(__file__)} --help" for more info.')
        sys.exit(1)

    if args.resume_file and not os.path.isfile(args.resume_file):
        quiet(f'[ERROR] FileNotFound: {args.resume_file}')
        sys.exit(1)

    if args.resume:
        sessions = os.path.join(cwd, 'sessions')
        if (os.path.isdir(sessions) and not os.listdir(sessions)) or not os.path.isdir(sessions):
            quiet('[ERROR] FileNotFound: no previous sessions found')
            sys.exit(1)

    if args.input and not os.path.isfile(args.input):
        quiet(f'[ERROR] FileNotFound: {args.input}')
        sys.exit(1)

def get_timestamp():
    '''Get current timestamp'''

    return datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

def get_output_dir(timestamp=get_timestamp()):
    '''Get output directory'''

    args = parse_arguments()

    if not args.output_dir:
        return os.path.join(pathlib.Path.home(), f'VSCO_{timestamp}')

    if os.path.isdir(args.output_dir):
        if args.output_dir.startswith('./'):
            output_dir_root = os.path.join(os.getcwd(), args.output_dir.replace('./', '', 1))
        elif args.output_dir == '.':
            output_dir_root = args.output_dir.replace('.', os.getcwd())
        else:
            output_dir_root = args.output_dir

        return os.path.join(output_dir_root, f'VSCO_{timestamp}')

    quiet('Invalid output path')
    sys.exit(1)

def get_session(timestamp):
    '''Define url list and return its filepath'''

    args = parse_arguments()

    if args.resume_file:
        session_file = args.resume_file

    if args.resume:
        session_filename = max(os.listdir(os.path.join(cwd, 'vsco_sessions')))
        session_file = os.path.join(cwd, 'vsco_sessions', session_filename)

    if args.input:
        sessions_dir = os.path.join(cwd, 'vsco_sessions')
        session_file = os.path.join(sessions_dir, f'{timestamp}_url_list.tmp')

        if not os.path.isdir(sessions_dir):
            os.mkdir(sessions_dir)

        with open(args.input, 'r', encoding='utf-8') as media_json:
            json_load = json.load(media_json)
            with open(session_file, 'a', encoding='utf-8') as session:
                for i, _ in enumerate(json_load):
                    key = 'responsive_url'
                    session.write(json_load[i][key].replace('im.vsco', '\nhttps://im.vsco'))

    return session_file

def remove_file(file_path):
    '''Remove file'''

    try:
        os.remove(file_path)
    except IsADirectoryError:
        os.rmdir(file_path)
    except (FileNotFoundError, OSError):
        pass

async def download_media(output_dir, session_file, url):
    '''Download media'''

    filename = os.path.basename(url)
    file_path = os.path.join(output_dir, filename)

    try:
        with open(file_path, 'wb') as media:
            media.write(requests.get(url).content)
        with open(session_file, 'r+', encoding='utf-8') as session:
            lines = session.readlines()
            session.seek(0)
            for line in lines:
                if line.strip('\n') not in (url, '\n'):
                    session.write(line)
            session.truncate()
        verbose(f'Saved {filename}')
    except (ConnectionError, requests.exceptions.SSLError):
        quiet(f'[ERROR] ConnectionError: {filename}')
        remove_file(file_path)

def cleanup(session_file):
    '''Cleanup empty temporary session file'''

    sessions_dir = os.path.join(cwd, 'vsco_sessions')

    with open(session_file, 'r', encoding='utf-8') as session:
        url_list = session.readlines()

    if len(url_list) == 0 or (len(url_list) == 1 and url_list[0] == '\n'):
        remove_file(session_file)

    if os.path.isdir(sessions_dir) and len(os.listdir(sessions_dir)) == 0:
        remove_file(sessions_dir)

def main():
    '''Main function'''

    check_args()

    try:
        timestamp = get_timestamp()
        os.mkdir(get_output_dir(timestamp))
    except FileExistsError:
        time.sleep(2)
        timestamp = get_timestamp()
        os.mkdir(get_output_dir(timestamp))
    finally:
        output_dir = get_output_dir(timestamp)
        quiet(f'Saving media in: {output_dir}')

    session_file = get_session(timestamp)

    with open(session_file, 'r', encoding='utf-8') as session:
        url_list = session.readlines()

    url_list = [url.strip() for url in url_list]

    for url in url_list:
        if url.startswith('https://'):
            asyncio.run(download_media(output_dir, session_file, url))

    cleanup(session_file)

if __name__ == '__main__':
    main()
