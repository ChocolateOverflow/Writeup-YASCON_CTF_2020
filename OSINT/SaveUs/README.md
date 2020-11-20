#  SaveUs!!

250 points (Medium)
YAS community is trying very hard to make their CTF a big success, But DrNezooOlga from Siberia is planning to do something which can ruin their plans. Be a pro by finding the flag and save the CTF game
Author: Deric

---

Found DrNezooOlga's github profile with 2 repositories

```
https://github.com/DrNezooOlga
https://github.com/DrNezooOlga/You-found-Something
https://github.com/DrNezooOlga/Yet-Another_AttackPlan
```

Specifically, the repo `Yet-Another_AttackPlan` has the file [YetAnother.jpg](https://github.com/DrNezooOlga/Yet-Another_AttackPlan/blob/main/YetAnother.jpeg).

![](YetAnother.jpg)

Running `exiftool` on it:

```sh
$ exiftool YetAnother.jpeg
ExifTool Version Number         : 12.00
File Name                       : YetAnother.jpeg
Directory                       : .
File Size                       : 126 kB
File Modification Date/Time     : 2020:10:31 17:07:39+07:00
File Access Date/Time           : 2020:10:31 17:07:39+07:00
File Inode Change Date/Time     : 2020:10:31 17:07:39+07:00
File Permissions                : rw-r--r--
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
JFIF Version                    : 1.01
Exif Byte Order                 : Big-endian (Motorola, MM)
X Resolution                    : 1
Y Resolution                    : 1
Resolution Unit                 : None
Y Cb Cr Positioning             : Centered
Copyright                       : aNGC0YLQv9GBOi8v0LTRgNC40LLQtS7Qs9C+0L7Qs9C70LUuY9C+0Lwv0YTQuNC70LUv0LQvMVHQuzRIOdCh0KPQldCY0JjQkNChONGC0J3Qk1HQsNC+0LfRi9CT0LDQk9Cj0JzQvDc50JzQtdCgL9Cy0LjQtXc/0YPRgdC/PdGI0LDRgNC40L3Qsw==
Image Width                     : 1229
Image Height                    : 470
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:4:4 (1 1)
Image Size                      : 1229x470
Megapixels                      : 0.578
```

we found a long Copyright string which seems to be base64-encoded, so we decoded it

```sh
$ echo "aNGC0YLQv9GBOi8v0LTRgNC40LLQtS7Qs9C+0L7Qs9C70LUuY9C+0Lwv0YTQuNC70LUv0LQvMVHQuzRIOdCh0KPQldCY0JjQkNChONGC0J3Qk1HQsNC+0LfRi9CT0LDQk9Cj0JzQvDc50JzQtdCgL9Cy0LjQtXc/0YPRgdC/PdGI0LDRgNC40L3Qsw==" -n | base64 -d
hттпс://дриве.гоогле.cом/филе/д/1Qл4H9СУЕИИАС8тНГQаозыГаГУМм79МеР/виеw?усп=шаринг
```

The decoded output looks like some strange Russian, but looking at the characters, it looks like a URL, just with Russian for their English equivalents. I then used [Lexilogos](https://www.lexilogos.com/keyboard/russian_conversion.htm) to convert the Cyrillic characters to Latin.

```
https://drive.google.com/file/d/1Ql4H9SUEIIAS8tNGQaozyGaGUMm79MeR/view?usp=šaring
```

It's not the most complete conversion but navigating to the URL will show the image `YAS.jpeg`.

![](YAS.jpeg)

When we run `exiftool` on `YAS.jpeg`, we again get some long Copyright string

```sh
$ exiftool YAS.jpeg
ExifTool Version Number         : 12.00
File Name                       : YAS.jpeg
Directory                       : .
File Size                       : 73 kB
File Modification Date/Time     : 2020:10:31 17:29:40+07:00
File Access Date/Time           : 2020:10:31 17:29:40+07:00
File Inode Change Date/Time     : 2020:10:31 17:29:54+07:00
File Permissions                : rw-r--r--
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
JFIF Version                    : 1.01
Exif Byte Order                 : Big-endian (Motorola, MM)
X Resolution                    : 1
Y Resolution                    : 1
Resolution Unit                 : None
Y Cb Cr Positioning             : Centered
Copyright                       : ====AQUPQRUAXPFM72MEVQ5LV23SV5ZJP2QGVAFL
Image Width                     : 1080
Image Height                    : 1080
Encoding Process                : Progressive DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:2:0 (2 2)
Image Size                      : 1080x1080
Megapixels                      : 1.2
```

With the `=`s at the beginning, this looks like a string that's base64-encoded and reversed. However, this time, it's not base64-encoded, but base32-encoded, so we `rev` & `base32 -d`

```sh
$ echo -n "====AQUPQRUAXPFM72MEVQ5LV23SV5ZJP2QGVAFL" | rev | base32 -d
YASCON{YoU_aR3_a_pR0}
```

Which gives us our flag!
