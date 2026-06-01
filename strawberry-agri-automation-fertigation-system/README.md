# Strawberry Agri-Automation Fertigation System (SAAFS)
# 草莓农业自动化配肥系统

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)

### 📝 Overview / 项目概述
**EN:** Core calculation engine for strawberry open-field fertigation based on the SAAFS solid powder nutrient architecture. This project integrates agricultural plant physiology with modern software engineering to provide dynamic precision fertigation formulas based on first principles.

**ZH:** 基于 SAAFS 固体粉末营养体系的草莓户外农田全生命周期水肥一体化计算核心引擎。本项目将农业植物生理学与现代软件工程相结合，提供基于第一性原理的动态精准配肥方案。

---

### 🚀 Core Features / 核心特性

- **Dynamic Ratio Logic / 动态配比逻辑**
  - **EN:** Rejects rigid static recipes, supporting algorithmic seamless transitions across three major growth stages (Vegetative, Flowering, and Fruit Expansion).
  - **ZH:** 解耦传统固定配方，支持三大生育阶段（营养生长、开花坐果、果实膨大）的算法化无缝切换。
- **Linear Scaling Engine / 线性缩放引擎**
  - **EN:** Computes exact solute mass weights dynamically for any target irrigation volume based on stoichiometry and mass conservation.
  - **ZH:** 基于化学计量与质量守恒定律，输入任意目标灌溉水量，自动计算各原料的精确称重。
- **Production Ready / 工业级集成**
  - **EN:** Built with strict type checking and defensive boundary validation. Zero external dependencies—highly optimized for AIoT edge or cloud integration.
  - **ZH:** 内置强类型检查与防御性边界验证。零外部依赖，极易嵌入 AIoT 边缘端或云端水肥控制系统。

---

### ⚡ Quick Start / 快速开始

#### 1. Run the Demo / 运行演示
**EN:** This project relies strictly on the Python standard library. Run the core module directly to execute telemetry validation loops:
**ZH:** 本项目完全基于 Python 标准库开发。直接运行核心模块即可执行边界与数据验证演示：
```bash
python strawberry_fertigation_calculator.py
