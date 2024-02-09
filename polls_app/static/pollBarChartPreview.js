const poll_results = {{ poll_answers | tojson }};

const pollAnswers = poll_results.map(subList => subList[0]);
const pollVotes = poll_results.map(subList => subList[1]);
const pollPercentages = poll_results.map(subList => subList[2]);

const ctx = document.getElementById('poll-results');

const chart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: pollAnswers,
        datasets: [{
            label: '# of Votes',
            data: pollVotes,
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

const chart_colors = chart.data.datasets[0].backgroundColor
const progressBars = document.querySelectorAll('.progress-bar');
for (let i = 0; i < progressBars.length; i++) {
    progressBars[i].style.backgroundColor = chart_colors[i];
}