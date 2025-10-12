#!/usr/bin/env python3
"""
Post-Quantum Cryptography Manager for V2X Communications
Handles PQC algorithm evaluation and integration
"""

import asyncio
import logging
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import statistics

try:
    import liboqs
except ImportError:
    print("Warning: liboqs not available, using mock implementation")
    liboqs = None

class PQCAlgorithm(Enum):
    KYBER512 = "Kyber512"
    KYBER768 = "Kyber768" 
    KYBER1024 = "Kyber1024"
    DILITHIUM2 = "Dilithium2"
    DILITHIUM3 = "Dilithium3"
    DILITHIUM5 = "Dilithium5"
    FALCON512 = "Falcon512"
    FALCON1024 = "Falcon1024"
    SPHINCS128 = "SPHINCS+-SHA2-128s"
    SPHINCS192 = "SPHINCS+-SHA2-192s"

@dataclass
class PQCPerformance:
    algorithm: PQCAlgorithm
    key_gen_time: float
    encryption_time: float
    decryption_time: float
    signature_time: float
    verification_time: float
    public_key_size: int
    private_key_size: int
    ciphertext_size: int
    signature_size: int
    security_level: int  # bits of security

@dataclass
class CryptoAnalysis:
    algorithm: str
    classical_security: int
    quantum_security: int
    migration_priority: str
    risk_level: str

class PQCManager:
    """
    Manager for Post-Quantum Cryptography operations in V2X networks
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.supported_algorithms = self._get_supported_algorithms()
        self.performance_data = {}
        self.security_assessments = {}
        
        self._initialize_liboqs()
    
    def _get_supported_algorithms(self) -> List[PQCAlgorithm]:
        """Get list of supported PQC algorithms"""
        return [
            PQCAlgorithm.KYBER512,
            PQCAlgorithm.KYBER768,
            PQCAlgorithm.DILITHIUM2,
            PQCAlgorithm.DILITHIUM3,
            PQCAlgorithm.FALCON512,
            PQCAlgorithm.SPHINCS128
        ]
    
    def _initialize_liboqs(self):
        """Initialize liboqs library"""
        if liboqs is None:
            self.logger.warning("liboqs not available, using mock implementation")
            return
        
        try:
            # Test liboqs availability
            with liboqs.KeyEncapsulation('Kyber512') as kem:
                self.logger.info("liboqs initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize liboqs: {e}")
    
    async def evaluate_pqc_performance(self, message_sizes: List[int] = None) -> Dict[PQCAlgorithm, PQCPerformance]:
        """
        Comprehensive performance evaluation of PQC algorithms
        """
        if message_sizes is None:
            message_sizes = [64, 128, 256, 512, 1024]  # Typical V2X message sizes
        
        self.logger.info("Starting PQC performance evaluation...")
        
        results = {}
        
        for algorithm in self.supported_algorithms:
            self.logger.info(f"Evaluating {algorithm.value}...")
            
            try:
                performance = await self._benchmark_algorithm(algorithm, message_sizes)
                results[algorithm] = performance
                self.performance_data[algorithm] = performance
                
                self.logger.info(f"Completed {algorithm.value}: "
                               f"key_gen={performance.key_gen_time*1000:.2f}ms, "
                               f"encrypt={performance.encryption_time*1000:.2f}ms")
                               
            except Exception as e:
                self.logger.error(f"Failed to evaluate {algorithm.value}: {e}")
                continue
        
        # Store results
        await self._save_performance_data(results)
        
        return results
    
    async def _benchmark_algorithm(self, algorithm: PQCAlgorithm, message_sizes: List[int]) -> PQCPerformance:
        """Benchmark a specific PQC algorithm"""
        if liboqs is None:
            return await self._mock_benchmark(algorithm, message_sizes)
        
        algorithm_name = algorithm.value
        
        # Benchmark Key Encapsulation Mechanisms (KEM)
        if algorithm_name.startswith('Kyber'):
            return await self._benchmark_kem(algorithm_name, message_sizes)
        
        # Benchmark Signature Schemes
        elif algorithm_name.startswith('Dilithium') or algorithm_name.startswith('Falcon'):
            return await self._benchmark_signature(algorithm_name, message_sizes)
        
        # Benchmark Stateless Hash-Based Signatures
        elif algorithm_name.startswith('SPHINCS'):
            return await self._benchmark_sphincs(algorithm_name, message_sizes)
        
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm_name}")
    
    async def _benchmark_kem(self, algorithm: str, message_sizes: List[int]) -> PQCPerformance:
        """Benchmark Key Encapsulation Mechanism"""
        key_gen_times = []
        encap_times = []
        decap_times = []
        
        with liboqs.KeyEncapsulation(algorithm) as client:
            with liboqs.KeyEncapsulation(algorithm) as server:
                # Key generation benchmark
                for _ in range(100):
                    start_time = time.perf_counter()
                    public_key = server.generate_keypair()
                    key_gen_times.append(time.perf_counter() - start_time)
                
                # Encapsulation/Decapsulation benchmark
                for msg_size in message_sizes:
                    test_message = b'A' * msg_size
                    
                    for _ in range(50):
                        # Encapsulation
                        start_time = time.perf_counter()
                        ciphertext, shared_secret_server = server.encap_secret(public_key)
                        encap_times.append(time.perf_counter() - start_time)
                        
                        # Decapsulation
                        start_time = time.perf_counter()
                        shared_secret_client = client.decap_secret(ciphertext)
                        decap_times.append(time.perf_counter() - start_time)
                        
                        # Verify correctness
                        assert shared_secret_server == shared_secret_client
        
        return PQCPerformance(
            algorithm=PQCAlgorithm(algorithm),
            key_gen_time=statistics.median(key_gen_times),
            encryption_time=statistics.median(encap_times),
            decryption_time=statistics.median(decap_times),
            signature_time=0.0,  # KEM doesn't provide signatures
            verification_time=0.0,
            public_key_size=len(public_key) if 'public_key' in locals() else 0,
            private_key_size=0,  # Would need to access internal state
            ciphertext_size=len(ciphertext) if 'ciphertext' in locals() else 0,
            signature_size=0,
            security_level=self._get_security_level(algorithm)
        )
    
    async def _benchmark_signature(self, algorithm: str, message_sizes: List[int]) -> PQCPerformance:
        """Benchmark digital signature scheme"""
        key_gen_times = []
        sign_times = []
        verify_times = []
        
        with liboqs.Signature(algorithm) as signer:
            # Key generation benchmark
            for _ in range(100):
                start_time = time.perf_counter()
                public_key = signer.generate_keypair()
                key_gen_times.append(time.perf_counter() - start_time)
            
            # Signing/Verification benchmark
            for msg_size in message_sizes:
                message = b'X' * msg_size
                
                for _ in range(50):
                    # Signing
                    start_time = time.perf_counter()
                    signature = signer.sign(message)
                    sign_times.append(time.perf_counter() - start_time)
                    
                    # Verification
                    start_time = time.perf_counter()
                    is_valid = signer.verify(message, signature)
                    verify_times.append(time.perf_counter() - start_time)
                    
                    assert is_valid, "Signature verification failed"
        
        return PQCPerformance(
            algorithm=PQCAlgorithm(algorithm),
            key_gen_time=statistics.median(key_gen_times),
            encryption_time=0.0,  # Signature scheme doesn't provide encryption
            decryption_time=0.0,
            signature_time=statistics.median(sign_times),
            verification_time=statistics.median(verify_times),
            public_key_size=len(public_key) if 'public_key' in locals() else 0,
            private_key_size=0,
            ciphertext_size=0,
            signature_size=len(signature) if 'signature' in locals() else 0,
            security_level=self._get_security_level(algorithm)
        )
    
    async def _benchmark_sphincs(self, algorithm: str, message_sizes: List[int]) -> PQCPerformance:
        """Benchmark SPHINCS+ signature scheme"""
        # SPHINCS+ is also a signature scheme
        return await self._benchmark_signature(algorithm, message_sizes)
    
    async def _mock_benchmark(self, algorithm: PQCAlgorithm, message_sizes: List[int]) -> PQCPerformance:
        """Mock benchmark for testing without liboqs"""
        # Simulate realistic performance characteristics
        base_times = {
            PQCAlgorithm.KYBER512: (0.001, 0.0005, 0.0006, 0.0, 0.0),
            PQCAlgorithm.KYBER768: (0.0015, 0.0007, 0.0008, 0.0, 0.0),
            PQCAlgorithm.DILITHIUM2: (0.002, 0.0, 0.0, 0.001, 0.0003),
            PQCAlgorithm.DILITHIUM3: (0.003, 0.0, 0.0, 0.0015, 0.0004),
            PQCAlgorithm.FALCON512: (0.005, 0.0, 0.0, 0.0008, 0.0002),
            PQCAlgorithm.SPHINCS128: (0.001, 0.0, 0.0, 0.002, 0.001)
        }
        
        key_gen, enc, dec, sig, ver = base_times.get(algorithm, (0.001, 0.0005, 0.0006, 0.001, 0.0003))
        
        return PQCPerformance(
            algorithm=algorithm,
            key_gen_time=key_gen,
            encryption_time=enc,
            decryption_time=dec,
            signature_time=sig,
            verification_time=ver,
            public_key_size=800,  # Approximate sizes
            private_key_size=1600,
            ciphertext_size=768,
            signature_size=2000,
            security_level=self._get_security_level(algorithm.value)
        )
    
    def _get_security_level(self, algorithm: str) -> int:
        """Get security level in bits for an algorithm"""
        security_levels = {
            'Kyber512': 128,
            'Kyber768': 192,
            'Kyber1024': 256,
            'Dilithium2': 128,
            'Dilithium3': 192,
            'Dilithium5': 256,
            'Falcon512': 128,
            'Falcon1024': 256,
            'SPHINCS+-SHA2-128s': 128,
            'SPHINCS+-SHA2-192s': 192
        }
        return security_levels.get(algorithm, 128)
    
    async def analyze_crypto_migration(self, current_algorithms: List[str]) -> List[CryptoAnalysis]:
        """
        Analyze cryptographic migration from classical to PQC
        """
        analysis_results = []
        
        for current_alg in current_algorithms:
            # Assess classical security
            classical_sec = self._assess_classical_security(current_alg)
            
            # Assess quantum security
            quantum_sec = self._assess_quantum_security(current_alg)
            
            # Determine migration priority
            priority = self._determine_migration_priority(classical_sec, quantum_sec)
            
            # Determine risk level
            risk = self._determine_risk_level(quantum_sec)
            
            analysis = CryptoAnalysis(
                algorithm=current_alg,
                classical_security=classical_sec,
                quantum_security=quantum_sec,
                migration_priority=priority,
                risk_level=risk
            )
            
            analysis_results.append(analysis)
            self.security_assessments[current_alg] = analysis
        
        return analysis_results
    
    def _assess_classical_security(self, algorithm: str) -> int:
        """Assess classical security of an algorithm"""
        classical_security = {
            'RSA-2048': 112,
            'RSA-3072': 128,
            'RSA-4096': 152,
            'ECC-256': 128,
            'ECC-384': 192,
            'AES-128': 128,
            'AES-256': 256
        }
        return classical_security.get(algorithm, 0)
    
    def _assess_quantum_security(self, algorithm: str) -> int:
        """Assess quantum security of an algorithm"""
        # Quantum security is typically sqrt of classical for symmetric,
        # and significantly reduced for asymmetric
        classical_sec = self._assess_classical_security(algorithm)
        
        if algorithm.startswith('AES'):
            # Grover's algorithm: security is sqrt
            return classical_sec // 2
        elif algorithm.startswith('RSA') or algorithm.startswith('ECC'):
            # Shor's algorithm: security is polynomial
            return 0  # Effectively broken by quantum computers
        else:
            return classical_sec
    
    def _determine_migration_priority(self, classical_sec: int, quantum_sec: int) -> str:
        """Determine migration priority based on security assessment"""
        if quantum_sec == 0:
            return "CRITICAL"
        elif quantum_sec < 128:
            return "HIGH"
        elif quantum_sec < 192:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _determine_risk_level(self, quantum_sec: int) -> str:
        """Determine risk level based on quantum security"""
        if quantum_sec == 0:
            return "EXTREME"
        elif quantum_sec < 128:
            return "HIGH"
        elif quantum_sec < 192:
            return "MEDIUM"
        else:
            return "LOW"
    
    async def recommend_pqc_algorithms(self, use_case: str, constraints: Dict) -> List[PQCAlgorithm]:
        """
        Recommend PQC algorithms based on use case and constraints
        """
        recommendations = []
        
        # Filter algorithms based on constraints
        candidate_algorithms = self.supported_algorithms.copy()
        
        # Apply performance constraints
        if 'max_latency' in constraints:
            candidate_algorithms = [
                alg for alg in candidate_algorithms
                if self._meets_latency_requirement(alg, constraints['max_latency'])
            ]
        
        # Apply size constraints
        if 'max_key_size' in constraints:
            candidate_algorithms = [
                alg for alg in candidate_algorithms
                if self._meets_size_requirement(alg, constraints['max_key_size'])
            ]
        
        # Apply security constraints
        if 'min_security' in constraints:
            candidate_algorithms = [
                alg for alg in candidate_algorithms
                if self._get_security_level(alg.value) >= constraints['min_security']
            ]
        
        # Rank by suitability for use case
        ranked_algorithms = self._rank_algorithms_for_use_case(candidate_algorithms, use_case)
        
        return ranked_algorithms[:3]  # Return top 3 recommendations
    
    def _meets_latency_requirement(self, algorithm: PQCAlgorithm, max_latency: float) -> bool:
        """Check if algorithm meets latency requirement"""
        if algorithm in self.performance_data:
            perf = self.performance_data[algorithm]
            total_operation_time = perf.signature_time + perf.verification_time
            return total_operation_time <= max_latency
        
        # Conservative estimate if no performance data
        return True
    
    def _meets_size_requirement(self, algorithm: PQCAlgorithm, max_size: int) -> bool:
        """Check if algorithm meets size requirement"""
        if algorithm in self.performance_data:
            perf = self.performance_data[algorithm]
            return perf.public_key_size <= max_size
        
        # Conservative estimate
        return True
    
    def _rank_algorithms_for_use_case(self, algorithms: List[PQCAlgorithm], use_case: str) -> List[PQCAlgorithm]:
        """Rank algorithms based on suitability for use case"""
        use_case_weights = {
            'v2x_safety': {'performance': 0.6, 'security': 0.4, 'size': 0.2},
            'v2x_efficiency': {'performance': 0.8, 'security': 0.3, 'size': 0.3},
            'v2x_security': {'performance': 0.3, 'security': 0.8, 'size': 0.1}
        }
        
        weights = use_case_weights.get(use_case, {'performance': 0.5, 'security': 0.5, 'size': 0.2})
        
        scored_algorithms = []
        
        for algorithm in algorithms:
            score = 0
            
            # Performance score (lower is better)
            if algorithm in self.performance_data:
                perf = self.performance_data[algorithm]
                perf_score = 1.0 / (perf.signature_time + perf.verification_time + 0.001)
                score += weights['performance'] * perf_score
            
            # Security score (higher is better)
            security_score = self._get_security_level(algorithm.value) / 256.0
            score += weights['security'] * security_score
            
            # Size score (smaller is better)
            if algorithm in self.performance_data:
                size_score = 1.0 / (self.performance_data[algorithm].public_key_size + 1)
                score += weights['size'] * size_score
            
            scored_algorithms.append((algorithm, score))
        
        # Sort by score descending
        scored_algorithms.sort(key=lambda x: x[1], reverse=True)
        
        return [alg for alg, score in scored_algorithms]
    
    async def _save_performance_data(self, performance_data: Dict[PQCAlgorithm, PQCPerformance]):
        """Save performance data to file"""
        import json
        import os
        
        os.makedirs('data/performance', exist_ok=True)
        
        serializable_data = {}
        for alg, perf in performance_data.items():
            serializable_data[alg.value] = {
                'key_gen_time': perf.key_gen_time,
                'encryption_time': perf.encryption_time,
                'decryption_time': perf.decryption_time,
                'signature_time': perf.signature_time,
                'verification_time': perf.verification_time,
                'public_key_size': perf.public_key_size,
                'private_key_size': perf.private_key_size,
                'ciphertext_size': perf.ciphertext_size,
                'signature_size': perf.signature_size,
                'security_level': perf.security_level
            }
        
        timestamp = int(time.time())
        filename = f'data/performance/pqc_benchmark_{timestamp}.json'
        
        with open(filename, 'w') as f:
            json.dump(serializable_data, f, indent=2)
        
        self.logger.info(f"Performance data saved to {filename}")
