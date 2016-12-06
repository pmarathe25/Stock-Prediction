function httpGetAsync(theUrl, callback)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.responseText);
    }
    xmlHttp.open("GET", theUrl, true); // true for asynchronous 
    xmlHttp.send(null);
}

function analyze(response) {
    console.log(response);
}

function getTrend(query) {
    httpGetAsync('http://localhost:8000?' + JSON.stringify({'term': query}), analyze);
}
