import unittest
import pandas as pd
import pandas_ta as ta
import Backtest_3 as bt3

class TestTechnicalIndicators(unittest.TestCase):
    def test_calculate_stoch(self):
        df = pd.DataFrame({'High': [1, 2, 3, 4, 5], 'Low': [0.5, 1.5, 2.5, 3.5, 4.5], 'Close': [1, 2, 3, 4, 5]})
        RSI_PERIOD = 7
        slow_k_period = 3
        slow_d_period = 3
        df = bt3.calculate_stoch(df, RSI_PERIOD, slow_k_period, slow_d_period)
        self.assertAlmostEqual(df.at[0, 'stoch_k'], 100.0)
        self.assertAlmostEqual(df.at[0, 'stoch_d'], 100.0)

    def test_calculate_rsi(self):
        df = pd.DataFrame({'Close': [1, 2, 3, 4, 5]})
        RSI_PERIOD = 7
        df = bt3.calculate_rsi(df, RSI_PERIOD)
        self.assertAlmostEqual(df.at[0, 'rsi'], 100.0)

    def test_calculate_macd(self):
        df = pd.DataFrame({'Close': [1, 2, 3, 4, 5]})
        FAST_PERIOD = 12
        SLOW_PERIOD = 26
        SIGNAL_PERIOD = 9
        df = bt3.calculate_macd(df, FAST_PERIOD, SLOW_PERIOD, SIGNAL_PERIOD)
        self.assertAlmostEqual(df.at[0, 'macd'], 0.0)
        self.assertAlmostEqual(df.at[0, 'macd_signal'], 0.0)
        self.assertAlmostEqual(df.at[0, 'macd_hist'], 0.0)

if __name__ == '__main__':
    unittest.main()
'''The SystemExit error message is indicating that the Python script you are running is trying to exit using the sys.exit() function. 
This can happen when the unittest.main() function is called and all tests have completed without any failures. 
The unittest.main() function returns True when all tests have passed and False when any tests have failed.

In this case, the message "SystemExit: True" suggests that all tests have passed and the script has exited successfully. 
If any tests had failed, the message would instead be "SystemExit: False".'''