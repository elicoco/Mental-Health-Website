green = "#81C784";
red = "#E57373";
orange ="#FFB74D";

const months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
];

const dailyTrackersJson = document.getElementById('daily-trackers').value;
const dailyTrackers = JSON.parse(dailyTrackersJson);

function generateCalendar(year, month){
    const trackersForMonth = [];
    const trackerDays = [];

    for (let i = 0; i < dailyTrackers.length; i++){
        const tracker = dailyTrackers[i];
        const trackerDate = tracker.date;
        if (trackerDate.slice(0,4) == year && trackerDate.slice(5,7) == month+1){
            trackersForMonth.push(tracker);
            trackerDays.push(parseInt(trackerDate.slice(8,10), 10));
        }
    }

    document.getElementById("month-year").innerHTML = `${months[month]} ${year}`;
    document.getElementById("daysContainer").innerHTML = "";

    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const startDay = new Date(year, month, 1).getDay();
    const targetDiv = document.getElementById("daysContainer");

    for (let j = 1; j <= startDay; j++){
        const blankDiv = document.createElement("div");
        blankDiv.classList.add("day.blank");
        targetDiv.appendChild(blankDiv);
    }

    const todayDate = new Date();
    todayDate.setHours(0, 0, 0, 0);

    for (let i = 1; i <= daysInMonth; i++){
        const dayDiv = document.createElement("div");
        dayDiv.textContent = i;
        dayDiv.classList.add("day");

        const thisDate = new Date(year, month, i);
        const isFuture = thisDate > todayDate;

        if (trackerDays.includes(i)){
            dayDiv.addEventListener("click", function() {
                handleDayClick(i, month+1, year);
            });
            dayDiv.classList.add("tracker-day");

            const trackerIndex = trackerDays.indexOf(i);
            const moodScore = trackersForMonth[trackerIndex].mood_score;

            if (moodScore >= 67){
                dayDiv.style.backgroundColor = green;
            } else if (moodScore >= 34){
                dayDiv.style.backgroundColor = orange;
            } else {
                dayDiv.style.backgroundColor = red;
            }
        } else if (!isFuture) {
            dayDiv.addEventListener("click", function() {
                handleDayClick(i, month+1, year);
            });
            dayDiv.classList.add("empty-day");
        } else {
            dayDiv.classList.add("future-day");
        }
        targetDiv.appendChild(dayDiv);
    }
}

function handleDayClick(day, month, year){
    const dayStr = day.toString().padStart(2, "0");
    const monthStr = month.toString().padStart(2, "0");
    const yearStr = year.toString();
    const date = `${yearStr}-${monthStr}-${dayStr}`;
    window.location.href = `/day/${date}`;
}

const today = new Date();
let currentYear = today.getFullYear();
let currentMonth = today.getMonth();
generateCalendar(currentYear, currentMonth);

function prevMonth() {
    currentMonth--;
    if (currentMonth < 0) {
        currentMonth = 11;
        currentYear--;
    }
    generateCalendar(currentYear, currentMonth);
}

function nextMonth() {
    currentMonth++;
    if (currentMonth > 11) {
        currentMonth = 0;
        currentYear++;
    }
    generateCalendar(currentYear, currentMonth);
}
