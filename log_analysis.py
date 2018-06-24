import psycopg2


db = psycopg2.connect("dbname=news")
c = db.cursor()

# create 4  views to help to complete the  project
# view 1 with name log_with_name to pdifay the ptah.log to be simlier to articles.slug
c.execute(" create view log_with_name as select SUBSTRING(log.path,10) as name from log;")
# view 2 with name auther_article  to link between articles, authors to get article with author
c.execute(" create view auther_article as select title, name ,slug from articles, authors "
          "where articles.author = authors.id;")
# view 3 with name error_day  to get number of error status per day after trunc time from each date
c.execute("create view error_day as select date_trunc('day',time) as day , count(*) as error from log"
          " where status='404 NOT FOUND' group by day;")
# view 4 with name requests_day to get total requests per day after trunc time from each date
c.execute("create view requests_day as select date_trunc('day',time) as day , count(*) as requests from log"
          " group by day;")
db.commit()

# 1. What are the most popular three articles of all time?

c.execute("select title, count (*) as views from articles, log_with_name "
          "where articles.slug = log_with_name.name group by articles.title "
          "order by views desc limit 3;")
article_views = c.fetchall()
print("1. What are the most popular three articles of all time?\n")
j = 1
for article in article_views:
    print(str(j) + "- " + article[0] + " --- " + str(article[1]) + " views")
    j += 1

# 2. Who are the most popular article authors of all time?
c.execute("select auther_article.name,count (*) as views from auther_article,log_with_name"
          " where auther_article.slug=log_with_name.name group by auther_article.name"
          " order by views desc;")
auther_views = c.fetchall()
print("\n2. Who are the most popular article authors of all time?\n")
i = 1
for auther in auther_views:
    print(str(i)+"- "+auther[0] + " --- " + str(auther[1]) + " views")
    i += 1


# 3. On which days did more than 1% of requests lead to errors?

c.execute("select requests_day.day , 100.0*error_day.error / requests_day.requests as views"
          " from error_day,requests_day where error_day.day=requests_day.day"
          "  and (100.0*error_day.error / requests_day.requests) >1; ")
max_error_day = c.fetchall()
print("\n3. On which days did more than 1% of requests lead to errors?\n")

print("* - "+str(max_error_day[0][0]).strip("00:00:00+00:00")
      + " --- " + str(round(max_error_day[0][1], 2)) + "% errors")

db.close()
