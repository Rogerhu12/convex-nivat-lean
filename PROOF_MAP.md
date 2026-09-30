# 证明对应与实现选择

## 当前完整证明链（2026-09-30）

当前 `TheoremB.periodic_of_low_convex_complexity` 的类型直接断言：对有限字母表上的二维配置，若非空有限窗口 `S` 恰含其凸包内全部格点，且**实际出现**的 `S`-模式数不超过 `S.card`，则存在非零的全局周期。签名不再量化 `ExternalInputs.Results` 或其他外部数学结论。最终 219 模块、27,091 净行导入闭包的完整审计已经成功：`audit-theorem-b-unconditional.json` 为 `success: true`，221 项检查通过，3,777 声明／3,176 theorem 仅标准三公理，源码哈希及闭包稳定；完整终端类型也已经检查。耗时 2,263.41 秒。此前的 202 模块检查点另作历史记录保留。

主证明的调用顺序如下：

| 环节 | 当前正式连接 |
|---|---|
| 低复杂度到整数分解 | `KariSzabados` 与 `ExternalInputs.low_complexity_integer_decomposition` 从真实模式数构造整数值、两两不平行周期分量；`ExternalInputs.Results` 的旧外部字段已从当前定理入口删除。 |
| 相反非膨胀方向与参考点 | `ColleOppositeDirections` 给出相反的真实单侧非膨胀方向；`ColleRegionalEntry` 经整数坐标变换、周期界面与真分解方向匹配，选出真实周期参考点及区域二分。 |
| Case 2：缺陷半条带 | `ColleCaseTwoConclusion` 从实际缺陷窗口与长边最大一致区域，经第二边界、半歧义及参考半平面周期，得到**非周期语言闭包点**在非空凸区域上的两个独立向前周期。 |
| Case 1：周期楔形 | `ColleCaseOneNormalizedReference` 保留同一个非周期闭包点 `x`，把参考周期和它的真实整数分解方向对齐。`ColleCaseOneWedgeSeed`、`ColleCaseOneSeedRegion` 在 `x=p` 的实际楔形内放置有限长边种子，构造两个方向的任意有限射线窗口。`ColleDirectedAgreement` 用共同种子与已证差分消去关系合并窗口；`ColleFixedAgreementRegion` 的并形成对**同一 `x,p`** 的闭长边区域，并证明有限扩张最大性。`ColleCaseOneProperRegion` 从 `x` 非周期和 `p` 的全局周期证明半平面内有真实缺陷；`ColleFirstBoundaryMinimum` 取底部边界，`ColleCaseOneReflectionTransport` 反射后复用 Case 2 的第二边界机制，得到 `x` 的一个固定平移（仍为非周期闭包点）的非空凸双周期区域。 |
| 区域到全局周期 | `ColleRegionalConclusion` 合并两支并把整数坐标变换映回；`RegionalReduction` 从真实非空凸区域的两个独立向前周期，经双侧周期尾部和 `StarNormalization` 调用 `TheoremA` 的严格复杂度下界，排除非周期情形；`ModularReduction` 将整数分量映到有限加法群，最后由单射字母表编码还原原配置。 |

Case 1 的最终实现**没有**把 Colle 原文 Claim 4.7 的逐角度扇区扩张照字面形式化。早期 `ColleCaseOneAngular*` 模块只给角度与局部边界辅助，粗楔形存在角点缺陷，不能单凭它们宣称原 Claim 4.7 完成。最终路线固定原非周期 `x`，把共享长边种子的有限一致窗口通过真实消去关系组成有向族，取其并，再通过反射调用已经证明的 Case 2 第二边界定理。构造最大区域时始终比较同一个实际 `x,p`；末步只作一个保留非周期性的整数平移，不取可能丢失非周期性的移动极限。

**历史快照说明：**以下从“原始对象”开始的章节记录 §§0–7 及随后扩展时的阶段性路线。其日期、模块数、行数、`ExternalInputs.Results` 和“外部边界”叙述只反映当时状态；当前证明范围与验证状态以上述新节为准。

对象：`convex-nivat.pdf`（2026-09-12）中的 §§0–7。本文档记录正式项目怎样从原始假设连接到复杂度结论，方便核对定理语义。2026-09-29 的全量审计已经通过：41 个数学模块、聚合入口和公理审查共 43 项全部成功；该阶段历史记录见 `audit-theorem-a.json`；第 8 节与附录 D 的当前补充见后文。

## 原始对象

`Star.Data` 保存 (S1)–(S3)：有限多个两两不平行的本原方向；各分量有该方向的非零整数周期、不是双周期；条带两侧分别等于双周期尾部。最终使用 `Nontrivial ι` 表达至少两个分量。`Star.Data.total` 是分量之和。

值域允许任意有限交换加法群，因而包括原文的有限域。模式复杂度是实际平移模式集合的基数。`LatticePolygon.IsLatticeConvex S` 表达格点嵌入的凸包与格点交集恰为 `S`。

## 依赖链

| 原文步骤 | 正式模块 | 连接内容 |
|---|---|---|
| §0 规范化周期 | `Star`、`Periodicity` | 从双周期尾部导出共同倍数，未把公共周期另作假设 |
| §1 局部差分、第一种情形 | `Strips`、`Algebra`、`FirstCase`、`Dichotomy` | 任意有限局部观测量的差分有有限支撑；非零时推出复杂度下界 |
| §2 隔离、频谱、编码、整除 | `Isolation`、`Spectral`、`Divisibility`、`GlobalSpectrum` | 从原始数据构造实际频谱和单射整数编码，并证明每个仿射关系均被频谱多项式整除 |
| §2 商的支撑、仿射维数 | `ConvexSupport`、`SpectralGeometry`、`AffineBudget` | 商的支撑位于真实的侵蚀窗口 `R_Z(S)`，再做核与像的维数计数 |
| §3 周期背景 | `SectorBackground`、`Background` | 有限例外之外的共同周期，利用有限支撑非消去将其提升为处处成立 |
| §4 非零见证 | `HalfPlane`、`Components`、`Witness` | 独立条带内的非零余因子场给出非零二点差分 |
| §5.1 双递推 | `BiRecursion`、`StarRecurrence` | 使用实际构造的多项式、编码与已证明的公共背景周期 |
| §5.2 商空间生成 | `CoefficientField`、`QuotientFactors`、`QuotientIdeals` 及后续商空间模块 | 在 Laurent 分式域上处理两关系商空间，显式证明所需互素和支撑界 |
| §5.3 见证限制 | `WitnessTransform`、`Confinement` | 有限支撑 Laurent 变换，系数域上的线性泛函及其消去关系理想的性质 |
| §6 格点差分解 | `Zonotope` | 差体中的格点可写为 zonotope 内两个格点之差 |
| §7 窗口、二次观测与相消 | `LatticePolygon`、`Quadratic`、`StarWindow` | 实际位置选择，平移见证的线性无关性，最终维数相消 |

## 与纸面路线的差异

1. **频谱只用两个方向的右侧缺陷。** 对每个方向取 `Xi_i^+ − G_i^{+,R}`、`Xi_i^- − G_i^{-,R}` 的颜色频谱并集。右侧缺陷已足以保证频谱非空、整除关系，以及 §3 所需消去性质。左尾部仍用于 §4 的条带支撑证明。这里使用的 zonotope 可能比原文定义的小。

2. **支撑下界直接针对二项式证明。** 在每条平行于因子方向的格点线上选取商的首末非零项，得到乘积支撑中的两个端点。利用凸性和凸集侵蚀逐因子归纳，推出商支撑加上整个 zonotope 位于窗口凸包。无需调用一般的 Newton 多面体乘法公式。

3. **周期背景直接证明有限周期缺陷。** 固定一个公共周期，扩大观测窗口以同时覆盖平移前后的值。在活动条带内，纵向坐标足够远时，观测窗口匹配相应的隔离构型；剩余点落在显式有限格点盒的有限并中。由此导出每个周期的有限缺陷，再用非零 Laurent 差分算子消去该缺陷。无需给所有扇区排序或证明扇区粘合。

4. **商环互素通过最大理想商域证明。** 因子已经在复数上分裂；若相应理想非全环，取最大理想商域，并用整数行列式关系推出一个非恒定 Laurent 单项式等于复常数，得到矛盾。所需结论是两个关系与各方向投影因子生成单位理想，不必构造两层 CRT 同构。

5. **zonotope 格点分解不需要三角剖分。** 写差体内格点为 `d = Σ s_i g_i`，其中 `s_i ∈ [-1,1]`、`g_i` 为整数生成向量。按 `s_i` 的正负选 `ε_i ∈ {0,1}`，令 `p = Σ ε_i g_i`。则 `p` 与 `p-d` 都是格点，且它们的系数分别在 `[0,1]` 内。这一论证不依赖维数、非退化性或本原性。

这些调整给出 Theorem A 所需结论。以下记录第 8 节和外部定理的阶段性实现。


## 附录 D 与第 8 节的完整内部链（2026-09-30）

当前完整工程为 65 个数学模块、10,923 净行；最终验证状态见 `audit-report.json`。Theorem A 的历史审计已另存 `audit-theorem-a.json`。

| 原文步骤 | 正式模块 | 已完成的实际连接 |
|---|---|---|
| D.3 一维 Morse–Hedlund 与有限状态 | `MorseHedlund` | 实际行词的延拓、周期性与模式数 |
| D.5 平衡凸窗口选择 | `BalancedWindows`、`BalancedTransforms` | 从原始低复杂度凸窗口选择上下两种平衡窗口之一；证明真实行长度与坐标变换性质 |
| D.7 歧义传播 | `AmbiguityPropagation`、`RowDetermination`、`BalancedPropagation` | 基于实际模式限制映射、歧义计数和逐行传播，把足够宽条带一致提升为半平面一致 |
| D.1 两分量定理 | `HorizontalCoordinates`、`TwoComponent`、`LatticeCoordinates` | 真正的整数可逆坐标变换、反射、有限块抽屉原理和周期矛盾；顶层仅保留独立周期与低凸复杂度 |
| 8.3 最小阶反例、8.5 闭包转移 | `ExternalInputs`、`IncrementSupport` | 最小化实际整数分解项数，证明差分消去关系传入语言闭包，并内部推出等阶性质 |
| 8.5 有限值域约化 | `ModularReduction` | 整数分量逐点模 `M+1`，原始颜色 `1,…,M` 保持单射、总和、周期及复杂度 |
| 8.2 周期区域扩张 | `RegionGeometry`、`Periodicity` | 从真实非空凸区域和两独立向前周期证明共同进入性，并构造全平面双周期扩张 |
| 8.8 半平面差分消去 | `OneSidedRecurrence` | 有限群差分积分与列表归纳，得到实际周期尾部；同时证明差分乘积与逐项差分的一致 |
| 8.9 第一侧周期尾部 | `IncrementSupport`、`FirstHalfPlane` | 余因子隔离分量、在真实侵蚀区域消失、基本域饱和、排除与共同进入方向平行，进而构造双周期尾场 |
| 8.13 差分双周期性 | `PeriodicDifference` | 从周期差分积分出额外周期，以及两分量周期和的代数后果 |
| 8.14 两分量极限 | `TwoComponentLimits` | 实际平移收敛、有限模式复杂度传递、吸收双周期背景，调用项目内完整 D.1 |
| 8.15 可用方向 | `AvailableDirections` | 共同严格正向条件下的有理斜率排序，真实选出隔离两分量的可用平移方向 |
| 8.16 从极限周期性到尾部一致 | `PeriodicSubshift`、`HalfPlaneLimit` | 证明紧全周期一维子移位有限；实际二维有限基本域编码与有限块重叠，推出整侧尾部一致 |
| 8.12 第二侧尾部 | `SecondHalfPlane` | 对尚未知第二侧尾部的有限指标集归纳，内部选择方向、构造安全极限、调用 8.14/8.16，得到每个分量的反侧尾部 |
| 8.17 星形配置提取 | `ReducedDecomposition`、`StarNormalization` | 吸收所有双周期分量并保持总和，至少剩两个非双周期分量；实际 gcd 本原化，调整尾部阈值，构造 `Star.Data` |
| 8.18 最终拼装 | `RegionalReduction`、`TheoremB` | 区域输入→双侧尾部→星形配置→Theorem A 矛盾；再接上显式外部输入和单射字母表编码 |

## 新增部分的路线调整

- D.5 的行基数界用凸端点插值及取整直接证明，未建立一般实凸体的截线长度凹性理论。
- 8.8 给出最终归约需要的存在式半平面阈值，没有声称证明原文特定的最优或显式 `c+β_-` 阈值公式。
- 8.9 使用两个实际区域周期之和作共同进入方向，再用整数基本域证明饱和后的半平面包含关系；没有重建所有衰退锥辅助命题。
- 8.15 在已有共同正向条件下用有理斜率和有限排序完成所需符号结论。
- 8.16 的紧全周期子移位有限性在项目内证明，没有作为额外结构性输入。
- 8.17 提前吸收双周期背景，使用已对齐的双侧尾部，从任意非零周期向量实际取出正整数倍和本原向量。
- 所有内部周期与代数步骤适用于有限加法交换群，因此最后选择 `ZMod (M+1)`；不必寻找素数，也不需要有限域乘法结构。

这些变化给出最终定理所需结论。依赖是单向的：D.1 不依赖 Theorem A 或第 8 节尾部构造；第二侧尾部依赖 D.1；最终区域归约再调用 Theorem A。

## 外部边界

`ExternalInputs.Results` 有两个字段：

- `KariSzabados`：本文 8.4 的整数周期分解后果（含固定差分乘积方向的分解）。
- `CollePeriodicRegion`：本文 8.6–8.7 合并区域推论，前提含闭包中非周期配置的同阶性。ONED、被引用的区域提取证明，以及从重叠周期到向前区域周期的解释仍属于外部包装。

`UniformOrder` 本身由项目内的最小反例选择证明，不是额外接受的未知原则。最终 Theorem B 的类型仍明确量化 `external : Results`。对这条条件定理的公理检查不构造 `Results`，不能据此宣称外部引用已经形式化。
# 外部引用更新（2026-09-30）

最新范围优先于以下历史阶段记录。Kari–Szabados 已完全内部证明：`IntegerAnnihilator` → `AnnihilatorDilation` → `LaurentVandermonde` → `BinomialDirections` → `ParallelCollapse` → `IntegerDecomposition` → `KariSzabados`。此链的无遗漏导入闭包随 TheoremB 通过 `audit-kari-checkpoint.json` 的 78 项审计。整数分量仍允许无界，未加入有限分量前提。

`NonexpansiveGeometry`/`NonexpansiveExistence` 内部证明所需 Boyle–Lind 二维后果；`MinimalHull`、`FiniteDetermination`、`RealHalfPlaneRecurrence`、`PeriodicBandCoding`、`FiniteIncrementFibers`、`SeparatedFiberLimits`、`MaximalIncrementFibers`、`JointFiberLimits`、`DirectionalElimination` 和 `KariMoutot` 给出实际方向对称化。`PeriodicNonexpansive`、`PeriodicInterface`、`ColleRegions` 与 `ColleOppositeDirections` 随后证明本文 8.6。上述新增结论已逐文件编译；8.6 已被主定理调用，更新后的完整闭包审计尚未完成。

目前唯一未构造的输入是 `ExternalInputs.CollePeriodicRegion`，现专指 8.7；它接收由 8.6 实际产生的相反 ONED 方向。`ColleGenerating`、`ColleBalancedRows`、`ColleBoundaryPropagation`、`ColleEnvelopeGeometry`、`ColleMaximalEnvelope`、`ColleFiniteEnvelope`、`ColleOrbitCofactor`、`ColleMinimality` 等是在推进这项输入，不能把它们的条件子结论宣称成完整区域存在性。

---
