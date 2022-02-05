---
author: Harry Hoang
date: 2022-01-27
---

# Transactions

## Overviews

`Transactions` trong ORM được ánh xạ từ khái niệm Transactions trong Database, được thể hiện bằng một nhóm tuần tự các câu lệnh, truy vấn hoặc các actions như select, insert, update hay delete và đều được thể hiện qua các module trong source code. Tùy từng ORM framework sẽ có các module khác nhau, nhưng nhìn chung đều có mục đích là thực hiện một Transactions tới Database như `single work unit` và nhận về kết quả là `committed` hoặc `rolled back`.

## Transactions in TypeORM

`TypeORM` là một ORM, có thể chạy trên các nền tảng NodeJS, Browser, Cordova, PhoneGap, Ionic, React Native, NativeScript, Expo và Electron và còn dùng được với TypeScript và JavaScript (ES5, ES6, ES7, ES8). TypeORM hỗ trợ cả `Active Record pattern` và `Data Mapper pattern`.

### Creating and using transactions
Trong TypeORM, một transactions được tạo ra bằng việc sử dụng `getConnection` hoặc `getManager`:

``` typescript title="using getConnection"
import {getConnection} from "typeorm";

await getConnection().transaction(async transactionalEntityManager => {
    
});
```

``` typescript title="using getManager"
import {getManager} from "typeorm";

await getManager().transaction(async transactionalEntityManager => {
    
});
```

Để dùng các Operations trong một Transactions, trong TypeORM ta có thể truyền các Operatinos vào `callback` của `transactionalEntityManager()` như sau:

``` typescript
import {getManager} from "typeorm";

await getManager().transaction(async transactionalEntityManager => {
    await transactionalEntityManager.save(users);
    await transactionalEntityManager.save(photos);
    // ...
});
```

### Specifying Isolation Levels

Việc chỉ định `isolation level` cho transation trong TypeORM được thực hiện bằng cách cung cấp `first parameter` cho `transaction()`, như code dưới đây đang dùng `SERIALIZABLE isolation level`:

``` typescript
import {getManager} from "typeorm";

await getManager().transaction("SERIALIZABLE", transactionalEntityManager => {
    
});
```

TypeORM hỗ trợ việc implement `Isolation level` vào transaction của một số Database Driver phổ biến hiện nay, cụ thể:

- Các chuẩn `isolation levels`: `READ UNCOMMITTED`, `READ COMMITTED`, R`EPEATABLE READ`, `SERIALIZABLE` cho các Database Driver:
    + `MySQL`
    + `Postgres`
    + `SQL Server`

- `SQlite` mặc định là `SERIALIZABLE`, nhưng nếu `shared cache mode is enabled`, một transactions có thể hoạt động ở `READ UNCOMMITTED isolation level`.

- `Oracle` chỉ supports hai isolation levels là `READ COMMITTED` và `SERIALIZABLE`.

### Transaction decorators

Trong Typescript, `Decorator` có thể coi như một cú pháp khai báo đặc biệt, không bao giờ đứng độc lập mà luôn được gắn kèm với một khai báo `class`, `method`, `property` hoặc `accessor`, được viết dưới cú pháp dạng `@expression`, với expression trỏ tới một function sẽ được gọi tới ở runtime, có nhiệm vụ thay đổi hoặc bổ sung cho đối tượng được decorate.

TypeORM hỗ trợ các decorators dưới đây để tổ chức transactions
:
-  `@Transaction`: wraps tất các các execution vào một `single database transaction`,

- `@TransactionManager`: cung cấp một `entity manager` cho mỗi `execute queries` trong 1 transaction. Ví dụ

    ```typescript
    @Transaction({ isolation: "SERIALIZABLE" })
    save(@TransactionManager() manager: EntityManager, user: User) {
        return manager.save(user);
    }
    ```

- `@TransactionRepository`: Cung cấp một `entity repository`, đưa các transactions vào một Repository:

    ```typescript
    @Transaction()
    save(user: User, @TransactionRepository(User) userRepository: Repository<User>) {
        return userRepository.save(user);    
    }
    ``` 

### QueryRunner

Trong TypeORM, `QueryRunner` dùng để tạo và kiểm soát `state` của `single database connection`.
Một `single transaction` chỉ được thiết lập để chạy trên một `single query runner` duy nhất để có thể kiểm soát `state` của một transaction. DƯới đây là sample code:

```typescript
import {getConnection} from "typeorm";

// get a connection and create a new query runner
const connection = getConnection();
const queryRunner = connection.createQueryRunner();

// establish real database connection using our new query runner
await queryRunner.connect();

// now we can execute any queries on a query runner, for example:
await queryRunner.query("SELECT * FROM users");

// we can also access entity manager that works with connection created by a query runner:
const users = await queryRunner.manager.find(User);

// lets now open a new transaction:
await queryRunner.startTransaction();

try {
    
    // execute some operations on this transaction:
    await queryRunner.manager.save(user1);
    await queryRunner.manager.save(user2);
    await queryRunner.manager.save(photos);
    
    // commit transaction now:
    await queryRunner.commitTransaction();
    
} catch (err) {
    
    // since we have errors let's rollback changes we made
    await queryRunner.rollbackTransaction();
    
} finally {
    
    // you need to release query runner which is manually created:
    await queryRunner.release();
}
```

Có tất cả 3 methods để `control transactions` trong `QueryRunner`:


* `startTransaction` - `starts` một transaction mới 
* `commitTransaction` - `commits` tất cả thay đổi trong transaction
* `rollbackTransaction` - `rollback` transaction

## Transactions in Doctrine ORM

`Doctrine` là một ORM, triển khai dựa trên `Data Mapper pattern`, hỗ trợ mạnh mẽ trong việc tách riêng các `buѕineѕѕ ruleѕ` của ứng dụng khỏi `perѕiѕtence laуer` của databaѕe.

Tương tự như TypeORM, Doctrine ORM cũng thể hiện transactions bằng một nhóm tuần tự các câu lệnh, truy vấn hoặc các actions và đều được thể hiện qua các module trong source code.

### Transaction Demarcation

`Transaction Demarcation` là việc phân ranh giới giữa các transaction trong `Doctrine ORM`. Việc phân định ranh giới cho các transaction rất quan trọng vì nếu không được thực hiện đúng cách, nó có thể ảnh hưởng tiêu cực đến hiệu suất của ứng dụng. 

Thông thường, theo mặc định các transaction trong Database sẽ hoạt động ở chế độ tự động commit, và trong Doctrine ORM, mọi câu lệnh SQL đơn được gói gọn trong một transaction nhỏ. Nếu không có bất kỳ ranh giới transaction rõ ràng ngay từ ban đầu sẽ dẫn đến hiệu suất kém vì `Nesting transaction` - các transaction lồng nhay sẽ tốn performance. Dưới đây là sample code cho transaction trong Doctrine ORM: 
``` php

<?php
// $em instanceof EntityManager
$em->getConnection()->beginTransaction(); // suspend auto-commit
try {
    // ... do some work
    $user = new User;
    $user->setName('George');
    $em->persist($user);
    $em->flush();
    $em->getConnection()->commit();
} catch (Exception $e) {
    $em->getConnection()->rollBack();
    throw $e;
}

```

Trong đó, `$em` là một instance của `EntityManager` - entity quản lý các transactions trong Doctrine ORM. Một transaction sẽ đi từ `beginTransaction()` &rarr; execute các operations trong transaction &rarr; `commit()` nếu transaction thành công, ngược lại thì `rollBack()`

### Locking Levels
`Doctrine ORM` hỗ trợ 2 loại lock là `Optimistic Locking` và `Pessimistic Locking`

Dưới đây là ví dụ cho việc sử dụng `Optimistic Locking`

``` php
<?php
use Doctrine\DBAL\LockMode;
use Doctrine\ORM\OptimisticLockException;

$theEntityId = 1;
$expectedVersion = 184;

$entity = $em->find('User', $theEntityId);

try {
    // assert version
    $em->lock($entity, LockMode::OPTIMISTIC, $expectedVersion);

} catch(OptimisticLockException $e) {
    echo "Sorry, but someone else has already changed this entity. Please apply the changes again!";
}
```

Còn về `Pessimistic Locking` thì Doctrine ORM hiện hỗ trợ hai mode:

- `Pessimistic Write` (Doctrine\DBAL\LockMode::PESSIMISTIC_WRITE): khóa các row trong cơ sở dữ liệu cho các Operations READ và WRITE. 

- `Pessimistic Read` (Doctrine\DBAL\LockMode::PESSIMISTIC_READ): khóa các concurrent requests đang UPDATE hoặc khóa các row ở write mode.


### Isolation Levels

`Doctrine ORM` cũng hỗ trợ 4 Isolation Levels là `READ UNCOMMITTED`, `READ COMMITTED`, `REPEATABLE READ` và `SERIALIZABLE`, đều dùng làm `parameter` cho hàm `setIsolation()`. Ví dụ:

``` php
<?php
    tx = $conn->transaction;
    tx->setIsolation('SERIALIZABLE');
    level = $tx->getIsolation();
```

## Reference

1. [Transactions - typeorm](https://orkhan.gitbook.io/typeorm/docs/transactions)

2. [Transactions and Concurrency - doctrine 2](https://www.doctrine-project.org/projects/doctrine-orm/en/2.10/reference/transactions-and-concurrency.html)

3. [Transactions - sequelize](https://sequelize.org/v3/docs/transactions/)

4. [Typeorm transactions - tutorialspoint](https://www.tutorialspoint.com/typeorm/typeorm_transactions.htm)

5. [Transactions - doctrine 1](https://www.doctrine-project.org/projects/doctrine1/en/latest/manual/transactions.html)