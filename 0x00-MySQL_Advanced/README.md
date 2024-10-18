# 0x00-MySQL_Advanced
Advanced MySQL

## 0-uniq_users.sql
Make a table with all columns capable of holding only unique values

## 1-country_users.sql
A table with an enum column

## 2-fans.sql
SQL script that ranks country origins of bands, ordered by the number of (non-unique) fans

## 3-glam_rock.sql
SQL script that lists all bands with Glam rock as their main style, ranked by their longevity

## 4-store.sql
creates a trigger that decreases the quantity of an item after adding a new order

## 5-valid_email.sql
creates a trigger that resets the attribute valid_email only when the email has been changed

## 6-bonus.sql
creates a stored procedure AddBonus that adds a new correction for a student

## 7-average_score.sql
creates a stored procedure ComputeAverageScoreForUser that computes and store the average score for a student

## 8-index_my_names.sql
script that creates an index idx_name_first on the table names and the first letter of name

## 9-index_name_score.sql
creates an index idx_name_first_score on the table names and the first letter of name and the score

## 10-div.sql
creates a function SafeDiv that divides (and returns) the first by the second number or returns 0 if the second number is equal to 0

## 11-need_meeting.sql
creates a view need_meeting that lists all students that have a score under 80 (strict) and no last_meeting or more than 1 month