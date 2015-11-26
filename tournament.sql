-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE  TABLE players (
    id SERIAL PRIMARY KEY,
    name  varchar(30) DEFAULT NULL
);

CREATE  TABLE matches (
    match_id SERIAL PRIMARY KEY,
    winner INTEGER REFERENCES players (id),
    loser INTEGER REFERENCES players (id)
);

CREATE VIEW player_win AS
    SELECT id, count(matches.winner) as win from players left join matches on id=matches.winner group by players.id;

CREATE VIEW player_loss AS
    SELECT id, count(matches.loser) as loss from players left join matches on id=matches.loser group by players.id;
    
 CREATE VIEW match_total AS
    SELECT player_win.id as id, win + loss as total from player_win, player_loss where player_win.id = player_loss.id;
 
 CREATE VIEW standings AS
    SELECT players.id, name, win, total from players, player_win, match_total where players.id = player_win.id and players.id = match_total.id;
