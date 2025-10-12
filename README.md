# v2x-quantum-security-
Comprehensive simulation framework for V2X network security in the quantum computing era
# 🚗 V2X Quantum Security Simulator

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![OMNeT++](https://img.shields.io/badge/OMNeT++-6.0+-orange)
![Qiskit](https://img.shields.io/badge/Qiskit-0.44+-purple)
![License](https://img.shields.io/badge/License-MIT-green)
![Build](https://img.shields.io/badge/Build-Passing-brightgreen)

A comprehensive simulation framework for analyzing V2X network security in the quantum computing era. This project evaluates Post-Quantum Cryptography (PQC) algorithms, simulates quantum attacks, and provides migration strategies for automotive security.

## 🌟 Features

- **Quantum Attack Simulation**: Simulate Shor's and Grover's algorithms on V2X cryptography
- **PQC Performance Analysis**: Benchmark NIST-standardized PQC algorithms in V2X scenarios
- **Real-time Visualization**: Interactive dashboard for monitoring simulation metrics
- **Hybrid Security Models**: Evaluate classical + quantum-resistant cryptographic systems
- **Extensible Architecture**: Modular design for custom scenarios and algorithms

## 🏗️ Architecture
┌─────────────────────────────────────────────────────────────┐
│ V2X Quantum Security Framework │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐ │
│ │ Quantum │ │ V2X │ │ Security │ │
│ │ Simulator │ │ Network │ │ Analyzer │ │
│ │ │ │ Engine │ │ │ │
│ └─────────────┘ └─────────────┘ └─────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐ │
│ │ PQC │ │ Attack │ │ Visualization │ │
│ │ Manager │ │ Scenarios │ │ Dashboard │ │
│ │ │ │ │ │ │ │
│ └─────────────┘ └─────────────┘ └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘

Basic Usage

from src.core.simulation_engine import V2XQuantumSimulationEngine

 Initialize simulation
engine = V2XQuantumSimulationEngine()

 Run simulation
metrics = await engine.run_simulation("urban_highway")

 Analyze results
print(f"Success Rate: {metrics.success_rate:.2%}")
print(f"Quantum Threat Level: {metrics.quantum_threat_level:.2%}")

📊 Example Results
PQC Algorithm Performance
<img width="697" height="236" alt="image" src="https://github.com/user-attachments/assets/85b2e272-8134-4543-a422-e845a363a697" />

Quantum Attack Impact
Shor's Algorithm: 98.7% success against ECDSA-256

Grover's Algorithm: 56.2% success against AES-128

Migration to PQC: Reduces quantum vulnerability to < 0.1%

