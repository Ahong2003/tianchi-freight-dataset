# 司机找货 Agent 仿真数据集

天池「司机找货 Agent 连续决策仿真赛」本地 Demo 配套数据的独立整理仓库。将输入数据与决策代码分开保存，便于下载、校验与复现实验。

配套代码：[tianchi-freight-agents](https://github.com/Ahong2003/tianchi-freight-agents)。

## 数据概览

| 文件 | 格式 | 规模 | 说明 |
| --- | --- | --- | --- |
| `data/cargo_dataset.jsonl.gz` | gzip 压缩的 UTF-8 JSONL | 500,000 条货源；解压后 210,674,085 字节 | 每行一条货源，完整保留原始字节 |
| `data/drivers.json` | UTF-8 JSON 数组 | 10 位司机 | 车辆、初始位置、里程成本与自然语言偏好 |
| `manifest.json` | JSON | 文件大小与 SHA-256 | 同时记录压缩文件和原始文件的校验值 |

货源 `create_time` 范围为 **2026-03-01 00:01:25 — 2026-03-31 23:59:06**。这是整份 Demo 输入，未额外划分训练集、验证集或测试集。

## 下载与解压

需要 Python 3.11+；解压脚本只依赖标准库，无需 Git LFS。

```bash
git clone https://github.com/Ahong2003/tianchi-freight-dataset.git
cd tianchi-freight-dataset
python scripts/prepare_dataset.py
```

脚本先校验仓库内的压缩文件和司机文件，再解压并校验原始 JSONL。默认输出 `data/cargo_dataset.jsonl`，重复运行会验证已有文件；发现不一致时退出，不覆盖已有文件。

如两个仓库位于同一父目录，可直接准备代码仓库的输入：

```bash
python scripts/prepare_dataset.py --output-dir ../tianchi-freight-agents/demo/server/data
```

原始 JSONL 约 211 MB，超过 GitHub 普通 Git 单文件限制，因此这里存储 gzip 无损压缩文件。解压后货源 SHA-256：

```text
da70a695a879fe7bef3c4b6915202e5baf61775d2b5fca8d89b186dcd1a0cc66
```

## 字段与单位

| 货源字段 | 含义 |
| --- | --- |
| `cargo_id` | 货源标识 |
| `create_time` / `remove_time` | 上架、下架时间 |
| `cargo_name` | 货源品类 |
| `start` / `end` | 起终点经纬度 |
| `load_time` | 装货时间窗，可为空 |
| `cost_time_minutes` | 运输耗时，单位分钟，按 Demo 口径包含装卸 |
| `price` | 原始价格，单位分；收益计算时除以 100 换算为元 |
| `truck_length` | 车辆长度要求 |

司机字段包括 `driver_id`、`name`、`vehicle_no`、`truck_length`、`cost_per_km`、`current_lat`、`current_lng`、`preferences`。字段原样保留，不重新解释为真实运营或真实个人记录。

仿真时间单位为分钟，起点为 `2026-03-01 00:00:00`；距离按仿真工具使用的 Haversine 大圆距离计算，单位 km。

详见随仓库保留的 [数据说明](docs/02-数据说明.md)、[赛题详情](docs/01-赛题详情.md)、[评测规则](docs/03-评测规则.md)。这些文档是原目录的说明快照。

## 决策接口约束

仿真运行时，参赛 Agent 应通过 `SimulationApiPort.query_cargo`、`get_driver_status`、`query_decision_history` 等接口获取可见信息。**不得直接读取本仓库全量货源或司机文件来进行决策**。独立存储数据不会改变原评测规则。

## 来源与许可说明

输入来自仓库所有者提供的 `alibabab/data/demo_docs_release_20260509/demo/server/data/`；该目录对应的发布压缩包名为 `demo_docs_release_20260509.zip`。压缩包 SHA-256 记录于 `manifest.json`。本地 `mb-main` 中的货源文件只是 Git LFS 指针，本仓库使用实际的完整数据，其 SHA-256 与该指针一致。

这里只整理和压缩既有文件，不声称创建了该数据集，也不声称代表比赛主办方。原目录未提供明确 LICENSE，因此未擅自为第三方数据和文档添加新的开源许可；使用和再分发仍需遵守原提供方的权利及比赛要求。

本仓库不包含模型密钥、本地配置、运行结果、缓存或 agent 代码。
