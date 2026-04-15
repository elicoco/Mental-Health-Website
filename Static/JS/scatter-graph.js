const STATS_JSON = document.querySelector("#stats").value;
const STATS = JSON.parse(STATS_JSON);
const points = STATS.points;
const GROUP_NAME = document.querySelector("#name").value.toLowerCase();
const pmcc = STATS.pmcc;
const pValue = STATS.p_value;
const absPmcc = Math.abs(pmcc);

// gets GROUP_NAME from HTML
if (GROUP_NAME == 'sleep') {
    document.getElementById("title-graph").textContent = `Mood vs Sleep Hours`;
}

// How much mood changes per hour
const moodChangePerHour = GROUP_NAME === 'sleep'
    ? Math.abs(STATS.slope).toFixed(2)
    : Math.abs(STATS.slope * 60).toFixed(2);

// Strength of correlation in plain English
function getStrengthLabel(r) {
    if (r < 0.1) return 'no noticeable';
    if (r < 0.3) return 'a weak';
    if (r < 0.6) return 'a moderate';
    if (r < 0.8) return 'a strong';
    return 'a very strong';
}

// What % of mood variation is explained (R²)
const rSquaredPercent = (pmcc * pmcc * 100).toFixed(1);
const strengthLabel = getStrengthLabel(absPmcc);
const directionWord = pmcc >= 0 ? 'positive' : 'negative';

// Significance in plain English
function getSignificanceText(p) {
    if (p > 0.1)  return "You may need more entries before a clear pattern emerges.";
    if (p > 0.05) return "This might be a real pattern, but more entries would help confirm it.";
    if (p > 0.01) return "This pattern is unlikely to be a coincidence.";
    return "This pattern is very unlikely to be a coincidence.";
}

const significanceText = getSignificanceText(pValue);

// Main sentence
let sentence1, sentence2;
if (pValue > 0.1 || absPmcc < 0.1) {
    sentence1 = `No clear relationship between your ${GROUP_NAME} and mood has been found yet.`;
    sentence2 = significanceText;
} else if (pmcc > 0) {
    sentence1 = `More ${GROUP_NAME} tends to go with a better mood. On average, each extra hour is linked to a ${moodChangePerHour} point increase in mood score.`;
    sentence2 = `About ${rSquaredPercent}% of your mood changes appear linked to your ${GROUP_NAME}, which is ${strengthLabel} ${directionWord} relationship. ${significanceText}`;
} else {
    sentence1 = `More ${GROUP_NAME} tends to go with a lower mood. On average, each extra hour is linked to a ${moodChangePerHour} point decrease in mood score.`;
    sentence2 = `About ${rSquaredPercent}% of your mood changes appear linked to your ${GROUP_NAME}, which is ${strengthLabel} ${directionWord} relationship. ${significanceText}`;
}

document.getElementById("correlation-sentence").textContent = sentence1;
document.getElementById("correlation-sentence2").textContent = sentence2;


// Line of best fit
function calculateRegressionLine(data) {
    const slope = STATS.slope;
    const intercept = STATS.intercept;
    const xValues = data.map(point => point.x);
    const maxX = Math.max(...xValues);
    if (intercept >= 0) {
        return [
            { x: 0, y: intercept },
            { x: maxX, y: slope * maxX + intercept }
        ];
    } else {
        return [
            { x: -intercept / slope, y: 0 },
            { x: maxX, y: slope * maxX + intercept }
        ];
    }
}

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
                type: 'line',
                borderColor: 'red',
                borderWidth: 2,
                fill: false,
                showLine: true,
                tension: 0
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
                min: 0,
            },
            y: {
                title: {
                    display: true,
                    text: STATS.yname
                },
                min: 0,
                max: 100
            }
        }
    }
};
new Chart(ctx, config);
