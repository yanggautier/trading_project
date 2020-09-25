// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';
// Area Chart Example
var ctx = document.getElementById("myAreaChart");

var myLineChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: [{% for date in dates %}
                "{{date}}",
            {% endfor %}],
datasets: [{
  backgroundColor: "rgba(2,117,216,0.2)",
  borderColor: "rgba(2,117,216,1)",
  pointBackgroundColor: "rgba(2,117,216,1)",
  pointBorderColor: "rgba(255,255,255,0.8)",
  pointHoverBackgroundColor: "rgba(2,117,216,1)",
  data: [{% for close in closes %}
            "{{close}}",
{% endfor %}]
        }],
            },
options: {
  scales: {
    xAxes: [{
      time: {
        unit: 'date'
      },
      gridLines: {
        display: false
      },
      ticks: {
        maxTicksLimit: 7
      }
    }],
      yAxes: [{
        ticks: {
          min: 0,
          max: {{ maxclose }},
  maxTicksLimit: 5
},
gridLines: {
  color: "rgba(0, 0, 0, .125)",
                        }
                    }],
                },
legend: {
  display: false
}
        }
        });