# What makes rust super star

Rust is a system programming language that runs **blazingly fast**, prevent segfaults, and guarantees **thread safety**.

Low-level system programming, such as C, C++, Assembly, had developed for nearly 50 years. But, there are two thorny problems that have not completely solved.

1. It's hard to write memory safety code
2. It's hard to write thread safety code

How about break down these traditional programming language barriers and design an absolutely new modern language?

*Why not?*

That's what rust does. Rust empowers you to build more reliable and efficient software.

## How rust achieve

Rust design principles:

- Memory Security
- Zero Cost Abstraction
- Thread Safety

### Memory Security

Different programming languages deal with memory issues in different ways. Some use GC mechanism and others like C/C++ completely
hand over this complex task to the developers. How rust achieve memory safety guarantees without a garbage collector?

Rust memory management tools:

1. Ownership.
2. References and lifetime.

Let's take about ownership firstly.

Ownership rules:

- Each value in Rust has a variable that’s called its owner
- There can only be one owner at a time
- When the owner goes out of scope, the value will be dropped

---

*Demo1* - Normal Reference

```rs
{
    let s = String::from("hello"); // s is valid from this point forward

    // do stuff with s
}   // this scope is now over, and s is no
    // longer valid
```

When `s` goes out of scrope, rust call a special function named `drop`, put the code to return the memory.

*Demo2* - Invalid Reference

```rs
    let s1 = String::from("hello");  // Actually, s1 is a reference

    let s2 = s1;    // assign s1 to s2
    println!("{}, world!", s1);
```

```rs
error[E0382]: borrow of moved value: `s1`
 --> src/main.rs:5:28
  |
2 |     let s1 = String::from("hello");
  |         -- move occurs because `s1` has type `std::string::String`, which does not implement the `Copy` trait
3 |
4 |     let s2 = s1;
  |              -- value moved here
5 |     println!("{}, world!", s1);
  |                            ^^ value borrowed here after move

error: aborting due to previous error

For more information about this error, try `rustc --explain E0382`.
```

The compiler says you can not use `s1` anymore since you have moved ownership of data under `s1` to `s2`.

You know `String` type is made up of three parts(a pointer to the memory that hold the content of the string, a length and a capacity).
When assigning `s1` to `s2`, it only copy the pointer and do not copy the data under the pointer.
Compiler helps you found this potential memory security tricky issue at compile time.

*Demo3* - Dangling Reference

```rs
fn main() {
    let reference_to_nothing = dangle();
}

fn dangle() -> &String {            // Return a reference
    let s = String::from("hello");

    &s      // Return a reference which point to s
} // Here, s goes out of scope and dropped. So where does s point now?
```

Unexpectedly, compiler says no.

```rs
Compiling playground v0.0.1 (/playground)
error[E0106]: missing lifetime specifier
 --> src/main.rs:5:16
  |
5 | fn dangle() -> &String {
  |                ^ help: consider giving it a 'static lifetime: `&'static`
  |
  = help: this function's return type contains a borrowed value, but there is no value for it to be borrowed from

error: aborting due to previous error

For more information about this error, try `rustc --explain E0106`.
error: Could not compile `playground`.
```

Diving into the error message, it's clearly:

```rs
this function's return type contains a borrowed value, but there is no value for it to be borrowed from
```

### Zero Cost Abstraction

The core concept of the rust zero cost abstraction is `Trait System`. In rust, trait is the abstraction of type
behavior. Similar to interface in other languages, but more abstracted and powerful.

*Demo1* - Trait Simplest Usage

I. Define a Trait

```rs
pub trait Summary {     // Defining a Trait `Summary`
    fn summarize(&self) -> String;  // define a behavior named summarize
}
```

II. Implementing a Trait on a type

```rs
pub struct NewsArticle {        // Define a struct `NewsArticle`
    pub headline: String,
    pub location: String,
    pub author: String,
    pub content: String,
}

impl Summary for NewsArticle {      // Implement `Summary` for `NewsArticle`
    fn summarize(&self) -> String {
        format!("{}, by {} ({})", self.headline, self.author, self.location)
    }
}

pub struct Tweet {      // Another struct `Tweet`
    pub username: String,
    pub content: String,
    pub reply: bool,
    pub retweet: bool,
}

impl Summary for Tweet {    // Implement `Summary` for `Tweet`
    fn summarize(&self) -> String {
        format!("{}: {}", self.username, self.content)
    }
}
```

III. Trait as Parameters

```rs
pub fn notify(item: impl Summary) {     // This parameter accepts any type that implements trait `Summary`
    println!("Breaking news! {}", item.summarize());
}
```

IV. Multiple trait bounds

```rs
pub fn notify<T: Summary + Display>(item: T) {  // item must implement both Display and Summary
                                                // Display is another trait, like Summary.
    println!("Breaking news! {}", item.summarize());
}
```

In addtion, rust provides several builtin traits:

* Sized trait: The trait indicates the type size is known at compile time
* Copy trait: The trait indicates the type can be copied in bits
* Send trait: The trait indicates the ownership of the type can be transferred between threads
* Sync trait: The trait indicates it is safey for the type can be referenced from multiple threads

### Thread Safety

Because of the uncontrolled system level threads, the code we write not works as we expected in multiple threads.

To achieve thread safety, rust provides two killer traits named `Send` and `Sync`:

* Send trait: Allowing transference of ownership between threads
* Sync trait: Allowing access from multiple threads

*Demo1* - Sharing Immutable Variable Between Threads

```rs
use std::thread;

fn main() {
    let x = vec![1, 2, 3, 4];
    thread::spawn(|| x);
}
```

That's ok.

*Demo2* - Sharing Mutable Variable Between Threads

```rs
use std::thread;

fn main() {
    let mut x = vec![1, 2, 3, 4];   // New a mutable vector
    thread::spawn(||{   // Try to modify value of vector in child
        x.push(1);
    });
    x.push(2);   // Modify value of vector in main to simulate data race
}
```

Compiler says no.

```rs
Compiling playground v0.0.1 (/playground)
error[E0373]: closure may outlive the current function, but it borrows `x`, which is owned by the current function
 --> src/main.rs:5:19
  |
5 |     thread::spawn(||{
  |                   ^^ may outlive borrowed value `x`
6 |         x.push(1);
  |         - `x` is borrowed here
  |
```

The `x` in closure is a reference to `x` in main thread. The rust compiler can not determine which `x` lives longer.
If `x` in the main thread dropped, then the closure `x` becomes a dangerous dangling reference.
Next, you can use `move` keyword to transfer ownership of `x` from main to child as following:

```rs
use std::thread;

fn main() {
    let mut x = vec![1, 2, 3, 4];      // New a mutable vector
    thread::spawn(move ||{                    // Use move to transfer x's ownership from main thread to child thread.
                                // Thus, x can be accessed in child thread
        x.push(1);
    });
    // x.push(2);  // The main thread can not modify x, because x's ownership had transferred to child thread.
}
```

**Note**: A variable can use `move` to transfer ownership only when the type has implemented `Send` and `Sync` traits.
By default, almost all primitive types are `Send`, any type composed entirely of `Send` types is automatically marked as `Send` as well.

*Demo3* - Transfer Ownership Between Threads

```rs
use std::thread;
use std::rc::Rc;

fn main() {
    let mut x = Rc::new(vec![1, 2, 3, 4]);       // New a mutable vector and wrap it with Rc container.
    thread::spawn(move ||{                      // Try to move ownership of Rc container to child thread.
        x.push(1);
    });
}
```

`Rc<T>` is a smart pointer provided by rust used to enable multiple owners to a value. `Rc<T>` is not a `Send` and `Sync` type and not safe to share across threads. In other words, you can't use `move` to transfer ownership of Rc container. Compiler will say no!

```rs
Compiling playground v0.0.1 (/playground)
error[E0277]: `std::rc::Rc<std::vec::Vec<i32>>` cannot be sent between threads safely
 --> src/main.rs:6:5
  |
6 |     thread::spawn(move ||{
  |     ^^^^^^^^^^^^^ `std::rc::Rc<std::vec::Vec<i32>>` cannot be sent between threads safely
  |
  = help: within `[closure@src/main.rs:6:19: 8:6 x:std::rc::Rc<std::vec::Vec<i32>>]`, the trait `std::marker::Send` is not implemented for `std::rc::Rc<std::vec::Vec<i32>>`
  = note: required because it appears within the type `[closure@src/main.rs:6:19: 8:6 x:std::rc::Rc<std::vec::Vec<i32>>]`
  = note: required by `std::thread::spawn`

error: aborting due to previous error

For more information about this error, try `rustc --explain E0277`.
error: Could not compile `playground`.
```

In order to share variable across threads, rust provides another safecontainer named `Arc<T>`.
`Arc` is a smart pointer like `Rc`, but it implemented `Send` and `Sync`. It's movable.

*Demo4* - Sharing Immutable Variable Between Threads

```rs
use std::thread;
use std::sync::Arc;

fn main() {
    let x = Arc::new(vec![1, 2, 3, 4]);   // New a mutable vector and wrap it with Arc container.
    thread::spawn(move ||{   // Try to move ownership of Rc container to child thread.
    });
        println!("vector is {:?}", x);
}
```

Compiler says yes!

*Note*: We changed `x` in main thread as immutable. The data wraped in `Arc` is read-only.
If you want to modify data inside, `Mutex<T>` is needed.  

*Demo5* - Sharing Mutable Between Threads

```rs
use std::thread;
use std::sync::{Arc, Mutex};

fn main() {
    let x = Arc::new(Mutex::new(vec![1, 2, 3, 4]));  // New a mutable vector and wrap it with Arc<Mutex<>> container.
    let x_clone = x.clone();     // Clone means creating a reference to data inside container

    let child = thread::spawn(move ||{        // Try to modify vector in child thread
        let mut x1 = x_clone.lock().unwrap();
        x1.push(5);
    });

    let _ = child.join();  // call join, let main thread wait for child thread to finish

    let mut x2 = x.lock().unwrap();   // Modify vector in main thread
    x2.push(6);

    println!("vector is {:?}", x2);
}
```

`Mutex<T>` is a container for safety sharing mutable variable across threads. a mutex allows only one thread to access data at any time.
To access the data inside the mutex, we use the `lock` method to acquire the lock.

Output:

```rs
vector is [1, 2, 3, 4, 5, 6]
```

Demos above demonstrate how rust achieve thread safety.
