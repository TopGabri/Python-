from pprint import pprint
import csv

PLAYERS = "PLAYERS.txt"
SCORES = "SCORES.txt"

def getPlayers(filename):
    players = dict()
    try:
        with open(filename, newline='') as input_file:
            for d in csv.DictReader(input_file):
                name = d.pop("PLAYER")
                players[name] = int(d["SELO"])
    except OSError as error:
        print(f"Something went wrong: {error}")
        exit(1)

    pprint(players)
    return players

def getScores(filename):
    scores = dict()
    try:
        with open(filename, newline='') as input_file:
            for d in csv.DictReader(input_file):
                players = d.pop("PLAYER A"), d.pop("PLAYER B")
                scores[players] = d["RESULT"].split('-')
    except OSError as error:
        print(f"Something went wrong: {error}")
        exit(1)
    pprint(scores)
    return scores

def uptadePlayers(players, scores):
    players_copy = dict(players)
    for match in scores:
        winner = ""
        loser = ""
        winner_selo = 0
        loser_selo = 0
        tie = False
        for player in range(2):
            if scores[match][player] == "1":
                if match[player] not in players_copy:
                    players_copy[match[player]] = 1_500
                winner = match[player]
                winner_selo = players_copy[match[player]]
            elif scores[match][player] == "0":
                if match[player] not in players:
                    players_copy[match[player]] = 1_500
                loser = match[player]
                loser_selo = players_copy[match[player]]
            else:
                tie = True
        if not tie:
            increase = delta(winner_selo, loser_selo)
            players_copy[winner] += round(200 * increase, 0)
            players_copy[loser] -= round(200 * increase, 0)

    return players_copy


def delta(winner, loser):
    return 1 / (1 + 2**((winner-loser) / 100))


def main():
    players = getPlayers(PLAYERS)
    scores = getScores(SCORES)
    update = uptadePlayers(players, scores)
    update_sorted = sorted(update, key=lambda x: update[x], reverse=True)
    for player in update_sorted:
        print(f"{player}: {update[player]:.0f}")



if __name__ == "__main__":
    main()