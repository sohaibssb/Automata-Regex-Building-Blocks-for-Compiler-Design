def remove_left_recursion(grammar):
    prods = grammar.split('\n')
    new_prods = []
    for prod in prods:
        prod_split = prod.split('->')
        nt = prod_split[0]
        rhs = prod_split[1].split('|')
        alpha = []
        beta = []

        for i in range(len(rhs)):
            if rhs[i][0] == nt:
                alpha.append(rhs[i][1:])
            else:
                beta.append(rhs[i])

        if alpha:
            new_nt = nt + "'"
            new_prod1 = nt + '->' + '|'.join(beta) + new_nt
            new_prod2 = new_nt + '->' + '|'.join(alpha) + new_nt + '|e'
            new_prods.append(new_prod1)
            new_prods.append(new_prod2)
        else:
            new_prods.append(prod)

    return '\n'.join(new_prods)


def remove_unreachable_symbols(grammar):
    prods = grammar.split('\n')
    nt_set = set()
    reachable_nt_set = set()
    new_prods = []

    # collect all non-terminal symbols
    for prod in prods:
        nt = prod.split('->')[0].strip()
        nt_set.add(nt)

    # start symbol is always reachable
    reachable_nt_set.add(prods[0].split('->')[0].strip())

    # find all reachable symbols
    while True:
        old_size = len(reachable_nt_set)
        for prod in prods:
            nt = prod.split('->')[0].strip()
            if nt in reachable_nt_set:
                rhs = prod.split('->')[1].strip()
                for sym in rhs.split():
                    if sym in nt_set:
                        reachable_nt_set.add(sym)
        if len(reachable_nt_set) == old_size:
            break

    # create new productions for reachable symbols
    for prod in prods:
        nt = prod.split('->')[0].strip()
        if nt in reachable_nt_set:
            new_prods.append(prod)

    return '\n'.join(new_prods)


if __name__ == '__main__':
    grammar = input('Введите грамматику КС-грамматику G = (N, Σ, P, S): ')
    new_grammar = remove_left_recursion(grammar)
    print('\nНовая грамматика без левой рекурсии:')
    print(new_grammar)

    new_grammar = remove_unreachable_symbols(new_grammar)
    print('\nНовая грамматика без недостижимых символов:')
    print(new_grammar)
    #Examples:
    # A->Aa|b
    #A->AA|b
    #A->Aa|b|c