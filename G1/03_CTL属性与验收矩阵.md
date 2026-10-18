# CTL 属性与验收矩阵

## 1. 术语约定

课程分工表使用“CTL 属性”这一称呼。技术报告中建议说明：UPPAAL 经典验证器使用的是适合时间自动机的符号查询语言，支持 `E<>`、`A[]`、`E[]`、`A<>` 和 leads-to (`-->`) 等受限形式，而不是允许任意嵌套的完整 CTL。

常用形式：

| 形式 | 含义 | 常见用途 |
| --- | --- | --- |
| `E<> p` | 存在一条路径最终到达满足 `p` 的状态 | 可达性、见证轨迹 |
| `A[] p` | 所有路径的所有可达状态都满足 `p` | 安全不变量 |
| `E[] p` | 存在一条路径始终保持 `p` | 存在性保持 |
| `A<> p` | 所有路径最终都到达满足 `p` 的状态 | 必然终止/进展 |
| `p --> q` | 每次出现 `p` 后最终都会出现 `q` | 响应/活性 |
| `A[] not deadlock` | 所有可达状态均不是死锁 | 全局死锁检查 |

不能因为 `E<> Done` 通过，就写成“车辆一定完成通行”。它只证明至少存在一条完成路径。若要表达等待后必然完成，应使用 `Waiting --> Done` 或相应的 `A<>` 性质，并检查模型是否允许无限拖延。

## 2. 时限属性表达

本项目不把 `within` 当成可以直接写入经典 UPPAAL 查询文件的通用关键字。对于“事件 A 后 T 时间内事件 B”这类有界响应，采用以下方法：

1. 增加观察者时钟或观察者模板，在 A 发生时复位时钟。
2. 观察者只读取同步事件/状态，不得阻止或新增被测系统行为。
3. 用错误位置表达超时，例如时钟超过 `T` 且 B 尚未发生时进入 `Observer.Timeout`。
4. 查询 `A[] not Observer.Timeout`，或查询系统状态中的等价时钟约束。

观察者属于验证插桩。应保留无观察者原模型，并说明插桩前后系统可见行为为何不变。

## 3. 统一属性矩阵

状态中的实例名以当前 G5 模型为基准：`Controller` 和 `VehicleProcess`。其他模型若命名不同，应建立名称映射，不得改变性质语义。

| 查询 ID | 需求 | 类别 | 建议查询/构造 | 版本 | 验收角色 |
| --- | --- | --- | --- | --- | --- |
| Q-S01 | SR-04 | 安全 | `A[] not deadlock` | v1-v3 | 必须通过；v3 若设计永久故障，故障位置也应允许时间/行为继续或明确例外 |
| Q-S02 | SR-01 | 安全 | `A[] (VehicleProcess.Crossing imply signal == GREEN)` | v1-v3 | 必须通过 |
| Q-S03 | SR-02 | 安全 | 控制器位置互斥通常由单模板位置语义保证；检查灯色变量与位置一致 | v1-v3 | 必须通过或给出等价查询 |
| Q-S04 | SR-03 | 安全 | 多车时：`A[] not (V1.Crossing && V2.Crossing)` | 可选 v2/v3 | 仅多车模型适用 |
| Q-R01 | RR-01 | 可达 | `E<> VehicleProcess.Done` | v1-v3 | 必须通过，并保存见证 |
| Q-R02 | FR-01 | 可达 | `E<> Controller.Red`、`E<> Controller.Yellow` | v1-v3 | 每个灯相位应可达 |
| Q-L01 | LR-01 | 活性 | `VehicleProcess.Waiting --> VehicleProcess.Done` | v2 | 目标性质；失败时保存反例并讨论无限拖延 |
| Q-L02 | FR-01 | 活性 | `Controller.Red --> Controller.Green` | v1-v2 | 正常场景应通过 |
| Q-T01 | TR-02 | 时限 | `A[] (VehicleProcess.Crossing imply crossingClock <= CROSSING_MAX)` | v1-v3 | 应由位置不变量保证 |
| Q-T02 | TR-01 | 时限 | 观察者超时位置；`A[] not WaitObserver.Timeout` | v2-v3 | `WAIT_BOUND` 冻结后执行 |
| Q-F01 | FRQ-01 | 故障可达 | `E<> FaultMonitor.Timeout` 或等价位置 | v3 | 必须存在故障见证 |
| Q-F02 | FRQ-02 | 恢复可达 | `E<> (FaultMonitor.Timeout && ...)` 后的观察者恢复位置 | v3 | 仅可恢复策略适用 |
| Q-F03 | FRQ-02 | 故障活性 | `FaultMonitor.Timeout --> Controller.Green` 或恢复位置 | v3 | 只有声称“必然恢复”时才是必选 |

## 4. v1 当前基线

G5 已在 UPPAAL 5.0.0 中保存以下实际结果：

| 查询 | 当前结果 | 证据 |
| --- | --- | --- |
| `A[] not deadlock` | SAT | `G5/UPPAAL_验证结果.txt` |
| `A[] (VehicleProcess.Crossing imply signal == GREEN)` | SAT | `G5/UPPAAL_验证结果.txt` |
| `E<> VehicleProcess.Done` | SAT | 同文件含最短见证轨迹 |

这些结果只覆盖 Q-S01、Q-S02 和 Q-R01。Q-L01、Q-T02 以及故障属性尚不能标记为完成。

## 5. 查询执行记录要求

每条查询至少记录：

- 查询 ID、完整公式和自然语言含义。
- 模型文件名、Git 提交号和模型版本。
- UPPAAL/verifyta 版本、命令行参数和运行日期。
- 结果 `SAT`、`UNSAT` 或 `ERROR`；不能只写“成功/失败”。
- 若 `UNSAT`，保存反例/诊断轨迹；若为存在性查询且 `SAT`，保存见证轨迹。
- 查询是否使用观察者、名称适配或其他验证插桩。
- 结果对应的需求结论，避免把存在性误写为必然性。

## 6. 反例分析流程

1. 固定失败模型、查询和工具版本，避免边改边解释。
2. 找出最早违反性质的状态或导致超时的循环。
3. 将轨迹映射到需求 ID、模板、源/目标位置和具体边。
4. 判断根因属于需求、模型、查询还是观察者错误。
5. 在模型评审记录中提出最小修复，不直接覆盖失败版本。
6. 修复后先复跑失败查询，再跑完整回归集合。
7. 同时保存“修复前失败”和“修复后通过”证据。

## 7. 审查重点

- `A[] not deadlock` 通过不代表业务活性自动成立。
- 位置不变量可能迫使系统离开位置，也可能在没有可执行出口时制造死锁。
- 普通可执行边不保证一定被选择；活性失败可能来自无限拖延或非公平调度。
- 观察者不能通过 urgent/committed/synchronization 意外限制原系统行为。
- v3 若允许永久故障，就不能同时无条件声称所有路径最终恢复。

## 8. 参考依据

- UPPAAL Symbolic Queries: <https://docs.uppaal.org/language-reference/query-syntax/symbolic_queries/>
- UPPAAL Query Syntax Overview: <https://docs.uppaal.org/language-reference/query-syntax/>
- UPPAAL Expressions and Clock Constraints: <https://docs.uppaal.org/language-reference/expressions/>
