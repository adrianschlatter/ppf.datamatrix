# Codecs

A datamatrix represents a text- or byte string. To do this, it first
encodes the string using one of several codepages. Its main codepage is
`datamatrix.ascii` (see below). This main codepage has special codes to
enable other codepages (`datamatrix.text`, `datamatrix.C40`, `datamatrix.X12`,
`datamatrix.edifact`, and `datamatrix.base256`). Each of these other
codepages provides a mechanism to return to the main codepage (but the
mechanism *differs* depending on the codepage!).

In principle, it is possible to mix and match multiple codepages to encode
a single message. `ppf.datamatrix` will encode the entire message in the
(sub-) codepage the users specifies.

The following information is mostly based on [Wikipedia's english article
on Data Matrix codes] [wiki_datamatrix].


## datamatrix.ascii

This is the main codepage. It always activate unless the codepage is
explicitly switched to something else. `datamatrix.ascii` provides special
codes to do this switching: See `E6`, `E7`, `EE`, `EF`, `F0` in the
table below. Note that the switched-to alphabet remains active until we
switch back to datamatrix.ascii (every sub-codepage has a mechanism to
achieve this).

`datamatrix.ascii` is able to encode the entire ASCII charset (hence the
name). It is *not* the same codepage as ASCII, though!


| code 	| meaning 	| code 	| meaning 	| code 	| meaning 	| code 	| meaning                              	|
|------	|---------	|------	|---------	|------	|---------	|------	|--------------------------------------	|
| 00   	| unused  	| 40   	| ?       	| 80   	| del     	| C0   	| 62                                   	|
| 01   	| NUL     	| 41   	| @       	| 81   	| EOM     	| C1   	| 63                                   	|
| 02   	| SOH     	| 42   	| A       	| 82   	| 00      	| C2   	| 64                                   	|
| 03   	| STX     	| 43   	| B       	| 83   	| 01      	| C3   	| 65                                   	|
| 04   	| ETX     	| 44   	| C       	| 84   	| 02      	| C4   	| 66                                   	|
| 05   	| EOT     	| 45   	| D       	| 85   	| 03      	| C5   	| 67                                   	|
| 06   	| ENQ     	| 46   	| E       	| 86   	| 04      	| C6   	| 68                                   	|
| 07   	| ACK     	| 47   	| F       	| 87   	| 05      	| C7   	| 69                                   	|
| 08   	| BEL     	| 48   	| G       	| 88   	| 06      	| C8   	| 70                                   	|
| 09   	| BS      	| 49   	| H       	| 89   	| 07      	| C9   	| 71                                   	|
| 0A   	| HT      	| 4A   	| I       	| 8A   	| 08      	| CA   	| 72                                   	|
| 0B   	| NL      	| 4B   	| J       	| 8B   	| 09      	| CB   	| 73                                   	|
| 0C   	| VT      	| 4C   	| K       	| 8C   	| 10      	| CC   	| 74                                   	|
| 0D   	| NP      	| 4D   	| L       	| 8D   	| 11      	| CD   	| 75                                   	|
| 0E   	| CR      	| 4E   	| M       	| 8E   	| 12      	| CE   	| 76                                   	|
| 0F   	| SOH     	| 4F   	| N       	| 8F   	| 13      	| CF   	| 77                                   	|
| 10   	| SI      	| 50   	| O       	| 90   	| 14      	| D0   	| 78                                   	|
| 11   	| DLE     	| 51   	| P       	| 91   	| 15      	| D1   	| 79                                   	|
| 12   	| DC1     	| 52   	| Q       	| 92   	| 16      	| D2   	| 80                                   	|
| 13   	| DC2     	| 53   	| R       	| 93   	| 17      	| D3   	| 81                                   	|
| 14   	| DC3     	| 54   	| S       	| 94   	| 18      	| D4   	| 82                                   	|
| 15   	| DC4     	| 55   	| T       	| 95   	| 19      	| D5   	| 83                                   	|
| 16   	| NAK     	| 56   	| U       	| 96   	| 20      	| D6   	| 84                                   	|
| 17   	| SYN     	| 57   	| V       	| 97   	| 21      	| D7   	| 85                                   	|
| 18   	| ETB     	| 58   	| W       	| 98   	| 22      	| D8   	| 86                                   	|
| 19   	| CAN     	| 59   	| X       	| 99   	| 23      	| D9   	| 87                                   	|
| 1A   	| EM      	| 5A   	| Y       	| 9A   	| 24      	| DA   	| 88                                   	|
| 1B   	| SUB     	| 5B   	| Z       	| 9B   	| 25      	| DB   	| 89                                   	|
| 1C   	| ESC     	| 5C   	| [       	| 9C   	| 26      	| DC   	| 90                                   	|
| 1D   	| FS      	| 5D   	| \       	| 9D   	| 27      	| DD   	| 91                                   	|
| 1E   	| GS      	| 5E   	| ]       	| 9E   	| 28      	| DE   	| 92                                   	|
| 1F   	| RS      	| 5F   	| ^       	| 9F   	| 29      	| DF   	| 93                                   	|
| 20   	| US      	| 60   	| _       	| A0   	| 30      	| E0   	| 94                                   	|
| 21   	| SP      	| 61   	| `       	| A1   	| 31      	| E1   	| 95                                   	|
| 22   	| !       	| 62   	| a       	| A2   	| 32      	| E2   	| 96                                   	|
| 23   	| "       	| 63   	| b       	| A3   	| 33      	| E3   	| 97                                   	|
| 24   	| #       	| 64   	| c       	| A4   	| 34      	| E4   	| 98                                   	|
| 25   	| $       	| 65   	| d       	| A5   	| 35      	| E5   	| 99                                   	|
| 26   	| %       	| 66   	| e       	| A6   	| 36      	| E6   	| switch to C40                        	|
| 27   	| &       	| 67   	| f       	| A7   	| 37      	| E7   	| switch to BASE256                    	|
| 28   	| '       	| 68   	| g       	| A8   	| 38      	| E8   	| FNC1                                 	|
| 29   	| (       	| 69   	| h       	| A9   	| 39      	| E9   	| structured append                    	|
| 2A   	| )       	| 6A   	| i       	| AA   	| 40      	| EA   	| reader programming                   	|
| 2B   	| *       	| 6B   	| j       	| AB   	| 41      	| EB   	| set high bit of following char       	|
| 2C   	| +       	| 6C   	| k       	| AC   	| 42      	| EC   	| 05 macro                             	|
| 2D   	| ,       	| 6D   	| l       	| AD   	| 43      	| ED   	| 06 macro                             	|
| 2E   	| -       	| 6E   	| m       	| AE   	| 44      	| EE   	| switch to X12                        	|
| 2F   	| .       	| 6F   	| n       	| AF   	| 45      	| EF   	| switch to TEXT                       	|
| 30   	| /       	| 70   	| o       	| B0   	| 46      	| F0   	| switch to EDIFACT                    	|
| 31   	| 0       	| 71   	| p       	| B1   	| 47      	| F1   	| extended channel interpretation code 	|
| 32   	| 1       	| 72   	| q       	| B2   	| 48      	| F2   	| unused                               	|
| 33   	| 2       	| 73   	| r       	| B3   	| 49      	| F3   	| unused                               	|
| 34   	| 3       	| 74   	| s       	| B4   	| 50      	| F4   	| unused                               	|
| 35   	| 4       	| 75   	| t       	| B5   	| 51      	| F5   	| unused                               	|
| 36   	| 5       	| 76   	| u       	| B6   	| 52      	| F6   	| unused                               	|
| 37   	| 6       	| 77   	| v       	| B7   	| 53      	| F7   	| unused                               	|
| 38   	| 7       	| 78   	| w       	| B8   	| 54      	| F8   	| unused                               	|
| 39   	| 8       	| 79   	| x       	| B9   	| 55      	| F9   	| unused                               	|
| 3A   	| 9       	| 7A   	| y       	| BA   	| 56      	| FA   	| unused                               	|
| 3B   	| :       	| 7B   	| z       	| BB   	| 57      	| FB   	| unused                               	|
| 3C   	| ;       	| 7C   	| {       	| BC   	| 58      	| FC   	| unused                               	|
| 3D   	| <       	| 7D   	| \|      	| BD   	| 59      	| FD   	| unused                               	|
| 3E   	| =       	| 7E   	| }       	| BE   	| 60      	| FE   	| unused                               	|
| 3F   	| >       	| 7F   	| ~       	| BF   	| 61      	| FF   	| unused                               	|


## datamatrix.C40

C40 is optimized for strings of numbers and capital letters with
occasional special characters.

The C40 (sub-) codepage has multiple (sub-) sub-codepages called sets 1 to 3.
To enable a sub-sub-codepage, set 0 provides switching codes (see `00` to `02`
in the table below). The sub-sub-codepage remains active for *a* *single*
*code* following the switching code. Afterwards, set 0 is active again.

After translating each input character into one or two codes according to
the codepage, the result is packed. 'Packing' means combining three
consecutive codes into one word of two bytes. The formula to do this is:

```
value    = code1 * 1600 + code2 * 40 + code3 + 1
highbyte = value // 256
lowbyte  = value % 256
word     = [highbyte, lowbyte]
```

Now, the largest word we can obtain given the largest code of 0x27
is 0xFA00. Datamatrix uses one of the unused highbytes (0xFE) as the
'Return to ASCII' indicator (RTA).

_Note 1_: The C40 codepage below does *not* specify an RTA code. The RTA
        indicator is a *word* not a *code*.

_Note 2_: The RTA indicator is actually *half* a word. When we find a highbyte
        of 0xFE in the packed data, we switch back to `datamatrix.ascii`
        immediately (there will be no lowbyte after the RTA highbyte).


| code 	| set 0           	| set 1 	| set 2 	| set 3 	|
|------	|-----------------	|-------	|-------	|-------	|
| 00   	| switch to set 1 	| NUL   	| !     	| `     	|
| 01   	| switch to set 2 	| SOH   	| "     	| a     	|
| 02   	| switch to set 3 	| STX   	| #     	| b     	|
| 03   	| SP              	| ETX   	| $     	| c     	|
| 04   	| 0               	| EOT   	| %     	| d     	|
| 05   	| 1               	| ENQ   	| &     	| e     	|
| 06   	| 2               	| ACK   	| '     	| f     	|
| 07   	| 3               	| BEL   	| (     	| g     	|
| 08   	| 4               	| BS    	| )     	| h     	|
| 09   	| 5               	| HT    	| *     	| i     	|
| 0A   	| 6               	| LF    	| +     	| j     	|
| 0B   	| 7               	| VT    	| ,     	| k     	|
| 0C   	| 8               	| FF    	| –     	| l     	|
| 0D   	| 9               	| CR    	| .     	| m     	|
| 0E   	| A               	| SO    	| /     	| n     	|
| 0F   	| B               	| SI    	| :     	| o     	|
| 10   	| C               	| DLE   	| ;     	| p     	|
| 11   	| D               	| DC1   	| <     	| q     	|
| 12   	| E               	| DC2   	| =     	| r     	|
| 13   	| F               	| DC3   	| >     	| s     	|
| 14   	| G               	| DC4   	| ?     	| t     	|
| 15   	| H               	| NAK   	| @     	| u     	|
| 16   	| I               	| SYN   	| [     	| v     	|
| 17   	| J               	| ETB   	| \     	| w     	|
| 18   	| K               	| CAN   	| ]     	| x     	|
| 19   	| L               	| EM    	| ^     	| y     	|
| 1A   	| M               	| SUB   	| _     	| z     	|
| 1B   	| N               	| ESC   	| FNC1  	| {     	|
| 1C   	| O               	| FS    	|       	| \|    	|
| 1D   	| P               	| GS    	|       	| }     	|
| 1E   	| Q               	| RS    	| hibit 	| ~     	|
| 1F   	| R               	| US    	|       	| DEL   	|
| 20   	| S               	|       	|       	|       	|
| 21   	| T               	|       	|       	|       	|
| 22   	| U               	|       	|       	|       	|
| 23   	| V               	|       	|       	|       	|
| 24   	| W               	|       	|       	|       	|
| 25   	| X               	|       	|       	|       	|
| 26   	| Y               	|       	|       	|       	|
| 27   	| Z               	|       	|       	|       	|


## datamatrix.text

TEXT is optimized for strings of numbers and lowercase letters with
occasional special characters.

Similar to datamatrix.C40, it has multiple sub-sub-codepages. Also,
it uses the same word-packing math and the same mechanism to return
to the `datamatrix.ascii` codepage.


| code 	| set 0           	| set 1 	| set 2 	| set 3 	|
|------	|-----------------	|-------	|-------	|-------	|
| 00   	| switch to set 1 	| NUL   	| !     	| `     	|
| 01   	| switch to set 2 	| SOH   	| "     	| A     	|
| 02   	| switch to set 3 	| STX   	| #     	| B     	|
| 03   	| SP              	| ETX   	| $     	| C     	|
| 04   	| 0               	| EOT   	| %     	| D     	|
| 05   	| 1               	| ENQ   	| &     	| E     	|
| 06   	| 2               	| ACK   	| '     	| F     	|
| 07   	| 3               	| BEL   	| (     	| G     	|
| 08   	| 4               	| BS    	| )     	| H     	|
| 09   	| 5               	| HT    	| *     	| I     	|
| 0A   	| 6               	| LF    	| +     	| J     	|
| 0B   	| 7               	| VT    	| ,     	| K     	|
| 0C   	| 8               	| FF    	| –     	| L     	|
| 0D   	| 9               	| CR    	| .     	| M     	|
| 0E   	| a               	| SO    	| /     	| N     	|
| 0F   	| b               	| SI    	| :     	| O     	|
| 10   	| c               	| DLE   	| ;     	| P     	|
| 11   	| d               	| DC1   	| <     	| Q     	|
| 12   	| e               	| DC2   	| =     	| R     	|
| 13   	| f               	| DC3   	| >     	| S     	|
| 14   	| g               	| DC4   	| ?     	| T     	|
| 15   	| h               	| NAK   	| @     	| U     	|
| 16   	| i               	| SYN   	| [     	| V     	|
| 17   	| j               	| ETB   	| \     	| W     	|
| 18   	| k               	| CAN   	| ]     	| X     	|
| 19   	| l               	| EM    	| ^     	| Y     	|
| 1A   	| m               	| SUB   	| _     	| Z     	|
| 1B   	| n               	| ESC   	| FNC1  	| {     	|
| 1C   	| o               	| FS    	|       	| \|    	|
| 1D   	| p               	| GS    	|       	| }     	|
| 1E   	| q               	| RS    	| hibit 	| ~     	|
| 1F   	| r               	| US    	|       	| DEL   	|
| 20   	| s               	|       	|       	|       	|
| 21   	| t               	|       	|       	|       	|
| 22   	| u               	|       	|       	|       	|
| 23   	| v               	|       	|       	|       	|
| 24   	| w               	|       	|       	|       	|
| 25   	| x               	|       	|       	|       	|
| 26   	| y               	|       	|       	|       	|
| 27   	| z               	|       	|       	|       	|


## datamatrix.X12

`datamatrix.X12` is optimized for string consisting of numbers, capital
letters, CR, '*', '>', and ' '. It cannot encode other characters at all.

While `datamatrix.X12` again uses the same word-packing math and the same
return-to-ascii mechanism as `datamatrix.C40` and `datamatrix.text` above,
it does not have sub-sub-codepages (and therefore no set-switching codes).

The latter makes a difference during decoding as we do not have to account
for multi-byte codes.


| code 	| meaning 	| code 	| meaning 	| 
|------	|---------	|------	|---------	|
| 00   	| CR      	| 14   	| G       	|
| 01   	| *       	| 15   	| H       	|
| 02   	| >       	| 16   	| I       	|
| 03   	| SP      	| 17   	| J       	|
| 04   	| 0       	| 18   	| K       	|
| 05   	| 1       	| 19   	| L       	|
| 06   	| 2       	| 1A   	| M       	|
| 07   	| 3       	| 1B   	| N       	|
| 08   	| 4       	| 1C   	| O       	|
| 09   	| 5       	| 1D   	| P       	|
| 0A   	| 6       	| 1E   	| Q       	|
| 0B   	| 7       	| 1F   	| R       	|
| 0C   	| 8       	| 20   	| S       	|
| 0D   	| 9       	| 21   	| T       	|
| 0E   	| A       	| 22   	| U       	|
| 0F   	| B       	| 23   	| V       	|
| 10   	| C       	| 24   	| W       	|
| 11   	| D       	| 25   	| X       	|
| 12   	| E       	| 26   	| Y       	|
| 13   	| F       	| 27   	| Z       	|


## datamatrix.edifact

`datamatrix.edifact` is optimized for strings consisting of numbers,
capital letters, and set of typical special characters used in text
messages.

`datamatrix.edifact` employs word-packing after translating each character
into a code. It is not the same method as in `datamatrix.C40`,
`datamatrix.text`, and `datamatrix.X12`, though. Instead, it packs four 6-bit
codes into one 24-bit word (3 bytes).

The return-to-ascii mechanism is different as well. In fact, it is simpler:
It simply provides an RTA ("Return To Ascii") code in its codepage.


| code 	| meaning 	| code 	| meaning 	|
|------	|---------	|------	|---------	|
| 00   	| @       	| 20   	| SP      	|
| 01   	| A       	| 21   	| !       	|
| 02   	| B       	| 22   	| "       	|
| 03   	| C       	| 23   	| #       	|
| 04   	| D       	| 24   	| $       	|
| 05   	| E       	| 25   	| %       	|
| 06   	| F       	| 26   	| &       	|
| 07   	| G       	| 27   	| '       	|
| 08   	| H       	| 28   	| (       	|
| 09   	| I       	| 29   	| )       	|
| 0A   	| J       	| 2A   	| *       	|
| 0B   	| K       	| 2B   	| +       	|
| 0C   	| L       	| 2C   	| ,       	|
| 0D   	| M       	| 2D   	| –       	|
| 0E   	| N       	| 2E   	| .       	|
| 0F   	| O       	| 2F   	| /       	|
| 10   	| P       	| 30   	| 0       	|
| 11   	| Q       	| 31   	| 1       	|
| 12   	| R       	| 32   	| 2       	|
| 13   	| S       	| 33   	| 3       	|
| 14   	| T       	| 34   	| 4       	|
| 15   	| U       	| 35   	| 5       	|
| 16   	| V       	| 36   	| 6       	|
| 17   	| W       	| 37   	| 7       	|
| 18   	| X       	| 38   	| 8       	|
| 19   	| Y       	| 39   	| 9       	|
| 1A   	| Z       	| 3A   	| :       	|
| 1B   	| [       	| 3B   	| ;       	|
| 1C   	| \       	| 3C   	| <       	|
| 1D   	| ]       	| 3D   	| =       	|
| 1E   	| ^       	| 3E   	| >       	|
| 1F   	| RTA     	| 3F   	| ?       	|


## datamatrix.base256

`datamatrix.base256` encodes _byte_ strings, not _text_ strings.

In BASE256 mode you first declare the length of data bytes you want to encode.
After this number of bytes, we automatically return to ASCII mode. A length
of 1 to 249 is encoded as a single byte. Longer lengths are stored as two bytes:

```
L1 = (length // 250) + 249
L2 = length % 250
```

To avoid long sequences of zeroes in the encoded data (diffult for scanners
to read without losing synchronization), the length- and data bytes are
randomized by adding pseudo-random values `R(n)`, where `n` is the position
in the byte stream:

```
R(n) = (149 * n) % 255 + 1
```


## References

[wiki_datamatrix]: https://en.m.wikipedia.org/wiki/Data_Matrix

