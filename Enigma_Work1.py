from abc import ABC, abstractmethod
import cProfile, pstats, io
from random import *
import string

class Substitutor(ABC):#abstract class
    def __init__(self):
        super().__init__()
    @abstractmethod
    def letterCo(self,letter):#convert the letter to 0-25
        letter=ord(letter)-65
        return letter
    @abstractmethod
    def indexCo(self,index):#convert the index to letter
        index=chr(index+65)
        return index
    @abstractmethod
    def reverseTr(self,str,letter):#reverse translation 
        return self.letterCo(str[letter])
    @abstractmethod
    def circularS(self,letter):#circular shifts
        if letter<0:
            letter=letter+26
        if letter>25:
            letter=letter%26
        return letter
    @abstractmethod
    def checkInput(self,input):#input check
        if not input.isalpha():
            #print("the Input include onle letter")
            return 0
        return 1

class Translator(Substitutor):
    def letterCo(self,letter):
        return super().letterCo(letter)
    def indexCo(self,index):
        return super().indexCo(index) 
    def reverseTr(self,str,letter):
        return super().reverseTr(str,letter)
    def circularS(self,str):
        return super().circularS(str)
    def checkInput(self,input):
        return super().checkInput(input)

class Reflector(Translator):        
    def __init__(self):
        self.refStr="YRUHQSLDPXNGOKMIEBFZCWVJAT"# reflector B
        return super().__init__()
    def runRef(self,letter):#convert letter in reflactor
        return self.reverseTr(self.refStr,letter)

class Plugboard(Translator):
    def __init__(self):
        self.plugStr="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        return super().__init__()   
    def changePlug(self,plugIn):#swith letter from input
        if plugIn=="":
            return 0
        plugIn=plugIn.upper()
        tav1=''
        tav2=''
        plugIn=plugIn.replace(" ","")
        if self.checkInput(plugIn)==0 or len(plugIn)%2!=0 or len(plugIn)>20:
           print("error: The input string support (less than 10 pairs) or the Input support onle letter")
           return -1
        else:
            for x in plugIn[::2]:
                tav1=x
                tav2=plugIn[plugIn.index(x)+1]
                self.plugStr=self.plugStr.replace(tav1,"#").replace(tav2,tav1).replace("#",tav2)
            return 0    
    def runPlug(self,letter):#convert letter in plugboard
        return self.reverseTr(self.plugStr,letter)

class Rotors(Translator):
    def __init__(self,strIn,ringOf,ringSet,notch):
        self.strIn=strIn
        self.strInR=""
        self.ringOf=self.letterCo(ringOf)
        self.ringSet=self.letterCo(ringSet)
        self.notch=self.letterCo(notch)
        return super().__init__()    
    def forwardTRotor(self,letter):# work by method P(A+B−C)−B+C
        per=self.circularS(letter+self.ringOf-self.ringSet)
        return self.circularS(self.letterCo(self.strIn[per])-self.ringOf+self.ringSet)    
    def reverseTRotor(self,letter):# work by method P(A+B−C)−B+C
        self.reverseStrIn()
        per=self.circularS(letter+self.ringOf-self.ringSet)
        return self.circularS(self.letterCo(self.strInR[per])-self.ringOf+self.ringSet)    
    def reverseStrIn(self):# do reverse for str input
        len=['']*26
        for i in range(0,26):
            len[self.letterCo(self.strIn[i])]=self.indexCo(i)
        self.strInR=''.join(len)    
    def notchCheck(self):# check notch
        if self.ringOf==self.notch:
            return True
        return False

class EnigmaMachine(Substitutor):
    def __init__(self):
        self.re=Reflector()
        self.plug=Plugboard()
        self.L=Rotors("AJDKSIRUXBLHWTMCQGZNPYFVOE","C","S","E")
        self.M=Rotors("VZBRGITYUPSDNHLXAWMJQOFECK","O","I","Z")
        self.R=Rotors("ESOVPZJAYQUIRHXLNFTGKDCMWB","N","X","J")
        return super().__init__()   
    def runEnigma(self,input):#enigma run get input
        output=""
        for i in input:
            if i==" ": output+=" "
            else:
                self.letterI=self.letterCo(i)
                self.letterI=self.plug.runPlug(self.letterI)
                if self.R.notchCheck() or self.M.notchCheck():
                    if self.M.notchCheck():
                        self.L.ringOf+=1
                    self.M.ringOf+=1
                self.R.ringOf+=1
                if self.R.ringOf==26:self.R.ringOf=0
                if self.M.ringOf==26:self.M.ringOf=0
                if self.L.ringOf==26:self.L.ringOf=0
                self.letterI=self.R.forwardTRotor(self.letterI)
                self.letterI=self.M.forwardTRotor(self.letterI)
                self.letterI=self.L.forwardTRotor(self.letterI)
                self.letterI=self.re.runRef(self.letterI)
                self.letterI=self.L.reverseTRotor(self.letterI)
                self.letterI=self.M.reverseTRotor(self.letterI)
                self.letterI=self.R.reverseTRotor(self.letterI)
                self.letterI=self.plug.runPlug(self.letterI)
                output+=self.indexCo(self.letterI)
        return output    
    def letterThreeRun(self,letterThree):#task5 
        newOf=self.runEnigma(letterThree)
        self.L.ringOf=self.letterCo(newOf[0])
        self.M.ringOf=self.letterCo(newOf[1])
        self.R.ringOf=self.letterCo(newOf[2])
    def buildRotor(self,input,offset,setting):#build rotot for enigma 
        input=input.split(" ")
        offset=offset.split(" ")
        setting=setting.split(" ")
        i=0
        for x in "LMR":
            if input[i]=="I":
                self.x=Rotors("EKMFLGDQVZNTOWYHXUSPAIBRCJ",offset[i],setting[i],"Q")
            if input[i]=="II":
                self.x=Rotors("AJDKSIRUXBLHWTMCQGZNPYFVOE",offset[i],setting[i],"E")
            if input[i]=="III":
                self.x=Rotors("BDFHJLCPRTXVZNYEIWGAKMUSQO",offset[i],setting[i],"V")
            if input[i]=="IV":
                self.x=Rotors("ESOVPZJAYQUIRHXLNFTGKDCMWB",offset[i],setting[i],"J")
            if input[i]=="V":
                self.x=Rotors("VZBRGITYUPSDNHLXAWMJQOFECK",offset[i],setting[i],"Z")
            if i==0:self.L=self.x
            if i==1:self.M=self.x
            if i==2:self.R=self.x
            i+=1 
    def letterCo(self,letter):
        return super().letterCo(letter)
    def indexCo(self,index):
        return super().indexCo(index) 
    def reverseTr(self,str,letter):
        return super().reverseTr(str,letter)
    def circularS(self,str):
        return super().circularS(str)
    def checkInput(self,input):
        return super().checkInput(input)

class main():
    #___Defult Run___#
    def defultEnigmaMachine(self):
        E=EnigmaMachine()
        input="UMDPQ CUAQN LVVSP IARKC TTRJQ KCFPT OKRGO ZXALD RLPUH AUZSO SZFSU GWFNF DZCUG VEXUU LQYXO TCYRP SYGGZ HQMAG PZDKC KGOJM MYYDD H"
        plug="ZU HL CQ WM OA PY EB TR DN VI"#choose Plugboard by big letter with space and pairs
        E.plug.changePlug(plug)
        E.buildRotor("II V IV","C O N","S I X")#choose Rotor by big letter(I-V)(L-M-R)||choose Offset by big letter with space||choose Setting by big letter with space
        E.letterThreeRun("MLD")#for task 5, choose Offset by big letter
        print("input:"+input)
        print("rotor build:|(rotor)|II V IV|(offset)|C O N|(setting|S I X||")
        print("output:"+E.runEnigma(input))
    #___Input Run___#
    def inputEnigmaMachine(self):
        E=EnigmaMachine()
        flag=1
        typeRotor="I II III IV V"
        while (flag!=0):
            plugChange=input('enter plugboard change (less than 10 pairs):')
            plugChange=plugChange.upper()
            flag=E.plug.changePlug(plugChange)
        flag=1
        while (flag!=0):
            rotorL=input('enter type rotor Left (I,II,III,IV,V):')
            rotorL=rotorL.upper()
            offsetL=input('enter Offset for Left rotor(A-Z):')
            offsetL=offsetL.upper()
            settingL=input('enter Setting for Left rotor(A-Z):')
            settingL=settingL.upper()
            if (not rotorL in typeRotor) or offsetL.isdigit() or settingL.isdigit():
                print("error: choose type rotor from the list or offest,setting error")
            else:flag=0
        flag=1
        while (flag!=0):
            rotorM=input('enter type rotor Middle (I,II,III,IV,V):')
            rotorM=rotorM.upper()
            offsetM=input('enter Offset for Middle rotor(A-Z):')
            offsetM=offsetM.upper()
            settingM=input('enter Setting for Middle rotor(A-Z):')
            settingM=settingM.upper()
            if (not rotorL in typeRotor) or rotorM==rotorL or offsetM.isdigit() or settingM.isdigit():
                print("error: choose type rotor from the list, do not choose same rotor or offest,setting error")
            else:flag=0
        flag=1
        while (flag!=0):
            rotorR=input('enter type rotor Right (I,II,III,IV,V):')
            rotorR=rotorR.upper()
            offsetR=input('enter Offset for Right rotor(A-Z):')
            offsetR=offsetR.upper()
            settingR=input('enter Setting for Right rotor(A-Z):')
            settingR=settingR.upper()
            if (not rotorL in typeRotor) or rotorR==rotorM or rotorR==rotorL or offsetR.isdigit() or settingR.isdigit():
                print("error: choose type rotor from the list, do not choose same rotor or offest,setting error")
            else:flag=0
        flag=1
        E.buildRotor(rotorL+' '+rotorM+' '+rotorR,offsetL+' '+offsetM+' '+offsetR,settingL+' '+settingM+' '+settingR)
        while (flag!=0):
            inputS=input("enter the string for Enigma Machine:")
            inputS=inputS.upper()
            if not inputS.isalpha:
                print("The input string support onle letter")
            else:flag=0
        print("output:"+E.runEnigma(inputS))
#Cprofile (task 6)
def profile(fnc):
    print("--------------------------------------------------------------------------------")
    """A decorator that uses cProfile to profile a function"""
    def inner(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval
    return inner
@profile
def cProfileTime():# performance bottlenecks 
  E=EnigmaMachine()
  for x in range(0,1000):
    min_char = 3
    max_char = 10
    allchar = string.ascii_letters
    input = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
    input=input.upper()
    plug = "".join(choice(allchar) for x in range(randint(6,6)))
    plug=plug.upper()
    E.plug.changePlug(plug)
    E.buildRotor("II V IV","C O N","S I X")
    E.runEnigma(input)

#__________Run Enigma Machine_________#
mac=main()
c=8
while(c!=0):
    print("_________Enigma Machine_________")
    print("1.normal machine")
    print("2.defult machine - task 5")
    print("3.performance bottlenecks")
    print("0.Exit")
    c=input("enter the choice:")
    if c=='1':
        mac.inputEnigmaMachine()#run normal machine by input from the user
    if c=='2':
        mac.defultEnigmaMachine()#run task 5
    if c=='3':
        cProfileTime()#run task 6
    else:exit()
#_____________________________________#
