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
    except:
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
        print(df3)
        dff = df3.reindex(columns=['Sound','Flame','Humidity','Temperature'])
        print(dff)
        dff['Sound']=dff['Sound'].apply(np.ceil) #().astype('int')
        dff['Sound']=dff['Sound'].astype('int')
        dff['Flame']=dff['Flame'].apply(np.ceil) #().astype('int')
        dff['Flame']=dff['Flame'].astype('int')
        dff['Humidity']=dff['Humidity'].round(0).astype('int')
        dff['Temperature']=dff['Temperature'].round(0).astype('int')
        dff.to_csv('/data/data1.csv')
	dff.flush
        dff.close
	print(dff)
	url = os.environ.get('CLOUDAMQP_URL', 'amqps://kacojdss:aUd8wEoKcyHLCK46a1_AifxUBDzjsLHi@beaver.rmq.cloudamqp.com/kacojdss')
	params = pika.URLParameters(url)
	params.socket_timeout = 5
	connection1 = pika.BlockingConnection(params) # Connect to CloudAMQP
	channel1 = connection1.channel() # start a channel
	channel1.queue_declare(queue='pdfprocess') # Declare a queue
	csv.register_dialect('csv_dialect',delimiter='[',skipinitialspace=True,quoting=csv.QUOTE_ALL)
	with open('/data/data1.csv', 'r') as csvfile:
    		reader = csv.reader(csvfile, dialect='csv_dialect')
    		header=next(reader)
   		if header != None:
        		for row in reader:
           			print(row)
           			channel1.basic_publish(exchange='', routing_key='pdfprocess', body=str(row))
		print ("[x] Message sent to consumer")
		connection1.close()




