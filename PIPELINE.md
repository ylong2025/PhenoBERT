

### **Environment Setup**
1. Create a conda environment:
   ```bash
   conda create -n phenobert python=3.8 -y
   conda activate phenobert
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

### **Data Preparation**
1. **NLTK Data**:

The project requires NLTK's Punkt tokenizer data. There are two ways to install it:

- Option 1: Automatic Download (Recommended if internet connection is stable)

- Option 2: Manual Installation (For restricted network environments)
   - Download the NLTK dataset from [nltk_data/gh-pages](https://github.com/nltk/nltk_data/tree/gh-pages).
   - Unzip and install manually
   ```bash
   # Rename the downloaded folder from 'packages' to 'nltk_data'
   mv packages nltk_data

   # Move to the /root directory
   mv nltk_data /root/
   ```
   ```python
   import os
   import zipfile

   # Define the root directory to process
   root_dir = os.path.expanduser('/root/nltk_data')

   # Recursively traverse directory and subdirectories
   for root, dirs, files in os.walk(root_dir):
      for file in files:
         if file.endswith('.zip'):
               zip_file_path = os.path.join(root, file)
               try:
                  # Open the zip file
                  with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                     # Extract to current directory
                     zip_ref.extractall(root)
                  print(f"Extracted {zip_file_path}")
               except zipfile.BadZipFile:
                  print(f"Cannot extract {zip_file_path}, may be a corrupted zip file.")
   ```

2. **Pretrained Model**:
   - Download pretrained files (refer to the project's README for instructions).

3. **HPO Data**:
   - Place the latest `hpo.obo` file into the `data/` directory.

4. **Stanza resources**:

When running test.ipynb, if automatic download fails, you need to manually download all models from [stanfordnlp/stanza-en](https://huggingface.co/stanfordnlp/stanza-en)

```bash
# Create directory structure:
mkdir -p phenobert/stanza-en/en

# Place downloaded models in:
phenobert/
└── stanza-en/
    └── en/
        ├── ner/
        ├── pos/
        ├── ... (all other model folders)
        └── tokenize/
```
---

### **Execution Steps**
1. **Preprocess HPO Data**:
   ```bash
   cd phenobert/utils
   python process_hpo.py --obo ../data/hpo.obo --output ../data/hpo.json
   ```

2. **Generate Datasets**:
   ```bash
   python produce_trainSet.py
   python produce_trainSet_sub.py
   python produce_data4train_new.py
   ```

3. **Start Training**:


**Device:** NVIDIA RTX 3090 (24GB VRAM)

| Script            | Time     | VRAM Usage | Epochs |
|-------------------|----------|------------|-------|
| `train.py`        | ~15min   |         | 100   |
| `train_sub.py`    | ~100min  |        | 150   |
| `my_bert_match.py` | ~1d  | <5GB      | 10    |

   ```bash
   # produce trained models for CNN model
    python train.py
    python train_sub.py

    # produce trained models for BERT model
    python my_bert_match.py
   ```