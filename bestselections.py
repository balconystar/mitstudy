
import pylab
import itertools
import math
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="A simple greeting script.")
parser.add_argument("-p", "--path", type=str, help="Path to take the matchday results from")
parser.add_argument("-s", type=int, help="Maximum number of selections for each betslip", default=1)
parser.add_argument("--mdstart", type=int, help="What matchday to start calculating form", default=1)
parser.add_argument("--mdend", type=int, help="What matchday to end calculating form", default=-1)
parser.add_argument("-b", type=int, help="The banker odds to apply to each slip", default=1 )


args = parser.parse_args()


collection_of_results = []

output_tuples = []

booster = args.b

max_selections = args.s

matchday_start = args.mdstart

matchday_end = args.mdend

path = args.path

markets = ["draw", "handicap(0:1) win", "u2.5gg", "handicap(0:1) draw", 
"handicap(0:2) win", "handicap(0:2) draw", "handicap(1:0) draw"  ]



results = {}


class House():

    def __init__(self, data, markets):
        self.data = data
        self.markets = markets
        self.matchday = 0

    def setMatchday(self, matchday):
        self.matchday = matchday

    def assess(self, betslip):
        selections = len(betslip) - 2
        is_won = True

        if self.markets[betslip[0]] == "handicap(1:0) draw":
            for i in range(selections):

                home_score, away_score = map(
                    int, self.data[self.matchday][betslip[i + 2]].split())
                if (home_score + 1) != away_score: is_won = False

        if self.markets[betslip[0]] == "draw":
            for i in range(selections):
                home_score, away_score = map(
                    int, self.data[self.matchday][betslip[i+2]].split())

                if not home_score == away_score: is_won = False
        if self.markets[betslip[0]] == "handicap(0:1) win":
            for i in range(selections):

                home_score, away_score = map(
                    int, self.data[self.matchday][betslip[i + 2]].split())
                if not (home_score) > (away_score + 1): is_won = False

        if self.markets[betslip[0]] == "handicap(1:0) draw":
            for i in range(selections):

                home_score, away_score = map(
                    int, self.data[self.matchday][betslip[i + 2]].split())
                if not (home_score + 1) == (away_score): is_won = False        

        if self.markets[betslip[0]] == "handicap(0:2) win":
            for i in range(selections):

                home_score, away_score = map(
                    int, self.data[self.matchday][betslip[i + 2]].split())
                if not (home_score) > (away_score + 2): is_won = False        

        if self.markets[betslip[0]] == "u2.5gg":
            for i in range(selections):

                home_score, away_score = map(
                    int, self.data[self.matchday][betslip[i + 2]].split())
                if not (home_score == 1 and away_score == 1): is_won = False

        if self.markets[betslip[0]] == "handicap(0:1) draw":
            for i in range(selections):

                home_score, away_score = map(
                    int, self.data[self.matchday][betslip[i + 2]].split())
                if not home_score == away_score + 1: is_won = False

        if self.markets[betslip[0]] == "handicap(0:2) draw":
            for i in range(selections):

                home_score, away_score = map(
                    int, self.data[self.matchday][betslip[i + 2]].split())
                if not home_score == away_score + 2: is_won = False        

        if is_won == True:
            return (is_won, betslip[1]**selections)

        if is_won == False:
            return (is_won, -1)


def import_data(path):
    data = []

    scores = []
    with open(path, "r", encoding="utf-8") as file:
        for line in file:

            if not line.strip():
                continue

            if line.rstrip("\n") == "eom":
                data.append(scores)
                scores = []
                continue

            scores.append(line.rstrip("\n"))

    return data


def simulation(path):

    # data = ["2 1","3 0","4 1","2 2"," 3 3", "1 1", "0 1", "0 2"]
    data = import_data(path)

    house = House(data, markets)

    odds = {
        markets[0]: np.arange(3.3*booster, 3.6*booster, 0.1*booster),
        markets[1]: np.arange(3.0 * booster,3.6 * booster, 0.1*booster),
        markets[2]: np.arange(7*booster, 7.3*booster, 0.1*booster),
        markets[3]: np.arange(3.5*booster,4.2*booster,0.1*booster),
        markets[4]: np.arange(5*booster,6.1*booster,0.1*booster),
        markets[5]: np.arange(4.7*booster, 5.4* booster, 0.1* booster),
        markets[6]: np.arange(4.4*booster,5.8*booster,0.1*booster),


    }

    betslip = [0, 0]


    if(matchday_start < 1):
        print("Invalid matchday parameters")
        exit()

    data_length = len(data)

    global matchday_end
    if(data_length < matchday_end):
        print("The data doesn't reach ", matchday_end, " matchdays")
        print("Using the maximum matchdays provided in the data")    
        matchday_end = data_length

    if(matchday_end == -1):
        matchday_end = data_length
    #for h in range(len(data)):
        
    for h in range(matchday_start-1,matchday_end):
        house.setMatchday(h)
        for i in range(len(markets)):
            betslip[0] = i
            for j in odds.get(markets[i]):
                betslip[1] = j
                for k in range(max_selections):
                    possible_combinations = generate_custom_combinations(
                        k+1, len(data[h]))
                    combination_number = 0
                    for l in range(len(possible_combinations)):
                        for m in range(len(possible_combinations[l])):
                            betslip.append(possible_combinations[l][m]-1)

                        result = house.assess(betslip)

                        key = str(i) + " : " + str(round(j, 1)) + \
                                  " : " + str(k+1)

                        try:
                            results[key][0] += result[-1]
                            if result[0] == True:
                                results[key][1] += 1
                            else:
                                results[key][2] += 1

                        except (KeyError):
                            results[key] = [0, 0, 0]

                            results[key][0] = result[-1]
                            if result[0] == True:
                                results[key][1] += 1
                            else:
                                results[key][2] += 1

                        # if key == "0 : 4.0 : 5" and h > 1 and h < 3:
                        #     roi = unitToYield(results[key][0],results[key][1],results[key][2])
                        #     print(results[key][0]," " ,results[key][1]," " , results[key][2], " roi ", roi)
                        #     combination_number = combination_number + 1
                        #     print("Combination number: ", combination_number, "Matchday: ", h+1)
                        betslip = [i, j]

        #print("Matchday: ", h)
        collection_of_results.append(results.copy())
        # results.clear()
    report()


def unitToYield(unit, winCount, looseCount):
    profit = unit - winCount
    roi = (profit / (winCount + looseCount)) * 100
    return roi


def report():

    for j in range(len(collection_of_results)):

        for i in collection_of_results[j].keys():
            result_tuple = results.get(i)

            result_tuple[0] = unitToYield(result_tuple[0], result_tuple[1], result_tuple[2])
            
            global output_tuples        

            output_tuples.append((i,j,result_tuple[0]))
       
    
    output_tuples = sorted(output_tuples, key=lambda x: (-x[2]))    

    
    for i in range(len(output_tuples)):
        if(i > 20):
            break
        print(tupleToString(output_tuples[i][0]) , " Yield: ", output_tuples[i][2])
        
    
def tupleToString(input):
    result = [float(num) for num in input.split(":")]
    return markets[int(result[0])] + " " + str(result[1]) + " odds " + str(int(result[2])) + " selections"


def report_market(market, matchday=37):
    for i in range(len(output_tuples)):
        if(market == output_tuples[i][0] and matchday == output_tuples[i][1]):
            print(tupleToString(market), " Yield: ", output_tuples[i][2])   
            break

def generate_custom_combinations(r, n_max):
    pool = list(range(1, n_max +1))

    combos = list(itertools.combinations(pool, r))    

    return combos



simulation(path)

       

