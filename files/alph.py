
class Alphabet:
    alphabet = ['a', 'á', 'ä', 'b', 'c', 'č', 'd', 'ď', 'e', 'é', 'f', 'g', 'h', 'i', 'í', 'j', 'k', 'l', 'ľ', 'ĺ', 'm',
                'n', 'ň', 'o', 'ó', 'ô', 'p', 'q', 'r', 'ŕ', 's', 'š', 't', 'ť', 'u', 'ú', 'v', 'w', 'x', 'y', 'ý', 'z',
                'ž', '.', ',', '?', '!']
    length = len(alphabet)

    def __init__(self):
        self.len = Alphabet.length

    # metóoda mi vráti index znaku v poli-alphabet
    def getIndex(self, c):
        for i in range(len(self.alphabet)):
            if self.alphabet[i] == c:
                return i

    # mmetóda getChar vracia znak z alphabet na danom indexe p
    def getChar(self, p):
        return self.alphabet[p]





