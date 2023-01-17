import os
import random
import re
import sys
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    page_links = len(corpus[page])
    corpus_links = len(corpus)
    prob_dist = dict()
    for value in corpus:
        prob_dist[value] = (1 - damping_factor) / corpus_links
    if page_links == 0:
        pass
    else:
        for value in corpus[page]:
            prob_dist[value] += damping_factor / page_links
    
    return prob_dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    ranking = dict()
    sample = random.choice(list(corpus))
    samples = dict()
    for i in range(n - 1):
        model = transition_model(corpus, sample, damping_factor)
        sample = random.choices(list(model), weights=model.values(), k=1).pop()
        if sample in samples:
            samples[sample] += 1
        else:
            samples[sample] = 1
    for page in corpus:
        ranking[page] = samples[page] / n
    sum = 0
    for page in ranking:
        sum += ranking[page]
    if sum != 1.0:
        for page in ranking:
            ranking[page] = ranking[page] / sum
    return ranking


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    ranking = dict()
    newranking = dict()
    for page in corpus:
        ranking[page] = 1 / len(corpus)
    while True:
        iteration = 0
        for page in corpus:
            sigma = 0
            for p2 in corpus:
                if page in corpus[p2]:
                    sigma += ranking[p2] / len(corpus[p2])
            
            newranking[page] = (1 - damping_factor) / len(corpus) + (damping_factor * sigma)
            if abs(ranking[page] - newranking[page]) < 0.0001:
                iteration += 1
            if iteration == len(corpus):
                sum = 0
                for page in newranking:
                    sum += newranking[page]
                while sum != 1.0:
                    for page in newranking:
                        newranking[page] = newranking[page] / sum
                    sum = 0
                    for page in newranking:
                        sum += newranking[page]
                return newranking
        ranking = copy.deepcopy(newranking)


if __name__ == "__main__":
    main()
