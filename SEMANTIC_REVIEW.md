# 最新终端复核（2026-09-30）

最终 `TheoremB.periodic_of_low_convex_complexity` 已去掉外部参数并单编通过。`ExternalInputs.Results` 和 `CollePeriodicRegion` 已删除。当前前提仅是任意有限字母表上的实际配置、非空有限格点凸窗口、实际平移模式数不超过窗口大小；结论为存在非零全局整数周期。

最新区域结论由 `ColleRegionalConclusion.regional_configuration_of_low_complexity` 提供。它内部构造整数方向的真实区域二分，并合并 Case 1 与 Case 2，再还原原坐标。最终 Theorem B 从实际整数分解出发，在非周期区域 hull 点上继承分解，以模单射编码接入 `RegionalReduction`。没有把均匀最小阶、相反非膨胀方向、参考周期或最大一致区域作为终端输入。

Case 1 使用同一非周期配置与参考配置的有限长边窗口有向族。实际乘积差分编码保证两个有共同长边窗口的候选区域可以合并；有限方向见证保证并集仍是包络。有限扩张最大性由相同合并证明得到。非周期性与半平面周期刚性保证区域不是整个半平面，整数支撑最小值给出实际边界点。平移和反射后接入已证第二边界论证，最后仍得到原配置的一个平移，非周期性没有在紧性过程中丢失。

`PeriodicOn` 包含区域向前不变性及其上的实际值等式；区域非空另行证明，两个周期的行列式非零。区域进入性定理从这些性质和凸性推出覆盖，不另需未证的满维或无限区域假设。第二周期截取区域的非空性来自实际高度无界。

具体交叉核对见 `CASE_ONE_DIRECTED_REVIEW.md` 与 `CASE_ONE_REFLECTION_REVIEW.md`。这些仍是同一实现任务内部的源码审查，不能称为第三方独立认证。所实现的 Colle 推论是下游证明使用的凸区域双独立周期，不包含原文更强的两条无界边均为 ONED 的边界分类。

验证状态：219 模块、27,091 净行的最终闭包审计已经成功，`audit-theorem-b-unconditional.json` 为 `success: true`。221 项检查全部通过；3,777 个声明（其中 3,176 个 theorem）仅依赖标准三公理，源码哈希及闭包稳定，耗时 2,263.41 秒。`logs/FinalTheoremB/FinalTheoremBAxioms.log` 打印的实际终端类型只含有限字母表、实际配置、非空凸窗口和低模式数前提；结论是 `IsPeriodic θ`，没有外部记录或剩余数学接口。该结果与上述源码语义核对共同构成当前交付证据，但仍不称为第三方独立认证。

以下保留历史阶段审查。“外部引用仍未形式化”“当前65模块”等旧表述仅属于其所在历史阶段，不能替代上述最新状态。

---
# 源码对应审查：历史记录与本轮补充

Theorem A 阶段日期：2026-09-29。该阶段报告保存在 `audit-theorem-a.json`；以下先保留历史审查，当前第 8 节与附录 D 的补充见后文。

审查者：本轮实现代理 `/root/trial_patterns`（GPT-6-sol / xhigh）。

本文记录同一协作任务内的只读源码对应审查。审查者参与实现了 Patterns、Dynamics、Periodicity、MorseHedlund、Zonotope、LatticePolygon、SectorBackground、WitnessTransform 和 Confinement，因此这**不是第三方独立验证**。源码对应审查也不等同于论文整体正确性认证。

## 结论与验证状态

本轮审查未发现 Theorem A 顶层隐藏前提、对象替换或具体量词漏洞。`NivatTrial.TheoremA.complexity_lower_bound` 的输入为至少两个分量的原始 `Star.Data`（另有 `[Nontrivial ι]`）和有限窗口 `S` 的 `IsLatticeConvex`，结论为实际模式复杂度 `S.card + 1 ≤ patternComplexity T.total S`。谱整除、支撑预算、背景周期性、商空间张成、见证约束与窗口放置均由下层证明供给，没有作为最终用户输入保留。

主代理已报告 `TheoremA.lean` 与 `QuotientSpanning.lean` 最终构建均为 `exit 0`；审查者本人编译的五个新增模块均为 `exit 0`。这些信息与下面的源码语义结论分开记录。

**全量审计结果（由主代理填入）：**

- 41 个数学模块、聚合入口及公理审查共 43 项重新构建，全部返回码为 0；历史报告 `audit-theorem-a.json` 的 `success` 为 `true`。
- 共检查 1,482 个项目声明，其中 1,217 个 theorem 声明（含自动生成声明）。所有传递公理依赖限于 `propext`、`Classical.choice`、`Quot.sound`；最终定理单独检查得到同样的三项依赖。
- 源码扫描未发现 `sorry`、`admit`、自定义 `axiom` 或 `native_decide`；审计前后的数学源文件 SHA-256 一致。
- 命令为 `python audit.py`；该阶段完整报告保存在 `audit-theorem-a.json`。日志当时写入 `logs/verified/`，最终类型与公理输出写入 `logs/verified/AxiomAudit.log`；这些日志路径会被本轮审计覆盖，不能再作为永久历史日志。2026-09-29 15:09:49 UTC 开始，整轮耗时 822.04 秒。

数学源码在本轮审查期间冻结；本文未改写任何数学证明。

全量审计完成后，另一实现代理 `/root/trial_algebra`（GPT-6-sol / xhigh）另行只读核对了 `Star.Data`、周期定义、实际模式集合、格点凸性和最终定理，与论文 §0.1–0.2 对应；未发现额外加强假设、隐藏结论前提或因计数定义造成空泛结论的具体疑点。这仍属于同一协作任务内的交叉检查。

## 检查覆盖

1. **原始输入与实际模式集合。** 对照论文第 4 页 §0.1，`Star.Data` 给出原始 S1–S3、primitive 方向、两两非平行及非双周期分量；有限 `Nontrivial ι` 对应至少两个分量。`commonMultiplier` 的公共周期由尾场双周期性证明。有限加法交换群值域包含原文有限域情形。`patternSet` 是全部格点平移下实际出现的窗口函数的 range，`patternComplexity` 是其实际基数。`IsLatticeConvex` 使用嵌入实平面的凸包，正是 `S = Conv(S) ∩ ℤ²`。
2. **第一分支与非零见证。** `Strips` 从实际条带相交有限性证明每个有限窗口观察的有限差分支撑；`FirstCase` 从实际低模式数导出非平凡仿射关系。`Components` 用真实局部极限及一侧消去证明 cofactor 场非零且有条带支撑；`Witness` 从两个非平行条带场推出非零二点见证，并证明每个位移的见证有限支撑。没有要求随位移统一的支撑界。
3. **谱、编码与仿射预算。** `GlobalSpectrum` 构造实际出现的频率、非空方向谱和保谱的注入整数编码，证明常值仿射关系的真实整除。`ConvexSupport` 沿整格直线使用支撑最小和最大指数，证明实际乘积支撑中的端点不能消去；迭代后 `SpectralGeometry` 将商因子的支撑约束到实际 `placementFinset`，并供给 `AffineBudget` 的 bounded factorization。
4. **背景周期与双递推。** `SectorBackground` 实际构造有限例外集合，对远处的窗口使用同一个 isolated 场或 pure-tail 场；有限缺陷消去随后给出各个公共周期。`GlobalSpectrum` 证明两个符号的 isolated−pureRight 消去，`StarRecurrence` 据此给出实际背景周期和 `BiRecursion.bi_recursion`，没有留下 sector 连通或有限缺陷假设。
5. **商空间张成与约束。** 检查了 `QuotientFactors`、`QuotientIdeals`、`QuotientLinear`、`QuotientSupport`、`SupportGeometry`、`QuotientSpanning` 以及 `QuotientRelations` 的接口和使用。商环是 Laurent 分式域上的实际两关系理想之商，指数区间是实际 `Z−Z`。`WitnessTransform` 的移位符号与正向 Laurent action 一致，且证明功能泛函消去整个生成理想。`Confinement` 通过实际投影的核和张成推出约束见证，没有仅消去两个生成元便直接断言消去理想。
6. **整数点、窗口放置与最终维数。** `Zonotope` 证明真正的整数点差集恒等式；`LatticePolygon` 给出同一见证的两个实际整数点在每个 placement 中均落入 `S`。`Quadratic` 的二次观察定义于实际 `patternSet`，通过非零有限支撑场的不同平移证明模仿射空间的独立性。`AffineBudget` 的核维数注入和最终相消给出正确的 `+1`，没有把独立性或维数结论作为额外假设。

## 与论文的数学路线差异

- **两种频谱定义尚未建立字面等价。** 论文 §2.2 取 `σ ∈ {+,−}`、`ϵ ∈ {L,R}` 的四族颜色差场频谱并集；当前 `GlobalSpectrum.frequencies` 只取两个符号的 isolated−pureRight 差场频谱并集。当前证明对该实际谱证明了非空、保谱编码、整除、两个符号的消去、真实支撑预算和见证约束，足以推出 Theorem A。但源码没有额外证明这个辅助谱定义等于论文的四族谱，不能把它描述为逐定义原样翻译。
- 公共方向周期选择满足分量及全部尾场周期性的任意正共倍数，没有实现论文书写的最小可取倍数。当前论证不使用最小性；论文 Remark 1.4 也允许这样的周期选择。
- §3 用实际有限缺陷论证代替全局扇区排序；§5.2 用实际最大理想商域排除公共零点和 projector 张成论证，代替原文的 Nullstellensatz/CRT 组织方式。
- §6 对 signed zonotope 系数逐项选整数端点，从而直接构造两个整数点，代替一般格点多边形的 unimodular triangulation。此证明不把三角剖分或整数分解性质作为假设。

这些差异是证明路线差异，未发现它们导致当前最终结论缺失所需前提。全文逐 lemma 覆盖则不能由本次审查声称。

## 范围边界

上述历史审查以 §§0–7 的 Theorem A 链为目标，当时尚未完成 §8/Theorem B 归约。当前内部归约已经完成，外部引用仍未形式化；详见下节。

现有 Dynamics、Periodicity 和 MorseHedlund 包含可复用的轨道闭包、模式计数、有限状态、共同周期及一维 Morse–Hedlund 证明。当时尚缺的 balanced-set 几何、D.7 歧义传播和 D.1 两分量拼装已在本轮实现，以下单列其审查范围。


## 第 8 节与附录 D 的补充审查（2026-09-30）

前文保留 Theorem A 阶段的审查记录。当前工作已补齐 D.1 和第 8 节内部归约。

本轮全量审计共 67 项全部通过（65 个数学模块、聚合入口、公理审查），`audit-report.json` 的 `success` 为 `true`，固定副本为 `audit-theorem-b-conditional.json`。覆盖 2,213 个项目声明，其中 1,780 个 theorem 声明（含自动生成声明）；全部传递公理仅为 `propext`、`Classical.choice`、`Quot.sound`。四个终端定理单独打印了类型与公理；Theorem B 的外部记录参数仍清晰出现在类型中。源码扫描无 `sorry`、`admit`、自定义 `axiom` 或 `native_decide`；审计前后模块集合与源码哈希一致。审计于 2026-09-29 16:20:58 UTC 开始（本地 2026-09-30），耗时 1,041.67 秒。

两位参与实现的 GPT-6-sol / xhigh 子代理分别做了只读交叉审查，主代理检查了最终集成与实际类型。它们仍属于同一协作任务，不是第三方独立验证。

### 检查结果

未发现内部循环、把后续半平面或星形提取结论放进外部输入、或者将实际模式数替换为抽象预算的具体问题。重点检查了：

1. `RegionGeometry` 从非空凸区域及两个独立向前平移，实际推出每点沿共同方向最终进入；有限基本域用于单周期场的半平面消失，不把区域进入性作为最终未证假设。省去区域闭性给出更一般的内部几何结论，仍覆盖原论文。
2. `FirstHalfPlane` 使用实际差分余因子、侵蚀窗口和有限群上的差分消去；与共同进入方向平行的情况会导致整个分量双周期，从而被实际非双周期假设排除。
3. `TwoComponent` 的顶层只接受独立周期、实际非空凸窗口与复杂度界。平衡集选择、D.7 歧义传播、坐标变换和有限状态步骤已经在下层证明，没有保留为输入。
4. `HalfPlaneLimit` 使用真实平移的聚点集合，证明其有限性，再从有限块重叠得到同一个极限配置的整个尾部一致；并非把“所有极限双周期”直接当作“原配置最终双周期”。
5. `SecondHalfPlane` 对未解决指标集做严格缩小归纳。可用方向选择、安全尾部极限以及 D.1 的应用均有下层证明。
6. `ReducedDecomposition` 实际吸收双周期背景、保留总和并证明至少两个分量。`StarNormalization` 实际 gcd 归一化而非要求周期向量预先本原。`RegionalReduction` 将这些对象送入已有 Theorem A。
7. `ExternalInputs.minimal_counterexample` 在固定字母表及窗口的反例中最小化分解项数，通过真实局部消去关系转移到语言闭包，得到 Colle 所需的 `UniformOrder`。这里的分解方向两两不平行；其与通常最小分解阶数的数学对应利用平行周期分量可以合并。
8. `TheoremB` 使用整数颜色 `1,…,M`，模 `M+1` 后仍单射。实际整数分量可以无界，只有模约化后才使用有限群论证。最终结论适用于任意有限字母表。

### 引用接口与来源边界

`KariSzabados` 对应本文 8.4 的分解后果。子代理对 [Kari–Szabados 预印本](https://arxiv.org/pdf/1605.05929) pp.10–12 的 Lemma 14/15 与 Theorem 13 证明作了局部抽查，报告固定因子分解及整数递推支持任意整数场、可能无界分量的量词。该抽查不构成整篇外部证明的验证。

`CollePeriodicRegion` 是本文 8.6–8.7 **合并后的区域推论输入**，包括原文从 overlap 周期转成向前区域周期的几何说明。子代理抽查了 [Colle 预印本](https://arxiv.org/pdf/1909.08195) 的 §4.1 与 Case 1–2，报告同阶前提、所需非周期极限和周期区域的来源相符，未见额外矩形窗口假设。已检预印本的编号与本文所列引用编号不同；未逐页核验发表版，不能把这一编号差异直接算作数学错误。ONED、完整区域提取论证和全部传递引用并未在 Lean 中证明。

因此，最终 `TheoremB.periodic_of_low_convex_complexity` 仍是以 `ExternalInputs.Results` 为前提的条件定理。来源抽查、源码语义审查、Lean 编译及公理检查是不同层次的证据。尤其是，`#print axioms` 只列标准三项不会消除定理参数中的外部结果。

新增部分使用的路线调整详见 `PROOF_MAP.md`。其中 8.8 只证明所需存在式阈值，没有声明精确阈值公式；整项工作不声称论文每个中间引理的逐字形式化。
# 最新外部边界审查（2026-09-30）

以下正文保留历史阶段审查。本次新增的 Kari–Szabados 证明已经消除原同名输入，`Results` 只剩 Colle 区域字段。`audit-kari-checkpoint.json` 对该阶段的 76 模块、12,043 净行完成 78 项检查，2,347 声明／1,899 theorem 的传递公理仅标准三项，源码哈希稳定。此结论只覆盖报告记录的源码快照。

此后新增的 `KariMoutot` 顶层直接量化实际有限值整数配置和非零 Laurent 消去子，未接受方向对称性或有限纤维结论作为参数。`ColleOppositeDirections.exists_opposite_nonexpansive_of_finite_range` 对同样的实际配置及消去子证明“非双周期 ⇒ 存在相反 ONED”。`OneSidedNonexpansive` 的定义量化实际 `languageHull` 中两个不同配置在真实闭半平面的一致性；没有预设方向有理或周期区域存在。

8.6 证明路线中，双周期极限的 proper 半平面界面只能先推出“非双周期”；随后产品消去子使其具有沿边界的单周期。这种界面本身不能充当 8.7 所需的“非周期配置”。当前实现保留这一区别，区域提取仍未完成。

8.6 已接入 TheoremB 源码，并成为剩余 Colle 输入的显式前提。新快照逐文件验证与整链审计分开记录；不能把旧 12,043 行审计扩大解释为覆盖后续所有文件。最终定理类型仍有 `external : Results`，所以还不是无外部数学前提的结果。

`ColleEnvelopeGeometry`/`ColleMaximalEnvelope` 的有限法向凸包络不是自动等同原文 E(U)-enveloped：原文还要求各边格点长度下界，当前基础几何不把这一要求藏进定义或省略后声称完成。`ColleMinimality` 的方向极限排除则使用真实更短整数分解给出矛盾，未借入未证的 KS Cor24。

---

## Case 2 定向语义审读（后续进度，2026-09-30）

GPT-6-sol / xhigh 子代理对 `ColleCaseTwoConclusion` 及新引用传播链进行了只读审读，root 检查实际编译与终端类型。未发现本次新增链的对象替换、阈值符号错误或前提逃逸。此结论限于该链，不是全仓库或第三方审计。

- 最终输出是 `aperiodic_region_of_defective_patches` 的同一个 `y, hy, hnot`。周期参考 `q` 只传递区域内颜色等式，没有替换实际非周期配置。
- 撤销 `shift a p` 使用 `z-a`，高行阈值为 `lo+a₂`；保向坐标公式 `det u (f z)=P*z₂` 将门槛变成 `P*lo`。
- 最终 `K=R∩{det u≥b}` 的非空性来自区域高度无界，凸性来自凸区域与半平面的交。`-u` 与 `M k` 都明确保持 K，行列式为 `-M det u k≠0`。
- Q 的四角及整个格点胞腔确实来自实际凸窗口。余数类覆盖、删边运行、共同尾周期和每条高水平行的连续种子均内部证明。上下两条边的长度次序通过两个实际传播朝向处理，未留为顶层假设。
- 顶层 `hpatch` 正是实际 `actual_regional_dichotomy` 的右分支；`hproper` 来自参考选择并以同一分解方向定向。`CaseTwoEndpointAudit.lean` 成功检查该现有编译闭包中 2,715 个声明、2,309 个 theorem，仅标准三公理，并打印实际顶层类型。此检查没有重新编译整个依赖闭包，不能代替运行中的固定快照审计。

Case 1 尚未完成。首个整数楔层坏点可能只是角点附近的有限缺陷，不能推出任意远的半歧义；初版角链的粗包含界也不能代替原文精确半群扩张区域。当前在修正精确角几何并证明生成窗与消去子的边界传播。即使局部带 margin 的传播引理编译成功，margin 尚未从实际区域推出时仍不是完整 Claim 4.7。
