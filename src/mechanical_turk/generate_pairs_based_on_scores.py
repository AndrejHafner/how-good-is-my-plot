import pandas as pd
import os
from shutil import copyfile
import random

def generate_pairs_by_scores(seed, list, csv_filename):
    '''
    This script generates plot pairs, that are based on scores that plots have obtained so far.
    Writes csv file with generated pairs.
    :param seed: random seed
    :param list: list of plots with scores
    :param csv_filename: name of the csv file where pairs will be written
    '''
    random.seed(seed)
    max_score = max(list, key=lambda x: x[1])[1]
    lists = [[] for i in range(max_score + 1)]
    for plot in list:
        lists[plot[1]].append(plot)

    for plots in lists:
        random.shuffle(plots)

    done = False
    while not done:
        list_of_plots = []
        for plots in lists:
            list_of_plots += plots
        pairs = []
        try:
            for i in range(0, len(list_of_plots) - 1, 2):
                pair = (list_of_plots[i][0], list_of_plots[i + 1][0], list_of_plots[i][1], list_of_plots[i + 1][1])
                if check_if_pair_existed((pair[0],pair[1])):
                    print('PAIR EXISTED')
                    for index, group in enumerate(lists):
                        for el in group:
                            if el[0] == pair[0]:
                                j = index
                                random.shuffle(lists[j])
                                raise Exception
                else:
                    print('-----')
                    pairs.append(pair)
            done = True
        except:
            pass
    random.shuffle(pairs)

    df = pd.DataFrame(columns=['first', 'second', 'score1', 'score2'])
    for i in pairs:
        df = df.append({'first': i[0], 'second': i[1], 'score1': i[2], 'score2': i[3]}, ignore_index=True)

    df.to_csv(f'{csv_filename}.csv', index=False)

def sample_pictures(dir,n, new_dir, seed):
    '''
    Samples n instances from dir
    :param dir: dir path
    :param n: int, sample size
    '''
    random.seed(seed)
    files = [f for f in os.listdir(dir) if f.lower().endswith(('.jpg', '.jpeg'))]
    sample = random.sample(files, n)
    for file in sample:
        copyfile(dir + '/' + file, new_dir + '/' + file)

def make_initial_scores(dir):
    '''
    For every plot in directory, creates initial 0 points
    :param dir: directory where plots are
    :return: list of scores for every plot
    '''
    list_scores = []
    for plot in os.listdir(dir):
        list_scores.append((plot,0))
    return list_scores

def get_scores(dir, csv_name):
    '''
    Gets scores of the results saved in csv
    :param dir: directory of where the plots are
    :param csv_name: csv name of the csv file of the results of a batch
    '''
    names = {}
    for file in os.listdir(dir):
        names[file] = 0
    data = pd.read_csv(csv_name)
    for winner in data['selected']:
        names[winner] += 1
    list_of_all = []
    for plot in list(names.keys()):
        list_of_all.append((plot, names[plot]))
    return list_of_all

def get_results(csv_name):
    '''
    Gets results
    :param csv_name: csv name of batch results
    :return: dataframe with 3 columns, first two represents plots that were compared and the third is 0 if first won, otherwise 1
    '''
    df = pd.DataFrame(columns=['name1', 'name2', 'win'])
    data = pd.read_csv(csv_name)
    for index, row in data.iterrows():
        selected = int(row['second_plot'] == row['selected'])
        df = df.append({'name1': row['first_plot'], 'name2': row['second_plot'], 'win' : selected}, ignore_index=True)

    return df


def sum_scores(dir, list_of_scores):
    '''
    Sums together the points for every plot
    :param dir: directory path to all the plots
    :param list_of_scores: list of list of scores for every plot
    :return: List of all plots with scores
    '''
    names = {}
    for file in os.listdir(dir):
        names[file] = 0
    for list_ in list_of_scores:
        for plot in list_:
            names[plot[0]]+=plot[1]
    list_of_all = []
    for plot in list(names.keys()):
        list_of_all.append((plot, names[plot]))
    return list_of_all

def check_if_pair_existed(pair):
    '''
    Checks if pair was already made in previous batches.
    :param pair: pair of plots, (plot1, plot2)
    :return: True if existed before, otherwise False
    '''
    df1 = pd.read_csv('batch_1/first_batch.csv')
    df2 = pd.read_csv('batch_2/second_batch.csv')
    df3 = pd.read_csv('batch_3/third_batch.csv')
    df4 = pd.read_csv('batch_4/batch_4.csv')
    df5 = pd.read_csv('batch_5/batch_5.csv')
    df6 = pd.read_csv('batch_6/batch_6.csv')
    df7 = pd.read_csv('batch_7/batch_7.csv')
    df8 = pd.read_csv('batch_8/batch_8.csv')
    for df in [df1,df2, df3, df4, df5, df6, df7, df8]:
        for index, row in df.iterrows():
            if (row['first'] in pair) and (row['second'] in pair):
                return True
    return False


if __name__ == '__main__':

    dir = 'C:/Users/Acer/Desktop/Data science/1 letnik/Project/data/filtered_images/line_plot/sampled'
    new_dir = 'C:/Users/Acer/Desktop/Data science/1 letnik/Project/data/filtered_images/line_plot/sampled/final'

    #sample_pictures(dir, 500, new_dir, 0)
    #l = make_initial_scores(new_dir)
    #generate_pairs_by_scores(0,l,'first_batch')

    plots_list = get_scores(new_dir, 'batch_1/swiss_sys_run_1_parsed.csv')
    #generate_pairs_by_scores(4,plots_list, 'second_batch')


    plots_list2 = get_scores(new_dir, 'batch_2/swiss_sys_run_2_parsed.csv')
    #current_scores = sum_scores(new_dir, [plots_list, plots_list2])
    #generate_pairs_by_scores(3**2,current_scores, 'third_batch')

    plots_list3 = get_scores(new_dir, 'batch_3/swiss_sys_run_3_parsed.csv')
    #current_scores = sum_scores(new_dir, [plots_list, plots_list2, plots_list3])
    #generate_pairs_by_scores(4**2,current_scores, 'batch_4')

    plots_list4 = get_scores(new_dir, 'batch_4/swiss_sys_run_4_parsed.csv')
    #current_scores = sum_scores(new_dir, [plots_list, plots_list2, plots_list3, plots_list4])
    #generate_pairs_by_scores(5**2,current_scores, 'batch_5')

    plots_list5 = get_scores(new_dir, 'batch_5/swiss_sys_run_5_parsed.csv')
    #current_scores = sum_scores(new_dir, [plots_list, plots_list2, plots_list3, plots_list4, plots_list5])
    #generate_pairs_by_scores(6**2,current_scores, 'batch_6')

    plots_list6 = get_scores(new_dir, 'batch_6/swiss_sys_run_6_parsed.csv')
    #current_scores = sum_scores(new_dir, [plots_list, plots_list2, plots_list3, plots_list4, plots_list5, plots_list6])
    #generate_pairs_by_scores(7**2,current_scores, 'batch_7')

    plots_list7 = get_scores(new_dir, 'batch_7/swiss_sys_run_7_parsed.csv')
    #current_scores = sum_scores(new_dir, [plots_list, plots_list2, plots_list3, plots_list4, plots_list5, plots_list6, plots_list7])
    #generate_pairs_by_scores(8**2,current_scores, 'batch_8')

    plots_list8 = get_scores(new_dir, 'batch_8/swiss_sys_run_8_parsed.csv')
    #current_scores = sum_scores(new_dir, [plots_list, plots_list2, plots_list3, plots_list4, plots_list5, plots_list6, plots_list7, plots_list8])
    #generate_pairs_by_scores(9**2,current_scores, 'batch_9')

    plots_list9 = get_scores(new_dir, 'batch_9/swiss_sys_run_9_parsed.csv')
    current_scores = sum_scores(new_dir, [plots_list, plots_list2, plots_list3, plots_list4, plots_list5, plots_list6, plots_list7, plots_list8, plots_list9])
    # generate_pairs_by_scores(9**2,current_scores, 'batch_9')


    # creates csv file with all comparisons
    df = pd.DataFrame(columns=['name1', 'name2', 'win'])
    results = ['batch_1/swiss_sys_run_1_parsed.csv', 'batch_2/swiss_sys_run_2_parsed.csv', 'batch_3/swiss_sys_run_3_parsed.csv', 'batch_4/swiss_sys_run_4_parsed.csv', 'batch_5/swiss_sys_run_5_parsed.csv', 'batch_6/swiss_sys_run_6_parsed.csv', 'batch_7/swiss_sys_run_7_parsed.csv', 'batch_8/swiss_sys_run_8_parsed.csv', 'batch_9/swiss_sys_run_9_parsed.csv']
    for res in results:
        d = get_results(res)
        df =  pd.concat([df, d], ignore_index=True)
    df.to_csv(f'all_matches.csv', index=False)



    # writes csv file of final scores of all plots
    df = pd.DataFrame(columns=['plot_name', 'score'])
    for i in current_scores:
        df = df.append({'plot_name': i[0], 'score': i[1]}, ignore_index=True)

    df.to_csv(f'final_scores.csv', index=False)



    # if you want to double-check if some pairs are repeated
    '''
    df = pd.read_csv('batch_9.csv')
    for index, row in df.iterrows():
        t = check_if_pair_existed((row['first'], row['second']))
        if t:
            print('######')
        else:
            print('------')'''