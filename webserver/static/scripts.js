
var select_options = document.getElementById("select_city");
var data = document.getElementById('data').textContent;
var cities = JSON.parse(data)['cities'];
for (var i = 0; i < cities.length; i++) {
    var selected_cities = document.createElement("OPTION");
    var txt = document.createTextNode(cities[i]["縣市名"]);
    selected_cities.appendChild(txt);
    selected_cities.setAttribute("value",cities[i]["city_id"]);
    select_options.insertBefore(selected_cities,select_options.lastChild);
}
selected_city(document.getElementById('select_city').value);

document.getElementById('select_city').addEventListener('change', function() {selected_city(this.value);});

function selected_city(selectedCityId) {
    fetch('/', 
    {
        method: 'POST',
        headers: {'Content-Type': 'application/json',},
        body: JSON.stringify({selected_city_id: selectedCityId})
    })
    .then(response => response.text())
    .then(data => {
        var select_options = document.getElementById("select_district");
        select_options.innerHTML = '<option value="0" selected="selected">請選擇</option>';
        var districts = JSON.parse(data);
        for (var i = 0; i < districts.length; i++) {
            var districts_options = document.createElement("OPTION");
            var txt = document.createTextNode(districts[i]["鄉鎮名"]);
            districts_options.appendChild(txt);
            districts_options.setAttribute("value",districts[i]["district_id"]);
            select_options.insertBefore(districts_options,select_options.lastChild);
        }
    });
}

var select_options = document.getElementById("rental_type");
select_options.innerHTML = '<option value="0" selected="selected">不限</option>';
var rental_types = JSON.parse(data)['rental_types'];
for (var i = 0; i < rental_types.length; i++) {
    var selected_cities = document.createElement("OPTION");
    if (rental_types[i]["出租型態"]) {
        var txt = document.createTextNode(rental_types[i]["出租型態"]);
    } else {
        var txt = document.createTextNode("未分類的");
    }
    selected_cities.appendChild(txt);
    select_options.insertBefore(selected_cities,select_options.lastChild);
}

// document.getElementById('submitBtn').addEventListener('click', function() {submit();});
function submit() {
    var return_results = {
        city: document.getElementById('select_city').value,
        district: document.getElementById('select_district').value,
        lowerprice: document.getElementById('lowerprice').value,
        upperprice: document.getElementById('upperprice').value,
        lowerarea: document.getElementById('lowerarea').value,
        upperarea: document.getElementById('upperarea').value,
        rental_type: document.getElementById('rental_type').value
    };

    fetch('/results', 
    {
        method: 'POST',
        headers: {'Content-Type': 'application/json',},
        body: JSON.stringify(return_results)
    })
    .then(response => response.text())
    .then(data => {console.log(data)
    });
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
    window.location.href = 'add_data';
}

function deleteFunction() {
    // Logic to handle 'Delete'
}

function modifyFunction() {
    // Logic to handle 'Modify'
}






