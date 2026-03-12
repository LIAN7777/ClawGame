# ClawGame 工作机制文档

## 一、任务流转规范

### 任务生命周期

```
待执行 → 执行中 → 已完成 → 已验证
   │         │         │         │
   │         │         │         └── QAClaw 验证通过 + CI通过
   │         │         └── 子Agent完成汇报
   │         └── 子Agent开始执行
   └── 主Agent分配任务
```

### 流转规则

| 当前阶段 | 下一阶段 | 触发条件 |
|----------|----------|----------|
| 待执行 | 执行中 | 主Agent分配任务给子Agent |
| 执行中 | 已完成 | 子Agent汇报完成 |
| 已完成 | 已验证 | QAClaw验证通过 **+ CI运行通过** |
| 已完成 | 执行中 | 测试失败/CI失败，返回开发 |

### CI 监控流程

```
DevOpsClaw 推送代码
        │
        ▼
GitHub Actions 触发
        │
        ▼
QAClaw 检查 CI 状态
        │
   ┌────┴────┐
   │ CI通过? │
   └────┬────┘
        │
   ┌────┴────┐
   Yes       No
   │         │
   ▼         ▼
任务完成   分析失败原因
          │
          ▼
    报告给对应Agent修复
```

### 任务状态标识

- ⏳ 执行中
- ✅ 已完成
- ❌ 失败/阻塞
- 🔄 返工中

---

## 二、记忆固化规范

### 固化时机

| 时机 | 操作 | 负责人 |
|------|------|--------|
| 最小任务完成 | 更新每日记录 | 子Agent |
| 阶段完成 | 更新项目文档 | 主Agent |
| 重要决策 | 更新MEMORY.md | 主Agent |
| 发现问题 | 记录到问题清单 | 发现者 |

### 固化内容模板

**每日记录 (`memory/YYYY-MM-DD.md`):**
```markdown
# YYYY-MM-DD 工作记录

## 完成的任务
- [X] 任务1: 描述
- [X] 任务2: 描述

## 遇到的问题
- 问题1: 描述 → 解决方案

## 学到的经验
- 经验1: 描述

## 下一步计划
- [ ] 任务3
```

---

## 三、ClawCoins 奖励机制

### 基础奖励

| 任务类型 | 基础 ClawCoins |
|----------|----------------|
| 简单功能实现 | 10 |
| 中等功能实现 | 20 |
| 复杂功能实现 | 50 |
| Bug修复 | 5-15 |
| 测试用例编写 | 5 |
| CI/CD配置 | 15 |

### 质量系数

| 质量等级 | 系数 |
|----------|------|
| 超出预期 | 2.0 |
| 高质量 | 1.5 |
| 合格 | 1.0 |
| 需改进 | 0.5 |

### 分配流程

1. 主Agent评估任务完成质量
2. 计算实际奖励 = 基础奖励 × 质量系数
3. 记录到 MEMORY.md 的 ClawCoins 表
4. 向用户汇报分配情况

---

## 四、断点续传流程

### 恢复步骤

1. **读取主Agent记忆**
   - `MEMORY.md` - 长期记忆
   - `memory/YYYY-MM-DD.md` - 最近工作

2. **读取项目状态**
   - `workspace-clawgame/docs/PROJECT.md` - 项目文档
   - `workspace-clawgame/memory/` - 项目记忆

3. **检查任务清单**
   - 找到最后一个 ⏳ 状态的任务
   - 确认该任务的产出物是否存在

4. **继续执行**
   - 从断点任务继续
   - 向用户汇报恢复情况

### 关键文件清单

```
/root/.openclaw/
├── workspace/
│   ├── MEMORY.md          # 主Agent长期记忆
│   └── memory/            # 主Agent每日记录
├── workspace-clawgame/
│   ├── docs/PROJECT.md    # 项目状态
│   └── memory/            # 项目每日记录
├── workspace-gamedev/
│   ├── MEMORY.md          # GameDevClaw记忆
│   └── memory/            # GameDevClaw记录
├── workspace-qa/
│   ├── MEMORY.md          # QAClaw记忆
│   └── memory/            # QAClaw记录
└── workspace-devops/
    ├── MEMORY.md          # DevOpsClaw记忆
    └── memory/            # DevOpsClaw记录
```
