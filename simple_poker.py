import random
import itertools

def poker(hands):
    "Return a list of winning hands: poker([hand,...]) => [hand,...]"
    return allmax(hands, key=hand_rank)

def allmax(iterable, key=None):
    "Return a list of all items equal to the max of the iterable."
    result = [iterable[0]]
    for hand in iterable[1:]:
        if hand_rank(hand) == hand_rank(result[0]):
            result.append(hand)
        elif hand_rank(hand) > hand_rank(result[0]):
            result=[]
            result.append(hand)
    return result

def hand_rank(hand):
    "Return a value indicating the ranking of a hand."
    ranks = card_ranks(hand) 
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)

def card_ranks(hand):
    "Return a list of the ranks, sorted with higher first."
    ranks = ['--23456789TJQKA'.index(r) for r, s in hand]
    ranks.sort(reverse = True)
    return [5, 4, 3, 2, 1] if (ranks == [14, 5, 4, 3, 2]) else ranks

def flush(hand):
    "Return True if all the cards have the same suit."
    suits = [s for r,s in hand]
    return len(set(suits)) == 1

def straight(ranks):
    "Return True if the ordered ranks form a 5-card straight."
    return (max(ranks)-min(ranks) == 4) and len(set(ranks)) == 5

def kind(n, ranks):
    """Return the first rank that this hand has exactly n-of-a-kind of.
    Return None if there is no n-of-a-kind in the hand."""
    for r in ranks:
        if ranks.count(r) == n: return r
    return None

def two_pair(ranks):
    "If there are two pair here, return the two ranks of the two pairs, else None."
    pair = kind(2, ranks)
    lowpair = kind(2, list(reversed(ranks)))
    if pair and lowpair != pair:
        return (pair, lowpair)
    else:
        return None

def deal(numhands, n=5, deck=[r+s for r in '23456789TJQKA' for s in 'SHDC']):
    "Deal function deals numhands hands with n cards each."
    random.shuffle(deck)
    return [deck[n*i:n*(i+1)] for i in range(numhands)]

def best_hand(hand):
    "From a 7-card hand, return the best 5 card hand."
    return max(itertools.combinations(hand, 5),key=hand_rank)
    
'''
def best_wild_hand(hand):
    "From a 7-card hand, return the best 5 card hand."
    black_cards = [r+s for r in '23456789TJQKA' for s in 'SC']
    red_cards = [r+s for r in '23456789TJQKA' for s in 'HD']
   
    all_hands = list(itertools.combinations(hand, 5))
    all_hands = [list(hand) for hand in all_hands]

    for hand in all_hands:
        if '?B' in hand:
            for black_card in black_cards:
                temp = [black_card if card == '?B' else card for card in hand]
                all_hands.append(temp)
    all_hands = [hand for hand in all_hands if '?B' not in hand]

    for hand in all_hands:
        if '?R' in hand:
            for red_card in red_cards:
                temp = [red_card if card == '?R' else card for card in hand]
                all_hands.append(temp)
    all_hands = [hand for hand in all_hands if '?R' not in hand]

    return max(all_hands,key=hand_rank)
'''
allranks = '23456789TJQKA'
redcards = [r+s for r in '23456789TJQKA' for s in 'DH']
blackcards = [r+s for r in '23456789TJQKA' for s in 'SC']

def best_wild_hand(hand):
    "Try all values for jokers in all 5-card collections"
    hands = set(best_hand(h) for h in itertools.product(*map(replacements, hand)))
    return max(hands, key=hand_rank)

def replacements(card):
    """Return a list of the possible replacements for a card.
    There will be more than 1 only for wild cards."""
    if card == '?B': return blackcards
    elif card == '?R': return redcards
    else: return [card]



def test():
    "Test cases for the functions in poker program."
    sf1 = "6C 7C 8C 9C TC".split() # Straight Flush
    sf2 = "6D 7D 8D 9D TD".split() # Straight Flush
    fk = "9D 9H 9S 9C 7D".split() # Four of a Kind
    fh = "TD TC TH 7C 7D".split() # Full House
    assert poker([sf1, sf2, fk, fh]) == [sf1, sf2]
    assert (sorted(best_hand("6C 7C 8C 9C TC 5C JS".split()))
            == ['6C', '7C', '8C', '9C', 'TC'])
    assert (sorted(best_hand("TD TC TH 7C 7D 8C 8S".split()))
            == ['8C', '8S', 'TC', 'TD', 'TH'])
    assert (sorted(best_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    return 'test_best_hand passes'



print(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
print(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
print(40*"#")
