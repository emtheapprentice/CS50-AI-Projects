import nltk
import sys
import os
import string
import math

FILE_MATCHES = 4
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = dict()
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), encoding='utf-8') as f:
            files[filename] = f.read()
    
    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = [
        word.lower() for word in
        nltk.word_tokenize(document)
        if word.isalpha
    ]
    tokenized = []
    
    for word in words:
        if word in nltk.corpus.stopwords.words("english"):
            continue
        punctuation = 0
        for c in word:
            if c in string.punctuation:
                punctuation += 1
        if len(word) == punctuation:
            continue
        tokenized.append(word)

    return tokenized


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = dict()
    words = set()
    
    for filename in documents:
        words.update(documents[filename])
    for word in words:
        f = sum(word in documents[filename] for filename in documents)
        idf = math.log(len(documents) / f)
        idfs[word] = idf
    
    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tfidfs = dict()
    top_files = []
    for filename in files:
        tf = dict()
        tfidf = dict()
        total = 0
        for word in files[filename]:
            if word in query:
                if word in tf.keys():
                    tf[word] += 1
                    total += 1
                else:
                    tf[word] = 1
                    total += 1
            else:
                total += 1
        for word in tf:
            tfidf[word] = (tf[word] / total) * idfs[word]
        for word in tfidf:
            if word in tfidfs.keys():
                tfidfs[filename] += tfidf[word]
            else:
                tfidfs[filename] = tfidf[word]
    filelist = sorted(tfidfs.items(), key=lambda x: x[1], reverse=True)

    i = 0
    for file in filelist:
        top_files.append(file[0])
        i += 1
        if i == n:
            break
        
    return top_files


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    top_sentences = []
    for sentence in sentences:
        sentencelist = []
        idf = 0
        density = 0
        for word in query:
            if word in sentences[sentence]:
                idf += idfs[word]
                density += sentences[sentence].count(word) / len(sentences[sentence])
        if idf != 0:
            sentencelist.extend([sentence, idf, density])
            top_sentences.append(sentencelist)
        
    return [sentence for sentence, idf, density in sorted(top_sentences, key=lambda x: (x[1], x[2]), reverse=True)][:n]


if __name__ == "__main__":
    main()
