function validateNumericInput(id) {
    var input = document.getElementById(id).value;
    if (input && isNaN(input)) {
        alert("請鍵入阿拉伯數字，例75000，勿輸入中英文字或全形符號");
        document.getElementById(id).value = ''; // Reset the input field
    }
}
function chineseToArabic(chineseNumber) {
    const chineseDigits = { '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9 };
    const multipliers = { '十': 10, '百': 100, '千': 1000 };

    let result = 0;
    let currentMultiplier = 1;
    for (let i = chineseNumber.length - 1; i >= 0; i--) {
        const char = chineseNumber[i];
        if (multipliers[char]) {
            currentMultiplier = multipliers[char];
            if (i === 0) {
                // For cases like 十 (10), where the digit before 十 is implied
                result += currentMultiplier;
            }
        } else {
            result += (chineseDigits[char] || 0) * currentMultiplier;
            currentMultiplier = 1; // Reset the multiplier
        }
    }
    return result;
}
function convertDateToArray(dateString) {
    // First, replace Chinese characters with hyphens
    var cleanString = dateString.replace(/年|月/g, '-').replace(/日/g, '');

    // Now split the string into an array based on the hyphen
    var parts = cleanString.split('-');
    
    // Convert each part to an integer
    return parts.map(part => parseInt(part, 10));
}
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
        document.getElementById("serial_number").innerHTML = '';
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
function getSerialNumberOptions(id) {
    fetch('/add_item', 
    {
        method: 'POST',
        headers: {'Content-Type': 'application/json',},
        body: JSON.stringify({case: 1, selected_id: id})
    })
    .then(response => response.text())
    .then(data => {
        var select_options = document.getElementById("serial_number");
        select_options.innerHTML = '<option value="" selected="selected">請選擇</option>';
        var serial_number = JSON.parse(data);
        for (var i = 0; i < serial_number.length; i++) {
            var options = document.createElement("OPTION");
            var txt = document.createTextNode(serial_number[i]["serial_number"]);
            options.appendChild(txt);
            options.setAttribute("value",serial_number[i]["serial_number"]);
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
document.getElementById('select_district').addEventListener('change', function() {getSerialNumberOptions(this.value);});


function getOptions(id,c) {
    var select_options = document.getElementById(id);
    select_options.innerHTML = '<option value="" selected="selected"> - </option>';
    var d = JSON.parse(data)[id];
    for (var i = 0; i < d.length; i++) {
        var options = document.createElement("OPTION");
        if (d[i][c]) {
            var txt = document.createTextNode(d[i][c]);
            options.appendChild(txt);
            select_options.add(options);
        }
    }
}
getOptions("land_using_type_for_urban","都市土地使用分區");
getOptions("land_using_type_for_non_urban","非都市土地使用分區");
getOptions("non_urban_land_classification","非都市土地使用編定");
getOptions("building_type","建物型態");
getOptions("rental_type","出租型態");
getOptions("parking_type","車位類別");


function isLeapYearInRepublicEra(year) {
    // 將民國年份轉換為公曆年份
    var gregorianYear = year + 1911;

    // 判斷是否為閏年
    if ((gregorianYear % 4 === 0 && gregorianYear % 100 !== 0) || gregorianYear % 400 === 0)
        return 1;
    return 0;
}
function selected_year(mId,dId){
    document.getElementById(mId).value = '';
    document.getElementById(dId).innerHTML = '';
}
function selected_month(selectedMonthVal,yId,dId) {

    if (selectedMonthVal <= 7)
        if (selectedMonthVal % 2)
            max_day = 31;
        else
            if (selectedMonthVal == 2)
                if (isLeapYearInRepublicEra(document.getElementById(yId).value))
                    max_day = 29;
                else
                    max_day = 28;
            else
                max_day = 30;
    else
        if (selectedMonthVal % 2)
            max_day = 30;
        else
            max_day = 31;

    var select_options = document.getElementById(dId);
    select_options.innerHTML = '<option value="" selected="selected">請選擇</option>';
    for (var i = 1; i <= max_day; i++) {
        var options = document.createElement("OPTION");
        var txt = document.createTextNode(i);
        options.appendChild(txt);
        select_options.add(options);
    }
}
function getDateOptions(yId,mId) {
    var select_options = document.getElementById(yId);
    select_options.innerHTML = '<option value="" selected="selected">請選擇</option>';
    for (var i = 113; i >= 20; i--) {
        var options = document.createElement("OPTION");
        var txt = document.createTextNode(i);
        options.appendChild(txt);
        select_options.add(options,);
    }
    var select_options = document.getElementById(mId);
    select_options.innerHTML = '<option value="" selected="selected">請選擇</option>';
    for (var i = 1; i <= 12; i++) {
        var options = document.createElement("OPTION");
        var txt = document.createTextNode(i);
        options.appendChild(txt);
        select_options.add(options);
    }
}
document.getElementById('rent_year').addEventListener('change', function() {selected_year("rent_month","rent_day");});
getDateOptions('rent_year','rent_month');
document.getElementById('rent_month').addEventListener('change', function() {selected_month(this.value,"rent_year","rent_day");});

document.getElementById('finish_year').addEventListener('change', function() {selected_year("finish_month","finish_day");});
getDateOptions('finish_year','finish_month');
document.getElementById('finish_month').addEventListener('change', function() {selected_month(this.value,"finish_year","finish_day");});

function checkSelectValue() {
  var select = document.getElementById('serial_number');
  var input = document.getElementById('serial_number_input');
  var val;

  if (!select.value) {
    input.required = true;
    input.disabled = false;
  } else {
    getData(select.value);
    input.required = false;
    input.disabled = true;
  }
}
checkSelectValue();

function getData(id) {
    fetch('/add_item', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({case: 2, selected_id: id})
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        const contentType = response.headers.get("content-type");
        if (!contentType || !contentType.includes("application/json")) {
            throw new TypeError("Received non-JSON response");
        }
        return response.text();
    })
    .then(data => {
        var d = JSON.parse(data);
        var date = convertDateToArray(d[0]['建築完成日期']);
        document.getElementById("main_material").value = d[0]['主要建材'];
        document.getElementById("finish_year").value = date[0];
        document.getElementById("finish_month").value = date[1];
        selected_month(document.getElementById("finish_month").value,"finish_year","finish_day");
        document.getElementById("finish_day").value = date[2];
        document.getElementById("t_floor").value = chineseToArabic(d[0]['總層數']);
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}

document.getElementById('serial_number_input').addEventListener('change', function() {getData(this.value);});


function deleteFunction() {
    // Logic to handle 'Delete'
}

function modifyFunction() {
    // Logic to handle 'Modify'
}






