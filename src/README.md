## Usage

### 1. Apply MLLM-as-a-Judge

Get Gemini 1.5 Pro relevance assesment for articles in `file`.

<b>Note:</b> Must have the following files:
- `{DATA_DIR_PATH}topics.csv`: Parsed topics - transformation from the task's XML files to CSV files (output of [this](https://github.com/catarinaopires/eval-multimodal-medical-case-retrieval/tree/main/src#parse-datasets))
- `{DATA_DIR_PATH}articles.csv`: Parsed articles - transformation from the task's XML files to CSV files (output of [this](https://github.com/catarinaopires/eval-multimodal-medical-case-retrieval/tree/main/src#parse-datasets))
- `{DATA_DIR_PATH}relevant.csv`: CSV file with example of a relevant article for each topic (columns: topic, doi)

```
usage: mllm_as_judge.py [-h] -o O [-t T] file

positional arguments:
  file        file with articles to be judged

options:
  -h, --help  show this help message and exit
  -o O        output file name
  -t T        topic number
```

### 2. Create QRELS file

Create QRELS file based on relevance judgments from previous step. `file` corresponds to `O` (output file name) from previous step.

```
usage: create_qrels.py [-h] -o O file

positional arguments:
  file        file with articles judged

options:
  -h, --help  show this help message and exit
  -o O        output qrels file name
```