# 自由能基础理论

<span class='git-page-authors'><a href='mailto:jane@abc.com'>Jane Doe</a>

## 什么是自由能
热力学观点 (恒温恒体积下)：

$$F = U - TS$$

即一个体系的（亥姆霍兹）自由能$F$包含两个部分，第一个部分是体系的内能，第二个部分是体系的熵（混乱度）。由于热力学第二定我们知道，孤立系统总是会朝着熵增的状态变化。而热力学第二定律在恒温恒体积下的表述为：系统总是会朝着自由能$F$变小的状态变化。而由上面的公式我们可以看到，这一趋势被两个系统状态量所决定：1. 系统会倾向于向内能$U$小的状态变化。2.系统会倾向于向熵$S$大的状态变化。并且由于熵前面的系数温度$T$的存在，我们会立刻发现，温度高的时候系统状态的变化受熵的影响更大，温度低的时候系统状态受内能的影响更大。

统计力学观点:

$$
F = - \frac{1}{\beta} \ln Z, Z =\int \mathrm{d}^N \mathbf{r} \mathrm{e}^{-\beta E \left(\mathbf{r}_1, \ldots, \mathbf{r}_N\right)}
$$

其中$\beta = \frac{1}{k_B T}$, $Z$为体系的配分函数, 从自由能$F$的统计力学定义来看, 体系的自由能完全取决于能量$E$在坐标空间的大小和分布。为了让自由能变小，体系会倾向于呈现能量$E$小的状态，并且由于积分号的存在，体系会倾向于形成同能量下微观状态数多的状态，这其实也就是热力学中的熵。

## 自由能的计算
由前述定义，一个直接的观察是，体系的自由能$F$取决于内能$U$的定义，由于能量定义的相对性，体系的自由能$F$的绝对数值也是没有意义的。通常情况下我们几乎总是关心的是系统在两个状态之间自由能的变化值，即：

$$
\Delta F = F_B - F_A
$$

根据自由能的统计力学定义，这里的自由能变化可以写作：

$$
\Delta F = - k_B T \ln Z_B + k_B T \ln Z_A = - k_B T \ln \frac{Z_B}{Z_A}
$$

其中$Z_A$和$Z_B$分别为系统在状态A和状态B下的配分函数，即：

$$
\begin{aligned}
Z_{\mathcal{A}} & =\int \mathrm{d}^N \mathbf{r} \mathrm{e}^{-\beta U_{\mathcal{A}}\left(\mathbf{r}_1, \ldots, \mathbf{r}_N\right)} \\
Z_{\mathcal{B}} & =\int \mathrm{d}^N \mathbf{r} \mathrm{e}^{-\beta U_{\mathcal{B}}\left(\mathbf{r}_1, \ldots, \mathbf{r}_N\right)} .
\end{aligned}
$$

到这里，关于自由能计算的定义就介绍完了。接下来的所有内容都是关于如何计算它，特别地，由于这是一本关于分子动力学的教程，我们真正关心的问题是：如何利用分子动力学模拟来计算自由能。

如果我们知道了系统在状态A和状态B下能量函数$U(r)$的形式，那么配分函数的计算是直接的，但一般情况下我们是不知道的，这也是我们为什么要费劲用分子动力学这个工具的其中一个原因。然而，对于分子动力学来说，我们通常是没法得到关于体系在某个状态下的配分函数的，我们能得到的，是某个物理量在系统该状态下的系综分布（通常是恒温恒体积）下的系综平均（时间平均）。因此，要用分子动力学的手段来得到体系状态的自由能变化，我们的核心思想是把自由能的变化转换成某个物理量的系综平均，这也是大部分自由能计算方法的出发点。

接下来我们将看到两大计算自由能的思路，平衡态方法和非平衡态方法。

## 平衡态自由能计算方法
### 自由能微扰（FEP）
为了将体系的自由能变化写成某个物理量的系综平均，我们注意到，体系自由能变化中的配分函数部分可以写成：

$$
\begin{aligned}
\frac{Z_{\mathcal{B}}}{Z_{\mathcal{A}}} & =\frac{1}{Z_{\mathcal{A}}} \int \mathrm{d}^N \mathbf{r} \mathrm{e}^{-\beta U_{\mathcal{A}}\left(\mathbf{r}_1, \ldots, \mathbf{r}_N\right)} \mathrm{e}^{-\beta\left(U_{\mathcal{B}}\left(\mathbf{r}_1, \ldots, \mathbf{r}_N\right)-U_{\mathcal{A}}\left(\mathbf{r}_1, \ldots, \mathbf{r}_N\right)\right)} \\
& =\left\langle\mathrm{e}^{-\beta\left(U_{\mathcal{B}}\left(\mathbf{r}_1, \ldots, \mathbf{r}_N\right)-U_{\mathcal{A}}\left(\mathbf{r}_1, \ldots, \mathbf{r}_N\right)\right)}\right\rangle_{\mathcal{A}},
\end{aligned}
$$

因此体系的自由能变化就变成了：

$$
\Delta F_{\mathcal{A B}}=-k T \ln \left\langle\mathrm{e}^{-\beta\left(U_{\mathcal{B}}-U_{\mathcal{A}}\right)}\right\rangle_{\mathcal{A}} .
$$

从分子动力学采样的角度，这个公式可以解释为，我们利用系统在状态A下的势能面进行采样，得到系统在状态A下的系综分布的一系列构象，对每一个这样的构象，我们计算$\mathrm{e}^{-\beta\left(U_{\mathcal{B}}-U_{\mathcal{A}}\right)}$, 最终得到的这一些列构象的平均值就是该物理量的系综平均。

注意系统在状态A和状态B时势能的定义$U_A$和$U_B$的定义时不同的，正因为如此，对于状态A来说的低能构象不一定也是对于状态B的低能构象。当状态A和状态B相差较大的时候，很可能对于我们采样到的状态A系综下的构象，计算状态B下的能量都会是高能构象，此时$\mathrm{e}^{-\beta\left(U_{\mathcal{B}}-U_{\mathcal{A}}\right)}$权重因子会很小，而权重因子很大的构象由于我们分子动力学采样的时间有限，无法采样到。这就造成了我们实际计算的时候的一个效率问题，如果状态A和状态B差距很大的话，我们就需要非常长的时间才能得到一个收敛的自由能差估计。

为了解决这个采样效率的问题，我们的解决方案是，由于自由能是一个平衡态的状态量，我们可以通过设计一条从状态A和状态B的路径，然后计算这条路径上相邻两个状态之间的自由能差，那么最终的状态A和状态B的自由能差就可以表示为：

$$
\Delta F_{\mathcal{A B}}= \sum_{\alpha=1}^{M-1}  F_{\alpha+1} - F_{\alpha} = -k T \sum_{\alpha=1}^{M-1} \ln \left\langle\mathrm{e}^{-\beta \Delta U_{\alpha, \alpha+1}}\right\rangle_\alpha,
$$

由于路径相邻状态间的差距比较小，因此其自由能差的收敛是比较快的，我们可以同时对路径上的各个状态进行采样，从而更快的得到一个收敛的自由能差，这就是自由能微扰方法。

### BAR/MBAR

在前述自由能微扰理论的推导过程中，我们发现关键的一步在于对配分函数之比的变形，即：

$$
\begin{aligned}
\frac{Z_{\mathcal{B}}}{Z_{\mathcal{A}}} & =\frac{1}{Z_{\mathcal{A}}} \int \mathrm{d}^N \mathbf{r} \mathrm{e}^{-\beta U_{\mathcal{A}}\left(\mathbf{r}_1, \ldots, \mathbf{r}_N\right)} \mathrm{e}^{-\beta\left(U_{\mathcal{B}}\left(\mathbf{r}_1, \ldots, \mathbf{r}_N\right)-U_{\mathcal{A}}\left(\mathbf{r}_1, \ldots, \mathbf{r}_N\right)\right)} \\
& =\left\langle\mathrm{e}^{-\beta\left(U_{\mathcal{B}}\left(\mathbf{r}_1, \ldots, \mathbf{r}_N\right)-U_{\mathcal{A}}\left(\mathbf{r}_1, \ldots, \mathbf{r}_N\right)\right)}\right\rangle_{\mathcal{A}},
\end{aligned}
$$

那么问题来了，这样的变形显然不是唯一的，比如，我们可以采取如下的变形方式：

$$
\frac{Z_B}{Z_A}=\frac{Z_B}{Z_A} \frac{\int W e^{-U_B-U_A} d \mathbf{q}}{\int W e^{-U_B-U_A} d \mathbf{q}}=\frac{\left\langle W e^{-U_B}\right\rangle_A}{\left\langle W e^{-U_A}\right\rangle_B}
$$

在这个变形中任意的W函数的选择都是可以的，特别地，如果我们选取$W = e^{U_A}$, 那么这个变形就回归到了前述FEP方法中的式子。

那么现在一个问题来了，什么样的W函数形式的选取可以让我们的变形达到最优呢？更确切地来说，什么样的选取可以让我们利用这个变形进行分子动力学的采样的时候达到最好的收敛性？面对这个问题，BAR方法应运而生。

BAR,全称为Bennett acceptance ratio, 是1976年Bennet提出的一个自由能计算的方法，这个方法的核心就在于选取这个M函数的形式。详细的推导可见[Bennet 1976](http://www2.stat.duke.edu/~scs/Courses/Stat376/Papers/NormConstants/FreeEnergy/BennettJCompPhys1976.pdf). 下面我们直接给出结果, 假设我们利用分子动力学模拟在体系状态A时的采样数目为$N_A$, 在体系状态B的采样数目为$N_B$，那么让配分函数之比在该采样下方差最小的W函数的选取为：

$$W = \frac{1}{\frac{Z_B}{N_B} e^{-U_A}+\frac{Z_A}{N_A} e^{-U_B}} $$

注意到，这里的W函数时取决于$Z_B$和$Z_A$的数值的，因而W函数和配分函数是相互依赖的，在实际计算中我们是需要进行一个自洽的计算迭代。

由上述所述，用BAR方法可以来计算两个态之间的自由能差，虽然W函数的选取已经是在两个态已有采样下最优的选择，但是其依然存在A和B两个状态相差过大时采样效率过低的问题。那么我们能否效仿FEP，来计算多个态之间的自由能差呢？MBAR方法，即Multistate Bennett Acceptance Ratio， 便是BAR的多态推广。

简而言之，MBAR方法要解决的问题时：面对一个系统的K个状态，我们有对这K个状态分别的一系列采样，对每个态的采样数目分别为$N_i$, 那么我们如何以最优的方式来计算两两状态之间的自由能差呢？即：

$$
\Delta F_{i j}=-\beta^{-1} \ln \frac{Z_j}{Z_i}
$$

正如同BAR方法一样，我们同样有对两两配分函数之比的变形，即：

$$
Z_i\left\langle\alpha_{i j} \exp \left(-\beta U_j\right)\right\rangle_i=Z_j\left\langle\alpha_{i j} \exp \left(-\beta U_i\right)\right\rangle_j
$$

MBAR方法的结论是我们对系数$\alpha_{i j}$有最优的选取，即：

$$
\alpha_{i j}=\frac{N_j{\hat{z_j}}^{-1}}{\sum_{k=1}^K N_k{\hat{z_k}}^{-1} \exp \left(-\beta U_k\right)}
$$

其中$\hat{z_i}$ 是我们根据目前的采样对各个配分函数的估计，可以看到这依然是一个自洽迭代的计算公式。

### 哈密顿量热力学积分（Hamiltonian integration)
我们介绍了两种常见的自由能计算方法，并且可以看到MBAR方法是FEP方法的一个推广。接下来让我们以更普适的观点来看待自由能的计算。

前面介绍的两种方法，FEP和MBAR方法都需要对一个系统的多个态进行采样，并且进行势能函数的计算，在这个过程中我们需要注意到的一点是：对于一个系统的不同态，势能函数其实也是在发生变化的。这一点非常重要，实际上这也是我们能够进行自由能计算的出发点。更确切地说，对于实际系统进行计算的时候，势能函数的形式为：

$$U = U(\mathbf{r}, \lambda (\mathbf{r}))$$

用另外一个表达方式来说，一个系统的不同状态实际上拥有着不同的哈密顿量：

$$H = H(\mathbf{r}, \lambda (\mathbf{r}))$$

而我们最终得到的不同态之间的自由能差，或者说不同状态的自由能，实际上就是这个函数中变量$\lambda$的函数。具体来说，如果我们计算一个配体和受体的结合自由能，那么初始状态A：配体和受体分开的时候，整个系统的哈密顿量是不包含受体和配体的相互作用函数的。而最终状态B：配体和受体结合的时候，系统的哈密顿量实际上是包含了受体和配体的相互作用函数。并且这个相互作用的打开时逐渐的。

我们前面介绍的两种方法：FEP和MBAR，它们刻画系统不同状态的哈密顿量的改变都是隐式的，都是通过改变系统的构象，利用MD内置的势能函数隐式地改变系统的哈密顿量，也就是说这里的$\lambda$是一个隐变量。这里我们得到的不同状态的自由能我们不知道是系统哪个具体变量的函数，只知道是和系统整体状态有关的一个变量。那么我们是否有办法显示地把系统不同态的哈密顿量的变化写出来呢？当然是可以的，既然自由能是系统的一个状态函数，那么我们自然可以认为的设计一条路径来让系统从状态A演化到状态B。

我们定义如下的一系列哈密顿量：

$$
\mathcal{H}(\mathbf{x}, \lambda)=(1-\lambda) \mathcal{H}_A+\lambda \mathcal{H}_B
$$

由于系统哈密顿量显含变量$\lambda$,那么自然系统的自由能也显含$\lambda$，即:

$$
F(N, V, T, \lambda)=-k_B T \ln Z(N, V, T, \lambda)
$$

由于这个显示的表达式，我们可以直接写出自由能对于变量$\lambda$的导数：

$$
\begin{aligned}
\frac{\partial F}{\partial \lambda} & =-k_B T \frac{\frac{\partial}{\partial \lambda} Z(N, V, T, \lambda)}{Z(N, V, T, \lambda)} \\
& =-k_B T \frac{\int \exp [-\beta \mathcal{H}(\mathbf{x}, \lambda)] \cdot(-\beta) \frac{\partial \mathcal{H}}{\partial \lambda} \mathrm{d} \mathbf{x}}{\int \exp [-\beta \mathcal{H}(\mathbf{x}, \lambda)] \mathrm{d} \mathbf{x}} \\
& =\left\langle\frac{\partial \mathcal{H}}{\partial \lambda}\right\rangle_\lambda \\
& =\left\langle U_B-U_A\right\rangle_\lambda
\end{aligned}
$$

由于积分的定义，我们自然可以得到自由能差的公式：

$$
\Delta F = F_B - F_A =\int_0^1\left\langle U_B-U_A\right\rangle_\lambda \mathrm{d} \lambda
$$

在实际的采样中，我们利用这个公式的方式是，在不同的离散$\lambda$值处做一系列采样，然后分别计算对应的$U_B - U_A$，最终求和，得到近似的自由能差的估计。

### 伞形采样 (Umbrella sampling)
通过上一节热力学积分理论中的讲解，我们认识到了自由能计算中的出发点，便是或隐式(FEP和MBAR)或显式（HI方法）地利用一些变量来表达哈密顿量（势能函数）的变化，再通过采样的方式来估计地计算自由能差。我们凭借着这个认知，来看一个新的采样（同时也是自由能计算的）方法：伞形采样，这也是一种显式地表达哈密顿量变化的采样方法。

在伞形采样中，我们定义一个集合变量$\xi(r)$,用这个显式的集合变量来表达系统状态的变化,并且认为和这个集合变量无关的坐标对系统状态变化的刻画影响很小。因此系统的哈密顿量就变成了这个集合变量的函数，即：
$$H = H(\mathbf{r}, \xi (\mathbf{r}))$$
同时，正如哈密顿量积分方法中要在不同的参数$\lambda$值处采样一样，在伞形采样中，我们要在集合变量$\xi(r)$值不同的值处进行大量的采样。而伞形采样实现这一种采样的方式是针对集合变量$\xi(r)$施加一个很大的限制势函数，即：

$$
\omega_i(\xi)=K / 2\left(\xi(r)-\xi_i^{\mathrm{ref}}\right)^2
$$

加上偏置势之后的总势函数为：

$$
E^{\mathrm{b}}(r)=E^{\mathrm{u}}(r)+\omega_i(\xi)
$$

而我们知道，自由能是一个系统平衡态的性质，换句话说，自由能应该由系统的平衡势函数所决定，即：

$$ 
F_i (\xi) = - \frac{1}{\beta} \int \exp [-\beta E^{u}(r)] \delta\left[\xi(r)-\xi\right] d^{N}{r} =- \frac{1}{\beta} P_{i}^{\mathrm{u}}(\xi)
$$

其中 $P_{i}^{\mathrm{u}}(\xi)$ 为体系在平衡状态下关于集合变量$\xi(r)$的概率分布：

$$
P_{i}^{\mathrm{u}}(\xi)=\frac{\int \exp [-\beta E(r)] \delta\left[\xi(r)-\xi\right] d^{N}{r}}{\int \exp [-\beta E(r)] d^{N}{r}}
$$

另一方面，伞形采样中系统是在加了偏置势之后的总势函数$E^{\mathrm{b}}(r)$下演化的，在伞形采样中我们真正要问的问题其实是：如何利用在加了偏置势函数之后的轨迹中进行平衡自由能的计算。为了达到这一目的，我们来尝试利用偏置势函数来表达平衡的自由能。首先我们可以写出在偏置势函数下，体系关于集合变量$\xi(r)$的概率分布：

$$ P_{i}^{\mathrm{b}}(\xi)=\frac{\int \exp \left\{-\beta\left[E(r)+\omega_{i}\left(\xi(r)\right)\right]\right\} \delta\left[\xi(r)-\xi\right] d^{N}{r}}{\int \exp \left\{-\beta\left[E(r)+\omega_{i}\left(\xi(r)\right)\right]\right\} d^{N}{r}} $$

因此我们可以用偏置势下的概率分布来表达平衡态的概率分布：

$$
\begin{aligned}
P_{i}^{\mathrm{u}}(\xi)=& P_{i}^{\mathrm{b}}(\xi) \exp \left[\beta \omega_{i}(\xi)\right] \\
& \times \frac{\int \exp \left\{-\beta\left[E(r)+\omega_{i}(\xi(r))\right]\right\} d^{N}{r}}{\int \exp [-\beta E(r)] d^{N}{r}} \\
=& P_{i}^{\mathrm{b}}(\xi) \exp \left[\beta \omega_{i}(\xi)\right] \\
& \times \frac{\int \exp [-\beta E(r)] \exp \left\{-\beta \omega_{i}[\xi({r})]\right\} d^{N}{r}}{\int \exp [-\beta E(r)] d^{N}{r}} \\
=& P_{i}^{\mathrm{b}}(\xi) \exp \left[\beta \omega_{i}(\xi)\right]\left\langle\exp \left[-\beta \omega_{i}(\xi)\right]\right\rangle
\end{aligned}
$$

注意这里的期望值是在体系的平衡系综下的平均，这样一来体系真正的平衡自由能为：

$$
F_i (\xi) = - \frac{1}{\beta} P_{i}^{\mathrm{u}}(\xi) = -(1 / \beta) \ln P_{i}^{\mathrm{b}}(\xi)-\omega_{i}(\xi)+Q_{i}
$$

其中$Q_i = -(1 / \beta) \ln \left\langle\exp \left[-\beta \omega_{i}(\xi)\right]\right\rangle$. 这里我们注意到真正的平衡自由能有三项，其中第一项$-(1 / \beta) \ln P_{i}^{\mathrm{b}}(\xi)$可以直接从采样中得到，第二项$\omega_{i}(\xi)$是我们已知的偏置势函数的形式，只有第三项$Q_i$是不知道的, 从定义中我们可以看出$Q_i$实际上是取决于平衡态分布或者说平衡自由能本身的，因此通常这样的一个等式我们可以通过自洽迭代的方式计算得到。

注意到，以上的讨论中我们只考虑了一个偏置势窗口下的自由能计算，也就是说我们只得到了只有窗口$i$采样下的自由能$F_i (\xi)$, 我们可以想象到，如果只有一个窗口内的采样，那么采样的构型只会集中在窗口$i$的中心附近，窗口之外的构型采样到的概率会很低，因此自由能的估计值的方差就会非常大。因此，我们在真正使用伞形采样的时候，几乎总是会在集合变量上划分很多bins，用多个采样窗口来进行采样，来得到集合变量在一个整体区间内的自由能的估计值。

还记得在BAR/MBAR方法中，当我们有个在多个状态的采样点之后，我们通过选取合适的参数让自由能的估计值的方差最小嘛？在伞形采样中我们遇到的情形是一样的，我们在计算自由能的时候真正的问题是：有了多个窗口的采样点之后，我们如何利用这些采样点，来让自由能的估计值的方差达到最小？Weighted Histogram Analysis Method (WHAM)方法的目的就是达到这一点。

我们首先把从一个窗口$i$中由于采样得到的无偏概率分布的估计设为 $P_i^{\mathrm{u}}(\xi)$, 并且假设整个集合变量区间的无偏概率分布$P^{\mathrm{u}}(\xi)$是每个窗口得到概率分布的一个线性组合：

$$
P^{\mathrm{u}}(\xi)=\sum_i^{\text {windows }} p_i(\xi) P_i^{\mathrm{u}}(\xi)
$$

这样的一个假设是比较合理的，它满足了在每一个窗口内，不同采样构型的概率比值是保持近似不变的。为了让整个区间的概率分布满足归一化条件，我们还需要满足：

$$
\sum p_i = 1
$$

在这样的一个假设前提下，WHAM方法的目标是让由这个公式得到的无偏概率分布$P^{\mathrm{u}}(\xi)$的方差最小，更确切地说，我们要选取$p_i$，使得其满足：

$$
\frac{\partial \sigma^2\left(P^{\mathrm{u}}\right)}{\partial p_i}=0
$$

经过一些繁琐的计算 (详细的推导可见[Shankar 1992](https://quantum.ch.ntu.edu.tw/ycclab/wp-content/uploads/2015/02/WHAM_1992.pdf))，我们发现系数$p_i$要满足如下的关系：

$$
p_i=\frac{a_i}{\sum_j a_j}, a_i(\xi)=N_i \exp \left[-\beta \omega_i(\xi)+\beta F_i\right]
$$

其中$N_i$是在窗口$i$中的采样点数量，而$F_i$的表达式为：

$$
\exp \left(-\beta F_i\right)=\int P^{\mathrm{u}}(\xi) \exp \left[-\beta w_i(\xi)\right] d \xi
$$

注意到这里$F_i$的表达式取决于全局的概率分布$P^{\mathrm{u}}(\xi)$，与此前单一窗口的采样情形一样，这里我们仍然需要一个自洽迭代的过程来最终得到我们自由能的估计。

## 非平衡态自由能计算方法


