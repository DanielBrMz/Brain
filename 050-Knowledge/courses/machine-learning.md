---
title: "Course: Machine Learning"
type: course
status: active
created: 2026-03-22
tags: [knowledge, course, cs, machine-learning, deep-learning, nlp, computer-vision, medical-imaging]
prerequisites: [linear-algebra, probability-statistics, multivariable-calculus, python]
---

# Machine Learning

> *Back to [[../cs-syllabus|CS Syllabus]] | Related: [[data-structures-algorithms|DSA]], [[databases|Databases]], [[distributed-systems|Distributed Systems]]*

## Motivation

Machine learning is the study of algorithms that improve through experience. From recommendation systems to autonomous vehicles, from drug discovery to language understanding, ML has become the most transformative technology of the 21st century. This course covers classical methods through modern deep learning, with special attention to medical imaging applications relevant to clinical research.

## Prerequisites

- **Linear Algebra:** Vectors, matrices, eigenvalues/eigenvectors, SVD, matrix calculus
- **Probability & Statistics:** Bayes' theorem, distributions, MLE, MAP, hypothesis testing
- **Multivariable Calculus:** Gradients, chain rule, Jacobians, Hessians
- **Python:** NumPy, pandas, matplotlib proficiency

---

## I. Foundations

### 1.1 Learning Framework

- **Supervised learning:** Labeled training data (x, y). Goal: learn f: X -> Y.
- **Unsupervised learning:** Unlabeled data. Goal: discover structure (clusters, manifolds, distributions).
- **Semi-supervised:** Small amount of labeled data + large amount of unlabeled data.
- **Self-supervised:** Generate labels from the data itself (e.g., predicting masked tokens).
- **Reinforcement learning:** Agent interacts with environment, receives rewards.

### 1.2 Bias-Variance Tradeoff

- **Bias:** Error from overly simplistic model assumptions (underfitting).
- **Variance:** Error from sensitivity to training data fluctuations (overfitting).
- **Decomposition:** Expected error = Bias^2 + Variance + Irreducible noise.
- **Regularization** reduces variance at the cost of increased bias.

### 1.3 Evaluation

- **Classification metrics:** Accuracy, precision, recall, F1, ROC-AUC, PR-AUC, confusion matrix.
- **Regression metrics:** MSE, RMSE, MAE, R-squared.
- **Cross-validation:** k-fold, stratified k-fold, leave-one-out.
- **Medical imaging specific:** Dice coefficient, Hausdorff distance, sensitivity/specificity at clinical operating points.

---

## II. Classical Machine Learning

### 2.1 Linear Regression

- Model: y = w^T x + b. Minimize MSE loss.
- **Closed-form (Normal equation):** w = (X^T X)^{-1} X^T y. O(d^3) computation.
- **Gradient descent:** Iteratively update w -= alpha * gradient. Scales to large d.
- **Regularization:** L2 (Ridge) adds lambda * ||w||^2; L1 (Lasso) adds lambda * ||w||_1 for sparsity; Elastic Net combines both.

### 2.2 Logistic Regression

- Model: P(y=1|x) = sigma(w^T x + b) where sigma is the sigmoid function.
- Maximize log-likelihood (minimize cross-entropy loss).
- No closed-form; solved via gradient descent or Newton's method.
- Decision boundary is a hyperplane in feature space.
- **Multi-class:** Softmax regression (multinomial logistic regression). One-vs-rest or one-vs-one for binary classifiers.

### 2.3 Support Vector Machines (SVM)

**Hard-margin SVM:**
- Find the hyperplane that maximizes the margin between two classes.
- Optimization: minimize ||w||^2 subject to y_i(w^T x_i + b) >= 1.

**Soft-margin SVM:**
- Allow misclassifications with slack variables xi_i. Regularization parameter C controls the trade-off.

**Dual Formulation:**
- Lagrangian dual reveals that the solution depends only on dot products x_i^T x_j.
- Support vectors are the training points with non-zero Lagrange multipliers.

**Kernel Trick:**
- Replace dot products with kernel function K(x_i, x_j) = phi(x_i)^T phi(x_j).
- **Linear kernel:** K(x, z) = x^T z.
- **Polynomial kernel:** K(x, z) = (x^T z + c)^d.
- **RBF (Gaussian) kernel:** K(x, z) = exp(-gamma * ||x - z||^2). Maps to infinite-dimensional space.
- Mercer's theorem: any positive semi-definite kernel corresponds to a valid feature mapping.

### 2.4 Decision Trees

- Recursive binary partitioning of feature space.
- **Split criteria:** Information gain (entropy reduction), Gini impurity, variance reduction (regression).
- **Pruning:** Pre-pruning (max depth, min samples) or post-pruning (cost-complexity pruning).
- Interpretable but prone to overfitting. High variance.

### 2.5 Ensemble Methods

**Random Forests:**
- Bagging (bootstrap aggregation) of decision trees + random feature subsets at each split.
- Reduces variance while maintaining low bias. Highly robust.
- Feature importance via mean decrease in impurity or permutation importance.

**Boosting:**
- Sequentially train weak learners, each focusing on previously misclassified examples.
- **AdaBoost:** Reweight misclassified samples; combine weak learners by weighted vote.
- **Gradient Boosting:** Fit new trees to the negative gradient (residuals) of the loss function.
- **XGBoost:** Regularized gradient boosting with second-order Taylor expansion, column subsampling, and efficient histogram-based split finding. Often the top performer on tabular data.
- **LightGBM:** Leaf-wise tree growth (vs. level-wise). Gradient-based one-side sampling (GOSS) and exclusive feature bundling for speed. Handles large datasets efficiently.
- **CatBoost:** Native categorical feature handling. Ordered boosting to reduce prediction shift.

### 2.6 Clustering

**K-Means:**
- Iteratively assign points to nearest centroid, then recompute centroids.
- Converges to local minimum. Sensitive to initialization — use k-means++ (smart initialization).
- Assumes spherical clusters of similar size.

**DBSCAN:**
- Density-based: core points (>= minPts within epsilon radius), border points, noise points.
- Discovers clusters of arbitrary shape. No need to specify k.
- Struggles with varying density clusters.

**Hierarchical Clustering:**
- **Agglomerative (bottom-up):** Merge closest clusters iteratively. Linkage: single, complete, average, Ward's.
- **Divisive (top-down):** Split clusters recursively.
- Produces a dendrogram; cut at desired level for k clusters.

### 2.7 Dimensionality Reduction

**PCA (Principal Component Analysis):**
- Find orthogonal directions of maximum variance. Eigenvectors of covariance matrix.
- Linear, fast, well-understood. Reconstruction error minimized.
- Choose components retaining 95%+ of variance.

**t-SNE:**
- Non-linear. Preserves local structure in 2D/3D visualizations.
- Minimizes KL divergence between high-dimensional and low-dimensional pairwise probability distributions.
- Perplexity hyperparameter. Not deterministic; do NOT interpret distances between clusters literally.

**UMAP:**
- Faster than t-SNE, better preserves global structure.
- Based on Riemannian geometry and algebraic topology (fuzzy simplicial complexes).
- Preferred for large datasets and when global structure matters.

---

## III. Deep Learning Foundations

### 3.1 Neural Networks

- **Perceptron:** Single linear unit with step activation. Can only learn linearly separable functions.
- **Multi-layer perceptron (MLP):** Stack of fully connected layers with non-linear activations.
- **Universal approximation theorem:** A single hidden layer with enough units can approximate any continuous function (but may need exponentially many units).

### 3.2 Activation Functions

- **ReLU:** max(0, x). Simple, avoids vanishing gradient for positive inputs. Dying ReLU problem.
- **Leaky ReLU / PReLU:** Allow small negative slope. Addresses dying ReLU.
- **GELU:** x * Phi(x). Smooth approximation to ReLU. Used in Transformers.
- **Sigmoid / Tanh:** Saturating; used in gates (LSTM, GRU) but generally avoided in hidden layers.
- **Swish / SiLU:** x * sigmoid(x). Self-gated; good empirical performance.

### 3.3 Backpropagation

- Compute gradients of loss w.r.t. all parameters using the chain rule.
- Forward pass: compute activations layer by layer.
- Backward pass: propagate error gradients from output to input.
- Automatic differentiation (autograd) in PyTorch/JAX handles this computationally.

### 3.4 Optimization

**Stochastic Gradient Descent (SGD):**
- Update on mini-batches rather than full dataset. Introduces noise that helps escape local minima.
- **SGD with momentum:** Accumulate exponentially decayed gradient history. Dampens oscillations.
- **Nesterov momentum:** Look-ahead gradient evaluation.

**Adaptive Methods:**
- **AdaGrad:** Per-parameter learning rates that decrease with accumulated squared gradients. Good for sparse features.
- **RMSProp:** Exponentially decayed average of squared gradients. Fixes AdaGrad's diminishing learning rates.
- **Adam:** Combines momentum and RMSProp. First and second moment estimates with bias correction. Default choice for most deep learning.
- **AdamW:** Adam with decoupled weight decay. Preferred over Adam with L2 regularization.

**Learning Rate Schedules:**
- Step decay, cosine annealing, linear warmup + decay, one-cycle policy, reduce on plateau.
- **Warmup:** Start with low LR, ramp up linearly. Critical for Transformer training.

### 3.5 Regularization

- **Dropout:** Randomly zero out activations during training with probability p. Ensemble effect.
- **Batch Normalization:** Normalize activations across the batch. Reduces internal covariate shift. Allows higher learning rates.
- **Layer Normalization:** Normalize across features (not batch). Used in Transformers.
- **Weight Decay:** Add lambda * ||w||^2 to loss. Equivalent to L2 regularization for SGD.
- **Data augmentation:** Artificial training data expansion (flips, rotations, crops, color jitter, Mixup, CutMix).
- **Early stopping:** Monitor validation loss; stop training when it increases.
- **Label smoothing:** Soften one-hot targets. Reduces overconfidence.

---

## IV. Convolutional Neural Networks (CNNs)

### 4.1 Convolution Operation

- Slide a learned kernel (filter) across input, compute dot products.
- **Parameters:** Kernel size, stride, padding (valid/same), dilation.
- **Properties:** Translation equivariance, parameter sharing, local connectivity.
- Output size: floor((input_size + 2*padding - kernel_size) / stride) + 1.

### 4.2 Pooling

- Downsample feature maps. Max pooling (most common), average pooling.
- **Global average pooling (GAP):** Reduce each feature map to a single value. Replaces fully connected layers in modern architectures.

### 4.3 Architectures (Historical Progression)

- **LeNet-5 (1998):** Pioneer architecture for digit recognition. Conv -> Pool -> Conv -> Pool -> FC.
- **AlexNet (2012):** Deep CNN with ReLU, dropout, GPU training. Won ImageNet; launched the deep learning era.
- **VGGNet (2014):** Very deep (16-19 layers) with 3x3 convolutions throughout. Simple but large.
- **GoogLeNet/Inception (2014):** Inception modules with parallel convolutions of different kernel sizes. Much more parameter-efficient.
- **ResNet (2015):** Skip connections (residual learning). Solved vanishing gradient for very deep networks (100+ layers). The single most influential architecture design.
- **DenseNet (2017):** Each layer connected to all subsequent layers. Feature reuse.
- **EfficientNet (2019):** Compound scaling (depth, width, resolution) with neural architecture search. State-of-the-art efficiency.
- **ConvNeXt (2022):** Modernized ResNet with Transformer-inspired design choices. Competitive with Vision Transformers.

### 4.4 Transfer Learning

- **Feature extraction:** Use pretrained CNN (ImageNet) as fixed feature extractor. Train only the final classifier.
- **Fine-tuning:** Unfreeze some/all pretrained layers. Lower learning rate for pretrained layers.
- Critical for medical imaging where labeled data is scarce.

---

## V. Recurrent Neural Networks

### 5.1 Vanilla RNN

- Hidden state h_t = tanh(W_hh * h_{t-1} + W_xh * x_t + b). Process sequences step by step.
- **Vanishing/exploding gradient problem:** Gradients multiplied through many timesteps.
- Gradient clipping mitigates exploding gradients; vanishing gradient requires architectural changes.

### 5.2 LSTM (Long Short-Term Memory)

- **Cell state** c_t carries information through time with minimal transformation.
- **Gates:** Forget gate (what to discard), input gate (what to add), output gate (what to expose).
- Each gate is a sigmoid layer + elementwise multiplication.
- Effectively learns long-range dependencies. The workhorse of sequence modeling before Transformers.

### 5.3 GRU (Gated Recurrent Unit)

- Simplified LSTM: combines forget and input gates into a single "update gate." No separate cell state.
- Fewer parameters than LSTM. Comparable performance in most tasks.

### 5.4 Bidirectional and Stacked RNNs

- **Bidirectional:** Two RNNs (forward + backward). Captures both past and future context.
- **Stacked:** Multiple RNN layers. Each layer's output is the next layer's input.

---

## VI. Attention and Transformers

### 6.1 Attention Mechanisms

- **Motivation:** RNNs compress entire sequence into a fixed-size vector (bottleneck). Attention lets the model "look back" at all positions.
- **Bahdanau (additive) attention:** score(s, h) = v^T tanh(W_1 s + W_2 h).
- **Luong (multiplicative) attention:** score(s, h) = s^T W h.
- **Scaled dot-product attention:** score(Q, K) = QK^T / sqrt(d_k). The Transformer's core.

### 6.2 Transformer Architecture

**Self-Attention:**
- Input projected to Query (Q), Key (K), Value (V) matrices.
- Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) V.
- Each position attends to all other positions. O(n^2) in sequence length.

**Multi-Head Attention:**
- Run h parallel attention heads with different learned projections.
- Concatenate outputs and project. Allows the model to attend to different aspects simultaneously.

**Full Transformer Block:**
- Multi-head self-attention -> Add & LayerNorm -> Feed-forward network (two linear layers + GELU) -> Add & LayerNorm.
- **Positional encoding:** Sinusoidal or learned embeddings added to input. Necessary because self-attention is permutation-invariant.

**Encoder-Decoder:**
- Encoder: stack of self-attention blocks (bidirectional).
- Decoder: masked self-attention (causal) + cross-attention to encoder outputs + feed-forward.

**Variants:**
- **Encoder-only:** BERT. Bidirectional context. Good for classification, NER, question answering.
- **Decoder-only:** GPT. Autoregressive. Good for text generation.
- **Encoder-decoder:** T5, BART. Good for sequence-to-sequence (translation, summarization).

### 6.3 Efficient Transformers

- **Linear attention:** Replace softmax attention with linear kernels. O(n) complexity.
- **Sparse attention:** Attend to local windows + global tokens (Longformer, BigBird).
- **Flash Attention:** IO-aware exact attention. Reduces memory from O(n^2) to O(n) by tiling.
- **Multi-query / Grouped-query attention (MQA/GQA):** Share K/V heads across query heads. Faster inference.

---

## VII. Generative Models

### 7.1 GANs (Generative Adversarial Networks)

- **Generator G:** Maps noise z ~ N(0, I) to data space. Goal: fool the discriminator.
- **Discriminator D:** Distinguishes real data from generated. Goal: correctly classify.
- **Minimax game:** min_G max_D E[log D(x)] + E[log(1 - D(G(z)))].
- **Training challenges:** Mode collapse, training instability, vanishing generator gradients.
- **DCGAN:** Convolutional GAN. Architectural guidelines (batch norm, no pooling, LeakyReLU in D).
- **CycleGAN:** Unpaired image-to-image translation. Cycle-consistency loss. Applications: style transfer, domain adaptation.
- **StyleGAN:** Style-based generator with adaptive instance normalization. State-of-the-art face generation.
- **Wasserstein GAN (WGAN):** Earth mover's distance. More stable training. Gradient penalty variant (WGAN-GP).

### 7.2 Diffusion Models

**Denoising Diffusion Probabilistic Models (DDPM):**
- **Forward process:** Gradually add Gaussian noise over T timesteps until data becomes pure noise.
- **Reverse process:** Learn to denoise step by step. Neural network predicts noise epsilon at each step.
- **Training:** Minimize ||epsilon - epsilon_theta(x_t, t)||^2 — predict the noise that was added.
- **Sampling:** Start from noise, iteratively denoise. Slow (many steps) but high quality.
- **DDIM:** Deterministic sampling with fewer steps.

**Score Matching:**
- Learn the score function (gradient of log probability) nabla_x log p(x).
- **Noise-conditioned score networks:** Estimate scores at multiple noise levels.
- Connection: DDPM's noise prediction is equivalent to score estimation.

**Latent Diffusion (Stable Diffusion):**
- Diffusion in the latent space of a pretrained autoencoder. Much more efficient than pixel-space diffusion.
- Conditioning via cross-attention (text embeddings from CLIP).

### 7.3 Autoencoders

**Vanilla Autoencoder:**
- Encoder maps input to bottleneck latent code; decoder reconstructs.
- Learns compressed representation. Used for denoising, anomaly detection.

**Variational Autoencoder (VAE):**
- Encoder outputs parameters of a distribution q(z|x) (typically Gaussian: mean and log-variance).
- **Reparameterization trick:** z = mu + sigma * epsilon, epsilon ~ N(0, I). Enables backprop through sampling.
- **Loss:** Reconstruction loss + KL divergence D_KL(q(z|x) || p(z)). Balances reconstruction quality and latent space regularity.

**VQ-VAE (Vector Quantized):**
- Discrete latent space. Encoder output quantized to nearest codebook vector.
- Avoids "posterior collapse" of VAEs. Combined with autoregressive priors for generation.

---

## VIII. Natural Language Processing

### 8.1 Text Preprocessing

- **Tokenization:** Word-level, subword (BPE, WordPiece, SentencePiece, Unigram), character-level.
- BPE: start with characters, iteratively merge most frequent pairs. Handles out-of-vocabulary words.
- Vocabulary size tradeoff: smaller vocab = longer sequences; larger vocab = sparse embeddings.

### 8.2 Word Embeddings

- **Word2Vec:** Skip-gram (predict context from word) and CBOW (predict word from context). Dense vectors capturing semantic relationships.
- **GloVe:** Global co-occurrence statistics. Combines count-based and predictive methods.
- **FastText:** Subword embeddings. Handles morphologically rich languages and rare words.

### 8.3 Pretrained Language Models

**BERT (Bidirectional Encoder Representations from Transformers):**
- Pretrained with masked language modeling (MLM) and next sentence prediction (NSP).
- Fine-tune for downstream tasks: classification, NER, question answering, sentence similarity.
- Variants: RoBERTa (more data, no NSP), ALBERT (parameter sharing), DeBERTa (disentangled attention).

**GPT Family:**
- Autoregressive (left-to-right) language models. Predict next token given previous tokens.
- **Scaling laws:** Performance scales as power laws with model size, data size, and compute.
- **GPT-3/4:** In-context learning (few-shot prompting) without fine-tuning.
- **Instruction tuning:** Fine-tune on instruction-following datasets (FLAN, Alpaca).
- **RLHF (Reinforcement Learning from Human Feedback):** Train a reward model from human preferences; optimize the language model with PPO against the reward model. Critical for alignment.
- **DPO (Direct Preference Optimization):** Skip the reward model; directly optimize the policy from preference data. Simpler alternative to RLHF.

---

## IX. Computer Vision

### 9.1 Object Detection

**Two-Stage Detectors:**
- **Faster R-CNN:** Region Proposal Network (RPN) proposes candidate boxes; classifier refines and classifies. Anchor boxes at multiple scales/ratios.
- High accuracy but slower inference.

**One-Stage Detectors:**
- **YOLO (You Only Look Once):** Divide image into grid; each cell predicts bounding boxes and class probabilities simultaneously. Real-time detection.
- **YOLOv5/v8:** Modern iterations with CSP backbone, PANet neck, anchor-free detection.
- **SSD:** Multi-scale feature maps for detection at different scales.

**Anchor-Free:**
- **FCOS:** Fully convolutional, predicts distances to bounding box edges per pixel.
- **DETR:** End-to-end detection with Transformers. No anchors, no NMS. Set prediction with Hungarian matching.

### 9.2 Semantic & Instance Segmentation

**Semantic Segmentation (pixel-level classification):**
- **FCN (Fully Convolutional Networks):** Replace FC layers with 1x1 convolutions. Upsampling via transposed convolutions.
- **U-Net:** Encoder-decoder with skip connections. The gold standard for medical image segmentation. Symmetric architecture preserves fine spatial details.
- **DeepLab:** Atrous (dilated) convolutions for multi-scale context. ASPP module. CRF post-processing.

**Instance Segmentation:**
- **Mask R-CNN:** Extends Faster R-CNN with a parallel mask prediction branch. Per-instance binary masks.
- **SAM (Segment Anything Model):** Foundation model for segmentation. Promptable with points, boxes, or text. Zero-shot segmentation.

### 9.3 Vision Transformers

- **ViT:** Split image into patches (e.g., 16x16), flatten and linearly embed, add position embeddings, process with standard Transformer encoder.
- Requires large-scale pretraining (ImageNet-21k or JFT-300M). With sufficient data, outperforms CNNs.
- **Swin Transformer:** Hierarchical ViT with shifted window attention. O(n) complexity. Strong backbone for detection and segmentation.
- **DINOv2:** Self-supervised ViT pretraining. Learns powerful visual features without labels.

---

## X. Medical Imaging ML

### 10.1 MRI Segmentation

- **Challenge:** Limited labeled data, high inter-rater variability, class imbalance (small structures).
- **Architectures:** U-Net and its 3D extensions (3D U-Net, V-Net with Dice loss). nnU-Net: self-configuring U-Net that adapts architecture and preprocessing to the dataset.
- **Loss functions:** Dice loss (handles class imbalance), focal loss, boundary loss, compound losses (Dice + cross-entropy).
- **Data augmentation for medical images:** Elastic deformation, intensity augmentation, random cropping, simulation-based augmentation.

### 10.2 Harmonization

- **Problem:** MRI scans from different scanners/protocols have systematic intensity and contrast differences (site effects), confounding downstream analysis.
- **Statistical methods:** ComBat (empirical Bayes batch effect correction). Assumes additive and multiplicative site effects.
- **Deep learning approaches:** CycleGAN-based domain adaptation, style transfer networks, disentangled representation learning (separate anatomy from scanner style).
- **Evaluation:** Compare downstream task performance before/after harmonization. Ensure biological variability is preserved.

### 10.3 Super-Resolution

- **Goal:** Reconstruct high-resolution images from low-resolution inputs.
- **Methods:** SRCNN, EDSR, ESRGAN (perceptual + adversarial loss for realistic textures).
- **Medical application:** Upgrade thick-slice clinical MRI to isotropic resolution. Enable volumetric analysis from anisotropic acquisitions.
- **Evaluation:** PSNR, SSIM, and downstream task performance (segmentation accuracy on super-resolved images).

### 10.4 Slice-to-Volume Reconstruction (SVR)

- **Problem:** Reconstruct a 3D volume from multiple 2D slice stacks acquired at different orientations (common in fetal MRI).
- **Pipeline:** Motion estimation (rigid/affine registration of each slice) -> Outlier rejection -> Scattered data interpolation -> Regularized reconstruction.
- **Deep learning approaches:** Learning-based motion estimation, implicit neural representations for reconstruction, self-supervised methods.
- **Key challenge:** Motion corruption, especially in fetal and neonatal imaging.

---

## XI. Reinforcement Learning

### 11.1 Framework

- **Markov Decision Process (MDP):** States S, actions A, transition probabilities P(s'|s,a), reward function R(s,a), discount factor gamma.
- **Policy pi(a|s):** Probability of taking action a in state s.
- **Value function V^pi(s):** Expected cumulative discounted reward from state s under policy pi.
- **Q-function Q^pi(s,a):** Expected return from taking action a in state s, then following pi.
- **Bellman equation:** V(s) = max_a [R(s,a) + gamma * sum_{s'} P(s'|s,a) V(s')].

### 11.2 Value-Based Methods

- **Q-Learning:** Off-policy. Update Q(s,a) toward r + gamma * max_{a'} Q(s', a'). Converges to optimal Q*.
- **Deep Q-Network (DQN):** Q-function approximated by a neural network. Experience replay + target network for stability.
- **Double DQN:** Decouple action selection and evaluation to reduce overestimation.

### 11.3 Policy Gradient Methods

- **REINFORCE:** Monte Carlo policy gradient. High variance; use baselines to reduce.
- **Actor-Critic:** Actor (policy) + Critic (value function). Critic reduces variance of policy gradient.
- **PPO (Proximal Policy Optimization):** Clipped surrogate objective prevents too-large policy updates. The default RL algorithm for LLM alignment (RLHF).
- **SAC (Soft Actor-Critic):** Maximum entropy RL. Encourages exploration. State-of-the-art for continuous control.

---

## XII. MLOps and Practical Considerations

### 12.1 Experiment Tracking

- Tools: MLflow, Weights & Biases (wandb), TensorBoard, Neptune.
- Track: hyperparameters, metrics, model checkpoints, code version, data version.
- Reproducibility: fix random seeds, log environment/dependencies, version datasets.

### 12.2 Model Serving

- **Batch inference:** Process accumulated data periodically. Simpler infrastructure.
- **Real-time inference:** Model behind an API. Latency-critical. Frameworks: TorchServe, TF Serving, Triton, ONNX Runtime.
- **Optimization:** Quantization (FP16, INT8), pruning, knowledge distillation, operator fusion.

### 12.3 Feature Stores

- Centralized repository for feature computation and serving.
- Ensures consistency between training and inference features.
- Tools: Feast, Tecton, Hopsworks.

### 12.4 Data and Model Management

- **Data versioning:** DVC, Delta Lake, LakeFS.
- **Model registry:** MLflow Model Registry, SageMaker Model Registry.
- **Monitoring:** Detect data drift (KS test, PSI), concept drift, model degradation in production.

---

## References

1. Bishop — *Pattern Recognition and Machine Learning*
2. Goodfellow, Bengio, Courville — *Deep Learning* (deeplearningbook.org)
3. Murphy — *Probabilistic Machine Learning: An Introduction* (2022) and *Advanced Topics* (2023)
4. Vaswani et al. — "Attention Is All You Need" (2017)
5. He et al. — "Deep Residual Learning for Image Recognition" (2015)
6. Ronneberger et al. — "U-Net: Convolutional Networks for Biomedical Image Segmentation" (2015)
7. Ho et al. — "Denoising Diffusion Probabilistic Models" (2020)
8. Ouyang et al. — "Training language models to follow instructions with human feedback" (2022)
9. Isensee et al. — "nnU-Net: a self-configuring method for deep learning-based biomedical image segmentation" (2021)
10. Sutton, Barto — *Reinforcement Learning: An Introduction*, 2nd ed. (free online)
11. Hugging Face documentation and model hub (huggingface.co)
