import tkinter as tk
import tkinter.scrolledtext as text
import tkinter.messagebox as Mbox
from tkinter import *
from tkinter import filedialog
import numpy as np
from decimal import Decimal, ROUND_HALF_UP

from files.alph import Alphabet as alphabet
from files.modularInverse import ModularInverse

class Application(alphabet):
    # vvzkreslenie plochy so vsetkými objektmi
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Hillov kryptosystém')

        width = 850
        height = 650
        self.window.resizable(width=FALSE, height=FALSE)
        self.window.geometry("%dx%d+0+0" % (width, height))
        self.window.configure(background='lightgray')

        self.label = tk.Label(self.window, text='Zvoľ rozmer matice', bg='lightgray')
        self.label.grid(column=0, columnspan=2, sticky=W, padx=10)

        self.size = Spinbox(self.window, from_=2, to=5, width=3, state='readonly')
        self.size.grid(row=0, column=1)

        self.textMatrix = tk.Label(self.window, text='Kľúčová matica', bg='lightgray',
                                   height=10, compound=RIGHT)

        self.textMatrix.grid(row=0, column=5, columnspan=4)

        gener = tk.Button(self.window, text='Generuj', command=self.wait, bg='white', relief=RIDGE, width=17,
                          overrelief=SUNKEN)
        gener.grid(row=0, column=2)
        self.can = False

        load = tk.Button(self.window, text='Načítaj súbor', command=self.load, bg='white', relief=RIDGE, width=15,
                         overrelief=SUNKEN)
        load.grid(row=1, column=0, sticky=E+W)

        encrypt = tk.Button(self.window, text='Šifruj', command=self.encrypt, bg='white', relief=RIDGE, width=10,
                            overrelief=SUNKEN)
        encrypt.grid(row=1, column=2, sticky=E)
        self.enc = False

        decrypt = tk.Button(self.window, text='Dešifruj', command=self.decrypt, bg='white', relief=RIDGE, width=10,
                            overrelief=SUNKEN)
        decrypt.grid(row=1, column=3, sticky=E)

        delete = tk.Button(self.window, text='Zmaž', command=self.delete, bg='white', relief=RIDGE, width=10,
                            overrelief=SUNKEN)
        delete.grid(row=1, column=9, sticky=E+W)

        save = tk.Button(self.window, text='Ulož', command=self.save, bg='white', relief=RIDGE, width=10,
                         overrelief=SUNKEN)
        save.grid(row=1, column=10, sticky=E+W, padx=1)

        self.block1 = text.ScrolledText(self.window, width=50, heigh=29, wrap=WORD)
        self.block1.grid(row=2, column=0, columnspan=6)

        self.block2 = text.ScrolledText(self.window, width=51, heigh=29, wrap=WORD)
        self.block2.config(state='disabled')
        self.block2.grid(row=2, column=6,  columnspan=5)


    # načítanie súboru pomocou dialogového okna, chybové správy pri zlých vstupoch
    def load(self):
        file_path = filedialog.askopenfilename()
        if file_path and file_path.lower().endswith('.txt'):
            self.setLeft(file_path)
        elif file_path is '':
            Mbox.showinfo('Info', 'Zvoľte si nejaký súbor.txt alebo \n napíšte vlastný text.')
        else:

            Mbox.showwarning('Chyba', 'Zlý typ súboru, zvoľte si súbor.txt')

    # načíta textový súbor a vypíše ho do self.block1
    def setLeft(self, file):
        self.block1.delete('1.0', END)
        with open(file,  errors='ignore') as f:
            text = f.read()
        self.block1.insert(INSERT, text)

    # načíta textový súbor a vypíše ho do self.block2
    def setRight(self, text):
        self.block2.configure(state='normal')
        self.block2.delete('1.0', END)
        self.block2.insert(INSERT, text)
        self.block2.configure(state='disabled')


    def delete(self):
        self.block1.delete('1.0', END)
        self.block2.configure(state='normal')
        self.block2.delete('1.0', END)
        self.block2.configure(state='disabled')

    # vracia text zo self.block1
    def getLeft(self):
        textLeft = self.block1.get('1.0', END+'-1c')
        return textLeft

    # vracia text zo self.block2
    def getRight(self):
        textRight = self.block2.get('1.0', END + '-1c')
        return textRight

    # vráti determinant matice zaokrúhlený na 1 desatinné miesto
    def getDeterminant(self, array):
        return round(np.asscalar((np.linalg.det(array))), 1)

    # zabezpečuje spustenie generovania
    def wait(self):
        if int(self.size.get())==5:
            self.textMatrix.config(text=str('Počkajte prosím, \n generujem správny kĺúč.'))

        self.window.config(cursor="wait")
        self.window.update()
        self.gener()
        self.window.config(cursor="")

    #generovanie a samotná kontrola správnosti kľúčovej matice
    def gener(self):
        self.can = True
        self.enc = False
        length = alphabet.length

        self.key = self.generKey()[0]
        self.sizeMatrix = self.generKey()[1]

        determinant = self.getDeterminant(self.key)
        if determinant == 0:
            self.textMatrix.config(text=str('Počkajte prosím, \n generujem správny kĺúč.'))
            self.wait()

        # modularny inverz matice(kluc) podla vzorca >> A^-1(mod n) = (det(A)^-1(mod n))*(det(A)A^-1)
        self.m = ModularInverse(self.key, length)

        if self.m.getResult() is None:
            self.textMatrix.config(text=str('Počkajte prosím, \n generujem správny kĺúč.'))
            self.wait()
        self.modular = self.m.getResult()
        self.textMatrix.config(text=str(self.key))

    # generuje cisla v matici mensie ako velkost abecedy-1
    def generKey(self):
        size = int(self.size.get())
        array = np.random.choice([x for x in range(0, alphabet.length-1)], size * size)
        array.resize(size, size)
        return array, size

    # násobenie vektorov pôvodného textu s kľúčom
    def multiple(self):
        wordIndexes = self.getindexes()
        size = self.sizeMatrix

        string = []
        self.tmpSize = 0

        for i in range(0, len(wordIndexes), size):
            if (len(wordIndexes[i:])) < size:
                self.tmpSize = size-len(wordIndexes[i:])

                for j in range(self.tmpSize):
                    wordIndexes.append(alphabet.getIndex(self, 'o'))

            tmp = []
            for k in range(i, i+size):
                tmp.append(wordIndexes[k])

            result = np.matmul(tmp, self.key)
            newRes = []
            for n in result:
                newRes.append(self.m.remake(n))
            for s in self.returnCipher(newRes):
                string.append(s)
        for o in self.others:
            if o[0] != ' ':
                string.insert(o[1], o[0])
        output = ''.join(string)
        return output

    # z vektora čísel spätne urobí text
    def returnCipher(self, vector):
        result = ""
        for i in vector:
            result += str(alphabet.getChar(self, self.m.remake(i)))
        return result

    # vracia pole s indexami veľkýc znakov v pôvodnom texte
    def upperIndex(self, text):
        upperSign = []
        for i in range(len(text)):
            if text[i].isupper():
                upperSign.append(i)
        return upperSign

    # pamätá si indexy neznámych znakov a pole pretvoreného textu na indexy
    def getindexes(self):
        text = self.getLeft()
        self.upper = self.upperIndex(text)
        text =text.lower()

        chars = []
        self.others = []
        for i in range(len(text)):
            if text[i] not in alphabet.alphabet:
                self.others.append((text[i], i))
            else:
                chars.append(alphabet.getIndex(a, text[i].lower()))
        return chars

    # ošetrenie zlých vtupných textov, výsledok šifrovania
    def encrypt(self):

        txt = self.getLeft()
        if self.can is False:
            Mbox.showwarning('Chyba', 'Najskôr generujte kľúčovú maticu.')
            return

        if len(txt) < 2:
            Mbox.showwarning('Chyba', 'Zadaj dlhší text, musí mať aspoň 2 znaky.')
            self.text = ''
            return



        self.text = self.multiple()
        self.setRight(self.text)
        self.enc = True

    #vráti indexy šifrovanéh textu, pamäatá si aj pozície neznámych znakov
    def getNewIndexes(self):
        if self.enc is False:
            self.text = ''
            return self.text
        text = self.text

        chars = []
        others = []
        for i in range(len(text)):
            if text[i] not in alphabet.alphabet:
                others.append((text[i], i))
            else:
                chars.append(alphabet.getIndex(self, text[i]))
        return chars

    #ošetrenie chybných postupov, dešifrovanie šifrovaného textu
    def decrypt(self):
        indexes = self.getNewIndexes()
        if indexes == '' or self.getLeft() == '':
            Mbox.showinfo('Chyba', 'Najskôr zašifruj maticou nejaký text')
            return

        if self.enc is False:
            Mbox.showinfo('Chyba', 'Nemám čo dešifrovať')
            return

        inverseKey = self.m.getResult()
        if self.can is False:
            Mbox.showinfo('Chyba', 'Generujte kľúčovú maticu')
            return

        size = self.sizeMatrix

        string = []
        for i in range(0, len(indexes), size):
            tmp = []
            for k in range(i, i + size):
                tmp.append(indexes[k])

            result = np.matmul(tmp, inverseKey)
            newResult = []

            for n in result:
                n = self.m.remake(n)
                ind = int(Decimal(round(np.asscalar(n), 1)).quantize(0, rounding=ROUND_HALF_UP))
                newResult.append(alphabet.getChar(self, ind))

            for s in newResult:
                string.append(s)

        for o in self.others:
            string.insert(o[1], o[0])

        if self.tmpSize != 0:
            tmp = self.tmpSize
            while tmp > 0:
                string.pop()
                tmp -= 1

        up = self.upper
        for u in up:
            string[u] = string[u].upper()
        result = ''.join(string)
        self.setRight(result)

    #uloženie výsledkov z block2 pomocou dialógového okna
    def save(self):
        adress = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        if adress is None:
            return
        right = str(self.getRight())

        adress.write(right)
        adress.close()


a = Application()
a.window.mainloop()
