from datetime import datetime
from time import sleep
from sys import exit
from os import path
from os import mkdir
import json

class clock():
    pay = 0.0  # This should be in dollars, properly rounded
    worked_time = 0.0
    rate = 8.00
    data = {}  # This holds total pay data
    livable_rate = 16.41  # find the min livable rate for your state with livingwage.mit.edu/
    livable_pay = 0
    
    
    def __init__(self):
        # Calculate how bad/good your pay is
        if self.rate > 11.03:
            print(f'Amount above minimum livable wage: {(self.rate / self.livable_rate):.02f}X')
        else:
            print(f'Percent below minimum livable wage: {100 - ((self.rate / self.livable_rate) * 100):.02f}%')
        
        # This will determine the start time
        self.start_time = datetime.now()
        self.shutdown = False  # end program if true
        self.load_data()  # Collect data from previous session
        self.current_time = self.start_time  # We just started
        print(f'Rate: ${self.rate:.02f}/hour')
        
        
    def get_time_passed(self):
        """
        This function determines how much time has passed in seconds
        
        :param start_time: the start time as seconds
        :return: int seconds worked
        """
        
        # 1. Figure out what time it is and when we started
        now = datetime.now()
        start_time=self.start_time
        
        # 2. Figure out how much time has passed
        now_seconds = (now.hour * 3600) + (now.minute * 60) + now.second  # Get total seconds of now
        start = (start_time.hour * 3600) + (start_time.minute * 60) + start_time.second  # do same for start
        
        
        passed = now_seconds - start
        #print(f'NOW: {now_seconds}; START: {start}')
        
        # 3. Record passed time
        self.worked_time = passed
        
        return passed
        
    
    def update_pay(self, passed):
        """
        This function gets the passed time, calculates pay, and 
        updates pay variable
        
        :param passed: The amount of time that has passed in seconds 
        from start
        :return: None
        """
        
        # 1. Determine how much money made per second
        persec = (self.rate / 60) / 60  # rate divided by 60 minutes, then by 60 sec
        persec_live = (self.livable_rate / 60) / 60
        
        # 2. Calculate current cash based on time worked
        self.pay = (persec * passed)
        self.livable_pay = (persec_live * passed)
        
        
    def load_data(self):
        """
        Reads data from json file and loads into class if it can
        
        """
        if path.exists('data') and path.isfile('data/pay.json'):
            with open('data/pay.json', 'r') as file:
                self.data = json.loads(file.read())
                
        elif not path.exists('data'):
            mkdir('data')
        
        
    def save_data(self, error=False):
        """
        This saves the data to a json file
        """
        
        # 1. Collect data
        now = self.current_time
        today = f'{now.month}\\{now.day}'
        data = (self.pay, self.worked_time)
        self.data[today] = data  # Append to data with key of day
        
        # 2. Write data
        if not error:
            with open(f'data/pay.json', 'w') as file:
                file.write(json.dumps(self.data))
                
        else:
            with open(f'data/crash.json', 'w') as file:
                file.write(json.dumps(data))
        
        
    def can_buy(self):
        """
        Thresholds that show what you can buy; 18 gallon
        """
        # Lists with items according to pay
        items = {'6.49':'a classic pepperoni pizza from Little Caesars', 
                 '56.12': 'a full tank of gas in September 2022', 
                 '6.99': 'a regular sandwich from JJs',
                 '60.00': 'a new video game',
                 '4.99': 'a 40 pack of water bottles'}  # The key is the cost, the value is the item
        
        try:
            can_get = items[f'{self.pay:.02f}']
            print(f'\rYou can now buy {can_get} for {self.pay:.02f}')
        
        except KeyError:
            return  # You can't buy anything
        
        except Exception as e:  # Something weird happened, don't know why
            print(f'Error: {str(e)}')
            self.save_data(error=True)
            exit(1)
        
        
    def start(self):
        """
        This starts the main loop that keeps track of time
        
        :return: None
        """
        
        try:
            while self.worked_time < 43200:
                # Get data
                worked = self.get_time_passed()
                self.update_pay(worked)

                # Print data
                self.can_buy()
                
                print(f'\r{self.worked_time / 60:.02f} minutes worked for a pay of ${self.pay:.02f}' +
                      f' | livable: ${self.livable_pay:.02f}', end='')

                sleep(1)
                
        except KeyboardInterrupt:
            print('\nExiting ...')
            self.save_data()
            exit(0)
            
        except Exception as e:
            print(f'\nERROR: {str(e)}')
            self.save_data(error=True)
            exit(1)
            
                       
if __name__ == '__main__':
    timer = clock()
    timer.start()
