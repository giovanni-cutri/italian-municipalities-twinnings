SELECT first_name, count(first_name) FROM "twinnings"
GROUP BY first_name
ORDER BY count(first_name) DESC
