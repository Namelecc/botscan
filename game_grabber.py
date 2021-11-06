import requests as req
import json
import statistics as stat
def scan(a, b, c, d):
    
    username = a.casefold()
    move_minimums = 10
    variant = b
    variants = {"ultraBullet", "bullet", "blitz", "rapid", "classical", "correspondence", "chess960", "crazyhouse", "antichess", "atomic", "horde", "kingOfTheHill", "racingKings", "threeCheck"}
    standard = {"ultraBullet", "bullet", "blitz", "rapid", "classical"}
    if variant not in variants:
        raise ValueError("Not a possible input")
    speed = c
    if variant in standard:
        speed = variant
    if speed not in standard:
       raise ValueError("Not a possible input") 
    min_opponent = 0
    try:
        min_opponent = int(d)
    except:
        pass


    url = f"https://lichess.org/api/games/user/{username}"
    request = req.get(
        url,
        params={"rated":"true", "perfType":variant, "analysed":"true", "pgnInJson":"true", "clocks":"true","evals":"True"},
        # "max":1000, 
        headers={"Accept": "application/x-ndjson"}
    )
    stuff = request.iter_lines()
    coefficient = []
    games = []

    for x in stuff:
        game = json.loads(x)
        try:
            if game['speed'] == speed:
                initial = game['clock']['initial']
                increment = game['clock']['increment']
                #__________________________
                berserk = False
                #__________________________
                player_color = ""
                opponent_color = ""
                if game['players']['white']['user']['id'] == username.casefold():
                    player_color = "white"
                    opponent_color = "black"

                else:
                    player_color = "black"
                    opponent_color = "white"
                if game['players'][opponent_color]['rating'] >= min_opponent:
                    acpl = game["players"][player_color]["analysis"]["acpl"]
                    if acpl < 5:
                        acpl = 5 #Because in variants such as rk, 0 acpl basically negates the effect of standard dev
                    #__________________________

                    pgn = game["pgn"]
                    clock = []
                    clock_reader = []
                    pgn = pgn.split("[")
                    for y in pgn:
                        if "clk" in y:            
                            clock.append(y[6:12].strip(":"))
                    for x in range(0, len(clock)):
                        if player_color == "white":
                            if x % 2 == 0:
                                clock_reader.append(clock[x])
                        else:
                            if x % 2 == 1:
                                clock_reader.append(clock[x])
                    move_times = []
                    for x in range(0, len(clock_reader)):
                        y = clock_reader[x].split(":")
                        seconds = int(y[0]) * 60 + int(y[1]) 
                        clock_reader[x] = seconds
                    if clock_reader[0] != initial and initial != 0:
                        berserk = True
                    if berserk == False:
                        clock_reader.insert(0, initial)
                        for x in range(1, len(clock_reader)):
                            move_times.append(clock_reader[x-1] - clock_reader[x] + increment)
                        if len(move_times) >= move_minimums:
                            stdev = stat.stdev(move_times)
                            acpl_dev = acpl * stdev / (game["clock"]["totalTime"])
                            coefficient.append(acpl_dev)
                            games.append(game["id"])
                    else: 
                        clock_reader.insert(0, initial/2)
                        for x in range(1, len(clock_reader)):
                            move_times.append(clock_reader[x-1] - clock_reader[x])
                        if len(move_times) >= move_minimums:
                            stdev = stat.stdev(move_times)
                            acpl_dev = acpl * stdev / (initial/2)
                            coefficient.append(acpl_dev)
                            games.append(game["id"])
        except:
            pass
    for repetition in range(len(games)):
        for x in range(len(games)):
            first = coefficient[repetition]
            if coefficient[x] > first: 
                coefficient[repetition] = coefficient[x]
                coefficient[x] = first
                first_game = games[repetition]
                games[repetition] = games[x]
                games[x] = first_game
    final_games = []
    final_coefficient = []
    for x in range(0, 30):
        try:
            final_games.append(games[x])
            final_coefficient.append(coefficient[x])
        except:
            pass
    return (final_games, final_coefficient)

