---
author: Harry Hoang
date: 2022-01-27
---

# Migrations/Seeder

## Concepts

`Migrations` - database version control: là cách thức quản lý các phiên bản của CSDL, thuận tiện cho việc chia sẻ và thay đổi các kiến trúc CSDL (database schema). Migration có các tính năng như định nghĩa các bảng trong CSDL, định nghĩa nội dung các bảng cũng như cập nhật thay đổi các bảng đó. Đồng thời các thao tác với CSDL này còn có thể sử dụng trên các loại CSDL khác nhau như MySQL, SQL Server, Postgres, ... mà không cần phải chỉnh sửa lại code theo từng CSDL.

Sau khi đã đã có CSDL, việc cần làm tiếp theo là thêm một số `sample data` trước khi bắt đầu thực hiện việc code các tính năng. Việc thêm dữ liệu mẫu thủ công sẽ tốn nhiều thời gian, công sức. Để giải quyết vấn đề này, `Seeder` cung cấp các phương thức đơn giản để tạo ra dữ liệu mẫu cần thiết cho việc phát triển các tính năng.

## Migrations in ORM - TypeORM

Sau khi ứng dụng được đưa lên production, sẽ cần phải dùng `Migrations` để đồng bộ hóa các thay đổi vào cơ sở dữ liệu. Quá trình Migrations của TypeORM dựa trên một tệp duy nhất với các sql query để cập nhật database schema và áp dụng các thay đổi mới cho database hiện có.

Giả sử có một database và một post entity:

``` typescript
import { Entity, Column, PrimaryGeneratedColumn } from 'typeorm';

@Entity()
export class Post {

    @PrimaryGeneratedColumn()
    id: number;

    @Column()
    title: string;

    @Column()
    text: string;

}
```

Cái Post Entity này đã hoạt động trên production từ rất lâu rồi mà không có bất kỳ thay đổi nào. Đến khi ta cần tạo một bản release và phải rename cái thằng `@Column() title: string;` lại thành `name`. Khi này `Post` đang có hàng nghìn data chứa các bài đăng trong database. Lúc này sẽ cần dùng tới `Migrations`.TypeORM có thể tự động tạo các tệp Migrations với các thay đổi của database schema, với trường hợp trong ví dụ này:

``` typescript
import {MigrationInterface, QueryRunner} from "typeorm";

export class PostRefactoringTIMESTAMP implements MigrationInterface {

    async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "post" RENAME COLUMN "title" TO "name"`);
    }

    async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "post" RENAME COLUMN "name" TO "title"`); // reverts things made in "up" method
    }
}
```

Một `MigrationInterface` chứa 2 hàm `up()` và `down()`. Hàm `up()` được sử dụng để tạo 1 bảng, cột, hay index, trong trường hợp này là rename cột cho database. Hàm `down()` sẽ làm ngược lại những action của hàm up.

Để tạo migrations, ta dùng command `typeorm migration:create` và `typeorm migration:generate`, nó sẽ sinh ra một `.ts` file. Sau khi có migrations, ta có thể `Running` và `reverting` migrations này bằng các command trên CLI `typeorm migration:run` và `typeorm migration:revert`, hai lệnh này sẽ làm việc dựa trên file `.ts` kể trên. 

## Seeder in ORM - TypeORM

Lấy ví dụ sử dụng `TypeORM Seeding` để tạo một Seeder trong TypeORM. Ta có 2 TypeORM entites là User và Pet

``` typescript title="user.enity.ts"
// user.enity.ts
@Entity()
export class User {
  @PrimaryGeneratedColumn('uuid') id: string
  @Column({ nullable: true }) name: string
  @Column({ type: 'varchar', length: 100, nullable: false }) password: string
  @OneToMany((type) => Pet, (pet) => pet.user) pets: Pet[]
 
  @BeforeInsert()
  async setPassword(password: string) {
    const salt = await bcrypt.genSalt()
    this.password = await bcrypt.hash(password || this.password, salt)
  }
}
```

``` typescript title="pet.enity.ts"
@Entity()
export class Pet {
  @PrimaryGeneratedColumn('uuid') id: string
  @Column() name: string
  @Column() age: number
  @ManyToOne((type) => User, (user) => user.pets)
  @JoinColumn({ name: 'user_id' })
  user: User
}
```

Sau đó, đối với mỗi entity User và Pet sẽ có một `factory`. Mục đích của một `factory` giống như trong Factory Pattern, là tạo ra các đối tượng mới kèm theo dữ liệu mẫu.

``` typescript title="user.factory.ts"

define(User, (faker: typeof Faker) => {
  const gender = faker.random.number(1)
  const firstName = faker.name.firstName(gender)
  const lastName = faker.name.lastName(gender)
 
  const user = new User()
  user.name = `${firstName} ${lastName}`
  user.password = faker.random.word()
  return user
})

```

``` typescript title="pet.factory.ts"

define(Pet, (faker: typeof Faker) => {
  const gender = faker.random.number(1)
  const name = faker.name.firstName(gender)
 
  const pet = new Pet()
  pet.name = name
  pet.age = faker.random.number()
  pet.user = factory(User)() as any
  return pet
})

```

Sau khi đã có các entites và seeders tương ứng, ta tiến hàng tạo ra dữ liệu mẫu với 10 Pets thuộc một User.

``` typescript title="create-pets.seed.ts"

export default class CreatePets implements Seeder {
  public async run(factory: Factory, connection: Connection): Promise<any> {
    await factory(Pet)().createMany(10)
  }
}
```

Lấy ví dụ này để thấy được quá trình Seeder đơn giản nhất diễn ra như thế nào. Mỗi Seeder sẽ tương ứng với một Entity trong database, sau khi có các Seeder này, ta có thể tha hồ dùng để dev, test các tính năng mà không lo ảnh hưởng tới dữ liệu trong database và càng không phải tốn nhiều thời gian để create từng seeder theo cách thủ công, ORM hỗ trợ cho mình hết, mình chỉ cần tập trung dev, test các tính năng thôi.

## Reference

1. [Migrations - typeorm](https://orkhan.gitbook.io/typeorm/docs/migrations)

2. [typeorm-seeding - npmjs.com](https://www.npmjs.com/package/typeorm-seeding)

3. [How to Seed Database using TypeORM Seeding - dev.to](https://dev.to/franciscomendes10866/how-to-seed-database-using-typeorm-seeding-4kd5)