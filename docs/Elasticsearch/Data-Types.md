---
author: Harry Hoang
date: 2022-02-07
---

# Data Types

Data Types cho biết kiểu dữ liệu của data trong một field như `strings` hay `boolean`. For example, you can index strings to both text and keyword fields. However, text field values are analyzed for full-text search while keyword strings are left as-is for filtering and sorting.

## Common types

- `binary`: Binary value được encoded dưới dạng Base64 string.

- `boolean`: true and false values.

- `Keywords` gồm `keyword`, `constant_keyword`, và `wildcard`.

- `Numbers`: Numeric types, như kiểu `long` and `double`,

- `Dates`: Date types, gồm `date` và `date_nanos`.

Trên đây là các Common data types. Trong Elasticsearch, data types được chia thành các nhóm như sau:

- `Objects and relational types` như `object`, `flattened`, `nested` 
- `Structured data types` như `Range`, `ip`, `version`
- `Aggregate data types` như `aggregate_metric_double`, `histogram`
- `Text search types`
- `Document ranking types`
- `Spatial data types`

xem đầy đủ tại: [Field Data type](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html#mapping-types)


## Core Data Types

### Strings
Kiểu string là một Data Types, trong Elasticsearch, string type không chỉ lưu trữ value có giá trị chuỗi mà còn có thể lưu `full text` hay `key work`.

#### Strings – Full Text

Thường được sử dụng cho các tìm kiếm dựa trên văn bản, chẳng hạn như khi tìm kiếm sản phẩm theo tên. Các field có data type này sẽ được Elasticsearch phân tích để chuyển đổi các chuỗi thành danh sách các thuật ngữ riêng lẻ. Điều này xảy ra trước khi dữ liệu được lập index, cho phép Elasticsearch tìm kiếm các từ riêng lẻ trong một văn bản. `Full Text` không được sử dụng để sắp xếp và hiếm khi được sử dụng để tổng hợp, phân tích.

#### Strings – Keywords

`Keywords` được sử dụng để lưu trữ các giá trị chính xác như `tags`, `statuses`, v.v. Fields thuộc loại này thường được sử dụng để `filtering`, chẳng hạn như tìm tất cả các sản phẩm đang được bán. Ngoài ra cũng được sử dụng để phân loại và tổng hợp.

### Numeric

Core data type tiếp theo là numeric. Numeric hỗ trợ các kiểu số sau.

- long (signed 64-bit integer)
- integer (signed 32-bit integer)
- short (signed 16-bit integer)
- byte (signed 8-bit integer)
- double (double-precision 64-bit floating point)
- float (single-precision 32-bit floating point)

### Dates

Dates có thể là một string dưới một định dạng nhất định thể hiện thời gian, ngày tháng như: `2016-01-01` hoặc `2016/01/01 12:00:00`. Elasticsearch lưu trữ date thông qua `Dates – Formats` như sau

#### Dates – Formats
Định dạng mặc định là `date` cộng với `optional time` hoặc `number of milliseconds since the epoch` (số mili giây sau mỗi epoch): `strict_date_optional_time||epoch_millis`. Ví dụ:

- 2016-01-01 (date only)
- 2016-01-01T12:00:00Z (date including time)
- 1410020500000 (milliseconds since the epoch)

### Boolean
If a field can only contain on or off values, then the boolean data type is appropriate. Just like in JSON, boolean fields can accept true and false values. They also accept strings and numbers, which will be interpreted as a boolean. I would personally not recommend this, unless you need to do this for some reason. False values include the boolean false, a string with a value of “false”, “off”, “no”, “0” or an empty string (“”), or the number 0. Everything that is not interpreted as false, will be interpreted as true.

Cũng giống như trong JSON, các boolean data type chấp nhận các giá trị `true` và `false` hoặc các chuỗi và số được hiểu là boolean như `0`, `1`.

### Binary
Một chuỗi nhị phân được Base64 encoded, ví dụ `aHR0cDovL2NvZGluZ2V4cGxhaW5lZC5jb20=`

## Complex Data Types

### Object

Các JSON document có phân cấp, nghĩa là một object có thể chứa các object bên trong. Trong Elasticsearch, chúng sẽ được `flattened` trước khi lập index và được lưu trữ dưới dạng các key-value pair đơn giản, ví dụ:
```json
{
	"message": "Some text...",
	"customer.age": 26,
	"customer.address.city": "Copenhagen",
	"customer.address.country": "Denmark"
}
```

Customer là một `object` chứa `age` property, age property này sẽ được lưu trữ trong một field tên là `customer.age`, tương tự với `customer.address.city` và `customer.address.country`.

### Array

Elasticsearch có các Array data type như sau:.

- Array of strings: `[“Elasticsearch”, “rocks”]`
- Array of integers: `[1, 2]`
- Array of arrays: `[1, [2, 3]] – equivalent of [1, 2, 3]`
- Array of objects: `[{ “name”: “Andy”, “age”: 26 }, { “name”: “Brenda”, “age”: 32 }]`

Elasticsearch sẽ tiến hành `flattens` các documents, do đó trong trường hợp `Arrays – Objects` này, Elasticsearch sẽ sắp xếp lại như sau: `{ "users.name": ["Andy", "Brenda"], "users.age": [32, 26] }`. Tuy nhiên làm như vậy thì các object đã bị trộn lẫn vào nhau, nên Elasticsearch mới có khái niệm `nested data type`.

### Nested

Kiểu dữ liệu này nên được sử dụng khi ta cần lập index các Array of objects như trên và vẫn duy trì tính độc lập của từng objects. Các giá trị của tất cả các objects sẽ không bị trộn lẫn với nhau và bên trong mỗi objects này sẽ được lập index riêng biệt. 

## Geo Data Types

Geo Data Types dùng để lưu trữ dữ liệu địa lý - `geographical data` và được Elasticsearch chia làm 2 loại là `Geo-point` và `Geo-shape`


### Geo-point

`geo-point` data type được dùng để lưu trữ tọa độ của một vị trí địa lý, gồm vĩ độ và kinh độ - `latitude-longitude pairs` và có thể được sử dụng để tìm kiếm documents trong bán kính của tọa độ, sắp xếp theo khoảng cách từ các tọa độ với nhau, v.v. `geo-point` được Elasticsearch chia làm 4 formats khác nhau:

- `lat` and `lon` properties.

```json
{
	"location": { 
		"lat": 33.5206608,
		"lon": -86.8024900
	}
}
```

- Separated by a comma

```json
{
	"location": "33.5206608,-86.8024900" 
}
```

- geohash

```json
{
	"location": "drm3btev3e86" 
}
```

- Array

```json
{
	"location": [-86.8024900,33.5206608] 
}
```

### Geo-shape

`Geo-shape` có thể chứa các hình dạng như hình chữ nhật và đa giác, do đó có thể được sử dụng để tạo các hình dạng phức tạp.Kiểu dữ liệu này nên được sử dụng khi dùng `Geo-point` thôi chưa đủ. Một `Geo-shape` có thể được xây dựng theo nhiều cách, một trong số đó là thêm nó dưới dạng `linestring` hoặc `polygon`. 

- `linestring` là một mảng có hai hoặc nhiều vị trí, về bản chất là một mảng của các mảng. Nếu mảng chỉ chứa hai vị trí, thì kết quả là một đường thẳng. 

- `polygon` là một đa giác dưới dạng một mảng các mảng, trong đó mỗi mảng chứa các điểm. Điểm đầu tiên và điểm cuối cùng trong mảng phải giống nhau, điểm này sẽ đóng đa giác.

## Specialized Data Types

Trong Elasticsearch có một số kiểu dữ liệu hơi đặc biệt, gọi chung là `Specialized Data Types`. Có thể kể đến là `ip data types` dùng để ánh xạ cho kiểu dữ liệu dưới IPv4 và IPv6 format; `Token Count` để phân tích số lượng token hay `Attachment` cho phép Elasticsearch lập index các tệp đính kèm với nhiều định dạng phổ biến như tệp PDF, spreadsheets, PowerPoint v.vv.


## Reference

1. [Field Data type - elastic documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html#mapping-types)

2. [Data types - elastic documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/sql-data-types.html)

3. [Field Data Types - codingexplained.com](https://codingexplained.com/coding/elasticsearch/field-data-types)