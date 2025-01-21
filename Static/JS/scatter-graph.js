const statsjson = document.querySelector("#stats").value;
const stats = JSON.parse(statsjson);
const points = stats.points;
let hour_moodscoreincrease;
const groupname = document.querySelector("#name").value.toLowerCase();
// gets groupname from HTML
if (groupname == 'sleep'){ // if it's for sleep then it needs update title
    document.getElementById("title-graph").textContent = `Mood vs Sleep Hours`;
    hour_moodscoreincrease = (stats.slope).toFixed(2);
}
else{
    hour_moodscoreincrease = (stats.slope * 60).toFixed(2);
}
const pmcc = (stats.pmcc*100).toFixed(1);
if (pmcc > 0){ // if it is a positive correlation than it will show this in the sentences
    document.getElementById("correlation-sentence").textContent = `On average, every hour of ${groupname} increased your mood score by 
    ${hour_moodscoreincrease}`; // sentences to communicate with user
    document.getElementById("correlation-sentence2").textContent = `Mood and ${groupname} are positively correlated by ${pmcc}%`;
}
else{ // if correlation is negative
    document.getElementById("correlation-sentence").textContent = `On average, every hour of ${groupname} decreased your mood score by 
    ${Math.abs(hour_moodscoreincrease)}`; // sentences to communicate with user
    document.getElementById("correlation-sentence2").textContent = `Mood and ${groupname} are negatively correlated by ${Math.abs(pmcc)}%`;
    // absolute value so it is a positive number
}


// Function to create line of best fit 
function calculateRegressionLine(data) {
    const slope = stats.slope;
    const intercept = stats.intercept;

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
                    text: stats.xname
                },
                min: 0, // Force x-axis to start at 0
            },
            y: {
                title: {
                    display: true,
                    text: stats.yname
                },
                min: 0, // Force y-axis to start at 0
                max: 100
            }
        }
    }
};
// Render the scatter plot with the line of best fit
new Chart(ctx, config);