# diese datei, audiotags.txt und mp3-dateien müssen sich im selben Verzeichnis befinden
# audiotags.txt:
#   erste zeile ist der tag (title, album, artist, ...) der geändert werden soll, der rest die tag-Werte
#   wenn nur EIN Wert angegeben ist, wird er auf ALLE Audiodateien angewendet
#   wenn KEIN Wert angegeben ist, wird der tag aus ALLEN Dateien gelöscht


import os
import mutagen as mut


def tag_info(audiofiles, newtags, tag):
    col_space = {'artist': 30, 'album': 30, 'title': 40, 'filename': 75, 'default': 50}
    print(
        f'\n{"ARTIST":<{col_space["artist"]}}'
        f'{"ALBUM":<{col_space["album"]}}'
        f'{"TITLE":<{col_space["title"]}}'
        f'{"NEW " + tag.upper():<{col_space["default"]}}', end='')

    if tag not in ('artist', 'album', 'title'):
        print(f'{"OLD " + tag.upper():<{col_space["default"]}}', end='')

    print(f'{"FILENAME":<{col_space["filename"]}}')

    for i, file in enumerate(audiofiles):
        easy = mut.File(file, easy=True)
        try:
            nt = newtags[i]
        except IndexError:
            nt = 'N/A'
        try:
            art = easy["artist"][0]
        except KeyError:
            art = 'N/A'
        try:
            alb = easy["album"][0]
        except KeyError:
            alb = 'N/A'
        try:
            tit = easy["title"][0]
        except KeyError:
            tit = 'N/A'

        print(f'{art:<{col_space["artist"]}}'
              f'{alb:<{col_space["album"]}}'
              f'{tit:<{col_space["title"]}}'
              f'{nt:<{col_space["default"]}}', end='')

        if tag not in ('artist', 'album', 'title'):
            try:
                other = easy[tag][0]
            except KeyError:
                other = 'N/A'

            print(f'{other:<{col_space["default"]}}', end='')


        print(f'{os.path.split(file)[1]:<{col_space["filename"]}}')


    if len(newtags) > len(audiofiles):
        space = ' ' * (col_space['artist'] + col_space['album'] + col_space['title'])

        for i, tag in enumerate(newtags):
            if i >= len(audiofiles):
                print(f'{space}{tag:<{col_space["tagfile"]}}')


def apply_changes(audiofiles, newvalues, tag):
    for i, file in enumerate(audiofiles):
        if i >= len(newvalues):
            break
        easy = mut.File(file, easy=True)
        try:
            easy[tag] = newvalues[i]
        except KeyError:
            print(f'ERROR: {tag} is not a valid tag')
            quit(0)
        easy.save()


def parse_audiotags(tag_file, file_count):

    if not os.path.exists(tag_file):
        print('ERROR: ', tag_file, 'existiert nicht!')
        quit(0)

    with open(tag_file) as f:
        values = f.read().strip().split('\n')

        tag = values.pop(0)
        if len(values) == 1:
            values = values * file_count
        if len(values) == 0:
            values = [''] * file_count

    return tag, values


if __name__ == '__main__':

    mp3directory = os.getcwd()  # verzeichnis in dem die mp3s liegen
    tagfile = 'audiotags.txt'  # datei mit der tag/value-liste
    tag_default = 'title'

    print('Directory:', mp3directory)
    print('Tagfile: ', tagfile)

    mp3files = [os.path.join(mp3directory, f) for f in os.listdir(mp3directory) if f.endswith(".mp3")]
    mp3files.sort()

    if len(mp3files) == 0:
        print('ERROR: no audiofiles found')
        quit(0)

    tagfile = os.path.join(os.getcwd(), tagfile)
    parse_result = parse_audiotags(tagfile, len(mp3files))

    tag, new_values = parse_result

    print('Tag to Change: ', tag)

    tag_info(mp3files, new_values, tag)

    if len(new_values) != len(mp3files):
        print('\nDIFFERENT NUMBERS: ', len(new_values), ' VALUES, ', len(mp3files), ' MP3s ', end='')
        choice = input('CONTINUE? (y/n) ')
        if choice.lower() != 'y':
            quit()

    choice = input('APPLY CHANGES? (y/n) ')
    if choice.lower() == 'y':
        apply_changes(mp3files, new_values, tag)
        tag_info(mp3files, new_values, tag)
        input('\nPRESS <ENTER> TO EXIT')
