from math import sin, asin, cos, radians, sqrt
from Geohash import encode
from DataAnalysis import read_data
from Graph import draw_map
from similarity import find_same
import time
import numpy
from pandas import DataFrame

class k_and_r:

    def haversine(self, lon1, lat1, lon2, lat2):
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 6371  # average radium of the earth , kilometer
        # 单位是米
        return c * r * 100

    def preprocessing(self, df):
        h4 = []
        h3 = []
        h2 = []
        h1 = []
        for index in range(df.shape[0]):
            h = encode(df['lat'][index], df['lon'][index], 4)
            h4.append(h)
            h3.append(h[0:3])
            h2.append(h[0:2])
            h1.append(h[0])
        df.insert(0, 'h4', h4)
        df.insert(0, 'h3', h3)
        df.insert(0, 'h2', h2)
        df.insert(0, 'h1', h1)
        return df

    def cal(self, df, lon, lat, n, attr, query_str):
        return df
        pass

    # 模板方法
    def top_fun(self, lon, lat, n, map_html, attr, query_str):
        self.df = read_data()
        start = time.time()
        self.df = self.preprocessing(self.df)
        self.df_res = self.cal(self.df, lon, lat, n, attr, query_str)
        end = time.time()
        run_time = end-start
        draw_map(self.df_res, map_html)
        return run_time


class R(k_and_r):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(R, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    # 排序
    def heap_adjust(self, arr, low, high):
        tmp = arr[low]
        i = low
        j = 2 * i + 1

        while j < high:
            if j < high - 1 and arr[j] < arr[j + 1]:
                j = j + 1
            if tmp < arr[j]:
                arr[i] = arr[j]
                i = j
                j = 2 * i + 1
            else:
                break
        arr[i] = tmp

    def top_heap_sort(self, arr):
        length = len(arr)
        first_exchange_elem = (int)(length / 2) - 1
        for x in range(first_exchange_elem + 1):
            self.heap_adjust(arr, first_exchange_elem - x, length)
        return arr

    def find_largest(self, df1, lon, lat, r):
        if df1.shape[0] == 0:
            return r - 1
        else:
            dis = []
            for index in range(df1.shape[0]):
                distance = self.haversine(df1['lat'][index], df1['lon'][index], lat, lon)
                dis.append(distance)
            df1.insert(0, 'distance', dis)

            arr = numpy.array(dis)
            arr = self.top_heap_sort(arr)
            return arr[0]

    def r_cal(self, df, lon, lat, r):
        h_goal = encode(lat, lon, 4)
        df1 = df[df.h4 == h_goal[0:4]]
        df1 = df1.reset_index(drop=True)
        if (self.find_largest(df1, lon, lat, r) < r):
            df1 = df[df.h3 == h_goal[0:3]]
            df1 = df1.reset_index(drop=True)
            if (self.find_largest(df1, lon, lat, r) < r):
                df1 = df[df.h2 == h_goal[0:2]]
                df1 = df1.reset_index(drop=True)
                if (self.find_largest(df1, lon, lat, r) < r):
                    df1 = df[df.h1 == h_goal[0]]
                    df1 = df1.reset_index(drop=True)
                    if (self.find_largest(df1, lon, lat, r) < r):
                        df1 = df.copy()
                        self.find_largest(df1, lon, lat, r)
                    else:
                        df1 = df1
                else:
                    df1 = df1
            else:
                df1 = df1
        else:
            df1 = df1
        df_r = df1[df1.distance < r]
        return df_r

    def cal(self, df, lon, lat, n, attr, query_str):
        df_res = self.r_cal(df, lon, lat, n)
        df_res = df_res.reset_index(drop='True')
        return df_res


class K(k_and_r):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(K, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def k_cal(self,df, lon, lat, k):
        dis = []
        for index in range(df.shape[0]):
            distance = self.haversine(df['lat'][index], df['lon'][index], lat, lon)
            dis.append(distance)
        df.insert(0, 'distance', dis)
        df_k = df.sort_values(by=['distance'], ascending=True).head(k)
        df_k = df_k.reset_index(drop=True)
        return df_k

    def topk(self, df, lon, lat, k):
        h_goal = encode(lat, lon, 4)
        df1 = df
        if df1[df1.h1 == h_goal[00000]].shape[0] > k:
            df1 = df1[df1.h1 == h_goal[0]]

            if df1[df1.h2 == h_goal[0:2]].shape[0] > k:
                df1 = df1[df1.h2 == h_goal[0:2]]
                if df1[df1.h3 == h_goal[0:3]].shape[0] > k:
                    df1 = df1[df1.h3 == h_goal[0:3]]
                    if df1[df1.h4 == h_goal[0:4]].shape[0] > k:
                        df1 = df1[df1.h4 == h_goal[0:4]]
        df1 = df1.reset_index(drop=True)

        df_res = self.k_cal(df1, lon, lat, k)
        return df_res

    def cal(self, df, lon, lat, n, attr, query_str):
        df_same = find_same(df, attr, query_str)
        df_res = self.topk(df_same, lon, lat, n)
        df_res = df_res.reset_index(drop='True')
        return df_res

    def topk_k_analysis(self, df, lon, lat):
        list_time = []
        for i in range(1, 50):
            k = 100 * i

            start = time.time()
            df_k = self.topk(df, lon, lat, k)
            end = time.time()

            df = df.reset_index(drop=True)
            list_time.append(end - start)
        k_analysis = DataFrame({
            'k': range(1, 50),
            'time': list_time
        })
        k_analysis.transpose()

        return k_analysis
