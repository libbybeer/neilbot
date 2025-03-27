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
    chunks = [glue.join(tokenlist[i:i+lookback]) for i in range(len(tokenlist)-lookback)]
    bumplist = tokenlist[lookback:]
    for t1,t2 in zip(chunks,bumplist):
        newt = transitions.get(t1)
        if not newt:
            newt = []
        newt = newt + [t2]
        transitions[t1] = newt
    return transitions

def construct_response(transitions,sep="\n",glue=" ",lookback=1,start=None):
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
        print([glue.join(outs),nextw])
        if glue == "":
            outs[0] += nextw[0]
        else:
            outs += [nextw]
        if nextw == sep:
            break
    return glue.join(outs)


input_fns = ["cookie.txt","fox.txt","hp1.txt","ces_staff.txt"]

word_transitions = {}
for i in input_fns:
    word_transitions[i] = read_in_words(i)

letter_transitions = {}
for i in input_fns:
    letter_transitions[i] = read_in_words(i,sep=" ",glue="")


print(construct_response(letter_transitions["ces_staff.txt"],sep="\n",glue="",lookback=1,start="Dr."))
