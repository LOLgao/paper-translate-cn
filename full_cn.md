# 不同蒸发速率下钙钛矿薄层结晶模拟——补充信息



M. Majewski1, S. Qiu2, O. Ronsin1, L. Lüer2, V. M. Le Corre2, T. Du2, 3, C. Brabec2, 3, H.-J. Egelhaaf2, 3, J. Harting1, 4

1埃尔朗根-纽伦堡可再生能源亥姆霍兹研究所（HIERN），于利希研究中心有限公司   
2材料科学与工程系电子与能源技术材料研究所（i-MEET），德国埃尔朗根-纽伦堡弗里德里希-亚历山大大学   
3埃尔朗根-纽伦堡可再生能源亥姆霍兹研究所（HIERN），Immerwahr Straße 2, 91058 埃尔朗根，德国   
4化学与生物工程系及物理系，德国纽伦堡弗里德里希-亚历山大大学，Fürther Straße 248, 90429 纽伦堡，德国

# 目录



1. 模拟模型的补充信息...   
2. 正文“模拟流程与实验方法”部分的补充信息 ...................... 9   
3. 正文“干燥速率对形貌的影响及模型验证”部分的补充信息 17   
4. 正文“器件性能对薄膜形貌的依赖性”部分的补充信息..... 25   
5. 参考文献.... .. 31

# 1. 关于仿真模型的补充信息

本章介绍了本工作中使用的相场模型，该模型是对文献1中提出的多组分模型的简化。在当前情况下，系统通过三个体积分数进行建模：一个用于可结晶溶质的场变量（$( \varphi _ { 1 }$，钙钛矿材料），一个用于可蒸发的溶剂（$\left( \varphi _ { 2 } \right)$），以及一个用于空气（$\left( \varphi _ { 3 } \right)$）。此外，还存在两个序参数。在液相中，两个序参数均为零。在晶相中，结晶序参数（$\phi _ { c }$）等于1，而气相序参数等于零。在气相中，气相序参数（$\phi _ { v a p }$）等于1，而结晶序参数等于零。使用单一溶质和单一晶相来代表钙钛矿的形成是一个极大的简化，因为钙钛矿的结晶涉及复杂的化学过程，包括多种离子络合物的形成，有时还会形成胶体聚集体和/或固态前驱晶体2。然而，我们的研究重点在于成核和生长的物理机制及其对形貌形成的影响。为此，我们将证明，即使不考虑溶液化学的细节，我们也能获得非常有用的见解。这是可能的，因为在所研究的系统中，已证明直接钙钛矿结晶占主导地位，不存在SSI阶段。在模拟中，晶体从随机热波动中自发成核，并可能相互接触。为了处理相互碰撞晶体之间的相互作用，使用了一个额外的标记场（$\theta$）。该场仅在晶相中定义，即结晶序参数（及溶质体积分数）超过某一阈值时。系统中包含空气作为缓冲材料，以便处理凝聚相与气相之间的可变形界面1。最后，两个额外的场?和$P$分别用于追踪薄膜中的速度和压力。

# 1.1. 吉布斯自由能

系统的能量贡献被收集在一个自由能泛函中。该吉布斯自由能 $G$ 可以分解为非局域贡献和局域贡献

$$
G = \int_ {V} \Delta G _ {V} d V = \int_ {V} \left(\Delta G _ {V} ^ {\text {n o n l o c}} + \Delta G _ {V} ^ {\text {l o c}}\right) d V. \tag {S1}
$$

非局域项 $\Delta G _ { V } ^ { n o n l o c }$ 描述了系统中各种界面产生的表面张力，其表达式为

$$
\varDelta G _ {V} ^ {n o n l o c} = \sum_ {i = 1} ^ {3} \frac {\kappa_ {i}}{2} (\nabla \varphi_ {i}) ^ {2} + \frac {\epsilon_ {v a p} ^ {2}}{2} (\nabla \phi_ {v a p}) ^ {2} + \frac {\epsilon_ {c} ^ {2}}{2} (\nabla \phi_ {c}) ^ {2} + p (\phi_ {c}) \frac {\pi \epsilon_ {g}}{2} \delta_ {D} (\nabla \theta), \qquad \qquad \mathrm {(S 2)}
$$

其中 $\kappa _ { i }$ 定义了与相应成分梯度相关的表面张力强度，$\epsilon _ { v a p }$ 定义了气相与非气相之间的表面张力强度，$\epsilon _ { c }$ 定义了晶相与非晶相之间的表面张力强度，而 $\epsilon _ { g }$ 定义了晶界能。当标记场 $\theta$ 中存在阶跃时（在晶界处），项 $\delta _ { D } ( \nabla \theta )$ 等于1，否则为零。因此，该项在晶体之间的界面处产生能量贡献，导致晶体之间形成边界，从而能够处理多晶体系。

自由能的局域贡献 $\Delta G _ { V } ^ { l o c }$ 可以写为

$$
\begin{array}{l} \varDelta G _ {V} ^ {l o c} \\ = \left(1 - p \left(\phi_ {v a p}\right)\right) \Delta G _ {v} ^ {c o n d} \left(\varphi_ {i}, \phi_ {c}\right) + p \left(\phi_ {v a p}\right) \Delta G _ {v} ^ {v a p} \left(\phi_ {v a p}\right) + \Delta G _ {v} ^ {c r y s t v a p} \left(\phi_ {c}, \phi_ {v a p}\right) \tag {S3} \\ + \Delta G _ {v} ^ {\text {n u m}} (\varphi_ {i}), \\ \end{array}
$$

其中凝聚相的能量项 $\Delta G _ { v } ^ { c o n d } ( \phi _ { i } , \phi _ { c } )$ 写为

$$
\begin{array}{l} \Delta G _ {v} ^ {\text {c o n d}} \left(\varphi_ {i}, \phi_ {c}\right) \\ = \rho_ {1} \varphi_ {1} ^ {2} \left(g \left(\phi_ {c}\right) W + p \left(\phi_ {c}\right) \Delta G _ {v} ^ {c r y s t}\right) \\ + \frac {R T}{\nu_ {0}} \left(\sum_ {i = 1} ^ {3} \varphi_ {i} \ln (\varphi_ {i}) + \sum_ {i = 1} ^ {3} \sum_ {j > i} ^ {3} \varphi_ {i} \varphi_ {j} \chi_ {i j, L L} + \sum_ {j = 2} ^ {3} \phi_ {c} ^ {2} \varphi_ {1} \varphi_ {j} \chi_ {1 j, S L}\right). \tag {S4} \\ \end{array}
$$

第一个括号内的贡献解释了从液相转变为固相所引起的能量密度变化。$g ( \phi _ { c } )$ 和 $p ( \phi _ { c } )$ 是选定的插值函数3，使得流体相具有比晶相更高的能量势，并且在从 $\phi _ { c } = 0$ 到 $\phi _ { c } = 1$ 的液-固转变过程中存在一个能量势垒。使用的函数如下：

$$
p \left(\phi_ {c}\right) = \phi_ {c} ^ {2} \left(3 - 2 \phi_ {c}\right) \tag {S5}
$$

$$
g \left(\phi_ {c}\right) = \phi_ {c} ^ {2} \left(1 - \phi_ {c}\right) ^ {2} \tag {S6}
$$

$\rho$ 是材料的密度，? 定义了液相和晶相之间的能量势垒高度，$\Delta G _ { v } ^ { c r y s t } = L _ { f u s } ( T / T _ { m } - 1 )$ 是结晶时的能量增益，其中 $\tau$ 是温度，$T _ { m }$ 是熔点，$L _ { f u s }$ 是熔化焓。第二部分解释了熵的贡献以及不同材料之间的焓相互作用。$R$ 是气体常数，$\nu _ { 0 }$ 是晶格尺寸的摩尔体积，$\chi _ { i j , L L }$ 是非晶材料 ? 和 $j . \chi _ { 1 j , S L }$ 之间的弗洛里-哈金斯相互作用参数，代表溶质（材料1）晶相中结晶溶质与溶剂和/或空气（假定为非晶态）之间额外的焓相互作用。请注意，在此考虑的二元共混物中，只有溶质材料（'钙钛矿'）可以结晶，因此不存在 $\chi _ { i j , S S }$ 参数4。$L _ { f u s }$、$W$、$\varepsilon _ { c }$ 的值选择为使熔化热和表面张力处于合理的数量级（分别为75 J/kg和60mJ/m2），从而确保结晶时始终存在需要克服的能量势垒，并且界面厚度至少为6个网格节点，以实现适当的空间收敛。

气相被假定为理想混合物，因此气相中的能量贡献可以写为

$$
\Delta G _ {v} ^ {v a p} \left(\varphi_ {i}\right) = \frac {R T}{\nu_ {0}} \sum_ {i = 1} ^ {3} \varphi_ {i} \ln \left(\frac {\varphi_ {i}}{\varphi_ {s a t , i}}\right), \tag {S7}
$$

其中 $\varphi _ { s a t , i } = P _ { s a t , i } / P _ { 0 }$，$P _ { s a t , i }$ 是蒸气压，$P _ { 0 }$ 是参考压力。晶相与气相序参数 $\Delta G _ { v } ^ { c r y s t v a p } \left( \varphi _ { 1 } , \phi _ { c } , \phi _ { v a p } \right)$ 之间的相互作用表达式为

$$
\Delta G _ {v} ^ {\text {c r y s t v a p}} \left(\varphi_ {1}, \phi_ {c}, \phi_ {v a p}\right) = E \left(\varphi_ {1}, \phi_ {c}\right) \phi_ {c} ^ {2} \phi_ {v a p} ^ {2}, \tag {S8}
$$

其中 $E$ 定义了该相互作用的强度：

$$
E \left(\varphi_ {1}, \phi_ {k}\right) = E _ {0} \frac {d _ {s v}}{f \left(\varphi_ {1} \phi_ {c} , d _ {s v} , c _ {s v} , W _ {s v}\right)} \tag {S9}
$$

其中 $E _ { 0 }$ 定义了相互作用强度，$d _ { s v } , c _ { s v } , W _ { s v }$ 定义了惩罚函数 f 的强度、中心和宽度：

$$
\log (f (x, d, c, w)) = \frac {1}{2} \log (d) \left(1 + \tanh  (w (x - c))\right) \tag {S10}
$$

其中 d、c 和 w 分别定义了惩罚的强度、中心和宽度。添加此项是为了防止气相渗入晶相，反之亦然。这有助于确保晶体在固-气界面处的稳定性3。最后，纯数值贡献 $\Delta G _ { v } ^ { n u m } ( \varphi _ { \mathrm { i } } )$ 确保体积分数保持在 ]0,1[ 范围内。

$$
\Delta G _ {v} ^ {\text {n u m}} \left(\varphi_ {i}\right) = \sum_ {i = 1} ^ {3} \frac {\beta}{\varphi_ {i}} \tag {S11}
$$

系数 $\beta$ 被选择得尽可能小，以对热力学性质产生最小的影响，同时仍能提供数值稳定性。

# 1.2. 卡恩-希利亚德方程与随机艾伦-卡恩方程

体积分数场的演化由对流性Cahn-Hilliard方程给出：

$$
\frac {\partial \varphi_ {i}}{\partial t} + \boldsymbol {v} \nabla \varphi_ {i} = \frac {v _ {0}}{R T} \nabla \left[ \sum_ {j = 1} ^ {2} \Lambda_ {i j} \nabla \left(\mu_ {j} - \mu_ {3}\right) \right] \tag {S12}
$$

这是对流-扩散方程的广义形式，其中 $\Lambda _ { i j }$ 是对称的Onsager迁移系数，它们本身依赖于组成和相态。这些系数通常在晶相中较低，而当存在大量溶剂时则较高³。Cahn-Hilliard迁移系数表示为：

$$
\Lambda_ {i i} ^ {c o n d} = \omega_ {\mathrm {i}} \left(1 - \frac {\omega_ {i}}{\sum_ {k = 1} ^ {n} \omega_ {k}}\right) \tag {S13}
$$

$$
\Lambda_ {i j} ^ {\text {c o n d}} = - \frac {\omega_ {i} \omega_ {j}}{\sum_ {k = 1} ^ {n} \omega_ {k}} \tag {S14}
$$

其中

$$
\omega_ {i} = N _ {i} \varphi_ {i} f \left(\phi_ {c}, d _ {s l}, w _ {s l}, c _ {s l}\right) \prod_ {j = 1} ^ {n} \left(D _ {s, i} ^ {\varphi_ {j} \rightarrow 1}\right) ^ {\varphi_ {j}} \tag {S15}
$$

这里 ?@&→! i $D _ { s , i } ^ { \varphi _ { j }  1 }$ 是纯材料中的自扩散系数。$\mu _ { j } - \mu _ { 3 }$ 是通过自由能 $G$ 的泛函导数计算得到的交换化学势：

$$
\mu_ {j} - \mu_ {3} = \frac {\delta G}{\delta \varphi_ {j}} - \frac {\delta G}{\delta \varphi_ {3}} = \frac {\partial \Delta G _ {V}}{\partial \varphi_ {j}} + \nabla \left(\frac {\partial \Delta G _ {V}}{\partial \nabla \varphi_ {j}}\right) - \frac {\partial \Delta G _ {V}}{\partial \varphi_ {3}} - \nabla \left(\frac {\partial \Delta G _ {V}}{\partial \nabla \varphi_ {3}}\right) \tag {S16}
$$

晶体的成核、生长、粗化和碰撞通过基于随机对流Allen-Cahn方程的晶体序参量的动态演化来描述：

$$
\frac {\partial \phi_ {c}}{\partial t} + \boldsymbol {v} \nabla \phi_ {c} = - \frac {v _ {0}}{R T} M _ {c} \frac {\delta \Delta G _ {v}}{\delta \phi_ {c}} + \zeta_ {A C} \tag {S17}
$$

其中 $M _ { c }$ 是固-液界面的迁移系数，$\zeta _ { A C }$ 是一个零均值且标准差为以下值的非相关高斯噪声：

$$
\left\langle \zeta_ {A C} (x, t), \zeta_ {A C} \left(x ^ {\prime}, t ^ {\prime}\right) \right\rangle = \frac {2 \nu_ {0}}{N _ {a}} M _ {c} \delta \left(t - t ^ {\prime}\right) \delta \left(x - x ^ {\prime}\right) \tag {S18}
$$

其中 $N _ { a }$ 是阿伏伽德罗常数。在本工作所展示的模拟中，由于液-液相分离不可能发生，晶体序参量上的涨落对于触发成核起主导作用。这就是为什么在Cahn-Hilliard方程中没有考虑涨落的原因。尽管如此，已验证在体积分数场中包含涨落并不会改变结晶行为。

# 1.3. 蒸发

模拟箱顶部初始化为干燥膜上方的一层空气。为模拟溶剂的蒸发过程，在模拟箱顶部施加溶剂流出通量 $\scriptstyle { j ^ { z = z _ { m a x } } }$（$\left( z = z _ { m a x } \right.$）：

$$
j ^ {z = z _ {\max }} = \alpha \sqrt {\frac {\nu_ {0}}{2 \pi R T \rho}} P _ {0} \left(\varphi_ {2} ^ {v a p} - \varphi_ {2} ^ {\infty}\right) \tag {S19}
$$

该表达式对应于Hertz-Knudsen理论5–7，其中 $\alpha$ 为蒸发-凝结系数，$P _ { 0 }$ 为参考压力，$\varphi _ { i } ^ { \infty } = P _ { i } ^ { \infty } / P _ { 0 }$（其中 $P _ { i } ^ { \infty }$ 为环境中的溶剂压力）。$\varphi _ { i } ^ { v a p }$ 是根据薄膜表面局部液-气平衡计算得到的气相体积分数。

气相序参数 $\phi _ { v a p }$ 的演化受控于气相对流型Allen-Cahn方程：

$$
\frac {\partial \phi_ {v a p}}{\partial t} + \boldsymbol {v} \nabla \phi_ {v a p} = - \frac {v _ {0}}{R T} M _ {v a p} \frac {\delta \Delta G _ {v}}{\delta \phi_ {v a p}} \tag {S20}
$$

式中 $M _ { v a p }$ 为液-气界面的Allen-Cahn迁移率。选择足够高的 $M _ { v a p }$ 值以确保整个模拟过程中局部液-气平衡得以维持。需注意空气也需赋予蒸气压，该值虽无物理意义，但必须设定为（非现实意义的）高值以防止空气渗入凝聚相8。溶质在气相中的扩散常数需设置得足够小，以阻止分离区域通过气相进行扩散传质；而溶剂与空气在气相中的扩散常数则需足够大，以确保整个气相中溶剂体积分数保持恒定。在此条件下，通过仅在模拟箱顶部（而非直接在液-气界面）设置流出通量，即可获得正确的干燥动力学8。这使得系统能够形成可形变的液-气界面，并获得具有针孔等缺陷的粗糙薄膜。

# 1.4. 流体动力学

流体动力学方程用于计算速度场？该速度场源于所有界面产生的毛细力，从而解析了对流质量传输。对流质量传输导致薄膜表面的晶体在蒸发过程中因液-气表面张力而被向下推移，并使相邻晶体因它们之间的流场而相互吸引。在本文相关的系统尺度下，雷诺数始终很小，流体惯性可以忽略。同时，与所产生的毛细力相比，重力也可以忽略。假定流体流动不可压缩，并可由单一速度场3描述。因此，连续性方程为：

$$
\nabla \boldsymbol {v} = 0 \tag {S21}
$$

动量守恒方程可写为：

$$
- \nabla P + \nabla \left(2 \eta_ {m i x} S\right) + F _ {\varphi} + F _ {\phi} = 0, \tag {S22}
$$

其中 $P$ 是确保不可压缩性的压力场，它是流体力学方程求解的结果，但对当前研究没有相关的物理意义，下文将不作详细讨论。？是应变率张量 $\eta _ { m i x }$ 是依赖于组分和相态的粘度3：

$$
\frac {1}{\eta_ {m i x}} = f \left(\delta_ {D} \left(\theta_ {k}\right) \phi_ {c} \varphi_ {1}, d _ {\eta}, c _ {\eta}, w _ {\eta}\right) \sum_ {\mathrm {i} = 1} ^ {3} \frac {\phi_ {i}}{\eta_ {i}} \tag {S23}
$$

其中 $\eta _ { i }$ 是材料 i 的粘度，$\delta _ { D } ( \theta _ { k } )$ 在取向参数存在时为 1，否则为 0，$d _ { \eta } , c _ { \eta } , w _ { \eta }$ 定义了惩罚函数的强度、中心和宽度。由体积分数场和序参量场产生的毛细力可写为9：

$$
F _ {\varphi} = \nabla \left[ \sum_ {i = 1} ^ {3} \kappa_ {i} \left(\left| \nabla \varphi_ {i} \right| ^ {2} I - \nabla \varphi_ {i} \times \nabla \varphi_ {i}\right) \right] \tag {S24}
$$

和

$$
F _ {\phi} = \nabla \left[ \epsilon_ {c} ^ {2} \left(| \nabla \phi_ {c} | ^ {2} I - \nabla \phi_ {c} \times \nabla \phi_ {c}\right) + \epsilon_ {v a p} ^ {2} \left(\left| \nabla \phi_ {v a p} \right| ^ {2} I - \nabla \phi_ {v a p} \times \nabla \phi_ {v a p}\right) \right] \tag {S25}
$$

其中？是单位张量。

在本模型中，所选的粘度值是不切实际地高。遗憾的是，这是为了获得可处理的模拟运行时间所必需的。然而，基于以下考虑，我们预期这一假设不会对干燥薄膜中涉及的传输过程产生影响。结晶通常在体积分数约为 $20 \mathrm { - } 3 0 \%$ 的溶液中开始，此时溶液粘度略大于纯溶剂，扩散系数小于纯溶剂，但我们假设 $5 \cdot 1 0 ^ { - 3 } P a \cdot s$ 和 $1 0 ^ { - 9 } m ^ { 2 } \cdot s ^ { - 1 }$ 为合理值。相关过程（干燥、结晶）的时间尺度在 $1 - 1 0 s$ 量级。一方面，特征扩散长度高达 $L \approx \sqrt { D t } \approx 1 0 \mu m$ ，这确保了液体溶液的组成保持完全均匀。另一方面，晶体在该溶液中的传输可能通过对流和/或扩散进行。利用斯托克斯-爱因斯坦关系，预计一个 10?? 晶体在溶液中的扩散系数约为 $D = 4 \cdot 1 0 ^ { - 1 2 } m ^ { 2 } \cdot s ^ { - 1 }$ ，而运动粘度约为 $1 0 ^ { - 6 } m ^ { 2 } \cdot s ^ { - 1 }$ 。这表明对流是纳米晶体的主要传输机制。总而言之，要模拟的情况是：晶体在均匀的液体溶液中通过对流进行传输，晶体扩散在一阶近似下是可忽略的机制。在我们的模型中，即使粘度值不切实际地高且与扩散系数值解耦，情况仍然如此：使用真实的扩散系数确保了溶液的均匀性，流体力学确保了晶体的对流传输。因此，即使选择了非常高的粘度值，来自具有典型表面张力 $\sigma = 2 0 m N \cdot m ^ { - 1 }$ 的界面的毛细力也能产生速度约为 $1 0 0 n m \cdot s ^ { - 1 }$ 的流动。考虑到系统的特征长度为几百纳米分之一，干燥特征时间约为 10?，这对于晶体传输是足够的。当然，晶体传输被低估了，这可能会影响

干燥薄膜中最终的晶体空间排列，从而影响粗糙度和针孔密度的精确值。然而，晶体形成不受影响：已经验证，晶体成核和生长过程对对流不敏感（见图 S1），正如在均匀溶液中所预期的那样。因此，导致形貌随干燥速率变化（粗糙度和针孔密度增加，晶体尺寸随干燥速率降低而减小）的过程（限域、过饱和）不受对流强度的影响，这解释了我们研究结果的定性稳健性（见图 S2）。

![](images/923f7ca72df472b937be50bdfe21ce7134544c9d586f376bb55844f71a8cea19.jpg)

![](images/2f171447bf92bfbb91b8ec1441618d75d100bd7811bffd4f46f1b017316ac9a2.jpg)
图 S 1：在固定溶质体积分数 $\varphi$ 的二元溶质-溶剂共混物模拟中测得的结晶半衰期 $t _ { 1 / 2 }$（左）和 $t _ { 1 / 2 }$ 时的晶体半径（右），无对流（黑线）和有对流（红线）。对流对晶体成核和生长过程没有影响。注意，低于 $\varphi = 0 . 4$ 时，晶体数量非常少，因此半径评估的精度非常差。

![](images/fc9921c8ee5ff20572bfaf007353ef42be3d3500b7e37f885dc5f5089f5208e5.jpg)

![](images/eefd527b67517f6ee16bef32dc76b7050702be5ef356d07f08acd875c39f1e60.jpg)

![](images/397021d4a2dbce264b76a83ba34fcdc68687d20382c3f6d66e46c528a09e9c4a.jpg)

![](images/3de19f9b574fbdc4e7df7fdaa6404b69b67cc8ef5c8d0f1c1ed36ac4ea63f2c5.jpg)

![](images/3b460302313c14aab2810c362cc53fe28f6fa86e6b40322205683f5ef942e728.jpg)

![](images/82861dd7275e36a42ed8ae01a64f0b9fbf57241e1c0689f6918796eb7703a844.jpg)

![](images/9ea321a1b41f4facd06ca2ed41b2f9ece85b2c93e8079cbe44b3f0cd148ede99.jpg)

![](images/6adeda118d6b0552e367dc5288fc99cd069d7c9cf39546ef5f397a8057012c0b.jpg)

![](images/3f93a1a2094d66015068c37385caf18fd81b6065e5182253ae12c30d17678630.jpg)
图 S 2：干燥结束时的薄膜形貌。显示了晶体序参量。不同的行对应不同的蒸发速率。从上到下：

$v _ { e v a p } = 6 7$ , 201, 536 ?? ∙ ?L!。（左）如下表所示的粘度（中）粘度除以 10（右）粘度除以 100。

# 1.5. 仿真参数

<table><tr><td>Parameters</td><td>Full Name</td><td>Value</td><td>Unit</td></tr><tr><td>α</td><td>Evaporation-condensation coefficient</td><td>(1-9)·2.3·10-5</td><td>-</td></tr><tr><td>dx, dy</td><td>Grid Spacing</td><td>1</td><td>nm</td></tr><tr><td>T</td><td>Temperature</td><td>300</td><td>K</td></tr><tr><td>ρi</td><td>Density</td><td>1000</td><td>kg/m3</td></tr><tr><td>m1,m2,m3</td><td>Molar Mass</td><td>0.1, 0.1, 0.03</td><td>kg/mol</td></tr><tr><td>ν0</td><td>Molar Volume of the Flory Huggins Lattice Site</td><td>3·10-5</td><td>m3/mol</td></tr><tr><td>χ12,LL,χ13,LL,χ23,LL</td><td>Liquid – liquid interaction parameter</td><td>0.57, 1,0</td><td>-</td></tr><tr><td>χ12,SL,χ13,SL</td><td>Liquid – solid interaction parameter</td><td>0.15, 0.5</td><td>-</td></tr><tr><td>Tm</td><td>Melting Temperature</td><td>600</td><td>K</td></tr><tr><td>Lfus</td><td>Heat of Fusion</td><td>75789</td><td>J/kg</td></tr><tr><td>W</td><td>Energy barrier upon crystallization</td><td>142105</td><td>J/kg</td></tr><tr><td>P0</td><td>Reference Pressure</td><td>105</td><td>Pa</td></tr><tr><td>Psat,1, Psat,2, Psat,3</td><td>Vapor Pressure</td><td>102,1.5·103, 108</td><td>Pa</td></tr><tr><td>Psat,1, Psat,2, Psat,3</td><td>Vapor Pressure during annealing</td><td>102,1.5·102, 108</td><td>Pa</td></tr><tr><td>Pi∞</td><td>Partial Vapor Pressure in the Environment</td><td>0</td><td>Pa</td></tr><tr><td>E0</td><td>Solid-Vapor interaction energy</td><td>5·109</td><td>J/m3</td></tr><tr><td>β</td><td>Numerical Free Energy Coefficient</td><td>10-5</td><td>J/m3</td></tr><tr><td>κ1, κ2, κ3</td><td>Surface Tension Parameters for Volume Fraction Gradients</td><td>2·10-10, 2·10-10, 6·10-9</td><td>J/m</td></tr><tr><td>εc, εvap</td><td>Surface Tension Parameters for Order Parameter Gradients</td><td>1.5·10-5, 2·10-4</td><td>(J/m)0.5</td></tr><tr><td>εg</td><td>Surface Tension parameters for the grain boundaries</td><td>0.2</td><td>J/m2</td></tr><tr><td>Dφj→1s,i</td><td>Self-Diffusion Coefficients in pure materials (all)</td><td>10-9</td><td>m2/s</td></tr><tr><td>Mc,Mv</td><td>Allen Cahn mobility coefficients</td><td>4,106</td><td>s-1</td></tr><tr><td>η1,η2,η3</td><td>Material viscosities</td><td>5·106, 5·103, 5·10-2</td><td>Pa·s</td></tr><tr><td>D1vap, D2vap, D3vap</td><td>Diffusion Coefficients in the Vapor Phase</td><td>10-16, 10-10, 10-10</td><td>m2/s</td></tr><tr><td>tφ, tφ, tφv</td><td>Thresholds for crystal detection</td><td>0.4, 0.02, 5·10-2</td><td>-</td></tr><tr><td>dsl,csl, wsl</td><td>Amplitude, center and with of the penalty function for the diffusion coefficients upon liquid solid transition</td><td>10-9, 0.7, 10</td><td>-</td></tr><tr><td>dξ, cξ, wξ</td><td>Amplitude, center and with of the penalty function for the order parameter fluctuations</td><td>10-2, 0.85, 15</td><td>-</td></tr><tr><td>dη, cη, wη</td><td>Amplitude, center and with of the penalty function for the viscosities</td><td>10-7, 0.2, 20</td><td>-</td></tr><tr><td>dsv, csv, wsv</td><td>Amplitude, center and with of the penalty function for the Allen Cahn mobility and the solid- vapor interaction energy</td><td>10-9, 0.3, 15</td><td>-</td></tr></table>

# 2. 对正文“模拟流程与实验方法”章节的补充信息

模拟设置如下：在256×256的格点上模拟薄膜的二维截面。初始时，假设流体薄膜完全为非晶态且充分混合，并在模拟盒顶部放置一层薄空气/蒸汽相。凝聚相初始化为溶质体积分数为$20 \%$、溶剂体积分数为$80 \%$（大致对应1.3 M MAPbI3）。选择该初始体积分数是为了使其远低于$26 \%$的结晶阈值（参见第0节）。水平方向采用周期性边界条件，底部（基底）采用无流动的诺伊曼边界条件，顶部（蒸汽相）采用蒸发溶剂的流出条件（参见公式S19）。

选择相互作用参数$\chi _ { i j }$，使得溶质与溶剂在流体状态下完全互溶，但在结晶相中不互溶，从而模拟出的晶体几乎不含溶剂（参见第2.1节）。此外，液相中溶质的最终平衡浓度（饱和浓度$\varphi _ { s }$）非常低，为$( 3 . 7 \% )$。成核与生长达到平衡，使系统既不纯粹由生长主导，也不纯粹由成核主导。选择扩散常数时，确保晶体生长和蒸发均不受扩散限制，因此溶质在液相中保持均匀分布。完整参数列表见第1.5节。

进行了两组模拟。第一组仅溶剂的蒸发速率不同；第二组仅结晶速率不同。蒸发速率通过调整蒸发-凝结系数$\alpha$来改变（参见公式S19）。结晶速率通过调整艾伦-卡恩迁移率M来改变（参见公式S17）。选择结晶相的蒸发-凝结系数和艾伦-卡恩迁移率，使得蒸发速率的变化足以覆盖所有可能的形态形成路径：从结晶远快于蒸发，到结晶远慢于蒸发。研究的蒸发速率范围接近一个数量级，每个蒸发速率进行五次模拟。经过足够长时间，当所有未被捕获的溶剂蒸发后，增加蒸发的驱动力。这是通过将蒸汽压提高十倍来实现的，以模拟实验中退火步骤的效果。这是对退火过程的极度简化描述。若要定量描述该处理步骤中的真实行为，则需考虑模型大多数热力学参数的温度依赖性，这超出了本工作的范围。尽管如此，我们的简化方法能够定性再现退火过程中发生的两个主要演变：残留溶剂的去除和晶粒粗化。

在干燥的最终阶段可能存在残留溶剂，因为溶剂可能被捕获在晶体下方或晶体间的小通道中。在这种情况下，溶剂表面张力会从能量上阻碍进一步蒸发。部分残留溶剂可能在溶剂蒸汽压升高时被去除，这模拟了热退火过程。

# 2.1. 模拟溶质溶剂共混体系的相图及晶体形成机制

![](images/d27afbc6165d12404cd0dd874335e6ce136c20174e16359863b201110ff9e42f.jpg)
图 S 3：左图：所研究体系的相图。蓝色：液相线（对应于饱和浓度的液相中溶质平衡体积分数，${ \cal T } = 2 8 ~ ^ { \circ } C )$ 时 $\varphi _ { s } =$ 为 0.0374），黄色：固相线（固相中溶质平衡体积分数），绿色：亚稳态两相区。干燥模拟中的温度设定为 300K（约 $2 8 ~ ^ { \circ } C )$）。中图：300K 时依赖于结晶序参量和体积分数的自由能景观。注意不存在不稳定区域，因此结晶只能通过成核和生长实现。右图：在固定选定体积分数下，自由能随 $\phi$ 变化的曲线，显示了从 $\varphi = 0 . 2 5$ 到 $\varphi =$ 0.99 的能量势垒。在低体积分数下，自由能随 $\phi$ 增加，无法形成晶体。

仔细审视自由能景观有助于理解晶体形成机制。下图除了展示自由能面的等值线外，还显示了：(a) 二维空间中的液相点和固相点，(b) 在固定组成下沿序参量变量的最大值（能量势垒）和最小值（晶相）位置，(c) 描述分相特性的'伪'旋节线和双节线（在固定序参量下），以及 (d) 相场模拟中晶体形成过程中观察到的路径。显然，在高序参量和中等体积分数区域存在一个'伪'亚稳态和一个'伪'不稳定区域。这意味着，原则上，通过成核生长甚至旋节分解进行分相的过程，可以发生在达到此{组成-结晶度}区域的空间域内。然而，体系初始是完全非晶态的（$\phi = 0$），并且无论组成如何，非晶相都是稳定的。只有序参量的涨落使得在空间某些有限区域内能够克服结晶的能量势垒。然后，这些区域（实际上是晶核）迅速向更高的序参量和体积分数值（稳定的固相点）演化，而非晶相则向稳定的液相点演化。这些正是成核过程的特征。注意，成核仅在溶质体积分数足够大（$( \varphi > 0 . 2 )$）时才可能发生。因此，对于最高的溶质浓度，结晶路径大多避开'伪'不稳定和亚稳区域。然而，对于较低浓度，结晶路径可能会穿过该区域，因此人们可能预期在晶核内部会发生分相。但实际上这并未发生。原因如下：自由能景观中的不稳定和亚稳区域只是一个必要条件，但分相需要一定的空间10和时间11 12才能发生。实际上，晶核太小，且其组成/结晶度演化太快，这阻止了其内部发生分相。相反，晶核内的组成迅速向'伪'双节线组成演进（参见 $\varphi = 0 . 2 5$ 混合物中晶核的示例）。

![](images/1f3b12873264c72a618faafc9b7e1831237a79353b07c9e24e91c036577d1835.jpg)
图 S 4：自由能面的二维等高线图，显示了二维空间中的液相点和固相点（粉色点）、在固定 $\varphi$ 下沿 $\phi$ 的能量最大值（红色曲线）和最小值（蓝色曲线）位置、'伪'旋节线（黑色实线）和双节线（黑色虚线）。图中用紫色虚线显示了在晶体形成过程中观察到的典型轨迹，分别起始于溶质体积分数 $\varphi = 0 . 2 5$、$\varphi = 0 . 5$ 和 $\varphi = 0 . 9$。

下面的系列快照显示了在二元混合物中成核过程中体积分数和序参量场的演化，溶质含量分别为 $2 5 \%$、$50 \%$ 和 $90 \%$，对应于上述自由能面上报告的三条轨迹。因此，请注意局部体积分数的变化是局部序参量变化克服能量势垒的结果。

![](images/5bf2dfbf208cdd720ceb99f0daf2f44a493708c52f686ddccb086f5d4b02e30a.jpg)

![](images/95431ff50ffc64b5ab362b753bb303565576f0607c067dab2470e51c0d59f003.jpg)

![](images/b925e6240482589b48dddb4076f09c4142997edf4e5ff50e61eaf47fc7c81dbc.jpg)

![](images/305b88aed5cc478c87d26d195f255454f725fbf011f067946392c859c485038e.jpg)

![](images/39d4027cf686e309081362496496e499ae385a5304120d3f4e13bd63e587629f.jpg)

![](images/b9def3a6bb05c874d0decf775d600a4982d49a46a7027981df04b4964cb1dbdb.jpg)

![](images/9ff4b6a474907367ca886b21a4e0734bdd64f9261bef50265eb7622dd78f9648.jpg)

![](images/58412199e32a1bae9131baabace7d1831d4314c900b39588230f23c6bcd181da.jpg)

![](images/20ea31b15af0ee287f5c8168310ce97e05d28579f760ae3f6ddcedeeb93dc688.jpg)

![](images/c16a96bfc1ef1321417e1645cf24199d1ff34cf3e1ac890d4fd2967e29586d96.jpg)

![](images/5b492647d2adc7d20dcfcdcf74f2f8fd823080f3fa3d59428ecf92781e1b386e.jpg)
图 S 5：二元共混物结晶过程中（溶质含量为 $\varphi = 0 . 2 5$），随时间增加（从左到右）的体积分数场（上行）和序参量场（下行）。

![](images/b65d462d37a8b743e922e3621e6183d9493064f88fa48fce9553c8d792199f25.jpg)

![](images/5a76909420dc16ed6b102a2ee40ab5f13467c8f7f570b5bea43bea654b6b4821.jpg)

![](images/bc309287ab618c47671a7c855752790840496a63d969d53c7492b75b10a24ae7.jpg)

![](images/62802ffac6ce1226530c27b3f935c980cb8e52bb231cb30f79df3b215d673d6a.jpg)

![](images/7764845df68bcdb7c8016e488ed178a33d9e3134f45de9a8c882e1d7c6727a9e.jpg)

![](images/fb213ee908bfd58404fe5a64e8ae98dfeb823557aa94b0b3d0fb0c8458a6e202.jpg)

![](images/e248c2522d1c22cd6417bbdaa70b4b8c4d650399cb855b493539f9ec9a290949.jpg)

![](images/299a1172c891f6388c2b5043c44acfceae0579f4b94590d9dd901c4b363aa004.jpg)

![](images/d4fe6c156da895e57d266cd6a86d1f07f8ffe4e2ca221d11d2687b58b938632e.jpg)

![](images/19896fd75e2d598ea3238e2cba8bbed0b990f0c4be6a9f37e21d10d9ce0a9260.jpg)
图 S 6：二元共混物结晶过程中（溶质含量为 $\varphi = 0 . 5$），随时间增加（从左到右）的体积分数场（上行）和序参量场（下行）。

![](images/61d2656482b9dd2b0cccccb8b1920791a068f646516cb4a2b08733c1a4219eeb.jpg)

![](images/0c9003befbf7fc81b1ceb9110d58cb2f7b142078241e08cafc5a8ca48bbb8ac5.jpg)

![](images/64e16d44fc7f7d542a71aaf0607d2ef3e0add330d6ea6d33fe1f5871801dede8.jpg)

![](images/d400fb101ffa4afa07053b003896e431a3dd87acedd70659afa0f8dd50bb7da7.jpg)

![](images/e3566fda79cb2c084443a9d405a6ab4af0066697168334c85663d08bca01de96.jpg)

![](images/da74ea70d7e9f9d25570278aaae4b75bb90b5cb849deff99f3be7c23d206b1fc.jpg)

![](images/d0e2a1c509530dcbdccdee3b908cba9ef87555d94a957a01a8ca637845aebe6f.jpg)

![](images/201b2ca70c6ce19b034bd22988b909590b63b5846cc7efc16869c7fd3a552315.jpg)

![](images/cc78924f58dcda6d227adbd3a6f226647920d3bbea200686812db1763495e868.jpg)
图 S 7：二元共混物结晶过程中（溶质含量为 $\varphi = 0 . 9$），随时间增加（从左到右）的体积分数场（上行）和序参量场（下行）。

总之，采用本工作中使用的热力学参数，晶体完全通过一步成核和生长形成。关于具有不同热力学性质的其他可能成核路径的更一般性讨论，读者可参阅先前的工作。13

# 2.2. 临界体积分数（成核起始点）



在这些模拟中，总体组成保持恒定（溶剂不会蒸发）。模拟持续进行直至溶质完全结晶。从数据中提取溶质一半结晶所需的时间 $t _ { 1 / 2 }$ 。进行了包含溶质和溶剂的二维模拟。

![](images/79b73278ba38be10f8b865c913ee18f4561ac02bc2bb316e1ca777325022370d.jpg)  
图 S 8：在二元共混物中测得的结晶半衰期 $t _ { 1 / 2 }$ 。随着体积分数的降低，时间增加。低于某个（低）体积分数时，材料不足，结晶驱动力过低，结晶时间趋于发散。我们关注的量 $\varphi _ { c r i t }$ 是临界体积分数，低于该值时，在干燥模拟的蒸发时间内无法发生结晶。蒸发时间最多为 $6 \tau$ 。结晶半衰期与最大蒸发时间的交点即为 $\varphi _ { c r i t }$ ，其值约为 0.26。

# 2.3. 低蒸发速率下单一模拟的时间序列



![](images/8546074b9e8f5789aba5e585edf725bd85cf75642270c4a09f651a28cddeca7f.jpg)  
图 S 9：低干燥速率下单一模拟的时间序列。时间从上到下逐行增加。从左到右依次为：溶质体积分数 $( \varphi _ { 1 } )$ 、溶剂体积分数 $( \varphi _ { 2 } )$ 、空气体积分数 $( \varphi _ { 3 } )$ 、结晶序参数 $( \phi _ { c } )$ 、气相序参数 $( \phi _ { v a p } )$ 以及取向参数 (?)。

# 2.4. 实验方法

# 材料：

碘化铅（PbI2，$9 9 \%$）、碘化甲铵（MAI，$98 \%$）、氯化苄（CB，$9 9 \%$）和聚（3-己基噻吩-2,5-二基）（P3HT）购自Sigma公司。无水2-甲氧基乙醇（2ME，Aldrich，$9 9 . 8 \%$）和1-甲基-2-吡咯烷酮（NMP，$9 9 . 8 \%$）购自Aldrich公司。氧化锡（IV）（SnO2，$1 5 \%$，H2O胶体分散液）购自Alfa Aesar公司。碳浆购自辽宁汇特光电科技有限公司。所有化学品均按收到状态使用，未经进一步纯化。

钙钛矿薄膜的气体淬火辅助刮涂沉积：

将等摩尔量的MAI和PbI2溶解在无水2ME和NMP中（2ME:NMP，$\mathsf { v } : \mathsf { v } = 3 7 : 3 )$），制备1 M MAPbI3储备溶液，并在室温下搅拌1小时。将20 µL前驱体溶液刮涂到$2 5 \ : \mathrm { m m } \times 2 5$ mm玻璃基底上，刮涂速度为$3 \ : \mathsf { m m } \ : \mathsf { s } ^ { - 1 }$，刮刀间隙高度为$1 5 0 ~ { \mu \mathrm { m } }$。涂布后，用连续流动的干燥空气从上方吹扫湿膜60秒，此过程称为“气体淬火”。空气压力可在0 Bar至5.0 Bar之间调节。随后，使用热风枪在$100 \%$下对薄膜进行热退火10分钟。钙钛矿前驱体薄膜的刮涂是在室温空气中，使用商用刮涂机（ZEHNTNER的ZAA2300.H）和ZUA 2000.100刮刀（ZEHNTNER）进行的。

# 太阳能电池制造：

预先图案化的氧化铟锡（ITO）镀膜玻璃（辽宁汇特光电科技有限公司）依次通过丙酮和异丙醇各超声清洗15分钟进行清洁。随后，将基板置于紫外-臭氧箱中处理20分钟，以去除有机残留物并改善润湿性。采用$\mathsf { s n O } _ { 2 }$纳米颗粒水溶液制备电子传输层。该溶液被稀释至5.0 wt% $\mathsf { S n O } _ { 2 }$，并在超声浴中处理10分钟，随后使用$0 . 4 5 \mu \mathrm { m }$ PTFE滤头过滤。接着，在$80 \%$和$1 5 \mathsf { m m } \mathsf { s } ^ { - 1 }$条件下，以$1 0 0 \mu \mathsf { m }$的刮刀间隙高度进行刮涂。随后，将薄膜在$1 5 0 ~ ^ { \circ } \mathrm { C }$下退火30分钟以形成致密层。钙钛矿吸收层随后使用上述气体淬火辅助刮涂法进行沉积。

对于空穴传输层，将$1 0 \mathrm { m g } \mathrm { m L } ^ { - 1 }$ P3HT溶解于无水氯苯中，并在$80 \%$下搅拌至少2小时。刮涂P3HT溶液时使用的间隙高度为$1 5 0 ~ { \mu \mathrm { m } }$，溶液体积为$4 0 ~ \mu \ L$。P3HT的涂布温度和速度分别为60 $^ \circ \mathsf { C }$和$5 \mathsf { m m } \mathsf { s } ^ { - 1 }$。涂覆P3HT层后，薄膜在100 $^ \circ \mathsf { C }$下退火5分钟。对于碳电极，将碳浆通过丝网印刷涂覆在制备好的薄膜上，并在$120 ^ { \circ } \mathsf { C }$下退火15分钟。为此，使用激光从胶带上切割出电极图案。随后将胶带粘性面朝下放置在基板上。通过刮涂将碳浆填入切割出的图案中。然后小心移除胶带，并将基板在热板上于$100 ^ { \circ } \mathsf { C }$下退火15分钟。

# 人物塑造：

太阳能电池的表征通过测量其电流-电压（J-V）特性完成，使用AAA级太阳光模拟器提供AM1.5G光照，并配合LOT-Quantum Design的源测量系统，该系统经认证的硅太阳能组件校准。电压扫描范围为$- 0 . 5$至$1 . 5 \lor$，步长为$2 0 \ \mathsf { m V } .$。钙钛矿薄膜的形貌通过共聚焦显微镜（FEI Apreo LoVac）成像。

扫描电子显微镜（SEM）：使用FEI Helios Nanolab 660获取SEM图像并制备FIB截面。离子束的最终抛光在$5 \mathsf { k V }$和80 pA条件下进行。

X射线粉末衍射（XRD）：采用经典的异位布拉格-布伦塔诺几何结构，使用帕纳科X'pert粉末衍射仪进行X射线衍射分析，该仪器配备滤波的Cu-Kα辐射和X'Celerator固态条带检测器。

样品的透射率和反射率光谱使用紫外-可见-近红外光谱仪（Perkin Elmer Lambda 950）测量。对于雾度测量，分别在不放置和放置反射标准件的情况下检测漫透射率和总透射率。配备R955 PMT的检测器工作波长为160 nm至900 nm。

钙钛矿薄膜的粗糙度和厚度通过NanoFocus AG的定制共聚焦显微镜μsurf测量。

原位白光反射光谱仪（WLRS，Thetametrisis）：为进行高质量反射测量，所有薄膜均沉积在切割成$1 \times 1$厘米基底的硅片上。钙钛矿湿膜的折射率（n）和消光系数（k）分别设定为$1 . 5 \pm 0 . 5$和$0 . 3 \pm 0 . 1$。

原位PL：PL测量在自建的共聚焦装置上进行，使用532 nm或450 nm激光二极管、基板上方的平凸透镜、550 nm长通滤波器和制造商校准的光纤耦合光谱仪（AVANTES，ULS2048XL Sensline系列）。平凸透镜与基板之间的距离经过优化，以使干膜的PL强度最大化。工作距离在干燥过程中不随湿膜厚度的变化而调整。

原位紫外-可见光谱：原位吸收测量使用配备钨卤素和氘灯光源（Filmetrics公司）的F20-UVX光谱仪（Filmetrics公司）进行。信号通过同一光纤耦合光谱仪检测，光谱范围为300至1000 nm。大多数测量中，每个光谱的积分时间为0.5秒（薄钙钛矿层）。紫外-可见吸收光谱根据透射光谱计算，使用以下公式：$\mathsf { A } \lambda = -$ $\mathsf { l o g } _ { 1 0 } ( \mathsf { T } )$，其中Aλ为特定波长（λ）下的吸光度，T为校准后的透射辐射。

# 3. 对正文章节“干燥速率对形态的影响及模型验证”的补充说明

# 3.1. 红外反射光谱与XRD谱图

![](images/1efef7f3339b0d00a0806896532a6609151cbf86fe3853531730d628c54e24ec.jpg)

![](images/44925768ea13d2f4d5ea7778137103496eb34811266afef2e12bcee890f0fb63.jpg)
图 S 10：环境干燥薄膜、退火后薄膜以及纯 NMP 的红外反射光谱。

对于纯 NMP，位于 1675 cm-1 处的强峰对应于 $\complement { = } \complement$ 对称伸缩振动，而环境干燥薄膜在相似位置有一个弱峰，但经过热退火处理后的环境干燥薄膜中此峰消失。因此，我们证实，如果不进行气体淬火处理，NMP 可能会残留在薄膜中，这与 XRD 图谱结果非常吻合。

![](images/fd926cfaad4b3db881ae3da6fa3ba64924a7691df01ddf99f3cff75d5a96fb1c.jpg)

![](images/bbc04d119078ae79cfd86d64c54f12ee9e370a9152fe14861b56c9daa8f6b7bb.jpg)
图 S 11：左图：所有实验干燥条件下的 XRD 光谱。右图：所有样品 (110) 峰的半高宽 (FWHM) 和强度。

关于 ED 薄膜的 XRD 图谱，我们发现在 $6 . 4 ^ { \circ }$ 、$7 . 8 ^ { \circ }$ 和 $9 . 3 ^ { \circ }$ 处存在峰，这表明 PbI2 晶体的晶格被大分子扩大了。这些大分子可能是 NMP，因为一些报道提到 PbI2(NMP) 的 XRD 峰位于 $8 . 1 ^ { \circ }$ 。峰位由晶格决定，层状 PbI2 具有弱键合，允许通过范德华相互作用插入不同的客体分子。

如图 S11 所示，观察到一组优选取向峰，分别位于 $1 4 . 1 5 ^ { \circ }$ 、28.44°、$3 1 . 8 5 ^ { \circ }$ 、$4 0 . 6 2 ^ { \circ }$ 和 $4 3 . 1 4 ^ { \circ }$ ，这些峰分别对应于 MAPbI3 钙钛矿四方结构的 (110)、(220)、(310)、(224) 和 (330) 晶面。在 2θ 值分别为 $2 0 . 0 3 ^ { \circ }$ 、$2 3 . 5 0 ^ { \circ }$ 和 $2 4 . 5 5 ^ { \circ }$ 处存在 (200)、(211) 和 (202) 晶面的次要峰，这清楚地表明所有钙钛矿薄膜都具有较高的相纯度。

如有必要，我们可以绘制 $1 4 . 1 5 ^ { \circ }$ 处 XRD 峰的半高宽和强度。 (110) 峰的半高宽和强度如图 S11b 所示，钙钛矿薄膜的结晶度随着蒸发速率的增加而增加。

# 3.2. 干燥后薄膜中溶剂捕获机制的可视化



![](images/7791923f78327f386c7b67c609758c02b73657710c309a3588614cd8e1dc4ae0.jpg)  
图 S 12：中等至慢蒸发速率模拟的典型干燥状态。图中显示了晶体有序参数和溶剂体积分数（作为插图）。左侧的溶剂被完全捕获在晶体与基底之间，因此几乎无法蒸发。右侧捕获的溶剂由于表面张力效应而无法蒸发：进一步蒸发将需要液体弯月面曲率的大幅增加，这将导致无法承受的表面能增加。

# 3.3. 退火过程中薄膜高度与结晶度的演变



![](images/532d04f2aee8125bb941e552363bb202fbec3a7d9cda397bcedfcb3549fe2a7b.jpg)

![](images/3fe0b6029f207b6711b5ec6876ffc009b6dda6053d8c93f3d92e5d0434d4906b.jpg)  
图 S 13：左图：包含退火过程的模拟薄膜高度。退火开始时可见薄膜高度略有下降，这有两个原因。首先，由于蒸气压突然增加，蒸发速率显著提高，导致先前被截留的溶剂快速蒸发。其次，薄膜-蒸气界面发生改变，这纯粹是数值效应。遗憾的是，这两个效应的具体影响程度无法独立评估。右图：包含退火过程的体系结晶度。退火开始时结晶度的增加同样是数值假象，源于退火起始阶段弥散性薄膜-蒸气界面结构的改变。这对薄膜内部整体结晶度的计算具有明显但有限的影响。

# 3.4. 模拟中晶体尺寸、未覆盖基底比例及粗糙度的评估



未覆盖基底比例是指模拟中垂直线段内溶质体积分数未超过0.8的线段所占比例。本次覆盖度评估选用溶质体积分数而非晶体序参数，是因为施加涨落作用导致晶体序参数场存在噪声。选择0.8作为阈值是因为超过该值时，干膜中的溶质始终处于结晶状态。

对于粗糙度计算，选取模拟箱各垂直线段中溶质体积分数超过0.8的最高点作为薄膜上边界。随后通过下式计算粗糙度：

$$
R _ {Q} = \sqrt {\frac {\sum_ {i = 1} ^ {N} \left(h _ {i} - h _ {f i n a l}\right) ^ {2}}{N}} \tag {S26}
$$

其中$N$表示列数。

针对晶体尺寸，计算每个独立晶粒（定义为具有均匀/相同取向值的区域）的等效半径。平均晶体尺寸计算公式如下：

$$
r = \frac {\sum_ {i = 1} ^ {N} v _ {i} r _ {i}}{V} \tag {S27}
$$

式中V为晶体总体积，$v _ { i }$表示第i个晶体的体积分数。

# 3.5. 扫描电子显微镜图像



![](images/78ccea75e4097cd37272acac397a1e185b53189224d6b290a4bd5e2200426ff0.jpg)  
图 S 14：第一行和第二行：退火后不同放大倍率的扫描电子显微镜俯视图。第三行：扫描电子显微镜横截面图。从左至右：制造过程中采用气体淬火时的空气压力分别为 0、0.2、0.5、0.8、1、1.5 和 2 巴。

# 3.6. 干燥与退火后的模拟薄膜形貌



![](images/037d8f8c64c316b298afff9fba17d50307dd1dfe0cbe914e6aa6c3f0778e0c29.jpg)  
图 S 15：干燥结束时的薄膜形貌。图中展示了晶体有序参数。不同行对应不同的蒸发速率。从上至下：$v _ { e v a p } = 6 7$ 、134、201、268、335、402、469、536、603 nm/s。各列代表五次完全相同的模拟参数运行结果，包括 ?K%&'。

![](images/61455abee1501593df20645cfff094dc0522ab656ea21eebdf1b8a32da8793cc.jpg)  
图 S 16：退火结束时的薄膜形貌（时间跨度为30秒）。图中展示了晶体有序参数。不同行对应不同的蒸发速率。从上至下：$v _ { e v a p } = 6 7$ 、134、201、268、335、402、469、536、603 nm/s。各列代表五次完全相同的模拟参数运行结果，包括 ?K%&'。

# 3.7. 干燥后与退火后薄膜形貌的对比



![](images/c1edd40c7799541ef3ea141b54d948853c02337269ade67147d5d09a4a30dcdd.jpg)

![](images/fe5fd650c2af6b1a35d48277916148886d74dd4336e91623a4a825cda56f7044.jpg)

![](images/27d1580b6e5c17177d38d2285addfb192f02ee3046aa720104710be333e9b7e0.jpg)  
图 S 17：干燥后与 30 秒退火后形貌描述符的对比。（左）由于晶粒粗化，晶体尺寸在退火过程中增大。对于低蒸发速率，形貌特征仅为少数、大而分离的晶体，因此该效应不太明显。（中）薄膜粗糙度：如果固-气界面的晶体因粗化而消失，薄膜的粗糙度保持不变或略有下降。（右）未覆盖基底：由于粗化作用，退火过程中未覆盖的基底面积减少。

# 3.8. 雾度因子



![](images/aceecab4461a36a07e2ecf47ac48acee0a458e12497837f20c9541be9b794ec0.jpg)  
图 S 18：雾度因子：雾度因子是评估薄膜光散射能力的一种测量指标。雾度因子通过漫透射与总透射的比值计算得出。自然干燥的薄膜在长波长处表现出非常高的雾度，这可能归因于未覆盖区域，导致了高光散射。对于使用较高空气流速（即1.0巴）处理的薄膜，其雾度因子低于 $10 \%$ ，表明薄膜表面光滑，使得光在低散射下被吸收。

# 3.9. 光致发光晶粒尺寸与紫外-可见光谱

![](images/92ad21cea13097d6620aab223db05bd6df78a345e78174bfdb0fa9a9fe502248.jpg)

![](images/ca6ee6e3dde1d82feef2d69467c26524646acd06b5eea120b0d33f25548b6f48.jpg)

![](images/088db8508e4f0da81babc4b1a70efc39cf2d9a3b3ebae279c6bd534e65dea0ad.jpg)

![](images/4afbdf6f8252d3905eabd3d8ac87af1a32b9d55009f551851b6eb80d373044b0.jpg)

![](images/19fd0b7f1a9f4a465ca791ab93414932141a9cc68c9f6104e4d0067f96547c56.jpg)

![](images/83d2bc86360d02147542acfa52f65cbeaf1bba6d989eed1188acee5cab2a08a3.jpg)  
图 S 19：环境干燥、0.2 bar 和 2 bar 条件下测得的光致发光曲线（从左至右）。第一行：光谱图，第二行：热图。

晶体的晶粒尺寸可通过以下公式计算 14,15：

$$
E _ {g} = E _ {g, b u l k} + \frac {2 \pi^ {2} \hbar^ {2}}{m _ {e} d ^ {2}}, \tag {S28}
$$

其中 $E _ { g , b u l k }$ 为块体材料的带隙能量，$\hbar$ 为约化普朗克常数，$m _ { e }$ 为激子的有效质量，$d$ 为晶粒的平均尺寸。

![](images/01ef567a7efa9f31acd2323070dcfaac2c7e81faea659e49a54d82f984f15ca1.jpg)

![](images/86a7fd8c1b82cf402e8659d6c9dcc43330aa67941dd8cac7742620af14275f25.jpg)

![](images/705de284d81b00bc1b6f1020d901cd7f90e5d829acd9fa103904f776d5a76063.jpg)  
图 S 20：环境干燥、0.2 bar 和 2 bar 空气压力条件下测得的紫外-可见光谱（从左至右）。

# 4. 对正文“器件性能对薄膜形貌的依赖性”章节的补充信息

# 4.1. 稳定功率输出



![](images/cf72b50499f72d9e0de7a8be7d39a9eba9265dffc8ff1416af3c6095972c616f.jpg)

![](images/0e72d0aec960d40def75db0257ae41f8878437cfdfe39ef4757c2ec62822b206.jpg)  
图 S 21：左图：稳定功率输出。右图：冠军电池在最大功率点处的随时间变化的光电流和光电转换效率。

# 4.2. 冠军电池的JV扫描与器件良率



![](images/e22ba0ebfe26d1b9181f9a56b4f6334a97811c137487242767a687690970d829.jpg)

![](images/51b42b958875a6afb7cb2d0d70e1c6ffd127e168d9c3bc1346fff20e188ef569.jpg)  
图 S 22：左图：冠军电池的正向与反向扫描。右图：基于不同蒸发速率（分别为0、0.2、0.5、0.8、1.0、1.5和2.0 bar）制备的钙钛矿薄膜所测太阳能电池的器件良率。

# 4.3. 漂移-扩散模拟

![](images/2e6765a38fa0a1c655a3ca5fe07696105dd92b8e032dca73982e51af6d13f037.jpg)

![](images/6b4915fc4108aad50fa8b252615b577c8dc00689c705e550ed0008373ad80b03.jpg)  
图 S 23：漂移扩散模拟。第一行：实验（叉号）与模拟（实线）JV曲线。拟合参数包括界面处的陷阱密度、产生率、串联电阻和分流电阻。电子和空穴迁移率、体陷阱密度以及离子密度均保持恒定，但0 bar和0.2 bar蒸气压的情况除外。在这两个压力下，若保持这三个参数恒定，则无法获得合理的拟合结果。所得数值显示在第二行。随着气压降低，分流电阻减小而陷阱密度增加。其余参数大致保持恒定。另请注意，高电压下JV曲线的微弱斜率及其S形特征无法仅通过串联电阻的变化来解释。

<table><tr><td>Parameters</td><td>Full Name</td><td>Value</td><td>Unit</td></tr><tr><td>T</td><td>Temperature</td><td>295</td><td>K</td></tr><tr><td>L</td><td>Total thickness of the device</td><td>470·10-9</td><td>m</td></tr><tr><td>eps_r</td><td>Relative dielectric constant</td><td>24</td><td></td></tr><tr><td>CB</td><td>Conduction band edge</td><td>3.9</td><td>eV</td></tr><tr><td>VB</td><td>Valence band edge</td><td>5.49</td><td>eV</td></tr><tr><td>Nc</td><td>Effective density of states</td><td>5·1024</td><td>m-3</td></tr><tr><td>n_0</td><td>Ionised n-doping</td><td>0</td><td>m-3</td></tr><tr><td>p_0</td><td>Ionised p-doping</td><td>0</td><td>m-3</td></tr><tr><td>L_TCO</td><td>Tickness of the ITO layer</td><td>110·10-9</td><td>m</td></tr><tr><td>L_BE</td><td>Tickness of the back electrode</td><td>200·10-9</td><td>m</td></tr><tr><td>lambda_min</td><td>Minimum wavelength of the spectrum for the calculated generation profile</td><td>350·10-9</td><td>m</td></tr><tr><td>lambda_max</td><td>Maximum wavelength of the spectrum for the calculated generation profile</td><td>800·10-9</td><td>m</td></tr><tr><td>mun_0</td><td>Electron mobility at zero field</td><td>6·10-4(fitted for 0,0.2 bar)</td><td>m2/Vs</td></tr><tr><td>mup_0</td><td>Hole mobility at zero field</td><td>6·10-4(fitted for 0,0.2 bar)</td><td>m2/Vs</td></tr><tr><td>mob_n_dep</td><td>Electron mobility</td><td>0,constant</td><td></td></tr><tr><td>mob_p_dep</td><td>Hole mobility</td><td>0,constant</td><td></td></tr><tr><td>W_L</td><td>Work function of the left electrode</td><td>4.25</td><td>eV</td></tr><tr><td>W_R</td><td>Work function of the right electrode</td><td>5.1</td><td>eV</td></tr><tr><td>Sn_L</td><td>Surface recombination velocity of electrons at the left electrode</td><td>-1·10-7</td><td>m/s</td></tr><tr><td>Sp_L</td><td>Surface recombination velocity of holes at the left elecctord</td><td>-1·10-7</td><td>m/s</td></tr><tr><td>Sn_R</td><td>Surface recombination velocity of electrons at the right electrode</td><td>-1·10-7</td><td>m/s</td></tr><tr><td>Sp_R</td><td>Surface recombination velocity of holes at the right electrode</td><td>-1·10-7</td><td>m/s</td></tr><tr><td>Rshunt</td><td>Shunt resistance</td><td>5·103(fitted)</td><td>Ωm2</td></tr><tr><td>Rseries</td><td>Resistance place in series with the device</td><td>2·10-4(fitted)</td><td>Ωm2</td></tr><tr><td>L_LTL</td><td>Thickness of the left transport layer</td><td>20·10-9</td><td>m</td></tr><tr><td>L_RTL</td><td>Thickness of the right transport layer</td><td>50·10-9</td><td>m</td></tr><tr><td>Nc_LTL</td><td>Effective density of states of the left transport layer</td><td>2.7·1024</td><td>m-3</td></tr><tr><td>Nc_RTL</td><td>Effective density of states of the right transport layer</td><td>5·1026</td><td>m-3</td></tr><tr><td>doping_LTL</td><td>Density of ionized dopants of the left transport layer</td><td>0</td><td>m-3</td></tr><tr><td>doping_RTL</td><td>Density of ionized dopants of the right transport layer</td><td>0</td><td>m-3</td></tr><tr><td>mob_LTL</td><td>Mobility of electrons and holes in the left transport layer</td><td>5·105</td><td>m2/Vs</td></tr><tr><td>mob_RTL</td><td>Mobility of electrons and holes in the right transport layer</td><td>5·107</td><td>m2/Vs</td></tr><tr><td>nu_int_LTL</td><td>Interface transfer velocity between the main layer and the left transport layer</td><td>1·103</td><td>m/s</td></tr><tr><td>nu_int_RTL</td><td>Interface transfer velocity between the main layer and the right transport layer</td><td>1·103</td><td>m/s</td></tr><tr><td>eps_r_LTL</td><td>Relative dielectric constant of the left transport layer</td><td>10</td><td></td></tr><tr><td>eps_r_RTL</td><td>Relative dielectric constant of the right transport layer</td><td>3</td><td></td></tr><tr><td>CB_LTL</td><td>Conduction band edge of the left transport layer</td><td>4.2</td><td>eV</td></tr><tr><td>CB_RTL</td><td>Conduction band edge of the right transport layer</td><td>3</td><td>eV</td></tr><tr><td>VB_LTL</td><td>Valence band edge of the left transport layer</td><td>8.4</td><td>eV</td></tr><tr><td>VB_RTL</td><td>Valence band edge of the right transport layer</td><td>5.15</td><td>eV</td></tr><tr><td>TLsGen</td><td>Transport layer absorption</td><td>0, no</td><td></td></tr><tr><td>TLsTraps</td><td>Transport layer contain traps</td><td>0, no</td><td></td></tr><tr><td>InosInTls</td><td>Ions can move from the bulk into the transport layers</td><td>0, no</td><td></td></tr><tr><td>CNI</td><td>Concentration of negative ions</td><td>2·1022 (fitted for 0, 0.2 bar)</td><td>m-3</td></tr><tr><td>CPI</td><td>Concentration of positive ions</td><td>2·1022 (fitted for 0, 0.2 bar)</td><td>m-3</td></tr><tr><td>mob/ion_spec</td><td>Which ionic species can move</td><td>1, only positive</td><td></td></tr><tr><td>ion_red_rate</td><td>Rate at which the ion distribution is updated</td><td>1</td><td></td></tr><tr><td>Gehp</td><td>Average generation rate of the electron-hole pairs in the absorbing layer</td><td>2.83·1027 (fitted)</td><td>m-3s-1</td></tr><tr><td>Gfrac</td><td>Actual average generation rate as a fraction of Gehp</td><td>1</td><td></td></tr><tr><td>Gen_profile</td><td>File of the generation profile</td><td>None, uniform</td><td></td></tr><tr><td>Field_dep_G</td><td>Field-dependent splitting of the electron-hole pairs</td><td>0, no</td><td></td></tr><tr><td>kdirect</td><td>Rate of direct recombination</td><td>1.6·10-17</td><td>m3/s</td></tr><tr><td>UseLangevin</td><td>Constant rate of recombination of Langevin expression</td><td>0, direct recombination</td><td></td></tr><tr><td>Bulk_tr</td><td>Density of traps in the bulk</td><td>1.04·1020 (fitted)</td><td>m-3</td></tr><tr><td>St_L</td><td>Number of traps per area at the left interface between the left transport layer and the main absorber</td><td>2·1012 (fitted)</td><td>m-2</td></tr><tr><td>St_R</td><td>Number of traps per area at the left interface between the left transport layer and the main absorber</td><td>\( 1 \cdot 10^{10} (fitted) \)</td><td>\( m^{-2} \)</td></tr><tr><td>num_GBs</td><td>Number of grain boundaries</td><td>0</td><td></td></tr><tr><td>GB_tr</td><td>Number of traps per area at a grain boundary</td><td>\( 1 \cdot 10^{13} \)</td><td>\( m^{-2} \)</td></tr><tr><td>Cn</td><td>Capture coefficient for electrons (for all traps)</td><td>\( 1 \cdot 10^{-13} \)</td><td>\( m^3 \)</td></tr><tr><td>Cp</td><td>Capture coefficient for holes (for all traps)</td><td>\( 1 \cdot 10^{-13} \)</td><td>\( m^3 \)</td></tr><tr><td>ETrapSingle</td><td>Energy level of all traps</td><td>4.91</td><td>eV</td></tr><tr><td>Tr_type_L</td><td>Traps at the left interface</td><td>-1, acceptor</td><td></td></tr><tr><td>Tr_type_R</td><td>Traps at the right interface</td><td>1, donor</td><td></td></tr><tr><td>Tr_type_B</td><td>Traps at grain boundaries and in the bulk</td><td>-1, acceptor</td><td></td></tr><tr><td>Vdistribution</td><td>Distribution of voltages that will be simulated</td><td>1, uniform</td><td></td></tr><tr><td>PreCond</td><td>Use of pre-conditioner</td><td>0, no</td><td></td></tr><tr><td>Vscan</td><td>Direction of voltage scan</td><td>-1, down</td><td></td></tr><tr><td>Vmin</td><td>Minimum voltage that will be simulated</td><td>0.0</td><td>V</td></tr><tr><td>Vmax</td><td>Maximum voltage that will be simulated</td><td>1.4</td><td>V</td></tr><tr><td>Vstep</td><td>Voltage step</td><td>0.01</td><td>V</td></tr><tr><td>until_Voc</td><td>Simulation termination at Voc</td><td>0, no</td><td></td></tr></table>

# 4.4. 稳态光致发光光谱与时间分辨光致发光

![](images/36d2f2212568127e32294520b73219f0475c9f49f40b0df2abf02fbb22df0c38.jpg)

![](images/16ae9a8505fdc59c4ec801d98c0542652820c2e9c93ea753447966b8cd04f5b4.jpg)  
图 S 24：左：稳态光致发光。右：时间分辨光致发光。

通过稳态光致发光和时间分辨光致发光衰减测量来研究钙钛矿薄膜中的电荷复合行为。如图 S 24 所示，随着蒸发速率的增加，观察到光致发光强度增强和平均载流子寿命延长，这表明在高气流条件下处理的薄膜中非辐射复合中心减少。这些结果可以解释为由于界面非辐射复合降低而导致的开路电压提升，这与薄膜形貌的观察结果高度一致。

# 5. 文献综述

(1) Ronsin, O. J. J.; Harting, J. 有机太阳能电池中晶体体异质结的形成：来自相场模拟的见解。ACS Appl. Mater. Interfaces 2022, 14 (44), 49785−49800. https://doi.org/10.1021/acsami.2c14319.
(2) Shargaieva, O.; Näsström, H.; Li, J.; Többens, D. M.; Unger, E. L. 不同溶剂中甲基铵碘化铅钙钛矿的温度依赖性结晶机制。Frontiers in Energy Research 2021, 9.
(3) Ronsin, O. J. J.; Harting, J. 蒸发结晶多组分薄膜中形态形成的相场模拟。Advanced Theory and Simulations 2022, 2200286. https://doi.org/10.1002/adts.202200286.
(4) Matkar, R. A.; Kyu, T. 晶体-非晶相互作用在晶体-非晶聚合物共混物相平衡中的作用。J. Phys. Chem. B 2006, 110 (25), 12728– 12732. https://doi.org/10.1021/jp061159m.
(5) Persad, A. H.; Ward, C. A. Hertz-Knudsen关系中蒸发与凝结系数的表达式。Chemical Reviews 2016, 116 (14), 7727–7767. https://doi.org/10.1021/acs.chemrev.5b00511.
(6) Knudsen, M. 汞的最大蒸发速度。Annalen der Physik 1915, 352 (13), 697–708. https://doi.org/10.1002/andp.19153521306.
(7) Hertz, H. 论液体，特别是汞在真空中的蒸发。Annalen der Physik 1882, 253 (10), 177–193. https://doi.org/10.1002/andp.18822531002.
(8) Ronsin, O. J. J.; Jang, D.; Egelhaaf, H.-J.; Brabec, C. J.; Harting, J. 流体混合物液-汽平衡与蒸发的相场模拟。ACS Appl. Mater. Interfaces 2021, 13 (47), 55988–56003. https://doi.org/10.1021/acsami.1c12079.
(9) Jaensson, N. O.; Hulsen, M. A.; Anderson, P. D. 含悬浮刚性颗粒两相流的Stokes–Cahn–Hilliard公式与模拟。Computers & Fluids 2015, 111, 1–17. https://doi.org/10.1016/j.compfluid.2014.12.023.
(10) Nauman, E. B.; Balsara, N. P. 相平衡与Landau—Ginzburg泛函。Fluid Phase Equilibria 1989, 45 (2–3), 229–250. https://doi.org/10.1016/0378-3812(89)80260-2.
(11) Cabral, J. T.; Higgins, J. S. 聚合物共混物中的旋节线纳米结构：论Cahn-Hilliard长度尺度预测的有效性。Progress in Polymer Science 2018, 81, 1–21. https://doi.org/10.1016/j.progpolymsci.2018.03.003.
(12) König, B.; Ronsin, O. J. J.; Harting, J. 二元混合物旋节分解粗化动力学的二维Cahn–Hilliard模拟。Phys. Chem. Chem. Phys. 2021, 23 (43), 24823–24833. https://doi.org/10.1039/D1CP03229A.
(13) Siber, M.; J. Ronsin, O. J.; Harting, J. 二元混合物相场模拟中的晶体形态形成。Journal of Materials Chemistry C 2023, 11 (45), 15979–15999. https://doi.org/10.1039/D3TC03047D.
(14) Yu, H.; Wang, H.; Zhang, J.; Lu, J.; Yuan, Z.; Xu, W.; Hultman, L.; Bakulin, A. A.; Friend, R. H.; Wang, J.; Liu, X.-K.; Gao, F. 原位合成钙钛矿量子点的高效可调电致发光。Small 2019, 15 (8), 1804947. https://doi.org/10.1002/smll.201804947.
(15) Ummadisingu, A.; Meloni, S.; Mattoni, A.; Tress, W.; Grätzel, M. 钙钛矿薄膜中晶体尺寸诱导的带隙调控。Angewandte Chemie International Edition 2021, 60 (39), 21368–21376. https://doi.org/10.1002/anie.202106394.