import sys
data = {'selectedOptions': {'0': 1, '1': 3}, 'feedback1': {'0': 'helpful', '1': 'helpful'}, 'feedback2': {'0': 'not_Ambiguous', '1': 'Ambiguous'}, 'feedback3': {'0': 'not_easy_to_eliminate', '1': 'easy_to_eliminate'}, 'feedback4': {'0': 'not_lenghty', '1': 'lenghty'}} 

def debug():
    for key,value in data['feedback1'].items():
        # values = [[data['feedback1'][key],data['feedback2'][key],data['feedback3'][key],data['feedback4'][key]]]
        print(data['feedback2'][key])
        print(key)
    
    
    
if __name__ == '__main__':
    debug()