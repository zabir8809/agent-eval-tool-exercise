#!/usr/bin/env python3
"""
Evaluation runner for the AI Travel Agent.

This script provides a comprehensive evaluation pipeline using built-in evaluation logic.
It can:
1. Run evaluations on logged test data
2. Generate evaluation reports
3. Provide insights and recommendations
4. Create sample test cases for evaluation

Usage:
    python run_evaluation.py --run-eval
    python run_evaluation.py --generate-sample-data
    python run_evaluation.py --analyze-results
"""

import argparse
import json
import os
from eval_utils import TravelAgentEvaluator

def generate_sample_test_data():
    """Generate sample test data for evaluation."""
    sample_cases = [
        {
            "destination": "Paris",
            "num_days": 3,
            "description": "Short city break in Paris"
        },
        {
            "destination": "Tokyo",
            "num_days": 7,
            "description": "Week-long trip to Tokyo"
        },
        {
            "destination": "New York",
            "num_days": 5,
            "description": "5-day New York adventure"
        },
        {
            "destination": "London",
            "num_days": 4,
            "description": "4-day London exploration"
        },
        {
            "destination": "Sydney",
            "num_days": 6,
            "description": "6-day Sydney trip"
        }
    ]
    
    # Create test data file
    with open("eval_data.jsonl", "w") as f:
        for case in sample_cases:
            test_case = {
                "input": {
                    "destination": case["destination"],
                    "num_days": case["num_days"]
                },
                "description": case["description"]
            }
            f.write(json.dumps(test_case) + "\n")
    
    print(f"Generated sample test data with {len(sample_cases)} cases")
    return "eval_data.jsonl"

def run_comprehensive_evaluation():
    """Run a comprehensive evaluation using built-in evaluation logic."""
    evaluator = TravelAgentEvaluator()
    
    print("🚀 Starting comprehensive evaluation...")
    
    # Generate sample test data if no logged data exists
    if not os.path.exists("logs.jsonl") or os.path.getsize("logs.jsonl") == 0:
        print("📝 No logged data found, generating sample test data...")
        test_data_file = generate_sample_test_data()
    else:
        print("📊 Using existing logged data for evaluation...")
        test_data_file = evaluator.convert_logs_to_test_data()
    
    # Run evaluation
    print("🔍 Running built-in evaluation...")
    results = evaluator.run_evaluation(test_data_file=test_data_file)
    
    if results is None:
        print("❌ Evaluation failed. Check test data and agent configuration.")
        return None
    
    # Analyze results
    print("📈 Analyzing evaluation results...")
    analysis = evaluator.analyze_results(results)
    
    # Save results to file for later analysis
    with open("evaluation_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("💾 Saved evaluation results to evaluation_results.json")
    
    # Print summary
    print("\n" + "="*50)
    print("📊 EVALUATION SUMMARY")
    print("="*50)
    print(f"Total Tests: {analysis['summary']['total_tests']}")
    print(f"Passed: {analysis['summary']['passed_tests']}")
    print(f"Failed: {analysis['summary']['failed_tests']}")
    
    if analysis['failed_cases']:
        print("\n❌ Failed Cases:")
        for case in analysis['failed_cases']:
            print(f"  - {case['test']}: Score {case['score']}")
    
    if analysis['insights']:
        print("\n💡 Insights:")
        for insight in analysis['insights']:
            print(f"  - {insight}")
    
    if analysis['recommendations']:
        print("\n🎯 Recommendations:")
        for rec in analysis['recommendations']:
            print(f"  - {rec}")
    
    return analysis

def analyze_existing_results():
    """Analyze existing evaluation results."""
    evaluator = TravelAgentEvaluator()
    
    # Check if results file exists
    if not os.path.exists("evaluation_results.json"):
        print("❌ No existing results found. Run evaluation first.")
        print("💡 To generate results, run: python run_evaluation.py --run-eval")
        return
    
    print("📊 Loading existing evaluation results...")
    with open("evaluation_results.json", "r") as f:
        results = json.load(f)
    
    analysis = evaluator.analyze_results(results)
    report_file = evaluator.generate_report(analysis)
    
    print(f"📄 Generated analysis report: {report_file}")
    
    # Print summary
    print("\n" + "="*50)
    print("📊 ANALYSIS SUMMARY")
    print("="*50)
    print(f"Total Tests: {analysis['summary']['total_tests']}")
    print(f"Passed: {analysis['summary']['passed_tests']}")
    print(f"Failed: {analysis['summary']['failed_tests']}")
    
    if analysis['failed_cases']:
        print("\n❌ Failed Cases:")
        for case in analysis['failed_cases']:
            print(f"  - {case['test']}: Score {case['score']}")
    
    if analysis['insights']:
        print("\n💡 Insights:")
        for insight in analysis['insights']:
            print(f"  - {insight}")
    
    if analysis['recommendations']:
        print("\n🎯 Recommendations:")
        for rec in analysis['recommendations']:
            print(f"  - {rec}")
    
    return analysis

def main():
    parser = argparse.ArgumentParser(description="AI Travel Agent Evaluation Runner")
    parser.add_argument("--run-eval", action="store_true", 
                       help="Run comprehensive evaluation")
    parser.add_argument("--generate-sample-data", action="store_true",
                       help="Generate sample test data")
    parser.add_argument("--analyze-results", action="store_true",
                       help="Analyze existing evaluation results")
    
    args = parser.parse_args()
    
    if args.generate_sample_data:
        generate_sample_test_data()
    elif args.analyze_results:
        analyze_existing_results()
    elif args.run_eval:
        run_comprehensive_evaluation()
    else:
        print("🤖 AI Travel Agent Evaluation Runner")
        print("\nAvailable commands:")
        print("  --run-eval              Run comprehensive evaluation")
        print("  --generate-sample-data  Generate sample test data")
        print("  --analyze-results       Analyze existing results")
        print("\nExample:")
        print("  python run_evaluation.py --run-eval")

if __name__ == "__main__":
    main() 