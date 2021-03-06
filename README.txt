PROJECT Tournament Results - Version 1 - May 2015
------------------------------------------------------------------------------


PROJECT DESCRIPTION
------------------------------------------------------------------------------
In this project, a Python module that uses the PostgreSQL database can be used 
to keep track of players and matches in a game tournament.

The game tournament will use the Swiss system for pairing up players in each 
round: players are not eliminated, and each player should be paired with 
another player with the same number of wins, or as close as possible.
------------------------------------------------------------------------------


DOWNLOAD
------------------------------------------------------------------------------

The project files are on GitHub: 
https://github.com/LisaJK/tournament-results.git

Use, e.g., Git to clone them:
$ git clone https://github.com/LisaJK/tournament-results.git
------------------------------------------------------------------------------


INSTALLATION REQUIREMENTS
------------------------------------------------------------------------------
To run the project, Python, PostgreSQL database and psycopg2 language binding 
must be installed on your system.
------------------------------------------------------------------------------


DESCRIPTION OF THE PROJECT FILES
------------------------------------------------------------------------------

1. README.txt
   This file (hopefully containing all necessary information to download and
   run the project, otherwise please contact: lisa.kugler@googlemail.com). 

2. tournament.py
   This python file contains the implementation of the Swiss-system 
   tournament.
   For details see documentation file generated by Pycco in folder docs.

2. tournament_lisa.sql
   This file contains all SQL statements which are necessary to create the 
   tables and views of the database tournament:
   - table players
   - table matches
   - view played_matches
   - view won_matches
   - view opponent_match_wins
   - view player_standings

   If the tables and views have been existing before, they are dropped before 
   they are recreated.

3. tournament_test.py
   This python file contains the (slightly changed, to enable draws) testcases 
   of tournament.py provided by Udacity. 
   For details see documentation file generated by Pycco in folder docs.

4. tournament_test_lisa.py
   This python file contains more testcases, especially to test the extra 
   credits (draw matches, odd number of players and the integration of opponent 
   match wins to the player standings). 
   For details see documentation file generated by Pycco in folder docs.

5. A folder docs containing a documentation file for each python file
   generated by Pycco.
------------------------------------------------------------------------------


INSTRUCTIONS TO EXECUTE THE TEST FILES
------------------------------------------------------------------------------

A. Execute tournament_test.py provided by Udacity
   1. Open bash and change to the folder the project files are in
      (e.g. .../vagrant/tournament)
   2. create a database named tournament 
      (drop the old database tournament if necessary)
      - type in bash: 
               $ dropdb --if-exists tournament; 
      - type in bash:
			   $ createdb tournament;
   3. execute the script tournament_lisa.sql
      - type in bash:
      		   $ psql tournament -f tournament_lisa.sql
   4. run tournament_test.py
      - type in bash:
               $ python tournament_test.py


B. Execute tournament_test_lisa.py added to test the extra credits
   1. Open bash and change to the folder the project files are in
      (e.g. .../vagrant/tournament)
   2. create a database named tournament
      (drop the old database tournament if necessary)
      - type in bash: 
               $ dropdb --if-exists tournament; 
      - type in bash:
			   $ createdb tournament;
   3. run tournament_test_lisa.py
      - type in bash:
               $ python tournament_test_lisa.py
   Please note: The script tournament_lisa.sql is executed within the execution
                of the python file. Make sure it is placed in the same folder
                as tournament_test_lisa.py.
------------------------------------------------------------------------------


IMPLEMENTED EXTRA CREDITS
------------------------------------------------------------------------------

The following extra credits are implemented:

1. Draw is possible
   Implementation: Draw counts as 1/2 point, if a match is reported and no 
   winner is given, both players get 1/2 point.

2. Odd number of players is possible
   Implementation: The last player in the player standings not having a "bye" 
   yet gets a free win. 
   A match is reported with only one player, who is also the winner.

3. Opponent Match Win
   Implementation: The player standings are extended and have one extra field 
   containing the total number of wins of all opponents of the player.

The player standings therefore consider:

- points (win points + draw points)
- opponent match wins
- played matches
- player id

For further details please see the documentation files generated by Pycco.
------------------------------------------------------------------------------

CONTACT 
------------------------------------------------------------------------------
lisa.kugler@googlemail.com
