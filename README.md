# log-analysis
the project is to create a reporting tool that prints out reports (in plain text) based on the data in the database. 
This reporting tool is a Python program using the psycopg2 module to connect to the database.
below are the questions the reporting tool should answer
1. What are the most popular three articles of all time? 
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors

in th project i created 4 views on data base as below

1- view 1 with name log_with_name to pdifay the ptah.log to be simlier to articles.slug by substring function as below

create view log_with_name as

select SUBSTRING(log.path,10) as name from log;

and you can use it with below  command 
 select * from log_with_name;  

2- view 2 with name auther_article  to link between articles, authors to get article with author

create view auther_article as
select title, name ,slug
from articles, authors
where articles.author = authors.id;

and you can use it with below command 
 select * from auther_article;  

3- view 3 with name error_day  to get number of error status per day after trunc time from each date

create view error_day as
select date_trunc('day',time) as day , count(*) as error from log
where status='404 NOT FOUND'
group by day;

and you can use it with below command 
 select * from error_day; 

4- view 4 with name requests_day to get total requests per day after trunc time from each date
create view requests_day as
select date_trunc('day',time) as day , count(*) as requests from log
group by day;

and you can use  it with below command 
 select * from requests_day; 

- after creating above below each question can be done with single query


 to run the code from shell as below after CD to the file location 

vagrant@vagrant:/vagrant$ python log_analysis.py


