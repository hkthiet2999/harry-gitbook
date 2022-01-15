---
author: Harry Hoang
date: 2022-01-10
---

# Linux Commands

## Basic file and directory management & permission commands
1. Điều hướng file system
*Điều hướng tới thư mục chỉ định*

```
$ cd ~/.ssh/
```

*Điều hướng quay lại thư mục cha*

```
$ cd ../Documents
```

*Tạo file mới*

```
$ touch hello.txt
```

*Copy file hoặc directory*

```
$ cp hello.txt hello.txt
```

*Rename file*

```
$ mv hello.txt bonjour.txt
```

*Remove file*

```
$ rm ciao.txt
```

*Femove files không cần xác nhận và remove các file con của nó*

```
$ rm -rf ~/Downloads
```

*Xem list các file trong thư mục hiện tại*

```
$ ls ~/Downloads
```

2. `cat`, `grep`, và `piping`

*Concatenate file, hoặc dùng để xem nội dung file*

```
$ cat hello.txt
```

*`cat` kết hợp với `grep` để search*
```
$ cat guest_list.txt | grep Lucy
```

```
$ cat /var/log/messages | grep '500 Internal Server Error'
```

*Dùng grep để tìm object (any kind of output, not just file contents)*

```
$ docker ps | grep my-awesome-container
```

*Lưu output của bất kỳ lệnh nào vào một tệp bằng cách sử dụng redirection `(>)`*

```
$ echo "Linux was created by Linus Torvalds" > bio.txt
```

3. `find`

*Tìm thư mục bằng name*

```
$ find . -name CS101
```

4. File permissions và ownership

Mọi tệp và thư mục trong `File system` của Linux đều có `permissions ` và `owner`. Để xem thông tin về `permissions ` và `owner` của một file:

```
-rw-r--r--
```

*Đổi onwer*

```
$ su sudo
```

*Đổi permissions*

```
$ chmod u=rwx,g=rx,o=r hello.txt
```

*Set permissions*

```
$ chmod 766 hello.txt
```

```
$ chown <your_user>:<your_group> hello.txt
```

5. `reverse-i-search`

`reverse-i-search` là một tiện ích dùng để tìm kiếm lại lịch sử lệnh và chạy lại lệnh trước đó, dùng Ctrl + R

## Package install/remove commands

*Liệt kê tất cả available packages*

```
$ apt-cache pkgnames
```

*Tìm Package Name and Description của Software*

```
$ apt-cache search vsftpd
```


*Xem thông tin của Package*

```
$ apt-cache show netcat
```

*Xem Dependencies của Specific Packages*

```
$ apt-cache showpkg vsftpd
```

*Xem statistics của Cache*

```
$ apt-cache stats
```

*Update System Packages*
```
$ sudo apt-get update
```

*Upgrade Software Packages*

```
$ sudo apt-get upgrade
```

*Install hoặc Upgrade Specific Packages*

```
$ sudo apt-get install netcat
```

*Install Multiple Packages*

```
$ sudo apt-get install nethogs goaccess
```

*Install Several Packages sử dụng Wildcard*

```
$ sudo apt-get install '*name*'
```

 `'*name*'` kiểu string, tên của `package-name`.

*Install Packages không cần Upgrading*

```
$ sudo apt-get install packageName --no-upgrade
```

*Chỉ Upgrade Specific Packages*

```
$ sudo apt-get install packageName --only-upgrade
```

*Install Specific Package theo Version*

```
$ sudo apt-get install vsftpd=2.3.5-3ubuntu1
```

*Remove Packages không cần cấu hình*

```
$ sudo apt-get remove vsftpd
```

*Remove hoàn toàn Packages*

```
$ sudo apt-get purge vsftpd
```

*Dọn dẹp Disk Space*

```
$ sudo apt-get clean
```

*Download mỗi Source Code của Package*

```
$ sudo apt-get --download-only source vsftpd
```

*Download sau đó Unpack thằng Package*
```
$ sudo apt-get source vsftpd
```

*Download rồi Unpack xong Compile thằng Package*

```
$ sudo apt-get --compile source goaccess
```

*Download Package mà không cài đặt nó*

```
$ sudo apt-get download nethogs
```

*Xem Change Log của Package*

```
$ sudo apt-get changelog vsftpd
```

*Xem Broken Dependencies*

```
$ sudo apt-get check
```

*Search và Build Dependencies*

```
$ sudo apt-get build-dep netcat
```

*Auto clean Apt-Get Cache*

```
$ sudo apt-get autoclean
```

*Auto remove Installed Packages*

```
$ sudo apt-get autoremove vsftpd
```


## Reference
1. [25 Useful Basic Commands of APT-GET and APT-CACHE for Package Management](https://www.tecmint.com/useful-basic-commands-of-apt-get-and-apt-cache-for-package-management/)

2. [37 Important Linux Commands You Should Know](https://www.howtogeek.com/412055/37-important-linux-commands-you-should-know/)

3. [10 Things Every Linux Beginner Should Know](https://www.codementor.io/linux/tutorial/10-things-every-linux-beginner-should-know)