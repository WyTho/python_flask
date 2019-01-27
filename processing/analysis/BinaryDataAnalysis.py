import pandas as pd
from sklearn.cluster import DBSCAN
from collections import Counter
from sklearn.preprocessing import LabelEncoder
from collections import defaultdict


def to_milliseconds(seconds):
    return seconds * 60 * 1000


class BinaryDataAnalysis:
    """Convert non-nummeric values in the dataframe to numbers so that the dataframe can be used to fit a model

    Args (all optional):
        eps: The epsilon in minutes (starting minimum distance between datapoints to cluster them together)
        cluster_degregation: The next epsilon divider to use if clusters are too large
                             (if eps=5 and cluster_degregation=2 then the next eps will be 2.5, and the next 1.25 etc.)
        max_cluster_distance: the maximum size of a cluster in minutes
        weeks: the amount of weeks to analyze,
               a minimum of 1 needed,
               a minimum of 2 is recommended
        decay_strength: how much the next week counts for predicting relevant groups
                        e.g. with a decay_strength of 0.5, ech week before last week will
                             count half as strong for predicting if the groups are still relevant
        cluster_threshold: from how many occourences (in one week) should it get 'self.threshold_percentage'
                           as percentage that it is a group...
                           More occourences will result in a higher persentage than 'self.threshold_percentage'
                           Less occourences will result in a lower persentage
        threshold_percentage: the persentage to give a group if the amount of occourences is 'self.cluster_threshold'
    """

    def __init__(self,
                 eps=5,
                 cluster_degregation=2,
                 max_cluster_distance=7.5,
                 weeks=5,
                 decay_strength=0.5,
                 cluster_threshold=7,
                 threshold_percentage=90):
        self.eps = eps
        self.cluster_degregation = cluster_degregation
        self.max_cluster_distance = max_cluster_distance
        self.weeks = weeks
        self.decay_strength = decay_strength
        self.cluster_threshold = cluster_threshold
        self.threshold_percentage = threshold_percentage

    def analyze(self, df):
        """Analyze a dataframe and return a list of predicted groups & relevant groups

        Args:
            df: the dataframe to analyze

        Returns:
            result: an array of predicted groups in the following format:
                [
                    {
                        item_ids: a list of item-id's that are predicted to be a group,
                        is_predicted_group_percentage: the percentage chance that this is a group,
                        is_relevant_group_percentage: the percentage chance that this group is still relevant
                                                      (depending on how much it has been used lately)
                    },
                    {...},
                    {...}
                ]
        """
        self.lookup_table = self.create_lookup_table(
            df=df
        )
        print(self.lookup_table)
        df_fit = self.clean_dataframe(
            df=df
        )
        week_hashcodes = self.get_week_clusters_hash_codes(
            df=df_fit
        )
        hashcode_occurances = self.get_hashcode_occurances_per_week(
            week_hashcodes=week_hashcodes
        )
        predicted_groups = self.calculate_groups(
            hashcode_occurances_per_week=hashcode_occurances
        )

        result = []
        # print(predicted_groups)
        for key in predicted_groups:
            items = self.get_lookup_values(
                hashcode=key
            )
            result.append({
                'item_ids': [int(item) for item in items],
                'is_predicted_group_percentage': predicted_groups[key]['is_predicted_group_percentage'],
                'is_relevant_group_percentage': predicted_groups[key]['is_relevant_group_percentage']
            })

        return result

    def create_lookup_table(self, df):
        """Creates a lookup table for all unique row-id's

        Args:
            df: the dataframe containing an id column with several diffrent devices creating events

        Returns:
            lookup_dict: a dictionary where each id corresponds to an index e.g.
                         { 0: 1743, 1: 1749, 2: 1803, 3: 1890, 4: 1911}
        """
        df_lookup = pd.DataFrame(data={'id': pd.Series(df['id']).unique()})
        print(df_lookup)
        df_lookup['hashcode'] = self.clean_dataframe(
            df=df_lookup.copy()
        )['id']
        print(df_lookup)
        lookup_dict = dict()
        for index, row in df_lookup.iterrows():
            lookup_dict[row['hashcode']] = row['id']
        return lookup_dict

    def clean_dataframe(self, df):
        """Convert all the id's to numbers ranging from 0 to the amount of unique id's
            e.g. with events for items with id's 33, 35, 37 & 45 the id's will be 0, 1, 2, 3

        Args:
            df: The dataframe to clean.

        Returns:
            df_fit: The dataframe with ascending id's from 0 to the amount of unique ones
        """
        df_ids_only = pd.DataFrame()
        df_ids_only['id'] = df['id']
        d = defaultdict(LabelEncoder)
        df_ids_only = df_ids_only.apply(lambda x: d[x.name].fit_transform(x))
        df_fit = df
        df_fit['id'] = df_ids_only['id']
        return df_fit

    def get_week_clusters_hash_codes(self, df):
        """Get Cluster for a dataframe per week

        Args:
            df: The dataframe with more than one week of timestamps to cluster.

        Returns:
            week_hashcodes: A multidimentional array where each array is one week, and in one week array
                            are a list of clusters represented by a hashcode.

                            A hashcode is the reversed binary representation of a cluster,
                            e.g.
                            hashcode 3
                            is binary 00000011
                            is reversed 11000000
                            means devices with index 0 and 1 (from the lookup table) are grouped

                            Example output:
                                [[3, 5, 20], [3, 3, 20]]
                            means:
                                amount of weeks: 2
                                clusters in week 1:
                                    3  (00000011) = a group with device 0 & 1
                                    5  (00000101) = a group with device 0 & 2
                                    20 (00010100) = a group with device 2 & 4
                                clusters in week 2:
                                    3  (00000011) = a group with device 0 & 1
                                    3  (00000011) = another group with device 0 & 1
                                    21 (00010101) = a group with device 0, 2 & 4
        """
        one_week_in_milliseconds = (1000 * 60 * 60 * 24 * 7)
        last_timestamp = df['time'].max()
        week_hashcodes = []
        for week in range(self.weeks):
            week_hashcodes.append([])
            df_week = df[df['time'] >= last_timestamp - ((week + 1) * one_week_in_milliseconds)]
            df_week = df_week[df_week['time'] < last_timestamp - (week * one_week_in_milliseconds)]

            if not df_week.empty:
                cluster_arr = self.split_dataframe_on_state_and_get_cluster_arr(
                    df=df_week,
                    starting_eps=self.eps
                )
                for idx, df_week in enumerate(cluster_arr):
                    cluster = []
                    for row in df_week.iterrows():
                        index, data = row
                        cluster.append(data['id'].tolist())

                    cluster = list(set(cluster))

                    hashcode = 0
                    for lamp in cluster:
                        hashcode += pow(2, lamp)

                    if len(cluster) > 1:
                        week_hashcodes[week].append(hashcode)
            else:
                print(
                    'WARNING!!! There are not',
                    self.weeks,
                    'weeks in the dataset... amount_of_weeks HAS BEEN CHANGED TO',
                    week
                )
                self.weeks = week
                break
        return week_hashcodes

    def split_dataframe_on_state_and_get_cluster_arr(self, df, starting_eps):
        """Split a dataframe into 2 seperate dataframes (one with state=0, the other with state=1)
           and get the clusters for both of the dataframes

        Args:
            df: The dataframe to split & get clusters from.

        Returns:
            cluster_arr: an array that holds 0 or more dataframes (clusters)
        """
        df_1 = df.loc[df['state'] == 1]
        df_0 = df.loc[df['state'] == 0]
        cluster_arr1 = self.get_clusters_recursive(df=df_1.copy(), eps=starting_eps)
        cluster_arr2 = self.get_clusters_recursive(df=df_0.copy(), eps=starting_eps)
        cluster_arr = cluster_arr1 + cluster_arr2
        return cluster_arr

    def get_clusters_recursive(self, df, eps, iteration=0, cluster_arr=None):
        """Get clusters for a single dataframe

        Args:
            df: The dataframe
            eps: the epsilon to start with (maximum distance between two datapoints)

        Returns:
            cluster_arr: An array of dataframes (each one represents a cluster)e.g.
                         [DataFrame, DataFrame, DataFrame, ...]
        """
        if cluster_arr is None:
            cluster_arr = []

        model = self.fit_model(df, eps)
        cluster_dict = self.get_clusters(df=df, model=model)

        for idx, df in cluster_dict['too_large'].items():
            cluster_arr + self.get_clusters_recursive(
                df=cluster_dict['too_large'][idx],
                eps=eps / self.cluster_degregation,
                iteration=iteration + 1,
                cluster_arr=cluster_arr
            )

        for idx, df in cluster_dict['perfect_size'].items():
            cluster_arr.append(df)
        return cluster_arr

    def fit_model(self, df, eps):
        """Fit the dataframe in the DBSCAN algoritm and return the model

           more information: https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html

        Args:
            df: The dataframe to run the algorithm on
            eps: the epsilon (maximum distance between two datapoints)

        Returns:
            model: The fitted DBSCAN model
        """
        model = DBSCAN(
            eps=to_milliseconds(eps),
            min_samples=2
        ).fit(df)
        return model

    def get_clusters(self, df, model):
        """Get clusters for a single dataframe

        Args:
            df: The dataframe
            model: the fitted model

        Returns:
            dict: A dictionary with 2 keys, each of wich is another dictionary which contains all dataframes (one per cluster)
            e.g.
            {
                'too_large': {
                    0: DataFrame,
                    1: DataFrame,
                    2: DataFrame
                },
                'perfect_size': {
                    0: DataFrame,
                    1: DataFrame
                }
            }
        """
        df['cluster'] = model.labels_

        cluster_dict_too_large = {}
        cluster_dict_perfect_size = {}

        # Calculate amount of clusters
        cluster_data_count = Counter(model.labels_)
        if -1 in cluster_data_count:
            cluster_data_count.pop(-1)  # don't count outliers as a cluster
        if bool(cluster_data_count):
            amount_of_clusters = max(cluster_data_count) + 1
        else:
            amount_of_clusters = 0

        for idx in range(amount_of_clusters):
            cluster_df = df.loc[df['cluster'] == idx].drop(columns=['cluster'])

            first_time = cluster_df['time'].iloc[0]
            last_time = cluster_df['time'].iloc[cluster_df['time'].size - 1]
            difference_in_milliseconds = last_time - first_time
            if difference_in_milliseconds > to_milliseconds(self.max_cluster_distance):
                cluster_dict_too_large[idx] = cluster_df
            else:
                cluster_dict_perfect_size[idx] = cluster_df

        return {
            'too_large': cluster_dict_too_large,
            'perfect_size': cluster_dict_perfect_size
        }

    def get_hashcode_occurances_per_week(self, week_hashcodes):
        """Count all occourences of hashcodes per week

         Args:
             week_hashcodes: The week_hashcodes (generated from self.get_week_clusters_hash_codes())

         Returns:
             count_dict: A dictionary with an index for each hashcode, with all
                         occourences per week (last week = 0, the week before that = 1).
             e.g.
             {
                 '3': {
                     'occurance_week': {
                         '0': 24,
                         '1': 56,
                         '2': 32,
                         '3': 12
                     }
                 },
                 '5': { 'occurance_week': { ... } },
                 '20': { 'occurance_week': { ... } },
                 ...
             }
        """
        count_dict = {}
        for week, hashcodes_arr in enumerate(week_hashcodes):
            for i in hashcodes_arr:
                if i in count_dict:
                    count_dict[i]['occurance_week'][str(week)] += 1
                else:
                    count_dict[i] = {}
                    count_dict[i]['occurance_week'] = {}
                    for w in range(self.weeks):
                        count_dict[i]['occurance_week'][str(w)] = 0
        return count_dict

    def calculate_groups(self, hashcode_occurances_per_week):
        """Calculate the predicted groups & relevant groups persentages from the amount of occourences.

         Args:
             hashcode_occurances_per_week: The hashcode occurances per week
                                           (generated from self.get_hashcode_occurances_per_week())

         Returns:
             count_dict: A dictionary with an index for each hashcode and the predicted groups & relevant groups persentages
             e.g.
             {
                 '3': {
                     'is_predicted_group_percentage': 92.3,
                     'is_relevant_group_percentage': 72.1,
                 },
                 '5': {
                     'is_predicted_group_percentage': 42.9,
                     'is_relevant_group_percentage': 51.8,
                 },
                 '20': { ... },
                 ...
             }
        """
        count_dict = hashcode_occurances_per_week
        for key, val in count_dict.items():
            threshold = self.cluster_threshold * self.weeks

            total_occurances = 0
            for week in range(self.weeks):
                total_occurances += val['occurance_week'][str(week)]

            if total_occurances >= threshold:
                div = (total_occurances / threshold)
                count = 1
                perc = self.threshold_percentage

                while div > 1:
                    div /= 2
                    perc += ((100 - self.threshold_percentage) / 2) * (1 / count)
                    count *= 2

            else:
                perc = (total_occurances / threshold) * self.threshold_percentage

            count_dict[key]['is_predicted_group_percentage'] = round(perc, 2)

        for key, val in count_dict.items():
            total = 0
            current = 0
            for week in range(self.weeks):

                perc = 0
                if val['occurance_week'][str(week)] >= self.cluster_threshold:
                    div = (val['occurance_week'][str(week)] / self.cluster_threshold)
                    count = 1
                    perc = self.threshold_percentage
                    while div > 1:
                        div /= 2
                        perc += ((100 - self.threshold_percentage) / 2) * (1 / count)
                        count *= 2
                else:
                    perc = (val['occurance_week'][str(week)] / self.cluster_threshold) * self.threshold_percentage

                total += 100 * (0.5) / pow(2, week * self.decay_strength)
                current += perc * (0.5) / pow(2, week * self.decay_strength)

            count_dict[key]['is_relevant_group_percentage'] = round((current / total) * 100, 2)
            count_dict[key].pop('occurance_week', None)
        return count_dict

    def get_lookup_values(self, hashcode):
        """Get the individual item-indexes for a given hashcode

        Args:
            hashcode: The dataframe hashcode
                      e.g. 21

        Returns:
            items: An array of items
                   e.g. [0, 2, 4]

        e.g.
            hashcode 21
            = 00010101 in binary
            = 10101000 reversed
            =   item 0 = true,
                item 1 = false
                item 2 = true
                item 3 = false
                item 4 = true
                item 5 = false
                item 6 = false
                item 7 = false
            = a group with device 0, 2 & 4
        """

        def bitfield(n):
            return [int(digit) for digit in bin(n)[2:]]

        bits = bitfield(hashcode)[::-1]

        items = []
        for idx, bit in enumerate(bits):
            if bit == 1:
                items.append(self.lookup_table[idx])
        return items
