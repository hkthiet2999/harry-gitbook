---
author: Harry Hoang
date: 2022-01-17
---
# Composer

- Install/remove package 

- Package version constrains & composer.lock 

- Auto loading

## Overview

- `Composer` là công cụ để quản lý package hay library của PHP. Về cơ cản, Composer sẽ không cài package ở global và gọi là `Dependency` &rarr;  Composer là công cụ quản lý các Dependency vì thế nó còn được gọi là `Dependency Manager`. 

- Tương tự như `npm` hay `bundle`, `composer` ra đời để giải quyết các vấn đề khó khăn như khi dung lượng project lớn, việc cập nhật cũng như chèn các package hay library vào project rất phức tạp và phiền phức. Với `composer`, chỉ cần khai báo `name` và `version` của các package hay library, `composer` sẽ tự động tìm và tải các package hay library mà mình cần về project.

- `Composer` quản lý `dependencies` dựa trên từng Project PHP riêng biệt, nó cài đặt các `dependencies` này vào một folder `vendor` trong dự án (mỗi dự án có một thư mục vendor riêng). `Composer` tự động sinh ra file` vendor/autoload.php`, từ file này giúp ta nạp các `dependencies` đã cài đặt vào project.

- `composer.json`: Là nơi khai báo dependencies dùng trong project, những thông tin về name, version, licenses, source … được declare theo JSON format.

```
{
    "name": "wataridori/bphalcon",
    "type": "project",
    "description": "A small library which implement some features to phalcon",
    "license": "GPL-3.0",
    "authors": [
        {
            "name": "Harry Hoang",
            "email": "harry.hoang@contemi.com"
        }
    ],
    "require": {
        "php": ">=5.4"
    }
}
```

- `composer.lock`: Là nơi lưu trữ thông tin về dependencies đã được cài đặt. 


- `composer.json` vs. `composer.lock`: Ví dụ khi ta dùng lệnh install để cài đặt package thì composer sẽ đọc thông tin về dependencies ở trong file `composer.json`, sau đó cài đặt và tạo ra file composer.lock để lưu thông tin cụ thể về những dependencies đó. Giả sử ta commit cả 2 file `composer.json` và `composer.lock` vào `version control` của mình, rồi bất cứ ông dev nào tải code về thì dù có cài đặt vào thời điểm khác nhau đi chăng nữa thì vẫn sẽ nhận được những dependencies với những version giống nhau, do nó được đọc từ file `composer.lock`, chứ không phải file `composer.json`.
## Install/remove package

Danh sách các [package](https://packagist.org/) của PHP

### Install a package

- `require`
    ```
    composer require <package>[:<tag>]
    ```

    + Câu lệnh trên sẽ thêm mới một library hay package và ghi vào file `composer.json` tại current directory.

    + Options: 
        + `--dev`: Thêm packages vào `require-dev`, dùng package này để dev.
        + xem full [tại](https://getcomposer.org/doc/03-cli.md#require)

    + Ví dụ, install thư viện `monolog/monolog` phiên bản mới nhất (thư viện lưu log thông dụng cho php):

    ```
    composer require monolog/monolog
    ```

    Sau lệnh này, Composer sẽ tải tất cả các `dependencies` để dùng được thư viện `monolog/monolog` vào dự án, sau đó nó lưu tại thư mục `vendor`, đồng thời cũng có luôn file `vendor/autoload.php`

    Mở lại file composer.json ta thấy đã có thêm đoạn code:
    ```
    {
        "require": {
            "monolog/monolog": "^1.24"
        }
    }
    ```


- `install`, `update` và `reinstall`

    Có hai câu lệnh dùng để tải, cập nhật package dựa trên 2 file `package.json` và `package.lock`:
    
    ```
    composer install
    ```
    
    Tương tự như `require`, `install` dùng để tải package, nhưng khác là package đó phải được declare bằng 1 json object trong `composer.json`. Khi chạy lệnh `instal`, composer tiến hành đọc file `package.lock` và `composer.json`, tải các dependencies và lưu vào `vendor`.

    ```
    composer update
    ```

    Dùng để tải phiên bản mới nhất của các dependencies và cập nhật tệp `composer.lock`. Nó sẽ thêm hoặc xóa các `dependencies` dựa trên `composer.json`, ignored `composer.lock`.

    ```
    composer reinstall
    ```

    Cơ chế install tương tự như `install` nhưng trước tiên nó tiến hành `looks up installed packages by name` trong `composer.json`, xóa hết packages cũ rồi mới install.

### Remove a package
- Ngược lại với require, command này thực hiện delete package dựa trên `composer.json`

    ```
    composer remove <package>
    ```

- Có options là `--dev`, chỉ remove các package được khai báo trong `require-dev`

- Ngoài ra, cách 2 để remove packages, mở file `composer.json`, xóa tên thư viện đó trong phần require, sau đó chạy lệnh
```
composer update
```
_xem thêm các [Command-line interface/Commands](https://getcomposer.org/doc/03-cli.md) của Composer_
## Package version constrains & composer.lock 

- `Package version constrains` là những ràng buộc về phiên bản của packages theo đúng nghĩa đen.

- `Composer Versions Constrains` tuân theo `Version Control System (VCS)`, tương tự như Git, cũng có các khái niệm như:
    + Tags: `v1.0.1`
    + Branches: `v1.x-dev` 
    + Stabilities: `v1.1-BETA`
    + Version Range: sử dụng các operators `>`, `>=`, `<`, `<=`, `!=`
        + `>=1.0`
        + `>=1.0 <2.0`
        + `>=1.0 <1.1 || >=1.2`
    + Hyphenated Version Range (`-`): Thay vì dùng `>=1.0.0 <=2.1.0`, có thể thay bằng `1.0.0 - 2.1.0` cho gọn

    + Wildcard Version Range (`.*`): Thay vì dùng ` >=1.0.0 <1.1.0`, có thể thay bằng `1.0.*` cho gọn

    + Tilde Version Range (`~`): `~1.2` tương đương với `>=1.2 <2.0.0`, hay `~1.2.3` tương đương với `>=1.2.3 <1.3.0`

    + Caret Version Range (`^`): `^1.2.3` tương đướng với `>=1.2.3 <2.0.0`, hay `^0.3` tương đướng với `>=0.3.0 <0.4.0`.

- Stability Constraints: Stability dùng trong các thay đổi lớn của version, giúp tăng tính rõ ràng, minh bạch. Nếu không xác định rõ `Stability` trong version, Composer sẽ thêm các hậu tố sau version một các `Internally`, thường mặc định thành `-dev` hoặc `-stable`. Ví dụ:

| Constraint  | Internally |
| ----------- | ----------- |
| `1.2.3` | `=1.2.3.0-stable` |
| `>1.2` | `>1.2.0.0-stable` |
| `>=1.2` | `>=1.2.0.0-dev` |
| `>=1.2-stable` | `>=1.2.0.0-stable` |
| `<1.3` | `<1.3.0.0-dev` |
| `<=1.3` | `<=1.3.0.0-stable` |
| `1 - 2` | `>=1.0.0.0-dev <3.0.0.0-dev` |
| `~1.3` | `>=1.3.0.0-dev <2.0.0.0-dev` |
| `1.4.*` | `>=1.4.0.0-dev <1.5.0.0-dev` |

### Summary

```json
"require": {
    "vendor/package": "1.3.2", // exactly 1.3.2

    // >, <, >=, <= | specify upper / lower bounds
    "vendor/package": ">=1.3.2", // anything above or equal to 1.3.2
    "vendor/package": "<1.3.2", // anything below 1.3.2

    // * | wildcard
    "vendor/package": "1.3.*", // >=1.3.0 <1.4.0

    // ~ | allows last digit specified to go up
    "vendor/package": "~1.3.2", // >=1.3.2 <1.4.0
    "vendor/package": "~1.3", // >=1.3.0 <2.0.0

    // ^ | doesn't allow breaking changes (major version fixed - following semver)
    "vendor/package": "^1.3.2", // >=1.3.2 <2.0.0
    "vendor/package": "^0.3.2", // >=0.3.2 <0.4.0 // except if major version is 0
}
```
## Auto loading

### PSR
- `PSR` - `PHP Standards Recommendations`, nó là tiêu chuẩn được khuyến nghị áp dụng khi lập trình PHP, nó vẫn đang hoàn chỉnh, trong đó khá nhiều tiêu chuẩn con đã hoàn chỉnh và được các lập trình viên, tổ chức chấp nhận sử dụng. Sử dụng PSR để đảm bảo thống nhất về cách thức viết code, tổ chức ứng dụng ... nhằm dễ quản lý, đọc, và sử dụng lại giữa các Framework ... đồng thời đảm bảo có một giao diện lập trình chung giữa các ứng dụng,các Framework, khi nó cùng thực hiện một chức năng.

- Danh sách các PSR tại [php-fig.org](http://www.php-fig.org/psr/). Đến nay có 18 tiêu chuẩn từ `PSR-0` đến `PSR-17`, trong đó có các tiêu chuẩn đã được phê duyệt có các tiêu chuẩn đang soạn thảo và có tiêu chuẩn đã lỗi thời (ví dụ PSR-0 đã lỗi thời, bị thay bởi PSR-4).

- Các tiêu chuẩn PSR should know:
    + `PSR-1` - Basic Coding Standard: Tiêu chuẩn về viết code
    + `PSR-2`- Coding Style Guide: Tiêu chuẩn về trình bày code
    + `PSR-3` - Logger Interface: Trình bày về các thành phần cần phải có của một Logger
    + `PSR-4` - Autoloading Standard:  Trình bày về cách chỉ định ứng dụng tự động nạp (giống include, require) các file php, lớp, hàm khi nó cần dùng đến.
    + `PSR-6` -  Caching Interface: Tiêu chuẩn cần có của một bộ ứng dụng caching
    + `PSR-7` -  HTTP Message Interface: Tiêu chuẩn về interface của một ứng dụng sử HTTP Message - request và respone
### PSR-4 Autoloader
- Trước đây trong PHP việc nạp các file thư viện, mã dùng lại vào một file PHP khác thường dùng các lệnh include và require. Điều này gây mất thời gian, rắc rối, dài code.
```php
    <?php
        include __DIR__ . '/classes/MyClass.php';
        include __DIR__ . '/classes/Foo.php';
        include __DIR__ . '/classes/Bar.php';
        // ...

        $obj = new MyClass;
        $foo = new Foo;
        $bar = new Bar;
        // ...
    ?>
```

- Tiếp theo từ PHP5 có các hàm trợ giúp tự động hóa việc gọi thư viện bằng các hàm như: `__autoload`, `spl_autoload_register`, `spl_autoload_functions`, `spl_autoload_extensions` ...


```php
<?php
    spl_autoload_register(function ($classname) {
        include __DIR__ . </classes/< . $classname . <.php<;
    });

    $myClass = new MyClass;
    $foo = new Foo;
    $bar = new Bar;
?>
```

- Tuy nhiên để dễ dàng chia sẻ code, dùng lại code giữa các framework, giữa các dự án ..., cộng đồng PHP thống nhất một cách thức tự động nạp thư viện theo một chuẩn  là `PSR-4 Autoload`. Ngoài tiêu chuẩn tự động load PSR-4 còn có tiêu chuẩn tự động load theo PSR-0 (tuy nhiên đã lỗi thời, các dự án mới không nên theo PSR-0 nữa). 


- `PSR-4 Autoload`: Phải có một có chế và cách bố trí code trong các thư mục sao cho mọi class đều có thể được tham chiếu đến bằng cách viết code như sau:
    ```
    \<NamespaceName>(\<SubNamespaceNames>)*\<ClassName>
    ```

Có nghĩa là mỗi lớp ta phải xây dựng sao cho có thể được tham chiếu đến bởi dòng code ba thành phần: `Namespace`, các `SubNamespaceNames` con, và tên lớp `ClassName`.

+ `NameSpace` : Tiền đố đầu tiên bắt buộc phải có. Tên này do ta tự đặt, sao cho không xung đột tên các thư viện khác.

+ `SubNameSpaces`: Các namespace con (theo sau NameSpace đầu tiên). Có một hoặc nhiều tùy dự án mình config. Nhưng bắt đầu từ `SubNameSpace` phải tương ứng với cấu trúc thư mục lưu trữ code. 

+ `ClassName`: Bắt buộc phải có và phải có tên file PHP trùng tên `ClassName` ở thư mục tương ứng với namespace cuối cùng (vd ClassName.php), trong file đó sẽ định nghĩa nội dung của code của class mình cần load.

Đó là cách thống nhất viết bố trí code PHP trên các thư mục và theo các `namespace`. Khi đã viết code tuân thủ theo hướng dẫn này thì các famework khác nhau đều sử dụng một cơ chế tự động nạp tương tự nhau nên có thể dùng lại thư viện. 

### Composer và PSR-4 : Autoload

- Composer cung cấp 1 module `autoload`, tuân theo chuẩn `PSR-4`. Cụ thể mỗi package trong dự án nằm theo cấu trúc `vendor/package-name`. Sau đó, để đảm bảo `vendor/autoload.php` được gọi, ta cần cập nhật `composer.json` dùng dependency `autoload`:

```
{
    "autoload": {
        "psr-4": {
            "MyCompany\\": "src/",
         }
    }
}
```

Khai báo composer.json như trên xong, gõ lệnh:
```
composer dum-autoload
```

_Example_

- Xây dựng một lớp có tên `FirstClass`, có namespace là `MyCompany/Mymodule`. Code file lưu trong file `src/Mymodule/FirstClass.php`.

```php
<?php
    namespace MyCompany\Mymodule

    class FirstClass {
        function helloComposer()
        {

        }
    }
?>
```
Như trên là đã đúng chuẩn `PRS-4`, composer sẽ giúp ta tích hợp vào `vendor/autoload.php`, để có thể tự động include có trên khi cần dùng đến bằng đoạn code ví dụ:
```php
<?php

    $cls = new MyCompany\Mymodule\FirstClass();
?>

//Hoặc

<?php
    use MyCompany\Mymodule;

    $cls = new FirstClass();
?>
```
## Reference

1. [Difference between composer install , composer update and composer require](https://ourcodeworld.com/articles/read/72/what-s-the-difference-between-composer-install-composer-update-and-composer-require)

2. [Versions and constraints](https://getcomposer.org/doc/articles/versions.md)

3. [Composer - Basic usage](https://getcomposer.org/doc/01-basic-usage.md)

4. [Composer - Command-line interface/Commands](https://getcomposer.org/doc/03-cli.md)

5. [Standard autoloader](http://framework.zend.com/manual/current/en/modules/zend.loader.standard-autoloader.html)

6. [PSR-4 Autoloader - Tiêu chuẩn viết tự động nạp khởi tạo PHP](https://xuanthulab.net/psr-4-autoloader-tieu-chuan-viet-tu-dong-nap-khoi-tao-php.html)

