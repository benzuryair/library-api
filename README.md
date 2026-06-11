# Project name Library — API

## System description

The system will manage a list of friends  
and a list of books. You can add friends and add books.  
The system will be able to manage  
the number of books per friend  
and it will be able to return a summary of data.

##

## Docker requirements

Run this command to set up  
and run the container and create the database.

```docker run mysql_library my-mysql \```  
```-e  MYSQL_ROOT_PASSWORD=root \```  
```-e MYSQL_DATABASE=library_db \```  
```-p 3306:3306 \```  
```mysql:latest```
##

## Folder structure

library-api/  
│  
├── app/  
│   ├── main.py  
│   ├── database/  
│   │   ├── db\_connection.py  
│   │   ├── book\_db.py  
│   │   └── member\_db.py  
│   ├── routes/  
│   │   ├── book\_routes.py  
│   │   ├── member\_routes.py  
│   │   └── report\_routes.py  
│   └── logs/  
│       └── app.log  
│  
├── README.md  
├── requirements.txt  
└── .gitignore
##

## Table structure

### books table

|field | type|  
| :----- | ----------|  
id | INT PRIMARY KEY AUTO_INCOMANT 
title | VARCHAR(50)  NOT NULL  
author | VARCHAR(50)NOT NULL   
genre | ENUM (Fiction Non-Fiction Science History Other) NOT NULL
is_available_is | boolean NOT NULL  
borrowed_by_member_id | INT   

##

### Member table  
|field | type|  
| :----- | ----------|  
id | INT PRIMARY KEY AUTO_INCOMANT  
name | VARCHAR(50) NOT NULL  
email | UNIQUE NOT NULL  
is_active | boolean NOT NULL  
total_borrows | INT NOT NULL  

##

## System rules  

|law|subject|rule|
| :-----| :-------| :-------------|
|1|Creating book | User sends genre/author/title — system adds is_available=True, borrowed_by=NULL|  
|2|genre|Must be  Fiction / Non-Fiction / Science / History / Other-Any other value returns an error Make sure both the POST and PATCH are valid.  
|3|Create friend|User sends email/name — system adds is_active=True total_borrows=0  
|4|email|Must be unique — if it already exists returns an error  
|5| Inactive member| If is_active=False — book cannot be borrowed  
|6| Book unavailable|You cannot borrow a book that is already borrowed (is_active=False)  
|7| Maximum Books| A member cannot hold more than 3 books at a time.  
|8|Returning book| A book can only be returned if it is lent to the same friend who is returning it.  

##

# Endpoint list  

### Books
|Method|Endpoint|Description|
| :----| :----------| :---------|
|POST|  /books | Creating a book|
|GET| /books | All books|  
|GET| /books/{id}| Book by id|
|PATCH | /books/{id} | Book update|  
|PATCH | /books/{id}/borrow/{member_id} | Lending a book to a friend|  
|PATCH| /books/{id}/return/{member_id}| Returning a book to a friend  

##

### Members
|Method|Endpoint|Description|
| :----| :----------| :---------|
|POST| /members|Create a friend|  
GET | /members| All friends|  
GET | /members/{id} | Member by ID|  
|PATCH|/members/{id}|Member Update  
|PATCH| /members/{id}/deactivate| Disabling a friend  
|PATCH |/members/{id}/activate | Member activation  

##

### Reports
|Method|Endpoint|Description|
| :----| :----------| :---------|  
|GET| /reports/summary| General report|  
|GET | /reports/top-member| The most active member|

##
# System flow  
HTTP request -> Fast API -> End point -> Database query -> Returning a response to the user  
 
##
# Running instructions  

- Python 3.13.14
- Docker
- python -m venv venv
- venv\Scripts\activate
- Fast API
- uvicorn
- mysql.connector
- pip install -r requirements.txt