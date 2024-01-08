function getDistrictOptions(id) {
    fetch('/getDistrictOptions', 
    {
        method: 'POST',
        headers: {'Content-Type': 'application/json',},
        body: JSON.stringify({selected_id: id})
    })
    .then(response => response.text())
    .then(data => {
        var select_options = document.getElementById("select_district");
        select_options.innerHTML = '<option value="" selected="selected">請選擇</option>';
        var districts = JSON.parse(data);
        for (var i = 0; i < districts.length; i++) {
            var options = document.createElement("OPTION");
            var txt = document.createTextNode(districts[i]["鄉鎮名"]);
            options.appendChild(txt);
            options.setAttribute("value",districts[i]["district_id"]);
            select_options.add(options);
        }
    });
}

var select_options = document.getElementById("select_city");
var data = document.getElementById('data').textContent;
var cities = JSON.parse(data)['cities'];
for (var i = 0; i < cities.length; i++) {
    var selected_cities = document.createElement("OPTION");
    var txt = document.createTextNode(cities[i]["縣市名"]);
    selected_cities.appendChild(txt);
    selected_cities.setAttribute("value",cities[i]["city_id"]);
    select_options.add(selected_cities);
}
getDistrictOptions(document.getElementById('select_city').value);

document.getElementById('select_city').addEventListener('change', function() {getDistrictOptions(this.value);});

var select_options = document.getElementById("rental_type");
select_options.innerHTML = '<option value="0" selected="selected">不限</option>';
var rental_type = JSON.parse(data)['rental_type'];
for (var i = 0; i < rental_type.length; i++) {
    var options = document.createElement("OPTION");
    if (rental_type[i]["出租型態"]) {
        var txt = document.createTextNode(rental_type[i]["出租型態"]);
    } else {
        var txt = document.createTextNode("未分類的");
    }
    options.appendChild(txt);
    select_options.add(options);
}

function validateNumericInput(id) {
    var input = document.getElementById(id).value;
    if (input && isNaN(input)) {
        alert("請鍵入阿拉伯數字，例75000，勿輸入中英文字或全形符號");
        document.getElementById(id).value = ''; // Reset the input field
    }
}


function addFunction() {
    // Logic to handle 'Add'
    window.location.href = 'add_item';
}

function deleteFunction() {
    // Logic to handle 'Delete'
}

function modifyFunction() {
    // Logic to handle 'Modify'
}






