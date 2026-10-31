# MPI-Cactus-Data-analysis-of-gaze-trajectory-in-photographs

# V1-Inspired Stochastic Gaze Simulator
**A Mathematical and Biologically-Grounded Approach to Free-Viewing Trajectories**

This repository contains an experimental computational pipeline designed to simulate human gaze trajectories (saccades and fixations) on natural images. Rather than relying on black-box deep learning models, this project approaches visual attention from a **First-Principles perspective**, bridging light physics, primary visual cortex (V1) neurobiology, and stochastic Markov processes.

This project serves as a foundational proof-of-concept for analyzing large-scale free-viewing datasets (such as **COCO-FreeView**) to understand the underlying mechanics of human visual attention.

---

## 1. Physical Light Extraction (Retinal Input)
Visual data processing must begin with how the human eye physically perceives light. The pipeline converts raw RGB scenes into a **Physical Luminance Map** based on Photopic Vision principles. 

Using the standard ITU-R BT.709 photometric formula, the system applies specific weights to reflect the exact spectral sensitivity of retinal cone cells (peaking at ~555 nm for green light):

$$ Y(x,y) = 0.2126 \cdot R(x,y) + 0.7152 \cdot G(x,y) + 0.0722 \cdot B(x,y) $$

<div align="center">
  <!-- TODO: Upload your generated images to a 'docs' folder and replace these links -->
  <img src="docs/original_vs_luminance.png" alt="RGB to Luminance" width="700"/>
  <p><i>Left: Original RGB Scene | Right: Physical Luminance Map</i></p>
</div>

---

## 2. Primary Visual Cortex (V1) Saliency Modeling
In neurobiology, V1 simple cells act as directional edge detectors. To mathematically replicate this mechanism, the system applies a bank of **2D Gabor Filters** across multiple orientations ($\theta \in \{0, \frac{\pi}{4}, \frac{\pi}{2}, \frac{3\pi}{4}\}$).

A Gabor filter is a Gaussian kernel modulated by a sinusoidal plane wave, defined mathematically as:

$$ g(x,y; \lambda, \theta, \psi, \sigma, \gamma) = \exp\left(-\frac{x'^2 + \gamma^2 y'^2}{2\sigma^2}\right) \cos\left(2\pi \frac{x'}{\lambda} + \psi\right) $$

*Where:*  
$x' = x \cos\theta + y \sin\theta$  
$y' = -x \sin\theta + y \cos\theta$

The absolute responses from these orientation-selective filters are aggregated using a maximum-activation strategy, yielding a **Bottom-Up Saliency Map** ($S$) that highlights structurally complex regions.

<div align="center">
  <img src="docs/v1_saliency.png" alt="V1 Saliency Map" width="500"/>
  <p><i>Aggregated V1 Biological Saliency Map highlighting structural contrasts.</i></p>
</div>

---

## 3. Stochastic Gaze Simulation (Markov Process)
Finding salient regions is only half the problem; simulating how the human eye traverses these regions requires modeling behavioral dynamics. The human gaze alternates between **Fixations** (focusing on a point) and **Saccades** (ballistic jumps).

This module models the gaze trajectory as a biased **Stochastic Process (Markov Chain)**. The transition probability $P(x_{t+1} | x_t)$ of the eye jumping to a new pixel $x_{t+1}$ given the current position $x_t$ is determined by:

$$ P(x_{t+1} | x_t) = \frac{1}{Z} \cdot S(x_{t+1}) \cdot \exp\left(-\frac{||x_{t+1} - x_t||^2}{2\sigma_{spatial}^2}\right) $$

*Where:*
*   $S(x_{t+1})$ is the biological saliency at the target location.
*   The exponential term is a **2D Gaussian Spatial Penalty** that penalizes long-distance saccades, replicating the brain's energy-conservation mechanism.
*   $Z$ is the normalization constant ensuring $\sum P = 1$.

By sampling from this dynamically updated probability distribution, the system mathematically synthesizes a realistic visual scanpath.

<div align="center">
  <img src="docs/final_trajectory.png" alt="Simulated Gaze Trajectory" width="700"/>
  <p><i>Simulated Scanpath: Red dots indicate fixations, cyan lines represent saccades.</i></p>
</div>

---

## 4. Next Steps & Future Research
While this deterministic-stochastic approach provides a strong mathematical baseline, human free-viewing behavior contains significant individual variance and top-down cognitive biases. 

My next objective is to integrate this pipeline with the **COCO-FreeView dataset** (containing over 820,000 fixations). By applying Machine Learning techniques, I aim to:
1. Optimize the Markov transition matrix parameters ($\sigma_{spatial}$) based on real human data.
2. Train a neural network to capture the residual top-down cognitive behaviors that purely bottom-up models miss.
