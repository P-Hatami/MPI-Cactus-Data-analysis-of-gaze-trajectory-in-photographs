# MPI-Cactus-Data-analysis-of-gaze-trajectory-in-photographs

# Luminance-Biased Stochastic Gaze Simulator
**A Mathematical and Biologically-Grounded Approach to Free-Viewing Trajectories**

This repository contains an experimental pipeline to simulate human gaze trajectories on natural images, heavily inspired by the physiological processing in the retina and primary visual cortex (V1). 

## 1. Physical Light Extraction (Retinal Input Simulation)
Before extracting high-level features, visual data must be mapped to how the human eye physically perceives light. The script processes raw RGB scenes into a **Physical Luminance Map** based on Photopic Vision principles. 

Using the ITU-R BT.709 photometric formula, the pipeline applies specific mathematical weights to color channels ($Y = 0.2126R + 0.7152G + 0.0722B$) to reflect the exact spectral sensitivity of retinal cone cells (peaking at ~555 nm for green light). This ensures that the downstream saliency algorithms operate on biologically accurate intensity values rather than naive grayscale conversions.

## 2. Primary Visual Cortex (V1) Saliency Modeling
Once the physical luminance is extracted, the pipeline simulates the low-level processing of the Primary Visual Cortex (V1). 

In neurobiology, V1 simple cells function as directional edge detectors. To mathematically replicate this mechanism, the system applies a bank of **Gabor Filters** across multiple orientations (e.g., 0°, 45°, 90°, 135°). The absolute responses from these orientation-selective filters are aggregated using a maximum-activation strategy. 

The resulting **Bottom-Up Saliency Map** highlights regions with high spatial contrast and structural complexity. These regions represent the visual stimuli that naturally attract human saccades before any top-down cognitive tasks (like object recognition) are engaged.
