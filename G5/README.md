# G5：基础交通灯模型 v1

本目录保存 G5 独立重建的基础 UPPAAL 模型、查询和验证记录。

## 内容

- [`traffic_light_v1.xml`](traffic_light_v1.xml)：信号灯控制器与车辆进程。
- [`queries.q`](queries.q)：无死锁、安全性和可达性查询。
- [`UPPAAL_验证结果.txt`](UPPAAL_验证结果.txt)：Verifier 运行输出及见证轨迹。
- [`G5_模型说明与验证记录.md`](G5_模型说明与验证记录.md)：模型边界、时钟/不变量设计和贡献说明。

## 运行

在安装 UPPAAL 5.0.0 的环境中，从本目录执行：

```bash
verifyta -t 1 -y traffic_light_v1.xml queries.q
```

三条查询均已通过：`A[] not deadlock`、`A[] (VehicleProcess.Crossing imply signal == GREEN)`、`E<> VehicleProcess.Done`。

本版没有收到 G2 的 AI 原始模型，所以这是按 G5 分工独立重建的基础模型，不是针对特定 AI 初稿的修复版。Verifier 见证轨迹不等同于 GUI Simulator 录屏；本目录没有 GUI 录屏文件。许可证密钥不在仓库中。
