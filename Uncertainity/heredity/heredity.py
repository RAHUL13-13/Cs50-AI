import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    i = dict()
    with open(filename) as f:
        read = csv.DictReader(f)
        for r in read:
            name = r["name"]
            i[name] = {"name": name,"mother": r["mother"] or None,"father": r["father"] or None,"trait": (True if r["trait"] == "1" else False 
            if r["trait"] == "0" else None)}
    return i


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    r = [set(s) for s in itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s) + 1))]
    return r


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    prob = float(1)
    for j in people:
        gene = (2 if j in two_genes else 1 if j in one_gene else 0)
        trait = j in have_trait
        m = people[j]["mother"]
        f = people[j]["father"]
        if m is None and f is None:
            prob *= PROBS["gene"][gene]
        else:
            passing = {m: 0, f: 0}
            for i in passing:
                passing[i] = ((1 - PROBS["mutation"]) if i in two_genes else 0.5 if i in one_gene else
                              (PROBS["mutation"]))
            prob = prob* (passing[m] * passing[f] if gene == 2 else passing[m] * (1 - passing[f]) +
                     (1 - passing[m]) * passing[f] if gene == 1 else
                     (1 - passing[m]) * (1 - passing[f]))
        prob = prob* PROBS["trait"][gene][trait]
    return prob


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for i in probabilities:
        genes = (2 if i in two_genes else 1 if i in one_gene else 0)
        trait = i in have_trait
        probabilities[i]["gene"][genes] += p
        probabilities[i]["trait"][trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for i in probabilities:
        for k in probabilities[i]:
            total = sum(dict(probabilities[i][k]).values())
            for j in probabilities[i][k]:
                probabilities[i][k][j] /= total


if __name__ == "__main__":
    main()
