import time
import MetaTrader5 as mt5
from datetime import datetime
import pandas as pd
       

class Meta:
    def __init__(self,test,path):
        self.test=test
        self.path=path

      
        
    def onBar(self,timeframe,function_done):
     while True:
        function_done()
        time.sleep(timeframe) 



    def last(self,pair):
        # establish connection to the MetaTrader 5 terminal
        if not mt5.initialize():
            print("initialize() failed, error code =",mt5.last_error())
            quit()
        # attempt to enable the display of the GBPUSD in MarketWatch
        selected=mt5.symbol_select(pair,True)
        if not selected:
            print("Failed to select GBPUSD")
            mt5.shutdown()
            quit()
        # display the last GBPUSD tick
        # lasttick=mt5.symbol_info_tick("GBPUSD")
        symbol_info_tick_dict = mt5.symbol_info_tick(pair)._asdict()
        return  symbol_info_tick_dict


    def getBarByIndex(self,pair,numbers,timeframe):
      
        pd.set_option('display.max_columns', 500) # number of columns to be displayed
        pd.set_option('display.width', 1500)      # max table width to display
        
        # establish connection to MetaTrader 5 terminal
        if not mt5.initialize(self.path):
            print("initialize() failed, error code =",mt5.last_error())
            quit()
        if timeframe=="H1":
            timeFrames=mt5.TIMEFRAME_H1
        if timeframe=="M15":
            timeFrames=mt5.TIMEFRAME_M15      
            
        if timeframe=="M5":
            timeFrames=mt5.TIMEFRAME_M5  
        if timeframe=="M1":
            timeFrames=mt5.TIMEFRAME_M1            
        #for example timeframe
        #mt5.TIMEFRAME_H1
        # get 10 GBPUSD D1 bars from the current day
        rates = mt5.copy_rates_from_pos(pair, timeFrames, 0, numbers)
        
        # shut down connection to the MetaTrader 5 terminal
        mt5.shutdown()
        
        # create DataFrame out of the obtained data
        rates_frame = pd.DataFrame(rates)
        # convert time in seconds into the datetime format
        rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
        return rates_frame

        
    def Order_Send(self,pair):
            # establish connection to the MetaTrader 5 terminal
            if not mt5.initialize():
                print("initialize() failed, error code =",mt5.last_error())
                quit()
            
            # prepare the buy request structure
            symbol = pair
            symbol_info = mt5.symbol_info(symbol)
            if symbol_info is None:
                print(symbol, "not found, can not call order_check()")
                mt5.shutdown()
                quit()
            
            # if the symbol is unavailable in MarketWatch, add it
            if not symbol_info.visible:
                print(symbol, "is not visible, trying to switch on")
                if not mt5.symbol_select(symbol,True):
                    print("symbol_select({}}) failed, exit",symbol)
                    mt5.shutdown()
                    quit()
            
            lot = 0.1
            point = mt5.symbol_info(symbol).point
            price = mt5.symbol_info_tick(symbol).ask
            deviation = 20
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot,
                "type": mt5.ORDER_TYPE_BUY,
                "price": price,
                "sl": price - 100 * point,
                "tp": price + 100 * point,
                "deviation": deviation,
                "magic": 234000,
                "comment": "python script open",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_RETURN,
            }
            
            # send a trading request
            result = mt5.order_send(request)
            # check the execution result
            print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol,lot,price,deviation));
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print("2. order_send failed, retcode={}".format(result.retcode))
                # request the result as a dictionary and display it element by element
                result_dict=result._asdict()
                for field in result_dict.keys():
                    print("   {}={}".format(field,result_dict[field]))
                    # if this is a trading request structure, display it element by element as well
                    if field=="request":
                        traderequest_dict=result_dict[field]._asdict()
                        for tradereq_filed in traderequest_dict:
                            print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
                print("shutdown() and quit")
        


    def ChangingStop(self,ticket,sl):
         # establish connection to the MetaTrader 5 terminal
            if not mt5.initialize(self.path):
                print("initialize() failed, error code =",mt5.last_error())
                quit()
            request = { 'action': mt5.TRADE_ACTION_SLTP, 'position': ticket, 'sl': sl }
            #// perform the check and display the result 'as is'
            result = mt5.order_send(request)
            # print("Modified StopLoss")

            # if result.retcode != mt5.TRADE_RETCODE_DONE:
                # print("4. order_send failed, retcode={}".format(result.retcode))

                # print(" result",result)
            return True


    def ChangingTP(self,ticket,tp):
         # establish connection to the MetaTrader 5 terminal
            if not mt5.initialize(self.path):
                print("initialize() failed, error code =",mt5.last_error())
                quit()
            request = { 'action': mt5.TRADE_ACTION_SLTP, 'position': ticket, 'tp': tp }
            #// perform the check and display the result 'as is'
            result = mt5.order_send(request)
            # print("Modified StopLoss")

            # if result.retcode != mt5.TRADE_RETCODE_DONE:
                # print("4. order_send failed, retcode={}".format(result.retcode))

                # print(" result",result)
            return True        


    def PositionTotal(self):
        # establish connection to MetaTrader 5 terminal
        if not mt5.initialize(self.path):
            print("initialize() failed, error code =",mt5.last_error())
            quit()
        
        # check the presence of open positions
        positions_total=mt5.positions_total()  
        return position_total  

    def LoginAccount(self):
        # now connect to another trading account specifying the password
        # establish connection to the MetaTrader 5 terminal
            if not mt5.initialize(self.path):
                print("initialize() failed, error code =",mt5.last_error())
                quit()
            account=5003581043
            authorized=mt5.login(account, password="rmxxi5er",server="MetaQuotes-Demo")
            if authorized:
                # display trading account data 'as is'
                print(mt5.account_info())
                # display trading account data in the form of a list
                print("Show account_info()._asdict():")
                account_info_dict = mt5.account_info()._asdict()
                for prop in account_info_dict:
                    print("  {}={}".format(prop, account_info_dict[prop]))
            else:
                print("failed to connect at account #{}, error code: {}".format(account, mt5.last_error()))
 
    