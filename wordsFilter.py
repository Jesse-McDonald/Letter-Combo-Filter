from datetime import *
from time import *
numberOfLetters=0
numberOfCombos=0
log=open("log.txt",'w')

def lprint(stringIn):
    now = datetime.now()
    print('['+str(now.hour)+':'+str(now.minute)+':'+str(now.second)+']'+stringIn)
    log.write('['+str(now.hour)+':'+str(now.minute)+':'+str(now.second)+']'+stringIn+'\n')
    
def vowel(check):
    charList="aeiouy"
    return check in charList

def consonant(check):
    charList="bcdfghjklmnpqrstvwxz"
    return check in charList

def processWords(infile,outfile):
    lprint("Word Processing Started")
    sectionStart=time()
    line=""
    fin=open(infile,'r')
    fout=open(outfile,'w')
    inWords=fin.read()
    inWords=inWords.split()
    for word in inWords:
        maxV=len(word)
        edge=0
        current=0
        sequence=""
        start=0
        for i in range(len(word)):
            c=word[i]
            if vowel(c):
                current=2
            elif c=='y' and i==0:
                current=1
            elif consonant(c):
                current=1
            else:
                current=0
            if current==0:
                continue
            if i==0:
                edge=current
            if edge!=current:
                sequence=word[start:i]
                fout.write(str(sequence)+'\n')
                start=i
                edge=current
    fin.close()
    fout.close()
    sectionTime=time()-sectionStart
    lprint("Word Processing Finished in "+str(sectionTime)+"s.")
	
    
def filterSequence(infile, outfile,outfile2):
    global numberOfLetters
    lprint("Letter Filtering Started")
    sectionStart=time()
    fin=open(infile,'r')
    fout=open(outfile,'w')
    fout2=open(outfile2,'w')
    inWords=fin.read()
    inWords=inWords.split()
    fin.close()
    inWords.sort()
    inputLine=inWords[0]
    count=1
    for word in inWords:
        if inputLine==word:
            count+=1    
        else:
            fout.write(word+"\t"+str(count)+'\n')
            fout2.write(word+'\n')
            numberOfLetters+=1
            inputLine=word
            count=1;
    fin.close()
    fout.close()            
    sectionTime=time()-sectionStart
    lprint("Letter Filtering Finished in "+str(sectionTime)+"s.")

def findCommonCombo(infile, outfile,cfile):
    global numberOfCombos
    lprint("Combo processing started")
    sectionStart=time()
    line=""
    fin=open(infile,'r')
    fcheck=open(cfile,'r')
    fout=open(outfile,'w')
    inWords=fin.read()
    inWords=inWords.split()
    

    check=fcheck.read()
    check=check.split()
    for word in inWords:
        wordStart=time()
        lprint("Started scanning combinations of "+word+"...")
        for otherWord in inWords:
            combo=word+otherWord
            count=0
            if combo not in inWords:
                for cWord in check:
                    if combo in cWord:
                        count+=1
                if count:
                    fout.write(combo+" "+str(count)+"\n")
                    numberOfCombos+=1
        lprint("Finished scanning combinations of "+word+"\nTime taken "+str((time()-wordStart))+"s.")
    lprint("Finished scanning combinations "+str(time()-sectionStart ))
    fin.close()
    fcheck.close()
    fout.close()
def main():
    startTime=time()

    breakOut=True
    while breakOut:
        cin=input("Enter path to file containing text sample: ")
        path=input("Enter path to output directory: ")
        processWords(cin,path+"/letterCombos.txt")
        filterSequence(path+"/letterCombos.txt",path+"/filteredLetters.txt",path+"/uncountedLetters.txt")
        ch=input("The next step can take quite a while, would you like to continue. (Y/N): ")
        ch=ch.lower()

        if ch=='y':
            findCommonCombo(path+"/uncountedLetters.txt",path+"/Every_Occurance_Ever_Filtered.txt",cin)
    endTime = time()
    totalTime = endTime - startTime
    lprint("Program Finished in "+str(totalTime)+\
          "s.\n"+str(numberOfLetters)+\
          " lines in \"data/Letter_Combos.txt\"."+\
          "\n"+str(numberOfCombos)+\
          " lines in \""+path+"/Every_Occurance_Ever_Filtered.txt\".")
    cin=input("Process new file? (Y/N): ")
    cin=cin.lower()

        if not cin=='y':    
            breakOut=False
    log.close()
main()

