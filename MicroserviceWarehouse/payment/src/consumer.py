####################################################################################################
# Imports                                                                                         ##
####################################################################################################

# Standard modules:
import time

# Use the following when trying to run this file directly rather than using this module from outside
#import sys                                               
#from os.path import dirname, abspath                     
#sys.path.insert(0, dirname(dirname(abspath(__file__))))  

# Internal Modules:
from src import redis
from src.models import Order


####################################################################################################
# Configurations                                                                                  ##
####################################################################################################

key = 'order_refund'
group = 'payment-group'


####################################################################################################
# Code start                                                                                      ##
####################################################################################################

def run_consumer_stream():
    try:
        redis.xgroup_create(key, group)
    except:
        print('Group already exists')

    while True:
        try:
            results = redis.xreadgroup(group, key, {key: '>'}, None) 
            # `>` means read newer msgs not read by any consumers in consumer group
            
            #print(results)     
            
            if results != []:
                print(results)
                for result in results:
                    obj = result[1][0][1]
                    order = Order.get(obj['pk'])

                    order.status = 'refunded'
                    order.save()
                    
        except Exception as e:
            print(str(e))
        
        time.sleep(1)

# Only needed when running this file directly
# run_consumer_stream()
