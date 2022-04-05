#!/usr/bin/env python
import pika, sys, os
import datetime
from datetime import datetime
import time
import csv
import pandas
##
import pika, os, logging
logging.basicConfig()
from csv import reader
##
def main():
    with open('/data/data.csv', mode='a') as data:
        data_writer = csv.writer(data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    import pandas as pd
    f = open("/data/data.csv","a")
    if os.stat('/data/data.csv').st_size == 0:
        f.write("Date,Sound,Flame,Humidity,Temperature\n")
    f = open('/data/data.csv', 'r+')
#    f.truncate(0) # need '0' when using r+
    credentials = pika.PlainCredentials('haleema', '4chyst')
    parameters = pika.ConnectionParameters('192.168.0.126',
                                   5672,
                                   '/',
                                   credentials)

    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
#    channel.queue_declare(queue='task_queue', durable=True)
    channel.exchange_declare(exchange='logs', exchange_type='fanout')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='logs', queue=queue_name)

    x=''
    h=''
    def callback(ch, method, properties, body): #for tem
            f = open("/data/data.csv","a")
            print(datetime.today().strftime('%Y/%m/%d %H:%M:%S') + ":   received    "+ str( body)+"\n")
            m= body.decode()   
#            print(str(m[0]),str(m[2]),str(m[4]),str(m[6]))
            if m[5]==':':
                h=str(m[4])
            else:
                h=str(m[4:6])
            if m[7]=='-':
                x=str(m[7:10])
            else:
                x=str(m[7:9])        
            f.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S')+","+m[0] +","+m[2]+","+h+","+x+"\n")
 
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
if __name__ == '__main__':
    try:
        main()
#        val1,val2,val3,val4 =  main()
#        f = open("/data/data.csv","a")
 ##       f.write(datetime.today().strftime('%Y-%m-%d' + "," '%H:%M:%S')+","+str( val1)+","+str(val2)+","+str(val3)+","+str(val4)+"\n")
   #     print(datetime.today().strftime('%Y-%m-%d' + "," '%H:%M:%S') + ": " + str(val1) + ":" + str(val2)+":"+str(val3)+":"+str(val4))   

#        from pandas import read_csv
#        mydf = read_csv("/data/data.csv")
#        mydf.set_index('Date',inplace=True)
#        new_mydf=mydf.interpolate(method="time")
#        n=new_mydf.dropna()
 #       print(mydf.head())
        #print(n)
#        main()
#heeeereeeeeee    print (st)
#    except KeyboardInterrupt:
    except:
     #   f = open("/data/data.csv","a")
      #  f.write(datetime.today().strftime('%Y-%m-%d' + "," '%H:%M:%S')+","+str( val1)+","+str(val2)+","+str(val3)+","+str(val4)+"\n")
       # print(datetime.today().strftime('%Y-%m-%d' + "," '%H:%M:%S') + ": " + str(val1) + ":" + str(val2)+":"+str(val3)+":"+str(val4))   
        connection.close()
        import pandas as pd
        df=pd.read_csv("/data/data.csv")
        df['Date']=pd.to_datetime(df['Date'])
        print (type(df['Date'][0]))
        print(df)
        df.set_index('Date', inplace=True)
        import numpy as np
        df=df.replace({'Humidity':'0', 'Temperature':'0'},np.NaN)
        df=df.interpolate()
        df3=df.pivot_table(index=pd.Grouper(freq='T')) #.agg({'Sound':'sum','Flame':'sum'}) #,columns=['Humidity','Temperature']) #/// freq=S,T,h,M,Y
#        df3 = df3[['Date','Sound','Flame','Humidity','Temperature']] #[['mean', '0', '1', '2', '3']]
        print(df3)
        dff = df3.reindex(columns=['Sound','Flame','Humidity','Temperature'])
#        dff.columns = pd.Index([0], dtype='int64')

        #df3.sort(['Date','Sound','Flame','Humidity','Temperature'])
        print(dff)
        dff['Sound']=dff['Sound'].apply(np.ceil) #().astype('int')
        dff['Sound']=dff['Sound'].astype('int')
        dff['Flame']=dff['Flame'].apply(np.ceil) #().astype('int')
        dff['Flame']=dff['Flame'].astype('int')
        dff['Humidity']=dff['Humidity'].round(0).astype('int')
        dff['Temperature']=dff['Temperature'].round(0).astype('int')
        dff.to_csv('/data/data1.csv') #, index=False)     
	print(dff)
        
#######################
#######################
#########################
url = os.environ.get('CLOUDAMQP_URL', 'amqps://kacojdss:aUd8wEoKcyHLCK46a1_AifxUBDzjsLHi@beaver.rmq.cloudamqp.com/kacojdss')
params = pika.URLParameters(url)
params.socket_timeout = 5

connection1 = pika.BlockingConnection(params) # Connect to CloudAMQP
channel1 = connection1.channel() # start a channel
channel1.queue_declare(queue='pdfprocess') # Declare a queue
# send a message
##import pandas as pd
##df=pd.read_csv('data1.csv')
##for row in df:
#with open('data1.csv', 'r') as read_obj:
 #   csv_reader = reader(read_obj)
   # header = next(csv_reader)

csv.register_dialect('csv_dialect',
                    delimiter='[',
                    skipinitialspace=True,
                    quoting=csv.QUOTE_ALL)
with open('/data/data1.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, dialect='csv_dialect')
    header=next(reader)
   
 # Check file as empty
    if header != None:
#import pandas as pd
#df=pd.read_csv('data1.csv')
        for row in reader:
   # row variable is a list that represents a row in csv
#import pandas as pd
#df=pd.read_csv('data1.csv') #,usecols=['Date', 'Sound', 'Flame', 'Humidity', 'Temperature']) 

#for row in 'data1.csv': 
           print(row)
           channel1.basic_publish(exchange='', routing_key='pdfprocess', body=str(row))
print ("[x] Message sent to consumer")
connection1.close()


############################
###########################
##########################
        

        
#####        from pandas import read_csv
####        mydf = read_csv("/data/data.csv")
#        mydf = read_csv("/data/data.csv",parse_dates=['date'],dayfirst=True)
       # mydf.set_index('date',inplace=True)
        #new_mydf=mydf.interpolate()
       # new_mydf=mydf.replace(0,np.NaN)
#        n=new_mydf.dropna()
#        import pandas as pd 
 #       import numpy as np
  #      df=pd.read_csv("/data/data.csv")
#        new_mydf=mydf.pivot_table(index="Time",columns="Date",aggfunc="sum") 
#####        new_mydf = mydf.to_csv("ddd.csv",header=False)
  #      new_mydf=df.replace(0,np.NaN)
#####        print(new_mydf)        
    #    print("\n")       
     #   n=new_mydf.dropna(how="all")
      #  print(n)
##1 Cloud        df4=df.resample('D').mean() #in Cloud
##2         print(df4)
##3         print('Interrupted')
        ####try:
#            from pandas import read_csv
#            mydf = read_csv("/data/data.csv",parse_dates=["Date"])
 #           mydf.set_index('Date',inplace=True)
  #          new_mydf=mydf.interpolate(method="time")
    #        n=new_mydf.dropna()
   #         print(mydf.head())
     #       print(n)
            ####sys.exit(0)
        ####except SystemExit:
            ####os._exit(0)

          # from pandas import read_csv
#           f = open("/data/data.csv","r+")
          # mydf.set_index('Date',inplace=True)
          # new_mydf=mydf.interpolate(method="time")
           #n=new_mydf.dropna()
 #          print(f)
  #         os.exit(0)
#           print(mydf.head())
 #   f.flush
  #  f.close

## a=w and the close and flush is enabled
