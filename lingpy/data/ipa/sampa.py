import sys
import regex as re
# data for sampa2ipa (Peter Kleiwegs implementation)
xsdata = '''
#||----- CONSONANTS --------

#||| Plosive
p    p
b    b
t    t
d    d
t`   \u0288
d`   \u0256
c    c
J\\   \u025F
k    k
g    \u0261
q    q
G\\   \u0262
?    \u0294

#||| Nasal
m    m
F    \u0271
n    n
n`   \u0273
J    \u0272
N    \u014B
N\\   \u0274

#||| Trill
B\\   \u0299
r    r
R\\   \u0280

#||| Tap or flap
4    \u027E
r`   \u027D

#||| Fricative
p\\   \u0278
B    \u03B2
f    f
v    v
T    \u03B8
D    \u00F0
s    s
z    z
S    \u0283
Z    \u0292
s`   \u0282
z`   \u0290
C    \u00E7
j\\   \u029D
x    x
G    \u0263
X    \u03C7
R    \u0281
X\\   \u0127
?\\   \u0295
h    h
h\\   \u0266

#||| Lateral fricative
K    \u026C
K\\   \u026E

#||| Approximant
P    \u028B
v\\   \u028B
r\\   \u0279
r\\`  \u027B
j    j
M\\   \u0270

#||| Lateral approximant
l    l
l`   \u026D
L    \u028E
L\\   \u029F

#||----- CONSONANTS (NON-PULMONIC) --------

#||| Clicks
O\\[?] \u0298
|\\   \u01C0
!\\   \u01C3
=\\   \u01C2
|\\|\\ \u01C1

#||| Voiced implosives
b_<  \u0253
d_<  \u0257
J\\_<  \u0284
g_<  \u0260
G\\_<  \u029B

#||| Ejectives
_>   \u02BC

#||----- SUPRASEGMENTALS --------

"    \u02C8
%    \u02CC
:    \u02D0
:\\   \u02D1
_X   \u0306
.    .
|    \u01C0
||   \u01C1
-\\   \u035C

#||----- TONES & WORD ACCENTS

#||| Level
_T   \u02E5
_H   \u02E6
_M   \u02E7
_L   \u02E8
_B   \u02E9
!    \u2193
^    \u2191

#||| Contour
_R   /|[?]
_F   \\|[?]
<R>  \u2197
<F>  \u2198
->[?] \u2192

#||----- DIACRITICS --------

_0   \u0325
_v   \u032C
_h   \u02B0
_O   \u0339
_c   \u031C
_+   \u031F
_-   \u0320
_"   \u0308
_X[?] \u033D
_=   \u0329
_^   \u032F
`    \u02DE
_t   \u0324
_k   \u0330
_N   \u033C
_w[?]   \u02B7
\'   \u02B2
_j   \u02B2
_G   \u02E0
_?\\  \u02E4
_e   \u0334
5    \u026B
_r   \u031D
_o   \u031E
_A   \u0318
_q   \u0319
_d   \u032A
_a   \u033A
_m   \u033B
~    \u0303
_~   \u0303
_n   \u207F
_l   \u02E1
_}   \u031A

#||----- VOWELS --------

#||| Close
i    i
y    y
I    \u026A
Y    \u028F
1    \u0268
}    \u0289
U    \u028A
M    \u026F
u    u

#||| Close-mid
e    e
2    \u00F8
@\\   \u0258
@    \u0259
8    \u0275
7    \u0264
o    o

#||| Open-mid
E    \u025B
{    \u00E6
9    \u0153
3    \u025C
6    \u0250
3\\   \u025E
V    \u028C
O    \u0254

#||| Open
a    a
&    \u0276
A    \u0251
Q    \u0252

#||----- OTHER SYMBOLS --------

W    \u028D
w    \u028b
H    \u0265
H\\   \u029C
<\\   \u02A2
>\\   \u02A1
s\\   \u0255
z\\   \u0291
l\\   \u027A
x\\[?]  \u0267
k_p  k\u0361p
#t_s  t\u0361s
p_f  p\u0361f

dz   \u02A3
dZ   \u02A4
dz\\  \u02A5
ts   \u02A6
tS   \u02A7
tz\\  \u02A8
fN   \u02A9
ls   \u02AA
lz   \u02AB
ww[?] \u02AC
xx[?] \u02AD

#||------Special affricates------(added by JML)
t_s\   \u02a8
d_z\   \u02a5
t_S   ʧ
d_Z   ʤ   
d_z   ʣ
t_s   ʦ
,   \u0323
#||--specific character ';' for multiple entries-(added by JML)
;   ;
#||----- END --------
'''
"""
Data for L{xs2uni()<lingpy.entities.sequence.StrOps.xs2uni()>} an algorithm for the
conversion of XSAMPA to IPA (Unicode) by U{Peter 
Kleiweg<http://www.let.rug.nl/~kleiweg/L04/devel/python/xsampa.html>}.
@author: Peter Kleiweg
@date: 2007/07/19
"""
_xsKeys = [' ']
xs = {' ': ' '}
"""
The source-target dictionary for L{xs2uni()<lingpy.entities.sequence.StrOps.xs2uni()>} 
an algorithm for the conversion of XSAMPA to IPA (Unicode) by U{Peter 
Kleiweg<http://www.let.rug.nl/~kleiweg/L04/devel/python/xsampa.html>}.
@author: Peter Kleiweg
@date: 2007/07/19

"""
for _line in xsdata.split('\n'):
    _line = _line.strip()
    if not _line or _line[0] == '#':
        continue
    _key, _val = _line.split()
    try:
        assert _key not in xs 
    except:
        sys.stderr.write(_key + '\n')
        sys.stderr.flush()
        raise
    _xsKeys.append(_key)
    xs[_key] = _val;

_kk = []
for _k in _xsKeys:
    _kk.append(re.escape(_k))
_kk.sort(reverse = True)  # long before short
_xsPat = '|'.join(_kk)
reXS = re.compile('(' + _xsPat + ')|(.)')
"""
The regular expression used in the sampa2unicode-converter 
is taken from an
algorithm for the conversion of XSAMPA to IPA (Unicode) by Peter 
Kleiweg <http://www.let.rug.nl/~kleiweg/L04/devel/python/xsampa.html>.
@author: Peter Kleiweg
@date: 2007/07/19
"""
