from datetime import datetime
from time import sleep
from sys import exit
from os import path
from os import mkdir
import json

class clock():
    pay = 0.0  # This stores your earned pay
    worked_time = 0.0  # This records how long you've worked
    rate = 8.00  # This is your pay per hour, edit it to match your rate
    data = {}  # This holds total pay data; will contain data from previous days
    
    
    def __init__(self):
        # This will determine the start time
        self.start_time = datetime.now()  # This grabs the current time 
        self.shutdown = False  # end program if true
        self.load_data()  # Collect data from previous session
        self.current_time = self.start_time  # Set the current time to the start time; it will update as we go
        
        
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
        
        # 2. Calculate current cash based on time worked
        self.pay = (persec * passed)
        
        
        
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
                print(f'\r{self.worked_time / 60:.02f} minutes worked for a pay of ${self.pay:.02f}', end='')

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
