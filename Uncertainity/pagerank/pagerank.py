import os
import random
import re
import sys

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
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.
    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    N = len(corpus)
    MOD = dict()
    for p in corpus:
        pRank = 0.15 / N
        if len(corpus[page]):
            if p in corpus[page]:
                pRank += 0.85 / len(corpus[page])
        else:
            pRank += 0.85 / N
        MOD[p] = pRank
    return MOD


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.
    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    prank = {P: 0 for P in corpus}
    cPage = random.choice(list(corpus.keys()))
    for _ in range(n):
        prank[cPage] += 1
        model = transition_model(corpus, cPage, 0.85)
        cPage = random.choice(list(model.keys()))
    return {P: R / n for P, R in prank.items()}


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.
    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    total = len(corpus)
    prank = dict()
    for p in corpus:
        prank[p] = 1 / total
    n = 1
    while True:
        n+=1
        cuur = dict()
        for i in corpus:
            currpr = (0.15) / total
            for p, l in corpus.items():
                if l:
                    if p != i and i in l:
                        currpr += 0.85 * (prank[p] / len(corpus[p]))
                else:
                    currpr += 0.85 * (prank[p] / total)
            cuur[i] = currpr
        if ranks_converged(cuur, prank):
            print(n)
            return cuur
        prank = cuur.copy()


def ranks_converged(i, j):
    for p in i:
        if not i[p]:
            return False
        difference = i[p] - j[p]
        if round(difference, 3) > 0:
            return False
    return True


if __name__ == "__main__":
    main()