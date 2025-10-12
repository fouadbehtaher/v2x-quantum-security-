#!/bin/bash

set -e  # Exit on any error

echo "🚀 Setting up V2X Quantum Security Simulation Environment..."
echo "=========================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check system requirements
check_requirements() {
    log_info "Checking system requirements..."
    
    # Check Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        log_success "Python $PYTHON_VERSION found"
    else
        log_error "Python 3.11+ is required but not found"
        exit 1
    fi
    
    # Check Docker
    if command -v docker &> /dev/null; then
        log_success "Docker found"
    else
        log_warning "Docker not found - some features may be limited"
    fi
    
    # Check RAM
    TOTAL_RAM=$(free -g | awk '/^Mem:/{print $2}')
    if [ "$TOTAL_RAM" -lt 8 ]; then
        log_warning "Recommended RAM is 8GB+, found ${TOTAL_RAM}GB"
    else
        log_success "System RAM: ${TOTAL_RAM}GB"
    fi
}

# Create virtual environment
create_venv() {
    log_info "Creating Python virtual environment..."
    
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        log_success "Virtual environment created"
    else
        log_info "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
}

# Install Python dependencies
install_dependencies() {
    log_info "Installing Python dependencies..."
    
    pip install --upgrade pip
    
    # Install core requirements
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        log_success "Core dependencies installed"
    else
        log_error "requirements.txt not found"
        exit 1
    fi
    
    # Install development dependencies (optional)
    if [ -f "requirements-dev.txt" ]; then
        pip install -r requirements-dev.txt
        log_success "Development dependencies installed"
    fi
}

# Setup quantum computing environment
setup_quantum_environment() {
    log_info "Setting up quantum computing environment..."
    
    # Install Qiskit and quantum dependencies
    pip install qiskit qiskit-aer cirq
    
    # Check if IBM Quantum token is provided
    if [ -n "$IBM_QUANTUM_TOKEN" ]; then
        log_info "Setting up IBM Quantum account..."
        python3 -c "
from qiskit_ibm_runtime import QiskitRuntimeService
QiskitRuntimeService.save_account('$IBM_QUANTUM_TOKEN', overwrite=True)
        "
        log_success "IBM Quantum account configured"
    else
        log_warning "IBM Quantum token not provided - using local simulators only"
    fi
}

# Setup PQC libraries
setup_pqc_libraries() {
    log_info "Setting up Post-Quantum Cryptography libraries..."
    
    # Try to install liboqs Python bindings
    if pip install pyoqs; then
        log_success "liboqs Python bindings installed"
    else
        log_warning "Failed to install liboqs Python bindings - using mock implementation"
    fi
    
    # Clone and build liboqs from source (optional)
    log_info "Building liboqs from source..."
    if [ ! -d "third_party/liboqs" ]; then
        git clone https://github.com/open-quantum-safe/liboqs.git third_party/liboqs
        cd third_party/liboqs
        mkdir build && cd build
        cmake -DCMAKE_INSTALL_PREFIX=../../.. ..
        make -j$(nproc)
        make install
        cd ../../..
        log_success "liboqs built from source"
    else
        log_info "liboqs already exists in third_party/"
    fi
}

# Setup simulation frameworks
setup_simulation_frameworks() {
    log_info "Setting up simulation frameworks..."
    
    # Check for OMNeT++
    if command -v opp_config &> /dev/null; then
        log_success "OMNeT++ found"
    else
        log_warning "OMNeT++ not found - please install manually for full simulation capabilities"
        log_info "See docs/deployment/ for installation instructions"
    fi
    
    # Check for SUMO
    if command -v sumo &> /dev/null; then
        log_success "SUMO found"
    else
        log_warning "SUMO not found - please install manually for traffic simulation"
    fi
}

# Build Docker images
build_docker_images() {
    log_info "Building Docker images..."
    
    if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
        docker-compose build --parallel
        log_success "Docker images built successfully"
    else
        log_warning "Docker not available - skipping containerization"
    fi
}

# Run health checks
run_health_checks() {
    log_info "Running health checks..."
    
    # Test Python imports
    if python3 -c "
import numpy, pandas, qiskit
print('✅ Core imports successful')
try:
    import liboqs
    print('✅ liboqs import successful')
except ImportError:
    print('⚠️ liboqs not available - using mock implementation')
    "; then
        log_success "Python environment check passed"
    else
        log_error "Python environment check failed"
        exit 1
    fi
    
    # Test basic functionality
    if python3 -c "
from src.core.simulation_engine import V2XQuantumSimulationEngine
print('✅ Simulation engine import successful')
    "; then
        log_success "Module imports successful"
    else
        log_error "Module imports failed"
        exit 1
    fi
}

# Create necessary directories
create_directories() {
    log_info "Creating necessary directories..."
    
    directories=(
        "data/raw"
        "data/processed" 
        "data/results"
        "logs"
        "config"
        "assets/images"
        "assets/videos"
    )
    
    for dir in "${directories[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            log_success "Created directory: $dir"
        fi
    done
}

# Main setup function
main() {
    echo
    log_info "Starting V2X Quantum Security environment setup..."
    echo
    
    check_requirements
    create_venv
    install_dependencies
    setup_quantum_environment
    setup_pqc_libraries
    setup_simulation_frameworks
    build_docker_images
    create_directories
    run_health_checks
    
    echo
    log_success "🎉 V2X Quantum Security environment setup completed successfully!"
    echo
    log_info "📚 Next steps:"
    log_info "   1. Review configuration in config/"
    log_info "   2. Run tests: pytest tests/ -v"
    log_info "   3. Start simulation: python scripts/run_simulation.py"
    log_info "   4. Launch dashboard: streamlit run src/ui/dashboard.py"
    echo
    log_info "💡 For detailed usage, see docs/tutorials/getting-started.md"
    echo
}

# Run main function
main "$@"
