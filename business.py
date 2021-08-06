import pandas as pd 

def get_data():
    
    df = pd.read_csv('result.csv')

    #print(df['states'].tolist())

    Vote             = df['Vote'].tolist()

    Result         = df['Result'].tolist()

    list_of_tuples = [tuple(row) for row in df.values]
  
    print(list_of_tuples)

    result_dict = {
        'Vote '                : Vote ,
        'Result'               : Result,
        'data_list'             : list_of_tuples
    }

    #print(result_dict)

    return result_dict


def add_row(Vote, Result):

    df = pd.read_csv('result.csv') 

    new_row = {
    
        'Vote'            : Vote, 
        'Result'        : Result
    }

    print(df)

    df = df.append(new_row, ignore_index=True)

    print(df)

    df.to_csv('result.csv')

if __name__ == "__main__":
     get_data()
