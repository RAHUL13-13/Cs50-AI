from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Or(AKnight, AKnave),
    Implication(Not(AKnave), AKnight),
    Implication(Not(AKnight), AKnave),
    Biconditional(AKnight, And(AKnight, AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),

    Implication(AKnave, BKnight),
    Implication(BKnight, AKnave),

    Implication(AKnave, Not(AKnight)),
    Implication(BKnave, Not(BKnight)),

    Biconditional(AKnight, And(AKnave, BKnave)),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(And(AKnave, BKnight), And(AKnight, BKnave), And(BKnight, BKnave), And(AKnave, AKnight)),
    Implication(AKnight, BKnight),
    Implication(AKnave, BKnight),
    Biconditional(AKnight, And(BKnight, AKnight)),
    Biconditional(BKnight, And(BKnight, AKnave)),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(
        And(CKnight, And(BKnave, AKnight)),
        And(CKnave, And(BKnight, AKnave))
        ),

    Implication(AKnave, Not(AKnight)),
    Implication(BKnave, Not(BKnight)),
    Implication(CKnave, Not(CKnight)),

    Implication(CKnight, And(BKnave, AKnight)),
    Implication(CKnave, And(BKnight, AKnave)),

    Biconditional(CKnight, And(BKnave, AKnight)),
    Biconditional(CKnave, And(BKnight, AKnave)),

    Biconditional(BKnight, And(AKnight, CKnave)),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
