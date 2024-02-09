import  os
import mutagen as mut

def rename(preview_result):

    print()

    for file in preview_result:
        fn = preview_result[file]
        fn = os.path.join(os.path.split(file)[0], fn)

        os.rename(file, fn)
        print(fn)


def preview(audiofiles):
    result = {}
    for file in audiofiles:

        easy = mut.File(file, easy=True)

        try:
            artist = easy['artist'][0]
        except KeyError:
            artist = 'Unknown'
        try:
            album = easy['album'][0]
        except KeyError:
            album = ''
        try:
            title = easy['title'][0]
        except KeyError:
            title = ''
        try:
            tnr = easy['tracknumber'][0]
        except KeyError:
            tnr = ''

        ext = os.path.splitext(file)[1]
        old_fn = os.path.split(file)[1]

        fn = f'{artist} - {album} {tnr} - {title}{ext}'

        result[file] = fn

        print(f'{old_fn:<75}{fn}')

    return result


if __name__ == '__main__':

    mp3directory = os.getcwd()

    mp3files = [os.path.join(mp3directory, f) for f in os.listdir(mp3directory) if f.endswith(".mp3")]
    mp3files.sort()

    if len(mp3files) == 0:
        print('ERROR: no audiofiles found')
        quit(0)

    result = preview(mp3files)

    choice = input('\nAPPLY CHANGES? (y/n) ')
    if choice.lower() == 'y':
        rename(result)
        input('\nPRESS <ENTER> TO EXIT')




