# Mp3Tag 

### Features:

    - edit, delete mp3 tags
    - generate tracknumbers
    - set albumart
    - generate filenames from tags

### General usage

    1. Copy the script you want to use into the folder with your mp3 files.
    2. Depending on the script, create and edit a config file (see below).
    3. Start the script

### mp3tag.py

Main script to edit your files.

Config File:

- lines starting with # and empty lines will be ignored
- Run script with default config file
  `python3 mp3tag.py`

- Run script with another config file
`python3 mp3tag.py otherconfig.txt`

#### Generate tracknumbers

`tracks=true`

Files are numbered in ascending order as double digit number, starting with 01.


#### Albumart

`cover=true`

Copy your albumart(.jpg. .jpeg or .png) in your folder.
If there are more than on possible images, mp3tag uses the first one it finds.

#### Rename files

`rename=true`

Files will be renamed with below patter:

artist - album tracknumber - title.mp3

#### Tags

Lines beginning with 'tag=' indicate the audio tag to be changed, the following lines indicate the values to be set.
If no value is provided, the tag is deleted.
If only one value is set, the tag is changed in all files.


```
tag=mytag
value 1
value 2
...
```

example mp3config.txt:

```txt
# set tracknumbers
tracknumbers=true

# do not change the frontcover
cover=false

# do not rename files
#rename = true

# set tag artist to 'some artist' in all files
tag=artist
some artist

# delete tag albumartist in all files
tag=albumartist

# set title tag for the first 5 files
tag=title
title_1
title_2
title_3
title_4
title_5

```


### mp3tag_simple.py

Changes only one audiotag.

Config file:

- have to be 'audiotags.txt'
- first line is the tag to change, next line are the values
- if no value is provided, the tag is deleted in all files, if only one value is set, the tag is changed in all files.

delete date
```
date
```
change albumartist in all files
```
albumartist
Various
```
change title individually
```
title
title_1
title_2
title_3
```

### mp3tag_tracks.py

- No config file needed
- Files are numbered in ascending order as double digit number, starting with 01.


### mp3_cover.py

- No config file needed
- Copy your albumart(.jpg. .jpeg or .png) in your folder.
- If there are more than on possible images, mp3tag uses the first one it finds.


### mp3tag_rename.py

- No config file needed
- Files will be renamed with this pattern: 'artist - album tracknumber - title.mp3'







    
   
    