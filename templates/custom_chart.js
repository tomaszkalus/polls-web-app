var value = 57866;
var value2 = 4600;
var max = 80000;

var bar_ctx = document.getElementById('bar-chart');
var bar_chart = new Chart(bar_ctx, {
  type: 'horizontalBar',
  data: {
    labels: [],
    datasets: [
    {
      data: [value],
      backgroundColor: "rgba(51,230,125,1)"
    }, 
    {
      data: [value2],
      backgroundColor: "red",
    },
    {
    	data: [max - value],
      backgroundColor: "lightgrey"
    }
    
    
    
    ]
  },
  options: {
    legend: {
      display: false
    },
    tooltips: {
      enabled: true
    },
    scales: {
      xAxes: [{
        display: false,
        stacked: true
      }],
      yAxes: [{
        display: false,
        stacked: true
      }],
    } // scales
  } // options
});
