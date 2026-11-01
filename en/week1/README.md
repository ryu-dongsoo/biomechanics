# 🛠️ Week 1 Lab: Rectilinear Motion

> **Author / Rights Holder:** Dongsoo Ryu, Dept. of Biosystems Machinery Engineering, Jeonbuk National University (ryudongsoo@jbnu.ac.kr, ryudongsoo@gmail.com)

[Back to English Main](../README.md)

This folder contains the Python simulation and visualization (animation) materials for the rectilinear motion problems covered in the **Week 1 Lecture** of Biomechanics.

## 📌 Lab Overview & Objectives

- **Visual Understanding of Rectilinear Motion**: Observe the changes in position ($s$), velocity ($v$), and acceleration ($a$) over time through synchronized graphs and particle animations.
- **Coding Equations of Motion**: Implement the mathematical formulations (derivatives and integrals) learned in class as Python functions.
- **Problem Solving Skills**: Train to model physical constraints and program them under given conditions.

## 💻 Provided Simulation Codes

The following Python scripts simulate the problems solved during the lecture. Running the code will pop up an animation window.

| Filename | Target Problem | Description |
|----------|----------------|-------------|
| `ex2_1_kinematics.py` | Example 2.1 | Simulation of $s = 2t^3 - 24t + 6$ |
| `ex2_2_piecewise.py` | Example 2.2 | Piecewise constant acceleration (constant velocity then deceleration) |
| `ex2_3_spring.py` | Example 2.3 | Harmonic oscillation where acceleration is a function of position ($a = -k^2 s$) |
| `ex2_4_freight.py` | Example 2.4 | Deceleration where acceleration is proportional to square of velocity ($a = -k v^2$) |
| `prob2_1_extrema.py` | Problem 2/1 | Observation of points where acceleration is zero and velocity extrema |
| `prob2_4_integration.py`| Problem 2/4 | Position/velocity tracking through acceleration integration |

## 📝 Homework

- Filename: `homework_skeleton.py`
- This is a skeleton code designed for you to independently simulate the assigned homework problems (2/5, 2/6, 2/7, 2/8, 2/10).
- **Instructions**: Follow the comments marked with `TODO` to implement your own equations of motion and complete the graph animation.

## ▶️ How to Run

Execute the scripts via the terminal. (Make sure `numpy` and `matplotlib` are installed)

```bash
# Run Example 2.1
python ex2_1_kinematics.py
```

---

## 📝 Changelog
- **2026-05-22 18:55:00** [[ryu-dongsoo](mailto:ryudongsoo@jbnu.ac.kr)] feat: add Week 1 lab instructions and simulation codes

---

## 📝 변경 이력 (Changelog)
- **2026-11-01 23:35:00** [[Dongsoo Ryu](mailto:ryudongsoo@jbnu.ac.kr)] feat: release Weeks 1–15 bilingual biomechanics simulation portfolio & supplementary concept animations
