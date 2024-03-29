import json
import operator
from functools import reduce

import pandas as pd


def parse_comparisons(plots_1, plots_2, answers):
    """
    Parse the result of a single questionnaire (a single worker output)
    :param plots_1:
    :param plots_2:
    :param answers:
    :return:
    """

    def parse_single_comparison(first_plot, second_plot, answer):
        """
        Utility functions
        :param first_plot:
        :param second_plot:
        :param answer:
        :return:
        """
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
    """
    Parse the output CSV from mechanical turk into a nice format for further processing
    :param df: Pandas DataFrame created from the MT output CSV
    :return:
    """
    input_plots_1 = [json.loads(el.replace("'", '"')) for el in list(df["Input.plot_1"])]
    input_plots_2 = [json.loads(el.replace("'", '"')) for el in list(df["Input.plot_2"])]
    answers = [json.loads(el.replace("'", '"')) for el in list(df["Answer.data"])]

    data = reduce(operator.concat, [parse_comparisons(*comp_data) for comp_data in zip(input_plots_1, input_plots_2, answers)], list())
    return data

if __name__ == '__main__':
    df = pd.read_csv("./batches/results/swiss_sys_run_9.csv")
    data = parse_results(df)
    results_df = pd.DataFrame(data)
    results_df.to_csv("./batches/results/swiss_system/swiss_sys_run_9_parsed.csv", index=False)
