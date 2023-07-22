import pymysql

connection = pymysql.connect(host='localhost', port=3306, db='INVESTAR',
                             user='root', passwd='admin', autocommit=True)

cursor = connection.cursor()                    # cursor() 함수를 사용해 cursor객체를 생성한다.
cursor.execute('SELECT VERSION()')              # cursor객체의 execute()함수를 사용해 SELECT문을 실행한다.
result = cursor.fetchone()                      # cursor객체의 fetchone() 함수를 사용해 실행 결과를 튜플로 받는다.

print("MariaDB version : {}".format(result))

connection.close()