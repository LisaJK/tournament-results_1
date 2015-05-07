#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.

       Args: the database name tournament

       Returns a database connection and a cursor.
    """
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("Connection to database failed.")


def deleteMatches():
    """Remove all the match records from the database."""
    db, c = connect()
    query = "DELETE FROM matches"
    c.execute(query)
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, c = connect()
    query = "DELETE FROM players"
    c.execute(query)
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, c = connect()
    query = "SELECT COUNT(*) FROM players"
    c.execute(query)
    count = c.fetchone()[0]
    db.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db, c = connect()
    query = "INSERT INTO players (name) VALUES(%s)"
    cleansql = bleach.clean(query)
    c.execute(cleansql, (name,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains
        (id, name, wins, opponent match wins, matches).
        id: the player's unique id (assigned by the database),
        name: the player's full name (as registered),
        wins: the number of matches the player has won,
        opponent match wins: the total number of wins of all opponents,
        matches: the number of matches the player has played
    """
    db, c = connect()
    query = "SELECT * FROM player_standings"
    c.execute(query)
    rows = c.fetchall()
    db.close()
    return rows


def reportMatch(player1, player2, winner):
    """Records the outcome of a single match between two players.

    Args:
      player1: the id number of the first player
      player2: the id number of the second player (may be None if bye)
      winner:  the id number of the player who won (may be None if draw)
    """
    db, c = connect()
    query = """INSERT INTO matches(player_1, player_2, winner)
               VALUES(%s, %s, %s)"""
    c.execute(query, (player1, player2, winner))
    db.commit()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings. If an odd number is registered
    one player receives a bye. Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player
    adjacent to him or her in the standings.


    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
            id1: the first player's unique id,
            name1: the first player's name,
            id2: the second player's unique id,
            name2: the second player's name,
      Bye: id2 and name2 is None
    """
    standings = playerStandings()
    pairs = []
    if standings is None or len(standings) < 2:
        # check if another round has to be played
        print "Not enough player."
    elif standings[0][2] > standings[1][2]:
        print "Tournament finished. The winner is: "
        print str(standings[0][0]) + ", " + str(standings[0][1])

    # get all matches that have already been played
    else:
        db, c = connect()
        query = "SELECT * FROM matches"
        c.execute(query)
        matches = c.fetchall()
        db.close()
        paired_players = []
        # extra: odd number of players possible.
        # If odd number of players, the last player without a "bye" gets "bye"
        # which counts as a free win,
        # a match is added to the tournament: player1, None, player1
        if len(standings) % 2 == 1:
            # the last player without a 'bye' yet gets it
            for i in reversed(standings):
                for j in matches:
                    # check if the player already has a 'bye'
                    if j[0] == i[0] and j[1] is None:
                        continue
                    else:
                        break
                paired_players.append(i)
                pairs.append((i[0], i[1], None, None))
                break
        # pair each player with an opponent who has the same number of wins or
        # as close as possible
        # extra: draw is possible and counts 1/2 point
        for i in range(len(standings)):
            player1_id = standings[i][0]
            player1_name = standings[i][1]
            if standings[i] not in paired_players:
                for j in range(i + 1, len(standings)):
                    if standings[j] in paired_players:
                        continue
                    player2_id = standings[j][0]
                    player2_name = standings[j][1]
                    # check if the players have already played against each
                    # other
                    not_played_yet = True
                    for x in matches:
                        check1 = x[1] == player1_id and x[2] == player2_id
                        check2 = x[1] == player2_id and x[2] == player1_id
                        if (check1 or check2):
                            not_played_yet = False
                            break
                    if not_played_yet:
                        paired_players.append(standings[i])
                        paired_players.append(standings[j])
                        pair = (player1_id,
                                player1_name,
                                player2_id,
                                player2_name)
                        pairs.append(pair)
                        break
    return pairs
