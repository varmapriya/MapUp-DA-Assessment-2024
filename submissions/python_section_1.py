from typing import Dict, List
import pandas as pd
import re
import polyline
import numpy as np

def reverse_by_n_elements(lst: List[int], n: int) -> List[int]:
    result = []
    length = len(lst)

    for i in range(0, length, n):
        group = []
        for j in range(i, min(i + n, length)):
            group.append(lst[j])

        reversed_group = []
        for k in range(len(group) - 1, -1, -1):
            reversed_group.append(group[k])
        
        result.extend(reversed_group)

    return result

def group_by_length(lst: List[str]) -> Dict[int, List[str]]:
    length_dict = {}
    
    for string in lst:
        length = len(string)
        if length not in length_dict:
            length_dict[length] = []
        length_dict[length].append(string)
    
    sorted_dict = dict(sorted(length_dict.items()))
    
    return sorted_dict

def flatten_dict(nested_dict: Dict, sep: str = '.') -> Dict:
    items = {}
    
    for key, value in nested_dict.items():
        new_key = f"{key}" if not sep else f"{sep}{key}"
        
        if isinstance(value, dict):
            items.update(flatten_dict(value, new_key, sep=sep))
        elif isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    items.update(flatten_dict(item, f"{new_key}[{i}]", sep=sep))
                else:
                    items[f"{new_key}[{i}]"] = item
        else:
            items[new_key] = value
            
    return items

def unique_permutations(nums: List[int]) -> List[List[int]]:
    def backtrack(start):
        if start == len(nums):
            result.append(nums[:])
            return
        
        seen = set()
        for i in range(start, len(nums)):
            if nums[i] not in seen:
                seen.add(nums[i])
                nums[start], nums[i] = nums[i], nums[start]
                backtrack(start + 1)
                nums[start], nums[i] = nums[i], nums[start]

    nums.sort()
    result = []
    backtrack(0)
    return result

def find_all_dates(text: str) -> List[str]:
    date_patterns = [
        r'\b\d{2}-\d{2}-\d{4}\b',
        r'\b\d{2}/\d{2}/\d{4}\b',
        r'\b\d{4}\.\d{2}\.\d{2}\b'
    ]
    
    all_dates = []
    
    for pattern in date_patterns:
        matches = re.findall(pattern, text)
        all_dates.extend(matches)
    
    return all_dates

def polyline_to_dataframe(polyline_str: str) -> pd.DataFrame:
    coordinates = polyline.decode(polyline_str)
    
    data = {
        'latitude': [],
        'longitude': [],
        'distance': []
    }
    
    previous_lat = previous_lon = 0
    for lat, lon in coordinates:
        data['latitude'].append(lat)
        data['longitude'].append(lon)
        
        if data['distance']:
            distance = haversine(previous_lat, previous_lon, lat, lon)
        else:
            distance = 0
        
        data['distance'].append(distance)
        
        previous_lat, previous_lon = lat, lon
    
    df = pd.DataFrame(data)
    return df

def rotate_and_multiply_matrix(matrix: List[List[int]]) -> List[List[int]]:
    n = len(matrix)
    rotated = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            rotated[j][n - 1 - i] = matrix[i][j]
    
    transformed = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            row_sum = sum(matrix[i])
            col_sum = sum(matrix[k][j] for k in range(n))
            transformed[i][j] = row_sum + col_sum - matrix[i][j]
    
    return transformed

def time_check(df: pd.DataFrame) -> pd.Series:
    df['start'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    df['end'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])
    
    grouped = df.groupby(['id', 'id_2'])

    def is_complete(group):
        all_days = pd.date_range(start=group['start'].min().normalize(), 
                                  end=group['end'].max().normalize(), 
                                  freq='D')
        
        for day in all_days:
            day_records = group[(group['start'].dt.normalize() == day) | 
                                (group['end'].dt.normalize() == day)]
            if day_records.empty:
                return False
            
            if not (day_records['start'].min() <= day + pd.Timedelta(hours=0) and
                    day_records['end'].max() >= day + pd.Timedelta(hours=23, minutes=59, seconds=59)):
                return False
                
        return True

    completeness_results = grouped.apply(is_complete)
    return completeness_results
