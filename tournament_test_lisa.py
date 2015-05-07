from tournament import *
import random
import os

# you can change the test by changing the number of players
# (e.g. to an odd number or even number)
the_players = ['Donald', 'Daisy', 'April', 'May', 'June',
               'Huey', 'Dewey', 'Louie', 'Scrooge']
# if set to True draws are possible
draw_possible = True


def test():
    """tests the implemented swiss pairing
       and prints for each round the player standings and
       the next pairings.
    """
    # drop and create tables and views in database tournament
    dropAndCreateDB()

    # register the players
    for player in the_players:
        registerPlayer(player)

    # count the players
    count = countPlayers()
    print 'Count: ' + str(count)
    if count != len(the_players):
        print 'Players have not been registered correctly!'

    round = 1
    pairs = swissPairings()

    while pairs:
        printPlayerStandings(round)
        print '\nRound: ' + str(round)
        round = round + 1
        pairs = swissPairings()
        for pair in pairs:
            print pair
            reportRandomMatchResult(pair[0], pair[2])


def reportRandomMatchResult(player1, player2):
    """ reports matches for player1 and player2
        If player2 is None, the match is a bye.
        If draws are possible, winner may be None,
        player1 or player2, otherwise player1 or player2.
        The winner is chosen randomly.

        Args: player1 the id of the first player,
              player2 the id of the second player
    """
    # check bye (player1 gets free win)
    if player2 is None:
        reportMatch(player1, None, player1)
    else:
        # either one of the players is the winner or it is a draw
        if draw_possible:
            players = [player1, player2, None]
            reportMatch(player1, player2, random.choice(players))
        else:
            players = [player1, player2]
            reportMatch(player1, player2, random.choice(players))


def printPlayerStandings(round):
    """ Prints the player standings """
    player_standings = playerStandings()
    print '\nPlayer Standings before round ' + str(round)
    print 'Player Id, Player Name, Points, Opponent Match Wins, Matches'
    for player in player_standings:
        print player


def dropAndCreateDB():
    """ drops and creates the tables and views of the database
        tournament by executing an sql script
    """

    # get the relative path to the sql script
    dir = os.path.dirname(__file__)
    scriptPath = os.path.join(dir, 'tournament_lisa.sql')

    # read the file
    fd = open(scriptPath, 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    db, c = connect()

    # Execute every command from the input file
    for command in sqlCommands:
        # do not execute empty queries
        strippedCommand = command.strip()
        if strippedCommand:
            # skip over drop commands if nothing to drop
            try:
                c.execute(strippedCommand)
            except Exception, msg:
                print 'Command skipped: ', msg
    db.commit()
    db.close()
    print "SQL script was executed successfully."

if __name__ == '__main__':
    test()
