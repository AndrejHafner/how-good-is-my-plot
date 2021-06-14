import json
import operator
from functools import reduce

import pandas as pd


def parse_comparisons(plots_1, plots_2, answers):
    def parse_single_comparison(first_plot, second_plot, answer):
        def parse_checkbox(checkboxes, key):
            if checkboxes["first"][key]:
                return "first"
            elif checkboxes["second"][key]:
                return "second"
            else:
                return ""

        return {
            "first_plot": first_plot,
            "second_plot": second_plot,
            "selected": first_plot if answer["selected_plot"] == "left" else second_plot,
            **{key: parse_checkbox(answer["checkboxes"], key) for key in answer["checkboxes"]["first"].keys()}
        }

    return [parse_single_comparison(*el) for el in zip(plots_1, plots_2, answers)]



def parse_results(df):
    input_plots_1 = [json.loads(el.replace("'", '"')) for el in list(df["Input.plot_1"])]
    input_plots_2 = [json.loads(el.replace("'", '"')) for el in list(df["Input.plot_2"])]
    answers = [json.loads(el.replace("'", '"')) for el in list(df["Answer.data"])]

    data = reduce(operator.concat, [parse_comparisons(*comp_data) for comp_data in zip(input_plots_1, input_plots_2, answers)], list())
    return data

if __name__ == '__main__':
    df = pd.read_csv("./batches/results/prod_batch_1_test_results.csv")
    data = parse_results(df)

    results_df = pd.DataFrame(data)
    results_df.to_csv("./batches/results/prod_batch_1_parsed.csv", index=False)
