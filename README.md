# socialnetwork

## Run application
1- Build image with command <br>
docker build -t fastapi-app .

2- run docker compose with command <br>
docker-compose up

3- open this like in your browser <br>
http://0.0.0.0:8000/docs

## Create the social network database
connect the Postgres server with username admin and password admin, and the create database called socialnetwork

## fill database

1- add individuals

add individuals by using endpoint /v1/individual/ <br>
Name | birthday | other details

	1. "Ali"	"2024-11-23"	"string"
	2. "hassan"	"2024-11-23"	"string"
	3. "John"	"2024-11-23"	"string"	
	4. "travolta"	"2024-11-23"	"string"

2- add individuals

add family by using endpoint /v1/family/ <br>
family name

  1.	"home"
  2.	"work"
  3.	"sport"

3- create membership

create membership by using endpoint /v1/familymember/ <br>
family id | individual id
 
  1. 1 1
  2. 1 2
  3. 1 3
  4. 2 2
  5. 2 3
  6. 3 2
  7. 3 3
  8. 3 4

4- create patient /v1/patient/
creat a patient by using end point /v1/patient/ <br>
family id | individual id
  1. 1 1

5- creat memory
create a memory by using endpoint /v1/patient/ <br>
family id | individual id | text
  1. 1 1 "Hi all"
  2. 1 2 "Good Morning"
  3. 1 3 "How are you"
  4. 2 2 "Welcome"
  5. 2 3 "Bonjour"
  6. 3 2 "I am good"
  7. 3 3 "Good day"
  8. 3 4 "Happy"

     
