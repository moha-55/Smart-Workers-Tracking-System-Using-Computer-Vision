# SMART CONSTRUCTION WORKERS TRACKING SYSTEM USING COMPUTER VISION


## Introduction
The construction industry, characterized by its ever-evolving landscapes and high-risk activities, is a sector where safety and efficiency are Adjective. It is a field that demands constant caution, as workers navigate through a plenty of potential hazards daily. 

A critical aspect of construction safety is the mandatory use of personal protective equipment (PPE), including safety vests and hardhats. These are not mere accessories; they are vital tools that protect workers from common hazards. 

So....

Human behaviour is diverse and varied, making identifying human-object interactions difficult. Human movement tracking systems can help optimize workflow on construction sites. 

Systems that track and analyze the movements of specific persons or groups of people are known as human movement tracking systems, and their use in various sectors is growing.

and that will lead to.....

## Problem Statement

High Accident Risk: Construction sites are prone to accidents due to complex hazards, which require improved safety monitoring.

Safety Gear Non-Compliance: Inconsistent use of essential safety equipment like hardhats and vests by construction workers leads to increased injury risks.

Behavioral Monitoring Challenges: The diversity in worker behavior and interactions on construction sites complicates effective safety and efficiency monitoring.


## The Objectives of this project

*To track construction workers at the site and detect their safety.*

*To build motion profile of each worker based on the tracked recorded.*

*To construct metrices to classify the safety of the workers.*

## Methodolgy 

The proposed system is implemented through these nine stages: 

1- Collect the dataset for workers, safety vests, hard hats, and motion.

2- Preprocess and label the dataset.

3- Train the first model using the dataset to track workers and detect their safety.

4- Test the first model on videos.

5- Train the second model to detect motion of the workers.

6-Test the second model on videos.

7- Classify the safety of the workers through the dashboard.

8- Hardware implementation using Jetson Nano and the camera.

9- Evaluate the system in real cases.

![image](https://github.com/moha-55/Smart-Workers-Tracking-System-Using-Computer-Vision/assets/121754960/dec6f595-1d31-428e-a2f4-095e5636af48)


![image](https://github.com/moha-55/Smart-Workers-Tracking-System-Using-Computer-Vision/assets/121754960/b5186a0d-9cd7-4b58-96ca-d6f129e90ecd)


## Datasets collection

Have got access to a good dataset which is uner the name POLAR: Posture-level Action Recognition Dataset (https://data.mendeley.com/datasets/hvnsh7rwz7/1) used it to bulid a model using YOLOV8 that detect motion and actions of the workers at the site.

It has nine 9 categories ("bending", "jumping", "lying", "running", "sitting", "squatting", "standing", "stretching" and "walking") directly related to human pose with a total of 35,324 images and covers 99% of posture-level human actions in daily life according to authors' analysis on the VOC dataset.

The other dataset is from kaggle which is for construction Personal Protective Equipments. (https://www.kaggle.com/datasets/snehilsanyal/construction-site-safety-image-dataset-roboflow)

I have used 1500 images to build model to detect the PPE.

## The Results 

The system has used Jetsno Nano and Arducam 8 MP Sony IMX219 camera: to test the models and see the results.

Results video : https://www.youtube.com/watch?v=EkbhE7FkK6o&feature=youtu.be

![image](https://github.com/moha-55/Smart-Workers-Tracking-System-Using-Computer-Vision/assets/121754960/c9b1708d-edbd-418d-8a3f-9f998fe47ec2)

![image](https://github.com/moha-55/Smart-Workers-Tracking-System-Using-Computer-Vision/assets/121754960/f66d3f97-8270-4b3d-8ef6-8e9e2c16cd5a)

The system is divided into to codes and two models, the safety model is to track the workers and detect their safety with samll dashboard that gives the number of workers and warning if there is somethng wrong.
![image](https://github.com/moha-55/Smart-Workers-Tracking-System-Using-Computer-Vision/assets/121754960/8a6daa89-da0e-457f-ab68-a6afb1ed39a7)


The second model is motion model to detect the motion of the workers, which are 5 types of motion (Run, walk, Lie, Sit, and stand) with samll dashboard that gives the number of workers and warning if there is somethng wrong.
![image](https://github.com/moha-55/Smart-Workers-Tracking-System-Using-Computer-Vision/assets/121754960/1fc3ea7c-39de-410e-a06c-845fd25b13c5)


