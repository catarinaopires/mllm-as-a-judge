import argparse
import ast
import os
import sys
import time

import pandas as pd
from dotenv import load_dotenv
from PIL import Image

from llm.base_llm import LlmSession
from llm.gemini import GeminiLlm
from template_builder import TemplateBuilder

################ DATA LOADING ################

load_dotenv()
DATA_DIR_PATH = os.getenv("DATA_DIR_PATH")

DF_TOPICS, DF_ARTICLES, DF_RELEVANT = None, None, None


def load_data(topic_file, article_file, relevant_file):
    df_topics = pd.read_csv(topic_file, index_col=0)
    df_articles = pd.read_csv(article_file, index_col=0)
    df_relevant = pd.read_csv(relevant_file, index_col=0)

    return df_topics, df_articles, df_relevant


def get_article_images_info(images):
    image_paths = []
    captions = []

    for image in images:
        image_paths.append(f"{image['fig_id']}.jpg")
        captions.append(image["caption"])

    return image_paths, captions


def get_images_from_paths(images_paths, from_article=False):
    images = []

    for image_path in images_paths:
        path = ""
        if from_article:
            path = f"{DATA_DIR_PATH}figures/images/{image_path}"
        else:
            path = DATA_DIR_PATH + image_path

        if os.path.isfile(path):
            image = Image.open(path)
            images.append(image)
            image.close()
        else:
            print(f"Image not found: {image_path}")
    return images


##############################################
def judge_article_for_topic(topic, group, df):
    topics_images_paths = ast.literal_eval(DF_TOPICS.loc[topic, "images"])
    images = get_images_from_paths(topics_images_paths)

    # Set up the system instruction
    system_instruction = TemplateBuilder("system", "2").build()

    llm_session = LlmSession(
        GeminiLlm(
            api_key=os.getenv("GOOGLE_API_KEY"),
            system_instruction=system_instruction,
        )
    )

    # Present the patient's case
    case_presenting_prompt = TemplateBuilder("instructions", "4a").build(
        case_description=DF_TOPICS.loc[topic, "description"],
        case_images=topics_images_paths,
    )

    try:
        answer = llm_session.prompt([case_presenting_prompt, *images])
    except Exception as e:
        print(f"PError(topic={topic})=: {e}")

    # Relevant example
    relevant_doi = DF_RELEVANT.loc[topic, "doi"]
    relevant_article_figures = ast.literal_eval(
        DF_ARTICLES.loc[relevant_doi, "figures"]
    )
    relevant_figures_paths, relevant_captions = get_article_images_info(
        relevant_article_figures
    )
    relevant_figures = get_images_from_paths(relevant_figures_paths, from_article=True)

    # Present relevant example
    relevant_presenting_prompt = TemplateBuilder("instructions", "4b").build(
        article_title=DF_ARTICLES.loc[relevant_doi, "title"],
        article_authors=ast.literal_eval(DF_ARTICLES.loc[relevant_doi, "authors"]),
        article_abstract=DF_ARTICLES.loc[relevant_doi, "abstract"],
        article_fulltext=DF_ARTICLES.loc[relevant_doi, "fulltext"],
        article_images=relevant_figures_paths,
        article_captions=relevant_captions,
    )

    try:
        answer = llm_session.prompt([relevant_presenting_prompt, *relevant_figures])
    except Exception as e:
        print(f"RError(topic={topic})=: {e}")

    for _, row in group.iterrows():
        article_figures = ast.literal_eval(DF_ARTICLES.loc[row["doi"], "figures"])
        figures_paths, captions = get_article_images_info(article_figures)
        figures = get_images_from_paths(figures_paths, from_article=True)

        prompt = TemplateBuilder("context", "3").build(
            article_title=DF_ARTICLES.loc[row["doi"], "title"],
            article_authors=ast.literal_eval(DF_ARTICLES.loc[row["doi"], "authors"]),
            article_abstract=DF_ARTICLES.loc[row["doi"], "abstract"],
            article_fulltext=DF_ARTICLES.loc[row["doi"], "fulltext"],
            article_images=figures_paths,
            article_captions=captions,
        )

        try:
            answer = llm_session.prompt([prompt, *figures], llm_clean_message=True)

            if answer[0] == "0" or answer[0] == "1":
                answer = answer[0]
                df.loc[
                    (df["topic"] == topic) & (df["doi"] == row["doi"]), "llm_answer"
                ] = answer
            else:
                # Not possible to judge
                print(f"Answer(topic={topic},{row['doi']})=: {answer}")
        except Exception as e:
            # Not possible to judge
            print(f"Error(topic={topic},{row['doi']})=: {e}")


def get_args_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "file",
        help="file with articles to be judged",
        type=str,
    )

    parser.add_argument(
        "-o",
        help="output file name",
        type=str,
        required=True,
    )

    parser.add_argument("-t", help="topic number", type=int)

    return parser


def main(args):

    if not os.path.exists(args.file):
        print(f"File not found: {args.file}")
        sys.exit(1)

    print("Loading data...")
    global DF_TOPICS, DF_ARTICLES, DF_RELEVANT
    DF_TOPICS, DF_ARTICLES, DF_RELEVANT = load_data(
        f"{DATA_DIR_PATH}topics.csv",
        f"{DATA_DIR_PATH}articles.csv",
        f"{DATA_DIR_PATH}relevant.csv",
    )

    print(f"Reading file: {args.file}")
    df = pd.read_csv(args.file)

    if args.t:  # Filter topic
        df = df[df["topic"] == args.t]

    grouped = df.groupby("topic")

    start = time.time()
    print("Starting the process...")
    # Iterate over each group and call the function
    for topic, group in grouped:
        print(f"\nProcessing group for topic: {topic}")
        judge_article_for_topic(topic, group, df)
    print("Process finished.")

    output_dir = "../results/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    df.to_csv(f"{output_dir}{args.o}", index=False)
    print(f"Results saved to: {args.o}")

    end = time.time()
    print(f"Time taken: {end-start}")


if __name__ == "__main__":
    parser = get_args_parser()
    args = parser.parse_args()

    main(args)
