from datetime import datetime
# import module sys to get the type of exception
import sys, time
import yfinance as yf
import pandas_ta as ta
import pandas as pd
from yahoo_fin import stock_info as si
from halo import Halo

# record start time
start = time.time()

spinner = Halo(text='Processing', spinner='dots')
# Set my_debug to = 1 to display verbose feedback
my_debug = 0

# Define non-default RSI parameters
rsi_period = 7
rsi_wilder = False

# Set custom MACD parameters
fast_period = 12
slow_period = 26
signal_period = 9
#
n = 0
exceptions=0
# Get Data
stocklist = si.tickers_sp500()
date = datetime.today().strftime('%Y-%m-%d-%H-%M')

print('Process started.')
spinner.start()
try:
    for stock in stocklist:

        try:  # run the procedure inside of an error trap
        #
            n += 1
            time.sleep(1)

            if my_debug: 
                print ("\nAnalyzing {} with iteration number {}".format(stock, n))
            else:
                print(n, end = "")

            ticker = yf.Ticker(stock)
            df = ticker.history(period="1y")
            # 
            if my_debug:print(df)

            adx = ta.adx(df['High'], df['Low'], df['Close'])

            adx = df.ta.adx()

            stoch = ta.stoch(df['High'], df['Low'], df['Close'], 14, 3, 3)#STOCHk_14_3_3  STOCHd_14_3_3

            macd = df.ta.macd(fast=fast_period, slow=slow_period, signal=signal_period)#MACD_12_26_9  MACDh_12_26_9  MACDs_12_26_9

            rsi = df.ta.rsi(rsi_period)

            df = pd.concat([df, adx, stoch, macd, rsi], axis=1)

            df = df[df['RSI_7'] < 30]

            last_row = df.iloc[-1]
            if my_debug:print(last_row)

            if last_row['STOCHk_14_3_3'] >= 50 and last_row['STOCHk_14_3_3'] <=70:
                message1 = f"!Possible Uptrend: The Stoch %k is {last_row['STOCHk_14_3_3']:.2f}"
                print(message1)
            # else:
            #     message = f"The Stoch %k is {last_row['STOCHk_14_3_3']:.2f}"
            #     print(message1)

            if last_row['RSI_7'] >= 50:
                message2 = f"!Possible Uptrend: The RSI_7 is {last_row['RSI_7']:.2f}"
                print(message2)
            # else:
            #     message = f"The RSI_7 is {last_row['RSI_7']:.2f}"
            #     print(message2)

            if last_row['MACD_12_26_9'] > last_row['MACDs_12_26_9'] and last_row['RSI_7'] >= 50 and(last_row['STOCHk_14_3_3'] >= 50 and last_row['STOCHk_14_3_3'] <=70) :
                message3 = ("!Possible Uptrend {} : The MACD > Sig is {}".format(stock, last_row['MACD_12_26_9']))
                print(message3)
            # else:
            #     message = f"The MACD_12_26_9 is {last_row['MACD_12_26_9']:.2f}"
            #     print(message3)
        #
        # what happens when we have an error
        except ConnectionError as e:
            print("There was a ConnectionError", e)
            exceptions += 1
            pass
        except FileNotFoundError as e:
            print("There was a FileNotFoundError", e)
            exceptions += 1
            pass
        except KeyboardInterrupt as e:
            print("There was a KeyboardInterrupt", e)
            exception_message = f"Did user select  Ctrl-C? {e}"
            exceptions += 1
            sys.exit()
            #pass
        except KeyError as e:
            print("There was a KeyError", e)
            exceptions += 1
            pass
        except NameError as e:
            print("There was a NameError", e)
            exceptions += 1
            pass
        except IOError as e:
            print("There was a I/O error", e)
            exceptions += 1
            pass
        except RuntimeError as e:
            print("There was a RuntimeError", e)
            exceptions += 1
            pass
        except SyntaxError as e:
            print("There was a SyntaxError", e)
            exceptions += 1
            pass
        except SystemError as e:
            print("There was a SystemErrors", e)
            exceptions += 1
            pass
        except TypeError as e:
            print("There was a TypeError", e)
            exceptions += 1
            pass
        except ValueError as e:
            print("There was a ValueError", e)
            exceptions += 1
            pass
        except ZeroDivisionError as e:
            print("There was a ZeroDivisionError", e)
            exceptions += 1
            pass
        except:
            print("Exception ", sys.exc_info()[0], "occurred!")
            exceptions += 1
            #
        else:  # what happens when we don't have an error
            #
            #print('No exception occured for this ticker.')
            #n = n - exceptions
            exception_message = f"No exception occured for this many tickers {n- exceptions:.2f}"
            #
        finally:  # what happpens no matter what
            #print('Processing complete.')
            #print(date)
            pass
except:
    print("Exception ", sys.exc_info()[0], "occurred!")
    #
else:  # what happens when we don't have an error
    #
    print("**************************")
    print(exception_message)
    print('No exception occured and was passed to top level try.')
    #
finally:  # what happpens no matter what
    spinner.stop()
    print("Processing complete - ", exception_message)
    print(date)
# record end time
end = time.time()
# print the difference between start
# and end time in milli. secs
print("The time of execution of above program is :",
    (((end-start) * 10**3)/1000)/60, "mins")
  