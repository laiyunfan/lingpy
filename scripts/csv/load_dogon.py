import sys
from lingpy.basic import *

# relative or absolute paths must be given to the orthography profiles


# specify the column name-to-orthography profiles

d = {
"Sangha So (Moran, Sangha)":"../../lingpy/data/orthography_profiles/Moran2013.prf", 
"Ben Tey (Beni, JH)":"../../lingpy/data/orthography_profiles/Heath2013.prf",
"Toro Tegu (Toupere, JH)":"../../lingpy/data/orthography_profiles/Heath2013.prf",
"Bangime (Bounou, AH)":"../../lingpy/data/orthography_profiles/Heath2013.prf"
}

# load the spreadsheet, specify attributes like the black list file
s = Spreadsheet("dogon_wordlists_leipzig-jakarta.csv", meanings="Leipzig-Jakarta", skip_empty_concepts=False, cellsep="\\\\", blacklist="dogon.bl", profiles=d)


# s = Spreadsheet("/Users/stiv/Dropbox/Fieldwork/comparative_dogon/scripts/dogon_wordlists.csv", meanings="English")



# s = Spreadsheet("/Users/stiv/Dropbox/Fieldwork/comparative_dogon/scripts/test.csv", meanings="Leipzig-Jakarta", skip_empty_concepts=False, profiles=d)
# s = Spreadsheet("/Users/stiv/Dropbox/Fieldwork/comparative_dogon/scripts/test.csv", meanings="English", skip_empty_concepts=False, profiles=d, cellsep=",|\\") # , blacklist="dogon.bl")
# s = Spreadsheet("/Users/stiv/Dropbox/Fieldwork/comparative_dogon/parse_wordlists/testtest.csv", meanings="English", skip_empty_concepts=False, cellsep="\\\\", blacklist="dogon.bl", profiles=d)

# dogon_wordlists_basic.csv
# dogon_wordlists_leipzig-jakarta.csv
# dogon_wordlists_swadesh.csv


# s = Spreadsheet("../dogon_wordlists_leipzig-jakarta.csv", meanings="English", skip_empty_concepts=False, cellsep="\\\\", blacklist="dogon.bl", profiles=d)

wl = Wordlist(s)
wl.tokenize()

wl.output('qlc',filename='dogon-tokens')

# s = Spreadsheet("/Users/stiv/Dropbox/Fieldwork/comparative_dogon/scripts/test.csv", meanings="English")
# s.stats()
# analyses = s.analyze("graphemes")
# analyses = s.analyze("graphemes")
# analyses = s.analyze("words")
# s.pprint(analyses[0])

# s.pprint_matrix()
# s.transform(**d)