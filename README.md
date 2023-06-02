# BuildCompiler project 
# Programmed by Sohaibssb for Building Compilers Course at Bauman University, Start 6/4/2023

Lab#1: 
Folder_Name: (RegexToNFA_ToDFA_ToDFAM)

Program that takes an arbitrary regular expression as input and executes the following transformations:
1) Based on a regular expression, it builds an NFA.
2) Based on the NFA, constructs an equivalent DFA.
3) Based on the DFA, it constructs an equivalent FA that has the least possible number of states.
By using the algorithm: Minimization_DFA,_Hopcroft_algorithm.
4) Models the minimum CA for the input string from the terminals of the original grammar.

Lab#2: 
Folder_Name: (Left_Recursion_CSG)

Program that removes left recursion and unreachable symbols from a given context-sensitive grammar G = (N, Σ, P, S)

Lab#3:
Folder_Name: (RecursiveDescent)
Parsing using recursive descent
Grammar G1
The grammar of relational expressions with rules is considered.
<expression> ->
<simple expression> |
<simple expression> <relation operation> <simple expression>
<simple expression> ->
<term> |
<sign> <term> |
<simple expression> <addition type operation> <term>
<term> ->
<factor> |
<term> <multiplication type operation> <factor>
<factor> ->
<identifier> |
<constant> |
( < simple expression > ) |
not <factor>
<relationship operation> ->
= | <> | < | <= | > | >=
<sign> ->
+|-
<addition type operation> ->
+ | - | or
<multiplication type operation> ->
* | / | div | mod | and
Remarks.
1. Nonterminals <identifier> and <constant> are lexical units (lexemes) that
left undefined, and when performing laboratory work, you can either consider them
as terminal symbols, or define them as you like and add those definitions.
2. The terminals not, or, div, mod, and are keywords (reserved).
3. Terminals ( ) are delimiters and punctuation characters.
4. Terminals = <> < <= > >= + - * / are operation signs.
5. The non-terminal <expression> is the initial symbol of the grammar.