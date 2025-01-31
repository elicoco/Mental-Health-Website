green = "#81C784";
red = "#E57373";
orange ="#FFB74D";

const months = [
    "January", "February", "March", "April", "May", "June", 
    "July", "August", "September", "October", "November", "December"
  ];

const daily_trackersjson = document.getElementById('daily-trackers').value;
const daily_trackers = JSON.parse(daily_trackersjson);
console.log(daily_trackers)
// Function to generate calendar
function generateCalendar(year, month){
    let trackers_for_month = []
    let trackers_day = []
    // loop through daily trackers
    for (trackers in daily_trackers){
        curtracker = daily_trackers[trackers]
        curdate = curtracker.date
        // gets daily trackers for the days in the month
        if (curdate.slice(0,4) == year && curdate.slice(5,7) == month+1){
            trackers_for_month.push(curtracker)
            trackers_day.push(parseInt(curdate.slice(8,10), 10))
        }
    }
    console.log(trackers_day)
    // the month and year are displayed as the title
    document.getElementById("month-year").innerHTML = `${months[month]} ${year}`;
    // clear the calendar
    document.getElementById("daysContainer").innerHTML = "";
    // get days in month
    amountofdays = new Date(year, month + 1, 0).getDate();
    // finds day the month starts on
    startday = new Date(year, month, 1).getDay();
    // finds div I want to enter it into
    let targetDiv = document.getElementById("daysContainer");
    for (let j = 1; j <= startday; j++){ // loops through amount of days
        // to make the calendar start on the normal start day
        let newDiv = document.createElement("div");
        // creates new div
        newDiv.classList.add("day.blank");
        // adds blank class to it
        targetDiv.appendChild(newDiv);
    }
    for (let i = 1; i <= amountofdays; i++){ // loops through every day
        // of the month
        let newDiv = document.createElement("div");
        // creates new div
        newDiv.textContent = i;
        newDiv.classList.add("day");
        if (trackers_day.includes(i)){
            // add a function to each day of the calendar
            // which has a daily tracker
            newDiv.addEventListener("click", function() {
                handleDayClick(i, month+1, year);
            });
            newDiv.classList.add("tracker-day");
            const index_list = trackers_day.indexOf(i)
            const mood = trackers_for_month[index_list].mood_score
            // colour styling based on mood score
            if (mood >= 67){
                newDiv.style.backgroundColor = green;
            }
            else if (mood >= 34){
                newDiv.style.backgroundColor = orange;
            }
            else{
                newDiv.style.backgroundColor = red;
            }
        }
        targetDiv.appendChild(newDiv);
    }
}

// function which runs when a day is clicked
function handleDayClick(day, month, year){
    // turns day and month into 2 digit string
    const day1 = day.toString().padStart(2, "0")
    const month1 = month.toString().padStart(2, "0")
    const year1 = year.toString()
    // overall date formatted for SQL
    const date = `${year1}-${month1}-${day1}`
    window.location.href = `http://127.0.0.1:5000/day/${date}`;
}

// Load current month and year
const today = new Date();
let currentYear = today.getFullYear();
let currentMonth = today.getMonth();
generateCalendar(currentYear, currentMonth)

function prevMonth() {
    // makes the month one less
    currentMonth--;
    if (currentMonth < 0) {
        // if its less than 0 then
        // move the year back by 1
        currentMonth = 11;
        currentYear--;
    }
    generateCalendar(currentYear, currentMonth);
}

function nextMonth() {
    currentMonth++;
    if (currentMonth > 11) {
        // if its grater than 0 then
        // move the year forward by 1
        currentMonth = 0;
        currentYear++;
    }
    generateCalendar(currentYear, currentMonth);
}

