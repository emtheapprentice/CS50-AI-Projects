import sys

from crossword import *

import copy

import random


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.crossword.variables:
            domainlist = copy.deepcopy(self.domains[var])
            for word in domainlist:
                if len(word) != var.length:
                    self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        if self.crossword.overlaps[x, y] != None:
            domainlist = copy.deepcopy(self.domains[x])
            consistent = False
            revised = False
            for word in domainlist:
                for w2 in self.domains[y]:
                    if word[self.crossword.overlaps[x, y][0]] == w2[self.crossword.overlaps[x, y][1]]:
                        consistent = True
                if not consistent:
                    self.domains[x].remove(word)
                    revised = True
                consistent = False
            if revised:
                return True
        return False

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs == None:
            queue = []
            for var_pair in self.crossword.overlaps:
                if self.crossword.overlaps[var_pair] != None:
                    queue.append(var_pair)
        else:
            queue = arcs

        while queue:
            arc = queue.pop(0)
            x = arc[0]
            y = arc[1]
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for neighbor in self.crossword.neighbors(x):
                    if neighbor == y:
                        continue
                    if (neighbor, x) not in queue:
                        queue.append((neighbor, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.crossword.variables:
            if var not in assignment:
                return False
            if assignment[var] == None:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for var in assignment:
            for v2 in assignment:
                if v2 == var:
                    continue
                if assignment[var] == assignment[v2]:
                    return False
                if self.crossword.overlaps[var, v2] != None:
                    if assignment[var][self.crossword.overlaps[var, v2][0]] != assignment[v2][self.crossword.overlaps[var, v2][1]]:
                        return False
            if len(assignment[var]) != var.length:
                return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        #get neighbors
        #eliminate assigned
        #check all domains against var values
        #by counting failed words

        neighbors = self.crossword.neighbors(var)
        for neighbor in neighbors:
            if neighbor in assignment:
                neighbors.remove(neighbor)
        ordered_values = dict()
        for word in self.domains[var]:
            for neighbor in neighbors:
                for w2 in self.domains[neighbor]:
                    if word[self.crossword.overlaps[var, neighbor][0]] != w2[self.crossword.overlaps[var, neighbor][1]] or word == w2:
                        if not ordered_values[word]:
                            ordered_values[word] = 1
                        else:
                            ordered_values[word] += 1
        orderedList = sorted(ordered_values.items() , key=lambda t : t[1])
        order = []
        for keyvalue in orderedList:
            order.append(keyvalue[0])
        return order


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # loop all variables
        # if not in assignment keep track of fewest remaining values
        # if tied final variable, the one with most neighbors wins, else whatever

        minimum = 10000000000000000
        tied = []
        degrees = 10000000
        for var in self.crossword.variables:
            if var in assignment:
                continue
            else:
                if len(self.domains[var]) < minimum:
                    minimum = len(self.domains[var])
                    del tied[:]
                    tied.append(var)
                elif len(self.domains[var]) == minimum:
                    tied.append(var)
        if len(tied) > 1:
            for var in tied:
                if len(self.crossword.neighbors(var)) < degrees:
                    degrees = len(self.crossword.neighbors(var))
                    del tied[:]
                    tied.append(var)
                elif len(self.crossword.neighbors(var)) == degrees:
                    tied.append(var)
        else:
            variable = tied[0]
            return variable
        if len(tied) > 1:
            variable = random.choice(tied)
            return variable
        else:
            variable = tied[0]
            return variable

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for word in self.domains[var]:
            assignment[var] = word
            if self.consistent(assignment):
                solution = self.backtrack(assignment)
                if solution != None:
                    return solution
        assignment.pop(var)
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()