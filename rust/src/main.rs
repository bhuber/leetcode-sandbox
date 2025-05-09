use ferris_says::say;
use std::io::{stdout, BufWriter};

fn hello() -> i32 {
    println!("Hello, world!");
    3
}

fn main() {
    let _ =  hello();
    
    let stdout = stdout();
    let message = String::from("Hello fellow rustaceans");
    let width = message.chars().count();
    
    let mut writer = BufWriter::new(stdout.lock());
    say(&message, width, &mut writer).unwrap();
}
