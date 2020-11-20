# Infamous culprit

150 points (Easy)
A secret report about an infamous culprit's burrow with a secret driver made the cops to encircle him in his lodge. But the culprit with his defty driving tricks tried to dash away from their hands. After a car chase with all the adrenaline rush, the adept cops hooked him. But, by then the culprit had managed to burn away the drive of confidential files. An expert forensic scientist helped the cops to retrieve the memory, can you help them to open it?
[Click Here](https://mega.nz/file/ADhR0YBJ#mAgBHCzUYWhQDMpS8s64LOdnl8RsMdPmHsiCRCmZ-NA)
Author: Shahul

---

Work in Progress

First, download the file [Linux.zip](https://mega.nz/file/ADhR0YBJ#mAgBHCzUYWhQDMpS8s64LOdnl8RsMdPmHsiCRCmZ-NA) and `unzip` it.

```sh
$ unzip Linux.zip
Archive:  Linux.zip
  inflating: Linux.mem
 extracting: lubuntu-4.15.0-20-generic.zip
```

then `unzip` the new `lubuntu-4.15.0-20-generic.zip`

```sh
$ unzip lubuntu-4.15.0-20-generic.zip
Archive:  lubuntu-4.15.0-20-generic.zip
  inflating: volatility/tools/linux/module.dwarf
  inflating: boot/System.map-4.15.0-20-generic
```

Clearly we need to use `volatility`, but I'm not exactly good at it, so I'll walk you through my learning process.

First, we need a profile...

```sh
$ volatility -f Linux.mem imageinfo
Volatility Foundation Volatility Framework 2.6.1
INFO    : volatility.debug    : Determining profile based on KDBG search...
          Suggested Profile(s) : No suggestion (Instantiated with no profile)
                     AS Layer1 : LimeAddressSpace (Unnamed AS)
                     AS Layer2 : FileAddressSpace (/path/Writeup-YASCON_CTF_2020/Forensic/Infamous_culprit/Linux.mem)
                      PAE type : No PAE
```

No suggested profile...
