#!/usr/bin/env python3
"""
Interactive Dashboard for V2X Quantum Security Simulation
Real-time monitoring and visualization
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime
import asyncio
import json

class V2XSecurityDashboard:
    """
    Streamlit-based dashboard for V2X quantum security simulation
    """
    
    def __init__(self):
        self.setup_page_config()
        self.simulation_engine = None
        
    def setup_page_config(self):
        """Setup Streamlit page configuration"""
        st.set_page_config(
            page_title="V2X Quantum Security Simulator",
            page_icon="🚗",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Custom CSS
        st.markdown("""
        <style>
        .main-header {
            font-size: 3rem;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
        }
        .metric-card {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 10px;
            border-left: 5px solid #1f77b4;
        }
        .warning-card {
            background-color: #fff3cd;
            padding: 1rem;
            border-radius: 10px;
            border-left: 5px solid #ffc107;
        }
        .critical-card {
            background-color: #f8d7da;
            padding: 1rem;
            border-radius: 10px;
            border-left: 5px solid #dc3545;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Render the sidebar with configuration options"""
        st.sidebar.title("🔧 Simulation Configuration")
        
        # Simulation parameters
        st.sidebar.subheader("Simulation Parameters")
        duration = st.sidebar.slider("Duration (seconds)", 60, 3600, 600)
        vehicle_count = st.sidebar.slider("Vehicle Count", 10, 200, 50)
        rsu_count = st.sidebar.slider("RSU Count", 1, 20, 5)
        
        # Security configuration
        st.sidebar.subheader("Security Configuration")
        security_level = st.sidebar.selectbox(
            "Security Level",
            ["Classical", "Quantum-Resistant", "Hybrid"]
        )
        
        enable_quantum_attacks = st.sidebar.checkbox("Enable Quantum Attacks", True)
        enable_defenses = st.sidebar.checkbox("Enable Defense Mechanisms", True)
        
        # PQC algorithm selection
        st.sidebar.subheader("PQC Algorithms")
        pqc_algorithms = st.sidebar.multiselect(
            "Select PQC Algorithms",
            ["Kyber512", "Kyber768", "Dilithium2", "Dilithium3", "Falcon512", "SPHINCS128"],
            default=["Kyber512", "Dilithium2"]
        )
        
        # Attack scenarios
        st.sidebar.subheader("Attack Scenarios")
        shor_attack = st.sidebar.checkbox("Shor's Algorithm Attack", True)
        grover_attack = st.sidebar.checkbox("Grover's Algorithm Attack", True)
        eavesdropping = st.sidebar.checkbox("Quantum Eavesdropping", True)
        
        config = {
            "duration": duration,
            "vehicle_count": vehicle_count,
            "rsu_count": rsu_count,
            "security_level": security_level,
            "enable_quantum_attacks": enable_quantum_attacks,
            "enable_defenses": enable_defenses,
            "pqc_algorithms": pqc_algorithms,
            "attack_scenarios": {
                "shor_attack": shor_attack,
                "grover_attack": grover_attack,
                "eavesdropping": eavesdropping
            }
        }
        
        return config
    
    def render_header(self):
        """Render the main header"""
        st.markdown('<h1 class="main-header">🚗 V2X Quantum Security Simulator</h1>', 
                   unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown("""
            **Comprehensive simulation of V2X network security in the quantum computing era**
            - Post-Quantum Cryptography (PQC) performance analysis
            - Quantum attack simulation and impact assessment
            - Real-time security monitoring and visualization
            """)
        
        with col2:
            if st.button("🎬 Start Simulation", type="primary"):
                st.session_state.simulation_running = True
                asyncio.run(self.start_simulation())
        
        with col3:
            if st.button("⏹️ Stop Simulation"):
                st.session_state.simulation_running = False
    
    def render_real_time_metrics(self, metrics):
        """Render real-time metrics cards"""
        st.subheader("📊 Real-time Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Active Vehicles",
                value=metrics.get("vehicles_active", 0),
                delta=None
            )
        
        with col2:
            success_rate = metrics.get("success_rate", 0) * 100
            st.metric(
                label="Message Success Rate",
                value=f"{success_rate:.1f}%",
                delta=None
            )
        
        with col3:
            st.metric(
                label="Security Breaches",
                value=metrics.get("security_breaches", 0),
                delta=None
            )
        
        with col4:
            threat_level = metrics.get("quantum_threat_level", 0) * 100
            st.metric(
                label="Quantum Threat Level",
                value=f"{threat_level:.1f}%",
                delta=None
            )
    
    def render_network_visualization(self, network_data):
        """Render network topology visualization"""
        st.subheader("🌐 Network Topology")
        
        # Create network graph
        fig = go.Figure()
        
        # Add vehicles
        if 'vehicles' in network_data:
            vehicle_positions = network_data['vehicles']
            fig.add_trace(go.Scatter(
                x=[pos[0] for pos in vehicle_positions],
                y=[pos[1] for pos in vehicle_positions],
                mode='markers',
                name='Vehicles',
                marker=dict(size=10, color='blue')
            ))
        
        # Add RSUs
        if 'rsus' in network_data:
            rsu_positions = network_data['rsus']
            fig.add_trace(go.Scatter(
                x=[pos[0] for pos in rsu_positions],
                y=[pos[1] for pos in rsu_positions],
                mode='markers',
                name='RSUs',
                marker=dict(size=15, color='red', symbol='square')
            ))
        
        # Update layout
        fig.update_layout(
            title="V2X Network Topology",
            xaxis_title="X Position (m)",
            yaxis_title="Y Position (m)",
            showlegend=True,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_security_analysis(self, security_data):
        """Render security analysis section"""
        st.subheader("🔒 Security Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Quantum attack success probabilities
            if 'attack_scenarios' in security_data:
                attack_data = security_data['attack_scenarios']
                
                attack_names = list(attack_data.keys())
                success_probs = [attack_data[name].get('success_probability', 0) * 100 
                               for name in attack_names]
                
                fig = go.Figure(data=[
                    go.Bar(name='Success Probability', x=attack_names, y=success_probs)
                ])
                
                fig.update_layout(
                    title="Quantum Attack Success Probabilities",
                    yaxis_title="Success Probability (%)",
                    height=300
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # PQC performance comparison
            if 'pqc_performance' in security_data:
                pqc_data = security_data['pqc_performance']
                
                algorithms = list(pqc_data.keys())
                signature_times = [pqc_data[alg].get('signature_time', 0) * 1000 
                                 for alg in algorithms]
                
                fig = go.Figure(data=[
                    go.Bar(name='Signature Time', x=algorithms, y=signature_times)
                ])
                
                fig.update_layout(
                    title="PQC Algorithm Performance",
                    yaxis_title="Signature Time (ms)",
                    height=300
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    def render_threat_assessment(self, threat_data):
        """Render threat assessment section"""
        st.subheader("⚠️ Threat Assessment")
        
        # Risk matrix
        risks = threat_data.get('risks', {})
        
        for risk_name, risk_level in risks.items():
            if risk_level == "CRITICAL":
                st.markdown(f'<div class="critical-card"><strong>{risk_name}</strong>: {risk_level}</div>', 
                          unsafe_allow_html=True)
            elif risk_level == "HIGH":
                st.markdown(f'<div class="warning-card"><strong>{risk_name}</strong>: {risk_level}</div>', 
                          unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="metric-card"><strong>{risk_name}</strong>: {risk_level}</div>', 
                          unsafe_allow_html=True)
    
    def render_performance_metrics(self, performance_data):
        """Render performance metrics section"""
        st.subheader("⚡ Performance Metrics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            latency = performance_data.get('average_latency', 0) * 1000
            st.metric("Average Latency", f"{latency:.2f} ms")
        
        with col2:
            throughput = performance_data.get('throughput', 0)
            st.metric("Message Throughput", f"{throughput:.0f} msg/s")
        
        with col3:
            energy = performance_data.get('energy_consumption', 0)
            st.metric("Energy Consumption", f"{energy:.2f} W")
    
    async def start_simulation(self):
        """Start the simulation"""
        if self.simulation_engine is None:
            from src.core.simulation_engine import V2XQuantumSimulationEngine
            self.simulation_engine = V2XQuantumSimulationEngine()
        
        # Run simulation in background
        simulation_task = asyncio.create_task(
            self.simulation_engine.run_simulation()
        )
        
        # Update UI with real-time data
        await self.update_real_time_dashboard()
    
    async def update_real_time_dashboard(self):
        """Update dashboard with real-time simulation data"""
        placeholder = st.empty()
        
        while st.session_state.get('simulation_running', False):
            with placeholder.container():
                # Get real-time metrics
                if self.simulation_engine:
                    metrics = self.simulation_engine.get_real_time_metrics()
                    
                    # Render all dashboard components
                    self.render_real_time_metrics(metrics)
                    self.render_network_visualization(metrics.get('network_data', {}))
                    self.render_security_analysis(metrics.get('security_data', {}))
                    self.render_threat_assessment(metrics.get('threat_data', {}))
                    self.render_performance_metrics(metrics.get('performance_data', {}))
                
            # Wait before next update
            await asyncio.sleep(1)
    
    def run(self):
        """Run the dashboard"""
        # Initialize session state
        if 'simulation_running' not in st.session_state:
            st.session_state.simulation_running = False
        
        # Render sidebar and get configuration
        config = self.render_sidebar()
        
        # Render main content
        self.render_header()
        
        # Show configuration summary
        with st.expander("Configuration Summary"):
            st.json(config)
        
        # Render real-time dashboard if simulation is running
        if st.session_state.simulation_running:
            asyncio.run(self.update_real_time_dashboard())
        else:
            # Show static analysis or welcome content
            self.render_static_analysis()

def main():
    """Main function to run the dashboard"""
    dashboard = V2XSecurityDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()
