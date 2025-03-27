import random

def read_in_words(input_fn,sep="\n",glue=" ",lookback=1):
    with open(input_fn,"r") as f:
        lines = f.readlines()
    tokens = []
    if glue == "":
        for l in lines:
            for c in l:
                tokens += c
    else:
        for l in lines:
            for s in l.split(sep):
                tokens += l.split(glue)+[sep]
    transitions = compute_transitions(tokens,sep=sep,glue=glue,lookback=lookback)
    return transitions

def compute_transitions(tokenlist,sep="\n",glue=" ",lookback=1):
    transitions = {}
    tl = ["\n"]+tokenlist
    #print(tl)
    chunks = [glue.join(tl[i:i+lookback]) for i in range(len(tl)-lookback)]
    bumplist = tl[lookback:]
    for t1,t2 in zip(chunks,bumplist):
        newt = transitions.get(t1)
        #print([t1,newt,t2])
        if not newt:
            newt = []
        newt += t2
        transitions[t1] = newt
        #print(newt)
    return transitions

def construct_response(transitions,sep="\n",glue=" ",lookback=1,start=None,verbose=False):
    if start is None:
        start = sep
    outs = [start]
    while(1):
        #print("-"+glue.join(outs)+"-")
        if glue == "":
            lastw = glue.join(outs[0][-lookback:])
        else:
            lastw = glue.join(outs[-lookback:])
        ts = transitions.get(lastw)
        if not ts:
            print("error: no transitions for '"+lastw+"'")
            break
        nextw = random.choice(ts)
        if verbose:
            print([glue.join(outs),nextw])
        if glue == "":
            outs[0] += nextw[0]
        else:
            outs += [nextw]
        if nextw == sep:
            break
    return glue.join(outs)


def make_lines(fn="jj.txt",n=5):
    for i in range(n):
        print(construct_response(word_transitions[fn],sep="\n",glue=" ",lookback=1,start=None,verbose=False).strip())

def make_words(fn="ces_staff.txt",n=10,lookback=1,start="\n"):
    for i in range(n):
        print(construct_response(letter_transitions[fn][lookback],sep="\n",glue="",lookback=lookback,verbose=False,start=start).strip())


input_fns = ["cookie.txt","fox.txt","hp1.txt","ces_staff.txt","jj.txt"]
input_fns = ["ces_staff.txt","jj.txt"]

word_transitions = {}
for i in input_fns:
    word_transitions[i] = read_in_words(i)

letter_transitions = {}
lookback_max = 5
for i in input_fns:
    letter_transitions[i] = {}
    for j in range(lookback_max+1):
        letter_transitions[i][j] = read_in_words(i,sep=" ",glue="",lookback=j)

nout = 3
make_words("ces_staff.txt",lookback=1,start="\n",n=nout)
print("---------------------")
make_words("ces_staff.txt",lookback=1,start="D",n=nout)
print("---------------------")
make_words("ces_staff.txt",lookback=1,start="Dr.",n=nout)
print("=====================")
make_words("ces_staff.txt",lookback=4,start="Dr. ",n=nout)
