import pickle
import os, random
import numpy as np
from sklearn import preprocessing
from collections import deque
import pandas as pd
import json
from links import DogeLinks

TEST_PERCENT = 0.08
VALIDATION_PERCENT = 0
class Base:


    def __init__(self, file, cb=None):
        if cb is not None:
            self.df = cb()
        else:
            assert os.path.exists(file)
            with open( file, "rb" ) as f:
                self.df = pickle.load(f)
                print(self.df.shape)
        self.target_idx = None
        self.shift_window = -1 
        # self.df.columns = [str(i) for i in range(self.df.shape[1])]
        # self.df.set_index(0, inplace=True)

    def classify_sb(self, current, future):
        if float(future) < float(current) - self.marginal:
            return 0  # sell
        elif float(future) > float(current) + self.marginal:
            return 2  # buy
        else:
            return 1  # keep

    def preprocess(self):
        target_df = self.df[[self.target_idx]]
        print(self.target_idx)
        shift_df = target_df.shift(self.shift_window)
        gap = target_df - shift_df
        gap.dropna(inplace=True)
        print(gap.describe())
        gap_np = gap.to_numpy()
        self.marginal = max(np.mean(gap_np), np.median(gap_np))
        print(self.marginal)
        # print(gap)
        assert self.marginal > 0

        label = list(map(self.classify_sb, target_df.to_numpy(), shift_df.to_numpy()))
        print('--', len(label))
        self.seq_len = len(label) // 25
        print(self.seq_len)

        self.df['label'] = pd.Series(label)

        dates = sorted(self.df[[0]].values)
        print('---')

        dev_split = dates[-int((TEST_PERCENT + VALIDATION_PERCENT) * len(dates))]
        if -int(VALIDATION_PERCENT * len(dates)) == 0:
            val_split = dates[-1]
        else:
            val_split = dates[-int(VALIDATION_PERCENT * len(dates))]
        
        dev_df = self.df[(self.df[[0]] < dev_split).to_numpy()]
        test_df = self.df[(dev_split <= self.df[[0]]).to_numpy() & (self.df[[0]] <= val_split).to_numpy()]
        val_df = self.df[(self.df[[0]] > val_split).to_numpy()]

        print("dev : ", len(dev_df), ", test :", len(test_df), ", valid :", len(val_df))

        # drop date
        dev_df = dev_df.drop([0], True)
        test_df = test_df.drop([0], True)
        val_df = val_df.drop([0], True)
        return dev_df, test_df, val_df

    def train(self):
        dev_df, test_df, val_df = self.preprocess()
        train_x, train_y = self.process_sb_df(dev_df)
        test_x, test_y = self.process_sb_df(test_df)
        from models import create_model

        dropout_01 = 0.2
        dropout_02 = 0.1
        input_shape = (train_x.shape[1:])
        print('---')
        self.model = create_model(input_shape,dropout_01,dropout_02)
        self.model.fit(train_x,train_y)

    def predict(self):
        pass

    
    def prepare_sequential_data(self, main_df):
        df = main_df.copy(deep=True)
        

        for col in df.columns[:-1]:

            df[col] = df[col].pct_change()

                # if col not in PRICE_HEADERS:
                #     if VERBOSE:
                #         # check for stationarity
                #         # https://machinelearningmastery.com/time-series-data-stationary-python/
                #         diffed_result = adfuller(df[col].values[1:], autolag="AIC")
                #         print('ADF Statistic: %f' % diffed_result[0])
                #         print('p-value: %f' % diffed_result[1])
                #         print('Critical Values:')
                #         for key, value in diffed_result[4].items():
                #             print('\t%s: %.3f' % (key, value))

        df.dropna(inplace=True)

        sequential_data = []
        close_backup = []
        prev_days = deque(maxlen=self.seq_len)

        # print("column used: ", df.columns[:-2])
        # print("target column: ", df.columns[-2])

        for i in df.values:
            prev_days.append([n for n in i[:-1]])
            if len(prev_days) == self.seq_len:
                sequential_data.append([preprocessing.scale(np.array(prev_days)), i[-1]])
                close_backup.append(i[-1])

        return sequential_data, close_backup

    def process_sb_df(self, df):
        sequential_data, close_backup = self.prepare_sequential_data(df)
        random.shuffle(sequential_data)

        sells = []
        keeps = []
        buys = []
        for seq, target in sequential_data:
            if target == 0:  # sell
                sells.append([seq, target])
            elif target == 1:  # keep
                keeps.append([seq, target])
            elif target == 2:  # buy
                buys.append([seq, target])

        random.shuffle(sells)
        random.shuffle(keeps)
        random.shuffle(buys)

        lower = min(len(sells), len(keeps), len(buys))

        sells = sells[:lower]
        keeps = keeps[:lower]
        buys = buys[:lower]

        sequential_data = sells + keeps + buys
        random.shuffle(sequential_data)

        X = []
        y = []
        for seq, target in sequential_data:
            X.append(seq)
            y.append(target)

        return np.array(X), y


class CoinMarket(Base):


    def __init__(self, file, cb=None):
        super().__init__(file, cb=cb)
        self.target_idx = 1
    



if __name__ == "__main__":
    # coin = CoinMarket('doge_by_5min_day_20210422.pkl')

    dogeLink = DogeLinks.day_by_5_min
    def cb():
        yesterday = DogeLinks.get_5min_data_by_day(1)
        today = dogeLink.get_json()
        yesterday.extend(today)
        # print(yesterday)

        df = pd.read_json(json.dumps(yesterday))
        df.to_pickle(dogeLink.get_pklename())
        return df
    # coin = CoinMarket(dogeLink.get_pklename(), cb=cb)
    coin = CoinMarket(dogeLink.get_pklename())
    coin.train()