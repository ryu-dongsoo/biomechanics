# 🛠️ Week 2 Lab: Projectile Motion

> **Author / Rights Holder:** Dongsoo Ryu, Dept. of Biosystems Machinery Engineering, Jeonbuk National University (ryudongsoo@jbnu.ac.kr)

[Back to English Main](../README.md)

This folder contains Python simulation and visualization (animation) materials for the curvilinear and projectile motion problems covered in the **Week 2 Lecture** of Biomechanics.

## 📌 Lab Overview & Objectives

- **Resolution of 2D Motion**: Break down curvilinear motion into independent 1D motions along the $x$ and $y$ axes.
- **Projectile Motion Simulation**: Model various projectile trajectories under gravity (-g), such as a baseball, an airplane drop, or a projectile in a tunnel.
- **Problem Solving Skills**: Derive solutions that satisfy given constraints (target height, range, clearance) and visually verify them.

## 💻 Provided Simulation Codes

The following Python scripts simulate the problems solved during the lecture. Running the code will display an animation of the $x-y$ plane trajectory and velocity components.

| Filename | Target Problem | Description |
|----------|----------------|-------------|
| `ex2_5_curvilinear.py` | Example 2.5 | General curvilinear motion tracking ($v_x = 50 - 16t, y = 100 - 4t^2$) |
| `ex2_6_projectile.py` | Example 2.6 | Trajectory of a baseball clearing a 6m fence |
| `prob2_60_airplane_drop.py` | Problem 2/60 | Mail drop from an airplane at 100m altitude and sight angle |
| `prob2_67_tunnel.py` | Problem 2/67 | Maximum range trajectory without hitting the tunnel ceiling |

## 📝 Homework

- Filename: `homework_skeleton_proj.py`
- This is a skeleton code designed for you to independently simulate the assigned homework problems (2/62 ~ 2/66).
- **Instructions**: Follow the comments marked with `TODO` to implement your own initial conditions, equations of motion for $x$ and $y$, and complete the trajectory animation.

## ▶️ How to Run

Execute the scripts via the terminal. (Make sure `numpy` and `matplotlib` are installed)

```bash
# Run Example 2.6
python ex2_6_projectile.py
```

---

## 📝 Changelog
- **2026-05-22 19:00:00** [[ryu-dongsoo](mailto:ryudongsoo@jbnu.ac.kr)] feat: add Week 2 lab instructions and trajectory simulation codes

---

## 📝 변경 이력 (Changelog)
- **2026-11-01 23:35:00** [[Dongsoo Ryu](mailto:ryudongsoo@jbnu.ac.kr)] feat: release Weeks 1–15 bilingual biomechanics simulation portfolio & supplementary concept animations
