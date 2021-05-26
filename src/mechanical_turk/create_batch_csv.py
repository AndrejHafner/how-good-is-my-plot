import random
import pandas as pd
from itertools import islice

def chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())

if __name__ == '__main__':
    batch_name = "prod_batch_1_first_test"
    bucket_url = f"https://plot-comparisons.s3.eu-central-1.amazonaws.com/{batch_name}/"
    pairs_per_hit = 20
    plot_comparisons_csv = "./batches/prod_batch_1_first_test.csv"
    save_name = "./batches/prod_batch_1_first_test_deploy.csv"

    pairs = [(row["first"], row["second"]) for _, row in pd.read_csv(plot_comparisons_csv).iterrows()]
    random.shuffle(pairs)
    
    data = []
    for hit_data in chunk(pairs, pairs_per_hit):
        plot_comparisons = "\t".join([bucket_url + el[0] + ";" + bucket_url + el[1] for el in hit_data])
        data.append([plot_comparisons, str([el[0] for el in hit_data]), str([el[1] for el in hit_data])])

    df = pd.DataFrame(data, columns=["plot_comparisons", "plot_1", "plot_2"])

    df.to_csv(save_name, header=True, index=False)
