# End-to-end Serving Grounding Dino into Google Kubernetes Engine
<p align="center">
  <img src="https://github.com/duongnguyen-dev/serving_grounding_dino/blob/main/assets/grounding_dino_image.png" width="30%" height="30%"/>
</p>

- This repo will show you how to 📖:
  - **Train or fine-tune** Grounding Dino model on your own dataset ⭐
  - Serve your own **Grounding Dino API onto GKE** using **CI/CD** ⭐⭐

## System Architecture
<p align="center">
  <img src="https://github.com/duongnguyen-dev/serving_grounding_dino/blob/main/assets/system_architecture.png" />
</p>
## Table of content
1. <a href="#1.-train-and-fine-tune-model" color="blue">Train and fine-tune model</a>
2. [Create GKE Cluster](2.-create-gke-cluster)

## 1. Train and fine-tune model
- Create conda environment Python >= 3.9 (Recommend Python 3.11):
  ```
  conda create -n [your_env_name] python=3.11
  conda activate [your_env_name]
  ```
  **NOTE**: Replace `[your_env_name]` with your desired environment name
  
- Install all required dependencies:
  ```
  pip install -r requirements.txt
  ```

## 2. Create GKE cluster
- 
