#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2, random, math
VERBOSE = True


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM MATCHES")
    conn.commit() 
    if VERBOSE:
        print "all match records are deleted!"
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM PLAYERS")
    conn.commit()
    if VERBOSE:
        print "all player records are deleted!"
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM PLAYERS")
    for row in c:
        count = row[0]
    conn.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO PLAYERS (name) VALUES (%s)", (name,))
    conn.commit() 
    if VERBOSE:
        print "Player %s has been added" % name
    conn.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM standings ORDER BY win DESC")
    result =  c.fetchall()
    conn.close()
    if VERBOSE:
        print"---------------------------------"
        print "id | Name | Win | Loss"
        print"---------------------------------"
        for row in result:
            print row[0], row[1], row[2], row[3] 
    print "\n"
    return result

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO matches (winner, loser) VALUES (%s, %s)", (winner, loser,))
    conn.commit()
    if VERBOSE:
        print "Player %s wins a match with player %s" % (winner, loser)
    conn.close()
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    result=[]
    for i in range(0,len(standings),2):
        result.append(standings[i][0:2]+standings[i+1][0:2])
    return result
    
def truncateTables():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("TRUNCATE MATCHES, PLAYERS RESTART IDENTITY")
    conn.commit()
    if VERBOSE:
        print "tabe matches, players are trancated\n"
    conn.close()
    
def randomTournament():
    return 0

def registerPlayers(players):
    for player in players:
        registerPlayer(player)
        
def newPairings():
    standings = playerStandings()
    result=[]
    while (len(standings) > 0):
        i=0
        a = standings[i]
        standings.pop(i)
        b = standings[i]
        while (dupeyes(a,b)):
            i = i + 1
            b = standings[i]
        standings.pop(i)
        result.append(a[0:2]+b[0:2])
    return result

def dupeyes(a,b):
    conn = connect()
    c = conn.cursor()
    c.execute("select * from matches where (winner = %s and loser = %s) or (winner = %s and loser = %s)",(a[0],b[0],b[0],a[0]))
    conn.commit()
    conn.close()
    if c.rowcount == 0:
        return 0
    else:
        print "*** Player %s had previous match with %s ***" % (a[0], b[0])
        return 1
        
        