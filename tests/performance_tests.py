#!/usr/bin/env python3
"""
Performance testing for V2X Quantum Security Simulation
"""

import asyncio
import pytest
import time
from src.core.simulation_engine import V2XQuantumSimulationEngine
from src.crypto.pqc_manager import PQCManager

class TestPerformance:
    """Performance test suite"""
    
    @pytest.mark.asyncio
    async def test_simulation_scalability(self):
        """Test simulation performance with increasing vehicle counts"""
        vehicle_counts = [10, 50, 100, 200]
        results = {}
        
        for count in vehicle_counts:
            engine = V2XQuantumSimulationEngine()
            engine.config["simulation"]["max_vehicles"] = count
            engine.config["simulation"]["duration"] = 60  # Short test
            
            start_time = time.time()
            metrics = await engine.run_simulation("performance_test")
            end_time = time.time()
            
            results[count] = {
                "execution_time": end_time - start_time,
                "messages_per_second": metrics.total_messages / 60,
                "memory_usage": self._get_memory_usage()
            }
        
        # Assert scalability requirements
        assert results[200]["execution_time"] < 300  # 5 minutes max for 200 vehicles
    
    @pytest.mark.asyncio 
    async def test_pqc_performance(self):
        """Test PQC algorithm performance"""
        pqc_manager = PQCManager()
        
        start_time = time.time()
        results = await pqc_manager.evaluate_pqc_performance()
        evaluation_time = time.time() - start_time
        
        # Assert performance requirements
        assert evaluation_time < 60  # Should complete within 1 minute
        
        for algorithm, performance in results.items():
            # Signature/verification should be fast enough for V2X
            assert performance.signature_time < 0.01  # 10ms max
            assert performance.verification_time < 0.005  # 5ms max
    
    @pytest.mark.asyncio
    async def test_quantum_simulation_performance(self):
        """Test quantum attack simulation performance"""
        from src.quantum.quantum_simulator import QuantumAttackSimulator
        
        simulator = QuantumAttackSimulator()
        
        # Test Shor's algorithm simulation
        start_time = time.time()
        shor_results = await simulator.simulate_shors_attack(256, "ECC")
        shor_time = time.time() - start_time
        
        # Test Grover's algorithm simulation  
        start_time = time.time()
        grover_results = await simulator.simulate_grovers_attack(2**128, "AES")
        grover_time = time.time() - start_time
        
        assert shor_time < 30  # 30 seconds max for Shor simulation
        assert grover_time < 10  # 10 seconds max for Grover simulation
    
    def _get_memory_usage(self):
        """Get current memory usage"""
        import psutil
        import os
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024  # MB

if __name__ == "__main__":
    asyncio.run(TestPerformance().test_simulation_scalability())
