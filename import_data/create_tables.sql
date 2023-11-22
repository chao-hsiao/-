use mydatabase;
SET global local_infile=true;
SET NAMES 'UTF8';

CREATE TABLE taiwan_cities (
    city_id INT,
    縣市英文名 VARCHAR(255),
    縣市全名 VARCHAR(255),
    縣市名 VARCHAR(50),
    縣市代碼 INT,
    PRIMARY KEY(city_id)
);

CREATE TABLE taiwan_districts (
    district_id INT,
    city_id INT,
    鄉鎮英文名 VARCHAR(255),
    縣市鄉鎮名 VARCHAR(255),
    縣市名 VARCHAR(50),
    鄉鎮名 VARCHAR(50),
    鄉鎮代碼 INT,
    PRIMARY KEY(district_id),
    FOREIGN KEY(city_id) REFERENCES taiwan_cities(city_id)
);

CREATE TABLE lvr_land_c (
    district_id INT,
    交易標的 VARCHAR(255),
    土地位置建物門牌 VARCHAR(255),
    土地面積平方公尺 DECIMAL(10, 2),
    都市土地使用分區 ENUM('','住','商','工','農','其他'),
    非都市土地使用分區 ENUM('','特定農業區','一般農業區','工業區','鄉村區','森林區','山坡地保育區','風景區','國家公園區','河川區','海域區','特定專用區'),
    非都市土地使用編定 ENUM('','甲種建築用地','乙種建築用地','丙種建築用地','丁種建築用地','農牧用地','林業用地','養殖用地','鹽業用地','礦業用地','窯業用地','交通用地','水利用地','遊憩用地','古蹟保存用地','生態保護用地','國土保安用地','殯葬用地','海域用地','特定目的事業'),
    租賃年月日 INT,
    租賃筆棟數 VARCHAR(255),
    租賃層次 VARCHAR(50),
    總樓層數 INT,
    建物型態 ENUM('','店面(店鋪)','套房(1房1廳1衛)','廠辦','住宅大樓(11層含以上1電梯)','辦公商業大樓','華廈(10層含以下1電梯)','公寓(5樓含以下0電梯)','透天厝','其他','工廠','農舍'),
    主要用途 VARCHAR(255),
    主要建材 VARCHAR(255),
    建築完成年月日 INT,
    建物總面積平方公尺 DECIMAL(10, 2),
    建物現況格局_房 INT,
    建物現況格局_廳 INT,
    建物現況格局_衛 INT,
    建物現況格局_隔間 INT,
    有無管理組織 BOOLEAN,
    有無附傢俱 BOOLEAN,
    總額元 INT,
    單價元平方公尺 INT,
    車位類別 ENUM('','坡道平面','升降機械','坡道機械','其他','一樓平面','升降平面','塔式車位'),
    車位面積平方公尺 INT,
    車位總額元 INT,
    備註 VARCHAR(255),
    serial_number VARCHAR(255),
    出租型態 ENUM('','分租雅房','整棟(戶)出租','獨立套房','分租套房','分層出租'),
    有無管理員 BOOLEAN,
    租賃期間 VARCHAR(255),
    有無電梯 BOOLEAN,
    附屬設備 VARCHAR(255), 
    租賃住宅服務 ENUM('','一般轉租','社會住宅代管','一般代管','社會住宅包租轉租','一般包租'),
    city_id INT,
    FOREIGN KEY(district_id) REFERENCES taiwan_districts(district_id),
    FOREIGN KEY(city_id) REFERENCES taiwan_cities(city_id)
);

CREATE TABLE lvr_land_c_build (
    serial_number VARCHAR(255),
    屋齡 INT,
    建物移轉面積平方公尺 DECIMAL(10, 2),
    主要用途 VARCHAR(255),
    主要建材 VARCHAR(50),
    建築完成日期 VARCHAR(10),
    總層數 VARCHAR(10),
    建物分層 VARCHAR(50),
    移轉情形 VARCHAR(50)
);

CREATE TABLE lvr_land_c_land (
    serial_number VARCHAR(255),
    土地位置 VARCHAR(255),
    土地移轉面積平方公尺 DECIMAL(10, 2),
    使用分區或編定 VARCHAR(50),
    權利人持分分母 INT,
    權利人持分分子 INT,
    移轉情形 VARCHAR(255),
    地號 INT
);

CREATE TABLE lvr_land_c_park (
    serial_number VARCHAR(255),
    車位類別 VARCHAR(50),
    車位價格 INT,
    車位面積平方公尺 DECIMAL(10, 2),
    車位所在樓層 VARCHAR(50)
);

load data local infile './csv/taiwan_cities.csv'
into table taiwan_cities
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 lines;

load data local infile './csv/taiwan_districts.csv'
into table taiwan_districts
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 lines;

load data local infile './csv/lvr_land_c.csv'
into table lvr_land_c
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 lines;

load data local infile './csv/lvr_land_c_build.csv'
into table lvr_land_c_build
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 lines;

load data local infile './csv/lvr_land_c_land.csv'
into table lvr_land_c_land
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 lines;

load data local infile './csv/lvr_land_c_park.csv'
into table lvr_land_c_park
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 lines;

