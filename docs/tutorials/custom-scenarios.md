from src.core.simulation_engine import V2XQuantumSimulationEngine

# Create custom scenario
custom_config = {
    "vehicles": 100,
    "rsu_count": 10,
    "security_level": "quantum_resistant",
    "pqc_algorithms": ["Falcon512", "Dilithium2"]
}

engine = V2XQuantumSimulationEngine(config_path="custom_config.json")
results = await engine.run_simulation("custom_scenario")
