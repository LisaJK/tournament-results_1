-- Table definitions for the tournament project.

-- drop the tables if they already exist
DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS matches;

-- table containing the players
CREATE TABLE players
(
	id SERIAL UNIQUE PRIMARY KEY, 
	name VARCHAR(90)
);

-- table containing the matches
CREATE TABLE matches
(
   id SERIAL UNIQUE PRIMARY KEY,
   player_1 INTEGER REFERENCES players(id) NOT NULL,
   player_2 INTEGER REFERENCES players(id),
   winner INTEGER REFERENCES players(id)
);

-- view: How many matches has each player played?
CREATE VIEW played_matches AS 
(
	SELECT players.id AS player_id, players.name AS player_name, COUNT(matches.id) AS played
		FROM players LEFT JOIN matches ON players.id = player_1 OR players.id = player_2
		GROUP BY players.id
		ORDER BY played DESC, players.id ASC
);

-- view: How often has each player won?
CREATE VIEW won_matches AS 
(
	SELECT wins.player_id AS player_id, wins.player_name AS player_name, win_points + draw_points AS points FROM
	(SELECT players.id AS player_id, players.name AS player_name, COUNT(matches.id) AS win_points
		FROM players LEFT JOIN matches ON players.id = matches.winner 
		GROUP BY players.id 
		ORDER BY win_points DESC, players.id ASC) AS wins, 
	(SELECT players.id AS player_id, players.name AS player_name, 0.5 * COUNT(matches.id) AS draw_points
		FROM players LEFT JOIN matches ON ((players.id = matches.player_1 OR players.id = matches.player_2) AND matches.winner IS NULL)
		GROUP BY players.id 
		ORDER BY draw_points DESC, players.id ASC) AS draws
	WHERE wins.player_id = draws.player_id
);

-- view: Total number of wins of the opponents
CREATE VIEW opponent_match_wins AS
(
	SELECT p.id AS player_id, SUM(wm.points) AS omw FROM players p LEFT JOIN won_matches wm 
		ON wm.player_id IN 
		((SELECT player_2 FROM matches WHERE player_1 = p.id AND wm.player_id = player_2) 
			UNION 
	 	(SELECT player_1 FROM matches WHERE player_2 = p.id AND wm.player_id = player_1))
		GROUP BY p.id
		ORDER BY p.id ASC
);

-- view: Player standings
CREATE VIEW player_standings (player_id, name, points, omw, matches) AS
(
	SELECT played_matches.player_id, played_matches.player_name, won_matches.points, opponent_match_wins.omw, played_matches.played 
		FROM played_matches, won_matches, opponent_match_wins 
		WHERE played_matches.player_id = won_matches.player_id AND won_matches.player_id = opponent_match_wins.player_id
		ORDER BY won_matches.points DESC, opponent_match_wins.omw DESC, played_matches.played DESC, played_matches.player_id ASC
);

