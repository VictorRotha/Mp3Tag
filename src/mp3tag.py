import os
import sys
import mutagen as mut
from mutagen.id3 import ID3, APIC


def parse_tagfile(file):
    tag = None
    tracks = False
    cover = False
    rename = False

    tags = {}
    values = []

    with open(file) as f:
        for line in f.readlines():
            if line.startswith('#') or len(line.strip()) == 0:
                continue
            if line.startswith('tracks='):
                tracks = line.split('=')[1].strip().lower() == 'true'
                continue
            if line.startswith('rename='):
                rename = line.split('=')[1].strip().lower() == 'true'
                continue
            if line.startswith('cover'):
                cover = line.split('=')[1].strip().lower() == 'true'
                continue
            if line.startswith('tag='):
                if tag is not None:
                    tags[tag] = values
                values = []
                tag = line.split('=')[1].strip()
                continue

            values.append(line.strip())

        tags[tag] = values

    return tracks, cover, rename, tags


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
                info[tag] = None

        if tracks:
            try:
                info['tracknumber'] = easy['tracknumber'][0]
            except KeyError:
                info['tracknumber'] = None

        result[filename] = info

    return result


def print_file_info(fileinfo):
    if len(fileinfo) == 0:
        print('ERROR: fileinfo is empty')
        quit(())

    col_space = {'filename': 75, 'default': 30}

    print(f'\n{"FILENAME":<{col_space["filename"]}}', end='')

    values = [fileinfo[k] for k in fileinfo.keys()]
    for tag in values[0]:
        if tag == 'filename':
            continue
        print(f'{tag.upper():<{col_space["default"]}}', end='')

    print()

    keys = list(fileinfo.keys())
    keys.sort()

    for fn in keys:

        info = fileinfo[fn]
        print(f'{info["filename"]:<{col_space["filename"]}}', end='')
        for tag in info:
            if tag == 'filename':
                continue
            if info[tag] is None:
                print(f'{"":<{col_space["default"]}}', end='')
                continue
            print(f'{info[tag]:<{col_space["default"]}}', end='')

        print()


def create_preview(fileinfo, tags):
    result = {}
    keys = list(fileinfo.keys())
    keys.sort()

    for n, fn in enumerate(keys):
        info = fileinfo[fn]
        preview = {}
        for k in info:
            if k == 'filename':
                preview[k] = info[k]
                continue
            if k == 'tracknumber':
                preview[k] = f'{str(n+1):0>2}'
                continue
            if len(tags[k]) == 0:
                preview[k] = None
                continue

            if n < len(tags[k]):
                preview[k] = tags[k][n]
            else:
                preview[k] = info[k]

        result[fn] = preview

    return result


def create_new_filename(fileinfo):

    for file in fileinfo:
        artist = 'Unknown'
        album = ''
        title = ''
        tnr = ''

        if 'artist' in fileinfo[file]:
            artist = fileinfo[file]['artist']
        if 'album' in fileinfo[file]:
            album = fileinfo[file]['album']
        if 'title' in fileinfo[file]:
            title = fileinfo[file]['title']
        if 'tracknumber' in fileinfo[file]:
            tnr = fileinfo[file]['tracknumber']

        ext = os.path.splitext(file)[1]
        old_fn = os.path.split(file)[1]

        fn = f'{artist} - {album} {tnr} - {title}{ext}'

        fileinfo[file]['filename'] = fn



def find_cover(directory):

    covers = [os.path.join(directory, f) for f in os.listdir(directory)
              if f.endswith(".jpg") or f.endswith(".png") or f.endswith(".jpeg")]

    if len(covers) == 0:
        return None

    return covers[0]


def apply_cover(image, fileinfo):

    with open(image, 'rb') as albumart:
        data = albumart.read()

    if image.endswith('.png'):
        mime_type = 'image/png'
    else:
        mime_type = 'image/jpg'

    for fn in fileinfo:
        audio = mut.id3.ID3(fn)
        audio.setall('APIC', [APIC(mime=mime_type,
                                   encoding=3,
                                   type=3,
                                   desc=u'frontcover',
                                   data=data)]
                     )
        audio.save()


def apply_changes(new_fileinfo):

    for fn in new_fileinfo:

        easy = mut.File(fn, easy=True)
        info = new_fileinfo[fn]

        for tag in info:
            if tag == "filename":
                continue
            if info[tag] is None:
                try:
                    easy.pop(tag)
                except KeyError:
                    pass
                continue
            try:
                easy[tag] = info[tag]
            except KeyError:
                print("invalid key: ", tag)
        easy.save()


def apply_new_filenames(new_fileinfo):

    for file in new_fileinfo:
        fn = new_fileinfo[file]['filename']
        fn = os.path.join(os.path.split(file)[0], fn)

        os.rename(file, fn)



if __name__ == '__main__':

    directory = os.getcwd()
    tagfile = 'mp3tag.config'
    if len(sys.argv) > 1:
        tagfile = sys.argv[1]
    tagfile = os.path.join(os.getcwd(), tagfile)

    if not os.path.exists(tagfile):
        print('ERROR: ', tagfile, "doesn't exist!")
        quit(0)

    audio_files = get_target_files(directory)
    tracks, cover, rename, tags = parse_tagfile(tagfile)

    for tag in tags:
        if len(tags[tag]) == 1:
            tags[tag] = tags[tag] * len(audio_files)

    fileinfo = get_file_info(audio_files, tags)

    print('\n-- OLD --')
    print_file_info(fileinfo)

    new_fileinfo = create_preview(fileinfo, tags)
    if rename:
        create_new_filename(new_fileinfo)

    print('\n-- NEW --')
    print_file_info(new_fileinfo)

    print()
    if tracks:
        print('Track numbers will be generated!')
    if rename:
        print("Files will be renamed!")

    albumart = None
    if cover:
        albumart = find_cover(directory)
        if albumart is None:
            print("Can not find any albumart. Please provide cover as .jpg, .jpeg or .png!")
        else:
            print(f'Frontcover will be set to {albumart}')

    choice = input('\nAPPLY CHANGES? (y/n) ')
    if choice.lower() == 'y':
        apply_changes(new_fileinfo)
        if cover and albumart is not None:
            apply_cover(albumart, new_fileinfo)
        if rename:
            apply_new_filenames(new_fileinfo)
        input('\nPRESS <ENTER> TO EXIT')

