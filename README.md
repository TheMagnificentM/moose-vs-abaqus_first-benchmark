# Benchmark: MOOSE vs. Abaqus - Performance Comparison

## 1. Objective
This repository contains a performance and computational time benchmark comparing the MOOSE Framework to Abaqus. The goal is to investigate calculation times and scaling behavior using different element types (C3D8, C3D20, C3D20R) with a surface-to-surface penalty contact formulation.

## 2. Software & Hardware Specifications
To ensure reproducibility, here are the system and software details used for this benchmark:
* **Hardware:** AMD Ryzen Threadripper 7970X 32-Cores, 125Gi
* **Operating System:** Ubuntu 24.04.4 LTS
* **Abaqus Version:** Abaqus 2024
* **MOOSE Version:** 8e1829691aa5b117e1ef499e6304c11aa74881fa
* **Parallelization MOOSE:** cpus=8
* **Parallelization Abaqus:** mpiexec -n 8

## 3. Model Description
* **Physics:** Solid Mechanics
* **Material:** Linear elastic
* **Contact Formulation:** Surface-to-Surface Penalty Method (Penalty parameter = 1e5)
* **Time Integration:** dt = 0.5 (implicit)
* **Elements compared:** * C3D8 (Linear Hexahedral)
                         * C3D20 (Quadratic Hexahedral, fully integrated)
                         * C3D20R (Quadratic Hexahedral, reduced integration)

## 4. Solver Settings
* **Abaqus:** * Procedure: Implicit Dynamic (Quasi-static application)
              * Equation Solver: Default Direct Sparse Solver
              * Nonlinear Controls: Full Newton solution technique
* **MOOSE:** * Executioner: Transient
             * Nonlinear Solver: Full Newton
             * Linear Solver: Direct LU decomposition
             * Solver Package: MUMPS

## 5. Results Summary
A detailed presentation of the results can be found in the attached `presentation_github.pdf`. 
Brief summary of the issue:
* Both solvers yield the same physical results and stresses.
* Both MOOSE and Abaqus require a similar number of time steps and nonlinear iterations to converge, which indicates an excellent agreement in the fundamental solver mechanics.
* However, the total computational time in MOOSE is significantly higher. According to the performance logs, this overhead is primarily caused by the assembly of the Jacobian matrix, which takes an exceptionally long time.

## 6. My Question / Discussion Point
Since the number of nonlinear iterations is nearly identical, the bottleneck seems to be strictly related to the Jacobian assembly for higher-order elements with penalty contact. 
Are there any recommended MOOSE-specific performance optimizations, specific AD-flags (Automatic Differentiation), or alternative preconditioner settings to speed up the Jacobian evaluation for this specific setup?
