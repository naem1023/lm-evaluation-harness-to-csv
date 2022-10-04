import argparse, os, json
from itertools import product
import pandas as pd

metrics = ['kobest']

def get_candidates(args):
    """
    Return all possible combinations of evaluation file.
    """
    global metrics

    temp = list(product(args.few_shot, metrics))
    cand = ['-'.join([args.model, args.step, *t]) + '.json' for t in temp]

    return cand

            
def parse_evaluations(args):
    """
    Parse evaluation json file to csv file.
    """
    cand = get_candidates(args)
    json_d = {}
    for (path, dirs, files) in os.walk(args.base):
        for f in files:
            if f in cand:
                with open(os.path.join(path, f), 'r') as file:
                    json_d[f[:-5]] = json.load(file)

    csv_d = {}
    for path in json_d:
        temp = {}
        for metric in json_d[path]['results'].keys():
            temp[metric] = json_d[path]['results'][metric]['macro_f1']
        csv_d[path] = temp

    print(csv_d)

    dfs = []
    for path in csv_d:
        few_shot = path.split('-')[-2]
        df = pd.json_normalize(csv_d[path]).T
        dfs.append(df.rename(columns={0: f'{few_shot}-shot'}))
    
    temp = path.split('-')
    temp = temp[:4] + [temp[-1]]

    print(temp)

    concat_df = pd.concat(dfs, axis=1)

    concat_df = concat_df.rename(index=lambda x: x.split('_')[-1]).round(4).reset_index(level=0)
    
    concat_df = concat_df.rename(columns={'index': 'Task'})

    concat_df.to_csv('-'.join(temp) + '.csv', index=False)
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CSV convertor for evaluation json files')

    parser.add_argument('--base', type=str, default='./')
    parser.add_argument('--output', type=str, default='./')
    parser.add_argument('--model', type=str, required=True)
    parser.add_argument('--step',type=str, required=True)
    parser.add_argument('-f','--few_shot', nargs='+', help='a nubmer of few shot', default=['0', '1', '5', '10', '50', '100'])

    args = parser.parse_args()
    print(args)

    parse_evaluations(args)