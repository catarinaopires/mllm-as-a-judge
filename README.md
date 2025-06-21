## ImageCLEFmed 2013 case-based retrieval task relevance judgments expansion via an MLLM-as-a-Judge approach

<b>Authors:</b> Catarina Pires, Sérgio Nunes, Luís Filipe Teixeira

### Context

The [ImageCLEFmed 2013 case-based retrieval task](https://www.imageclef.org/2013/medical) was limited by the small sample size of evaluated articles, as human assessment was labor-intensive and not easily scalable, resulting in only 15,028 judgments across 35 topics. To address this challenge, we utilize multimodal large language models to expand relevance judgments and handle unjudged documents in the dataset.

### Description

[Our dataset](https://doi.org/10.5281/zenodo.14866104) contains additional relevance judgments (qrels) for the [ImageCLEFmed 2013 case-based retrieval task](https://www.imageclef.org/2013/medical). These judgments were generated using an MLLM-as-a-Judge approach, leveraging the Gemini 1.5 Pro model to simulate human assessment and expand the original qrels of the task.

The dataset includes 543,625 new relevance judgments for the ImageCLEFmed 2013 case-based retrieval task.

Each row represents a single judgment and follows the format:
`{topic_number} 0 {article_DOI} {relevance}`

Where:
- `{topic_number}` refers to the query topic.
- `{article_DOI}` identifies the document.
- `{relevance}` indicates the degree of relevance (0 for non-relevant, 1 for relevant).


### Installation and Use
1. Install the required packages using `pip install -r requirements.txt`.

2. Then follow the usage instructions [here](src/README.md) to run the code of each step of the pipeline, after setting the environment variables explained below.


### Environment Variables

In order to run the project, you need to set all of the following environment variables in a .env file:

- GOOGLE_API_KEY: Google API key.
- DATA_DIR_PATH: Dataset directory (file structure detailed [here](https://github.com/catarinaopires/eval-multimodal-medical-case-retrieval/blob/main/README.md#dataset)).


### Acknowledgements

This work is co-financed by Component 5 - Capitalization and Business Innovation, integrated into the Resilience Dimension of the Recovery and Resilience Plan, within the scope of the Recovery and Resilience Mechanism (MRR) of the European Union (EU), framed under Next Generation EU, for the period 2021–2026, within the project HfPT (reference 41).
Additionally, this work received funding from the project “PTicola - Increasing Computationally Language Resources for Portuguese” (reference CPCA-IAC/AV/594794/2023), with DOI 10.54499/CPCA-IAC/AV/594794/2023.

### Citation

Please cite the resource if you use this data.

```
@misc{mllm-expansion_qrel_2013_case_based,
    author = {Pires, Catarina and Nunes, Sérgio and Teixeira, Luís Filipe},
    title = {{ImageCLEFmed 2013 case-based retrieval task relevance judgments expansion via an MLLM-as-a-Judge approach}},
    doi = {10.5281/zenodo.14866104},
    howpublished= {\url{https://doi.org/10.5281/zenodo.14866103}},
    type = {Dataset},
    year = {2025},
    institution = {INESC TEC}
}
```
