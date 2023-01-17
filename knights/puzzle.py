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
    Biconditional(AKnight, Not(AKnave)), Biconditional(AKnave, Not(AKnight)),
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    Implication(Not(And(AKnight, AKnave)), AKnave),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Biconditional(AKnight, Not(AKnave)), Biconditional(AKnave, Not(AKnight)),
    Biconditional(BKnight, Not(BKnave)), Biconditional(BKnave, Not(BKnight)),
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),

    Implication(Not(Implication(AKnight, And(AKnave, BKnave))), AKnave),
    Implication((And(AKnave, BKnave)), AKnight),
    Implication(Not(AKnight), BKnight),
    Implication(AKnight, BKnave)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Biconditional(AKnight, Not(AKnave)), Biconditional(AKnave, Not(AKnight)),
    Biconditional(BKnight, Not(BKnave)), Biconditional(BKnave, Not(BKnight)),
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),

    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    Implication(AKnight, Or(And(AKnight, AKnight), And(AKnave, BKnave))),
    Implication(Not(AKnight), AKnave),
    Implication(Not(BKnight), BKnave),
    Implication(AKnight, BKnight),
    Implication(AKnave, BKnight),
    Implication(BKnight, AKnave)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Biconditional(AKnight, Not(AKnave)), Biconditional(AKnave, Not(AKnight)),
    Biconditional(BKnight, Not(BKnave)), Biconditional(BKnave, Not(BKnight)),
    Biconditional(CKnight, Not(CKnave)), Biconditional(CKnave, Not(CKnight)),
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave)),

    Implication(AKnight, Or(AKnight, AKnave)),
    Implication(AKnave, Not(Or(AKnight, AKnave))),
    Implication(BKnight, And(Not(Implication(AKnight, Or(AKnight, AKnave))), Implication(AKnight, Or(AKnight, AKnave)))),
    Implication(BKnave, And(Implication(AKnight, Or(AKnight, AKnave)), Implication(AKnight, Or(AKnight, AKnave)))),
    Implication(BKnight, CKnave),
    Implication(CKnight, BKnave),
    Implication(CKnight, AKnight),
    Implication(AKnave, CKnave),
    Implication(AKnight, CKnight)
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
