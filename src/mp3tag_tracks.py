import os
import mutagen as mut


def apply_track_numbers(audiofiles):
    for n, f in enumerate(audiofiles):

        easy = mut.File(f, easy=True)

        number = f'{str(n+1):0>2}'

        try:
            easy['tracknumber'] = number
        except KeyError:
            print('ERROR: track ', n)

        easy.save()


def show_preview(audiofiles):

    print(f'\n{"FILENAME":<70}'
          f'{"OLD TRACKNUMBER":<20}'
          f'{"NEW TRACKNUMBER":<20}'
          )

    for n, f in enumerate(audiofiles):
        filename = os.path.split(f)[1]

        number = f'{str(n+1):0>2}'
        easy = mut.File(f, easy=True)
        try:
            old_trn = easy['tracknumber'][0]
        except KeyError:
            old_trn = 'N/A'

        print(f'{filename:<70}'
              f'{old_trn:<20}'
              f'{number:<20}'
              )


if __name__ == '__main__':

    mp3directory = os.getcwd()

    print('Directory:', mp3directory)

    a = os.path.join(mp3directory, 'f')

    mp3files = [os.path.join(mp3directory, f) for f in os.listdir(mp3directory) if f.endswith(".mp3")]
    mp3files.sort()

    if len(mp3files) == 0:
        print('ERROR: no audiofiles found')
        quit(0)

    show_preview(mp3files)

    choice = input('\nAPPLY CHANGES? (y/n) ')
    if choice.lower() == 'y':
        apply_track_numbers(mp3files)
        show_preview(mp3files)
        input('\nPRESS <ENTER> TO EXIT')
