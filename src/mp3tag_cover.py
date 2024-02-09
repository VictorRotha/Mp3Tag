import os
import mutagen as mut
from mutagen.id3 import ID3, APIC


def apply_cover(audio_files, cover):
    with open(cover, 'rb') as albumart:
        data = albumart.read()

    if cover.endswith('.png'):
        mime_type = 'image/png'
    else:
        mime_type = 'image/jpg'

    for f in audio_files:
        audio = mut.id3.ID3(f)
        audio.setall('APIC', [APIC(mime=mime_type,
                                   encoding=3,
                                   type=3,
                                   desc=u'desc',
                                   data=data)]
                     )

        audio.save()


if __name__ == '__main__':

    mp3directory = os.getcwd()

    print('Directory:', mp3directory)

    mp3files = [os.path.join(mp3directory, f) for f in os.listdir(mp3directory) if f.endswith(".mp3")]
    mp3files.sort()

    if len(mp3files) == 0:
        print('ERROR: no audiofiles found')
        quit(0)

    covers = [os.path.join(mp3directory, f) for f in os.listdir(mp3directory)
              if f.endswith(".jpg") or f.endswith(".png") or f.endswith(".jpeg")]

    if len(covers) == 0:
        print('ERROR: no cover found')
        quit(0)

    cover = covers[0]

    print("Cover ", cover)

    print(f'\nChange covers in {len(mp3files)} files. Old albumart will be overwritten!')
    choice = input('Apply? (y/n) ')
    if choice.lower() == 'y':
        apply_cover(mp3files, cover)
        input('\nPRESS <ENTER> TO EXIT')

    apply_cover(mp3files, cover)
