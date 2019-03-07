
import typing
from apriori.itemset import itemsets_from_transactions
from apriori.rule import generate_rules_apriori


def apriori(transactions: typing.List[tuple], min_support: float = 0.5,
            min_confidence: float = 0.5, max_length: int = 8, verbosity: int = 0):
    itemsets, num_trans = itemsets_from_transactions(transactions, min_support,
                                                     max_length, verbosity)
    rules = generate_rules_apriori(itemsets, min_confidence, num_trans,
                                   verbosity)
    return itemsets, list(rules)

# transactions = [('a', 'b', 'c'), ('a', 'b', 'd'), ('f', 'b', 'g')]
# itemsets, rules = apriori(transactions, min_confidence=1)
# print(rules)
