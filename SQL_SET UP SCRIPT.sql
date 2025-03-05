ALTER TABLE rolling_averages 
DROP CONSTRAINT rolling_averages_player_id_fkey,
ADD CONSTRAINT rolling_averages_player_id_fkey 
FOREIGN KEY (player_id) REFERENCES player_stats(player_id) ON DELETE CASCADE;

ALTER TABLE shooting_trends 
DROP CONSTRAINT shooting_trends_player_id_fkey,
ADD CONSTRAINT shooting_trends_player_id_fkey 
FOREIGN KEY (player_id) REFERENCES player_stats(player_id) ON DELETE CASCADE;

ALTER TABLE injuries 
DROP CONSTRAINT injuries_player_id_fkey,
ADD CONSTRAINT injuries_player_id_fkey 
FOREIGN KEY (player_id) REFERENCES player_stats(player_id) ON DELETE CASCADE;

-- Drop and recreate the view properly
DROP VIEW IF EXISTS active_players;
CREATE VIEW active_players AS
SELECT * FROM player_stats
WHERE player_id NOT IN (
    SELECT player_id FROM injuries 
    WHERE CURRENT_DATE BETWEEN injury_start AND injury_end
);

-- Fix ev_analysis view
DROP VIEW IF EXISTS ev_analysis;
CREATE VIEW ev_analysis AS
SELECT 
    o.game_date, o.player_id, o.prop_type, o.line, 
    p.predicted_value, 
    (p.predicted_value - o.line) AS edge
FROM odds o
JOIN predictions p 
ON o.player_id = p.player_id 
AND o.game_date = p.game_date;

-- Fix rolling averages function
CREATE OR REPLACE FUNCTION update_rolling_averages()
RETURNS void AS $$
BEGIN
    DELETE FROM rolling_averages WHERE game_date = CURRENT_DATE;
    INSERT INTO rolling_averages (
        player_id, game_date, last5_avg_points, last10_avg_assists, last5_avg_rebounds
    )
    SELECT 
        player_id, game_date,
        AVG(points) OVER (PARTITION BY player_id ORDER BY game_date ROWS BETWEEN 4 PRECEDING AND CURRENT ROW),
        AVG(assists) OVER (PARTITION BY player_id ORDER BY game_date ROWS BETWEEN 9 PRECEDING AND CURRENT ROW),
        AVG(rebounds) OVER (PARTITION BY player_id ORDER BY game_date ROWS BETWEEN 4 PRECEDING AND CURRENT ROW)
    FROM player_stats;
END;
$$ LANGUAGE plpgsql;
