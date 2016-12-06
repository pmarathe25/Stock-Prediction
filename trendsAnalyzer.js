function httpGetAsync(theUrl, callback)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.responseText);
    }
    xmlHttp.open("GET", theUrl, true);
    xmlHttp.send(null);
}

function analyze(response) {
    console.log(response);
    response = JSON.parse(response)
    chartTrend(response['trend'], response['historical'][1]);
}

function chartTrend(trend, stockData) {
    var width = 700;
    var height = 500;
    var margin = [25, 25, 25, 25];
    var svg = d3.select('body').append('svg')
                .attr('width', width)
                .attr('height', height)
                .append('g')
                    .attr('transform', 'translate(' + margin[3] + ',' + margin[0] + ')');
    var curDate = new Date();
    var predictDate = new Date();
    predictDate.setDate(curDate + 0.5);
    var data = stockData.map(function(d, i) {
                var date = new Date()
                date.setDate(curDate.getDate() - (stockData.length - (i / 2)));
                return {'date': date, 'value': d};
    });
    data.unshift({'date': predictDate, 'value': data[0].value + trend.change});
    var x = d3.time.scale()
            .domain(d3.extent(data, function(d) { return d.date }))
            .range([0, width - margin[1] - margin[3]]);
    var y = d3.scale.linear()
            .domain(d3.extent(data, function(d) { return d.value }))
            .range([0, height - margin[0] - margin[2]]);
    var line = d3.svg.line()
            .x(function(d) {
                return x(d.date);
            })
            .y(function(d) {
                return y(d.value);
            });
    var xAxis = d3.svg.axis()
            .scale(x)
            .orient('bottom');
    var yAxis = d3.svg.axis()
            .scale(y)
            .orient('left');

    svg.append('path')
        .attr('class', 'axis')
        .attr('transform', 'translate(0,' + (height - margin[0]) + ')')
        .call(xAxis);
    svg.append('path')
        .attr('class', 'axis')
        .call(yAxis);
    svg.append('path')
        .attr('class', function(d, i) {
            var str = 'line';
            if (i == 0) {
                if (trend.change >= 0) {
                    str += ' growth';
                } else {
                    str += ' decline';
                }
            }
            return str;
        })
        .attr('d', line(data));
}

function getTrend(query) {
    httpGetAsync('http://localhost:8000?' + JSON.stringify({'term': query}), analyze);
}
