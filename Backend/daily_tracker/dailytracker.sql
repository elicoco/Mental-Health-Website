FROM dailytracker SELECT mood.mood_score, data.amount
INNER JOIN mood ON dailytracker.id == mood.day_id
INNER JOIN data ON dailytracker.id == data.day_id
WHERE dailytracker.date >= DATE_SUB(CURDATE(), INTERVAL amount_of_days DAY) 
and data.type = type_of_data -- only gets data from one type

