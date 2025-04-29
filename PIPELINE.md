

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
   - Download the NLTK dataset from [nltk_data/gh-pages](https://github.com/nltk/nltk_data/tree/gh-pages).
   - Unzip and place it in the correct directory:
     ```bash
     # Rename the `packages` folder to `nltk_data` and move it to the parent directory of the project root
     unzip /nltk_data/tokenizer/punkt_tab.zip
     ```

2. **Pretrained Model**:
   - Download pretrained files (refer to the project's README for instructions).

3. **HPO Data**:
   - Place the latest `hpo.obo` file into the `data/` directory.

---

### **GPU Configuration**
- In VSCode, search for `"cuda:"` and replace it with an available GPU ID (e.g., `cuda:0`).
 and 'device'
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