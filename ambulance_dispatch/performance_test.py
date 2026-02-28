"""
Performance Testing Script for D795 Ambulance Dispatch System
Student ID: 012687096

This script runs both prototypes 10 times each and collects performance data
for comparison between Dijkstra's and A* algorithms.
"""

import os
import sys
import time
import csv
import statistics
from typing import List, Dict


def run_prototype(prototype_path: str, prototype_name: str) -> Dict:
    """Run a prototype and capture performance data"""
    print(f"\nRunning {prototype_name}...")
    
    # Change to prototype directory
    original_dir = os.getcwd()
    os.chdir(prototype_path)
    
    try:
        # Import and run the prototype
        if "dijkstra" in prototype_name.lower():
            from ambulance_dispatch_dijkstra import AmbulanceDispatchSystem
        else:
            from ambulance_dispatch_astar import AmbulanceDispatchSystem
            
        # Create system instance
        system = AmbulanceDispatchSystem()
        
        # Record start time
        start_time = time.perf_counter()
        
        # Run simulation
        system.load_data()
        system.process_calls()
        
        # Record end time
        end_time = time.perf_counter()
        
        # Calculate total execution time
        total_execution_time = end_time - start_time
        
        # Get route finding performance data
        route_finding_times = system.route_finding_times
        avg_route_time = statistics.mean(route_finding_times) if route_finding_times else 0
        total_route_time = sum(route_finding_times) if route_finding_times else 0
        
        return {
            'prototype_name': prototype_name,
            'total_execution_time': total_execution_time,
            'avg_route_finding_time': avg_route_time,
            'total_route_finding_time': total_route_time,
            'route_calculations': len(route_finding_times),
            'calls_processed': system.total_calls_processed
        }
        
    except Exception as e:
        print(f"Error running {prototype_name}: {e}")
        return None
    finally:
        # Return to original directory
        os.chdir(original_dir)


def run_performance_tests():
    """Run performance tests for both prototypes"""
    print("D795 Ambulance Dispatch System - Performance Testing")
    print("=" * 60)
    
    # Define prototype paths
    dijkstra_path = r"c:\Users\Admin\D795\012687096_D795_PT1"
    astar_path = r"c:\Users\Admin\D795\012687096_D795_PT2"
    
    # Results storage
    dijkstra_results = []
    astar_results = []
    
    # Run Dijkstra prototype 10 times
    print("\n=== Testing Dijkstra's Algorithm (10 runs) ===")
    for i in range(10):
        print(f"Run {i+1}/10", end="... ")
        result = run_prototype(dijkstra_path, f"Dijkstra Run {i+1}")
        if result:
            dijkstra_results.append(result)
            print(f"Completed in {result['total_execution_time']:.4f}s")
        else:
            print("Failed")
    
    # Run A* prototype 10 times
    print("\n=== Testing A* Algorithm (10 runs) ===")
    for i in range(10):
        print(f"Run {i+1}/10", end="... ")
        result = run_prototype(astar_path, f"A* Run {i+1}")
        if result:
            astar_results.append(result)
            print(f"Completed in {result['total_execution_time']:.4f}s")
        else:
            print("Failed")
    
    # Calculate statistics
    print("\n=== Performance Analysis ===")
    
    if dijkstra_results:
        dijkstra_exec_times = [r['total_execution_time'] for r in dijkstra_results]
        dijkstra_route_times = [r['avg_route_finding_time'] for r in dijkstra_results]
        
        print(f"\nDijkstra's Algorithm Results ({len(dijkstra_results)} runs):")
        print(f"  Average total execution time: {statistics.mean(dijkstra_exec_times):.6f} seconds")
        print(f"  Min total execution time: {min(dijkstra_exec_times):.6f} seconds")
        print(f"  Max total execution time: {max(dijkstra_exec_times):.6f} seconds")
        print(f"  Average route finding time: {statistics.mean(dijkstra_route_times):.6f} seconds")
        print(f"  Standard deviation: {statistics.stdev(dijkstra_exec_times):.6f} seconds")
    
    if astar_results:
        astar_exec_times = [r['total_execution_time'] for r in astar_results]
        astar_route_times = [r['avg_route_finding_time'] for r in astar_results]
        
        print(f"\nA* Algorithm Results ({len(astar_results)} runs):")
        print(f"  Average total execution time: {statistics.mean(astar_exec_times):.6f} seconds")
        print(f"  Min total execution time: {min(astar_exec_times):.6f} seconds")
        print(f"  Max total execution time: {max(astar_exec_times):.6f} seconds")
        print(f"  Average route finding time: {statistics.mean(astar_route_times):.6f} seconds")
        print(f"  Standard deviation: {statistics.stdev(astar_exec_times):.6f} seconds")
    
    # Comparison
    if dijkstra_results and astar_results:
        dijkstra_avg = statistics.mean(dijkstra_exec_times)
        astar_avg = statistics.mean(astar_exec_times)
        
        print(f"\n=== Algorithm Comparison ===")
        print(f"Dijkstra average execution time: {dijkstra_avg:.6f} seconds")
        print(f"A* average execution time: {astar_avg:.6f} seconds")
        
        if dijkstra_avg < astar_avg:
            improvement = ((astar_avg - dijkstra_avg) / astar_avg) * 100
            print(f"Dijkstra is {improvement:.2f}% faster than A*")
        else:
            improvement = ((dijkstra_avg - astar_avg) / dijkstra_avg) * 100
            print(f"A* is {improvement:.2f}% faster than Dijkstra")
    
    # Save results to CSV
    save_performance_results(dijkstra_results, astar_results)
    
    print("\nPerformance testing completed!")


def save_performance_results(dijkstra_results: List[Dict], astar_results: List[Dict]):
    """Save performance results to CSV file"""
    results_file = r"c:\Users\Admin\D795\performance_test_results.csv"
    
    try:
        with open(results_file, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['Algorithm', 'Run', 'Total_Execution_Time', 'Avg_Route_Finding_Time', 
                         'Total_Route_Finding_Time', 'Route_Calculations', 'Calls_Processed']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            # Write Dijkstra results
            for i, result in enumerate(dijkstra_results, 1):
                writer.writerow({
                    'Algorithm': 'Dijkstra',
                    'Run': i,
                    'Total_Execution_Time': f"{result['total_execution_time']:.6f}",
                    'Avg_Route_Finding_Time': f"{result['avg_route_finding_time']:.6f}",
                    'Total_Route_Finding_Time': f"{result['total_route_finding_time']:.6f}",
                    'Route_Calculations': result['route_calculations'],
                    'Calls_Processed': result['calls_processed']
                })
            
            # Write A* results
            for i, result in enumerate(astar_results, 1):
                writer.writerow({
                    'Algorithm': 'A*',
                    'Run': i,
                    'Total_Execution_Time': f"{result['total_execution_time']:.6f}",
                    'Avg_Route_Finding_Time': f"{result['avg_route_finding_time']:.6f}",
                    'Total_Route_Finding_Time': f"{result['total_route_finding_time']:.6f}",
                    'Route_Calculations': result['route_calculations'],
                    'Calls_Processed': result['calls_processed']
                })
        
        print(f"\nPerformance results saved to: {results_file}")
        
    except Exception as e:
        print(f"Error saving performance results: {e}")


if __name__ == "__main__":
    run_performance_tests()