import pickle
import os
import numpy as np


TEST_PERCENT = 0.08
VALIDATION_PERCENT = 0
class Base:


    def __init__(self, file):
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

        return dev_df, test_df, val_df


class CoinMarket(Base):


    def __init__(self, file):
        super().__init__(file)
        self.target_idx = 1
    



if __name__ == "__main__":

    coin = CoinMarket('doge_by_5min_day_20210422.pkl')
    coin.preprocess()