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
from src.models import Product


####################################################################################################
# Configurations                                                                                  ##
####################################################################################################

key = 'order_complete'
group = 'inventory-group'


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
            
            #print(results)     # output in appendix 1 below
            if results != []:
                for result in results:
                    obj = result[1][0][1]       # Appendix 2
                    prod = Product.get(obj['product_id'])
                    
                    print(prod)
                    prod.qty = prod.qty - int(obj['qty'])
                    prod.save()
        except Exception as e:
            print(str(e))
        
        time.sleep(1)

# Only needed when running this file directly
# run_consumer_stream()


'''
Appendix 1:
Output of print(results):
[]
[]
[['order_complete', [('1662011548778-0', {'pk': '01GBVSPZ5Q6460RD49BF6G7PA8', 'product_id': '01GAJ4PX6WTKVAZJ4EQMF897CD', 'price': '800.0', 'fee': '160.0', 'total': '960.0', 'qty': '2', 'status': 'completed'})]]]
[]
[]

'''

'''
The output is :
[['order_complete', [('1662011548778-0', {'pk': '01GBVSPZ5Q6460RD49BF6G7PA8', 'product_id': '01GAJ4PX6WTKVAZJ4EQMF897CD', 'price': '800.0', 'fee': '160.0', 'total': '960.0', 'qty': '2', 'status': 'completed'})]]]

So result[0] is:
'order_complete'

So result[1] is:
[('1662011548778-0', {'pk': '01GBVSPZ5Q6460RD49BF6G7PA8', 'product_id': '01GAJ4PX6WTKVAZJ4EQMF897CD', 'price': '800.0', 'fee': '160.0', 'total': '960.0', 'qty': '2', 'status': 'completed'})]

It has one tuple so result[1][0]:
('1662011548778-0', {'pk': '01GBVSPZ5Q6460RD49BF6G7PA8', 'product_id': '01GAJ4PX6WTKVAZJ4EQMF897CD', 'price': '800.0', 'fee': '160.0', 'total': '960.0', 'qty': '2', 'status': 'completed'})

Therefore, result[1][0][1]:
{'pk': '01GBVSPZ5Q6460RD49BF6G7PA8', 'product_id': '01GAJ4PX6WTKVAZJ4EQMF897CD', 'price': '800.0', 'fee': '160.0', 'total': '960.0', 'qty': '2', 'status': 'completed'}

'''