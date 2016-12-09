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
    response = JSON.parse(response)
    console.log(response);
    chartTrend(response['symbol'], response['trend'], response['historical'][1], response['historical'][2]);
}

function chartTrend(symbol, trend, stockData, dates) {
    var timeFormat = (function(date) {
        console.log(date);
        return (date.getMonth()+1) + '/' + date.getDate();
    });
    var width = 700;
    var height = 500;
    var margin = [50, 50, 50, 60];
    var svg = d3.select('#graph-container').append('svg')
                .attr('class', 'graph')
                .attr('width', width)
                .attr('height', height)
                .append('g')
                    .attr('transform', 'translate(' + margin[3] + ',' + margin[0] + ')');
    var curDate = new Date();
    var todayOpen = new Date();
    todayOpen.setHours(0,0,0,0);
    todayOpen.setDate(todayOpen.getDate() + (9.5/24));
    console.log(todayOpen);
    var todayClose = new Date();
    todayClose.setHours(0,0,0,0);
    todayClose.setDate(todayClose.getDate() + (15.5/24));
    console.log(todayClose);
    var opens = dates.map(function(d) {
        var date = new Date(d + ' EST');
        date.setDate(date.getDate() + (9.5/24));
        return date;
    });
    var closes = dates.map(function(d) {
        var date = new Date(d + ' EST');
        date.setDate(date.getDate() + (15.5/24));
        return date;
    });
    var dates = [];
    for (var i = 0; i < opens.length; i++) {
        dates.unshift(opens[i], closes[i]);
    }
    console.log(dates);
    dates.push(todayOpen, todayClose);
    dates.reverse();
    var data = stockData.map(function(d, i) {
                return {'date': dates[i], 'value': d};
    });
    data = data.slice(1);
    data.reverse();
    data.forEach(function(d, i) { d.x = i });
    var predictedPoint = {'date': todayClose, 'value': data[data.length - 1].value + trend.change, 'x': data.length};
    console.log(predictedPoint);
    data.push(predictedPoint);
    console.log(data);
    var x = d3.scale.linear()
            .domain(d3.extent(data, function(d) { return d.x }))
            .range([0, width - margin[1] - margin[3]]);
    var y = d3.scale.linear()
            .domain(d3.extent(data, function(d) { return d.value }).reverse())
            .range([0, height - margin[0] - margin[2]])
            .nice();
    var line = d3.svg.line()
            .x(function(d, i) {
                return x(d.x);
            })
            .y(function(d) {
                return y(d.value);
            });
    var xAxis = d3.svg.axis()
            .scale(x)
            .orient('bottom')
            .tickFormat(function(d) { console.log(d); return timeFormat(data[d].date); });
    var yAxis = d3.svg.axis()
            .scale(y)
            .innerTickSize(-1 * (width - margin[1] - margin[3]))
            .outerTickSize(0)
            .orient('left');

    var historic = data.slice(0, data.length - 1);
    var predicted = data.slice(data.length - 2);

    svg.append('g')
        .attr('class', 'axis')
        .attr('transform', 'translate(0,' + (height - margin[0] - 24.5) + ')')
        .call(xAxis);
    svg.append('g')
        .attr('class', 'axis')
        .call(yAxis);
    svg.append('path')
        .attr('class', 'line')
        .attr('d', line(historic));
    svg.append('path')
        .attr('class', 'line ' + ((trend.change > 0) ? 'growth' : 'decline'))
        .attr('d', line(predicted));

    svg.append("text")
        .attr("x", (width / 2))
        .attr("y", -margin)
        .attr("text-anchor", "end")
        .style("font-size", "40px")
        .text(symbol.toUpperCase());
}

function getTrend(query) {
    console.log("starting query for" + query);
    httpGetAsync('http://localhost:8000?' + JSON.stringify({'term': query}), analyze);
}
