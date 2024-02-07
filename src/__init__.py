import os


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


def get_target_files(directory):

    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.mp3')]
    return files.sort()

    # mp3files = [f for f in allfiles if os.path.exists(f) and os.path.splitext(f)[1] == '.mp3']


#     new_tags = f.read().strip().split('\n')
#
# allfiles = [os.path.join(mp3directory, f) for f in os.listdir(mp3directory)]
# mp3files = [f for f in allfiles if os.path.exists(f) and os.path.splitext(f)[1] == '.mp3']
# tag = 'title'
# if new_tags[0] in ('title', 'album', 'artist'):
#     tag = new_tags.pop(0)


if __name__ == '__main__':

    directory = os.getcwd()
    tagfile = 'tagssample.txt'
    tagfile = os.path.join(os.getcwd(), tagfile)

    if not os.path.exists(tagfile):
        print('ERROR: ', tagfile, "doesn't exist!")
        quit(0)

    result = parse_tagfile(tagfile)
    print(result[0], "    ", result[1])

    get_target_files(directory)
