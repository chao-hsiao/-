function populateFormData(data) {
    columns = ['都市土地使用分區',
        '非都市土地使用分區',
        '非都市土地使用編定',
        '主要用途',
        '建物現況格局_房',
        '建物現況格局_廳',
        '建物現況格局_衛',
        '建物現況格局_隔間',
        '有無管理組織',
        '有無附傢俱',
        '總額元',
        '車位總額元',
        '備註',
        '出租型態',
        '有無管理員',
        '有無電梯',
        '附屬設備'];
    id = ['land_using_type_for_urban',
        'land_using_type_for_non_urban',
        'non_urban_land_classification',
        'main_use',
        'room',
        'living',
        'toilet',
        'cubicle',
        'has_org',
        'has_furniture',
        't_cost',
        'p_t_cost',
        'note',
        'rental_type',
        'has_security',
        'has_lift',
        'other_equipment'];
    data = data;

    document.getElementById('rent_year').value = toString(data['租賃年月日']).slice(-2);
    document.getElementById('rent_month').value = toString(data['租賃年月日']).slice(-4,-2);
    document.getElementById('rent_day').value = toString(data['租賃年月日']).slice(0,-4);

    var numbers = data['租賃筆棟數'].match(/\d+/g).map(Number);
    document.getElementById('land').value = numbers[0];
    document.getElementById('building').value = numbers[1];
    document.getElementById('park').value =  numbers[2];

    for (var i = id.length - 1; i >= 0; i--) {
        if(document.getElementById(id[i]).type == 'checkbox')
            if (data[columns[i]])
                document.getElementById(id[i]).checked = true;
            else
                document.getElementById(id[i]).checked = false;
        else if(data[columns[i]])
            document.getElementById(id[i]).value = data[columns[i]];
    }
    if(!data['車位類別'])
        var park_div = document.getElementById('park_div');
        if (park_div) {
            park_div.remove();
        }
}
function getOptions(id,c,data) {
    var select_options = document.getElementById(id);
    select_options.innerHTML = '<option value="" selected="selected"> - </option>';
    var d = data[id];
    for (var i = 0; i < d.length; i++) {
        var options = document.createElement("OPTION");
        if (d[i][c]) {
            var txt = document.createTextNode(d[i][c]);
            options.appendChild(txt);
            select_options.add(options);
        }
    }
}
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
function validateNumericInput(id) {
    var input = document.getElementById(id).value;
    if (input && isNaN(input)) {
        alert("請鍵入阿拉伯數字，例75000，勿輸入中英文字或全形符號");
        document.getElementById(id).value = ''; // Reset the input field
    }
}
var data = JSON.parse(document.getElementById('data').textContent);
var options = data.options;
data = data.data[0];

getOptions("land_using_type_for_urban","都市土地使用分區",options);
getOptions("land_using_type_for_non_urban","非都市土地使用分區",options);
getOptions("non_urban_land_classification","非都市土地使用編定",options);
getOptions("rental_type","出租型態",options);
populateFormData(data);

document.getElementById('rent_year').addEventListener('change', function() {selected_year("rent_month","rent_day");});
getDateOptions('rent_year','rent_month');
document.getElementById('rent_month').addEventListener('change', function() {selected_month(this.value,"rent_year","rent_day");});



function updateSelectState() {
    const select1 = document.getElementById('land_using_type_for_urban');
    const select2 = document.getElementById('land_using_type_for_non_urban');
    const select3 = document.getElementById('non_urban_land_classification');

    const select1Empty = !select1.value;
    const select2Empty = !select2.value;
    const select3Empty = !select3.value;

    if (!select1Empty) {
        select2.disabled = true;
        select3.disabled = true;
    } else if (!select2Empty || !select3Empty) {
        select1.disabled = true;
    } else {
        select1.disabled = false;
        select2.disabled = false;
        select3.disabled = false;
    }
}

document.getElementById('land_using_type_for_urban').addEventListener('change', updateSelectState);
document.getElementById('land_using_type_for_non_urban').addEventListener('change', updateSelectState);
document.getElementById('non_urban_land_classification').addEventListener('change', updateSelectState);

// Initialize the state on page load
updateSelectState();
