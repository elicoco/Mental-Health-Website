const months = [
    "January", "February", "March", "April", "May", "June", 
    "July", "August", "September", "October", "November", "December"
  ];
// Function to generate calendar
function generateCalendar(year, month){
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
        // add a function to each day of the calendar
        newDiv.addEventListener("click", function() {
            handleDayClick(i, month+1, year);
        });
        targetDiv.appendChild(newDiv);
    }
}

// function which runs when a day is clicked
function handleDayClick(day, month, year){
    console.log(`${day} ${month} ${year}`)
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

