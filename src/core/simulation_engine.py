#!/usr/bin/env python3
"""
V2X Quantum Security Simulation Engine
Core module for simulating V2X networks with quantum security analysis
"""

import asyncio
import logging
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json
import time

class SecurityLevel(Enum):
    CLASSICAL = "classical"
    QUANTUM_RESISTANT = "quantum_resistant"
    HYBRID = "hybrid"

class AttackType(Enum):
    SHOR_ATTACK = "shor_attack"
    GROVER_ATTACK = "grover_attack"
    EAVESDROPPING = "eavesdropping"
    REPLAY_ATTACK = "replay_attack"
    SYBIL_ATTACK = "sybil_attack"

@dataclass
class V2XMessage:
    message_id: str
    sender_id: str
    receiver_id: str
    message_type: str
    payload: bytes
    timestamp: float
    security_level: SecurityLevel
    signature: Optional[bytes] = None
    encryption_algorithm: Optional[str] = None

@dataclass
class SimulationMetrics:
    total_messages: int
    successful_deliveries: int
    failed_deliveries: int
    average_latency: float
    security_breaches: int
    quantum_attack_success: float
    energy_consumption: float

class V2XQuantumSimulationEngine:
    """
    Main simulation engine for V2X networks with quantum security analysis
    """
    
    def __init__(self, config_path: str = "config/simulation_config.json"):
        self.logger = self._setup_logging()
        self.config = self._load_config(config_path)
        self.vehicles = {}
        self.road_side_units = {}
        self.attack_scenarios = {}
        self.defense_mechanisms = {}
        self.metrics = SimulationMetrics(0, 0, 0, 0.0, 0, 0.0, 0.0)
        self.quantum_simulator = None
        self.pqc_manager = None
        
        self._initialize_components()
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/simulation.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def _load_config(self, config_path: str) -> Dict:
        """Load simulation configuration"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.warning("Config file not found, using defaults")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """Get default simulation configuration"""
        return {
            "simulation": {
                "duration": 3600,  # seconds
                "time_step": 0.1,   # seconds
                "area_size": "1000x1000m",
                "max_vehicles": 100
            },
            "security": {
                "default_algorithm": "ECDSA",
                "quantum_resistant_algorithms": ["Dilithium2", "Falcon512", "Kyber512"],
                "enable_quantum_attacks": True
            },
            "network": {
                "communication_range": 300,  # meters
                "message_frequency": 10,     # Hz
                "channel_capacity": 10e6     # bps
            }
        }
    
    def _initialize_components(self):
        """Initialize all simulation components"""
        self.logger.info("Initializing simulation components...")
        
        # Initialize quantum simulator
        from src.quantum.quantum_simulator import QuantumAttackSimulator
        self.quantum_simulator = QuantumAttackSimulator()
        
        # Initialize PQC manager
        from src.crypto.pqc_manager import PQCManager
        self.pqc_manager = PQCManager()
        
        # Initialize network
        from src.network.v2x_network import V2XNetworkManager
        self.network_manager = V2XNetworkManager(self.config["network"])
        
        # Initialize attack scenarios
        self._initialize_attack_scenarios()
        
        # Initialize defense mechanisms
        self._initialize_defense_mechanisms()
        
        self.logger.info("All components initialized successfully")
    
    def _initialize_attack_scenarios(self):
        """Initialize quantum and classical attack scenarios"""
        self.attack_scenarios = {
            AttackType.SHOR_ATTACK: {
                "name": "Shor's Algorithm Attack",
                "description": "Quantum attack breaking RSA/ECC cryptography",
                "success_probability": 0.0,
                "execution_time": 0.0,
                "qubit_requirements": 0
            },
            AttackType.GROVER_ATTACK: {
                "name": "Grover's Algorithm Attack",
                "description": "Quantum search attack on symmetric crypto",
                "success_probability": 0.0,
                "execution_time": 0.0,
                "qubit_requirements": 0
            },
            AttackType.EAVESDROPPING: {
                "name": "Quantum Eavesdropping",
                "description": "Intercept quantum-secured communications",
                "success_probability": 0.0,
                "detection_probability": 0.0
            }
        }
    
    def _initialize_defense_mechanisms(self):
        """Initialize quantum-resistant defense mechanisms"""
        self.defense_mechanisms = {
            "pqc_migration": {
                "name": "PQC Migration",
                "description": "Transition to post-quantum cryptography",
                "effectiveness": 0.0,
                "performance_impact": 0.0
            },
            "quantum_key_distribution": {
                "name": "QKD",
                "description": "Quantum Key Distribution for secure key exchange",
                "effectiveness": 1.0,
                "performance_impact": 0.3
            },
            "hybrid_crypto": {
                "name": "Hybrid Cryptography",
                "description": "Combine classical and quantum-resistant crypto",
                "effectiveness": 0.9,
                "performance_impact": 0.2
            }
        }
    
    async def run_simulation(self, scenario: str = "default") -> SimulationMetrics:
        """
        Run the main simulation loop
        """
        self.logger.info(f"Starting simulation with scenario: {scenario}")
        start_time = time.time()
        
        # Load scenario configuration
        scenario_config = self._load_scenario_config(scenario)
        
        # Initialize vehicles and infrastructure
        await self._initialize_simulation_environment(scenario_config)
        
        # Main simulation loop
        simulation_time = 0
        time_step = self.config["simulation"]["time_step"]
        total_duration = self.config["simulation"]["duration"]
        
        with tqdm(total=total_duration, desc="Simulation Progress") as pbar:
            while simulation_time < total_duration:
                # Update vehicle positions and states
                await self._update_vehicle_states(time_step)
                
                # Handle V2X communications
                await self._process_v2x_communications()
                
                # Execute attack scenarios
                await self._execute_attack_scenarios()
                
                # Apply defense mechanisms
                await self._apply_defense_mechanisms()
                
                # Collect metrics
                self._collect_metrics(time_step)
                
                simulation_time += time_step
                pbar.update(time_step)
                
                # Yield control for async operations
                await asyncio.sleep(0)
        
        # Finalize simulation
        await self._finalize_simulation()
        
        end_time = time.time()
        self.metrics.simulation_duration = end_time - start_time
        
        self.logger.info(f"Simulation completed in {self.metrics.simulation_duration:.2f} seconds")
        return self.metrics
    
    async def _initialize_simulation_environment(self, scenario_config: Dict):
        """Initialize vehicles, RSUs, and network topology"""
        self.logger.info("Initializing simulation environment...")
        
        # Create vehicles
        vehicle_count = scenario_config.get("vehicle_count", 50)
        for i in range(vehicle_count):
            vehicle_id = f"vehicle_{i:03d}"
            vehicle = await self._create_vehicle(vehicle_id, scenario_config)
            self.vehicles[vehicle_id] = vehicle
        
        # Create Road Side Units
        rsu_count = scenario_config.get("rsu_count", 5)
        for i in range(rsu_count):
            rsu_id = f"rsu_{i:02d}"
            rsu = await self._create_rsu(rsu_id, scenario_config)
            self.road_side_units[rsu_id] = rsu
        
        # Initialize network connections
        await self.network_manager.initialize_network(
            list(self.vehicles.values()),
            list(self.road_side_units.values())
        )
        
        self.logger.info(f"Environment initialized with {vehicle_count} vehicles and {rsu_count} RSUs")
    
    async def _create_vehicle(self, vehicle_id: str, config: Dict):
        """Create a vehicle with specified characteristics"""
        from src.network.vehicle import IntelligentVehicle
        
        vehicle = IntelligentVehicle(
            vehicle_id=vehicle_id,
            position=self._generate_random_position(),
            velocity=self._generate_random_velocity(),
            communication_range=config.get("communication_range", 300),
            security_level=SecurityLevel.QUANTUM_RESISTANT,
            crypto_algorithms=config.get("crypto_algorithms", ["Kyber512", "Dilithium2"])
        )
        
        return vehicle
    
    async def _create_rsu(self, rsu_id: str, config: Dict):
        """Create a Road Side Unit"""
        from src.network.rsu import RoadSideUnit
        
        rsu = RoadSideUnit(
            rsu_id=rsu_id,
            position=self._generate_fixed_position(len(self.road_side_units)),
            communication_range=config.get("rsu_range", 500),
            security_level=SecurityLevel.QUANTUM_RESISTANT,
            is_quantum_enhanced=config.get("quantum_enhanced", False)
        )
        
        return rsu
    
    def _generate_random_position(self) -> Tuple[float, float]:
        """Generate random position within simulation area"""
        area_size = self.config["simulation"]["area_size"]
        max_x, max_y = map(int, area_size.split('x'))
        return (np.random.uniform(0, max_x), np.random.uniform(0, max_y))
    
    def _generate_random_velocity(self) -> Tuple[float, float]:
        """Generate random velocity vector"""
        speed = np.random.uniform(0, 30)  # m/s
        angle = np.random.uniform(0, 2 * np.pi)
        return (speed * np.cos(angle), speed * np.sin(angle))
    
    def _generate_fixed_position(self, index: int) -> Tuple[float, float]:
        """Generate fixed position for RSUs"""
        area_size = self.config["simulation"]["area_size"]
        max_x, max_y = map(int, area_size.split('x'))
        
        positions = [
            (max_x * 0.2, max_y * 0.2),
            (max_x * 0.8, max_y * 0.2),
            (max_x * 0.5, max_y * 0.5),
            (max_x * 0.2, max_y * 0.8),
            (max_x * 0.8, max_y * 0.8)
        ]
        
        return positions[index % len(positions)]
    
    async def _update_vehicle_states(self, time_step: float):
        """Update positions and states of all vehicles"""
        for vehicle in self.vehicles.values():
            await vehicle.update_state(time_step)
    
    async def _process_v2x_communications(self):
        """Process V2X message exchanges"""
        messages = []
        
        # Generate messages from vehicles
        for vehicle in self.vehicles.values():
            if vehicle.should_send_message():
                message = await vehicle.generate_v2x_message()
                messages.append(message)
        
        # Generate messages from RSUs
        for rsu in self.road_side_units.values():
            if rsu.should_broadcast():
                message = await rsu.generate_broadcast_message()
                messages.append(message)
        
        # Process all messages through network
        for message in messages:
            success = await self.network_manager.deliver_message(message)
            if success:
                self.metrics.successful_deliveries += 1
            else:
                self.metrics.failed_deliveries += 1
            
            self.metrics.total_messages += 1
    
    async def _execute_attack_scenarios(self):
        """Execute quantum and classical attack scenarios"""
        if not self.config["security"]["enable_quantum_attacks"]:
            return
        
        # Execute Shor's algorithm attack on classical crypto
        shor_results = await self.quantum_simulator.simulate_shors_attack(
            key_size=256,
            crypto_system="ECC"
        )
        
        self.attack_scenarios[AttackType.SHOR_ATTACK].update({
            "success_probability": shor_results.success_probability,
            "execution_time": shor_results.execution_time,
            "qubit_requirements": shor_results.qubit_requirements
        })
        
        # Execute Grover's algorithm attack
        grover_results = await self.quantum_simulator.simulate_grovers_attack(
            search_space=2**128,
            crypto_system="AES"
        )
        
        self.attack_scenarios[AttackType.GROVER_ATTACK].update({
            "success_probability": grover_results.success_probability,
            "execution_time": grover_results.execution_time,
            "qubit_requirements": grover_results.qubit_requirements
        })
    
    async def _apply_defense_mechanisms(self):
        """Apply quantum-resistant defense mechanisms"""
        # Evaluate PQC migration effectiveness
        pqc_performance = await self.pqc_manager.evaluate_pqc_performance()
        
        self.defense_mechanisms["pqc_migration"].update({
            "effectiveness": pqc_performance.security_level,
            "performance_impact": pqc_performance.performance_impact
        })
    
    def _collect_metrics(self, time_step: float):
        """Collect simulation metrics"""
        # Calculate average latency
        if self.metrics.successful_deliveries > 0:
            total_latency = self.network_manager.get_average_latency()
            self.metrics.average_latency = total_latency
        
        # Count security breaches
        self.metrics.security_breaches = self._count_security_breaches()
        
        # Calculate quantum attack success rate
        quantum_success = sum(
            attack["success_probability"] 
            for attack in self.attack_scenarios.values() 
            if "success_probability" in attack
        ) / len(self.attack_scenarios)
        self.metrics.quantum_attack_success = quantum_success
        
        # Estimate energy consumption
        self.metrics.energy_consumption = self._estimate_energy_consumption(time_step)
    
    def _count_security_breaches(self) -> int:
        """Count number of security breaches in the simulation"""
        breaches = 0
        
        for vehicle in self.vehicles.values():
            breaches += vehicle.security_breaches
        
        for rsu in self.road_side_units.values():
            breaches += rsu.security_breaches
        
        return breaches
    
    def _estimate_energy_consumption(self, time_step: float) -> float:
        """Estimate total energy consumption"""
        base_consumption = 0.1  # watts per vehicle per second
        crypto_consumption = 0.05  # additional watts for crypto operations
        quantum_consumption = 0.2  # additional watts for quantum operations
        
        total_energy = 0
        
        for vehicle in self.vehicles.values():
            energy = base_consumption
            if vehicle.security_level == SecurityLevel.QUANTUM_RESISTANT:
                energy += crypto_consumption
            if vehicle.is_quantum_enhanced:
                energy += quantum_consumption
            total_energy += energy * time_step
        
        for rsu in self.road_side_units.values():
            energy = base_consumption * 2  # RSUs consume more power
            if rsu.security_level == SecurityLevel.QUANTUM_RESISTANT:
                energy += crypto_consumption
            if rsu.is_quantum_enhanced:
                energy += quantum_consumption * 2
            total_energy += energy * time_step
        
        return total_energy
    
    async def _finalize_simulation(self):
        """Finalize simulation and cleanup"""
        self.logger.info("Finalizing simulation...")
        
        # Save results
        await self._save_simulation_results()
        
        # Generate reports
        await self._generate_reports()
        
        # Cleanup resources
        await self.network_manager.cleanup()
        
        self.logger.info("Simulation finalized successfully")
    
    async def _save_simulation_results(self):
        """Save simulation results to files"""
        results = {
            "metrics": self.metrics.__dict__,
            "attack_scenarios": self.attack_scenarios,
            "defense_mechanisms": self.defense_mechanisms,
            "timestamp": time.time()
        }
        
        os.makedirs("data/results", exist_ok=True)
        with open(f"data/results/simulation_{int(time.time())}.json", 'w') as f:
            json.dump(results, f, indent=2)
    
    async def _generate_reports(self):
        """Generate comprehensive simulation reports"""
        from src.analysis.report_generator import ReportGenerator
        
        report_generator = ReportGenerator(self.metrics, self.attack_scenarios, self.defense_mechanisms)
        
        # Generate text report
        await report_generator.generate_text_report()
        
        # Generate visualizations
        await report_generator.generate_visualizations()
        
        # Generate security recommendations
        await report_generator.generate_security_recommendations()
    
    def get_real_time_metrics(self) -> Dict:
        """Get real-time metrics for monitoring"""
        return {
            "vehicles_active": len(self.vehicles),
            "rsus_active": len(self.road_side_units),
            "messages_processed": self.metrics.total_messages,
            "success_rate": (
                self.metrics.successful_deliveries / self.metrics.total_messages 
                if self.metrics.total_messages > 0 else 0
            ),
            "security_breaches": self.metrics.security_breaches,
            "quantum_threat_level": self.metrics.quantum_attack_success
        }
