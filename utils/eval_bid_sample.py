'''OIBC 입찰평가 샘플코드.

>>> python eval_bid_sample.py

- 거래일 전날 10시와 17시, 2회에 걸쳐 거래일의 발전량 예측치를 제출
- 값이 작을수록 우수한 것으로 평가
- 예측 구간의 평균값을 기준으로 한 예측 오차, 예측 구간의 범위, 실제 발전량이 예측 구간에 포함 여부를 평가 산식에 반영
'''
from typing import List

TOTAL_CAPACITY = 472.39
ONE_HOUR_SEC = 3600
BID_ROUNDS = (1, 2)



def get_bids(bid_round: int):
    '''It returns bids of a round.
    '''
    # yapf: disable
    if bid_round == 1:
        return [{'upper': 0.466345, 'lower':	0.230843 },
                {'upper': 0.567372, 'lower':	0.359294 },
                {'upper': 0.64214, 'lower':	0.422306 },
                {'upper': 0.633863, 'lower':	0.430583 },
                {'upper': 0.731684, 'lower':	0.523116 },
                {'upper': 4.46094, 'lower':	1.94934 },
                {'upper': 28.8429, 'lower':	21.5973 },
                {'upper': 157.968, 'lower':	135.319 },
                {'upper': 251.94, 'lower':	215.217 },
                {'upper': 301.396, 'lower':	256.607 },
                {'upper': 341.945, 'lower':	287.457 },
                {'upper': 350.265, 'lower':	295.476 },
                {'upper': 337.388, 'lower':	284.472 },
                {'upper': 292.387, 'lower':	246.6 },
                {'upper': 213.398, 'lower':	177.735 },
                {'upper': 126.211, 'lower':	104.286 },
                {'upper': 49.9768, 'lower':	41.1908 },
                {'upper': 10.7792, 'lower':	8.81546 },
                {'upper': 0.506506, 'lower':	0.23773 },
                {'upper': 0.437049, 'lower':	0.307187 },
                {'upper': 0.361154, 'lower':	0.223965 },
                {'upper': 0.393793, 'lower':	0.247636 },
                {'upper': 0.277296, 'lower':	0.124851 },
                {'upper': 0.289877, 'lower':	0.112269 },]
    if bid_round == 2:
        return [{'upper': 0.466345, 'lower':	0.230843},
                {'upper': 0.567372, 'lower':	0.359294},
                {'upper': 0.64214, 'lower':	0.422306},
                {'upper': 0.633863, 'lower':	0.430583},
                {'upper': 0.632836, 'lower':	0.424268},
                {'upper': 4.46094, 'lower':	1.94934},
                {'upper': 29.4418, 'lower':	22.1962},
                {'upper': 157.79, 'lower':	135.141},
                {'upper': 261.021, 'lower':	224.299},
                {'upper': 306.443, 'lower':	261.655},
                {'upper': 352.986, 'lower':	298.498},
                {'upper': 359.789, 'lower':	305},
                {'upper': 337.388, 'lower':	284.472},
                {'upper': 288.333, 'lower':	242.545},
                {'upper': 215.469, 'lower':	179.806},
                {'upper': 123.616, 'lower':	101.691},
                {'upper': 49.0548, 'lower':	40.2688},
                {'upper': 10.7792, 'lower':	8.81546},
                {'upper': 0.386865, 'lower':	0.118089},
                {'upper': 0.317408, 'lower':	0.187546},
                {'upper': 0.241513, 'lower':	0.104324},
                {'upper': 0.274152, 'lower':	0.127995},
                {'upper': 0.277296, 'lower':	0.124851},
                {'upper': 0.289877, 'lower':	0.112269}]
    return [{'upper': 0, 'lower': 0}]*24 
    # yapf: enable


def get_gens() -> List[float]:
    '''It returns pv power generations of a group.
    '''
    # yapf: disable
    return [0, 0, 0, 0, 0, 0, 3.6, 62.8, 161, 215.3, 307.3, 360.4, 
        366.7, 350.5, 317.6, 236.3, 153.9, 46.2, 3.6, 0, 0, 0, 0, 0]
    # yapf: enable


if __name__ == '__main__':
    gens = get_gens()
    sum_value: float = 0
    for idx, gen in enumerate(gens):
        util_errs = []
        for bid_round in BID_ROUNDS:
            bids = get_bids(bid_round)
            bid = bids[idx]
            real_gen = gens[idx]

            value = (
                abs((bid['upper'] + bid['lower']) / 2 - real_gen) / TOTAL_CAPACITY
                + (bid['upper'] - bid['lower']) / (2 * TOTAL_CAPACITY)
                + real_gen * (1 if bid['lower'] > real_gen or bid['upper'] < real_gen else 0) / TOTAL_CAPACITY
            )
            print(f'Idx({idx}), Round({bid_round}) | '
                  f'Evaluation value: {value} (%) / '
                  f'Bid: {bid} (kWh) / '
                  f'Gen: {gen} (kWh)')
            sum_value += value

    print(f'Total Evaluation value: {sum_value} (KRW)')