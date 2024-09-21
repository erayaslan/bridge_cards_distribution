from collections import namedtuple, Counter
from random import shuffle
import matplotlib.pyplot as plt

Card = namedtuple("Card", ["rank", "suit"])


class Deck:
    ranks = [str(n) for n in range(2, 11)] + list("JQKA")
    suits = "spades hearts diamonds clubs".split()

    def __init__(self) -> None:
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def shuffle(self):
        shuffle(self._cards)

    def deal(self, n_players):
        self.hands = [self._cards[i::n_players] for i in range(0, n_players)]

        # high card points
        # A = 4
        # K = 3
        # Q = 2
        # J = 1
        c = [
            Counter([self.hands[i][j].rank for j in range(len(self.hands[i]))])
            for i in range(len(self.hands))
        ]
        self.hcps = [
            c[i]["J"] * 1 + c[i]["Q"] * 2 + c[i]["K"] * 3 + c[i]["A"] * 4
            for i in range(len(self.hands))
        ]
        assert sum(self.hcps) == 40


if __name__ == "__main__":
    points_dist = Counter()
    partners_dist = Counter()
    players = 4
    for i in range(10_000_000):
        d = Deck()
        d.shuffle()
        d.deal(players)
        points_dist += Counter(d.hcps)
        partners_dist += Counter([d.hcps[0] + d.hcps[2], d.hcps[1] + d.hcps[3]])

    print(points_dist)
    print(partners_dist)

    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True
    plt.bar(points_dist.keys(), points_dist.values())
    plt.savefig("points_4way_deal.png")

    plt.bar(partners_dist.keys(), partners_dist.values())
    plt.savefig("partners_total.png")


# Output:
# individual hands points distribution:
# Counter({10: 3761277, 9: 3746540, 11: 3575449, 8: 3557988, 7: 3213044, 12: 3209070, 13: 2765831, 6: 2620763, 14: 2276714, 5: 2075164, 15: 1769195, 4: 1535597, 16: 1325719, 3: 984867, 17: 944201, 18: 642410, 2: 542861, 19: 414781, 1: 315290, 20: 256501, 21: 151135, 0: 145666, 22: 83612, 23: 45113, 24: 22640, 25: 10704, 26: 4802, 27: 1962, 28: 744, 29: 258, 30: 74, 31: 21, 32: 5, 33: 1, 34: 1})
# partners total points distribution:
# Counter({20: 1647498, 19: 1610590, 21: 1610590, 22: 1514605, 18: 1514605, 23: 1364569, 17: 1364569, 24: 1180984, 16: 1180984, 25: 977948, 15: 977948, 26: 775807, 14: 775807, 27: 588646, 13: 588646, 12: 424621, 28: 424621, 29: 291942, 11: 291942, 30: 191169, 10: 191169, 9: 117912, 31: 117912, 8: 67863, 32: 67863, 7: 36981, 33: 36981, 6: 18666, 34: 18666, 35: 8509, 5: 8509, 4: 3575, 36: 3575, 37: 1325, 3: 1325, 38: 428, 2: 428, 1: 96, 39: 96, 40: 15, 0: 15})
