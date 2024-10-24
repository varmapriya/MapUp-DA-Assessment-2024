import pandas as pd


def calculate_distance_matrix(df) -> pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    distance_matrix = pd.DataFrame()  
    return distance_matrix


def unroll_distance_matrix(df) -> pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    unrolled_df = pd.DataFrame(columns=['id_start', 'id_end', 'distance'])
    for id_start in df.index:
        for id_end in df.columns:
            if id_start != id_end:
                distance = df.loc[id_start, id_end]
                unrolled_df = unrolled_df.append({'id_start': id_start, 'id_end': id_end, 'distance': distance}, ignore_index=True)
    return unrolled_df


def find_ids_within_ten_percentage_threshold(df, reference_id) -> pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    avg_distance_ref = df[df['id_start'] == reference_id]['distance'].mean()
    lower_bound = avg_distance_ref * 0.9
    upper_bound = avg_distance_ref * 1.1
    filtered_ids = df[(df['id_start'] != reference_id) & 
                      (df['distance'] >= lower_bound) & 
                      (df['distance'] <= upper_bound)]['id_start'].unique()
    return pd.DataFrame({'id_start': filtered_ids})


def calculate_toll_rate(df) -> pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    toll_rates = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }
    for vehicle, rate in toll_rates.items():
        df[vehicle] = df['distance'] * rate
    return df


def calculate_time_based_toll_rates(df) -> pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    weekends = ['Saturday', 'Sunday']
    
    time_ranges = [
        (datetime.time(0, 0), datetime.time(10, 0), 0.8),
        (datetime.time(10, 0), datetime.time(18, 0), 1.2),
        (datetime.time(18, 0), datetime.time(23, 59, 59), 0.8)
    ]
    
    result_df = pd.DataFrame()
    
    for index, row in df.iterrows():
        for day in weekdays + weekends:
            for start_time, end_time, factor in time_ranges:
                if day in weekdays:
                    new_row = row.copy()
                    new_row['start_day'] = day
                    new_row['start_time'] = start_time
                    new_row['end_day'] = day
                    new_row['end_time'] = end_time
                    
                    new_row['moto'] *= factor
                    new_row['car'] *= factor
                    new_row['rv'] *= factor
                    new_row['bus'] *= factor
                    new_row['truck'] *= factor
                    
                    result_df = result_df.append(new_row, ignore_index=True)
                else:
                    new_row = row.copy()
                    new_row['start_day'] = day
                    new_row['start_time'] = datetime.time(0, 0)
                    new_row['end_day'] = day
                    new_row['end_time'] = datetime.time(23, 59, 59)

                    discount_factor = 0.7
                    new_row['moto'] *= discount_factor
                    new_row['car'] *= discount_factor
                    new_row['rv'] *= discount_factor
                    new_row['bus'] *= discount_factor
                    new_row['truck'] *= discount_factor
                    
                    result_df = result_df.append(new_row, ignore_index=True)

    return result_df
