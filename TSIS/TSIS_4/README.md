for leaderboard in pg admin :
" SELECT p.username, g.score, g.level_reached, g.played_at
FROM game_sessions g
JOIN players p ON p.id = g.player_id
ORDER BY g.score DESC; "
controls : " F for grid toggle, M for sound toggle " 
