#!/usr/bin/env python3
"""
Main execution script for V2X Quantum Security Simulation
"""

import asyncio
import argparse
import logging
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.simulation_engine import V2XQuantumSimulationEngine
from analysis.report_generator import ReportGenerator

async def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='V2X Quantum Security Simulation')
    parser.add_argument('--scenario', type=str, default='urban_highway',
                       help='Simulation scenario (urban_highway, city_center, highway)')
    parser.add_argument('--duration', type=int, default=600,
                       help='Simulation duration in seconds')
    parser.add_argument('--vehicles', type=int, default=50,
                       help='Number of vehicles')
    parser.add_argument('--output', type=str, default='results',
                       help='Output directory for results')
    parser.add_argument('--visualize', action='store_true',
                       help='Enable real-time visualization')
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('simulation.log'),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starting V2X Quantum Security Simulation")
        logger.info(f"Scenario: {args.scenario}")
        logger.info(f"Duration: {args.duration}s")
        logger.info(f"Vehicles: {args.vehicles}")
        
        # Initialize simulation engine
        engine = V2XQuantumSimulationEngine()
        
        # Update configuration based on arguments
        engine.config["simulation"]["duration"] = args.duration
        engine.config["simulation"]["max_vehicles"] = args.vehicles
        
        # Run simulation
        metrics = await engine.run_simulation(args.scenario)
        
        # Generate reports
        report_generator = ReportGenerator(metrics, engine.attack_scenarios, engine.defense_mechanisms)
        await report_generator.generate_comprehensive_report()
        
        logger.info("Simulation completed successfully")
        
        # Print summary
        print("\n" + "="*50)
        print("SIMULATION SUMMARY")
        print("="*50)
        print(f"Total Messages: {metrics.total_messages}")
        print(f"Success Rate: {(metrics.successful_deliveries/metrics.total_messages)*100:.1f}%")
        print(f"Security Breaches: {metrics.security_breaches}")
        print(f"Quantum Attack Success: {metrics.quantum_attack_success*100:.1f}%")
        print(f"Average Latency: {metrics.average_latency*1000:.2f} ms")
        print(f"Energy Consumption: {metrics.energy_consumption:.2f} W")
        
    except Exception as e:
        logger.error(f"Simulation failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
