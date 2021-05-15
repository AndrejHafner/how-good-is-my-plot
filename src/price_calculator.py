from generate_plot_pairs import generate_plot_pairs


def calculate_final_price(worker_price, master_worker_price, amazon_fee, csv_filename, pairs_per_questioner):
    '''
    Prints final price of the survey published on Amazon Mechanical Turk
    :param worker_price: price for each worker per questioner
    :param master_worker_price: bonus for each worker
    :param amazon_fee: price for amazon fee
    :param pairs_per_questioner: how many comparisons is on one questioner.
    :param csv_filename: name of the file where pairs are stored
    '''
    with open(f'{csv_filename}.csv') as f:
        lines = f.readlines()
        num_pairs = len(lines)-1
        print(f'Number of pairs generated: {num_pairs}')
    number_of_questionaries = num_pairs // pairs_per_questioner
    print(f'If each questioner has {pairs_per_questioner} comparisons, \n then number of questionaries: {number_of_questionaries}')

    print(f'If each worker is paid: {worker_price}, \n each master worker is paid {master_worker_price},')
    #is amazon fee charged for every worker?
    price = (worker_price + master_worker_price) * number_of_questionaries + amazon_fee
    print(f'then final is price: {price}')



if __name__ == '__main__':
    # Here write the dir, where folders with all plots are
    dir = 'C:/Users/Acer/Desktop/Data science/1 letnik/Project/filtered_images'

    # Here write the dir, where you want your sampled files to be copied to
    new_dir = 'C:/Users/Acer/Desktop/Data science/1 letnik/Project/filtered_images/sampled'

    # all the plot types you want to sample from
    plot_types = ['bar_plot', 'box_plot', 'histogram', 'line_plot', 'scatter_plot']

    # size of each sample
    sizes = [2, 1, 1, 2, 2]
    print(f'Number of plots {sum(sizes)}')

    # how many times each plot is compared, has to be even number
    k = 4

    # filename of the csv file, where plot pairs will be written
    csv_filename = 'test_final'

    generate_plot_pairs(plot_types, sizes, k, dir, new_dir, csv_filename)

    #here set the prices
    worker_price = 0.1
    master_worker_price = 0.2
    amazon_fee = 0.1
    pairs_per_questioner = 5

    calculate_final_price(worker_price, master_worker_price, amazon_fee, csv_filename, pairs_per_questioner)