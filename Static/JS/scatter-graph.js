const STATS_JSON = document.querySelector("#stats").value;
const STATS = JSON.parse(STATS_JSON);
const points = STATS.points;
let HOUR_MOOD_SCORE_INCREASE;
const GROUP_NAME = document.querySelector("#name").value.toLowerCase();
// gets GROUP_NAME from HTML
if (GROUP_NAME == 'sleep'){ // if it's for sleep then it needs update title
    document.getElementById("title-graph").textContent = `Mood vs Sleep Hours`;
    HOUR_MOOD_SCORE_INCREASE = (STATS.slope).toFixed(2);
}
else{
    HOUR_MOOD_SCORE_INCREASE = (STATS.slope * 60).toFixed(2);
}
const PMCC = (STATS.pmcc*100).toFixed(1);
if (PMCC > 0){ // if it is a positive correlation than it will show this in the sentences
    document.getElementById("correlation-sentence").textContent = `On average, every hour of ${GROUP_NAME} increased your mood score by
    ${HOUR_MOOD_SCORE_INCREASE}`; // sentences to communicate with user
    document.getElementById("correlation-sentence2").textContent = `Mood and ${GROUP_NAME} are positively correlated by ${PMCC}%`;
}
else{ // if correlation is negative
    document.getElementById("correlation-sentence").textContent = `On average, every hour of ${GROUP_NAME} decreased your mood score by
    ${Math.abs(HOUR_MOOD_SCORE_INCREASE)}`; // sentences to communicate with user
    document.getElementById("correlation-sentence2").textContent = `Mood and ${GROUP_NAME} are negatively correlated by ${Math.abs(PMCC)}%`;
    // absolute value so it is a positive number
}


// Function to create line of best fit 
function calculateRegressionLine(data) {
    const slope = STATS.slope;
    const intercept = STATS.intercept;

    // Generate points for the line of best fit
    const xValues = data.map(point => point.x);
    const maxX = Math.max(...xValues);
    if (intercept >= 0){
        return [
            { x: 0, y: intercept },
            { x: maxX, y: slope * maxX + intercept }
        ];
    }
    else{
        return [
            { x: -intercept / slope, y: 0 },
            { x: maxX, y: slope * maxX + intercept }
        ];
    }
}

// Get regression line data
const regressionLine = calculateRegressionLine(points);

// Chart.js 
const ctx = document.getElementById('scatterChart').getContext('2d');
const config = {
    type: 'scatter',
    data: {
        datasets: [
            {
                label: 'Datapoints',
                data: points,
                backgroundColor: 'blue',
                pointStyle: 'circle',
            },
            {
                label: 'Line of Best Fit',
                data: regressionLine,
                type: 'line', // Line overlay
                borderColor: 'red',
                borderWidth: 2,
                fill: false,
                showLine: true,
                tension: 0 // Straight line
            }
        ]
    },
    options: {
        scales: {
            x: {
                type: 'linear',
                position: 'bottom',
                title: {
                    display: true,
                    text: STATS.xname
                },
                min: 0, // Force x-axis to start at 0
            },
            y: {
                title: {
                    display: true,
                    text: STATS.yname
                },
                min: 0, // Force y-axis to start at 0
                max: 100
            }
        }
    }
};
// Render the scatter plot with the line of best fit
new Chart(ctx, config);