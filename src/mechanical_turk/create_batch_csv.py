import random
import pandas as pd
from itertools import islice

def chunk(it, size):
    """
    Chunk the iterable into chunks of size "size"
    :param it: Iterable that will be chunked
    :param size: Chunk size
    :return:
    """
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())

if __name__ == '__main__':
    bucket_url = f"https://plot-comparisons.s3.eu-central-1.amazonaws.com/batch_1_prod/"
    pairs_per_hit = 10
    plot_comparisons_csv = "./batches/batch_9.csv"
    save_name = "./batches/batch_9_prod.csv"

    # Select the pairs and shuffle them
    pairs = [(row["first"], row["second"]) for _, row in pd.read_csv(plot_comparisons_csv).iterrows()]
    random.shuffle(pairs)

    # Parse the plot comparisons into a format that will be parsed by the Javascript uploaded on MT
    # (; separator between image urls in the same comparisona and \t between comparisons)
    data = []
    for hit_data in chunk(pairs, pairs_per_hit):
        plot_comparisons = "\t".join([bucket_url + el[0] + ";" + bucket_url + el[1] for el in hit_data])
        data.append([plot_comparisons, str([el[0] for el in hit_data]), str([el[1] for el in hit_data])])

    # Store into a dataframe and write to a .csv
    df = pd.DataFrame(data, columns=["plot_comparisons", "plot_1", "plot_2"])
    df.to_csv(save_name, header=True, index=False)
