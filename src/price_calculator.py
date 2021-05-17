from generate_plot_pairs import generate_plot_pairs


def calculate_final_price(worker_price, master_worker_price, csv_filename, pairs_per_questioner):
    '''
    Prints final price of the survey published on Amazon Mechanical Turk.
    Amazon's fee is 20% on the reward for workers, additional 20% if there is more than 10 assignments.
    Additional 5% fee of the reward for masters workers.
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
    #print(f'If each questioner has {pairs_per_questioner} comparisons, \n then ')
    print(f'Number of questionaries: {number_of_questionaries}')

    #print(f'If each worker is paid: {worker_price}, \n each master worker is paid {master_worker_price},')

    price = (( 1 + 0.2 ) * worker_price + ( 1 + 0.05 )*master_worker_price) * number_of_questionaries
    print(f'Final price: {price}')



if __name__ == '__main__':
    '''
    # Here write the dir, where folders with all plots are
    dir = 'C:/Users/Acer/Desktop/Data science/1 letnik/Project/filtered_images'

    # Here write the dir, where you want your sampled files to be copied to
    new_dir = 'C:/Users/Acer/Desktop/Data science/1 letnik/Project/filtered_images/sampled'

    # all the plot types you want to sample from
    plot_types = ['bar_plot', 'box_plot', 'histogram', 'line_plot', 'scatter_plot', 'pie_chart']

    # size of each sample
    sizes = [200, 195, 200, 200, 200, 200]
    print(f'Number of plots {sum(sizes)}')

    # how many times each plot is compared, has to be even number
    k = 6

    # filename of the csv file, where plot pairs will be written
    csv_filename = 'test_final'

    generate_plot_pairs(plot_types, sizes, k, dir, new_dir, csv_filename)

    #here set the prices
    worker_price = 1
    master_worker_price = 0.2
    pairs_per_questioner = 20

    calculate_final_price(worker_price, master_worker_price, csv_filename, pairs_per_questioner)
    '''

    for size in [10,100,195]:
        for k in [4,6,10,15]:
            # Here write the dir, where folders with all plots are
            dir = 'C:/Users/Acer/Desktop/Data science/1 letnik/Project/filtered_images'

            # Here write the dir, where you want your sampled files to be copied to
            new_dir = f'C:/Users/Acer/Desktop/Data science/1 letnik/Project/filtered_images/sampled_{size}_{k}'

            # all the plot types you want to sample from
            plot_types = ['bar_plot', 'box_plot', 'histogram', 'line_plot', 'scatter_plot', 'pie_chart']

            # size of each sample
            sizes = [size for _ in range(len(plot_types))]
            print(f'Number of plots {sum(sizes)}')
            print(f'Each plot is shown {k} times')

            # how many times each plot is compared, has to be even number
            #k = 6

            # filename of the csv file, where plot pairs will be written
            csv_filename = 'test_final'

            generate_plot_pairs(plot_types, sizes, k, dir, new_dir, csv_filename)

            # here set the prices
            worker_price = 1
            master_worker_price = 0.2
            pairs_per_questioner = 20

            calculate_final_price(worker_price, master_worker_price, csv_filename, pairs_per_questioner)
            print('------------------------')
