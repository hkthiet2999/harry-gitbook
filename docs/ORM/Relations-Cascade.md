---
author: Harry Hoang
date: 2022-01-28
---

# Relations and Cascade


## Relations
`Relations` trong ORM đóng vai trò hỗ trợ  việc tương tác với `related entities` . Có các loại relations sau:

- one-to-one
- many-to-one 
- one-to-many 
- many-to-many 

Dưới đây mình sẽ lấy ví dụ về việc sử dụng TypeORM để thấy được cách một ORM framework implement các Relations trong database.

### One-to-One

One-to-One trong Relational ORM là trường hợp `instance` của một `table field` chứa instance của `table field` khác và ngược lại. Ví dụ với TypeORM, có một Details table trong database được thể hiện qua ORM như sau:

```typescript title="Details.ts"

import {Entity, PrimaryGeneratedColumn, Column} from "typeorm";

@Entity() 
export class Details {
   @PrimaryGeneratedColumn() 
   id: number; 
   
   @Column() 
   gender: string; 
   
   @Column() 
   country: string; 
}
```

và một Customer table:

``` typescript title="Customer.ts"
import {Entity, PrimaryGeneratedColumn, Column, OneToOne, JoinColumn} from "typeorm"; 

import {Details} from "./Details"; 

@Entity() 
export class Customer { 

   @PrimaryGeneratedColumn() 
   id: number; 
   
   @Column() 
   name: string; 
   
   @OneToOne(type => Details) @JoinColumn() 
   details: Details;
}
```
Để thể hiện Relations `OneToOne` bằng TypeORM, ta thêm ánh xạ OneToOne vào `Details table` bằng `@JoinColumn()` chứa cái `relation id` và  `foreign key` tới Customer table. 

``` typescript title="OneToOne.ts"

const details = new Details(); 
details.gender = "female"; 
details.country = "india" await connection.manager.save(details);

const customer = new Customer(); 
customer.name = 'customer1'; 
customer.details = Details; await connection.manager.save(Customer);
```
### One-to-Many and Many-to-One

Một Entity A có liên kết với nhiều Entity B1, B2, B3, B.... Nhưng ngược lại một Entity B1, B2 B chấm chấm đó lại có liên kết duy nhất với Entity A thì gọi là `One to many relationship`. Còn nhiều Entity A1, A2, A3, A... có cùng mối quan hệ với duy nhất một Entity B.

Với ví dụ bên dưới, một Entity được thể hiện bằng một class `Student`. Một Student sẽ có nhiều `Projects` khác nhau:

``` typescript title="Student.ts"
import {Entity, PrimaryGeneratedColumn, Column, OneToMany} from "typeorm"; import {Project} from "./Project"; 

@Entity() 
export class Student {  
   
   @PrimaryGeneratedColumn() 
   id: number; 
   
   @Column() 
   name: string; 
   
   @OneToMany(type => Project, project => project.student) projects: Project[];  
}
```

``` typescript title="Project.ts"
import {Entity, PrimaryGeneratedColumn, Column, ManyToOne} from "typeorm"; import {Student} from "./Student"; 
@Entity() 
export class Project {  

   @PrimaryGeneratedColumn() 
   id: number; 
   
   @Column() 
   projects: string; 
   
   @ManyToOne(type => Student, student => student.projects) student: Student; 
}
```

Bây giờ, `@OneToMany property` của `Student` sẽ tham chiếu tới Project. Và `@ManyToOne property` của Project sẽ tham chiếu tới Student thông qua `relation id` và foreign key:

``` typescript title="Project.ts"
const proj1 = new Project(); 
proj1.projects = "database management"; 
await connection.manager.save(proj1); 

const proj2 = new Project(); 
proj2.projects = "web application"; 
await connection.manager.save(proj2); 

const stud = new Student(); 
stud.name = "Student1"; 
stud.projects = [proj1, proj2]; 
await connection.manager.save(stud);

```

### Many-to-Many

Trường hợp này là một Entity A có liên kết với nhiều Entity B và ngược lại. Lấy ví dụ, một `Student` có thể đăng ký nhiều `Classes` trong một học kỳ và một `Classes` có thể có nhiều `Student`. Tóm lại, một học sinh có nhiều lớp, và một lớp có nhiều học sinh. Ta implement `Many-to-Many relationship` trong ORM như sau:

``` typescript title="Student.ts"
import {Entity, PrimaryGeneratedColumn, Column, ManyToMany, JoinTable} from "typeorm"; 
import {Classes} from "./Classes";

@Entity() 
export class Student { 

   @PrimaryGeneratedColumn() 
   id: number; 
   
   @Column() 
   name: string;

   @Column() 
   subjects: string; 
   
   @ManyToMany(type => Classes) @JoinTable() 
   classes: Classes[];
}
```

``` typescript title="Classes.ts"
import {Entity, PrimaryGeneratedColumn, Column} from "typeorm"; 

@Entity() 
export class Classes { 

   @PrimaryGeneratedColumn() 
   id: number; 
   
   @Column() 
   name: string; 
}
```

## Cascade

Một trong những Relation optional là Cascade. Options này sẽ thiết lập các Primary/Foreign keys giữa các table với nhau, khi ta tiến hành UPDATE hay DELETE trong 1 table thì các dữ liệu được table khác tham chiếu tới cũng sẽ UPDATE hay DELETE theo.

### Cascade in ORM

Dưới đây là một `Cascades example` trong TypeORM để hình dung được cách mà ORM thể hiện Cascade trong Database:

``` typescript title="Category.ts"
import {Entity, PrimaryGeneratedColumn, Column, ManyToMany} from "typeorm";
import {Question} from "./Question";

@Entity()
export class Category {

    @PrimaryGeneratedColumn()
    id: number;

    @Column()
    name: string;

    @ManyToMany(type => Question, question => question.categories)
    questions: Question[];

}
```

``` typescript title="Question.ts"
import {Entity, PrimaryGeneratedColumn, Column, ManyToMany, JoinTable} from "typeorm";
import {Category} from "./Category";

@Entity()
export class Question {

    @PrimaryGeneratedColumn()
    id: number;

    @Column()
    title: string;

    @Column()
    text: string;

    @ManyToMany(type => Category, category => category.questions, {
        cascade: true
    })
    @JoinTable()
    categories: Category[];

}
```

``` typescript title="Cascade.ts"
const category1 = new Category();
category1.name = "ORMs";

const category2 = new Category();
category2.name = "Programming";

const question = new Question();
question.title = "How to ask questions?";
question.text = "Where can I ask TypeORM-related questions?";
question.categories = [category1, category2];
await connection.manager.save(question);
```

Như trong `Cascade.ts`, ta không gọi method `save()` cho `category1` và `category2`. Chúng sẽ được tự động `insert` vào entity tương ứng luôn. 

Cascades có vẻ như là một cách tốt và dễ dàng để làm việc với `Relations`, nhưng chúng cũng có thể mang lại lỗi và các vấn đề bảo mật khi một số Objects không mong muốn được lưu vào database. 

### Cascade Options

Trong SQL, có 5 optional cho việc sử dụng  `ON DELETE`, `ON UPDATE` trong Cascade, được gọi là `referential actions`. Còn trong ORM, tùy từng ORM framework sẽ có cách implement khác nhau. Ví dụ trong TypeORM cung cấp các actions: `("insert" | "update" | "remove" | "soft-remove" | "recover")`. Còn trong Sequelize sẽ truyền options theo kiểu: `options.onDelete(SET NULL if foreignKey allows nulls, CASCADE if otherwise)`. Prisma hỗ trợ các referential actions sau: `Cascade`, `Restrict`, `NoAction`, `SetNull`, `SetDefault`. Còn trong Doctrine ORM thì hỗ trợ `persist, remove, merge, detach, refresh, all` để thể hiện associated entities.

Tùy từng trường hợp và từng ORM framework sẽ có cách sử dụng khác nhau, tuy nhiên nhìn chung thì đều sẽ implement Cascade trong database thông qua một build-in functions, method hay module nào đó được cung cấp sẵn, mình chỉ việc dùng đúng lúc đúng chỗ đúng logic là ok.

## Reference

1. [typeorm Relations - tutorialspoint](https://www.tutorialspoint.com/typeorm/typeorm_relations.htm)
2. [Referential Actions - Prisma](https://www.prisma.io/docs/concepts/components/prisma-schema/relations/referential-actions)
3. [Model - sequelize](https://sequelize.org/v5/class/lib/model.js~Model.html)
4. [Relations - TypeORM](https://orkhan.gitbook.io/typeorm/docs/relations)