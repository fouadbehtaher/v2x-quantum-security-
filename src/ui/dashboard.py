#!/usr/bin/env python3
"""
V2X Quantum Security Dashboard
Streamlit-based web interface for monitoring and analysis
"""

import streamlit as st
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="V2X Quantum Security Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
def load_css():
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #262730;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .security-alert {
        background-color: #ff4b4b;
        color: white;
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin: 0.5rem 0;
    }
    .success-metric {
        color: #00cc96;
    }
    .warning-metric {
        color: #ffa15a;
    }
    .danger-metric {
        color: #ff4b4b;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    """Main dashboard application"""
    
    # Load CSS
    load_css()
    
    # Sidebar
    st.sidebar.title("V2X Quantum Security")
    st.sidebar.markdown("---")
    
    # Navigation
    page = st.sidebar.radio(
        "Navigation",
        ["System Overview", "Quantum Security", "Simulation Results", "Security Analysis", "Configuration"]
    )
    
    # System Overview Page
    if page == "System Overview":
        show_system_overview()
    
    # Quantum Security Page
    elif page == "Quantum Security":
        show_quantum_security()
    
    # Simulation Results Page
    elif page == "Simulation Results":
        show_simulation_results()
    
    # Security Analysis Page
    elif page == "Security Analysis":
        show_security_analysis()
    
    # Configuration Page
    elif page == "Configuration":
        show_configuration()

def show_system_overview():
    """Display system overview dashboard"""
    
    st.markdown('<h1 class="main-header">🚗 V2X Quantum Security System Overview</h1>', unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Active Vehicles",
            value=45,
            delta="+3"
        )
    
    with col2:
        st.metric(
            label="RSU Connections",
            value=12,
            delta="+1"
        )
    
    with col3:
        st.metric(
            label="Quantum Keys Generated",
            value="1,234",
            delta="+56"
        )
    
    with col4:
        st.metric(
            label="Security Score",
            value="98%",
            delta="-2%"
        )
    
    st.markdown("---")
    
    # System status
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("System Status")
        
        # Status indicators
        status_data = {
            "Component": ["Quantum Core", "Simulation Engine", "Database", "Key Management", "Network Stack"],
            "Status": ["Online", "Online", "Online", "Online", "Warning"],
            "Latency (ms)": [12, 45, 8, 23, 156]
        }
        
        status_df = pd.DataFrame(status_data)
        st.dataframe(status_df, use_container_width=True)
    
    with col2:
        st.subheader("Quick Actions")
        
        if st.button("🔄 Refresh System", use_container_width=True):
            st.success("System refreshed successfully!")
        
        if st.button("🔐 Generate New Keys", use_container_width=True):
            st.info("Initiating quantum key generation...")
        
        if st.button("📊 Run Analysis", use_container_width=True):
            st.info("Starting security analysis...")
        
        if st.button("🚨 Security Audit", use_container_width=True):
            st.warning("Initiating comprehensive security audit...")

def show_quantum_security():
    """Display quantum security monitoring"""
    
    st.title("🔐 Quantum Security Monitoring")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Key Distribution Status")
        
        # Key distribution chart
        key_data = {
            "Time": pd.date_range("2024-01-01", periods=24, freq="H"),
            "Keys_Generated": [10, 15, 12, 18, 22, 25, 30, 28, 32, 35, 40, 38, 
                              42, 45, 48, 50, 52, 55, 58, 60, 62, 65, 68, 70],
            "Keys_Used": [8, 12, 10, 15, 18, 20, 25, 22, 28, 30, 35, 32,
                         38, 40, 42, 45, 48, 50, 52, 55, 58, 60, 62, 65]
        }
        
        key_df = pd.DataFrame(key_data)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=key_df["Time"], y=key_df["Keys_Generated"],
                                mode='lines', name='Keys Generated',
                                line=dict(color='#1f77b4', width=3)))
        fig.add_trace(go.Scatter(x=key_df["Time"], y=key_df["Keys_Used"],
                                mode='lines', name='Keys Used',
                                line=dict(color='#ff7f0e', width=3)))
        
        fig.update_layout(
            title="Quantum Key Distribution Over Time",
            xaxis_title="Time",
            yaxis_title="Number of Keys",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Security Metrics")
        
        st.metric("Active Quantum Keys", "256", "12")
        st.metric("Key Refresh Rate", "98%", "2%")
        st.metric("Quantum Resistance", "High", "-")
        st.metric("Encryption Strength", "AES-256", "-")
        
        st.subheader("Alerts")
        st.markdown('<div class="security-alert">⚠️ 3 Failed Key Exchanges</div>', unsafe_allow_html=True)
        st.markdown('<div class="security-alert">🔒 Quantum Audit Required</div>', unsafe_allow_html=True)

def show_simulation_results():
    """Display simulation results and analysis"""
    
    st.title("📊 Simulation Results")
    
    # Scenario selection
    scenario = st.selectbox(
        "Select Scenario",
        ["Highway", "Urban Center", "City Intersection", "Custom Scenario"]
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Performance Metrics")
        
        metrics_data = {
            "Metric": ["Message Delivery Rate", "Latency", "Security Score", "Quantum Overhead"],
            "Value": ["98.5%", "45ms", "96%", "12%"],
            "Status": ["Excellent", "Good", "Good", "Acceptable"]
        }
        
        metrics_df = pd.DataFrame(metrics_data)
        st.dataframe(metrics_df, use_container_width=True)
    
    with col2:
        st.subheader("Security Analysis")
        
        security_data = {
            "Attack Type": ["Quantum Brute Force", "Man-in-the-Middle", "Replay Attack", "DoS"],
            "Prevention": ["100%", "98%", "99%", "95%"],
            "Impact": ["Low", "Medium", "Low", "High"]
        }
        
        security_df = pd.DataFrame(security_data)
        st.dataframe(security_df, use_container_width=True)
    
    # Simulation visualization
    st.subheader("Network Performance")
    
    # Create sample network performance data
    performance_data = {
        "Time": range(100),
        "Throughput": [i * 0.5 + 10 for i in range(100)],
        "Latency": [50 - i * 0.2 for i in range(100)],
        "Packet Loss": [max(0, i * 0.01 - 0.5) for i in range(100)]
    }
    
    perf_df = pd.DataFrame(performance_data)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=perf_df["Time"], y=perf_df["Throughput"],
                            name="Throughput (Mbps)", line=dict(color='green')))
    fig.add_trace(go.Scatter(x=perf_df["Time"], y=perf_df["Latency"],
                            name="Latency (ms)", line=dict(color='red'), yaxis="y2"))
    
    fig.update_layout(
        title="Network Performance Over Time",
        xaxis_title="Time (seconds)",
        yaxis_title="Throughput (Mbps)",
        yaxis2=dict(title="Latency (ms)", overlaying="y", side="right"),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_security_analysis():
    """Display security analysis and threat monitoring"""
    
    st.title("📈 Security Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Threat Detection")
        
        threats = {
            "Timestamp": ["2024-01-01 10:30:00", "2024-01-01 10:35:22", "2024-01-01 10:40:15"],
            "Threat Type": ["Suspicious Key Exchange", "Potential MITM", "Unusual Traffic Pattern"],
            "Severity": ["Medium", "High", "Low"],
            "Status": ["Investigated", "Under Review", "Monitoring"]
        }
        
        threats_df = pd.DataFrame(threats)
        st.dataframe(threats_df, use_container_width=True)
    
    with col2:
        st.subheader("Security Score Over Time")
        
        # Security score visualization
        score_data = {
            "Date": pd.date_range("2024-01-01", periods=30, freq="D"),
            "Security_Score": [85 + i * 0.5 + (i % 7) for i in range(30)]
        }
        
        score_df = pd.DataFrame(score_data)
        
        fig = px.line(score_df, x="Date", y="Security_Score",
                     title="Security Score Trend",
                     labels={"Security_Score": "Security Score (%)"})
        fig.update_traces(line_color='#00cc96', line_width=3)
        fig.update_layout(height=300)
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Quantum resistance analysis
    st.subheader("Quantum Resistance Analysis")
    
    resistance_data = {
        "Algorithm": ["RSA-2048", "ECDSA", "Kyber-1024", "Dilithium", "Falcon"],
        "Classical Security": ["112 bits", "128 bits", ">128 bits", ">128 bits", ">128 bits"],
        "Quantum Security": ["Broken", "Broken", "Secure", "Secure", "Secure"],
        "Performance": ["Fast", "Very Fast", "Good", "Acceptable", "Slow"]
    }
    
    resistance_df = pd.DataFrame(resistance_data)
    st.dataframe(resistance_df, use_container_width=True)

def show_configuration():
    """Display system configuration interface"""
    
    st.title("⚙️ System Configuration")
    
    tab1, tab2, tab3 = st.tabs(["Quantum Settings", "Network Config", "Simulation Parameters"])
    
    with tab1:
        st.subheader("Quantum Security Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            key_size = st.selectbox(
                "Quantum Key Size",
                [128, 192, 256, 512],
                index=2
            )
            
            algorithm = st.selectbox(
                "PQC Algorithm",
                ["Kyber-1024", "Dilithium-5", "Falcon-1024", "SPHINCS+"]
            )
            
            key_refresh = st.slider(
                "Key Refresh Interval (minutes)",
                min_value=1,
                max_value=120,
                value=60
            )
        
        with col2:
            enable_quantum = st.checkbox("Enable Quantum Security", value=True)
            enable_hybrid = st.checkbox("Enable Hybrid Cryptography", value=True)
            auto_key_rotation = st.checkbox("Automatic Key Rotation", value=True)
        
        if st.button("Save Quantum Configuration", use_container_width=True):
            st.success("Quantum configuration saved successfully!")
    
    with tab2:
        st.subheader("Network Configuration")
        
        max_vehicles = st.number_input("Maximum Vehicles", min_value=10, max_value=1000, value=100)
        max_rsus = st.number_input("Maximum RSUs", min_value=1, max_value=50, value=10)
        simulation_duration = st.number_input("Simulation Duration (seconds)", min_value=60, max_value=3600, value=1800)
        
        if st.button("Save Network Configuration", use_container_width=True):
            st.success("Network configuration saved successfully!")
    
    with tab3:
        st.subheader("Simulation Parameters")
        
        scenario_file = st.file_uploader("Upload Scenario File", type=['json'])
        
        traffic_density = st.select_slider(
            "Traffic Density",
            options=["Very Low", "Low", "Medium", "High", "Very High"],
            value="Medium"
        )
        
        security_level = st.select_slider(
            "Security Level",
            options=["Basic", "Standard", "Enhanced", "Maximum"],
            value="Enhanced"
        )
        
        if st.button("Start Simulation", use_container_width=True):
            st.success("Simulation started successfully!")

if __name__ == "__main__":
    main()
