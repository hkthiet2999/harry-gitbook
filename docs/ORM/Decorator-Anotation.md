---
author: Harry Hoang
date: 2022-01-28
---

# Decorator and Annotation

## Concepts

`Annotation` trong Java có 3 loại: `- `@Deprecated`, `- `@Override`, `- `@SuppressWarnings`

Còn trong Typescript, có 5 loại `Decorator`: `class decorator`, `method decorator`, `property decorator`, `accessor decorator` và `parameter decorator`. Ví dụ về `class decorator` dùng để log ra mỗi khi có 1 instance mới của class được khởi tạo.

```typescript title="class-decorator.ts"
- `@logCreate
class Animal {
  constructor(footCount) {}
}

const dog = new Animal(4);
// => Object created with args: 4

```

Còn trong Angular, dùng cả hai khái niệm `Decorator` và `Annotation`. Nhìn chung thì `Decorator` và `Annotation` có thể coi như một cú pháp khai báo đặc biệt, không bao giờ đứng độc lập mà luôn được gắn kèm với một khai báo `class`, `method`, `property` hoặc `accessor`. Chúng được viết dưới cú pháp dạng `- `@expression`, với expression trỏ tới một function sẽ được gọi tới ở runtime, có nhiệm vụ thay đổi hoặc bổ sung cho đối tượng được decorate hay announce.

## Annotations Reference - Doctrine ORM

Trong Doctrine ORM, một Annotations gọi là `Docblock annotations`, là một công cụ để nhúng metadata vào bên trong document và xử lý chúng. `Doctrine 2` khái quát hơn về khái niệm của docblock annotations để chúng có thể được sử dụng cho bất kỳ loại metadata nào và dễ dàng xác định các docblock annotations mới, cho phép nhiều giá trị annotations liên quan hơn và giảm nguy cơ xung đột giữa các docblock annotations với nhau, cú pháp được lấy cảm hứng từ cú pháp Annotations trong Java 5 mình ví dụ ở trên.

Dưới đây là một vài Doctrine 2 Annotation:

- `@Column`
- `@Cache`
- `@Entity`
- `@HasLifecycleCallbacks`
- `@Index`
- `@Id`
- `@JoinColumn`
- `@JoinTable`
- `@ManyToOne`
- `@OneToMany`
- `@OrderBy`
- `@PreRemove`
- `@PreUpdate`
- `@Table`
- `@UniqueConstraint`
- `@Version`

xem full tại [Doctrine 2 - Annotations Reference](https://www.doctrine-project.org/projects/doctrine-orm/en/2.7/reference/annotations-reference.html)

### Entity Annotations

Lấy ví dụ với Annotation `@Entity`. Đây là Annotation bắt buộc dùng để đánh dấu một class là một Entity. Doctrine sẽ dựa vào đó để quản lý sự tồn tại của tất cả các class được đánh dấu là Entity.

```php title="@Entity"
<?php
/**
 * @Entity(repositoryClass="MyProject\UserRepository")
 */
class User
{
    //...
}
```

### Column Annotations

`@Column` là Annotation dùng để đánh dấu một `instance variable` là một Column trong Entity. Nó phải nằm bên trong các `DocBlock comment`, bất kỳ giá trị nào bên trong variable này sẽ được `lưu` và `tải` từ Database như một phần của entity-class. Ví dụ:

```php title="@Column"
<?php
/**
 * @Column(type="string", length=32, unique=true, nullable=false)
 */
protected $username;

/**
 * @Column(type="string", columnDefinition="CHAR(2) NOT NULL")
 */
protected $country;

/**
 * @Column(type="decimal", precision=2, scale=1)
 */
protected $height;

/**
 * @Column(type="string", length=2, options={"fixed":true, "comment":"Initial letters of first and last name"})
 */
protected $initials;

/**
 * @Column(type="integer", name="login_count", nullable=false, options={"unsigned":true, "default":0})
 */
protected $loginCount;
```


### Primary key Annotations

`@Id` sẽ được đánh dấu một `instance variable` ( tức Column trong Database) là định danh của một entity, tức là `primary key` trong cơ sở dữ liệu. Annotation này chỉ đánh dấu và không có thuộc tính bắt buộc. Dưới đây là ví dụ:

```php title="@Id"
<?php
/**
 * @Id
 * @Column(type="integer")
 */
protected $id = null;
```

### Relationships Annotations
Doctrine 2 có 4 Annotation Relationships tương ứng với 4 relationships trong Relational Database như sau: `@OneToOne`, `@OneToMany`, `@ManyToOne`, `@ManyToMany`. Tùy từng relationships mà mình sẽ dùng Annotation tương ứng. Lấy ví dụ với OneToMany relationships, trong Doctrine 2 dùng `@OneToMany`:

```php title="@OneToMany"
<?php
/**
 * @OneToMany(targetEntity="Phonenumber", mappedBy="user", cascade={"persist", "remove", "merge"}, orphanRemoval=true)
 */
public $phonenumbers;
```

Ngoài ra còn rất nhiều Annotations Reference trong Doctrine ORM, xem đầy đủ và bao gồm Descriptions, các Optional, Required attributes của từng Annotations trong Doctrine ORM tại [Annotations Reference](https://www.doctrine-project.org/projects/doctrine-orm/en/2.7/reference/annotations-reference.html)

## Decorators Reference - TypeORM
TypeORM chia các Decorators thành các nhóm sau:

- `Entity decorators`: Dùng để decorate cho các Entity

- `Column decorators`:  Dùng để decorate cho các Column và các Operations liên quan đến Column đó luôn

- `Relation decorators`:  Dùng để decorate cho các Relationshipts trong Database

- `Subscriber and listener decorators`: các Actions như `@AfterLoad`, `@BeforeInsert`, `@AfterUpdate`, `@BeforeRemove` v.vv và `@EventSubscriber`

- `Other decorators`: Decorate cho các contraints trong Database như `@Index`, `@Unique`, `@Check` và cả transactions trong database như `@Transaction`, `@TransactionManager` và `@TransactionRepository`.

### Entity decorators
Nhóm `Entity decorators` dùng để decorate cho các Entity, gồm có 2 loại là `@Entity` và `@ViewEntity`. Lấy ví dụ với `@Entity`, nó dùng để đánh dấu một MModel ( Model trong MVC) là một Entity. Entity khi này là một class được `transformed ` thành một Table trong Database:

```typescript title="@Entity"
@Entity({
    name: "users",
    engine: "MyISAM",
    database: 'example_dev',
    schema: 'schema_with_best_tables',
    synchronize: false,
    orderBy: {
        name: "ASC",
        id: "DESC"
    }
})
export class User {
```

### Column decorators and Primary key

`@Column` dùng để đánh dấu một property trong entity là một column trong table của Database. Ví dụ:

``` typescript title="@Column"
@Entity("users")
export class User {

    @Column({ primary: true })
    id: number;

    @Column({ type: "varchar", length: 200, unique: true })
    firstName: string;

    @Column({ nullable: true })
    lastName: string;

    @Column({ default: false })
    isActive: boolean;
}
```

Column decorators có rất nhiều optional dùng để chỉ định `type: ColumnType`, `name: string`, `length: string|number`, `onUpdate: string`, `nullable: boolean` v.vv đủ dùng cho việc `transformed` một property trong entity thành một Column trong Table Database. Ngoài ra còn có options `primary: boolean` để marks column này là Primary key. Ngoài cách này ra còn có thể dùng `@PrimaryColumn` như sau:

``` typescript title="@PrimaryColumn" 
@Entity()
export class User {

    @PrimaryColumn()
    id: number;
}
```

### Subscriber and listener decorators

`Subscriber and listener decorators` dùng để xác định một method bên trong Entity để thực hiện các actions `before/after load/insert/update/remove` bằng `QueryBuilder` hoặc listen các event bằng `@EventSubscriber`

Lấy ví dụ với `@AfterLoad`:

```typescript title="@Entity"
@Entity()
export class Post {

    @AfterLoad()
    updateCounters() {
        if (this.likesCount === undefined)
            this.likesCount = 0;
    }
}
```
`@AfterLoad` này dùng để xác định một method tên là `updateCounters` bên trong `Post` Entity và TypeORM sẽ gọi nó mỗi khi Post được load bằng `QueryBuilder` hoặc `repository/manager find methods`.

### Other decorators

Dùng để Decorate cho các contraints trong Database như `@Index`, `@Unique`, `@Check` và cả Transactions trong database như `@Transaction`, `@TransactionManager` và `@TransactionRepository`.

Ví dụ về Transactions trong database sử dụng `@Transaction`. Nó được sử dụng trên một method và gói tất cả việc thực thi của nó vào một Transactions duy nhất. Tất cả các database queries phải được thực hiện bằng provided manager tương ứng với `@TransactionManager` hoặc với các `transaction repositories` tương ứng với `@TransactionRepository` trong TypeORM. Ví dụ:

```typescript

@Transaction()
save(@TransactionManager() manager: EntityManager, user: User) {
    return manager.save(user);
}
```

```typescript
@Transaction()
save(user: User, @TransactionRepository(User) userRepository: Repository<User>) {
    return userRepository.save(user);
}
```

```typescript
@Transaction()
save(@QueryParam("name") name: string, @TransactionRepository() userRepository: UserRepository) {
    return userRepository.findByName(name);
}
```

Lấy một ví dụ khác về các ràng buộc trong Database, cụ thể là `unique contraint` tương ứng với `@Unique` decorator:

``` typescript
@Entity()
@Unique(["firstName"])
@Unique(["lastName", "middleName"])
@Unique("UQ_NAMES", ["firstName", "lastName", "middleName"])
export class User {

    @Column({ name: 'first_name' })
    firstName: string;

    @Column({ name: 'last_name' })
    lastName: string;

    @Column({ name: 'middle_name' })
    middleName: string;
}
```

`@Unique` này cho phép ta tạo ràng buộc trong cơ sở dữ liệu là `unique` cho một nhiều Column cụ thể. Decorator này chỉ có thể được áp dụng cho một Entity duy nhất. Ta phải chỉ định tên field của Entity (không phải tên cột cơ sở dữ liệu) làm đối số cho nó.

## Reference

1. [Differences between an Annotation and a Decorator in Angular? - geeksforgeeks](https://www.geeksforgeeks.org/what-are-the-differences-between-an-annotation-and-a-decorator-in-angular)

2. [Annotations Reference - Doctrine ORM](https://www.doctrine-project.org/projects/doctrine-orm/en/2.7/reference/annotations-reference.html)

3. [Decorator Reference - TypeORM](https://orkhan.gitbook.io/typeorm/docs/decorator-reference)