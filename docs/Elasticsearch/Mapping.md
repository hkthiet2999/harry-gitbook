---
author: Harry Hoang
date: 2022-02-08
---

# Mapping

![](./images/mapping-banner.jpg)

## About Mapping
???+ info "Mapping"

    Mapping is the process of defining how a document, and the fields it contains, are stored and indexed


`Mapping` là quá trình xử lý cách mà các document (và các properties bên trong document đó) sẽ được index và lưu trữ như thế nào. Mapping giúp chúng ta cùng lúc khởi tạo 1 field & định nghĩa cách field đó được index (thông qua cơ chế Analyzer), ví dụ:

- Những field nào sẽ có kiểu `number`, `date` hay `geolocations`

- Với string field thì những string field nào sẽ được xử lí dưới dạng `Full text field`

- format của các field, ví dụ với `"type": "date"`

Như mình đã tìm hiểu trước đó, mỗi `document` là một tập hợp các `fields`, mỗi `field` sẽ có một `data type`. Khi thực hiện `mapping` data của document, ES sẽ tạo một `mapping definition` chứa danh sách các `fields` và  `metadata fields`( như `_source field`) của document và customize cách xử lý các metadata trong `metadata fields`.


## Mapping Options

Use dynamic mapping and explicit mapping to define your data. Each method provides different benefits based on where you are in your data journey. For example, explicitly map fields where you don’t want to use the defaults, or to gain greater control over which fields are created. You can then allow Elasticsearch to add other fields dynamically.

Có hai `Mapping Options` là `dynamic mapping` và `explicit mapping` dùng để define data. 
Trước ES v.7.0.0, `mapping definition` bao gồm a `type name` và accept cái `default mapping` làm Mapping options mặc định. Từ ES v7.0+ không còn accept cái default mapping nữa. Xem thêm [Removal of mapping types](https://www.elastic.co/guide/en/elasticsearch/reference/current/removal-of-types.html).


Mỗi phương pháp cung cấp các lợi ích khác nhau, ví dụ dùng `explicit mapping` trong trường hợp không muốn các fields sử dụng giá trị mặc định hoặc để có được quyền kiểm soát các fields tốt hơn, saau đó vẫn có thể cho phép Elasticsearch thêm dynamic mapping cho các fields khác.

### Dynamic mapping

Dynamic mapping cho phép ta `experiment` và `explore` data trong các bước mapping ban đầu. Khi đó Elasticsearch sẽ tự động thêm các fields mới ngay khi document được index. Với option này, ta có thể thêm các fields vào `top-level mapping` - mapping cấp cao nhất và thêm các fields làm 1 object bên trong các fields lồng nhau.

Dynamic mapping có các `dynamic templates` để `define custom mappings`, được áp dụng cho các fields được thêm động dựa trên các điều kiện phù hợp, từ đó cho phép ta kiểm soát tốt hơn cách Elasticsearch mapping dữ liệu ngoài các [dynamic field mapping rules.](https://www.elastic.co/guide/en/elasticsearch/reference/current/dynamic-field-mapping.html) mặc định

Ta có thể enable `dynamic mapping` bằng cách set cái `dynamic parameter` thành `true` hoặc `runtime`. Sau đó có thể dùng `dynamic templates` để define custom mappings có thể áp dụng cho các fileds dựa trên các điều kiện:

- `match_mapping_type` hoạt động trên các data types mà Elasticsearch có thể detects. Bộ detect của ES có 1 vài giới hạn nhất định: 
chỉ 1 vài datatype có thể được detect, bao gồm `boolean`, `date`, `double`, `long`, `object`, `string`. Tùy từng `dynamic parameter` là `true` hay `runtime` mà ES detect cái data types theo cách khác nhau, xem cụ thể tại [Elasticsearch automatically detects data types](https://www.elastic.co/guide/en/elasticsearch/reference/current/dynamic-templates.html#template-variables)

- `match` và `unmatch` là các parameter của `match_pattern`, dùng để set `match` hoặc `unmatch` các field name, ví dụ:

```json
"match_pattern": "regex",
"match": "^profit_\d+$"
```

- `path_match` và `path_unmatch` tương tự như `match` và `unmatch` nhưng hoạt động trên các `full dotted path` của field chứ không chỉ là field name, ví dụ: `some_object.*.some_field`

Template này sẽ được process theo thứ tự: Template match đầu tiên được sử dụng &rarr; Template mới được apply sẽ được append vào Template List thông qua `PUT Mapping`. Nếu template mới có tên trùng với template cũ, template cũ sẽ được thay thế bẳng template mới này.

### Explicit mapping

`Explicit mapping` cho phép ta chọn chính xác `mapping definition` - tức là có thể định nghĩa mapping cho các fields ngay khi index được tạ, ví dụ:

- string fields nào là `full text fields`.

- Những fields nào chứa numbers, dates, hoặc geolocations.

- format của date values.

- Tùy chỉnh thêm các quy tắc dùng để kiểm soát việc mapping cho các fields được thêm động.

Ngoài ra, với Explicit mapping ta có thể thêm field vào các index đã tồn tại thông qua PUT Mapping, ví dụ:

```json
PUT my_index 
{
  "mappings": {
    "doc": { 
      "properties": { 
        "title":    { "type": "text"  }, 
        "name":     { "type": "text"  }, 
        "age":      { "type": "integer" },  
        "created":  {
          "type":   "date", 
          "format": "strict_date_optional_time||epoch_millis"
        }
      }
    }
  }
}
```

Explicit mapping sử dụng [runtime fields](https://www.elastic.co/guide/en/elasticsearch/reference/current/runtime-mapping-fields.html) để thực hiện các schema changes mà không cần reindexing. Có thể sử dụng `runtime fields` kết hợp với `indexed fields` để cân bằng giữa việc sử dụng tài nguyên và tối ưu hiệu suất - mapping mà cần nhiều resource sẽ tốn performance.


## Prevent mapping explosion

Việc define quá nhiều fields trong một index có thể dẫn đến trường hợp `mapping explosion`, có thể gây ra lỗi hết bộ nhớ và các tình huống khó khôi phục khác. ES hỗ trọ `mapping limit settings` để giới hạn số lượng field được mappings được tạo thủ công hoặc tự động, từ đó tránh được hiện tượng `mapping explosion`

Lấy ví dụ với một vài mapping limit settings:

- `index.mapping.total_fields.limit`: Set số lượng fields tối đa trong một index. Giá trị mặc định là 1000.

- `index.mapping.depth.limit`: Độ depth tối đa của field, tính bằng số lượng của inner objects. Ví dụ: tất cả các field được xác định là `root object level`, thì depth là 1. Nếu có một object mapping tới các filed này thì depth của nó là 2, v.v. Mặc định là 20.

Ngoài ra còn có các mapping limit settings khác như `index.mapping.nested_fields.limit` và `index.mapping.nested_objects.limit` để setting cho các nested fields, nested objects hay `index.mapping.field_name_length.limit`, `index.mapping.dimension_fields.limit`. Xem đầy đủ tại [Mapping limit settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-settings-limit.html)

## Removal of mapping types

### Mapping types

Elasticsearch được tổ chức thành các index, bên trong index là các type (hay còn được gọi là `mapping type`). Các index tương đương với database trong một Database Driver, còn type tương đương với table. 

Ví dụ với table trong mysql, với 2 table khác nhau có tên filed giống nhau thì kiểu dữ liệu vẫn có thể khác nhau:
- table `shop` và table `session` đều có `id` filed 
- table `shop` thì `id` filed có kiểu `int`
- table `session` thì `id` filed có kiểu `string`

2 table này không liên quan đến nhau thì sẽ không có vấn đề gì. Tuy nhiên trong Elasticsearch thì không thế. Bởi vì `data types` sẽ đi theo index => kể cả các type khác nhau thì data type của filed đó cũng sẽ không được thay đổi. Ví dụ cùng trong  1 index `ecommerce`:
- Type `shop` có `id` filed là kiểu `numberic` (long)
- Type `session` có `id` filed là kiểu `string`
Khi `session` insert vào mapping sẽ bị lỗi do data types không tương thích. Vì data types được đánh theo index, không phải theo từng type.

&rarr; Điều này dẫn tới nhiều user hiểu nhầm &rarr; dùng sai &rarr; ES quyết định bỏ dần từ ES v5.6, đến ES v7.0+ là chính thức bỏ hẳn khái niệm Mapping type, thay vào đó là cơ chế Mapping khác dùng tiện hơn

### Alternatives to mapping types
ES hỗ trợ 2 cách thay thế cho mapping types:

- `Index per document type`: Lập index cho từng document luôn, tức là index là table để tiện cho việc define data types. Khi nào cần thì điều chỉnh số `primary_shard` của từng index cho phù hợp với bài toán lưu trữ cụ thể, tránh dư thừa.

- `Custom type field`: Sử dụng 1 field để lưu data types. Ví dụ bình thường lưu 2 type cho `shop`, `session` thì bây giờ trong mỗi index, thêm 1 field là type, có value là string, number gì đó, khi search thì kèm thêm cái type này vào query là ok.

## Examples
- Tạo một index với predefined mapping:

```json
PUT /my_index?pretty
{
  "settings": {
    "number_of_shards": 1
  },
  "mappings": {
    "properties": {
      "name": {
        "type": "text"
      },
      "age": {
        "type": "integer"
      }
    }
  }
}
```

- Sau đó mapping cái index này:

```json
PUT /my_index/_mapping?pretty
{
  "properties": {
    "email": {
      "type": "keyword"
    }
  }
}
```

ES sẽ tiến hàng mapping cái index trên, có thể view bằng 

```json
GET my_index/_mapping?pretty
```
hoặc 

```json
GET /my_index/_mapping/field/name?pretty
```


## Reference

1. [Elasticsearch Mapping: The Basics, Updates & Examples - logz.io](https://logz.io/blog/elasticsearch-mapping/)

2. [Elasticsearch Mapping - opster.com](https://opster.com/guides/elasticsearch/glossary/elasticsearch-mapping/)

3. [Mapping - elastic document - current version](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html)

4. [Mapping limit settings - elastic document](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-settings-limit.html)

5. [Removal of mapping types](https://www.elastic.co/guide/en/elasticsearch/reference/6.8/removal-of-types.html)

6. [Elasticsearch Mapping - tutorialspoint.com](https://www.tutorialspoint.com/elasticsearch/elasticsearch_mapping.htm)