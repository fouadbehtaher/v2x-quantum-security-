from src.quantum.quantum_simulator import QuantumAttackSimulator

simulator = QuantumAttackSimulator()
shor_results = await simulator.simulate_shors_attack(
    key_size=256,
    crypto_system="ECC"
)

print(f"Shor's Attack Success: {shor_results.success_probability:.2%}")

