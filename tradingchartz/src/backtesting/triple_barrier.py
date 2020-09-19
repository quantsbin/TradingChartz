# import standard
import pandas as pd
import numpy as np

from typing import Tuple


# internal imports
from tradingchartz.src.backtesting.data_classes import TripleBarrier


def triple_barrier_labels(ohlcv_with_ref_df: pd.DataFrame,
                          uni_signal_df: pd.DataFrame,
                          triple_barrier: TripleBarrier,
                          entry_point_field: str = 'Open') -> pd.DataFrame:
    """
    Calculates the triple barrier for each signal bar.
    It returns the tuple with five elements, first indicates barrier hit bar (bar # post signal bar)
    and rest 3 corresponding to each barrier either 0 or 1 based on which barrier is hit first. Last is % return
    calculated based on which ever barrier is hit first.
    For upper and lower barrier last element will be % return at barrier level itself and for vertical barrier it will
    return based on close price for vertical barrier bar.
    Note: Upper barrier hit will be calculated based on High price of following bars and similarly Lower barrier
     will be calculated based on Low price of bars and vertical barrier based on close price.
    All returns are calculated based on entry point field which is open price of next bar from signal bar as default.
    Reco: Instead of fixing the barrier level %, we can dynamically determine it as multiple of average true range on
    signal day.
    :param ohlcv_with_ref_df: OHLCV dataframe with additional field required for determining upper or lowe barrier.
    :param uni_signal_df:  signal dataframe with only uni-directions signals filtered out.
    :param triple_barrier: Triple barrier data class with corresponding barrier values.
    :param entry_point_field: Column from ohlcv df based on which entry price on next bar to signal will be calculated.
    :return: Signal df with additional column with tuple of four elements.
    """
    # TODO: We might want to replace vertical barrier and barrier hit level with datetime instead of # of bars.
    # TODO: Add config dataclass as input to be able to alter what field to be used for each calculation.
    # filter signals to ensure non-zero rows only.
    uni_signal_df = uni_signal_df[uni_signal_df.values != 0]
    # barrier calculations
    temp_uni_signal_df = uni_signal_df.to_frame(name='signals')
    temp_uni_signal_df['entry_price'] = ohlcv_with_ref_df.shift(-1).loc[temp_uni_signal_df.index, entry_point_field]
    if triple_barrier.price_move_field:
        temp_uni_signal_df[triple_barrier.price_move_field] = ohlcv_with_ref_df.loc[temp_uni_signal_df.index,
                                                                                    triple_barrier.price_move_field]
    else:
        triple_barrier.price_move_field = 'entry_price'
    # Barrier level calculations
    if triple_barrier.lower:
        temp_uni_signal_df['lower_barrier'] = temp_uni_signal_df['entry_price'] \
                                              - (temp_uni_signal_df[triple_barrier.price_move_field] *
                                                 triple_barrier.lower)
    if triple_barrier.upper:
        temp_uni_signal_df['upper_barrier'] = temp_uni_signal_df['entry_price'] \
                                              + (temp_uni_signal_df[triple_barrier.price_move_field] *
                                                 triple_barrier.upper)
    if triple_barrier.vertical:
        temp_uni_signal_df['vertical_barrier'] = ohlcv_with_ref_df.shift(-triple_barrier.vertical).loc[temp_uni_signal_df.index, 'Close']
        # vertical barrier could be NAN here if for the latest signal vertical barrier is still not hit.

    for date_index, row in temp_uni_signal_df.iterrows():
        # find barrier strategy period.
        _signal_loc = ohlcv_with_ref_df.index.get_loc(date_index)
        barrier = None
        barrier_bar = None
        if triple_barrier.vertical:
            if (_signal_loc + triple_barrier.vertical) < len(ohlcv_with_ref_df.index):
                _ref_df = ohlcv_with_ref_df.iloc[_signal_loc + 1: _signal_loc + triple_barrier.vertical, :]
                barrier = 'vertical'
                barrier_bar = _ref_df.index[-1]
        else:
            _ref_df = ohlcv_with_ref_df.iloc[_signal_loc+1:, :]
        close_position = _ref_df.iloc[-1]['Close']
        if triple_barrier.lower:
            # barrier check
            lower_barrier_check = any((_ref_df['Low'] < row['lower_barrier']).values)
            if lower_barrier_check:
                barrier = 'lower'
                _ref_df = _ref_df.iloc[:np.argmax(lower_barrier_check)+1, :]
                barrier_bar = _ref_df.index[-1]
                close_position = row['lower_barrier']
        if triple_barrier.upper:
            upper_barrier_check = any(_ref_df['High'] > row['upper_barrier'])
            if upper_barrier_check:
                barrier = 'upper'
                barrier_bar = _ref_df.index[np.argmax(upper_barrier_check)]
                close_position = row['upper_barrier']
        temp_uni_signal_df.loc[date_index, 'barrier_type'] = barrier
        temp_uni_signal_df.loc[date_index, 'barrier_bar'] = barrier_bar
        temp_uni_signal_df.loc[date_index, 'close_level'] = close_position

    return temp_uni_signal_df
