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
const bedHour24 = Math.floor(bedTime);
const bedMinute = Math.round((bedTime - bedHour24) * 60);
const bedPeriod = bedHour24 >= 12 ? "PM" : "AM";
const bedHour12 = bedHour24 % 12 || 12;
const bedFormattedMinute = bedMinute.toString().padStart(2, "0");
document.getElementById("bedtime-hour").value = bedHour12;
document.getElementById("bedtime-minute").value = bedFormattedMinute;
document.getElementById("bedtime-period").value = bedPeriod;
showSleepHours();

function cancelEdit() {
    var userConfirmed = confirm("Are you sure you want to cancel the changes made to this daily tracker?");
    if (userConfirmed){
        window.location.reload();
    }
}

function getWakeupTime(){
    let hour = parseInt(document.getElementById('wakeup-hour').value);
    const minute = parseInt(document.getElementById('wakeup-minute').value);
    const period = document.getElementById('wakeup-period').value;
    if (hour == 12){ hour = 0; }
    if (period == 'PM'){ hour += 12; }
    return hour + (minute / 60);
}

function getBedTime(){
    let hour = parseInt(document.getElementById('bedtime-hour').value);
    const minute = parseInt(document.getElementById('bedtime-minute').value);
    const period = document.getElementById('bedtime-period').value;
    if (hour == 12){ hour = 0; }
    if (period == 'PM'){ hour += 12; }
    return hour + (minute / 60);
}

function saveDailyTracker(silent = false){
    showSleepHours();
    const dailyTrackerData = {
        comment: document.getElementById('daily-tracker-comment').innerText,
        mood_score: parseInt(document.getElementById('mood-display').innerText),
        wakeup_time: getWakeupTime(),
        bed_time: getBedTime(),
        exercise_mins: document.getElementById('exercise-mins-input').value || 0,
        productive_mins: document.getElementById('productive-mins-input').value || 0,
        meditation_mins: document.getElementById('meditation-mins-input').value || 0
    };
    fetch(window.location.href, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(dailyTrackerData)
    })
    .then(response => {
        if (response.ok){
            if (!silent) showSnackbar("Daily Tracker Successfully Saved", green);
        } else {
            showSnackbar("Failed to save, please try again", red);
        }
    })
    .catch(() => showSnackbar("Failed to save, please try again", red));
}

let autoSaveTimer;
function triggerAutoSave() {
    clearTimeout(autoSaveTimer);
    autoSaveTimer = setTimeout(() => saveDailyTracker(true), 1500);
}

function deleteDailyTracker(){
    const dailyTrackerId = document.getElementById("daily-tracker-id").value;
    var userConfirmed = confirm("Are you sure you want to delete this daily tracker?");
    if (userConfirmed){
        window.location.href = '/delete_daily_tracker/' + dailyTrackerId;
    }
}

function updateMoodDisplay(value) {
    document.getElementById("mood-display").textContent = value;
}

function calculateSleepHours(){
    let hours = getWakeupTime() - getBedTime();
    if (hours < 0){ hours = hours + 24; }
    return hours;
}

function showSleepHours(){
    document.getElementById('sleep-hours').innerText = 'You slept for ' + calculateSleepHours() + ' hours';
}

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById('daily-tracker-comment').addEventListener('input', triggerAutoSave);
    document.getElementById('mood-slider').addEventListener('input', triggerAutoSave);
    document.getElementById('exercise-mins-input').addEventListener('input', triggerAutoSave);
    document.getElementById('productive-mins-input').addEventListener('input', triggerAutoSave);
    document.getElementById('meditation-mins-input').addEventListener('input', triggerAutoSave);

    const bedtimeElements = document.querySelectorAll("#bedtime-hour, #bedtime-minute, #bedtime-period");
    const wakeupElements = document.querySelectorAll("#wakeup-hour, #wakeup-minute, #wakeup-period");
    [...bedtimeElements, ...wakeupElements].forEach(el => {
        el.addEventListener("change", showSleepHours);
        el.addEventListener("change", triggerAutoSave);
    });
});
