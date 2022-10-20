project_twitter = open("project_twitter_data.csv", 'r')
resulting_data = open("resulting_data.csv","w")
    

punctuation_chars = ["'", '"', ",", ".", "!", ":", ";", '#', '@']
# lists of words to use
positive_words = []
with open("positive_words.txt") as pos_f:
    for lin in pos_f:
        if lin[0] != ';' and lin[0] != '\n':
            positive_words.append(lin.strip())


negative_words = []
with open("negative_words.txt") as pos_f:
    for lin in pos_f:
        if lin[0] != ';' and lin[0] != '\n':
            negative_words.append(lin.strip())


def strip_punctuation(word):
    """
    Function to remove punctuation chars from word
    :param word: input string
    :return: word: all words without punctuation chars
    """
    for i in punctuation_chars:
        word = word.replace(i, "")
    return word


def get_pos(sentence):
    """
    Function to count positive words from a sentence
    :param sentence: input string
    :return: positive_count: counts all positive words
    """
    positive_count = 0
    sentence = strip_punctuation(sentence).lower().split(" ")
    for word in sentence:
        if word in positive_words:
            positive_count += 1
    return positive_count


def get_neg(sentence):
    """
    Function to count negative words from a sentence
    :param sentence: input string
    :return: negative_count: counts all negative words
    """
    negative_count = 0
    sentence = strip_punctuation(sentence).lower().split(" ")
    for word in sentence:
        if word in negative_words:
            negative_count += 1
    return negative_count


def write_data(result):
    """
    Function to create a csv file and populate it
    :param result: input file
    """
    result.write("Number of Retweets, Number of Replies, Positive Score, Negative Score, Net Score")
    result.write("\n")
    
    lines = project_twitter.readlines()
    header = lines[0]
    
    for word in lines[1:]:
        lst = word.strip().split(',')
        result.write("{}, {}, {}, {}, {}".format(lst[1], lst[2], get_pos(lst[0]), get_neg(lst[0]), (get_pos(lst[0])-get_neg(lst[0]))))    
        result.write("\n")


write_data(resulting_data)
project_twitter.close()
resulting_data.close() 