
sentence = 'the voice of the lord is powerful the voice of the lord is upon the waters the voice of the lord shaketh the wilderness obey the voice of the lord your god obey the voice of the lord thy god obey the voice of the lord our god'

def add_sentence(n,sentence):
    sentence = sentence + ' EOL'
    starters = []
    stoppers = []
    txt = ''
    states = []
    words = sentence.lower().split()
    starters.append(words[0])
    stoppers.append(words[len(words) - 1])

    for i in range(len(words)+1):
        states.append(words[i:n])
        n = n+1
    #print(states)


    #Dictionary
    all_dict = {}
    for i in range(len(states)):
        key = ' '.join(states[i])
        if key not in all_dict.keys():
            all_dict[key] = []
        else:
            all_dict[key].append(states[i+1][-1])




    print(all_dict)

   # txt = txt + ' ' + ' '.join(words[i:n])
   # print(txt)
        #key_split = key.split()
        #print(master_dict[str(key_split[1])])
        #all_dict[key] = master_dict[str(key_split[1])]
    #print(all_dict)







    '''
    sentence = sentence + ' EOF'
    starters = []
    stoppers = []
    all_states = []
    words = sentence.lower().split()
    starters.append(words[0])
    stoppers.append(words[len(words)-1])
    print(words)


    #Make Pairs
    states = [[words[i], words[i+1]] for i in range(0, len(words)-1)]
    for i in range(len(states)):
        all_states.append(tuple(states[i]))
    print(all_states)


    #Dict
    all_dict = {}
    for first, second in all_states:
        if first in all_dict.keys():
            all_dict[first].append(second)
        else:
            all_dict[first] = [second]
    print(all_dict)


    #while succesor not in stoppers:
    
    corpus = sentence.split()
    def make_pairs(corpus):
        for i in range(len(corpus) - 1):
            yield (corpus[i], corpus[i + 1])

    pairs = make_pairs(corpus)
    print(list(pairs))



    
    for i in range(0, len(words)-1):
        states.append(words[i])
    state = tuple(states)
    print(state)
    all_dict = {}
    for first in state:
        if first in all_dict.keys():
           all_dict[first].append(second)
        else:
            all_dict[first] = [second]
    print(all_dict)
    '''

add_sentence(3,sentence)