# Tapita: a book cover generator

This is of very limited usefulness for the average person, but
if you have ever needed to generate book covers for a few 
thousand files out of book metadata, then this may be for you!

The image it generates has some colorful "art" thanks to dicebear.com
which, again, will not change unless you change the title or subtitle
of the book.

This is based off code from [Tenprintcover](https://github.com/mgiraldo/tenprintcover-py) 
although I don't think anything survives of the original code, which has been ported
to Pillow and de-c64-fied.

Example usage:

```sh
$ python -m tapita -t "Dunes" -s "Oh, worms!" -a "Frank Herbert (has no sons)" -o cover.jpg
```
Which produces this image:

![A book cover](https://i.imgur.com/UcjdkkN.jpg)

There are plentiful opportunities for customization, which I will
probably not do anything about.

TODO: packaging and such.
