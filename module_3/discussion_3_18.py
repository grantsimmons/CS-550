# Author: Grant Simmons (gsimmons@stevens.edu)
# Course: CS-550-WS
# Professor: Edward Banduk
# I pledge my honor that I have abided by the Stevens Honor System.

# Please note: This is not meant to be good Python code; this was a quick exercise 
# meant to demonstrate the concepts outlined by the question below

###############################################################################
#18)  Write a program in your favorite language that will convert all ASCII uppercase and lowercase letters to EBCDIC code. 
# For an additional challenge, also convert the punctuation symbols, indicating with a failure-to-convert message, those symbols that are not represented in the EBCDIC system.
###############################################################################

# Example string
ascii_string = "Hello, EBCDIC world! I'm ASCII!"


###############################################################################
# Method 1: Using internal Python tools! (Very Easy)
###############################################################################

print(ascii_string.encode("cp037"))


###############################################################################
# Method 2: Directly map all hex values between ASCII and EBCDIC
###############################################################################

import codecs

# Here's a simple bidirectional dictionary for easy conversion both directions
class bidict(dict):
    # Object Source: https://stackoverflow.com/questions/3318625/how-to-implement-an-efficient-bidirectional-hash-table
    # Author: Basj (https://stackoverflow.com/users/1422096/basj)
    def __init__(self, *args, **kwargs):
        super(bidict, self).__init__(*args, **kwargs)
        self.inverse = {}
        for key, value in self.items():
            self.inverse.setdefault(value,[]).append(key) 

    def __setitem__(self, key, value):
        if key in self:
            self.inverse[self[key]].remove(key) 
        super(bidict, self).__setitem__(key, value)
        self.inverse.setdefault(value,[]).append(key)        

    def __delitem__(self, key):
        self.inverse.setdefault(self[key],[]).remove(key)
        if self[key] in self.inverse and not self.inverse[self[key]]: 
            del self.inverse[self[key]]
        super(bidict, self).__delitem__(key)

def generate_ascii(my_string):
    ascii_hex = []
    for char in my_string: #Iterate string characters
        #Encode as ASCII, extract bytes as hex, and convert
        ascii_char = codecs.encode(bytes(char, "ascii"), "hex")
        ascii_hex.append(ascii_char)
    return ascii_hex

def ascii_to_ebcdic(char_map, ascii_bytes):
    # Convert an ASCII string to EBCDIC-encoded byte array
    ebcdic_byte_arr = []
    for byte in ascii_bytes: #Iterate string characters
        #Encode as ASCII, extract bytes as hex, and convert
        ebcdic_byte = char_map[byte]
        if ebcdic_byte == b'3f' or ebcdic_byte == b'1a':
            print("Warning: failed to convert ASCII symbol: ", char)
            print("  Output string may contain unexpected characters")
        ebcdic_byte_arr.append(ebcdic_byte) #Append converted byte to return array
    return ebcdic_byte_arr

def generate_ebcdic(ebcdic_string):
    ebcdic_hex = []
    for char in ebcdic_string: #Iterate string characters
        #Encode as ASCII, extract bytes as hex, and convert
        ebcdic_char = codecs.encode(bytes(char, "cp500"), "hex")
        ebcdic_hex.append(ebcdic_char)
    return ebcdic_hex

def ebcdic_to_ascii(char_map, ebcdic_bytes):
    # Convert an EBCDIC string to ASCII-encoded byte array (Experimental, untested)
    ascii_byte_arr = []
    for byte in ebcdic_bytes:
        ascii_char = char_map.inverse[byte][0] #Grabbing first index because unpacking may throw error
        if byte == b'3f' or byte == b'1a':
            print("Warning: failed to convert EBCDIC symbol: ", char)
            print("  Output string may contain unexpected characters")
        ascii_byte_arr.append(ascii_char)
    return ascii_byte_arr

# ASCII-EBCDIC encoding map
# Source: https://www.ibm.com/support/knowledgecenter/SSZJPZ_11.7.0/com.ibm.swg.im.iis.ds.parjob.adref.doc/topics/r_deeadvrf_ASCII_to_EBCDIC.html
# Making bidirectional in the case that the user would want to conver EBCDIC to ASCII
ascii_ebcdic_map = bidict(
        {
        b'00': b'00', b'01': b'01', b'02': b'02', b'03': b'03', b'04': b'1a', b'05': b'09', b'06': b'1a', b'07': b'7f', b'08': b'1a', b'09': b'1a', b'0a': b'1a', b'0b': b'0b', b'0c': b'0c', b'0d': b'0d', b'0e': b'0e', b'0f': b'0f',
        b'10': b'10', b'11': b'11', b'12': b'12', b'13': b'13', b'14': b'3c', b'15': b'3d', b'16': b'32', b'17': b'26', b'18': b'18', b'19': b'19', b'1a': b'3f', b'1b': b'27', b'1c': b'1c', b'1d': b'1d', b'1e': b'1e', b'1f': b'1f',
        b'20': b'40', b'21': b'4f', b'22': b'7f', b'23': b'7b', b'24': b'5b', b'25': b'6c', b'26': b'50', b'27': b'7d', b'28': b'4d', b'29': b'5d', b'2a': b'5c', b'2b': b'4e', b'2c': b'6b', b'2d': b'60', b'2e': b'4b', b'2f': b'61',
        b'30': b'f0', b'31': b'f1', b'32': b'f2', b'33': b'f3', b'34': b'f4', b'35': b'f5', b'36': b'f6', b'37': b'f7', b'38': b'f8', b'39': b'f9', b'3a': b'7a', b'3b': b'5e', b'3c': b'4c', b'3d': b'7e', b'3e': b'6e', b'3f': b'6f',
        b'40': b'7c', b'41': b'c1', b'42': b'c2', b'43': b'c3', b'44': b'c4', b'45': b'c5', b'46': b'c6', b'47': b'c7', b'48': b'c8', b'49': b'c9', b'4a': b'd1', b'4b': b'd2', b'4c': b'd3', b'4d': b'd4', b'4e': b'd5', b'4f': b'd6',
        b'50': b'd7', b'51': b'd8', b'52': b'd9', b'53': b'e2', b'54': b'e3', b'55': b'e4', b'56': b'e5', b'57': b'e6', b'58': b'e7', b'59': b'e8', b'5a': b'e9', b'5b': b'4a', b'5c': b'e0', b'5d': b'5a', b'5e': b'5f', b'5f': b'6d',
        b'60': b'79', b'61': b'81', b'62': b'82', b'63': b'83', b'64': b'84', b'65': b'85', b'66': b'86', b'67': b'87', b'68': b'88', b'69': b'89', b'6a': b'91', b'6b': b'92', b'6c': b'93', b'6d': b'94', b'6e': b'95', b'6f': b'96',
        b'70': b'97', b'71': b'98', b'72': b'99', b'73': b'a2', b'74': b'a3', b'75': b'a4', b'76': b'a5', b'77': b'a6', b'78': b'a7', b'79': b'a8', b'7a': b'a9', b'7b': b'c0', b'7c': b'6a', b'7d': b'd0', b'7e': b'a1', b'7f': b'07',
        b'80': b'3f', b'81': b'3f', b'82': b'3f', b'83': b'3f', b'84': b'3f', b'85': b'3f', b'86': b'3f', b'87': b'3f', b'88': b'3f', b'89': b'3f', b'8a': b'3f', b'8b': b'3f', b'8c': b'3f', b'8d': b'3f', b'8e': b'3f', b'8f': b'3f',
        b'90': b'3f', b'91': b'3f', b'92': b'3f', b'93': b'3f', b'94': b'3f', b'95': b'3f', b'96': b'3f', b'97': b'3f', b'98': b'3f', b'99': b'3f', b'9a': b'3f', b'9b': b'3f', b'9c': b'3f', b'9d': b'3f', b'9e': b'3f', b'9f': b'3f',
        b'a0': b'3f', b'a1': b'3f', b'a2': b'3f', b'a3': b'3f', b'a4': b'3f', b'a5': b'3f', b'a6': b'3f', b'a7': b'3f', b'a8': b'3f', b'a9': b'3f', b'aa': b'3f', b'ab': b'3f', b'ac': b'3f', b'ad': b'3f', b'ae': b'3f', b'af': b'3f',
        b'b0': b'3f', b'b1': b'3f', b'b2': b'3f', b'b3': b'3f', b'b4': b'3f', b'b5': b'3f', b'b6': b'3f', b'b7': b'3f', b'b8': b'3f', b'b9': b'3f', b'ba': b'3f', b'bb': b'3f', b'bc': b'3f', b'bd': b'3f', b'be': b'3f', b'bf': b'3f',
        b'c0': b'3f', b'c1': b'3f', b'c2': b'3f', b'c3': b'3f', b'c4': b'3f', b'c5': b'3f', b'c6': b'3f', b'c7': b'3f', b'c8': b'3f', b'c9': b'3f', b'ca': b'3f', b'cb': b'3f', b'cc': b'3f', b'cd': b'3f', b'ce': b'3f', b'cf': b'3f',
        b'd0': b'3f', b'd1': b'3f', b'd2': b'3f', b'd3': b'3f', b'd4': b'3f', b'd5': b'3f', b'd6': b'3f', b'd7': b'3f', b'd8': b'3f', b'd9': b'3f', b'da': b'3f', b'db': b'3f', b'dc': b'3f', b'dd': b'3f', b'de': b'3f', b'df': b'3f',
        b'e0': b'3f', b'e1': b'3f', b'e2': b'3f', b'e3': b'3f', b'e4': b'3f', b'e5': b'3f', b'e6': b'3f', b'e7': b'3f', b'e8': b'3f', b'e9': b'3f', b'ea': b'3f', b'eb': b'3f', b'ec': b'3f', b'ed': b'3f', b'ee': b'3f', b'ef': b'3f',
        b'f0': b'3f', b'f1': b'3f', b'f2': b'3f', b'f3': b'3f', b'f4': b'3f', b'f5': b'3f', b'f6': b'3f', b'f7': b'3f', b'f8': b'3f', b'f9': b'3f', b'fa': b'3f', b'fb': b'3f', b'fc': b'3f', b'fd': b'3f', b'fe': b'3f', b'ff': b'3f'
        }
)

#Perform ASCII-EBCDIC conversion
ascii_string = "Hello, EBCDIC world! I'm ASCII!" #(Just as a reminder)
ascii_bytes = generate_ascii(ascii_string)
ebcdic_bytes = ascii_to_ebcdic(ascii_ebcdic_map, ascii_bytes)
print("Original string:\n", ascii_string)
print("ASCII bytes:\n", ascii_bytes)
print("Decoding with Python ascii for Sanity Check:")
print(codecs.decode(b''.join(ascii_bytes), "hex"))
print("EBCDIC bytes:\n", ebcdic_bytes)
print("Decoding with Python cp500 for Sanity Check:")
print(codecs.decode(b''.join(ebcdic_bytes), "hex").decode("cp500"))

#Go the other way! (Experimental, untested)
ebcdic_string = "Hello, ASCII world! I'm EBCDIC!"
ebcdic_bytes = generate_ebcdic(ebcdic_string)
ascii_bytes = ebcdic_to_ascii(ascii_ebcdic_map, ebcdic_bytes)
print("Original string:\n", ebcdic_string)
print("EBCDIC bytes:\n", ebcdic_bytes)
print("Decoding with Python cp500 for Sanity Check:")
print(codecs.decode(b''.join(ebcdic_bytes), "hex").decode("cp500"))
print("ASCII bytes:\n", ascii_bytes)
print("Decoding with Python ascii for Sanity Check:")
print(codecs.decode(b''.join(ascii_bytes), "hex"))
