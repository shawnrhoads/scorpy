import pandas as pd, os, json

def reverse(this_val, min_val, max_val):
    return (max_val + min_val) - this_val

def score_surveys(data_file, scale_list, method='average', reverse_score=True):
    '''
    data_file: path to csv file or pandas dataframe
    scale_list: list of scales to score
    method: 'average' or 'sum'
    reverse_score: True if raw data are not already reversed scored, or False if they are
    '''

    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.realpath(__file__))

    # Load data dataframe
    if isinstance(data_file, pd.DataFrame):
        data = data_file.copy()
    elif isinstance(data_file, str):
        data = pd.read_csv(data_file)
        # data.columns = data.columns.str.lower()

    # Loop over scales
    for scale in scale_list:
        
        # Construct the key file paths using the keys directory and scale names
        key_file = os.path.join(current_dir, "keys", f"{scale}_key.json")
        key = pd.read_json(key_file)
        min_val = key.iloc[0]['min_val']
        max_val = key.iloc[0]['max_val']
        key = key.drop(columns=['min_val', 'max_val'])

        # Find columns in data that start with "scale_"
        scale_columns = []
        try:
            scale_columns = [col for col in data.columns if str(col).startswith(f"{scale}_")]
        except Exception as e:
            raise ValueError(f"Error with scale name: {scale}. Error message: {str(e)}")

        # reshape key if key and data do not match (possibly because extra columns in data)
        if key.shape[1] != data[scale_columns].shape[1]:
            Warning(f'key {key.shape} and data {data[scale_columns].shape} shapes do not match for {scale}')
            key = key.reindex(columns=data[scale_columns].columns, fill_value=0)
        
        # Iterate over sub-scale names and compute scores for each
        for sub_scale_name in key.index:
            sub_scale_items = key.loc[sub_scale_name]
            
            # Select relevant columns from data
            sub_scale_data = data[scale_columns].loc[:, sub_scale_items.astype(bool)]
            
            # Reverse scores for items marked as -1 
            if reverse_score:
                reverse_items = sub_scale_items[sub_scale_items == -1]
                sub_scale_data.loc[:, reverse_items.index] = sub_scale_data[reverse_items.index].applymap(lambda x: reverse(x, min_val, max_val))
            
            # Compute sub-scale score using specified method
            if method == "average":
                sub_scale_score = sub_scale_data.mean(axis=1)
            elif method == "sum":
                sub_scale_score = sub_scale_data.sum(axis=1)
            
            # Add sub-scale score as a new column in data
            data[sub_scale_name] = sub_scale_score
    
    return data

def create_key(key_dict, scale, min_val, max_val):
    ''' Example Dictionary
    key_dict = {"Honesty-Humility": ["6", "30R", "54", "12R", "36", "60R", "18", "42R", "24R", "48R"],
                "Sincerity": ["6", "30R", "54"],"Fairness": ["12R", "36", "60R"],"Greed-Avoidance": ["18", "42R"],"Modesty": ["24R", "48R"],
                "Emotionality": ["5", "29", "53R", "11", "35R", "17", "41R", "23", "47", "59R"],
                "Fearfulness": ["5", "29", "53R"],"Anxiety": ["11", "35R"],"Dependence": ["17", "41R"],"Sentimentality": ["23", "47", "59R"],
                "Extraversion": ["4", "28R", "52R", "10R", "34", "58", "16", "40", "22", "46R"],
                "Social Self-Esteem": ["4", "28R", "52R"],"Social Boldness": ["10R", "34", "58"],"Sociability": ["16", "40"],"Liveliness": ["22", "46R"],
                "Agreeableness": ["3", "27", "9R", "33", "51", "15R", "39", "57R", "21R", "45"],
                "Forgiveness": ["3", "27"],"Gentleness": ["9R", "33", "51"],"Flexibility": ["15R", "39", "57R"],"Patience": ["21R", "45"],
                "Conscientiousness": ["2", "26R", "8", "32R", "14R", "38", "50", "20R", "44R", "56R"],
                "Organization": ["2", "26R"],"Diligence": ["8", "32R"],"Perfectionism": ["14R", "38", "50"],"Prudence": ["20R", "44R", "56R"],
                "Openness to Experience": ["1R", "25", "7", "31R", "13", "37", "49R", "19R", "43", "55R"],
                "Aesthetic Appreciation": ["1R", "25"],"Inquisitiveness": ["7", "31R"],"Creativity": ["13", "37", "49R"],"Unconventionality": ["19R", "43", "55R"],
                "Altruism": ["97", "98", "99R", "100R"]}
    '''

    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.realpath(__file__))

    # create the empty df with numbered columns
    item_list = list(sorted({ele for val in key_dict.values() for ele in val}))
    df = pd.DataFrame(columns=[f'{scale}_'+i.replace("R", "") for i in item_list])

    # iterate over the key:value pairs in the data dictionary
    for key, value in key_dict.items():

        # create a new row with all values set to 0
        row = pd.Series(data=0, index=df.columns)
        row['subscale'] = key

        # set the values that are present in the row to -1 or 1 as appropriate
        for val in value:
            if "R" in str(val):
                row[f'{scale}_'+str(val).replace("R", "")] = -1
            else:
                row[f'{scale}_'+str(val)] = 1

        # add the row to the df
        df = df.append(row, ignore_index=True)

    df = df.set_index('subscale')
    df.to_csv(os.path.join(current_dir, "keys", f"{scale}_key.csv"))

    # save the resulting df
    df_dict = df.to_dict()
    df_dict['min_val'] = min_val
    df_dict['max_val'] = max_val

    with open(os.path.join(current_dir, "keys", f"{scale}_key.json"), 'w') as outfile:
        json.dump(df_dict, outfile)

    return df