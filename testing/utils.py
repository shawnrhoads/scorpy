import pandas as pd, os

def create_key(key_dict, scale):
    ''' Example Dictionary
    key_dict = {"Honesty-Humility": [6, "30R", 54, "12R", 36, "60R", 18, "42R", "24R", "48R"],
                "Sincerity": [6, "30R", 54], "Fairness": ["12R", 36, "60R"], "Greed-Avoidance": [18, "42R"], "Modesty": ["24R", "48R"],
                "Emotionality": [5, 29, "53R", 11, "35R", 17, "41R", 23, 47, "59R"], 
                "Fearfulness": [5, 29, "53R"], "Anxiety": [11, "35R"], "Dependence": [17, "41R"], "Sentimentality": [23, 47, "59R"],
                "Extraversion": [4, "28R", "52R", "10R", 34, 58, 16, 40, 22, "46R"],
                "Social Self-Esteem": [4, "28R", "52R"], "Social Boldness": ["10R", 34, 58], "Sociability": [16, 40], "Liveliness": [22, "46R"],
                "Agreeableness": [3, 27, "9R", 33, 51, "15R", 39, "57R", "21R", 45],    
                "Forgiveness": [3, 27], "Gentleness": ["9R", 33, 51],"Flexibility": ["15R", 39, "57R"], "Patience": ["21R", 45], 
                "Conscientiousness": [2, "26R", 8, "32R", "14R", 38, 50, "20R", "44R", "56R"],
                "Organization": [2, "26R"], "Diligence": [8, "32R"], "Perfectionism": ["14R", 38, 50],"Prudence": ["20R", "44R", "56R"], 
                "Openness to Experience": ["1R", 25, 7, "31R", 13, 37, "49R", "19R", 43, "55R"],
                "Aesthetic Appreciation": ["1R", 25], "Inquisitiveness": [7, "31R"], "Creativity": [13, 37, "49R"],"Unconventionality": ["19R", 43, "55R"]}
    '''

    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.realpath(__file__))

    # create the empty df with columns 1-60
    df = pd.DataFrame(columns=[f'{scale}_'+str(i) for i in range(1, 61)])

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

    # save the resulting df
    df.to_csv(os.path.join(current_dir, "keys", f"{scale}_key.csv"))

    return df

def reverse(value, min, max):
    return (max + min) - value

def score_surveys(data_file, scales, min, max, method):

    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.realpath(__file__))

    # Load data dataframe
    data = pd.read_csv(data_file)

    # Loop over scales
    for scale in scales:
        
        # Construct the key file paths using the keys directory and scale names
        key_file = os.path.join(current_dir, "keys", f"{scale}_key.csv")
        key = pd.read_csv(key_file, index_col=0)

        # Find columns in data that start with "scale_"
        scale_columns = [col for col in data.columns if col.startswith(f"{scale}_")]
        
        # Iterate over sub-scale names and compute scores for each
        for sub_scale_name in key.index:
            sub_scale_items = key.loc[sub_scale_name]
            
            # Select relevant columns from data
            sub_scale_data = data[scale_columns].loc[:, sub_scale_items.astype(bool)]
            
            # Reverse scores for items marked as -1
            reverse_items = sub_scale_items[sub_scale_items == -1]
            sub_scale_data.loc[:, reverse_items.index] = sub_scale_data[reverse_items.index].applymap(lambda x: reverse(x, min, max))
            
            # Compute sub-scale score using specified method
            if method == "average":
                sub_scale_score = sub_scale_data.mean(axis=1)
            elif method == "sum":
                sub_scale_score = sub_scale_data.sum(axis=1)
            
            # Add sub-scale score as a new column in data
            data[sub_scale_name] = sub_scale_score
    
    return data