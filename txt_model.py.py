#
# A Textmodel
#
# Olivia Liberti
# oliberti@bu.edu
#

class TextModel:
    """A class that represents a text model"""

    def __init__(self, model_name):
        """constructor for objects of type TextModel."""
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.sentence_lengths = {}
        self.stems = {}
        self.commas_per_sentence = {}
        

    def __repr__(self):
        """returns a string that includes the name of the model as well as
           the sizes of the dictionaries for each feature of the text.
        """
        
        s = 'text model name: ' + self.name + '\n' 
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of word stems: ' + str(len(self.stems)) + '\n'
        s += '  number of commas counts: ' + str(len(self.commas_per_sentence)) + '\n'
        return s
    

    def add_string(self, s):
        """adds a string of text s to the model by augmenting the feature
           dictionaries defined in the constructor
        """
        k = s.split()
        
        l = 1
        for f in k:
            if f[-1] != '.' and f[-1] != '?' and f[-1] != '!':
                l += 1
            else:
                if l not in self.sentence_lengths:
                    self.sentence_lengths[l] = 1
                    l = 1
                else:
                    self.sentence_lengths[l] += 1
                    l = 1

        i = 0
        for c in k:
            if c[-1] != '.' and c[-1] != '?' and c[-1] != '!':
                if c[-1] == ',':
                    i = i + 1
            else:
                if i not in self.commas_per_sentence:
                    self.commas_per_sentence[i] = 1
                    i = 0
                else:
                    self.commas_per_sentence[i] += 1
                    i = 0
                    
                
        word_list = clean_text(s)
        
        for w in word_list:
            if w not in self.words:
                self.words[w] = 1
            else:
                self.words[w] += 1
        for x in word_list:
            if len(x) not in self.word_lengths:
                self.word_lengths[len(x)] = 1
            else:
                self.word_lengths[len(x)] += 1
        for t in word_list:
            if stem(t) not in self.stems:
                self.stems[stem(t)] = 1
            else:
                self.stems[stem(t)] += 1
        

    def add_file(self, filename):
       """adds all of the text in the file identified by filename to
          the model
       """
       f = open(filename, 'r', encoding='utf8', errors='ignore')
       text = f.read()
       f.close()
       self.add_string(text)

    def save_model(self):
        """saves the TextModel object self by writing its various
           feature dictionaries to files.
        """
        f = open(self.name + '_' + 'words', 'w')
        f.write(str(self.words))
        f.close

        f = open(self.name + '_' + 'word_lengths', 'w')
        f.write(str(self.word_lengths))
        f.close

        f = open(self.name + '_' + 'sentence_lengths', 'w')
        f.write(str(self.sentence_lengths))
        f.close

        f = open(self.name + '_' + 'stems', 'w')
        f.write(str(self.stems))
        f.close

        f = open(self.name + '_' + 'commas_per_sentence', 'w')
        f.write(str(self.commas_per_sentence))
        f.close

    def read_model(self):
        """reads the stored dictionaries for the called TextModel
           object from their files and assigns them to the attributes
           of the called TextModel.
        """
        f = open(self.name + '_' + 'words', 'r')
        self.words = f.read()
        f.close()
        elf.words = dict(eval(self.words))
      
        f = open(self.name + '_' + 'word_lengths', 'r')
        self.word_lengths = f.read()
        f.close()
        self.word_lengths = dict(eval(self.word_lengths))

        f = open(self.name + '_' + 'sentence_lengths', 'r')
        self.sentence_lengths = f.read()
        f.close()
        self.sentence_lengths = dict(eval(self.sentence_lengths))

        f = open(self.name + '_' + 'stems', 'r')
        self.stems = f.read()
        f.close()
        self.stems = dict(eval(self.stems))

        f = open(self.name + '_' + 'commas_per_sentence', 'r')
        self.commas_per_sentence = f.read()
        f.close()
        self.commas_per_sentence = dict(eval(self.commas_per_sentence))

    def similarity_scores(self, other):
        """computes and returns a list of log similarity scores measuring
           the similarity of self and other
        """
        word_score = compare_dictionaries(other.words, self.words)
        word_length_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        sentence_length_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        stem_score = compare_dictionaries(other.stems, self.stems)
        comma_score = compare_dictionaries(other.commas_per_sentence, self.commas_per_sentence)
        list_scores = [word_score, word_length_score, sentence_length_score, stem_score, comma_score]
        return list_scores

    def classify(self, source1, source2):
        """compares  the called TextModel object (self) to two other “source” TextModel objects (source1 and source2)
           and determines which of these other TextModels is the more likely source of the called TextModel
        """
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        print("scores for " + source1.name + ": " + str(scores1))
        print("scores for " + source2.name + ": " + str(scores2))

        weighted_sum1 = 5*scores1[0] + 7*scores1[1] + 8*scores1[2] + 6*scores1[3] + 7*scores1[4]
        weighted_sum2 = 5*scores2[0] + 7*scores2[1] + 8*scores2[2] + 6*scores2[3] + 7*scores2[4]
        if weighted_sum1 > weighted_sum2:
            print(self.name + " is more likely to have come from " + source1.name)
        else:
            print(self.name + " is more likely to have come from " + source2.name)

        
def stem(s):
    """returns the stem of s
    """
    special = {'appall', 'kill', 'stroll', 'kiss', 'thrill', 'chugg', 'dress', 'err', 'express', 'fall', 'free', 'gall', 'add','cross', 'impress', 'inn', 'call', 'ball', 'bill', 'buzz'}    
    ie_words = {'vying', 'lying', 'dying', 'tying'}
    short_ing = {'bring','sling','sping', 'bring', 'sing', 'ring', 'king', 'cling' ,'fling', 'wing', 'ding', 'ping', 'ting'}
    c_k_words = {'kick', 'muck', 'lock','pick', 'back', 'mock', 'peck', 'lock', 'nick'}

    if len(s) <= 3:
        return s
    if s[-3:] == 'ing' or s[-4:] == 'ings':  
        if s in short_ing:
            return s
        elif s in special:
            return s[:-3]
        elif s[:-3] not in special and s[-4] == s[-5]:
            return s[:-4]
        elif s[:-3] not in c_k_words and s[-4] == 'k':
            return s[:-4]
        elif s == 'everything' or s == 'anything' or s == 'something':
            return s[:-5]
        elif s in ie_words:
            return s[0] + 'ie'
        else:
            return s[:-3]
    elif s[-3:] == 'ers':
        return s[:-3]
    elif s[-2:] == 'es':
        return s[:-2]
    elif s[-2:] == 'en':
        return s[:-2]
    elif s[-2:] == 'er':
        if s[-3] == s[-4]:
            return s[:-3]
        else:
            return s[:-2] 
    elif s[-2:] == 'ed':
        if s[-3] == s[-4]:
            return s[:-3]
        else:
            return s[:-2]
    elif s[-3:] == 'ies':
        return s[:-2]
    elif s[-1:] == 's':
        return s[:-1]
    elif s[-1:] == 'e' and s not in ie_words:
        return s[:-1]
    elif s[-3:] == 'ful':
        return s[:-3]
    elif s[:2] == 'de':
        return s[2:]
    elif len(s) > 4 and s[-4:] == 'able' or s[-4] == 'ible':
        return s[:-4]
    elif s[:2] == 'in' or s[:2] == 'il' or s[:2] == 'ir':
        return s[2:]
    elif s[-1:] == 'y':
        return s[:-1] + 'i'
    else:
        return s
       
        
def clean_text(txt):
    """returns a list containing the words in txt after it has been
        'cleaned'-with common punctuation and other symbols removed.
    """

    for symbol in """.,'?!()/-:;""":
        txt = txt.replace(symbol, '')
    txt = txt.lower()
    txt = txt.split()
    return txt

import math

def compare_dictionaries(d1, d2):
    """computes and returns the log similartiy score of two feature
       dictionaries
    """
    score = 0
    total = 0
   
    for i in d1:
        total = total + d1[i]
    for i in d2:
        if i in d1:
            if total == 0:
                score = score
            else:
                probablility = (d1[i] / total)
                score = score + (math.log10(probablility) * d2[i])
        else:
             if total == 0:
                 score = score
             else:
                 score = score + ((0.5 / total) * d2[i])
    return score

    
def test():
    """ test for a mystery source """
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')
    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')
   

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)


def run_tests():
    """ test for hilary, bernie, trump, and bill clinton speaches """
    source1 = TextModel('hilary_speaches')
    source1.add_file('hilary_source_text.txt')

    source2 = TextModel('bernie_speaches')
    source2.add_file('bernie_source_text.txt')

    new1 = TextModel('trump_speach')
    new1.add_file('trump_text.txt')
    new1.classify(source1, source2)

    new2 = TextModel('hilary_test')
    new2.add_file('hilary_test.txt')
    new2.classify(source1, source2)

    new3 = TextModel('bernie_test')
    new3.add_file('bernie_test.txt')
    new3.classify(source1, source2)

    new4 = TextModel('bill_clinton_test')
    new4.add_file('bill_clinton_source.txt')
    new4.classify(source1, source2)



    
