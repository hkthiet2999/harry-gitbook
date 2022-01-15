---
author: Harry Hoang
date: 2022-01-10
---
# Supervisor and workers management

## Overview
```
Supervisor is a client/server system that allows its users to control a number of processes on UNIX-like operating systems.
```

- `Supervisor` là một hệ thống `client/server` giúp quản lý các tiến trình chạy trên Linux (hoặc UNIX-like).

- Một số ưu điểm mà Supervisor như:

    + `Convenience`: Tính tiện dụng ở đây là Supervisor bắt đầu `processes` khi `subprocesses` của nó và có thể được định cấu hình để tự động khởi động lại chúng khi gặp sự cố. Nó cũng có thể tự động được cấu hình để bắt đầu các `processes` trên lệnh gọi của chính nó luôn.

    + `Accuracy`: Supervisord luôn kiểm soát được trạng thái up/down thực sự của các `subprocesses` và có thể được truy vấn chính xác status này bất cứ lsuc nào.

    + `Delegation`: Đảm bảo một tiến trình nào đó luôn luôn chạy không ngừng nghỉ. Nếu vì lý do gì mà nó bị tắt, Supervisor sẽ khởi động `process` đó lại.

    + `Process Groups`: Quản lý nhiều tiến trình dưới dạng một group các tiến trình, từ đó có thể được bật/tắt cùng lúc.
  
    + Trong trường hợp tiến trình mà supervisor thực thi phát sinh lỗi, có thể cấu hình để Supervisor retry lại một số lần nhất định trước khi chính thức báo fail.

## Features
Supervisor có các tiện ích sau:

- `Simple`- Đơn giản:  được cấu hình thông qua tệp cấu hình kiểu INI-style, đơn giản dễ học. Nó cung cấp nhiều tùy chọn cho mỗi process như khởi động lại các process bị lỗi và tự động hóa việc ghi log.

- `Centralized` - Tập trung: Supervisor cung cấp cơ chế để start, stop, và monitor các process theo kiểu riêng lẻ từng process hoặc nhóm các process.

- `Efficient` - Hiệu quả: Supervisor start các `subprocesses` của nó thông qua cơ chế `fork/execute` và các `subprocesses` không `daemonize`, tăng hiệu năng.

- `Extensible` - Có thể mở rộng: Supervisor có một giao thức `event notification protocol` dùng để thông báo sự kiện,  các chương trình được viết bằng bất kỳ ngôn ngữ nào có thể sử dụng để theo dõi các `event` và dùng `XML-RPC interface` để quản lý.

- `Compatible` - Tương thích: Supervisor hoạt động trên mọi thứ ngoại trừ Windows. Nó hỗ trợ trên Linux, Mac OS X, Solaris và FreeBSD. Nó được viết hoàn toàn bằng Python, vì vậy việc cài đặt không yêu cầu `C-compiler`.

- `Proven`: Supervisor đã xuất hiện trong nhiều năm và đã được sử dụng trên nhiều máy chủ.
## Supervisor Components

`Supervisor` có 2 phần là `supervisord` (server) và `supervisorctl` (client). Thiết kế như vậy để ta có thể dựng nhiều server và dùng client kết nối tới nhiều server để quản lý.

- `Supervisord` (vai trò server) : Hay còn gọi là `supervisor daemon` đóng vai trò như server, chịu trách nhiệm start các programs, trả lời các lệnh từ client, restart các subprocess bị crash hoặc tắt, ghi log stdout & stderr từ các subprocess và xử lý các events tương ứng trong vòng đời của 1 subproces. Server này sẽ xử lý dựa trên file config dạng "Windows-INI". Mặc định là `/etc/supervisord.conf`.

- `Supervisorctl` (vai trò client) : cung cấp giao diện dòng lệnh để ta thao tác, ra lệnh cho remote server (supervisord. Từ `supervisorctl`, ta có thể connect tới supervisord, stop, start, lấy status của các subprocesses. client sẽ nói chuyện với server qua UNIX domain socket hay TCP socket.


## Reference

1. [Supervisord introduction](http://supervisord.org/introduction.html)