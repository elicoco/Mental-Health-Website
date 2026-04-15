green = "#4CAF50";
red = "#F44336";
blue = "#2196F3";
orange ="#FFBF00";

const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

const wakeupTime = document.getElementById('wakeup-time').value;
const hour24 = Math.floor(wakeupTime);
const minute = Math.round((wakeupTime - hour24) * 60);
const period = hour24 >= 12 ? "PM" : "AM";
const hour12 = hour24 % 12 || 12;
const formattedMinute = minute.toString().padStart(2, "0");
document.getElementById("wakeup-hour").value = hour12;
document.getElementById("wakeup-minute").value = formattedMinute;
document.getElementById("wakeup-period").value = period;

const bedTime = document.getElementById('bed-time').value;
const bed_hour24 = Math.floor(bedTime);
const bed_minute = Math.round((bedTime - bed_hour24) * 60);
const bed_period = bed_hour24 >= 12 ? "PM" : "AM";
const bed_hour12 = bed_hour24 % 12 || 12;
const bed_formattedMinute = bed_minute.toString().padStart(2, "0");
document.getElementById("bedtime-hour").value = bed_hour12;
document.getElementById("bedtime-minute").value = bed_formattedMinute;
document.getElementById("bedtime-period").value = bed_period;
showSleepHours();

function cancelEdit() {
    var userConfirmed = confirm("Are you sure you want to cancel the changes made to this daily tracker?");
    if (userConfirmed){
        window.location.reload();
    }
}

function get_wakeup_time(){
    let hour = parseInt(document.getElementById('wakeup-hour').value);
    const minute = parseInt(document.getElementById('wakeup-minute').value);
    const period = document.getElementById('wakeup-period').value;
    if (hour == 12){ hour = 0; }
    if (period == 'PM'){ hour += 12; }
    return hour + (minute / 60);
}

function get_bed_time(){
    let hour = parseInt(document.getElementById('bedtime-hour').value);
    const minute = parseInt(document.getElementById('bedtime-minute').value);
    const period = document.getElementById('bedtime-period').value;
    if (hour == 12){ hour = 0; }
    if (period == 'PM'){ hour += 12; }
    return hour + (minute / 60);
}

function saveDailyTracker(){
    showSleepHours();
    const daily_trackerData = {
        comment: document.getElementById('daily_tracker-comment').innerText,
        mood_score: document.getElementById('mood-display').innerText,
        wakeup_time: get_wakeup_time(),
        bed_time: get_bed_time(),
        exercise_mins: document.getElementById('exercise-mins-input').value || 0,
        productive_mins: document.getElementById('productive-mins-input').value || 0,
        meditation_mins: document.getElementById('meditation-mins-input').value || 0
    };
    if (daily_trackerData.comment == "Add a comment" || daily_trackerData.comment == ""){
        showSnackbar("Daily Tracker could not be saved: Comment is missing", orange);
    } else {
        fetch(window.location.href, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(daily_trackerData)
        })
        .then(response => {
            if (response.ok){
                showSnackbar("Daily Tracker Successfully Saved", green);
            } else {
                showSnackbar("Failed to save, please try again", red);
            }
        })
        .catch(() => showSnackbar("Failed to save, please try again", red));
    }
}

function deleteDailyTracker(){
    var daily_trackerid = document.getElementById("daily_trackerId").value;
    var userConfirmed = confirm("Are you sure you want to delete this daily tracker?");
    if (userConfirmed){
        window.location.href = '/delete_daily_tracker/' + daily_trackerid;
    }
}

function updateMoodDisplay(value) {
    document.getElementById("mood-display").textContent = value;
}

function calculateAsleepHours(){
    let hours = get_wakeup_time() - get_bed_time();
    if (hours < 0){ hours = hours + 24; }
    return hours;
}

function showSleepHours(){
    document.getElementById('sleep-hours').innerText = 'You slept for ' + calculateAsleepHours() + ' hours';
}

document.addEventListener("DOMContentLoaded", () => {
    const bedtimeElements = document.querySelectorAll("#bedtime-hour, #bedtime-minute, #bedtime-period");
    const wakeupElements = document.querySelectorAll("#wakeup-hour, #wakeup-minute, #wakeup-period");
    const allElements = [...bedtimeElements, ...wakeupElements];
    allElements.forEach((element) => {
        element.addEventListener("change", showSleepHours);
    });
});
