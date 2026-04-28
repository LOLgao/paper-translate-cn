# 与上下文对齐：通过上下文内联实现仓库级代码生成

胡超，上海交通大学，中国

曾文浩，上海交通大学，中国

施玉玲，上海交通大学，中国

沈备军，上海交通大学，中国

顾晓东∗，上海交通大学，中国

近年来，仓库级代码生成日益受到关注。与函数级代码生成不同，它要求模型理解整个代码仓库，对跨越函数、类和模块的复杂依赖关系进行推理。然而，现有的方法，如检索增强生成或基于上下文的函数选择，往往存在不足：它们主要依赖于表层相似性，难以捕捉支配仓库级语义的丰富依赖关系。本文提出了InlineCoder，一个用于仓库级代码生成的新颖框架。InlineCoder通过将未完成的函数内联到其调用图中，从而将具有挑战性的仓库理解问题重构为更简单的函数级编码任务，以此增强对仓库上下文的理解。给定一个函数签名，InlineCoder首先生成一个草稿补全，称为锚点，该锚点近似于下游依赖关系，并支持基于困惑度的置信度估计。这个锚点驱动一个双向内联过程：（i）上游内联，将锚点嵌入到其调用者中，以捕捉多样化的使用场景；以及（ii）下游检索，将锚点的被调用者集成到提示中，以提供精确的依赖上下文。结合了草稿补全以及上游和下游视角的丰富上下文，为大型语言模型提供了全面的仓库视图。在DevEval和RepoExec基准测试上进行的大量实验表明，InlineCoder显著优于一系列最先进的基线方法，在RepoExec上，相较于最强基线，其EM、ES和BLEU指标的平均相对增益分别为 $2 9 . 7 3 \%$、$2 0 . 8 2 \%$ 和 $4 9 . 3 4 \%$。这些结果突显了其在理解仓库上下文方面的有效性以及其跨领域的泛化能力。

# ACM 参考文献格式：



胡超、曾文浩、石玉玲、沈北军、顾晓东。2026年。与上下文一致：通过上下文内联实现仓库级代码生成。第1卷，第1期（2026年1月），共22页。https://doi.org/10.1145/nnnnnnn.nnnnnnn

# 1 引言

随着代码大语言模型的快速发展，仓库级代码生成近年来受到越来越多的关注[23, 27, 53, 63]。与函数级生成不同，仓库级生成需要对整个仓库进行推理，考虑编码规范、API使用以及复杂的函数间依赖关系[54]。在此场景下取得成功，不仅需要语法正确、语义有效的代码，还需要与仓库更广泛的设计和依赖关系保持一致[16, 24, 37, 45, 66]。

仓库级生成的一个关键障碍是仓库上下文本身。虽然它包含了准确生成所需的关键信息，但由于上下文窗口的限制以及大量无关或冗余代码的存在[49]，直接将整个仓库输入大语言模型是不可行的。这引发了一个核心挑战：我们如何从庞大的代码库中提炼并呈现最相关的上下文，以支持有效的代码生成？

先前的研究通过各种检索策略来应对这一挑战。最常见的是检索增强生成（RAG），它检索与未完成函数相似的代码片段[10, 11, 29, 32, 55, 63]。然而，在代码中，相似性并不一定意味着相关性：词汇相似的片段可能在功能上无关，从而导致提示信息嘈杂或具有误导性。基于智能体的流水线通过支持迭代检索和大语言模型引导的检索目标评估，进一步扩展了这些能力[4, 36, 64]。更先进的方法结合了程序分析，例如控制流或数据流图，以更准确地捕获语义依赖关系[6, 32, 33, 42, 44]。虽然这些方法对于行级补全或API预测等细粒度任务有效，但它们严重依赖局部上下文，并且通常难以推广到函数级生成，因为后者需要从头开始合成整个实现。

为了克服这些限制，我们提出了InlineCoder，一个用于仓库级代码生成的新颖框架。我们的核心见解是：一个函数在仓库中的角色由其在该仓库调用栈中的位置决定：它受到其上游调用者（如何使用它）的约束，而其实现则依赖于其下游被调用者（它依赖什么）。InlineCoder通过将未完成函数内联到其调用链中，从而将仓库级生成重新表述为更简单的函数级生成任务，以此增强上下文理解。给定一个函数签名，InlineCoder首先生成一个草稿实现——一个用于近似潜在依赖关系的锚点。然后，这个草稿驱动一个双向内联过程：（1）上游内联：将锚点内联到其调用者中，以提供丰富的使用场景。（2）下游检索：整合草稿调用的所有被调用者，捕获其依赖上下文。最后，我们将草稿代码与内联上下文整合到一个综合提示中，使大语言模型能够生成最终的、具有上下文感知的代码。

我们在两个广泛使用的仓库级代码生成基准测试（DevEval [27]和RepoExec [23]）上评估了InlineCoder，使用了三个骨干大语言模型：DeepSeek-V3 [30]、Qwen3-Coder [60]和GPT5-mini [41]。InlineCoder展示了最佳的整体性能。值得注意的是，在RepoExec上，与最强的基线相比，它在EM、ES和BLEU指标上分别实现了平均相对增益$2 9 . 7 3 \%$、$2 0 . 8 2 \%$和$4 9 . 3 4 \%$。消融研究证实了InlineCoder的每个组件都对最终效果有所贡献。此外，针对特定代码结构的针对性分析，以及在不同领域仓库和不同上下文环境下的实验表明，InlineCoder始终能带来显著增益——突显了其在仓库级代码生成方面的鲁棒性和泛化能力。

本文的主要贡献如下：

• 我们提出了一种新颖的仓库级代码生成框架，将目标函数置于其上游（调用者）和下游（被调用者）上下文中。
• 我们首次将函数内联到其调用者的上下文中，使大语言模型能够更深入地理解函数的预期目的和使用模式。
• 我们在多个基准测试上进行了广泛的评估。结果表明，我们的方法在不同的上下文环境和多个领域中，相比最先进的基线模型都取得了一致的改进。

# 2 研究动机

代码仓库级代码生成的一个核心挑战在于如何有效地将仓库上下文信息融入模型[6]。当前方法通常采用基于检索的框架，即根据文本相似性或结构邻近性选择相关代码片段。虽然这种策略

![](images/2a57d46376c8fd9ce3403ee3163ae3b4dac6ab9da428704781fc714e55d099bc.jpg)  
(a) 前置上下文

![](images/fb37c15844b38e63f1a84783f1ba65dc556cb07a32e0967781eb3d264823c9ef.jpg)  
(b) 内联上下文

![](images/06e4de171c09aa2a833dbc28616e5dd6459affda578f71eb7edf42f769963182.jpg)

![](images/ca3c76665d123f3ea8737f372e863d31ab8539960311375070b614e8a93ff365.jpg)

![](images/48c067ec44f00175f55b83731757632cb42c0108f4a5a145842ac413a7691591.jpg)  
图1. 动机示例。将目标函数内联到其调用链中，可创建更具上下文感知的任务表述，从而生成与仓库一致的代码补全。

能够提供局部上下文，但很少能系统性地表征函数如何被其调用者（上游）实际使用，或其如何依赖于被调用函数（下游）[63]。

近期一些研究尝试融入调用链信息，但通常只是简单地将检索到的函数前置在未完成的目标函数签名之前[32]。这种线性拼接忽略了目标函数在其真实调用环境中的功能角色。因此，模型可能无法感知输入/输出约束或调用约定，导致对函数语义的理解不完整或产生误导。若未将检索到的代码片段适配到实际调用点，模型很容易无法推断正确的变量绑定、返回类型或仓库中使用的适当API变体[64]。

图1(a)展示了这些缺陷的示例。传统方法通常将目标函数孤立处理，并在其上方附加工具函数或代码片段，未能捕捉真实的调用关系。因此，模型错误地调用了无关的工具函数extract_functions，并生成了dict类型而非预期的list[str]。

此示例引出了上下文融合的新范式，如图1(b)所示：我们可以将目标函数直接内联到其调用上下文中，从而提供内联上下文。这种方法将结构化的调用图信息转化为模型易于理解的形式，揭示出变量绑定、返回格式和有效API使用等关键信号。如示例所示，内联上下文使模型能够生成与仓库一致的代码：正确的函数现在返回list[str]类型并调用适当的被调用函数。通过将定向上下文检索与内联技术相结合，我们的方法实现了具有上下文感知能力且与仓库对齐的代码生成，从而解决了传统基于检索策略的缺陷。

# 3 方法论

# 3.1 总体框架

给定代码库 $\mathcal { D }$ 中一个未完成函数签名 $x$ ，仓库级代码生成的目标是利用来自 $\mathcal { D }$ 的上下文信息 $c$ 来生成函数体 $y$ 。该任务的主要挑战在于尽可能准确地提取有用的上下文 $c$ ，并让

![](images/14ac02fa32280892f17ad53ce06d6366b629f6d9424422c6f4f6a9ff76741f93.jpg)  
图 2. InlineCoder 框架。

模型理解上下文 $c$ 中的信息，这需要对整个仓库进行推理，理解跨函数、类和模块的复杂依赖关系。

为应对这一挑战，我们提出了 InlineCoder，一个用于仓库级代码生成的新颖框架。与以往在上下文中检索相似代码片段的技术不同，InlineCoder 的核心思想是将目标函数置于其调用图环境中。如图 2 所示，InlineCoder 遵循一个三阶段流程：

1)  草稿生成（第 3.2 节）：给定围绕目标函数签名构建的基础提示，InlineCoder 首先生成未完成函数的初步实现，以此作为锚点。该草稿不仅提供了潜在下游依赖的近似视图，有助于将目标函数定位在仓库的调用图中，还为困惑度评估提供了基础。
2)  上下文内联（第 3.3 节）：随后，将草稿内联到其调用者中以捕获上游使用场景，同时检索相关的被调用者实现并将其纳入下游。此过程产生一个连贯的、线性化的表示，将上游和下游的上下文信息扁平化为一个统一的视图供模型使用。
3)  上下文集成（第 3.4 节）：InlineCoder 将所有相关信息集成到一个上下文增强的提示中，该提示包含：(a) 基础提示（函数签名 $^ +$ 导入），(b) 检索到的上游和下游上下文，以及 (c) 初始草稿。这个丰富的提示为大型语言模型提供了全面的指导，使其能够生成语义准确且与仓库环境一致的最终实现。每个阶段的细节将在以下小节中详细阐述。

# 3.2 草稿生成



草稿生成阶段生成目标函数的初步实现，称为锚点。该草稿随后作为一个语义丰富的工件，指导后续检索，并为最终生成提供参考点。

为生成此草稿，我们首先构建一个初始提示，为LLM提供本地上下文和依赖关系的全面视图。我们从目标文件中收集所有导入语句，并附加在仓库中发现的所有直接引用依赖项（例如，变量、函数、类）的完整代码，同时保持原始的导入顺序。此跨文件引用信息由数据集（即REPOEXEC [23]和DevEval [27]）提供。随后，我们添加未完成函数的签名及其自然语言描述。

接着，将此结构化提示输入LLM，LLM会生成函数体的候选实现（草稿）以及其中使用的API调用列表。生成的草稿扮演双重角色：一方面，它作为检索的种子；识别出的API调用为后续的下游检索过程提供了明确、高置信度的信号。另一方面，它作为生成的参考；该草稿用于计算基于困惑度的置信度分数，以指导最终生成阶段，同时也作为一个可在最终生成过程中进行优化的草稿实现。

# 3.3 上下文内联

在草稿生成阶段的初步实现基础上，我们引入了一种双管齐下的内联过程，以整合其上游和下游上下文。其核心洞见基于这样一个观察：函数的作用由其在该仓库调用图中的位置所定义。其行为受上游调用者（如何使用它）的约束，而其实现则依赖于下游被调用者（它依赖什么）。

3.3.1 上游内联。上游内联旨在为LLM提供对目标函数预期使用方式的深入理解。该过程首先识别目标函数的所有调用者。我们遍历仓库的AST，以识别所有调用目标函数的调用点。对于每个调用点，我们提取相应的调用函数，称之为调用者。与传统方法仅将调用者上下文前置到提示中不同，InlineCoder提出了一种新颖的上下文内联技术。如图3所示，我们将草稿直接嵌入到其调用者中，生成一个连贯的、线性化的函数上下文表示。这是通过一个四步转换实现的：

(1) 参数替换：令 ${ \mathrm { A r g s } } = \left[ a _ { 1 } , a _ { 2 } , \ldots , a _ { m } \right]$ 表示调用点的实参列表，Params $\mathbf { \Phi } = [ p _ { 1 } , p _ { 2 } , \dots \cdot \cdot , p _ { m } ]$ 表示被调用者定义中的形参。我们定义一个针对标识符的替换函数：

$$
\sigma : \mathcal {I} \rightarrow \mathcal {I} ^ {\prime}, \quad \sigma (x) = \left\{\begin{array}{l l}a _ {i}&\text {i f} x = p _ {i} \in \operatorname {P a r a m s},\\x&\text {o t h e r w i s e},\end{array}\right. \tag {1}
$$

其中 $\boldsymbol { \mathcal { I } }$ 是被调用者函数体的标识符集合，$\scriptstyle { { \cal { T } } ^ { \prime } }$ 表示替换后的标识符集合。

我们将 $\sigma$ 提升到语句层面，$s \to s ^ { \prime }$ ，通过递归地将其应用于语句 $s \in S$ 中的所有标识符，其中 $s$ 是被调用者函数体中的语句集合，$S ^ { \prime }$ 表示标识符替换后的语句。

对于被调用者函数体 $\mathtt { B o d y } _ { f } = \{ s _ { 1 } , \ldots , s _ { N } \}$ ，参数替换后的函数体为：

$$
\sigma \left(\operatorname {B o d y} _ {f}\right) = \left\{\sigma (s) \mid s \in \operatorname {B o d y} _ {f} \right\} \subseteq S ^ {\prime}. \tag {2}
$$

![](images/e4a51de00987cf6f9f02f7ba46506523faafae0bf6cd8b85bd048b927c8f600a.jpg)  
图 3. 函数内联。

(2) 返回规范化：我们定义一个作用于语句的转换函数 $\tau : S  S$：

$$
\tau (s) = \left\{ \begin{array}{l l} \text {r e s u l t} = \exp & \text {i f} s \equiv \text {r e t u r n} \exp , \\ \text {r e s u l t} = \text {N o n e} & \text {i f} s \equiv \text {r e t u r n}, \\ s & \text {o t h e r w i s e .} \end{array} \right. \tag {3}
$$

将 $\tau$ 提升到语句集合层面，我们得到规范化后的函数体：

$$
\tau (\text {B o d y}) = \{\tau (s) \mid s \in \text {B o d y} \}. \tag {4}
$$

(3) 赋值重定向：假设原始调用点的形式为 $\textsf { x } = \textsf { f } ( a _ { 1 } , \ldots \ldots , a _ { m } )$ 。经过参数替换和返回规范化后，该赋值被重定向到 $\times \ =$ 结果，将调用结果绑定到调用者的变量。
(4) 内联展开：转换后的被调用者函数体通过顺序应用参数替换 $\sigma$（定义于公式1）和返回规范化 $\tau$（定义于公式3）得到：

$$
\operatorname {B o d y} _ {f} ^ {*} = \tau (\sigma (\operatorname {B o d y} _ {f})). \tag {5}
$$

内联展开用 Body∗?? 替换原始调用，同时保留调用者函数中的缩进和周围的语法结构。

此内联过程确保了语义等价，同时使目标函数的预期行为在上下文中变得明确。通过将草稿实现直接嵌入到其上游调用者函数体中，该过程将分布式的、结构化的跨文件调用关系集合转换为一个单一的、线性化的函数局部环境。因此，LLM获得了一个紧凑的、面向执行的目标函数角色视图，这有助于推断输入/输出预期，保持计算的逻辑流程，并突出变量与控制结构之间的关系。这种转换还减少了歧义，并消除了单独检索代码片段所固有的干扰，使模型能够专注于目标函数在其仓库上下文中的基本行为模式。

3.3.2 下游检索。下游检索旨在为LLM提供目标函数的依赖函数。虽然草稿最初可能从头开始实现功能，但高质量的代码通常依赖于仓库内现有的函数。为了识别这些依赖函数，我们考虑两个互补的来源：(i) 解析草稿的AST以提取所有被调用的函数调用，记为 $Q _ { \mathrm { A S T } }$ ，以及 (ii) 收集LLM生成的预测被调用者列表，记为 $Q _ { \mathrm { L L M } }$ 。然后我们显式地取它们的并集来构建整体查询词汇表：

$$
Q = Q _ {\mathrm {A S T}} \cup Q _ {\mathrm {L L M}} = \left\{q _ {1}, q _ {2}, \dots , q _ {m} \right\}, \tag {6}
$$

其中每个 $q _ { i }$ 表示一个候选函数名。给定一个表示为函数单元集合 $\mathcal { F } = \{ f _ { 1 } , f _ { 2 } , . . . , f _ { n } \}$ 的仓库，每个单元都有一个关联的函数标识符名称 $( f _ { j } )$ ，我们应用一种基于子串的检索策略：

$$
\mathcal {G} = \left\{f _ {j} \in \mathcal {F} \mid \exists q _ {i} \in Q, q _ {i} \subseteq \operatorname {n a m e} \left(f _ {j}\right) \right\}. \tag {7}
$$

其中 $\mathcal { G }$ 表示候选下游函数集合。$\mathcal { G }$ 最终用于形成下游上下文，为提示提供增强。为了防止数据泄露，我们将目标函数本身从 $\mathcal { G }$ 中排除。目标是最大化覆盖目标函数可能利用的潜在有用的仓库API，从而为LLM提供更丰富、更准确的实现环境。

因此，下游检索通过确保检索到的函数与模型的实际生成轨迹紧密对齐，弥合了嘈杂的、从头开始的草稿与基于仓库知识的简洁、高质量解决方案之间的差距。这个过程使系统能够在需要时精确地呈现最相关的实用函数，避免了检索不足（遗漏关键API）和检索过度（引入无关噪声）。因此，LLM配备了一个有针对性的、上下文连贯的函数集合，这最大化了仓库知识的重用，并最终促进了更高质量的、与仓库一致的代码生成。

# 3.4 上下文感知代码生成

在收集了草案实现和增强的上下文信息后，我们引导大语言模型生成最终代码。

我们允许模型以双重模式运行：它可以复用初始草案，也可以基于增强的上下文对其进行改进。草案是一个有价值的起点，但可能包含不准确或不完整的逻辑。为了校准模型应在多大程度上依赖此草案，我们引入了一种基于困惑度的置信度机制[19]。对于一个基于基础提示??生成的草案实现$R = \left( r _ { 1 } , \ldots , r _ { M } \right)$，其困惑度定义为：

$$
\operatorname {P P L} (R \mid B) = \exp \left(- \frac {1}{M} \sum_ {j = 1} ^ {M} \log p \left(r _ {j} \mid B, r _ {<   j}\right)\right). \tag {8}
$$

其中$p ( r _ { j } \mid B , r _ { < j } )$表示语言模型估计的条件概率。这个公式提供了一个直接的置信度度量：较低的PPL(?? | ??)值表示模型对草案的置信度更高。

我们根据困惑度将模型对草案代码的置信度（第3.4节）分为三个等级：低置信度$\mathrm { ( P P L > 2 ) }$）、中等置信度（PPL∈[1.3, 2]）和高置信度$( \mathrm { P P L } { < } 1 . 3 )$。阈值经过精心调整，使得大约$4 0 \%$的样本落入低置信度组，$4 0 \%$落入中等置信度组，$2 0 \%$落入高置信度组。

在高置信度（低困惑度）的情况下，模型被提示信任并严格遵循草案。当草案获得中等置信度时，模型被建议修改或改进草案。在低置信度的情况下，模型被提示批判性地重新评估草案，并可以自由地从头开始重新生成。每个置信度等级都映射到一个集成到最终提示中的自然语言指导：

• 高置信度：“当前实现和注释都很好，请参考它并保留这些注释。”
• 中等置信度：“当前实现有些不确定，但注释是合理的。请部分参考它。”
• 低置信度：“当前实现不太确定是否正确。请考虑重新生成它。”

如图5所示，最终提示聚合了所有上下文信号，包括导入项、增强的上下文、生成模式指导、草案和目标签名。这种结构化提示为大语言模型提供了多视角视图：仓库依赖关系、使用模式、先前的草案指导以及明确的任务规范，使模型能够生成一个在上下文中立足、语义一致且具备仓库感知的最终函数体。

图4展示了一个说明整个工作流程的实际示例。（1）模型生成了一个复杂的草案，试图从头开始重新实现深度优先搜索过程，而没有利用仓库中现有的实用工具。（2）基于此草案响应，提取了两个潜在的被调用函数来源——从AST解析出的函数调用和LLM预测的被调用函数——它们被统一为一个查询集??。（3）然后通过子字符串匹配，使用此查询在仓库的知识库中进行搜索，得到一个下游函数的候选集$c$。在这些检索到的函数中，系统识别出现有的实用工具dfs_paths。（4）在下一阶段，此下游信息$c$作为额外上下文注入到提示中。（5）然后引导模型执行最终的上下文感知代码生成。

# 最终上下文增强代码生成的提示模板



请完成代码库中部的 {target} 函数。同时提供目标函数中调用的下游函数。

函数上方的上下文为：{dependencies}{context_below}{context_above} 函数下方的上下文为：{import statements}

以下是调用目标函数的函数示例，以及将当前目标函数内联到调用函数中的结果。请确保您的实现在内联到调用函数时能够良好适配。

调用函数 [0]：

{upstream_function}

以下是内联结果：{ inlined_result}

调用函数 [1]:……

以下是有用的下游函数：

下游函数 [0]：

{downstream_function}

下游函数 [1]: ……

以下是目标函数的当前版本：

{guidance_Info}

{draft solution}

待完成的代码为：{target_signature} {docstring}

输入-输出参数：{argument_prompt}

![](images/0ce08ce58bb1eefe02e3e1e6165b62e445fd02d67a6bbe0a533cc945d76ea0a8.jpg)

内联上下文增强

![](images/64a88dd92e8c25f27895f1bb01e1cba25749bffa8233413409353a9d69535ed1.jpg)  
图 5. 最终上下文增强代码生成的提示模板。

基础提示

响应应遵循以下示例的格式：{JSON_example}请务必严格遵守此格式。响应应为一个有效的 JSON 对象。

您的响应：

# 4 实验设置



我们通过解决以下研究问题（RQs）来全面评估 InlineCoder 的有效性：

RQ1（整体有效性）：与最先进的基线方法相比，InlineCoder 在仓库级代码生成任务上的表现如何？   
RQ2（消融研究）：InlineCoder 的关键组件对其整体性能的贡献程度如何？   
RQ3（定性分析）：InlineCoder 中的上下游检索机制如何为代码生成提供有效的上下文？   
RQ4（领域泛化）：InlineCoder 的性能在不同编程领域间的泛化能力如何？

# 4.1 数据集



我们在两个重要的仓库级代码生成基准测试上进行了实验：DevEval [27] 和 REPOEXEC [23]。我们专注于补全未完成函数的整个函数体。

• DevEval 是一个与现实世界代码库对齐的仓库级基准测试，它提供了来自10个领域、115个仓库的1,825个Python标注样本，用于系统性地评估大语言模型的编码能力。
• REPOEXEC 是一个用于仓库级代码生成的基准测试，它提供了355个带有真实标注的Python函数。

# 4.2 评估指标

遵循代码仓库级代码生成研究的既定实践[6, 32, 63]，我们使用以下指标从多个维度评估生成代码的质量。令 $y$

表示参考代码片段（真实值），$\tilde { y }$ 表示模型生成的代码。从代码片段 $y$ 中提取标识符（如变量名、API调用和函数名）构成集合 $I ( y )$ 。这些定义构成了以下评估指标的基础。

• 精确匹配（EM）检查生成的代码是否与参考片段完全一致，产生一个二元分数。
• 编辑相似度（ES）[22] 基于莱文斯坦距离提供更细粒度的度量，计算公式为

$$
\operatorname {E S} (y, \tilde {y}) = 1 - \frac {\operatorname {L e v} (y , \tilde {y})}{\max  (| y | , | \tilde {y} |)}, \tag {9}
$$

其中 $\operatorname { L e v } ( y , \tilde { y } )$ 表示 $y$ 与 $\tilde { y }$ 之间的莱文斯坦距离，定义为将 $y$ 转换为 $\tilde { y }$ 所需的最小插入、删除或替换次数。

• BLEU [43] 评估候选文本与参考文本之间的n-gram重叠度，定义为

$$
\mathrm {B L E U} = \mathrm {B P} \cdot \exp \left(\sum_ {n = 1} ^ {N} w _ {n} \log p _ {n}\right), \tag {10}
$$

其中 $\scriptstyle { { \mathcal { P } } _ { n } }$ 是修正后的n-gram精确率，$w _ { n }$ 是权重（通常取均匀权重，$\begin{array} { r } { w _ { n } = \frac { 1 } { N } , } \end{array}$），${ \mathrm { B P } } = \operatorname* { m i n } \left( 1 , e ^ { 1 - { \frac { \left| { \tilde { y } } \right| } { \left| { y } \right| } } } \right)$ 是简洁惩罚因子。

• 标识符匹配F1（ID.F1）[32] 以F1分数评估标识符级别的重叠度，例如API和变量名。令 $I ( y )$ 和 $I ( \tilde { y } )$ 分别表示从参考代码和生成代码中提取的标识符集合。精确率、召回率和ID.F1分数定义为

$$
P r e c i s i o n = \frac {\left| I (y) \cap I (\tilde {y}) \right|}{\left| I (\tilde {y}) \right|}, \quad R e c a l l = \frac {\left| I (y) \cap I (\tilde {y}) \right|}{\left| I (y) \right|}, \quad I D. F 1 = \frac {2 \cdot P r e c i s i o n \cdot R e c a l l}{P r e c i s i o n + R e c a l l}. \tag {11}
$$

我们没有采用基于执行的指标，例如Pass@k（生成代码在测试用例上的通过率）。与编程竞赛基准[9, 38]不同，仓库级代码补全任务在结构和依赖关系上存在显著差异[13]。在我们的实验中，我们还观察到基于执行的分数在不同运行间波动很大。相同的模型输出常常由于与模型本身无关的细微环境问题而导致测试失败。这些波动可能导致误导性或不可比较的Pass@k结果。

# 4.3 基线方法

我们将InlineCoder与一系列涵盖多种技术的基线方法进行比较，包括文件内上下文方法、基于文本相似性的检索方法以及基于静态分析的方法。

• In-File 利用完整的文件内上下文，而不使用任何跨文件信息。  
• Vanilla 遵循现有基准测试（如DevEval [27]和RepoExec [23]）中提供的基本提示构建方式，其中仅将相关的仓库上下文简单前置在目标函数之前，未进行深度整合。  
• RepoCoder [63] 是一种检索增强框架，通过迭代结合基于相似性的检索与代码大语言模型，以利用仓库级上下文进行代码补全。具体而言，我们实现了其函数体补全流程，并使用UniXcoder1 [14]作为嵌入模型。在评估时，我们采用了第三次检索迭代阶段的结果，因为原文献报告此阶段效果最佳。

表1. DevEval数据集上的性能比较。表现最佳的基线方法已用下划线标出。

<table><tr><td rowspan="2">Methods</td><td colspan="4">DeepSeek-V3</td><td colspan="4">Qwen3-Coder</td><td colspan="4">GPT5-mini</td></tr><tr><td>EM</td><td>ES</td><td>BLEU</td><td>ID.F1</td><td>EM</td><td>ES</td><td>BLEU</td><td>ID.F1</td><td>EM</td><td>ES</td><td>BLEU</td><td>ID.F1</td></tr><tr><td>In-File</td><td>7.56</td><td>59.81</td><td>43.58</td><td>71.54</td><td>7.95</td><td>56.15</td><td>40.07</td><td>68.75</td><td>0.85</td><td>40.87</td><td>19.93</td><td>51.56</td></tr><tr><td>Vanilla</td><td>11.45</td><td>66.20</td><td>52.64</td><td>76.99</td><td>9.86</td><td>60.02</td><td>46.49</td><td>74.92</td><td>4.34</td><td>58.32</td><td>42.93</td><td>64.43</td></tr><tr><td>RepoCoder</td><td>11.12</td><td>68.61</td><td>55.19</td><td>77.26</td><td>2.90</td><td>45.00</td><td>29.09</td><td>72.57</td><td>3.65</td><td>59.50</td><td>43.72</td><td>62.40</td></tr><tr><td>GraphCoder</td><td>1.91</td><td>67.71</td><td>46.89</td><td>66.56</td><td>0.00</td><td>59.85</td><td>35.03</td><td>61.87</td><td>3.21</td><td>55.99</td><td>37.72</td><td>61.85</td></tr><tr><td>DRACO</td><td>0.64</td><td>47.72</td><td>28.06</td><td>46.17</td><td>0.00</td><td>51.91</td><td>31.25</td><td>41.12</td><td>1.27</td><td>42.93</td><td>23.60</td><td>45.19</td></tr><tr><td>InlineCoder</td><td>11.56</td><td>70.50</td><td>57.12</td><td>78.01</td><td>11.23</td><td>67.39</td><td>53.30</td><td>76.91</td><td>4.45</td><td>65.21</td><td>46.72</td><td>65.45</td></tr></table>

• DRACO [6] 通过数据流引导的检索增强仓库级代码补全，构建仓库特定的上下文图，为大语言模型提供精确且相关的信息。我们已调整此基线方法的提示模板，以支持完整的函数体补全任务。  
• GraphCoder [32] 采用基于图的检索-生成框架，利用代码上下文图和从粗到细的检索过程，以更有效地获取仓库特定知识。我们已调整此基线方法的提示模板，以支持完整的函数体补全任务。

# 4.4 实现细节

在草稿生成阶段，我们采用了与各数据集基线方法相同的Vanilla提示：即分别使用DevEval和RE-POEXEC提供的基础提示构建方法。对于上下文检索，我们借助Tree-Sitter2和Pydepcall3解析Python代码并构建调用图。

为了在不同模型上评估我们的框架，我们使用了三种先进的主干大语言模型：DeepSeek- $\cdot \vee 3 ^ { 4 }$ [30]、Qwen3-Coder5 [60] 和 GPT-5-mini6 [41]。我们采用 Qwen2.5-Coder- $1 . 5 \mathrm { B } ^ { 7 }$ [18] 作为最终阶段置信度估计的概率估计器。我们将每个模型配置为其原生上下文窗口大小以适应长输入序列，因为我们的评估任务需要大量上下文但生成简洁输出。配置的输入限制为：DeepSeek-V3 128 000个词元，Qwen3-Coder 262 144个词元，GPT-5-mini 400 000个词元。所有模型的输出生成均限制在10 000个词元以内，以确保生成的完整性。为保证确定性和可复现的解码，所有模型均使用温度为0.0，这使得top- $\mathcal { P }$ 采样参数失效。所有实验均在配备Intel Xeon Silver 4214R CPU和NVIDIA A40 GPU的计算服务器上运行。

# 5 实验结果

# 5.1 研究问题一：整体有效性

表1和表2比较了不同方法在三种骨干模型上于DevEval和RepoExec数据集上的性能表现。

表2. REPOEXEC数据集上的性能比较。表现最佳的基线方法已用下划线标出。

<table><tr><td rowspan="2">Methods</td><td colspan="4">DeepSeek-V3</td><td colspan="4">Qwen3-Coder</td><td colspan="4">GPT5-mini</td></tr><tr><td>EM</td><td>ES</td><td>BLEU</td><td>ID.F1</td><td>EM</td><td>ES</td><td>BLEU</td><td>ID.F1</td><td>EM</td><td>ES</td><td>BLEU</td><td>ID.F1</td></tr><tr><td>In-File</td><td>0.56</td><td>53.80</td><td>30.94</td><td>71.87</td><td>0.85</td><td>53.36</td><td>33.18</td><td>69.84</td><td>0.00</td><td>24.98</td><td>5.07</td><td>53.59</td></tr><tr><td>Vanilla</td><td>0.85</td><td>54.63</td><td>31.57</td><td>72.50</td><td>1.63</td><td>54.96</td><td>34.17</td><td>70.91</td><td>0.00</td><td>24.47</td><td>4.79</td><td>57.22</td></tr><tr><td>RepoCoder</td><td>0.28</td><td>53.01</td><td>30.43</td><td>72.08</td><td>1.69</td><td>56.75</td><td>36.13</td><td>71.17</td><td>0.00</td><td>33.87</td><td>13.33</td><td>57.63</td></tr><tr><td>GraphCoder</td><td>0.00</td><td>39.69</td><td>14.37</td><td>48.65</td><td>0.00</td><td>30.68</td><td>9.00</td><td>51.98</td><td>0.00</td><td>40.19</td><td>14.88</td><td>45.11</td></tr><tr><td>DRACO</td><td>0.28</td><td>52.98</td><td>29.25</td><td>47.29</td><td>0.00</td><td>55.27</td><td>33.72</td><td>48.08</td><td>0.00</td><td>33.55</td><td>12.28</td><td>51.83</td></tr><tr><td>InlineCoder</td><td>2.22</td><td>62.01</td><td>43.41</td><td>72.84</td><td>2.54</td><td>59.20</td><td>37.53</td><td>71.26</td><td>0.00</td><td>49.27</td><td>29.06</td><td>57.65</td></tr></table>

总体而言，InlineCoder在所有三种骨干模型上均取得了显著且稳定的改进。值得注意的是，与Vanilla相比，InlineCoder实现了稳定的性能提升；Vanilla是一种基线方法，也被用于InlineCoder的草稿生成阶段。为了量化这些增益，我们计算了每种骨干模型相对于最强基线的相对百分比改进，然后报告了三种模型上的平均结果。在DevEval上，平均相对改进在EM指标上达到$5 . 1 3 \%$，在ES指标上达到$\mathbf { 1 0 . 8 6 \% }$，在BLEU指标上达到$1 0 . 6 7 \%$；在RepoExec上，增益更为显著，EM指标为$2 9 . 7 3 \%$，ES指标为$2 0 . 8 2 \%$，BLEU指标为$4 9 . 3 4 \%$，这突显了InlineCoder在模型和数据集间的鲁棒性。

仅使用文件内上下文的In-File基线方法仍具有竞争力，有时甚至优于GraphCoder和DRACO。这表明保留局部上下文至关重要。相比之下，GraphCoder和DRACO通常表现不佳，因为它们最初是为行级代码补全设计的，并且依赖于一些在函数体生成任务中不成立的假设（例如，部分函数体或数据流分析）。此外，它们丢弃了文件内上下文，而这些上下文可能包含关键的局部信息，这进一步限制了它们在仓库级代码生成中的有效性。

我们注意到，本实验中的EM分数相较于先前工作中报告的结果相对较低。这种差异源于补全目标的不同：先前研究主要评估单行补全，而我们的任务需要补全整个函数体，这本质上更具挑战性。

# 对研究问题一的回答



InlineCoder在所有基线方法上均展现出显著优势，在不同数据集和模型上均实现了持续的性能提升。这些结果凸显了上下文内联技术在提升仓库级代码生成效果方面的有效性。

# 5.2 RQ2：消融研究

我们在DevEval数据集上使用DeepSeek-V3主干网络进行了消融实验。消融的变体包括：移除上游上下文检索（w/o upstream）、移除使用上下文内联（w/o inline）、移除下游上下文检索（w/o downstream）、移除基于草稿困惑度得出的置信度声明（w/o confidence），以及在上下文感知代码生成中移除草稿实现本身（w/o draft）。

如表3所示，移除任何关键组件都会导致性能下降，这证实了它们的有效性。移除草稿实现导致的下降幅度最大，表明将生成过程锚定于具体候选方案对于准确性和语义对齐至关重要。移除内联以及上游/下游上下文同样会持续降低性能，突显了它们的互补作用。值得注意的是，w/o inline的性能与

表3. DevEval数据集上数据流分析的消融研究   

<table><tr><td rowspan="2">Configuration</td><td colspan="4">DeepSeek-V3</td></tr><tr><td>EM</td><td>ES</td><td>BLEU</td><td>ID.F1</td></tr><tr><td>InlineCoder</td><td>11.56</td><td>70.50</td><td>57.12</td><td>78.01</td></tr><tr><td>w/o upstream</td><td>9.48 (-2.12)</td><td>65.12 (-5.38)</td><td>51.34 (-5.78)</td><td>77.43 (-0.58)</td></tr><tr><td>w/o inline</td><td>9.15 (-2.41)</td><td>65.95 (-4.55)</td><td>52.35 (-4.77)</td><td>78.01 (0.00)</td></tr><tr><td>w/o downstream</td><td>9.75 (-1.81)</td><td>65.87 (-4.63)</td><td>52.25 (-4.87)</td><td>77.60 (-0.41)</td></tr><tr><td>w/o confidence</td><td>10.74 (-0.82)</td><td>67.79 (-2.71)</td><td>54.24 (-2.88)</td><td>77.30 (-0.71)</td></tr><tr><td>w/o draft</td><td>7.67 (-3.89)</td><td>59.09 (-11.41)</td><td>44.24 (-12.88)</td><td>76.29 (-1.72)</td></tr></table>

表4. 返回语句最后一行的比较   

<table><tr><td>Methods</td><td>EM</td><td>BLEU</td><td>ES</td></tr><tr><td>Vanilla</td><td>35.40</td><td>50.17</td><td>58.72</td></tr><tr><td>RepoCoder</td><td>37.15</td><td>52.77</td><td>61.57</td></tr><tr><td>InlineCoder</td><td>37.92</td><td>53.80</td><td>62.51</td></tr></table>

w/o upstream的性能相当，这表明如果上游信息未能被适当线性化，其单独提供的效益有限。最后，移除置信度声明会导致适度但稳定的性能下降，说明基于困惑度的评分有助于选择更有效的提示。

# 对研究问题二的回答



InlineCoder的每个提议组件都对性能产生积极贡献。草稿实现发挥着最关键的作用，函数使用上下文内联对于有效利用上下文信息至关重要，而跨文件检索（上游和下游）则提供了补充性增益。这证实了InlineCoder受益于精心设计的上下文信号整合。

# 5.3 RQ3: 定性分析

5.3.1 返回语句性能提升。为了进一步研究上游上下文在函数补全中的作用，我们重点关注返回语句的生成，该语句通常位于目标函数的最后一行。具体而言，我们从基线生成结果和 InlineCoder 中提取代码的最后一行，并根据参考代码评估其准确性。遵循单行代码评估的常见做法，我们采用 EM、BLEU 和 ES 作为评估指标，这些指标均在 4.2 节中介绍。实验在 DevEval 数据集上使用 DeepSeek-V3 主干网络进行。我们将 InlineCoder 与两种代表性方法进行比较：Vanilla 和 RepoCoder（一种利用多次生成的强基线）。

如表 4 所示，InlineCoder 在所有指标上均持续取得最佳性能。特别是，InlineCoder 在返回语句上将 EM 分数提高了 $2 . 0 7 \%$。虽然 RepoCoder 也利用了迭代生成，但其表现仍不及 InlineCoder，这表明仅靠简单的多次生成是不够的。相反，结合结构化的上游使用信息能为生成准确的最终语句提供更可靠的指导。这些发现证实了上游信息在塑造返回表达式的正确性和自然性方面起着至关重要的作用，这补充了早期实验中展示的内联和检索策略的优势。

表 5. 调用语句对比

<table><tr><td>Methods</td><td>EM</td><td>Jaccard</td><td>F1</td><td>Coverage</td><td>DIR</td></tr><tr><td>Vanilla</td><td>29.86</td><td>53.10</td><td>60.67</td><td>63.16</td><td>69.21</td></tr><tr><td>RepoCoder</td><td>21.48</td><td>52.80</td><td>63.01</td><td>65.13</td><td>70.45</td></tr><tr><td>InlineCoder</td><td>30.74</td><td>54.99</td><td>62.88</td><td>65.40</td><td>71.86</td></tr></table>

5.3.2 函数调用语句性能提升。为了研究下游信息在提高函数调用正确性方面的作用，我们使用 DevEval 数据集和 DeepSeek-V3 主干网络，对生成的调用语句进行了针对性评估。对于每个生成的函数，我们提取所有调用语句，并将其与参考标注进行比较。我们采用了多种评估指标来衡量这种对齐程度，包括 EM、Jaccard 相似度、F1 分数、覆盖率和下游调用召回率（DIR）[23]。这些指标共同衡量了被调用方名称和完整调用实例的准确性和完整性。为了进行比较，我们还对 Vanilla、RepoCoder 和 InlineCoder 进行了实验。

如表 5 所示，所提出的上下文感知生成方法（InlineCoder）取得了总体最佳性能。特别是，InlineCoder 在函数调用语句上将 EM 提高了 $4 . 2 7 \%$。这些结果表明，结合下游信息能显著提高调用语句的正确性和覆盖率，从而增强生成代码的功能可靠性。

# 对研究问题三的解答



InlineCoder在多项评估指标上显著提升了返回语句和函数调用语句的准确性，这证明了其通过内联上下文利用上下游信息的新颖方法的有效性。

# 5.4 研究问题四：领域泛化

为了进一步探究我们方法在不同领域间的泛化能力，我们采用 DevEval [27] 数据集提供的领域分类法，并评估了四个指标：精确匹配率、编辑相似度、BLEU 和 ID.F1。实验在 DevEval 数据集上使用 DeepSeek-V3 主干网络进行。十个领域的结果总结于图 6。

在精确匹配率方面，InlineCoder 在十个领域中的九个取得了最佳性能。在编辑相似度方面，它在八个领域优于基线。在 BLEU 指标上，InlineCoder 在九个领域领先，而在 ID.F1 指标上，它在所有十个领域均取得了最佳结果。与 Vanilla 基线相比，InlineCoder 在几乎所有领域都表现出一致的改进。

唯一相对较弱的性能出现在科学与工程领域，这可能归因于该领域的特性：其任务主要面向科学计算，其中跨函数调用结构相对稀疏。因此，我们方法所利用的下游和上游信息在该领域提供的额外收益有限。

![](images/024da0440122d96a6f22eb72e293d609ba75e89d752627d804273ca9e671e852.jpg)
图 6. 各领域有效性对比。

# 对研究问题四的解答



InlineCoder在不同领域展现出强大的泛化能力，在几乎所有实验设置中均持续超越基线模型。结果表明，内联的上游与下游信号能够提供稳定的性能提升，即使在多样化的代码库结构下亦是如此。

# 5.5 案例研究

图7展示了一项将InlineCoder与其他基线方法进行比较的案例研究。待补全的目标函数是 parse_unique_urlencoder。该图以 $2 \times 5$ 网格形式组织，其中顶行展示了不同方法从代码库中检索到的关键上下文信息，底行则展示了真实参考实现以及InlineCoder和基线方法生成的代码。

本案例研究证明了InlineCoder在捕获上游和下游上下文方面的有效性。通过函数内联，InlineCoder成功识别并利用了直接影响实现正确性的关键上下文信息。相比之下，基线方法如依赖基于相似性检索的RepoCoder，以及采用数据流分析的DRACO，它们检索到的上下文信息虽然在结构上相关，但对于具体的实现任务效用有限。

我们方法的优势在以下两个关键方面尤为明显。首先，在处理下游依赖时，只有InlineCoder正确地使用了带有适当参数的 parse_qs 工具函数。虽然RepoCoder尝试使用名称相似的 parse_qsl 函数，但其参数用法与参考实现存在显著差异。这种API使用的精确性直接源于InlineCoder的下游检索机制，该机制不仅能识别正确的工具函数，还能捕获其实现细节，从而确保准确的功能名称和参数规范。其次，InlineCoder在处理返回值方面表现出有效性。如案例所示，InlineCoder始终能生成正确的返回类型 dict。

![](images/08785091b4e629bdabb4ee6795cccb2544aa9e923a46c4d8aacf26835948318b.jpg)  
图7. 关于双向调用内联有效性的案例。

![](images/a4ef8defe70210b851f3c9fe4e57356458cd75f9d7c18e27ca5c679e02c334a8.jpg)  
图8. 关于置信度引导对缓解自我重复偏差影响的案例。

相比之下，基线方法表现出不一致的行为——有时返回 dict，但也频繁产生 str、int 或 None。这种返回类型处理的准确性是通过InlineCoder的上游内联实现的，该机制识别出了调用者函数 safe_parse_query。

图8提供了另一个关于我们的置信度陈述如何缓解锚定偏差的案例。在“基础生成”中，LLM默认采用通用先验知识（例如 packet.timestamp），而非捕获增强的上下文信息。在没有置信度引导的情况下，模型表现出强烈的自我重复，尽管存在正确的内联上下文，它仍逐字复制其初始的错误草稿。

相反，当InlineCoder将草稿识别为中等置信度的结果时，它会附加一个置信度陈述。这将任务从简单的生成重新定义为主动修改，迫使LLM根据内联信息重新评估其草稿。因此，模型成功地识别了结构上的差异并采用了正确的约定，这表明虽然上下文内联提供了必要的知识，但置信度引导是确保代码库级别的信息被利用、而非被初始模型偏差所掩盖的关键触发因素。

![](images/f95dbc5b6d0c20133255909927cf635647340fa104029011d832fb209b637df9.jpg)  
图9. 不同上下文环境中的有效性比较。

# 6 讨论

# 6.1 不同上下文环境下的性能分析



图9展示了代码库环境如何影响InlineCoder的有效性。为了量化这种影响，我们在DevEval数据集上进行了分层分析——该数据集是从GitHub上的真实Python项目中精选出的基准——使用DeepSeek-V3模型，根据样本固有的结构特征将其分为四组：上游 $( 1 6 . 3 8 \% )$ ）、下游 $\left( 1 5 . 2 9 \% \right)$ 、上下游 $( 6 . 0 3 \% )$ 和无上下文 $( 7 4 . 3 6 \% )$ 。其中，无上下文组代表那些在其原始代码库中天然缺乏调用者-被调用者依赖关系的孤立函数，而非人为移除其上下文的结果。

结果表明，在几乎所有场景中，InlineCoder的表现都持续优于基线方法。值得注意的是，我们观察到无上下文设置下的总体得分通常高于依赖上下文的类别。这归因于没有上游或下游关系的函数通常是独立的，因此对代码库范围信息的依赖较低。这些独立任务固有的简单性导致了较高的基线性能。相反，在复杂的代码库环境（即存在调用者-被调用者关系的环境）中观察到的较低分数表明，主要挑战在于模型难以理解和整合复杂的结构上下文。

此外，在这四个类别中，InlineCoder在上游设置中取得了最显著的性能提升。这一实质性改进从经验上验证了我们的设计在捕获和利用上游调用者信息方面的有效性。

# 6.2 有效性威胁



与大多数现有的仓库级代码生成基准测试类似[8, 20, 23, 26, 27, 61, 63]，我们的实证评估是在Python仓库上进行的，这可能限制了我们研究结果对其他编程语言或不同类型软件项目的普适性。我们通过两种方式缓解这一威胁。首先，我们在两个涵盖多个领域和项目规模的不同数据集上评估我们的方法。其次，InlineCoder的基本原理——利用上游使用上下文和下游依赖上下文——是与语言无关的。该框架依赖于抽象语法树（AST）分析，这是一种适用于几乎所有现代编程语言的标准技术。尽管我们的实现是针对Python的，但其核心方法可以轻松扩展到其他编程语言，例如Java、$\mathrm { C } { + } { + }$或TypeScript。在诸如$\mathrm { C } { + } { + }$等强类型语言中，AST分析还可以提供更多的上游和下游信息。

# 7 相关工作

代码大语言模型（Code Large Language Models，LLMs），例如 Code Llama [47]、DeepSeek-Coder [15] 和 Qwen-Coder [18]，已在自动化软件开发任务中展现出显著潜力 [2, 3, 5, 12, 17, 25, 35, 39, 40, 46, 52, 56, 67, 68]。通过将海量代码语料库中的广泛知识内化到数十亿参数中，这些模型能够解决各种通用编程问题 [21, 34, 49, 51, 62]。基于这些基础能力，仓库级代码生成已取得显著进展 [23, 27, 53, 63]，先前的工作大致可分为以下几类：检索增强生成 [53, 63]、基于图和结构化检索 [4, 32, 33]、智能体/迭代优化 [1, 7, 28]、静态分析引导提示 [6, 31] 以及微调 [58, 59]。

**检索增强生成。** 早期研究表明，从代码仓库中检索相关代码片段可以显著提高生成质量。RepoCoder [63]、RepoFuse [29] 和 RepoFusion [53] 等方法利用检索机制为模型提供仓库范围的上下文。LongCodeZip [50] 基于大语言模型固有的困惑度选择多个相关上下文。其他工作探索了提示选择策略，以从大型仓库中选择最有用的片段 [54]。这些方法确立了仓库级上下文的价值，但通常依赖于相似性或主题相关性，而非关系型调用图信号。

**基于图和结构化检索。** 为了捕捉超越词汇相似度的结构关系，一系列研究构建了代码的图表示。CodexGraph [33] 构建了支持结构化查询的代码图数据库，而 GraphCoder [32] 则使用上下文图对控制流和数据依赖关系进行建模。RepoHyper 及相关方法使用语义仓库级图，结合搜索-扩展-优化策略来定位相关代码元素 [4]。这些方法通过利用结构关系提高了检索精度；然而，它们主要面向识别结构相似或语义相关的代码片段，而非将明确的上游或下游使用信号纳入提示中。

**智能体与迭代优化。** 智能体框架和迭代规划器执行多步推理，并使用外部工具（静态分析、测试或执行）来优化输出。例如，CodeRAG 结合了双图与智能体推理，并配备了用于图遍历和代码测试的专用工具 [28]；RRR 允许使用静态分析进行迭代探索 [7]；CodePlan 则将仓库级编码视为一个具有增量依赖分析的规划问题 [1]。这些工作凸显了多步问题分解的优势，但并未系统性地利用调用图编码的调用者-被调用者信号作为提示增强。

**静态分析与上下文剪枝。** 一些工作结合静态分析来剪枝或丰富提示上下文。STALL $^ +$ 将静态分析集成到提示、解码和后处理阶段 [31]；DRACO 使用数据流引导的检索来聚焦于与流程相关的片段 [6]；分层方法则在函数粒度上对仓库进行建模，利用拓扑依赖关系来减少噪声上下文 [65]。这些技术增强了相关性并减少了噪声；然而，它们主要侧重于上下文选择或压缩，而非注入明确的上游/下游使用信息或源自初步模型输出的置信度信号。

**微调方法。** 其他研究方向专注于领域专用模型训练策略 [44]：RTLRepoCoder 针对 Verilog 代码补全进行微调 [63]，课程数据集则针对困难模式 [48]。也有研究致力于改进检索器（例如通过强化学习），并将检索与强化或反思性训练相结合 [57, 58]。

与这些工作相比，InlineCoder 引入了几个关键创新点。首先，与依赖表层相似性或静态结构的传统 RAG 或基于图的方法不同，我们的方法通过将未完成的函数内联到其调用栈中，将仓库级生成重新定义为函数级任务，从而动态捕获上游使用约束和下游依赖关系。其次，我们利用草稿补全作为锚点来驱动双向检索，实现精确的上下文集成，而无需大量微调。这使得迭代优化成为可能，从而提高了生成精度和仓库一致性，解决了现有方法中常常忽视函数依赖性和使用情况的正交维度这一局限性。

# 8 结论



本文提出了InlineCoder，一种新颖的仓库级代码生成框架，它通过内联代码仓库中的相关上游和下游上下文来增强大语言模型。通过系统性地整合来自函数调用者和被调用者的上下文信息，InlineCoder在特定仓库中为目标函数的环境提供了更丰富、更自然的理解。在DevEval和REPOEXEC数据集上进行的大量实验表明，InlineCoder在多项指标上持续优于强基线模型。消融实验和针对性分析证实，内联的核心创新——即同时纳入上游和下游上下文——是显著提升返回语句准确性和函数调用精度的主要驱动力。除了这些实证收益之外，InlineCoder在不同编程领域展现出强大的泛化能力，并且在集成不同骨干大语言模型时保持稳定的性能。

# 数据可用性



本研究中使用的所有代码和数据均公开于：https://github.com/ythere-y/InlineCoder。

# 致谢



本研究由国家重点研发计划（项目编号：2023YFB4503802）、国家自然科学基金（项目编号：62232003）以及上海市自然科学基金（项目编号：25ZR1401175）资助。

# 参考文献

[1] Ramakrishna Bairi, Atharv Sonwane, Aditya Kanade, Vageesh D C, Arun Iyer, Suresh Parthasarathy, Sriram Rajamani, Balasubramanyan Ashok, and Shashank Shet. 2024. Codeplan: Repository-level coding using llms and planning. Proceedings of the ACM on Software Engineering 1, FSE (2024), 675–698.
[2] Antonio Valerio Miceli Barone and Rico Sennrich. 2017. A parallel corpus of python functions and documentation strings for automated code documentation and code generation. arXiv preprint arXiv:1707.02275 (2017).
[3] Brett A Becker, Paul Denny, James Finnie-Ansley, Andrew Luxton-Reilly, James Prather, and Eddie Antonio Santos. 2023. Programming is hard-or at least it used to be: Educational opportunities and challenges of ai code generation. In Proceedings of the 54th ACM Technical Symposium on Computer Science Education V. 1. 500–506.
[4] Zhangqian Bi, Yao Wan, Zheng Wang, Hongyu Zhang, Batu Guan, Fangxin Lu, Zili Zhang, Yulei Sui, Hai Jin, and Xuanhua Shi. 2024. Iterative refinement of project-level code context for precise code generation with compiler feedback. arXiv preprint arXiv:2403.16792 (2024).
[5] Silin Chen, Shaoxin Lin, Xiaodong Gu, Yuling Shi, Heng Lian, Longfei Yun, Dong Chen, Weiguo Sun, Lin Cao, and Qianxiang Wang. 2025. Swe-exp: Experience-driven software issue resolution. arXiv preprint arXiv:2507.23361 (2025).
[6] Wei Cheng, Yuhan Wu, and Wei Hu. 2024. Dataflow-guided retrieval augmentation for repository-level code completion. arXiv preprint arXiv:2405.19782 (2024).
[7] Ajinkya Deshpande, Anmol Agarwal, Shashank Shet, Arun Iyer, Aditya Kanade, Ramakrishna Bairi, and Suresh Parthasarathy. 2024. Class-Level Code Generation from Natural Language Using Iterative, Tool-Enhanced Reasoning over Repository. arXiv preprint arXiv:2405.01573 (2024).

[8] Yangruibo Ding, Zijian Wang, Wasi Ahmad, Hantian Ding, Ming Tan, Nihal Jain, Murali Krishna Ramanathan, Ramesh Nallapati, Parminder Bhatia, Dan Roth, et al. 2023. Crosscodeeval: A diverse and multilingual benchmark for cross-file code completion. Advances in Neural Information Processing Systems 36 (2023), 46701–46723.
[9] Xueying Du, Mingwei Liu, Kaixin Wang, Hanlin Wang, Junwei Liu, Yixuan Chen, Jiayi Feng, Chaofeng Sha, Xin Peng, and Yiling Lou. 2024. Evaluating large language models in class-level code generation. In Proceedings of the IEEE/ACM 46th International Conference on Software Engineering. 1–13.
[10] Xinyu Gao, Yun Xiong, Deze Wang, Zhenhan Guan, Zejian Shi, Haofen Wang, and Shanshan Li. 2024. Preferenceguided refactored tuning for retrieval augmented code generation. In Proceedings of the 39th IEEE/ACM International Conference on Automated Software Engineering. 65–77.
[11] Yunfan Gao, Yun Xiong, Xinyu Gao, Kangxiang Jia, Jinliu Pan, Yuxi Bi, Yixin Dai, Jiawei Sun, Haofen Wang, and Haofen Wang. 2023. Retrieval-augmented generation for large language models: A survey. arXiv preprint arXiv:2312.10997 2, 1 (2023).
[12] Leonidas Gee, Milan Gritta, Gerasimos Lampouras, and Ignacio Iacobacci. 2024. Code-optimise: Self-generated preference data for correctness and efficiency. arXiv preprint arXiv:2406.12502 (2024).
[13] Xiaodong Gu, Meng Chen, Yalan Lin, Yuhan Hu, Hongyu Zhang, Chengcheng Wan, Zhao Wei, Yong Xu, and Juhong Wang. 2025. On the effectiveness of large language models in domain-specific code generation. ACM Transactions on Software Engineering and Methodology 34, 3 (2025), 1–22.
[14] Daya Guo, Shuai Lu, Nan Duan, Yanlin Wang, Ming Zhou, and Jian Yin. 2022. UniXcoder: Unified Cross-Modal Pretraining for Code Representation. In Findings of the Association for Computational Linguistics: ACL 2022. 2563–2575.
[15] Daya Guo, Qihao Zhu, Dejian Yang, Zhenda Xie, Kai Dong, Wentao Zhang, Guanting Chen, Xiao Bi, Yu Wu, YK Li, et al. 2024. DeepSeek-Coder: When the Large Language Model Meets Programming–The Rise of Code Intelligence. arXiv preprint arXiv:2401.14196 (2024).
[16] Mehadi Hassen and Philip K Chan. 2017. Scalable function call graph-based malware classification. In Proceedings of the Seventh ACM on Conference on Data and Application Security and Privacy. 239–248.
[17] Baizhou Huang, Shuai Lu, Weizhu Chen, Xiaojun Wan, and Nan Duan. 2023. Enhancing large language models in coding through multi-perspective self-consistency. arXiv preprint arXiv:2309.17272 (2023).
[18] Binyuan Hui, Jian Yang, Zeyu Cui, Jiaxi Yang, Dayiheng Liu, Lei Zhang, Tianyu Liu, Jiajun Zhang, Bowen Yu, Keming Lu, et al. 2024. Qwen2. 5-coder technical report. arXiv preprint arXiv:2409.12186 (2024).
[19] Fred Jelinek, Robert L Mercer, Lalit R Bahl, and James K Baker. 1977. Perplexity—a measure of the difficulty of speech recognition tasks. The Journal of the Acoustical Society of America 62, S1 (1977), S63–S63.
[20] Carlos E Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and Karthik Narasimhan. 2023. Swe-bench: Can language models resolve real-world github issues?, 2024. URL https://arxiv. org/abs/2310.06770 7 (2023).
[21] Majeed Kazemitabaar, Justin Chow, Carl Ka To Ma, Barbara J Ericson, David Weintrop, and Tovi Grossman. 2023. Studying the effect of AI code generators on supporting novice learners in introductory programming. In Proceedings of the 2023 CHI conference on human factors in computing systems. 1–23.
[22] VI Lcvenshtcin. 1966. Binary coors capable or ‘correcting deletions, insertions, and reversals. In Soviet physics-doklady, Vol. 10.
[23] Nam Le Hai, Dung Manh Nguyen, and Nghi DQ Bui. 2024. Repoexec: Evaluate code generation with a repository-level executable benchmark. arXiv e-prints (2024), arXiv–2406.
[24] Daniel Le Métayer and David Schmidt. 1996. Structural operational semantics as a basis for static program analysis. ACM Computing Surveys (CSUR) 28, 2 (1996), 340–343.
[25] Han Li, Yuling Shi, Shaoxin Lin, Xiaodong Gu, Heng Lian, Xin Wang, Yantao Jia, Tao Huang, and Qianxiang Wang. 2025. Swe-debate: Competitive multi-agent debate for software issue resolution. arXiv preprint arXiv:2507.23348 (2025).
[26] Jia Li, Ge Li, Xuanming Zhang, Yihong Dong, and Zhi Jin. 2024. Evocodebench: An evolving code generation benchmark aligned with real-world code repositories. arXiv preprint arXiv:2404.00599 (2024).
[27] Jia Li, Ge Li, Yunfei Zhao, Yongmin Li, Huanyu Liu, Hao Zhu, Lecheng Wang, Kaibo Liu, Zheng Fang, Lanshen Wang, et al. 2024. DevEval: A Manually-Annotated Code Generation Benchmark Aligned with Real-World Code Repositories. In Findings of the Association for Computational Linguistics ACL 2024. 3603–3614.
[28] Jia Li, Xianjie Shi, Kechi Zhang, Lei Li, Ge Li, Zhengwei Tao, Jia Li, Fang Liu, Chongyang Tao, and Zhi Jin. 2025. CodeRAG: Supportive Code Retrieval on Bigraph for Real-World Code Generation. arXiv:2504.10046 [cs.SE] https: //arxiv.org/abs/2504.10046
[29] Ming Liang, Xiaoheng Xie, Gehao Zhang, Xunjin Zheng, Peng Di, Hongwei Chen, Chengpeng Wang, Gang Fan, et al. 2024. Repofuse: Repository-level code completion with fused dual context. arXiv preprint arXiv:2402.14323 (2024).
[30] Aixin Liu, Bei Feng, Bing Xue, Bingxuan Wang, Bochao Wu, Chengda Lu, Chenggang Zhao, Chengqi Deng, Chenyu Zhang, Chong Ruan, et al. 2024. Deepseek-v3 technical report. arXiv preprint arXiv:2412.19437 (2024).
[31] Junwei Liu, Yixuan Chen, Mingwei Liu, Xin Peng, and Yiling Lou. 2024. Stall+: Boosting llm-based repository-level code completion with static analysis. arXiv preprint arXiv:2406.10018 (2024).

[32] Wei Liu, Ailun Yu, Daoguang Zan, Bo Shen, Wei Zhang, Haiyan Zhao, Zhi Jin, and Qianxiang Wang. 2024. Graphcoder: Enhancing repository-level code completion via code context graph-based retrieval and language model. arXiv preprint arXiv:2406.07003 (2024).
[33] Xiangyan Liu, Bo Lan, Zhiyuan Hu, Yang Liu, Zhicheng Zhang, Fei Wang, Michael Qizhe Shieh, and Wenmeng Zhou. 2025. CodexGraph: Bridging Large Language Models and Code Repositories via Code Graph Databases. In Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers), Luis Chiruzzo, Alan Ritter, and Lu Wang (Eds.). Association for Computational Linguistics, Albuquerque, New Mexico, 142–160. https://doi.org/10.18653/v1/2025.naacl-long.7
[34] Vadim Liventsev, Anastasiia Grishina, Aki Härmä, and Leon Moonen. 2023. Fully autonomous programming with large language models. In Proceedings of the Genetic and Evolutionary Computation Conference. 1146–1155.
[35] Ziyang Luo, Can Xu, Pu Zhao, Qingfeng Sun, Xiubo Geng, Wenxiang Hu, Chongyang Tao, Jing Ma, Qingwei Lin, and Daxin Jiang. 2023. Wizardcoder: Empowering code large language models with evol-instruct. arXiv preprint arXiv:2306.08568 (2023).
[36] Yingwei Ma, Qingping Yang, Rongyu Cao, Binhua Li, Fei Huang, and Yongbin Li. 2025. Alibaba lingmaagent: Improving automated issue resolution via comprehensive repository exploration. In Proceedings of the 33rd ACM International Conference on the Foundations of Software Engineering. 238–249.
[37] Jonathan I Maletic and Andrian Marcus. 2001. Supporting program comprehension using semantic and structural information. In Proceedings of the 23rd International Conference on Software Engineering. ICSE 2001. IEEE, 103–112.
[38] Erik Nijkamp, Bo Pang, Hiroaki Hayashi, Lifu Tu, Huan Wang, Yingbo Zhou, Silvio Savarese, and Caiming Xiong. 2022. Codegen: An open large language model for code with multi-turn program synthesis. arXiv preprint arXiv:2203.13474 (2022).
[39] Kristian B Ølgaard, Anders Logg, and Garth N Wells. 2009. Automated code generation for discontinuous Galerkin methods. SIAM Journal on Scientific Computing 31, 2 (2009), 849–864.
[40] Kristian B Ølgaard and Garth N Wells. 2010. Optimizations for quadrature representations of finite element tensors through automated code generation. ACM Transactions on Mathematical Software (TOMS) 37, 1 (2010), 1–23.
[41] OpenAI. 2025. Introducing GPT-5. https://openai.com/index/introducing-gpt-5/.
[42] Siru Ouyang, Wenhao Yu, Kaixin Ma, Zilin Xiao, Zhihan Zhang, Mengzhao Jia, Jiawei Han, Hongming Zhang, and Dong Yu. 2024. Repograph: Enhancing ai software engineering with repository-level code graph. arXiv preprint arXiv:2410.14684 (2024).
[43] Kishore Papineni, Salim Roukos, Todd Ward, and Wei-Jing Zhu. 2002. Bleu: a method for automatic evaluation of machine translation. In Proceedings of the 40th annual meeting of the Association for Computational Linguistics. 311–318.
[44] Huy N Phan, Hoang N Phan, Tien N Nguyen, and Nghi DQ Bui. 2025. Repohyper: Search-expand-refine on semantic graphs for repository-level code completion. In 2025 IEEE/ACM Second International Conference on AI Foundation Models and Software Engineering (Forge). IEEE, 14–25.
[45] Gordon D Plotkin. 2004. The origins of structural operational semantics. The Journal of Logic and Algebraic Programming 60 (2004), 3–15.
[46] Saurabh Pujar, Luca Buratti, Xiaojie Guo, Nicolas Dupuis, Burn Lewis, Sahil Suneja, Atin Sood, Ganesh Nalawade, Matt Jones, Alessandro Morari, et al. 2023. Automated code generation for information technology tasks in yaml through large language models. In 2023 60th ACM/IEEE Design Automation Conference (DAC). IEEE, 1–4.
[47] Baptiste Roziere, Jonas Gehring, Fabian Gloeckle, Sten Sootla, Itai Gat, Xiaoqing Ellen Tan, Yossi Adi, Jingyu Liu, Romain Sauvestre, Tal Remez, et al. 2023. Code llama: Open foundation models for code. arXiv preprint arXiv:2308.12950 (2023).
[48] Hitesh Sagtani, Rishabh Mehrotra, and Beyang Liu. 2024. Improving FIM Code Completions via Context and Curriculum Based Learning. arXiv:2412.16589 [cs.IR] https://arxiv.org/abs/2412.16589
[49] Freda Shi, Xinyun Chen, Kanishka Misra, Nathan Scales, David Dohan, Ed H Chi, Nathanael Schärli, and Denny Zhou. 2023. Large language models can be easily distracted by irrelevant context. In International Conference on Machine Learning. PMLR, 31210–31227.
[50] Yuling Shi, Yichun Qian, Hongyu Zhang, Beijun Shen, and Xiaodong Gu. 2025. LongCodeZip: Compress Long Context for Code Language Models. arXiv preprint arXiv:2510.00446 (2025).
[51] Yuling Shi, Songsong Wang, Chengcheng Wan, and Xiaodong Gu. 2024. From code to correctness: Closing the last mile of code generation with hierarchical debugging. arXiv preprint arXiv:2410.01215 (2024).
[52] Yuling Shi, Hongyu Zhang, Chengcheng Wan, and Xiaodong Gu. 2024. Between Lines of Code: Unraveling the Distinct Patterns of Machine and Human Programmers. In 2025 IEEE/ACM 47th International Conference on Software Engineering (ICSE). IEEE Computer Society, 51–62.
[53] Disha Shrivastava, Denis Kocetkov, Harm De Vries, Dzmitry Bahdanau, and Torsten Scholak. 2023. Repofusion: Training code models to understand your repository. arXiv preprint arXiv:2306.10998 (2023).

[54] Disha Shrivastava, Hugo Larochelle, and Daniel Tarlow. 2023. Repository-level prompt generation for large language models of code. In International Conference on Machine Learning. PMLR, 31693–31715.
[55] Weihang Su, Yichen Tang, Qingyao Ai, Zhijing Wu, and Yiqun Liu. 2024. DRAGIN: dynamic retrieval augmented generation based on the information needs of large language models. arXiv preprint arXiv:2403.10081 (2024).
[56] Rahul Vadisetty, Anand Polamarasetti, Sameerkumar Prajapati, Jinal Bhanubhai Butani, et al. 2023. Leveraging Generative AI for Automated Code Generation and Security Compliance in Cloud-Based DevOps Pipelines: A Review. Available at SSRN 5218298 (2023).
[57] Jicheng Wang, Yifeng He, and Hao Chen. 2024. RepoGenReflex: Enhancing Repository-Level Code Completion with Verbal Reinforcement and Retrieval-Augmented Generation. arXiv:2409.13122 [cs.SE] https://arxiv.org/abs/2409.13122
[58] Yanlin Wang, Yanli Wang, Daya Guo, Jiachi Chen, Ruikai Zhang, Yuchi Ma, and Zibin Zheng. 2024. Rlcoder: Reinforcement learning for repository-level code completion. arXiv preprint arXiv:2407.19487 (2024).
[59] Peiyang Wu, Nan Guo, Junliang Lv, Xiao Xiao, and Xiaochun Ye. 2025. RTLRepoCoder: Repository-Level RTL Code Completion through the Combination of Fine-Tuning and Retrieval Augmentation. arXiv:2504.08862 [cs.SE] https://arxiv.org/abs/2504.08862
[60] An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao, Chengen Huang, Chenxu Lv, et al. 2025. Qwen3 technical report. arXiv preprint arXiv:2505.09388 (2025).
[61] Hao Yu, Bo Shen, Dezhi Ran, Jiaxin Zhang, Qi Zhang, Yuchi Ma, Guangtai Liang, Ying Li, Qianxiang Wang, and Tao Xie. 2024. Codereval: A benchmark of pragmatic code generation with generative pre-trained models. In Proceedings of the 46th IEEE/ACM International Conference on Software Engineering. 1–12.
[62] Wenhao Zeng, Yaoning Wang, Chao Hu, Yuling Shi, Chengcheng Wan, Hongyu Zhang, and Xiaodong Gu. 2025. Pruning the Unsurprising: Efficient Code Reasoning via First-Token Surprisal. arXiv preprint arXiv:2508.05988 (2025).
[63] Fengji Zhang, Bei Chen, Yue Zhang, Jacky Keung, Jin Liu, Daoguang Zan, Yi Mao, Jian-Guang Lou, and Weizhu Chen. 2023. RepoCoder: Repository-Level Code Completion Through Iterative Retrieval and Generation. In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing. 2471–2484.
[64] Kechi Zhang, Jia Li, Ge Li, Xianjie Shi, and Zhi Jin. 2024. Codeagent: Enhancing code generation with tool-integrated agent systems for real-world repo-level coding challenges. arXiv preprint arXiv:2401.07339 (2024).
[65] Lei Zhang, Yunshui Li, Jiaming Li, Xiaobo Xia, Jiaxi Yang, Run Luo, Minzheng Wang, Longze Chen, Junhao Liu, Qiang Qu, and Min Yang. 2025. Hierarchical Context Pruning: Optimizing Real-World Code Completion with Repository-Level Pretrained Code LLMs. Proceedings of the AAAI Conference on Artificial Intelligence 39, 24 (Apr. 2025), 25886–25894. https://doi.org/10.1609/aaai.v39i24.34782
[66] Dan Zhao, Li Miao, Dafang Zhang, et al. 2015. Reusable function discovery by call-graph analysis. Journal of Software Engineering and Applications 8, 04 (2015), 184.
[67] Tianyu Zheng, Ge Zhang, Tianhao Shen, Xueling Liu, Bill Yuchen Lin, Jie Fu, Wenhu Chen, and Xiang Yue. 2024. Opencodeinterpreter: Integrating code generation with execution and refinement. arXiv preprint arXiv:2402.14658 (2024).
[68] Li Zhong, Zilong Wang, and Jingbo Shang. 2024. Debug like a human: A large language model debugger via verifying runtime execution step-by-step. arXiv preprint arXiv:2402.16906 (2024).