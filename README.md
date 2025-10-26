# ML Projects

A collection of course and hobby experiments exploring a variety of machine-learning techniques, from classic NLP to modern deep learning and reinforcement learning. Each project lives in its own directory and can be run independently.

## Repository Table of Contents
- [Repository Overview](#repository-overview)
- [Projects](#projects)
  - [Author Classification – Naive Bayes NLP](#author-classification--naive-bayes-nlp)
  - [Credit Card Fraud Detection – Custom Neural Network](#credit-card-fraud-detection--custom-neural-network)
  - [Joke Recommendation – Collaborative Filtering](#joke-recommendation--collaborative-filtering)
  - [Raccoon Detection – Keras YOLOv2](#raccoon-detection--keras-yolov2)
  - [Mario AI Agent – Monte Carlo Reinforcement Learning](#mario-ai-agent--monte-carlo-reinforcement-learning)

## Repository Overview
The repository root contains individual project folders plus a standalone Java agent:

| Path | Description |
| ---- | ----------- |
| `Author Classification - naivebayLearning - NLP/` | Naive Bayes text classifier that distinguishes between disputed Federalist Papers. |
| `CreditCardFraudDetection-NN/` | Scratch-built feed-forward neural network for transaction fraud detection. |
| `Joke Recommentation Unsupervised Learning/` | Matrix factorisation recommender trained on the Jester joke ratings dataset. |
| `keras-yolo2-master-Raccoon Classification/` | YOLOv2-based object detector fine-tuned for raccoon imagery. |
| `ExMarioAgent.java` | Reinforcement-learning Mario agent submitted to the 2009 RL-Competition. |

Each project section below explains its layout, dependencies, configuration, and how to launch the code.

## Projects

### Author Classification – Naive Bayes NLP
- [Overview](#author-classification--naive-bayes-nlp-overview)
- [Directory Layout](#author-classification--naive-bayes-nlp-directory-layout)
- [Dependencies](#author-classification--naive-bayes-nlp-dependencies)
- [Configuration](#author-classification--naive-bayes-nlp-configuration)
- [Running the Classifier](#author-classification--naive-bayes-nlp-running-the-classifier)
- [Key Implementation Notes](#author-classification--naive-bayes-nlp-key-implementation-notes)

#### Author Classification – Naive Bayes NLP Overview
A Python 3 implementation that tokenises Federalist Papers essays and trains a unigram Naive Bayes classifier to attribute disputed essays to Hamilton, Madison, or Jay. The pipeline covers tokenisation, stop-word removal, stemming, dictionary smoothing, and log-probability scoring.

#### Author Classification – Naive Bayes NLP Directory Layout
| Path | Purpose |
| ---- | ------- |
| `main.py` | Entry point that orchestrates training and evaluation on the chosen author folders. |
| `tokenizer.py` | Handles tokenisation, stop-word removal, and stemming logic. |
| `dictionary.py` | Builds smoothed word-frequency dictionaries and computes log-probabilities. |
| `fileGet.py` | Splits documents into training/unknown sets and loads corpora. |
| `Hamilton/`, `Madison/`, `Jay/`, `Disputed/` | Default corpora of essays grouped by author. Binary subsets (`bin*`) are also provided for experiments. |

#### Author Classification – Naive Bayes NLP Dependencies
Install Python 3 plus the Natural Language Toolkit. The project requires the Punkt tokenizer and stop-word corpus:
```bash
pip install nltk pandas
python - <<'PY'
import nltk
nltk.download('punkt')
nltk.download('stopwords')
PY
```

#### Author Classification – Naive Bayes NLP Configuration
The dataset folders are configured at the top of `main.py`. Adjust the variables if you place corpora in different directories, or switch to the binary subsets by uncommenting the provided examples inside the script.

#### Author Classification – Naive Bayes NLP Running the Classifier
Run the default experiment with:
```bash
python3 main.py
```
By default the script analyses the `Hamilton`, `Madison`, `Jay`, and `Disputed` folders. Update the folder names (line 14 of `main.py`) to evaluate alternative corpora.

#### Author Classification – Naive Bayes NLP Key Implementation Notes
- Uses log-probabilities with add-one smoothing to avoid underflow.
- Unknown-token handling reserves a random split of each author’s texts to measure distinctive vocabulary usage.
- Outputs include per-author probabilities that incorporate prior publishing frequency.

### Credit Card Fraud Detection – Custom Neural Network
- [Overview](#credit-card-fraud-detection--custom-neural-network-overview)
- [Directory Layout](#credit-card-fraud-detection--custom-neural-network-directory-layout)
- [Dependencies](#credit-card-fraud-detection--custom-neural-network-dependencies)
- [Running the Trainer](#credit-card-fraud-detection--custom-neural-network-running-the-trainer)
- [Experiment Tips](#credit-card-fraud-detection--custom-neural-network-experiment-tips)

#### Credit Card Fraud Detection – Custom Neural Network Overview
Implements a neural network from first principles (no deep-learning frameworks) to classify credit-card transactions as fraudulent or legitimate. The network architecture, activation functions, and training loop are defined in pure Python.

#### Credit Card Fraud Detection – Custom Neural Network Directory Layout
| Path | Purpose |
| ---- | ------- |
| `neural_net.py` | Command-line interface for training and evaluating the model. |
| `neuron.py` | Defines the neuron and network classes powering forward/backward passes. |
| `trainCredit.csv`, `testCredit.csv` | Default Kaggle-style credit card datasets. Binary subsets (`trainBin.csv`, `testBin.csv`) are available for quick experimentation. |

#### Credit Card Fraud Detection – Custom Neural Network Dependencies
Requires Python 3 with NumPy for numerical operations.

#### Credit Card Fraud Detection – Custom Neural Network Running the Trainer
The script expects training and evaluation files, neuron count, and a decision threshold:
```bash
python3 neural_net.py trainCredit.csv testCredit.csv 28 0.5
```
- `28` specifies the neuron count per layer and must match the feature count in the CSVs.
- `0.5` sets the classification threshold; adjust as needed for new datasets.

#### Credit Card Fraud Detection – Custom Neural Network Experiment Tips
- The script skips the first row and column to match the supplied dataset formatting.
- Tune the `iterate` variable inside `neural_net.py` to change the number of passes over each training row.
- When experimenting with other datasets, start by increasing the threshold toward `0.9` to compensate for different class imbalances.

### Joke Recommendation – Collaborative Filtering
- [Overview](#joke-recommendation--collaborative-filtering-overview)
- [Directory Layout](#joke-recommendation--collaborative-filtering-directory-layout)
- [Dependencies](#joke-recommendation--collaborative-filtering-dependencies)
- [Running the Recommender](#joke-recommendation--collaborative-filtering-running-the-recommender)
- [Experiment Tips](#joke-recommendation--collaborative-filtering-experiment-tips)

#### Joke Recommendation – Collaborative Filtering Overview
A matrix-factorisation recommendation engine that predicts joke ratings using collaborative filtering on the Jester dataset. The implementation evaluates reconstruction accuracy across multiple optimisation iterations.

#### Joke Recommendation – Collaborative Filtering Directory Layout
| Path | Purpose |
| ---- | ------- |
| `project3.py` | Entry point implementing stochastic gradient descent for latent-factor learning. |
| `testJ.csv` | Lightweight sample dataset for quick experiments. |
| `jester_dataset_3.zip` | Full Jester dataset archive; unzip to access the complete ratings matrix. |

#### Joke Recommendation – Collaborative Filtering Dependencies
Install Python 3 along with the required scientific stack:
```bash
pip install pandas numpy matplotlib
```

#### Joke Recommendation – Collaborative Filtering Running the Recommender
Provide the dataset path and optional hyperparameters. Missing arguments fall back to sensible defaults.
```bash
python3 project3.py testJ.csv 0.005 0.001 10 500
```
Arguments correspond to `[dataset] [learning_rate] [regularisation_lambda] [latent_features] [iterations]`.

#### Joke Recommendation – Collaborative Filtering Experiment Tips
- Keep the learning rate small (≈0.005) to avoid divergence.
- Use `testJ.csv` for rapid iteration, then switch to the unzipped Jester dataset for full-scale evaluation.
- Visualisation hooks rely on Matplotlib; ensure you have a display backend if plotting on a remote server.

### Raccoon Detection – Keras YOLOv2
- [Overview](#raccoon-detection--keras-yolov2-overview)
- [Directory Layout](#raccoon-detection--keras-yolov2-directory-layout)
- [Dependencies](#raccoon-detection--keras-yolov2-dependencies)
- [Configuration](#raccoon-detection--keras-yolov2-configuration)
- [Training](#raccoon-detection--keras-yolov2-training)
- [Inference](#raccoon-detection--keras-yolov2-inference)
- [Notes](#raccoon-detection--keras-yolov2-notes)

#### Raccoon Detection – Keras YOLOv2 Overview
Forks the `keras-yolo2` project to train an object detector that finds raccoons in images. The workflow covers anchor generation, training on annotated images, and running inference with the trained weights.

#### Raccoon Detection – Keras YOLOv2 Directory Layout
| Path | Purpose |
| ---- | ------- |
| `config.json` | Central configuration for dataset paths, training hyperparameters, and model architecture. |
| `train.py` / `predict.py` | CLI scripts for training and inference, respectively. |
| `gen_anchors.py` | Utility for recomputing anchor boxes from the training annotations. |
| `images/` | Sample images for inference sanity checks. |
| `experimental/`, `examples/`, `backend.py`, `frontend.py`, `utils.py` | Core YOLOv2 implementation components. |

#### Raccoon Detection – Keras YOLOv2 Dependencies
Install Python 3 with the libraries listed in `requirements.txt` (Keras, OpenCV, imgaug, tqdm, h5py, etc.). Use a virtual environment for isolation:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### Raccoon Detection – Keras YOLOv2 Configuration
Edit `config.json` before training:
- Set `model: "Tiny Yolo"` to match the supplied lightweight backbone.
- Update `train_image_folder` and `train_annot_folder` to point at the extracted raccoon dataset (images + Pascal VOC XML annotations).
- Leave `pretrained_weights` blank unless resuming from existing weights.
- Choose a descriptive `saved_weights_name` for the output model file.

#### Raccoon Detection – Keras YOLOv2 Training
Generate anchors (optional) and train the network:
```bash
python gen_anchors.py -c config.json
python train.py -c config.json
```
Use the provided hyperparameters (e.g., 2 training iterations, 10 epochs, 3 warm-up epochs) as a starting point.

#### Raccoon Detection – Keras YOLOv2 Inference
After training, run detection on an image or video:
```bash
python predict.py -c config.json -w path/to/best_weights.h5 -i path/to/input
```
Detections are written alongside the input media with a `-Detected` suffix.

#### Raccoon Detection – Keras YOLOv2 Notes
- Ensure the raccoon dataset is resized consistently; YOLO performs best when training images share similar dimensions.
- The project is optimised for live video streams, so highly variable still-image sizes may reduce accuracy.

### Mario AI Agent – Monte Carlo Reinforcement Learning
- [Overview](#mario-ai-agent--monte-carlo-reinforcement-learning-overview)
- [Dependencies](#mario-ai-agent--monte-carlo-reinforcement-learning-dependencies)
- [Running the Agent](#mario-ai-agent--monte-carlo-reinforcement-learning-running-the-agent)
- [Implementation Notes](#mario-ai-agent--monte-carlo-reinforcement-learning-implementation-notes)

#### Mario AI Agent – Monte Carlo Reinforcement Learning Overview
`ExMarioAgent.java` customises the Rutgers RL-Competition 2009 Mario agent. It augments the baseline heuristic controller with Monte Carlo state-value updates, episodic memory, and JSON-driven policy initialisation to solve Mario levels via reinforcement learning.

#### Mario AI Agent – Monte Carlo Reinforcement Learning Dependencies
- Java 8 or newer.
- RL-Glue codec (`org.rlcommunity.rlglue`) to interface with the Mario environment.
- JSON processing library available on the classpath to parse `ref_export.json`.

#### Mario AI Agent – Monte Carlo Reinforcement Learning Running the Agent
Compile the agent alongside the RL-Competition environment and launch via the RL-Glue agent loader:
```bash
javac ExMarioAgent.java
java org.rlcommunity.rlglue.codec.util.AgentLoader edu.rutgers.rl3.comp.ExMarioAgent
```
Ensure `ref_export.json` and the RL environment resources are accessible on the classpath or working directory.

#### Mario AI Agent – Monte Carlo Reinforcement Learning Implementation Notes
- Tracks 13 binary state features covering monsters, pits, power-ups, and terrain topology.
- Maintains policy, reward, and iteration tables sized at `2^13 × 12` for Monte Carlo updates.
- Stores per-episode state/action/reward sequences to refine the policy after each run.

---

Have fun exploring the projects! Contributions and experiments are welcome—feel free to open issues or pull requests with improvements.
