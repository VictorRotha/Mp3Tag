import os
import sys
import mutagen as mut


def parse_tagfile(file):
    tag = None
    tracks = False

    tags = {}
    values = []

    with open(file) as f:
        for line in f.readlines():
            if line.startswith('#') or len(line.strip()) == 0:
                continue
            if line.startswith('tracks='):
                tracks = line.split('=')[1].strip() == 'true'
                continue
            if line.startswith('tag='):
                if tag is not None and len(values) > 0:
                    tags[tag] = values
                values = []
                tag = line.split('=')[1].strip()
                continue

            values.append(line.strip())

        tags[tag] = values

    return tracks, tags


def get_target_files(mp3dir):
    files = [os.path.join(mp3dir, f) for f in os.listdir(mp3dir) if f.endswith('.mp3')]
    files.sort()
    return files


def get_file_info(files, tags):

    result = {}
    for file in files:
        info = {}
        easy = mut.File(file, easy=True)

        filename = os.path.split(file)[1]
        info["filename"] = filename

        for tag in tags:
            try:
                info[tag] = easy[tag][0]
            except KeyError:
                info[tag] = 'N/A'

        result[filename] = info

    return result


def print_file_info(fileinfo, tags):
    col_space = {'artist': 30, 'album': 30, 'title': 30, 'filename': 75}
    print(
        f'\n{"ARTIST":<{col_space["artist"]}}{"ALBUM":<{col_space["album"]}}{"TITLE":<{col_space["title"]}}'
        f'{"FILENAME":<{col_space["filename"]}}', end='')

    other = [tag for tag in tags if tag not in ['artist', 'album', 'title', 'filename']]

    for o in other:
        print(f'{o:<30}', end='')
    print()

    keys = list(fileinfo.keys())
    keys.sort()

    for fn in keys:

        info = fileinfo[fn]

        print(f'{info["artist"]:<{col_space["artist"]}}{info["album"]:<{col_space["album"]}}'
              f'{info["title"]:<{col_space["title"]}}'
              f'{info["filename"]:<{col_space["filename"]}}', end = '')

        for o in other:
            try:
                print(f'{info[o]:<20}', end='')
            except KeyError:
                print(f'{"N/A":<20}', end='')

        print()


def create_preview(fileinfo, tags):
    print(fileinfo)
    result = {}
    keys = list(fileinfo.keys())
    keys.sort()
    for n, fn in enumerate(keys):
        info = fileinfo[fn]
        preview = {}
        for tag in fileinfo[fn]:
            if tag in tags:
                if n < len(tags[tag]):
                    preview[tag] = tags[tag][n]
                else:
                    preview[tag] = info[tag]
            else:
                preview[tag] = info[tag]
        result[fn] = preview

    return result


def apply_changes(audiofiles, fileinfo):

    for file in audiofiles:

        fn = os.path.split(file)[1]

        easy = mut.File(file, easy=True)
        info = fileinfo[fn]

        for tag in info:
            if tag == "filename":
                continue
            try:
                easy[tag] = info[tag]
            except KeyError:
                print("invalid key: ", tag)
        easy.save()


if __name__ == '__main__':

    print(sys.argv)

    directory = os.getcwd()
    tagfile = 'tagssample.txt'
    tagfile = os.path.join(os.getcwd(), tagfile)

    if not os.path.exists(tagfile):
        print('ERROR: ', tagfile, "doesn't exist!")
        quit(0)

    config = parse_tagfile(tagfile)
    print(config[0], "    ", config[1])

    audio_files = get_target_files(directory)
    print("mp3Files ", audio_files)

    for tag in config[1]:
        if len(config[1][tag]) == 1:
            config[1][tag] = config[1][tag] * len(audio_files)

    print(config[0], "    ", config[1])

    fileinfo = get_file_info(audio_files, config[1])

    print_file_info(fileinfo, config[1])

    new_fileinfo = create_preview(fileinfo, config[1])

    print("preview size ", len(new_fileinfo))

    print_file_info(new_fileinfo, config[1])

    choice = input('APPLY CHANGES? (y/n) ')
    if choice.lower() == 'y':
        apply_changes(audio_files, new_fileinfo)
        input('\nPRESS <ENTER> TO EXIT')

