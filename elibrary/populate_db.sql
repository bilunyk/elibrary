-- create all tables
CREATE TABLE users (
    id INTEGER NOT NULL,
    name VARCHAR(40),
    password VARCHAR(40),
    email VARCHAR(40),
    PRIMARY KEY (id),
    UNIQUE (email)
);
CREATE TABLE books (
    id INTEGER NOT NULL,
    title VARCHAR(200),
    info VARCHAR(512),
    PRIMARY KEY (id),
    UNIQUE (title)
);
CREATE TABLE authors (
    id INTEGER NOT NULL,
    name VARCHAR(200),
    info VARCHAR(512),
    PRIMARY KEY (id),
    UNIQUE (name)
);
CREATE TABLE books_authors (
    book_id INTEGER,
    author_id INTEGER,
    FOREIGN KEY(book_id) REFERENCES books (id),
    FOREIGN KEY(author_id) REFERENCES authors (id)
);
-- add admin user
INSERT INTO users(name, password, email) VALUES ("admin", "sha1$B9DvLSq8$94794131dc6f04ef1e8284ad416fe06b71a3dbec", "admin@example.com");
-- add books and authors
INSERT INTO books(title, info) VALUES ("Dive Into Python 3", "Dive Into Python 3 is a hands-on guide to Python 3 and its differences from Python 2. As in the original book, Dive Into Python, each chapter starts with a real, complete code sample, proceeds to pick it apart and explain the pieces, and then puts it all back together in a summary at the end.");
INSERT INTO authors(name, info) VALUES ("Mark Pilgrim", "Developer advocate for open source and open standards. By night, he is a husband and father who lives in North Carolina with his wife, his two sons, and his big slobbery dog. He spends his copious free time sunbathing, skydiving, and making up autobiographical information.");
INSERT INTO books_authors(book_id, author_id) VALUES (1,1);
INSERT INTO books(title, info) VALUES ("Learning Python (4th edition)", "With this hands-on book, you can master the fundamentals of the core Python language quickly and efficiently, whether you're new to programming or just new to Python. Once you finish, you will know enough about the language to use it in any application domain you choose. Learning Python is based on material from author Mark Lutz's popular training courses, which he's taught over the past decade. Each chapter is a self-contained lesson that helps you thoroughly understand a key component of Python before you continue. Along with plenty of annotated examples, illustrations, and chapter summaries, every chapter also contains Brain Builder, a unique section with practical exercises and review quizzes that let you practice new skills and test your understanding as you go. This book covers: Types and Operations -- Python's major built-in object types in depth: numbers, lists, dictionaries, and more Statements and Syntax -- the code you type to create and process objects in Python, along with Python's general syntax model Functions");
INSERT INTO authors(name, info) VALUES ("Mark Lutz", "Mark Lutz is the world leader in Python training, the author of Python's earliest and best-selling texts, and a pioneering figure in the Python community since 1992. He is also the author of O'Reilly's Programming Python, 3rd Edition and Python Pocket Reference, 3rd Edition. Mark began teaching Python classes in 1997, and has instructed more than 200 Python training sessions as of 2007. Mark also has BS and MS degrees in Computer Science and 25 years of software development experience. Whenever Mark gets a break from spreading the Python word, he leads an ordinary, average life with his kids in Colorado");
INSERT INTO books_authors(book_id, author_id) VALUES (2,2);
INSERT INTO books(title, info) VALUES ("Python Pocket Reference", "This is the book to reach for when you're coding on the fly and need an answer now. It's an easy-to-use reference to the core language, with descriptions of commonly used modules and toolkits, and a guide to recent changes, new features, and upgraded built-ins -- all updated to cover Python 3.X as well as version 2.6. You'll also quickly find exactly what you need with the handy index.");
INSERT INTO books_authors(book_id, author_id) VALUES (3,2);
INSERT INTO books(title, info) VALUES ("The Definitive Guide to Django: Web Development Done Right", "The Definitive Guide to Django is broken into three parts, with the first introducing Django fundamentals such as installation and configuration, and creating the components that together power a Django–driven web site. The second part delves into the more sophisticated features of Django, including outputting non–HTML content such as RSS feeds and PDFs, caching, and user management. The appendixes serve as a detailed reference to Django’s many configuration options and commands.");
INSERT INTO authors(name, info) VALUES ("Adrian Holovaty", "Web developer and journalist, is one of the creators and core developers of Django. He works at WashingtonPost.com, where he builds database web applications and does journalism as computer programming. Previously, he was lead developer for World Online in Lawrence, Kansas, where Django was created. When not working on Django improvements, Adrian hacks on side projects for the public good, such as ChicagoCrime.org, which won the 2005 Batten Award for Innovations in Journalism.");
INSERT INTO authors(name, info) VALUES ("Jacob Kaplan-Moss", "One of the lead developers of Django. At his day job, he's the lead developer for the Lawrence Journal-World, a locally owned newspaper in Lawrence, Kansas, where Django was developed. At the Journal-World, Jacob hacks on a number of sites including lawrence.com, LJWorld.com, and KUsports.com, and he is continually embarrassed by the multitude of media awards those sites win. In his spare time—what little of it there is—he fancies himself a chef.");
INSERT INTO books_authors(book_id, author_id) VALUES (4,3);
INSERT INTO books_authors(book_id, author_id) VALUES (4,4);
