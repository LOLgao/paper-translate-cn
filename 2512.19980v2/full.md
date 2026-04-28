# Neuron-Guided Interpretation of Code LLMs: Where, Why, and How?

ZHE YIN, Shanghai Jiao Tong University, China

XIAODONG GU, Shanghai Jiao Tong University, China

BEIJUN SHEN∗, Shanghai Jiao Tong University, China

Code language models have demonstrated strong capabilities across a wide range of code intelligence tasks. While the majority of existing research prioritizes performance improvements on benchmark datasets, few of them have focused on the internal interpretability of models—how specific neurons affect linguistic features such as syntax and semantics, which is critical for model transparency, controllability, and reliability. Although various neuron interpretability techniques have been developed in NLP, directly applying them to source code yields suboptimal results due to the unique characteristics of programming languages, such as their formal structure, hierarchical organization, and executability. In this work, we empirically investigate the intrinsic mechanisms of code LLMs at the neuron level, aiming to localize both language-specific neurons (i.e., neurons that are selectively responsive to individual programming languages) and concept layers (i.e., feedforward layers that encode language-agnostic representations of code). Our study employs two state-of-the-art models, Llama-3.1-8B and Qwen2.5-Coder-32B, across five programming languages: ${ \mathrm { C } } { + } { + }$ , Java, Python, Go, and JavaScript. By analyzing neuron activation patterns in response to multilingual code inputs, we investigate the role of individual neurons and the contribution of different layers during output generation. Our empirical findings reveal that: (1) code LLMs contain neurons specialized for individual programming languages, alongside a universal subset that supports general-purpose code generation; and (2) lower layers primarily encode language-specific syntactic structures, while middle layers capture semantic abstractions that generalize across languages, manifesting as concept layers. To demonstrate the practical usability of these findings, we apply our findings to three downstream tasks: neuron-guided fine-tuning for code generation, clone detection using concept-layer embeddings, and transfer learning guided by concept-layer representations for code summarization. Experimental evaluations show that each strategy consistently improves the performance of multilingual code LLMs.

CCS Concepts: • Software and its engineering Software development techniques; • Computing methodologies Artificial intelligence.

Additional Key Words and Phrases: Programming Language-specific Neurons, Layer-wise Representations, Code Intelligence Tasks, Large Language Models

# ACM Reference Format:

Zhe Yin, Xiaodong Gu, and Beijun Shen. 2026. Neuron-Guided Interpretation of Code LLMs: Where, Why, and How?. Proc. ACM Softw. Eng. 3, FSE, Article FSE055 (July 2026), 22 pages. https://doi.org/10.1145/3797083

# 1 Introduction

Large language models (LLMs), trained on extensive code repositories, have become powerful productivity tools in software development. They demonstrate strong performance across diverse

∗Corresponding author.

Authors’ Contact Information: Zhe Yin, Shanghai Jiao Tong University, Shanghai, China, yin_zhe@sjtu.edu.cn; Xiaodong Gu, Shanghai Jiao Tong University, Shanghai, China, xiaodong.gu@sjtu.edu.cn; Beijun Shen, Shanghai Jiao Tong University, Shanghai, China, bjshen@sjtu.edu.cn.

![](images/7c60ea4ed55c93309ac1d46c6cafe47db50e3835d4a023ed40b41386058380e9.jpg)

This work is licensed under a Creative Commons Attribution 4.0 International License.

© 2026 Copyright held by the owner/author(s).

ACM 2994-970X/2026/7-ARTFSE055

https://doi.org/10.1145/3797083

code-related tasks such as code completion [16], summarization [44], translation [53], and code question answering [25]. However, current research on code LLMs primarily focuses on enhancing predictive accuracy across benchmarks, often treating the models as black boxes. For example, approximately $9 6 \%$ of studies prioritize performance improvements [21], while largely neglecting the analysis of internal decision mechanisms. This narrow emphasis leaves the inner workings of code LLMs poorly understood, which may compromise model controllability and reduce trustworthiness [12].

Recently, the interpretability of code LLMs has attracted significant attention from both academic and industrial communities. Nevertheless, substantial challenges remain that hinder a deeper and more reliable understanding of these models’ inner workings. First, the scalability and computational efficiency of existing explanation methods often fail to keep pace with the rapidly growing size and complexity of modern LLMs. Second, there is no established “ground truth” for interpretability in code models, making it difficult to objectively evaluate the accuracy and quality of explanatory outputs [60]. Third, code LLMs exhibit characteristics unique to programming languages (PLs), shaped by code syntax, control flow, and data dependencies [26]. As a result, simply transferring explainability techniques from natural language processing (NLP) frequently leads to suboptimal performance [30]. For example, the direct use of LAPE [46] proves ineffective in accurately identifying programming language-specific neurons, as demonstrated in Section 2.2. These challenges demand a novel interdisciplinary approach that integrates deep learning interpretability with principles from programming languages and coding idioms. Our goal is to shift the focus from “which tokens are important” to “how internal representations map to and manipulate underlying program structures”.

In this paper, we investigate the internal mechanisms of code LLMs to identify network regions that encode programming language-specific semantic representations and utilize these insights to improve the performance of downstream code-related tasks. Specifically, we examine code LLMs at both neuron and layer levels. RQ1 explores the models’ behavior in terms of their internal neuron activations. RQ2 examines how the model’s output is built through its feed-forward layers and pinpoints potential “concept layers” that capture abstract, language-agnostic semantics of code. Building upon these findings, RQ3 focuses on leveraging these insights to enhance performance on downstream tasks such as code generation, clone detection, and code summarization. Our study employs two publicly available LLMs, namely Llama-3.1-8B and Qwen2.5-Coder-32B, along with five popular programming languages: $\mathrm { C } { + } { + }$ , Java, Python, Go, and JavaScript.

We explore the following research questions:

• RQ1: Are there programming language-specific neurons in code LLMs?

Motivation. Language-specific neurons within a code LLM help to enhance parameterefficient fine-tuning during adaptation to a specific language by selectively freezing nonspecialized neurons.

Protocol. In this research question, we propose the Programming Language Specialization (PLS) score, a novel metric that identifies neurons specialized for individual programming languages. The PLS score evaluates a neuron’s activation strength and the gradient of the loss with respect to that activation to identify neurons critical for specific languages. We then validate the language-specificity of these neurons through ablation-based intervention.

Result. Code LLMs contain neurons specialized for individual programming languages as well as a distinct set of universal neurons critical for general code generation. Notably, these neural representations reflect the phylogenetic relationships among programming languages.

• RQ2: Are there language-agnostic concept layers in code LLMs?

Motivation. The concept layers could act as both a potent semantic hub for code embedding and a bridge for cross-lingual knowledge transfer.

Protocol. In this research question, we employ a dual-pronged analytical framework that triangulates potential concept layers by using both semantic and syntactic probes. We use Representational Similarity Analysis (RSA) [24] as a semantic probe and an Abstract Syntax Tree (AST) node prediction probe as a syntactic probe, analyzing the layer-wise representational invariance and fidelity of these two properties.

Result. Code LLMs organize knowledge hierarchically, forming concept layers in the middle layers. They exhibit maximum representational invariance to lexical and syntactic changes while simultaneously demonstrating minimum fidelity in encoding fine-grained syntactic structures.

• RQ3: How can we utilize the interpretability of code LLMs to enhance code-related tasks?

Motivation. We demonstrate the practical utility of our insights on language-specific neurons (RQ1) and the concept layers (RQ2) across multiple code-related tasks.

Protocol. In this research question, we leverage the findings from RQ1 and RQ2 to enhance three downstream software engineering tasks: code generation using neuron-guided finetuning, clone detection using concept-layer embeddings, and code summarization via conceptlayer guided transfer learning.

Result. Our findings provide empirical evidence that leveraging mechanistic insights leads to significant performance improvements across all three tasks. Specifically, neuron-guided finetuning outperforms LoRA by mitigating catastrophic forgetting, concept-layer embeddings enable effective zero-shot semantic clone detection, and concept-layer guided transfer learning facilitates superior performance on low-resource code summarization tasks.

# 2 Background and Motivation

# 2.1 LLM Interpretability

LLM Interpretability seeks to uncover the internal mechanisms, decision-making processes, and representational structures of language models, making their behavior more comprehensible, trustworthy, and controllable for humans [60]. Research in this area has evolved along several interconnected paths.

One central line of research is the probing and analysis of model representations. Probing techniques examine the information encoded within model activations, using methods such as analyzing specific attention heads [3], decoding embedded concepts [31], or applying representation engineering [56, 62]. This also includes direct logit lens-style methods that decode activations into vocabulary tokens to understand what information is represented at various layers and positions [9]. These techniques provide insights into the nuanced ways LLMs process and structure information.

Further work delves into a more granular analysis of components, aiming to interpret the function of fundamental units like neurons and attention heads. Studies have successfully mapped individual neurons to human-interpretable concepts [11, 39]. For instance, Tang et al. [46] introduced Language Activation Probability Entropy (LAPE), a metric to identify language-specific neurons by measuring the entropy of their activations across different languages. Moving beyond individual components, a growing body of research focuses on circuit-level analysis, which examines how distributed groups of neurons and heads interact to perform specific computations. For example, studies have identified circuits responsible for tasks like indirect object identification [54]. More broadly, this approach can be used for functional localization, such as pinpointing the regions responsible for

Table 1. A Preliminary Study on Llama-3.1-8B by the LAPE Technique. The cell presents the pass $@ 3$ scores for code generation after ablating neurons identified by LAPE, and their $\Delta$ relative to the baseline is shown in parentheses $( \uparrow / )$ .   

<table><tr><td rowspan="2">Ablated Neuron Set</td><td rowspan="2"># Neurons</td><td colspan="8">Code Generation Performance on the Target Language</td></tr><tr><td>C++ (%)</td><td>Java (%)</td><td>Python (%)</td><td>Go (%)</td><td colspan="4">JavaScript (%)</td></tr><tr><td colspan="2">Baseline (No Ablation)</td><td>47.56</td><td>49.39</td><td>46.34</td><td>34.76</td><td colspan="4">40.85</td></tr><tr><td>C++ Specific</td><td>2,549 (0.186%)</td><td>45.85 (-3.6%)</td><td>46.53 (-5.8%)</td><td>48.47 (+4.6%)</td><td>33.86 (-2.6%)</td><td colspan="4">43.34 (+6.1%)</td></tr><tr><td>Java Specific</td><td>1,693 (0.124%)</td><td>44.99 (-5.4%)</td><td>51.51 (+4.3%)</td><td>47.78 (+3.1%)</td><td>33.86 (-2.6%)</td><td colspan="4">49.51 (+21.2%)</td></tr><tr><td>Python Specific</td><td>2,752 (0.201%)</td><td>39.05 (-17.9%)</td><td>39.36 (-20.3%)</td><td>42.77 (-7.7%)</td><td>29.41 (-15.4%)</td><td colspan="4">26.00 (-36.4%)</td></tr><tr><td>Go Specific</td><td>1,260 (0.092%)</td><td>40.76 (-14.3%)</td><td>45.09 (-8.7%)</td><td>47.04 (+1.5%)</td><td>33.86 (-2.6%)</td><td colspan="4">48.28 (+18.2%)</td></tr><tr><td>JavaScript Specific</td><td>1,994 (0.146%)</td><td>44.18 (-7.1%)</td><td>44.40 (-10.1%)</td><td>41.38 (-10.7%)</td><td>31.18 (-10.3%)</td><td colspan="4">47.06 (+15.2%)</td></tr><tr><td>Language Agnostic</td><td>14,304 (1.044%)</td><td>0.00(-100.0%)</td><td>0.00(-100.0%)</td><td>0.00(-100.0%)</td><td>0.00(-100.0%)</td><td colspan="4">0.00(-100.0%)</td></tr></table>

storing factual knowledge [5], without necessarily providing a complete explanation of the entire underlying circuit, as demonstrated by Merullo et al. [29].

# 2.2 Motivation

While various interpretability techniques have been proposed for general LLMs, directly applying them to code LLMs is often impractical due to the unique characteristics of code in programming languages [30]. Unlike natural language, programming languages often share common constructs, such as loops (‘for’, ‘while’), which may cause entropy-based measures to misclassify neurons representing these shared concepts as language-agnostic. In addition, lexical and sub-token overlaps (e.g., variable names and operators) across languages can bias entropy calculation by existing techniques.

To verify this challenge, we conduct a preliminary study using LAPE [46], an interpretability technique for natural languages, to analyze code LLMs. LAPE identifies a small and variable set of neurons per language, representing only a minor portion of the model’s total capacity. We apply LAPE to Llama-3.1-8B across five programming languages: $\mathrm { C } { + } { + }$ , Java, Python, Go, and JavaScript. As shown in the left part of Table 1, the detected language-specific neurons collectively comprise just $0 . 7 5 \%$ of all neurons. To validate these neurons, we deactivate the subsets associated with each language and assess their impact on code generation. Performance is evaluated on the HumanEval-X [61] benchmark with the pass@3 metric. The results, presented in the right part of Table 1, show that these ablations do not consistently degrade performance in the intended language and sometimes even enhance performance in others. This inconsistency suggests that the neurons highlighted by LAPE are not reliably language-specific. Supporting this observation, recent work [22] likewise finds that isolating neurons exclusive to a single language is particularly challenging, especially for closely related languages such as Java and $\mathrm { C } { + } { + }$ .

These factors motivate our study methodology to explain code LLMs by integrating deep learning interpretability with the inherent properties of programming languages.

# 3 Experimental Setup

We investigate the intrinsic mechanisms of code LLMs to understand how individual neurons influence linguistic features. In this section, we discuss the models and programming languages used for our experiments.

# 3.1 Language Models under Study

Our investigation is conducted on two publicly available LLMs: Llama-3.1-8B [6] and Qwen2.5- Coder-32B [18]. Llama-3.1 is a foundational model pre-trained on both broad text and code corpora, whereas Qwen2.5-Coder is a code-specialized model trained exclusively on over 3 trillion high-quality code tokens. Both are autoregressive and decoder-only transformers. We use the 8B version of Llama-3.1 ( ${ \sim } 1 . 5 { \mathrm { M } }$ neurons) as a lightweight backbone suitable for fine-tuning. For Qwen2.5-Coder, we select the 32B variant $\mathord { \left. \sim \right.} 4 . 8 M $ neurons) to examine a larger-scale model. We utilize only the base versions of each model, avoiding confounding effects from post-training alignment techniques such as RLHF. This enables a direct and unbiased analysis of the knowledge and architectural properties intrinsically acquired during pre-training.

# 3.2 Selected Programming Languages

Our study examines five widely adopted programming languages, including $\mathrm { C } { + } { + }$ , Java, Python, Go, and JavaScript, selected for their significant industry presence and distinct linguistic features. The set includes both statically-typed $( \mathrm { C } + +$ , Java, Go) and dynamically-typed (Python, JavaScript) languages, supporting various paradigms such as object-oriented, procedural, and scripting. It also spans different execution models, from compiled languages with manual memory management $\left( \mathbf { C } + + \mathbf { \right) }$ to interpreted or JIT-compiled languages with garbage collection (Python, JavaScript, Go). This diversity provides a comprehensive foundation for evaluating how code LLMs comprehend, distinguish, and generalize across different programming languages.

# 3.3 Implementation Details

All experiments are conducted within a standardized software and hardware environment to ensure reproducibility. We utilize the HuggingFace transformers [57] (v4.43.0) and PyTorch [35] (v2.3.0) libraries. The experimental platform is a workstation equipped with two NVIDIA GeForce RTX 4090 GPUs, running on CUDA 12.2. All base models are loaded directly from the Hugging Face Hub. To optimize for computational efficiency and memory usage, all training and inference operations are performed using the torch.bfloat16 mixed-precision format.

For all fine-tuning tasks, we adopt a consistent training configuration unless otherwise specified. We employ the AdamW optimizer [27] with a learning rate of $5 \times 1 0 ^ { - 5 }$ and a linear scheduler featuring a $1 0 \%$ warm-up phase. We use a maximum sequence length of 1,024 tokens and a perdevice batch size of 4, with gradient accumulation over 2 steps to achieve an effective batch size of 16. A fixed random seed of 42 is used across all experiments to ensure deterministic outcomes. The specific hyperparameters for each downstream task, such as the number of epochs and the exact fine-tuning strategy, are detailed in Section 6.

# 4 RQ1: Identifying Programming Language-Specific Neurons

In this study, we investigate neuron activations in response to multilingual code inputs and analyze the distribution of programming language-specific neurons in code LLMs.

# 4.1 Study Design

To address the limitations of NL-oriented measures like LAPE, we introduce the Programming Language Specialization (PLS) score, a novel metric that identifies programming language-specific neurons. The PLS evaluates both a neuron’s activation strength and the gradient of the loss with respect to its activation, distinguishing neurons activated by linguistic features from those that are functionally essential for accurate language generation. The analysis framework, shown in Figure 1, consists of two main stages: (1) identifying language-specific neurons using PLS scoring,

![](images/91012ccf861a3c56863625c9b0923fbc9fd0711b39e83ed0ee03b715a4de9960.jpg)

![](images/e270f87f06ac2bb7106204418752bb14e7b7e126d9e17155dfb85b406cfcfe03.jpg)  
Fig. 1. The Overall Structure of Our Analysis Framework for Language-Specific Neurons.

and (2) evaluating the influence of these neurons by ablating their activations and measuring the resulting change in model performance. Each stage is described in detail in the following sections.

4.1.1 Probing Language-Specific Neurons. We employ gradient-based attribution methods [43, 45] to evaluate a feature’s importance by multiplying its activation with the loss gradient. Extending this approach to internal neuron activations, we quantify each neuron’s contribution to model predictions.

For a neuron ?? and an input code sample ??, let $a _ { n } ( s )$ denote its activation. The gradient of the sequence-level cross-entropy loss $\mathcal { L } ( s )$ with respect to this activation is $\nabla _ { a _ { n } ( s ) } \mathcal { L } ( s )$ , where the loss is defined as:

$$
\mathcal {L} (s) = - \sum_ {t = 1} ^ {T} \log p _ {\theta} \left(x _ {t} \mid x _ {<   t}\right), \tag {1}
$$

with $( x _ { 1 } , \ldots , x _ { T } )$ representing the ground-truth token sequence and $\scriptstyle { \mathcal { P } } \theta$ the model’s predictive distribution.

The PLS score of neuron $n$ for language $L$ is defined as the expectation over language-specific samples $s \in D _ { L }$ of the product of the absolute activation and the absolute gradient:

$$
\operatorname {P L S} (n, L) = \mathbb {E} _ {s \in D _ {L}} \left[ | a _ {n} (s) | \cdot \left| \nabla_ {a _ {n} (s)} \mathcal {L} (s) \right| \right], \tag {2}
$$

where the expectation is taken over code samples ?? in the language-specific dataset $D _ { L }$

Language-specific neurons are identified through the following three-step procedure:

(1) Candidate Filtering. A neuron $n$ is considered a candidate if its PLS score exceeds a predefined threshold in at least one language. Neurons with uniformly low scores are discarded.   
(2) Specificity Verification. For each candidate, let $L ^ { * }$ be the language with the highest PLS score:

$$
L ^ {*} = \arg \max  _ {L _ {i} \in \mathbb {L}} \operatorname {P L S} (n, L _ {i}). \tag {3}
$$

A neuron is considered language-specific if this score is at least 1.5 times greater than the second-highest score, balancing precision and coverage.

(3) Ranking and Selection. Neurons are ranked by their maximal PLS score, and the top $1 \%$ are classified as language-specialized, each attributed to its corresponding $L ^ { * }$ .

This procedure yields a final set of neurons that are both highly responsive and influential for the model’s predictions, while being clearly specific to individual programming languages.

4.1.2 Validating Language-Specific Neurons. We adopt a standard ablation-based intervention protocol [5] to validate the identified language-specific neurons in code generation. It involves perturbing neuron activations and assessing the impact on the quality of the generated code:

(1) Intervention: During the forward pass for a code generation task, we ablate a previously identified set of specialized neurons (e.g., those for Python) by setting their activation values to zero immediately after computation. This intervention, applied within their respective neural modules (both self-attention and feed-forward layers), nullifies their contribution to subsequent layers and the final output.   
(2) Evaluation: We evaluate the model’s performance on the HumanEval-X [61] benchmark, a multilingual dataset for assessing cross-lingual code synthesis. For each problem, the model generates three candidate solutions, and performance is quantified using the pass $@ 3$ metric, which measures the probability that at least one of the three solutions passes all unit tests.

We compare the results of ablation guided by our proposed PLS scores with random ablation using an equal number of neurons. A sharp performance decline in the target language, with minimal impact on other languages, suggests high accuracy in identifying language-specific neurons.

# 4.2 Results

We apply the PLS technique to the studied models and identify specialized sets of neurons for $\mathrm { C } { + } { + }$ , Java, Python, Go, and JavaScript, along with a language-agnostic neuron set that exhibits high activation across all languages. The distribution of language-specific neurons is summarized in Table 2. Notably, these language-specific neurons account for less than $0 . 7 \%$ of the total in Llama-3.1-8B and $0 . 5 \%$ in Qwen2.5-Coder-32B. The results also reveal a significant quantitative imbalance across languages. For example, in Llama-3.1-8B, the number of Python-specific neurons (4,656) is more than 14 times greater than that of Go-specific neurons (315). This imbalance occurs because PLS relies on aggregated activation values and their gradient-based attribution. Languages that trigger stronger model activations, such as Python, receive more highly attributed neurons.

Table 2 presents the code generation performance after deactivating the language-specific neurons identified by PLS. A sharp performance decline is observed in the ablated language, with minimal impact on others. Compared to LAPE (Table 1), PLS demonstrates higher accuracy in pinpointing language-specific neurons. For instance, in Llama-3.1-8B, ablating Python-specific neurons identified by PLS leads to a performance drop of $8 2 . 9 \%$ , whereas LAPE-based ablation results in only a $7 . 7 \%$ decrease. The gap is even more pronounced for $\mathrm { C } { + } { + }$ : PLS-driven ablation causes an $8 5 . 9 \%$ decline, compared to a negligible $3 . 6 \%$ decrease with LAPE. These results confirm the importance of causal-based analysis, demonstrating that purely correlation-driven metrics like LAPE are insufficient for this task.

Additionally, the PLS method demonstrates both computational efficiency and scalability, yielding consistent results across models of varying sizes, such as the smaller Llama-3.1-8B and the larger Qwen2.5-Coder-32B. Despite the substantial difference in model size, PLS remains effective in identifying language-specific neurons, indicating its ability to handle the complexities inherent in models of different scales.

Beyond superior accuracy, the neurons identified by PLS also exhibit remarkable functional specificity. For instance, ablating the Go-specific neuron set induces a performance collapse of $8 7 . 8 \%$ (Llama-3.1-8B) and $9 4 . 0 \%$ (Qwen2.5-Coder-32B) for Go (e.g., from $3 4 . 7 6 \%$ to $4 . 2 7 \%$ in Llama-3.1-8B), yet has a negligible impact on Python’s performance. This targeted effect stands in stark contrast to the generalized degradation from random ablation. Furthermore, ablating the language-agnostic neuron set incapacitates the model entirely, reducing performance to $0 . 0 0 \%$ across all languages and confirming their foundational role in encoding universal programming constructs.

Table 2. Code Generation Performance after Ablating PLS-Identified Neurons (HumanEval-X). The percentage change $( \Delta \% )$ relative to the baseline is shown in parentheses $( \uparrow / \downarrow )$ .   

<table><tr><td rowspan="2">Ablated Neuron Set</td><td rowspan="2"># Neurons</td><td rowspan="2">Ablating Method</td><td colspan="6">Code Generation Performance on the Target Language</td></tr><tr><td>C++ (%)</td><td>Java (%)</td><td>Python (%)</td><td>Go (%)</td><td>JavaScript (%)</td><td></td></tr><tr><td colspan="9">LLAMA-3.1-8B</td></tr><tr><td colspan="2">Baseline (No Ablation)</td><td>-</td><td>47.56</td><td>49.39</td><td>46.34</td><td>34.76</td><td>40.85</td><td></td></tr><tr><td rowspan="2">C++ Specific</td><td rowspan="2">2,290 (0.167%)</td><td>PLS</td><td>6.71 (-85.9%)</td><td>31.71 (-35.8%)</td><td>48.17 (+3.9%)</td><td>25.00 (-28.1%)</td><td>31.10 (-23.9%)</td><td></td></tr><tr><td>Random</td><td>31.10 (-34.6%)</td><td>42.07 (-14.8%)</td><td>36.59 (-21.0%)</td><td>24.39 (-29.8%)</td><td>25.00 (-38.8%)</td><td></td></tr><tr><td rowspan="2">Java Specific</td><td rowspan="2">1,008 (0.074%)</td><td>PLS</td><td>43.29 (-9.0%)</td><td>27.44 (-44.4%)</td><td>45.12 (-2.6%)</td><td>35.32 (+1.6%)</td><td>45.73 (+11.9%)</td><td></td></tr><tr><td>Random</td><td>35.98 (-24.3%)</td><td>51.22 (+3.7%)</td><td>45.73 (-1.3%)</td><td>27.44 (-21.1%)</td><td>36.59 (-10.4%)</td><td></td></tr><tr><td rowspan="2">Python Specific</td><td rowspan="2">4,656 (0.340%)</td><td>PLS</td><td>29.26 (-38.5%)</td><td>36.58 (-25.9%)</td><td>7.93 (-82.9%)</td><td>26.83 (-22.8%)</td><td>9.15 (-77.6%)</td><td></td></tr><tr><td>Random</td><td>36.59 (-23.1%)</td><td>40.24 (-18.5%)</td><td>37.80 (-18.4%)</td><td>31.10 (-10.5%)</td><td>37.20 (-8.9%)</td><td></td></tr><tr><td rowspan="2">Go Specific</td><td rowspan="2">315 (0.023%)</td><td>PLS</td><td>38.41 (-19.2%)</td><td>49.39 (+0.0%)</td><td>44.51 (-3.9%)</td><td>4.27 (-87.7%)</td><td>43.90 (+7.5%)</td><td></td></tr><tr><td>Random</td><td>42.68 (-10.3%)</td><td>53.66 (+8.6%)</td><td>48.17 (+3.9%)</td><td>32.93 (-5.3%)</td><td>42.68 (+4.5%)</td><td></td></tr><tr><td rowspan="2">JavaScript Specific</td><td rowspan="2">1,148 (0.084%)</td><td>PLS</td><td>41.46 (-12.8%)</td><td>50.61 (+2.5%)</td><td>50.00 (+7.9%)</td><td>35.98 (+3.5%)</td><td>23.17 (-43.3%)</td><td></td></tr><tr><td>Random</td><td>45.12 (-5.1%)</td><td>52.44 (+6.2%)</td><td>46.95 (+1.3%)</td><td>36.59 (+5.3%)</td><td>40.24 (-1.5%)</td><td></td></tr><tr><td rowspan="2">Language Agnostic</td><td rowspan="2">12,087 (0.882%)</td><td>PLS</td><td>0.00 (-100.0%)</td><td>0.00 (-100.0%)</td><td>0.00 (-100.0%)</td><td>0.00 (-100.0%)</td><td>0.00 (-100.0%)</td><td></td></tr><tr><td>Random</td><td>14.64 (-69.2%)</td><td>16.47 (-66.7%)</td><td>21.34 (-53.9%)</td><td>7.95 (-77.1%)</td><td>12.36 (-69.7%)</td><td></td></tr><tr><td colspan="9">QWEN2.5-CODER-32B</td></tr><tr><td colspan="2">Baseline (No Ablation)</td><td>-</td><td>79.27</td><td>76.83</td><td>76.83</td><td>71.34</td><td>98.17</td><td></td></tr><tr><td rowspan="2">C++ Specific</td><td rowspan="2">1,931 (0.042%)</td><td>PLS</td><td>40.24 (-49.2%)</td><td>58.54 (-23.8%)</td><td>68.90 (-10.3%)</td><td>59.15 (-17.1%)</td><td>85.37 (-13.0%)</td><td></td></tr><tr><td>Random</td><td>73.17 (-7.7%)</td><td>76.22 (-0.8%)</td><td>77.44 (+0.8%)</td><td>70.73 (-0.9%)</td><td>97.56 (-0.6%)</td><td></td></tr><tr><td rowspan="2">Java Specific</td><td rowspan="2">1,809 (0.039%)</td><td>PLS</td><td>74.39 (-6.2%)</td><td>40.24 (-47.6%)</td><td>73.17 (-4.8%)</td><td>62.20 (-12.8%)</td><td>98.17 (+0.0%)</td><td></td></tr><tr><td>Random</td><td>79.88 (+0.8%)</td><td>71.95 (-6.4%)</td><td>75.61 (-1.6%)</td><td>71.95 (+0.9%)</td><td>97.56 (-0.6%)</td><td></td></tr><tr><td rowspan="2">Python Specific</td><td rowspan="2">9,400 (0.205%)</td><td>PLS</td><td>75.00 (-5.4%)</td><td>60.78 (-20.9%)</td><td>43.90 (-42.9%)</td><td>68.29 (-4.3%)</td><td>96.95 (-1.2%)</td><td></td></tr><tr><td>Random</td><td>64.02 (-19.2%)</td><td>59.76 (-22.2%)</td><td>54.88 (-28.6%)</td><td>51.83 (-27.3%)</td><td>82.32 (-16.1%)</td><td></td></tr><tr><td rowspan="2">Go Specific</td><td rowspan="2">6,110 (0.133%)</td><td>PLS</td><td>75.61 (-4.6%)</td><td>66.46 (-13.5%)</td><td>71.34 (-7.1%)</td><td>4.27 (-94.0%)</td><td>92.07 (-6.2%)</td><td></td></tr><tr><td>Random</td><td>70.12 (-11.5%)</td><td>65.85 (-14.3%)</td><td>67.07 (-12.7%)</td><td>57.98 (-18.7%)</td><td>88.41 (-9.9%)</td><td></td></tr><tr><td rowspan="2">JavaScript Specific</td><td rowspan="2">1,463 (0.032%)</td><td>PLS</td><td>71.34 (-10.0%)</td><td>74.39 (-3.2%)</td><td>67.68 (-11.9%)</td><td>70.12 (-1.7%)</td><td>79.87 (-18.6%)</td><td></td></tr><tr><td>Random</td><td>78.66 (-0.8%)</td><td>77.44 (+0.8%)</td><td>76.83 (+0.0%)</td><td>70.73 (-0.9%)</td><td>94.51 (-3.7%)</td><td></td></tr><tr><td rowspan="2">Language Agnostic</td><td rowspan="2">27,086 (0.589%)</td><td>PLS</td><td>0.00 (-100.0%)</td><td>0.00 (-100.0%)</td><td>0.00 (-100.0%)</td><td>0.00 (-100.0%)</td><td>0.00 (-100.0%)</td><td></td></tr><tr><td>Random</td><td>25.61 (-67.7%)</td><td>28.05 (-63.5%)</td><td>30.49 (-60.3%)</td><td>21.95 (-69.2%)</td><td>50.00 (-49.1%)</td><td></td></tr></table>

Ablation experiments reveal complex patterns of collateral performance degradation, often corresponding to the phylogenetic relationships between languages. A consistent, though asymmetric, relationship is observed between $\mathrm { C } { + } { + }$ and Java, which share C-style syntax. Ablating $\mathrm { C } { + } { + }$ -specific neurons results in a significant performance drop in Java, with reductions of $3 5 . 8 \%$ for Llama-3.1-8B and $2 3 . 6 \%$ for Qwen2.5-Coder-32B. This indicates that both models capture a shared neural representation reflecting the syntactic similarities between these languages, with $\mathrm { C } { + } { + }$ -specific neurons having a more pronounced effect on Java performance.

A more pronounced, yet model-dependent, interaction is observed between Python and JavaScript, two dynamically-typed scripting languages. For Llama-3.1-8B, ablating Python-specific neurons results in a substantial $7 7 . 6 \%$ decline in JavaScript performance, whereas for Qwen2.5-Coder-32B, the impact remains negligible. This stark divergence suggests that the models encode these languages in fundamentally different ways. Moreover, in Llama-3.1-8B, this relationship is further complicated as ablating JavaScript-specific neurons unexpectedly enhances Python performance, implying a complex inhibitory or competitive dynamic rather than a simple feature-sharing mechanism. These discrepancies are likely attributable to variations in model architectures or the different emphasis placed on certain aspects of the training data.

Finding 1: Code LLMs possess a small proportion of neurons specialized for individual programming languages (less than $0 . 7 \%$ ), as well as a language-agnostic set (less than $0 . 9 \%$ ) that exhibits strong causal influence across all languages.

# 5 RQ2: Characterizing Layer-wise Functional Specialization

Having identified language-specific neurons, we further investigate whether code LLMs exhibit language-agnostic “concept layers” that encode abstract, language-agnostic representations of code. These identified concept layers could serve as potent semantic hubs for code embedding and a bridge for cross-lingual knowledge transfer. We focus on examining the feed-forward layers of the Transformer model. Previous studies in NLP [20, 48, 51] have shown that feed-forward networks (FFNs) function as key memory components in LLMs, developing a feature hierarchy that transitions from surface-level syntax in lower layers to more abstract semantics in higher layers.

# 5.1 Study Design

We introduce a dual-pronged analytical framework to identify candidate concept layers using complementary semantic and syntactic probes. First, we apply Representational Similarity Analysis (RSA) [24] as a semantic probe to measure the invariance of layer-wise representations to both lexical variations and syntactic changes, a key indicator of abstraction. Second, we deploy a syntactic probe based on AST node prediction to track how grammatical structures are encoded across layers. The expectation is that a genuine concept layer should exhibit high semantic invariance while simultaneously demonstrating reduced sensitivity to fine-grained syntactic details.

5.1.1 Probing Semantic Abstraction. We apply RSA to investigate semantic abstraction in code LLMs on the HumanEval-X [61] benchmark. RSA enables the identification of concept layers by analyzing the representational geometry across model layers. The core premise is that a concept layer should capture semantic equivalence: code snippets with the same functionality should map to similar representations, even if they differ in surface form (e.g., variable names or syntactic structures).

To probe this property, we design two controlled experiments targeting distinct types of code modification. By examining whether certain layers exhibit consistent representations under these variations, we can identify which layers serve as candidates for semantic abstraction in code LLMs.

The first experiment tests intra-lingual invariance to lexical changes, evaluating whether the model remains unaffected by superficial identifier alterations within a single programming language. The ability to ignore such trivial differences is essential for genuine semantic understanding. If a representation changes significantly due solely to variable renaming, it suggests a failure to capture the underlying algorithmic logic. For each original function $F _ { \mathrm { o r i g } }$ , we generate a semantically equivalent version $F _ { \mathrm { a n o n } }$ by replacing all user-defined identifiers with random strings. Concretely, we only rename user-defined variables (e.g., local variables, parameters, and fields), leaving language keywords and library symbols unchanged. Each identifier is substituted with a short random alphanumeric string of length 2–7 to avoid introducing out-of-distribution naming patterns. After renaming, we execute the original HumanEval-X unit tests and retain only functions that pass all test cases, ensuring that $F _ { \mathrm { o r i g } }$ and $F _ { \mathrm { a n o n } }$ are both syntactically valid and behaviorally equivalent. We then measure the representational similarity between each $( F _ { \mathrm { o r i g } } , F _ { \mathrm { a n o n } } )$ pair.

The second experiment evaluates cross-lingual equivalence under syntactic changes, directly probing the existence of language-agnostic concept layers by assessing representational invariance across major syntactic variations. By measuring the similarity between semantically equivalent functions written in different languages (e.g., Python and Java), we gauge the model’s capacity

to look beyond divergent grammars, keywords, and type systems. High similarity here would strongly indicate that the model captures an abstract algorithmic core, independent of its syntactic expression. We use the parallel corpus of the HumanEval-X benchmark to compare function pairs that solve the same problem in different languages (e.g., $( F _ { \mathrm { p y t h o n } } , F _ { \mathrm { j a v a } } ) _ { \mathrm { . } }$ ).

For both experiments, the following steps are performed to quantify layer-wise representational similarity:

(1) Representation Extraction: Each code snippet is processed by a frozen model. For each transformer layer, we extract the final hidden-state vector for every input token.   
(2) Embedding Aggregation: To obtain a single vector representation of the entire code snippet at a specific layer, mean pooling is applied over the sequence of token vectors. This standard aggregation method produces a fixed-size embedding $V _ { l } ( s )$ for a snippet ?? at layer ?? .   
(3) Similarity Quantification: We compute the similarity between the representations of two code snippets, $s _ { A }$ and $s _ { B }$ , at each layer using cosine similarity, which measures the angular closeness between embedding vectors. For a given pair, the layer-wise similarity is defined as:

$$
\operatorname {S i m} \left(V _ {l} \left(s _ {A}\right), V _ {l} \left(s _ {B}\right)\right) = \frac {V _ {l} \left(s _ {A}\right) \cdot V _ {l} \left(s _ {B}\right)}{\left| V _ {l} \left(s _ {A}\right) \right| \left| V _ {l} \left(s _ {B}\right) \right|}. \tag {4}
$$

These similarity scores are averaged across all code pairs. The resulting intra-lingual invariance score quantifies the model’s robustness to superficial lexical variations, while the cross-lingual equivalence score evaluates the degree of abstraction from specific syntactic structures. Together, these metrics provide a quantitative foundation for assessing the formation of semantic concept layers across the model’s depth.

5.1.2 Probing Syntactic Structure. Along with the semantic probe, a syntactic probe is deployed to map the layer-wise encoding of grammatical structure. This analysis delineates the boundaries of potential concept layers by identifying where the model’s focus shifts from syntactic processing to semantic abstraction. To this end, we adapt established NLP probing techniques, using supervised classifiers to detect syntactic structures by predicting linguistic properties from hidden states [14]. Specifically, we use a linear classifier to ensure that the probe primarily surfaces information encoded in the representations, rather than relying on its capacity to learn the task. Prior work [13, 36] shows that high classification accuracy with a linear probe indicates that syntactic information is linearly separable in the LLM’s representation space, demonstrating the model’s ability to organize such structure.

The following steps are performed to quantify the degree to which syntactic information is explicitly encoded at each layer:

(1) Data Preparation: Each code sample from the HumanEval-X dataset is parsed into its corresponding AST.   
(2) Token-to-Node Alignment: A labeled dataset is constructed by identifying the corresponding AST node for each token in an input snippet. This step creates training instances where the input feature is the token’s hidden-state vector from a given layer, and the target label is its associated AST node type (e.g., FunctionDef, ForStmt, BinOp).   
(3) Layer-wise Probe Training: For each transformer layer of the frozen model, a linear classifier (multinomial logistic regression) is trained. The underlying model weights are held constant; only the probe’s parameters are updated. The probe aims to predict the AST node type from a single token’s hidden-state vector at that layer.   
(4) Evaluation: The performance of each layer-specific probe is evaluated using classification accuracy on a held-out test set. This step yields an accuracy score for each layer, generating a curve that illustrates the prominence of syntactic information across the model’s depth.

![](images/d65fe3e8a1b34d21057109a82574dff77166db55dbfe4914d74d3d242ebdd12f.jpg)  
(a) Llama-3.1-8B

![](images/1290d4293644cea9d787d8579b30745ba82cbf6e67d576d989206c62119d44b6.jpg)  
(b) Qwen2.5-Coder-32B

![](images/8c3bdc82e4e08ae2eec43668f3a4ad3e973635bf218304e60caa2c0cb0188cf6.jpg)  
Fig. 2. Intra-lingual Semantic Invariance Under Lexical Variations across Model Layers.   
(a) Llama-3.1-8B

![](images/4728f716df867b56ba67580c39d7b1ef6d24657128d759323deb4365a979b82c.jpg)  
(b) Qwen2.5-Coder-32B   
Fig. 3. Cross-lingual Semantic Equivalence under Syntactic Variations across Model Layers.

# 5.2 Results

We apply both a semantic probe with RSA and a syntactic probe with AST node prediction to measure how invariant layer-wise representations are to lexical and syntactic changes. We refer to concept layers as regions of layers that jointly satisfy two criteria: (i) they exhibit high semantic invariance under both intra-lingual and cross-lingual transformations, and (ii) they have low syntactic decodability, meaning that fine-grained syntactic details are no longer linearly recoverable. We next summarize how these two probes jointly reveal such layers.

Results of Semantic Abstraction Probing. Figure 2 shows intra-lingual invariance under lexical variations, measured by the cosine similarity between original and variable-renamed code representations. In Llama-3.1-8B, similarity is highest in a band of middle layers roughly spanning layers 8–15, while in Qwen2.5-Coder-32B it remains consistently high across layers 31–43. These bands indicate that the corresponding layers are robust to identifier changes within each language.

Figure 3 illustrates cross-lingual semantic equivalence under syntactic variations, showing the average cosine similarity between representations of the same algorithm implemented in different languages. Again, both models reach their highest, or near-highest, similarity in intermediate layers: layers 8–15 for Llama-3.1-8B and a broader plateau across layers 31–43 for Qwen2.5-Coder-32B. While some curves peak slightly earlier or decay slowly, these ranges correspond to contiguous regions where semantic similarity is stably high across languages rather than to a single sharp

![](images/57414e20ab3d13712f98504ed52f7def759bd6d0af19a33263d9a2dbf58900b7.jpg)  
(a) Llama-3.1-8B

![](images/a342f9bc5ab9c45dedcb4c85d3c66cd6bf760570b54b87ee65e9172627f27ff7.jpg)  
(b) Qwen2.5-Coder-32B   
Fig. 4. Accuracy of AST Node Prediction across Model Layers.

maximum. This suggests that these layers encode language-agnostic, algorithm-level structure that abstracts away from surface lexical and syntactic choices.

Overall, the semantic probes indicate that the middle layers of both models develop languageagnostic representations that capture essential algorithmic logic while largely ignoring superficial variations.

Results of Syntactic Structure Probing. The decodability of explicit syntactic information follows a distinct U-shaped curve for both models, as shown in Figure 4. The accuracy of AST node prediction is highest in the earliest layers, indicating that lower layers are strongly syntaxdominated and perform surface-level parsing. Performance then declines sharply, reaching its lowest point around layer 9 in Llama-3.1-8B and layer 36 in Qwen2.5-Coder-32B. This decline suggests that fine-grained syntactic features become less linearly separable and are encoded more abstractly in middle layers. Finally, accuracy recovers consistently in higher layers, consistent with the models’ need to reconstruct syntactically valid output during code generation.

Taken together, Figures 2–4 reveal an inverse relationship between semantic abstraction and syntactic fidelity across layers. Early layers combine relatively high semantic similarity with high AST prediction accuracy, reflecting strong surface-syntax encoding. In contrast, the middle layers are the first region where high semantic similarity coincides with minimal syntactic decodability, and we therefore designate these bands as the concept-layer regions of the models. Finally, upper layers recover syntactic information needed for generation, causing AST accuracy to rise again while semantic similarity gradually decreases.

More concretely, the convergence of peak (or near-peak) semantic similarity and minimum syntactic decodability delineates the concept layers. For example, in Llama-3.1-8B, the syntactic accuracy minimum at layer 9 falls within the semantic similarity band observed between layers 8 and 15. Similarly, in Qwen2.5-Coder-32B, the syntactic minimum at layer 36 lies inside the semantic plateau spanning layers 31 to 43. We therefore treat these intervals as approximate concept-layer regions where code is transformed into a universal, logic-centered representation before being converted back into language-specific syntactic structures in subsequent layers.

Finding 2: Code language models organize knowledge hierarchically, forming distinct “concept layers” in their middle layers. Two complementary properties characterize these layers: they show peak invariance to lexical and syntactic variations, yet minimal retention of fine-grained syntactic details.

Table 3. Summary of Enhancement Techniques for RQ3 Tasks   

<table><tr><td>Task</td><td>Enhancement Technique</td></tr><tr><td>Code Generation</td><td>Neuron-Guided Fine-Tuning</td></tr><tr><td>Code Clone Detection</td><td>Concept-Layer Embeddings (Zero-shot)</td></tr><tr><td>Code Summarization</td><td>Concept-Layer Guided Transfer Learning</td></tr></table>

# 6 RQ3: Implications for Downstream Code-related Tasks

To validate our findings and demonstrate the practical applicability of language-specific neurons (RQ1) and concept layers (RQ2) in software engineering, we design and conduct a series of targeted experiments across three code-related tasks: code generation, clone detection, and code summarization, as summarized in Table 3.

• RQ3.1 Does a mechanistically-informed, neuron-guided fine-tuning strategy outperform LoRA for code generation in terms of both task performance and knowledge retention? (Section 6.1)   
• RQ3.2 Are the language-agnostic representations extracted directly from the concept layers effective for zero-shot code clone detection? (Section 6.2)   
• RQ3.3 Can the concept layers facilitate effective cross-lingual transfer learning for code summarization, improving performance on low-resource languages? (Section 6.3)

Our approach moves beyond treating the LLM as an opaque “black box”, instead adopting a neuron-based mechanistic intervention strategy.

# 6.1 Neuron-Guided Fine-Tuning for Code Generation

6.1.1 Study Design. Parameter-efficient fine-tuning (PEFT) methods like LoRA are effective but typically modify a broad set of parameters without considering their functional roles. This may lead to suboptimal performance and catastrophic forgetting, where the model loses proficiency in previously learned tasks after fine-tuning [23]. A more targeted, mechanistic fine-tuning approach can address these issues by preserving prior knowledge while improving target task performance.

In code generation, effective adaptation requires learning the syntactic structures and conventions of the target programming language. Based on our findings of language-specific neurons (RQ1), we propose a neuron-guided fine-tuning method that updates only the parameters in modules containing specialized neurons. This sparse fine-tuning [58] enhances performance on the target task while maintaining general code intelligence by preserving the rest of the model.

The procedure involves three steps:

(1) Language-Specialized Neuron Identification: Select neurons specialized for the target language using PLS scores;   
(2) Parameter Freezing: Freeze all parameters except those in modules hosting the specialized neurons (e.g., linear layers like gate_proj);   
(3) Efficient Fine-Tuning: Update only the unfrozen parameters using the MCEval instructiontuning dataset.

We compare our method with LoRA [17], using Llama-3.1-8B as the base model due to resource constraints. To avoid potential contamination from benchmarks like HumanEval-X, we use the MCEval [1] benchmark for both training and evaluation. Evaluation is based on two metrics: the tunable parameter ratio, which reflects parameter efficiency, and the pass@3 metric, which measures the functional correctness of generated code. We also evaluate catastrophic forgetting by measuring the change $( \Delta )$ in pass@3 scores, specifically assessing non-target languages (e.g., Python) after

Table 4. Performance of Fine-Tuned Models for Code Generation (MCEval). The percentage change $( \Delta \% )$ in pass@3 score relative to the base model is indicated with $( \uparrow / \downarrow )$ .   

<table><tr><td rowspan="2">Tuning Lang.</td><td rowspan="2">Tuning Method</td><td rowspan="2">% Tunable Params</td><td colspan="6">Pass@3 for Target Language</td></tr><tr><td>Python</td><td>Java</td><td>Go</td><td>C++</td><td>JS</td><td></td></tr><tr><td colspan="3">Base Model (without tuning)</td><td>36%</td><td>56%</td><td>48%</td><td>48%</td><td>38%</td><td></td></tr><tr><td rowspan="2">Python</td><td>LoRA</td><td>0.53</td><td>42% (+16.7%)</td><td>58% (+3.6%)</td><td>34% (-29.2%)</td><td>48% (+0.0%)</td><td>34% (-10.5%)</td><td></td></tr><tr><td>Neuron-Guided</td><td>0.48</td><td>46% (+27.8%)</td><td>56% (+0.0%)</td><td>38% (-20.8%)</td><td>48% (+0.0%)</td><td>36% (-5.3%)</td><td></td></tr><tr><td rowspan="2">Java</td><td>LoRA</td><td>0.53</td><td>32% (-11.1%)</td><td>58% (+3.6%)</td><td>44% (-8.3%)</td><td>48% (+0.0%)</td><td>42% (+10.5%)</td><td></td></tr><tr><td>Neuron-Guided</td><td>0.10</td><td>40% (+11.1%)</td><td>56% (+0.0%)</td><td>46% (-4.2%)</td><td>46% (-4.2%)</td><td>40% (+5.3%)</td><td></td></tr><tr><td rowspan="2">Go</td><td>LoRA</td><td>0.53</td><td>44% (+22.2%)</td><td>54% (-3.6%)</td><td>48% (+0.0%)</td><td>50% (+4.2%)</td><td>34% (-10.5%)</td><td></td></tr><tr><td>Neuron-Guided</td><td>0.03</td><td>42% (+16.7%)</td><td>56% (+0.0%)</td><td>54% (+12.5%)</td><td>46% (-4.2%)</td><td>36% (-5.3%)</td><td></td></tr><tr><td rowspan="2">C++</td><td>LoRA</td><td>0.53</td><td>30% (-16.7%)</td><td>52% (-7.1%)</td><td>38% (-20.8%)</td><td>48% (+0.0%)</td><td>30% (-21.1%)</td><td></td></tr><tr><td>Neuron-Guided</td><td>0.23</td><td>34% (-5.6%)</td><td>54% (-3.6%)</td><td>42% (-12.5%)</td><td>50% (+4.2%)</td><td>38% (+0.0%)</td><td></td></tr><tr><td rowspan="2">JS</td><td>LoRA</td><td>0.53</td><td>32% (-11.1%)</td><td>50% (-10.7%)</td><td>42% (-12.5%)</td><td>44% (-8.3%)</td><td>52% (+36.8%)</td><td></td></tr><tr><td>Neuron-Guided</td><td>0.12</td><td>38% (+5.6%)</td><td>56% (+0.0%)</td><td>40% (-16.7%)</td><td>44% (-8.3%)</td><td>44% (+15.8%)</td><td></td></tr></table>

fine-tuning on a target language (e.g., Java). Superior forgetting mitigation is indicated by minimal degradation in non-target languages.

6.1.2 Results. The code generation performance of our neuron-guided fine-tuning method compared to LoRA is shown in Table 4. Our method achieves superior performance with a smaller fraction of tunable parameters. For example, when fine-tuned on Python, it achieves a $4 6 \%$ pass@3 score $\left( + 2 7 . 8 \% \right)$ , while LoRA achieves $4 2 \%$ $( + 1 6 . 7 \% )$ . These results suggest that updating only the modules containing causally relevant neurons (as identified in RQ1) can match or exceed the performance of broader PEFT methods that update more parameters.

A key advantage of our method is its ability to mitigate catastrophic forgetting. While LoRA applies broad updates that can disrupt knowledge of non-target languages, our targeted approach better preserves this knowledge. On average, across five languages, our method shows only a $2 . 6 \%$ decrease in performance on non-target languages, compared to $7 . 0 \%$ with LoRA. The difference is most pronounced in $\mathrm { C } { + } { + }$ : LoRA causes a $1 6 . 4 \%$ degradation, whereas our method limits this to $5 . 4 \%$ . These findings demonstrate that leveraging mechanistic insights about neurons offers a better trade-off between specialization and generalization.

Finding 3.1: Surgical fine-tuning of language-specific neurons outperforms standard LoRA with fewer updates while substantially mitigating catastrophic forgetting.

# 6.2 Clone Detection with Concept-Layer Embeddings

6.2.1 Study Design. The detection of semantic (Type-IV) code clones, which are code fragments that share functionality despite substantial differences in implementation, syntax, and lexicon, remains a significant challenge [47]. Existing methods that rely on surface-level features often fail to capture this kind of deep semantic equivalence [37]. The concept layers, which are identified in RQ2 as encoding abstract and language-agnostic representations of algorithmic logic, provide an ideal representational basis for this task.

The procedure consists of three steps:

![](images/4e0e30eed0415d8f3ea53510f6f2bc16b88dce7d4f6c15bbb34337e9818098f0.jpg)  
(a) Llama-3.1-8B

![](images/074a96c306833d5ce28d5947814636d5bd3d97888c5d7758ac3547d2f2ff02b7.jpg)  
(b) Qwen2.5-Coder-32B   
Fig. 5. F1-scores for Code Clone Detection using Embeddings across Model Layers.

(1) Representation Extraction: For a given pair of code fragments, $( c _ { A } , c _ { B } )$ , we process each using the frozen base model and extract the hidden-state vectors from the identified concept layers, ??concept.   
(2) Embedding Aggregation: We generate a single, fixed-size embedding vector for each fragment by applying mean pooling across the sequence of token vectors. This step yields the raw concept-layer embeddings:

$$
v _ {A} = \operatorname {P o o l} \left(H _ {L _ {\text {c o n c e p t}}} \left(c _ {A}\right)\right) \quad \text {a n d} \quad v _ {B} = \operatorname {P o o l} \left(H _ {L _ {\text {c o n c e p t}}} \left(c _ {B}\right)\right), \tag {5}
$$

where $H _ { L _ { \mathrm { c o n c e p t } } } ( c )$ denotes the hidden states at the concept layers for code fragment ??.

(3) Clone Classification: Finally, we quantify the semantic similarity between the two fragments by computing the cosine similarity of their raw embeddings, $v _ { A }$ and $v _ { B }$ . A pair is classified as a clone if this similarity score exceeds a threshold $\delta$ , which is optimized on a designated validation set.

We assess the effectiveness of concept-layer embeddings for semantic code clone detection in a zero-shot setting using Llama-3.1-8B and Qwen2.5-Coder-32B as base models, with comparative analysis across other feed-forward layers. We also include an LLM prompting approach as an additional baseline, where the model is instructed to judge whether two code fragments are functionally equivalent. F1-score measures performance on the CodeNet_clone [32] benchmark. Strong zero-shot results indicate that the model acquires powerful and generalizable representations of code functionality [32], contrasting with fine-tuning-based methods [8].

6.2.2 Results. Figure 5 presents the F1-scores for zero-shot semantic code clone detection using embeddings from each layer of the language models. For Llama-3.1-8B, the performance peaks within its identified concept layers (layers 8–15), reaching a maximum of 0.823 at layer 9. This represents a $2 0 . 3 \%$ relative improvement over the LLM prompting method of 0.684. A similar pattern is observed for Qwen2.5-Coder-32B, where performance also peaks within its concept layers (layers 31–43), achieving a maximum F1-score of approximately 0.86 at layer 38. This constitutes a $1 2 . 0 \%$ relative improvement over its baseline of 0.768. The F1-score curves for both models illuminate a distinct functional hierarchy within their architectures: in the lower layers, performance is limited by lexical and syntactic representations, while the upper layers are more specialized for token generation and lack the abstraction required for clone detection.

Notably, this strong performance is achieved in a zero-shot setting, without any task-specific fine-tuning. This indicates that the concept layers possess a powerful intrinsic generalization

capability, mapping semantically equivalent code from different languages to proximal points in the representation space. Such inherent structure, optimized for abstract reasoning, makes the concept layers an ideal source of representations for semantic understanding tasks. Moreover, these findings provide strong evidence for our RQ2 hypothesis that the concept layers serve as the locus of language-agnostic logical encoding.

Finding 3.2: The concept layers act as a potent semantic hub. Their direct zero-shot representations demonstrate superior performance in semantic clone detection, significantly outperforming both holistic LLM prompting and embeddings from other layers.

# 6.3 Concept-Layer Guided Transfer Learning for Code Summarization

6.3.1 Study Design. Generating high-quality natural language summaries for code in low-resource programming languages is challenging due to severe data scarcity and catastrophic forgetting of pre-trained knowledge [23]. We leverage the concept layers (Section 5), which are language-agnostic representations of program logic, as a semantic bridge to enable cross-lingual transfer.

To adapt the model efficiently, we use LoRA [17] and insert trainable low-rank adapters into the self-attention modules of all concept layers and higher layers, while freezing all original parameters. This focuses parameter updates on high-level semantic processing and preserves syntactic knowledge acquired during pre-training.

Training proceeds in two stages:

(1) High-Resource Adaptation: We first optimize the LoRA adapters on a large-scale code summarization dataset for high-resource languages (Python and Java), using cross-entropy loss over docstring tokens. This step teaches the model to map code semantics to natural language descriptions.   
(2) Low-Resource Transfer: We then continue training the same adapters on limited data from the target low-resource language (Ruby), again with cross-entropy loss. By reusing concept-layer representations learned on high-resource languages, the model can adapt to new syntax with substantially less data than training from scratch. This sequential approach offers a more efficient and direct form of cross-lingual transfer than conventional multilingual fine-tuning [4, 49].

We compare our concept-layer guided transfer learning against four baselines: (1) the Base model without any task-specific tuning; (2) Direct, which performs single-stage LoRA fine-tuning on a broad set of layers independently for each language, using only that language’s data; (3) Concept-LoRA, which applies single-stage LoRA only to the identified concept layers and is trained solely on the target low-resource language (Ruby); and (4) Two-Stage LoRA, a stronger baseline that follows the same high-resource→low-resource schedule as our method but places LoRA adapters on broad layers instead of restricting them to concept layers. As in previous experiments, Llama-3.1-8B serves as the base model, and we evaluate on CodeSearchNet [19] using BLEU-4 and ROUGE-L.

6.3.2 Results. The code summarization results are reported in Table 5. For Ruby, our designated low-resource language, the proposed two-stage concept-layer transfer (Ours) achieves the best performance among all methods, with 16.15 BLEU-4 and 31.80 ROUGE-L. This corresponds to a $9 . 1 \%$ improvement over Direct per-language LoRA (14.80 BLEU-4) and a $2 3 . 4 \%$ relative improvement over the single-stage Concept-LoRA model trained only on Ruby (13.09 BLEU-4). It also surpasses the stronger Two-Stage LoRA baseline (14.66 BLEU-4, 30.18 ROUGE-L), indicating that focusing adaptation on concept layers yields additional gains beyond those provided by the highresource low-resource schedule itself.

Table 5. Performance of Fine-Tuned Models for Code Summarization in Low-Resource Settings (CodeSearch-Net)   

<table><tr><td rowspan="2">Method</td><td colspan="2">Python</td><td colspan="2">Ruby</td><td colspan="2">Go</td><td colspan="2">Java</td><td colspan="2">JS</td><td colspan="2">PHP</td></tr><tr><td>BLEU-4</td><td>ROUGE-L</td><td>BLEU-4</td><td>ROUGE-L</td><td>BLEU-4</td><td>ROUGE-L</td><td>BLEU-4</td><td>ROUGE-L</td><td>BLEU-4</td><td>ROUGE-L</td><td>BLEU-4</td><td>ROUGE-L</td></tr><tr><td>Base</td><td>11.00</td><td>24.84</td><td>9.80</td><td>21.56</td><td>12.57</td><td>26.19</td><td>10.61</td><td>24.02</td><td>9.76</td><td>21.08</td><td>12.21</td><td>27.41</td></tr><tr><td>Direct</td><td>18.04</td><td>34.99</td><td>14.80</td><td>30.37</td><td>16.23</td><td>31.09</td><td>17.93</td><td>37.13</td><td>14.36</td><td>29.11</td><td>17.28</td><td>35.65</td></tr><tr><td>Concept-LoRA</td><td>14.34</td><td>31.00</td><td>13.09</td><td>28.00</td><td>14.08</td><td>28.41</td><td>15.08</td><td>33.29</td><td>13.06</td><td>26.53</td><td>14.52</td><td>32.04</td></tr><tr><td>Two-Stage LoRA</td><td>17.88</td><td>34.87</td><td>14.66</td><td>30.18</td><td>19.08</td><td>40.27</td><td>17.19</td><td>35.73</td><td>14.05</td><td>27.62</td><td>15.46</td><td>33.03</td></tr><tr><td>Ours</td><td>18.41</td><td>35.74</td><td>16.15</td><td>31.80</td><td>18.23</td><td>39.73</td><td>18.13</td><td>37.50</td><td>14.73</td><td>29.54</td><td>15.17</td><td>32.30</td></tr></table>

On high-resource Python, our method remains competitive or slightly better than the alternatives (18.41 / 35.74 BLEU-4 / ROUGE-L for Ours vs. 18.04 / 34.99 for Direct and 17.88 / 34.87 for Two-Stage LoRA). Across the remaining languages, Ours consistently outperforms the single-stage Concept-LoRA baseline and ranks among the top-performing methods, achieving the highest BLEU-4 in four out of six languages and at least the second-highest in one more. Overall, these patterns support the view that concept layers act as a semantic bridge: pre-adapting them on high-resource languages and then reusing the same adapters for a low-resource language yields more effective summarization in the low-resource setting, while maintaining competitive performance on high-resource languages.

Finding 3.3: Concept layers act as a semantic bridge for cross-lingual transfer: by first adapting them on high-resource languages and then reusing the same adapters for Ruby, our method substantially improves low-resource summarization compared with standard LoRA, direct indomain tuning, and a stronger Two-Stage LoRA baseline.

# 7 Limitations and Threats to Validity

This study has several limitations that could affect the validity of our findings:

Polysemy in neurons. This study investigates the distribution of programming languagespecific neurons in code LLMs by analyzing their activations under multilingual code inputs. However, prior work [7] indicates that individual neurons can be polysemous and may encode multiple distinct or unrelated concepts. Although the neurons identified here have been causally validated, their interpretation may remain incomplete and imprecise, since some neurons may participate in overlapping functionalities. A deeper examination of such polysemous neurons is reserved for future work.

Generalizability of models and languages. Our findings are derived from two specific dense transformer architectures and five programming languages. The extent to which these conclusions generalize to substantially different architectures (e.g., Mixture-of-Experts, models exceeding 70B parameters), proprietary closed-source models, or alternative programming paradigms warrants further investigation.

Absence of ground truth. Due to the lack of a standard “ground truth” for interpretability in code models, it is difficult to objectively evaluate explanation quality [60]. To address this, we validate our results from two perspectives: (1) deactivating identified language-specific neurons and measuring their impact on code generation, and (2) demonstrating how the language-specific neurons and concept layer can inform training strategies and code presentation methods for multilingual code intelligence.

# 8 Related Work

Most interpretability efforts for code LLMs have centered on analyzing attention mechanisms [40, 42, 59]. These studies examine attention weights and activations to understand where the model focuses throughout the input sequence. Mohammadkhani et al. [30] analyzed attention scores of CodeBERT and GraphCodeBERT, revealing how these models allocate attention to different code parts in software engineering tasks. Liu et al. [26] used attention interpretability to study how models like CodeT5 and CodeGPT attend to code elements during generation, translation, and repair. Paltenghi et al. [34] compared the attention patterns of neural code models to those of human developers. Wan et al. [52] combined attention analysis, word embedding probing, and syntax tree induction to understand code structure and semantics.

Another strand of research focuses on representation and concept analysis to investigate how code LLMs internally organize and represent programming knowledge. Sharma et al. [41] revealed how coding concepts are redundantly distributed across neurons. Ma et al. [28] used Fisher information to demonstrate how multilingual code models group languages based on structural similarities. Haider et al. [12] identified hierarchical concept encoding in feed-forward networks, ranging from syntax to semantics. Kargaran et al. [22] used logit lens and neuron activation analysis on Llama models to study the shared representations between multiple programming languages and English. They found that the model’s internal concept space is close to English and that while languagespecific neurons are concentrated in the bottom layers, neurons exclusive to a single programming language tend to appear in the top layers. Wang et al. [55] extracted minimal critical code segments that drive model predictions. Troshin et al. [50] quantitatively evaluated how program attributes are encoded across layers.

Finally, causal and counterfactual analysis is emerging as an approach that seeks to identify cause-effect relationships in code LLM behavior through targeted interventions. Nader-Palacio et al. [33] established a formal basis for causal reasoning in code models. Gupta et al. [10] extended this to multi-modal code generation, modeling how different inputs causally affect outputs. Cito et al. [2] generated minimal code perturbations to reveal model decision boundaries. Hooda et al. [15] tested concept understanding by altering program logic and observing model responses. Rodriguez-Cardenas et al. [38] evaluated and compared causal methods for code model interpretation.

Our work aligns firmly with the representation and concept analysis paradigm. In contrast to prior studies, we are the first to systematically analyze neuron activation patterns in response to multilingual code inputs and to assess the contributions of individual layers throughout the output generation process. Furthermore, we investigate the causal effects of identified programming language-specific neurons, and utilize these insights to strategically control model behavior, thereby enhancing performance on code-related tasks.

# 9 Conclusion

In this paper, we present a neuron-level interpretability study of code LLMs, uncovering the distinct roles of programming language-specific neurons and cross-lingual concept layers. Our findings offer deeper insights into the internal mechanisms underlying multilingual code understanding and generation. We further demonstrate the practical utility of these insights through neuronguided fine-tuning, concept-aware embeddings, and transfer learning—consistently improving performance on tasks including code generation, clone detection, and summarization. By enhancing the transparency and controllability of code language models, this work provides a foundation for future research in explainable AI for software engineering and supports advances in multilingual code intelligence.

# Data Availability

All code and data used in this study are publicly available at: https://github.com/mmuzhi/Neuron-Guided-Interpretation-of-CodeLLMs. The repository includes: (i) the code for our proposed PLS method, the layer-wise probing framework (RSA and AST probes), and the downstream tasks; and (ii) all experimental datasets and results.

# Acknowledgments

This research is funded by the National Key Research and Development Program of China (Grant No. 2023YFB4503802), the National Natural Science Foundation of China (Grant No. 62232003), and the Natural Science Foundation of Shanghai (Grant No. 25ZR1401175).

# References

[1] Linzheng Chai, Shukai Liu, Jian Yang, Yuwei Yin, Ke Jin, Jiaheng Liu, Tao Sun, Ge Zhang, Changyu Ren, Hongcheng Guo, Noah Wang, Boyang Wang, Xianjie Wu, Bing Wang, Tongliang Li, Liqun Yang, Sufeng Duan, Zhaoxiang Zhang, and Zhoujun Li. 2025. McEval: Massively Multilingual Code Evaluation. In Proceedings of the Thirteenth International Conference on Learning Representations, ICLR 2025, Singapore, April 24-28, 2025.   
[2] Jürgen Cito, Isil Dillig, Vijayaraghavan Murali, and Satish Chandra. 2024. Counterfactual Explanations for Models of Code. In Software Engineering 2024, Fachtagung des GI-Fachbereichs Softwaretechnik, Linz, Austria, February 26 - March 1, 2024 (LNI, Vol. P-343). Gesellschaft für Informatik e.V., 91–92.   
[3] Kevin Clark, Urvashi Khandelwal, Omer Levy, and Christopher D. Manning. 2019. What Does BERT Look at? An Analysis of BERT’s Attention. In Proceedings of the 2019 ACL Workshop BlackboxNLP: Analyzing and Interpreting Neural Networks for NLP, BlackboxNLP@ACL 2019, Florence, Italy, August 1, 2019. Association for Computational Linguistics, 276–286.   
[4] Alexis Conneau and Guillaume Lample. 2019. Cross-lingual Language Model Pretraining. In Proceedings of Advances in Neural Information Processing Systems 32: Annual Conference on Neural Information Processing Systems, NeurIPS 2019, December 8-14, 2019, Vancouver, BC, Canada. 7057–7067.   
[5] Damai Dai, Li Dong, Yaru Hao, Zhifang Sui, Baobao Chang, and Furu Wei. 2022. Knowledge Neurons in Pretrained Transformers. In Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), ACL 2022, Dublin, Ireland, May 22-27, 2022. Association for Computational Linguistics, 8493–8502.   
[6] Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman, and et al. 2024. The Llama 3 Herd of Models. CoRR abs/2407.21783 (2024).   
[7] Nelson Elhage, Tristan Hume, Catherine Olsson, Nicholas Schiefer, Tom Henighan, Shauna Kravec, Zac Hatfield-Dodds, Robert Lasenby, Dawn Drain, Carol Chen, Roger B. Grosse, Sam McCandlish, Jared Kaplan, Dario Amodei, Martin Wattenberg, and Christopher Olah. 2022. Toy Models of Superposition. CoRR abs/2209.10652 (2022).   
[8] Zhangyin Feng, Daya Guo, Duyu Tang, Nan Duan, Xiaocheng Feng, Ming Gong, Linjun Shou, Bing Qin, Ting Liu, Daxin Jiang, and Ming Zhou. 2020. CodeBERT: A Pre-Trained Model for Programming and Natural Languages. In Findings of the Association for Computational Linguistics: EMNLP 2020, Online Event, 16-20 November 2020 (Findings of ACL, Vol. EMNLP 2020). Association for Computational Linguistics, 1536–1547.   
[9] Asma Ghandeharioun, Avi Caciularu, Adam Pearce, Lucas Dixon, and Mor Geva. 2024. Patchscopes: A Unifying Framework for Inspecting Hidden Representations of Language Models. In Proceedings of Forty-first International Conference on Machine Learning, ICML 2024, Vienna, Austria, July 21-27, 2024.   
[10] Mukur Gupta, Noopur Bhatt, and Suman Jana. 2025. CodeSCM: Causal Analysis for Multi-Modal Code Generation. In Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics: Human Language Technologies, NAACL 2025 - Volume 1: Long Papers, Albuquerque, New Mexico, USA, April 29 - May 4, 2025. Association for Computational Linguistics, 6779–6793.   
[11] Wes Gurnee, Neel Nanda, Matthew Pauly, Katherine Harvey, Dmitrii Troitskii, and Dimitris Bertsimas. 2023. Finding Neurons in a Haystack: Case Studies with Sparse Probing. Trans. Mach. Learn. Res. 2023 (2023).   
[12] Muhammad Umair Haider, Umar Farooq, A. B. Siddique, and Mark Marron. 2024. Looking into Black Box Code Language Models. CoRR abs/2407.04868 (2024).   
[13] John Hewitt and Percy Liang. 2019. Designing and Interpreting Probes with Control Tasks. In Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing, EMNLP-IJCNLP 2019, Hong Kong, China, November 3-7, 2019. Association for Computational Linguistics, 2733–2743.

[14] John Hewitt and Christopher D. Manning. 2019. A Structural Probe for Finding Syntax in Word Representations. In Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, NAACL-HLT 2019, Minneapolis, MN, USA, June 2-7, 2019, Volume 1 (Long and Short Papers). Association for Computational Linguistics, 4129–4138.   
[15] Ashish Hooda, Mihai Christodorescu, Miltiadis Allamanis, Aaron Wilson, Kassem Fawaz, and Somesh Jha. 2024. Do Large Code Models Understand Programming Concepts? Counterfactual Analysis for Code Predicates. In Proceedings of Forty-first International Conference on Machine Learning, ICML 2024, Vienna, Austria, July 21-27, 2024.   
[16] Chao Hu, Wenhao Zeng, Yuling Shi, Beijun Shen, and Xiaodong Gu. 2026. In Line with Context: Repository-Level Code Generation via Context Inlining. In Proceedings of 2026 ACM International Conference on the Foundations of Software Engineering (FSE). ACM.   
[17] Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. 2022. LoRA: Low-Rank Adaptation of Large Language Models. In Proceedings of the Tenth International Conference on Learning Representations, ICLR 2022, Virtual Event, April 25-29, 2022.   
[18] Binyuan Hui, Jian Yang, Zeyu Cui, Jiaxi Yang, Dayiheng Liu, Lei Zhang, Tianyu Liu, Jiajun Zhang, Bowen Yu, Kai Dang, An Yang, Rui Men, Fei Huang, Xingzhang Ren, Xuancheng Ren, Jingren Zhou, and Junyang Lin. 2024. Qwen2.5-Coder Technical Report. CoRR abs/2409.12186 (2024).   
[19] Hamel Husain, Ho-Hsiang Wu, Tiferet Gazit, Miltiadis Allamanis, and Marc Brockschmidt. 2019. CodeSearchNet Challenge: Evaluating the State of Semantic Code Search. CoRR abs/1909.09436 (2019).   
[20] Ganesh Jawahar, Benoît Sagot, and Djamé Seddah. 2019. What Does BERT Learn about the Structure of Language?. In Proceedings of the 57th Conference of the Association for Computational Linguistics, ACL 2019, Florence, Italy, July 28- August 2, 2019, Volume 1: Long Papers. Association for Computational Linguistics, 3651–3657.   
[21] Jirayus Jiarpakdee, Chakkrit Tantithamthavorn, and John C. Grundy. 2021. Practitioners’ Perceptions of the Goals and Visual Explanations of Defect Prediction Models. In Proceedings of 18th IEEE/ACM International Conference on Mining Software Repositories, MSR 2021, Madrid, Spain, May 17-19, 2021. 432–443.   
[22] Amir Hossein Kargaran, Yihong Liu, François Yvon, and Hinrich Schütze. 2025. How Programming Concepts and Neurons Are Shared in Code Language Models. In Findings of the Association for Computational Linguistics, ACL 2025, Vienna, Austria, July 27 - August 1, 2025. Association for Computational Linguistics, 26905–26917.   
[23] James Kirkpatrick, Razvan Pascanu, Neil C. Rabinowitz, Joel Veness, Guillaume Desjardins, Andrei A. Rusu, Kieran Milan, John Quan, Tiago Ramalho, Agnieszka Grabska-Barwinska, Demis Hassabis, Claudia Clopath, Dharshan Kumaran, and Raia Hadsell. 2016. Overcoming catastrophic forgetting in neural networks. CoRR abs/1612.00796 (2016).   
[24] Nikolaus Kriegeskorte, Marieke Mur, and Peter Bandettini. 2008. Representational similarity analysis—connecting the branches of systems neuroscience. Frontiers in Systems Neuroscience 2 (2008).   
[25] Linyi Li, Shijie Geng, Zhenwen Li, Yibo He, Hao Yu, Ziyue Hua, Guanghan Ning, Siwei Wang, Tao Xie, and Hongxia Yang. 2024. InfiBench: Evaluating the Question-Answering Capabilities of Code Large Language Models. In Proceedings of Advances in Neural Information Processing Systems 38: Annual Conference on Neural Information Processing Systems, NeurIPS 2024, Vancouver, BC, Canada, December 10 - 15, 2024.   
[26] Yue Liu, Chakkrit Tantithamthavorn, Yonghui Liu, and Li Li. 2024. On the Reliability and Explainability of Language Models for Program Generation. ACM Trans. Softw. Eng. Methodol. 33, 5 (2024), 126:1–126:26.   
[27] Ilya Loshchilov and Frank Hutter. 2019. Decoupled Weight Decay Regularization. In Proceedings of 7th International Conference on Learning Representations, ICLR 2019, New Orleans, LA, USA, May 6-9, 2019.   
[28] Xinyu Ma, Xuebo Liu, and Min Zhang. 2023. Clustering Pseudo Language Family in Multilingual Translation Models with Fisher Information Matrix. In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, EMNLP 2023, Singapore, December 6-10, 2023. Association for Computational Linguistics, 13794–13804.   
[29] Jack Merullo, Carsten Eickhoff, and Ellie Pavlick. 2024. Circuit Component Reuse Across Tasks in Transformer Language Models. In Proceedings of the Twelfth International Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024.   
[30] Ahmad Haji Mohammadkhani, Chakkrit Tantithamthavorn, and Hadi Hemmati. 2023. Explaining Transformer-based Code Models: What Do They Learn? When They Do Not Work?. In Proceedings of 23rd IEEE International Working Conference on Source Code Analysis and Manipulation, SCAM 2023, Bogotá, Colombia, October 2-3, 2023. IEEE, 96–106.   
[31] John X. Morris, Volodymyr Kuleshov, Vitaly Shmatikov, and Alexander M. Rush. 2023. Text Embeddings Reveal (Almost) As Much As Text. In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, EMNLP 2023, Singapore, December 6-10, 2023. Association for Computational Linguistics, 12448–12460.   
[32] Micheline Bénédicte Moumoula, Abdoul Kader Kaboré, Jacques Klein, and Tegawendé F. Bissyandé. 2025. The Struggles of LLMs in Cross-Lingual Code Clone Detection. Proc. ACM Softw. Eng. 2, FSE (2025), 1023–1045.   
[33] David Nader-Palacio, Alejandro Velasco, Nathan Cooper, Alvaro Rodriguez, Kevin Moran, and Denys Poshyvanyk. 2024. Toward a Theory of Causation for Interpreting Neural Code Models. IEEE Trans. Software Eng. 50, 5 (2024),

1215–1243.   
[34] Matteo Paltenghi and Michael Pradel. 2021. Thinking Like a Developer? Comparing the Attention of Humans with Neural Models of Code. In Proceedings of 36th IEEE/ACM International Conference on Automated Software Engineering, ASE 2021, Melbourne, Australia, November 15-19, 2021. IEEE, 867–879.   
[35] Adam Paszke, Sam Gross, Francisco Massa, Adam Lerer, James Bradbury, Gregory Chanan, Trevor Killeen, Zeming Lin, Natalia Gimelshein, Luca Antiga, Alban Desmaison, Andreas Köpf, Edward Z. Yang, Zachary DeVito, Martin Raison, Alykhan Tejani, Sasank Chilamkurthy, Benoit Steiner, Lu Fang, Junjie Bai, and Soumith Chintala. 2019. PyTorch: An Imperative Style, High-Performance Deep Learning Library. In Proceedings of Advances in Neural Information Processing Systems 32: Annual Conference on Neural Information Processing Systems, NeurIPS 2019, December 8-14, 2019, Vancouver, BC, Canada. 8024–8035.   
[36] Tiago Pimentel, Naomi Saphra, Adina Williams, and Ryan Cotterell. 2020. Pareto Probing: Trading Off Accuracy for Complexity. In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing, EMNLP 2020, Online, November 16-20, 2020. Association for Computational Linguistics, 3138–3153.   
[37] Subroto Nag Pinku, Debajyoti Mondal, and Chanchal K. Roy. 2024. On the Use of Deep Learning Models for Semantic Clone Detection. In Proceedings of IEEE International Conference on Software Maintenance and Evolution, ICSME 2024, Flagstaff, AZ, USA, October 6-11, 2024. IEEE, 512–524.   
[38] Daniel Rodríguez-Cárdenas, David N. Palacio, Dipin Khati, Henry Burke, and Denys Poshyvanyk. 2023. Benchmarking Causal Study to Interpret Large Language Models for Source Code. In Proceedings of IEEE International Conference on Software Maintenance and Evolution, ICSME 2023, Bogotá, Colombia, October 1-6, 2023. IEEE, 329–334.   
[39] Biagio La Rosa, Leilani Gilpin, and Roberto Capobianco. 2023. Towards a fuller understanding of neurons with Clustered Compositional Explanations. In Proceedings of Advances in Neural Information Processing Systems 36: Annual Conference on Neural Information Processing Systems, NeurIPS 2023, New Orleans, LA, USA, December 10 - 16, 2023.   
[40] Mootez Saad and Tushar Sharma. 2024. Naturalness of Attention: Revisiting Attention in Code Language Models. In Proceedings of the 2024 ACM/IEEE 44th International Conference on Software Engineering: New Ideas and Emerging Results, NIER@ICSE 2024, Lisbon, Portugal, April 14-20, 2024. ACM, 107–111.   
[41] Arushi Sharma, Zefu Hu, Christopher J. Quinn, and Ali Jannesari. 2024. Redundancy and Concept Analysis for Code-trained Language Models. In Proceedings of the 39th IEEE/ACM International Conference on Automated Software Engineering Workshops, ASEW 2024, Sacramento, CA, USA, 27 October 2024 - 1 November 2024. ACM, 24–34.   
[42] Rishab Sharma, Fuxiang Chen, Fatemeh H. Fard, and David Lo. 2022. An exploratory study on code attention in BERT. In Proceedings of the 30th IEEE/ACM International Conference on Program Comprehension, ICPC 2022, Virtual Event, May 16-17, 2022. ACM, 437–448.   
[43] Karen Simonyan, Andrea Vedaldi, and Andrew Zisserman. 2014. Deep Inside Convolutional Networks: Visualising Image Classification Models and Saliency Maps. In Proceedings of 2nd International Conference on Learning Representations, ICLR 2014, Banff, AB, Canada, April 14-16, 2014, Workshop Track Proceedings.   
[44] Weisong Sun, Yun Miao, Yuekang Li, Hongyu Zhang, Chunrong Fang, Yi Liu, Gelei Deng, Yang Liu, and Zhenyu Chen. 2025. Source Code Summarization in the Era of Large Language Models. In Proceedings of 47th IEEE/ACM International Conference on Software Engineering, ICSE 2025, Ottawa, ON, Canada, April 26 - May 6, 2025. IEEE, 1882–1894.   
[45] Mukund Sundararajan, Ankur Taly, and Qiqi Yan. 2017. Axiomatic Attribution for Deep Networks. In Proceedings of the 34th International Conference on Machine Learning, ICML 2017, Sydney, NSW, Australia, 6-11 August 2017 (Proceedings of Machine Learning Research, Vol. 70). PMLR, 3319–3328.   
[46] Tianyi Tang, Wenyang Luo, Haoyang Huang, Dongdong Zhang, Xiaolei Wang, Xin Zhao, Furu Wei, and Ji-Rong Wen. 2024. Language-Specific Neurons: The Key to Multilingual Capabilities in Large Language Models. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), ACL 2024, Bangkok, Thailand, August 11-16, 2024. Association for Computational Linguistics, 5701–5715.   
[47] Chenning Tao, Qi Zhan, Xing Hu, and Xin Xia. 2022. C4: contrastive cross-language code clone detection. In Proceedings of the 30th IEEE/ACM International Conference on Program Comprehension, ICPC 2022, Virtual Event, May 16-17, 2022. ACM, 413–424.   
[48] Ian Tenney, Dipanjan Das, and Ellie Pavlick. 2019. BERT Rediscovers the Classical NLP Pipeline. In Proceedings of the 57th Conference of the Association for Computational Linguistics, ACL 2019, Florence, Italy, July 28- August 2, 2019, Volume 1: Long Papers. Association for Computational Linguistics, 4593–4601.   
[49] Chau Tran, Yuqing Tang, Xian Li, and Jiatao Gu. 2020. Cross-lingual Retrieval for Iterative Self-Supervised Training. In Proceedings of Advances in Neural Information Processing Systems 33: Annual Conference on Neural Information Processing Systems, NeurIPS 2020, December 6-12, 2020, virtual.   
[50] Sergey Troshin and Nadezhda Chirkova. 2022. Probing Pretrained Models of Source Codes. In Proceedings of the Fifth BlackboxNLP Workshop on Analyzing and Interpreting Neural Networks for NLP, BlackboxNLP@EMNLP 2022, Abu Dhabi, United Arab Emirates (Hybrid), December 8, 2022. Association for Computational Linguistics, 371–383.

[51] Betty van Aken, Benjamin Winter, Alexander Löser, and Felix A. Gers. 2019. How Does BERT Answer Questions?: A Layer-Wise Analysis of Transformer Representations. In Proceedings of the 28th ACM International Conference on Information and Knowledge Management, CIKM 2019, Beijing, China, November 3-7, 2019. ACM, 1823–1832.   
[52] Yao Wan, Wei Zhao, Hongyu Zhang, Yulei Sui, Guandong Xu, and Hai Jin. 2022. What Do They Capture? - A Structural Analysis of Pre-Trained Language Models for Source Code. In Proceedings of IEEE/ACM 44th International Conference on Software Engineering, ICSE 2022, Pittsburgh, PA, USA, May 25-27, 2022. ACM, 2377–2388.   
[53] Chaofan Wang, Tingrui Yu, Beijun Shen, Jie Wang, Dong Chen, Wenrui Zhang, Yuling Shi, Chen Xie, and Xiaodong Gu. 2026. EvoC2Rust: A Skeleton-guided Framework for Project-Level C-to-Rust Translation. In Proceedings of IEEE/ACM 44th International Conference on Software Engineering, ICSE 2026 SEIP. Rio de Janeiro, Brazil, April 12-18, 2026. ACM.   
[54] Kevin Ro Wang, Alexandre Variengien, Arthur Conmy, Buck Shlegeris, and Jacob Steinhardt. 2023. Interpretability in the Wild: a Circuit for Indirect Object Identification in GPT-2 Small. In Proceedings of the Eleventh International Conference on Learning Representations, ICLR 2023, Kigali, Rwanda, May 1-5, 2023.   
[55] Yu Wang, Ke Wang, and Linzhang Wang. 2023. An Explanation Method for Models of Code. Proc. ACM Program. Lang. 7, OOPSLA2 (2023), 801–827.   
[56] Jan Wehner, Sahar Abdelnabi, Daniel Tan, David Krueger, and Mario Fritz. 2025. Taxonomy, Opportunities, and Challenges of Representation Engineering for Large Language Models. CoRR abs/2502.19649 (2025).   
[57] Thomas Wolf, Lysandre Debut, Victor Sanh, Julien Chaumond, Clement Delangue, Anthony Moi, Pierric Cistac, Tim Rault, Rémi Louf, Morgan Funtowicz, Joe Davison, Sam Shleifer, Patrick von Platen, Clara Ma, Yacine Jernite, Julien Plu, Canwen Xu, Teven Le Scao, Sylvain Gugger, Mariama Drame, Quentin Lhoest, and Alexander M. Rush. 2020. Transformers: State-of-the-Art Natural Language Processing. In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing: System Demonstrations, EMNLP 2020 - Demos, Online, November 16-20, 2020. Association for Computational Linguistics, 38–45.   
[58] Haoyun Xu, Runzhe Zhan, Yingpeng Ma, Derek F. Wong, and Lidia S. Chao. 2025. Let’s Focus on Neuron: Neuron-Level Supervised Fine-tuning for Large Language Model. In Proceedings of the 31st International Conference on Computational Linguistics, COLING 2025, Abu Dhabi, UAE, January 19-24, 2025. Association for Computational Linguistics, 9393–9406.   
[59] Kechi Zhang, Ge Li, and Zhi Jin. 2022. What does Transformer learn about source code? CoRR abs/2207.08466 (2022).   
[60] Haiyan Zhao, Hanjie Chen, Fan Yang, Ninghao Liu, Huiqi Deng, Hengyi Cai, Shuaiqiang Wang, Dawei Yin, and Mengnan Du. 2024. Explainability for Large Language Models: A Survey. ACM Trans. Intell. Syst. Technol. 15, 2 (2024), 20:1–20:38.   
[61] Qinkai Zheng, Xiao Xia, Xu Zou, Yuxiao Dong, Shan Wang, Yufei Xue, Lei Shen, Zihan Wang, Andi Wang, Yang Li, Teng Su, Zhilin Yang, and Jie Tang. 2023. CodeGeeX: A Pre-Trained Model for Code Generation with Multilingual Benchmarking on HumanEval-X. In Proceedings of the 29th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, KDD 2023, Long Beach, CA, USA, August 6-10, 2023. ACM, 5673–5684.   
[62] Andy Zou, Long Phan, Sarah Li Chen, James Campbell, Phillip Guo, Richard Ren, Alexander Pan, Xuwang Yin, Mantas Mazeika, Ann-Kathrin Dombrowski, Shashwat Goel, Nathaniel Li, Michael J. Byun, Zifan Wang, Alex Mallen, Steven Basart, Sanmi Koyejo, Dawn Song, Matt Fredrikson, J. Zico Kolter, and Dan Hendrycks. 2023. Representation Engineering: A Top-Down Approach to AI Transparency. CoRR abs/2310.01405 (2023).

Received 2025-09-12; accepted 2025-12-22