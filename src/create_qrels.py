import argparse
import os
import sys

import pandas as pd


def get_stats(df_results):
    # Count number of documents
    total_docs = len(df_results)
    print("Number of documents:", total_docs)
    # Count number of relevant documents
    nr_relevant_docs = df_results["llm_answer"].sum().astype(int)
    print("Number of relevant documents:", nr_relevant_docs)
    # Percentage of relevant documents
    print("Percentage of relevant documents:", nr_relevant_docs / total_docs * 100)
    # Count nan values (not possible to judge)
    nr_nan = df_results["llm_answer"].isna().sum()
    print("Number of nan values:", nr_nan)
    # Percentage of nan values
    print("Percentage of nan values:", nr_nan / total_docs * 100)


def create_qrels_file(df_results, file):
    # QRELS file format: <topic> <0> <doc_id> <relevance=0/1>

    # Not possible to judge considered as non-relevant
    df_results["llm_answer"] = df_results["llm_answer"].fillna(0)
    df_results["llm_answer"] = df_results["llm_answer"].astype(int)

    for _, row in df_results.iterrows():
        topic = row["topic"]
        doi = row["doi"]
        llm_answer = row["llm_answer"]

        file_row = f"{topic}\t0\t{doi}\t{llm_answer}\n"
        file.write(file_row)


def get_args_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "file",
        help="file with articles judged",
        type=str,
    )

    parser.add_argument(
        "-o",
        help="output qrels file name",
        type=str,
        required=True,
    )

    return parser


def main(args):

    if not os.path.exists(args.file):
        print(f"File not found: {args.file}")
        sys.exit(1)

    print(f"Reading file: {args.file}")
    df = pd.read_csv(args.file)

    file = open(args.o, "w")
    create_qrels_file(df, file)
    file.close()


if __name__ == "__main__":
    parser = get_args_parser()
    args = parser.parse_args()

    main(args)
