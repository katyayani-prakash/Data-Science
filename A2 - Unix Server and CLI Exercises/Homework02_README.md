# COMP 598 Homework 2 – Unix server and command-line exercises
30 pts

The goal of this assignment is for you to get more familiar with your Unix EC2 – both as a data science machine and as a server (as a data scientist, you’ll need it as both).

## Task 1: Setting up a webserver (15 pts)

The objective of this task is to setup your EC2 instance to run an apache webserver on port 8008. Your goal is to have it serving up the file comp598\_hw2.txt at the www root. In other words, my web browser can access it at [http://X.Y.Z.W:8008/comp598_hw2.txt](http://x.y.z.w:8008/comp598_hw2.txt), where X.Y.Z.W is the public IP address of your EC2. The file itself should be empty.

One key detail to keep in mind is the security configuration of your EC2 - you’ll need to ensure that it allows port 8008 traffic through.

## Task 2: Setting up a database server (15 pts)

The objective of this task is to setup your EC2 instance to run an instance of the MariaDB database on port 6002. Your goal is for a TA to be able to log into the database server and access an empty database named “comp598\_test” as the “comp598\_grader” user. To do this, you will need to do the following in roughly this order:

1. Install the MariaDB database server (try Googling “install mariadb ubuntu”...)
2. Configure the database to run on an external port
3. Create an empty database named “comp598\_test”
4. Add a new user “comp598\_grader” to your database server with permission to access the comp598\_test database. Use the password “$ungl@ss3s” for the password for this user.

Make sure your MariaDB instance is publicly accessible, otherwise the TAs won't be able to grade this question.

To test this, the TA will use the mariadb (or mysql) command line client to log into the database (e.g., “mariadb -u comp598\_grader -p -h INSTANCE\_IP”) and then enter “use comp598\_test;” at the prompt. You should be able to do this as well.

Some Tips
- This assignment will involve a substantial amount of googling and working on the UNIX command line.
- If you don’t understand a concept, google it and read up on it
- If you don’t understand how to do something, try googling it and making sense of instructions you find
- You **will** need to edit files on your EC2. My preferred editor is vim - but there’s a learning curve. If this is your first time really using unix, I would recommend using pico or nano.

Submission Instructions

Your MyCourses submission should contain – at minimum - the following:
- ip\_address.txt containing exactly one line containing the public IP address of your EC2 instance.

In addition to the submission file:
- Leave your EC2 server running until Sept 28 @ 11:59 PM so that the server can be checked for the file and database login.
