import csv
from collections import Counter
import nltk
from nltk.stem import *
from nltk import word_tokenize
import multiprocessing
import os

# Variables
movies = dict()
genres = []
genre_words = dict()

# functions
def get_words(genre):
    global movies
    genre_words = list()
    exclude_list = ['aka', 'vs', 'i', 'ii', 'iii']
    titles = movies[genre]

    for title in titles:
        clean = ''
        for char in title:
            if char.isalpha() or char == ' ':
                clean += char.lower()
        title = clean
        raw = word_tokenize(title) # get a list of every word in the sanitized title
        tokens = nltk.pos_tag(raw) # analyze each word to see what part of speech it is
        nouns = [x[0] for x in tokens if x[1] == 'NN' or x[1] == 'NNS' or x[1] == 'NNP' or x[1] == 'NNPS' ] # make a new list of the words only if they are nouns
        nouns = [x for x in nouns if x not in exclude_list] # remove exculded words
        stemmer = PorterStemmer()
        nouns = [stemmer.stem(w) for w in nouns]
        if len(genre_words) > 0: # add each word of word list to genre_words
            for word in nouns:
                genre_words.append(word)
        else:
            genre_words = nouns
    
    c = Counter(genre_words)
    # get the 10 most common words used in titles for the given genre
    most_common = c.most_common(10)
    f = open('answers~.txt', "a")
    f.write("\033[1m" + genre + "\033[0m" + ':\n')
    for item in most_common:
        f.write(item[0] + '\n')
    f.write('\n')
    f.close()

# read in data
with open('data/movies.csv', newline = '') as csvfile:
    next(csvfile)
    reader = csv.reader(csvfile, delimiter = ',')
    for row in reader:
        the_id = row[0]
        title = row[1]
        genres = row[2].split('|')
        for genre in genres:
            try:
                movies[genre].append(title)
            except:
                movies[genre] = [title]


if __name__ == "__main__":
    # Part 1
    # Among all movies, list the top 10 genres - in terms of number of movies 
    # associated with the genre. Do not include "no genres listed" in the most
    # frequent list. List the number of movies with each of the 10 genres.
    print('Answering Part 1...')
    print('Part 1')
    movies.pop('(no genres listed)', None)
    genre_movies = [(k, len(v)) for k, v in movies.items()]
    genre_movies.sort(key=lambda x: x[1], reverse = True)
    genre_movies = genre_movies[:10]
    for key in genre_movies:
        print(str(key))
    print('\n')

    # Part 2
    # For each of the top 10 genres, find the 10 most common nouns that appear
    # in movies associated with that genre. For this part, you will need to use
    # a natural language processing library called nltk.
    print('Answering Part 2...')
    print('Part 2')
    genres = [k[0] for k in genre_movies]
    processes = list()
    for key in genres:
        p = multiprocessing.Process(target=get_words, args=(key, ))
        processes.append(p)
    for p in processes:
        p.start()
    for p in processes:
        p.join()

    with open('answers~.txt') as f:
        lines = f.readlines()
        for line in lines:
            print(line.rstrip())
    if os.path.exists('answers~.txt'):
        os.remove('answers~.txt')