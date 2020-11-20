# Among us

150 points (Easy)
identify the imposter among us
[Click Here](https://mega.nz/file/InhUnZZK#-qU3Xo38GwQCVLPY96mSJULg100iiTcyQpzBxNNLYns)
Author: Anil & Nizam

---

Download an `unzip among_us.zip` to get the directory `Challenge` with 99 PNG files.

Using `sxiv` to view a few images, the seem to all look the same, so I tried using `diff` on a couple of images.

```sh
$ diff 1.png 2.png
```

There's no output, meaning the 2 files are identical. This means all files but 1 are the same file. With that, I used a one-liner do `diff` everything.

```sh
$ for i in $(seq 1 998); do diff $i.png $((i+1)).png; done
Binary files 698.png and 699.png differ
Binary files 699.png and 700.png differ
```

The file `699.png` differs, so that's our imposter. Running `exiftool` shows a funny-looking Maker Note

```sh
$ exiftool 699.png
ExifTool Version Number         : 12.00
File Name                       : 699.png
Directory                       : .
File Size                       : 13 kB
File Modification Date/Time     : 2020:10:19 02:01:48+07:00
File Access Date/Time           : 2020:10:30 16:54:47+07:00
File Inode Change Date/Time     : 2020:10:31 14:16:47+07:00
File Permissions                : rw-r--r--
File Type                       : PNG
File Type Extension             : png
MIME Type                       : image/png
Image Width                     : 720
Image Height                    : 720
Bit Depth                       : 8
Color Type                      : RGB with Alpha
Compression                     : Deflate/Inflate
Filter                          : Adaptive
Interlace                       : Noninterlaced
Software                        : Adobe ImageReady
XMP Toolkit                     : Image::ExifTool 12.06
Maker Note                      : WUFTQ09Oe0xvMGshbmdfTTN0NF9EYVRhXyE1X0Z1Tn0=
Image Size                      : 720x720
Megapixels                      : 0.518
```

Which is base64-encoded, so...

```sh
$ echo 'WUFTQ09Oe0xvMGshbmdfTTN0NF9EYVRhXyE1X0Z1Tn0=' | base64 -d
YASCON{Lo0k!ng_M3t4_DaTa_!5_FuN}
```

and we've got the flag!
