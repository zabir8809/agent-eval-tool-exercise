import json
import datetime
import os
from typing import Dict, Any, Optional

class TravelAgentEvaluator:
    """
    Comprehensive evaluation system for the AI Travel Agent using built-in evaluation logic.
    
    This class handles:
    - Logging agent interactions to JSONL format
    - Running built-in evaluations
    - Analyzing evaluation results
    - Generating insights and recommendations
    """
    
    def __init__(self, log_file: str = "logs.jsonl"):
        self.log_file = log_file
        self.ensure_log_file_exists()
    
    def ensure_log_file_exists(self):
        """Ensure the log file exists with proper headers."""
        if not os.path.exists(self.log_file):
            # Create empty file
            open(self.log_file, 'w').close()
    
    def log_interaction(self, 
                       user_input: Dict[str, Any],
                       planner_output: str,
                       researcher_output: Optional[str] = None,
                       metadata: Optional[Dict[str, Any]] = None):
        """
        Log an agent interaction to the JSONL file.
        
        Args:
            user_input: Dictionary containing destination and num_days
            planner_output: The cleaned itinerary output from the planner
            researcher_output: Optional researcher agent output
            metadata: Optional additional metadata (timestamps, agent steps, etc.)
        """
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user_input": user_input,
            "planner_output": planner_output,
            "researcher_output": researcher_output,
            "metadata": metadata or {}
        }
        
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
     
    def run_evaluation(self, test_data_file: str = None):
        """
        Run evaluation on logged test data using built-in evaluation logic.
        
        Args:
            test_data_file: Optional custom test data file
            
        Returns:
            Dictionary containing evaluation results
        """
        if not test_data_file:
            # Convert logged data to test format
            test_data_file = self.convert_logs_to_test_data()
        
        # Read test data
        test_cases = []
        with open(test_data_file, 'r') as f:
            for line in f:
                if line.strip():
                    test_cases.append(json.loads(line))
        
        if not test_cases:
            print("No test cases found")
            return None
        
        # Run built-in evaluation
        results = []
        for i, test_case in enumerate(test_cases):
            result = self._evaluate_single_case(test_case, i)
            results.append(result)
        
        return {
            "results": results,
            "summary": {
                "total_tests": len(results),
                "passed_tests": sum(1 for r in results if r.get("passed", False)),
                "failed_tests": sum(1 for r in results if not r.get("passed", False))
            }
        }
    
    def _evaluate_single_case(self, test_case: Dict[str, Any], case_index: int) -> Dict[str, Any]:
        """
        Evaluate a single test case using built-in logic.
        
        Args:
            test_case: Test case data
            case_index: Index of the test case
            
        Returns:
            Evaluation result dictionary
        """
        destination = test_case["input"]["destination"]
        num_days = test_case["input"]["num_days"]
        
        # Generate response using the agent
        try:
            response, _ = self._generate_response(destination, num_days)
        except Exception as e:
            return {
                "test": {"description": f"Test Case {case_index + 1}"},
                "passed": False,
                "score": 0.0,
                "details": {"error": str(e)}
            }
        
        # Run evaluations
        evaluations = []
        
        # 1. Answer Relevance (simplified)
        relevance_score = self._evaluate_relevance(destination, num_days, response)
        evaluations.append({
            "type": "answer-relevance",
            "passed": relevance_score >= 0.7,
            "score": relevance_score
        })
        
        # 2. Contains Required Elements
        contains_score = self._evaluate_contains(destination, response)
        evaluations.append({
            "type": "contains",
            "passed": contains_score >= 0.8,
            "score": contains_score
        })
        
        # 3. Quality Rubric
        quality_score = self._evaluate_quality(response, num_days)
        evaluations.append({
            "type": "llm-rubric",
            "passed": quality_score >= 0.7,
            "score": quality_score
        })
        
        # Overall result
        overall_passed = all(e["passed"] for e in evaluations)
        overall_score = sum(e["score"] for e in evaluations) / len(evaluations)
        
        return {
            "test": {"description": f"Test Case {case_index + 1}: {destination} for {num_days} days"},
            "passed": overall_passed,
            "score": overall_score,
            "details": {
                "evaluations": evaluations,
                "response": response[:500] + "..." if len(response) > 500 else response
            }
        }
    
    def _generate_response(self, destination: str, num_days: int) -> tuple:
        """
        Generate a response using the travel agent.
        
        Args:
            destination: Travel destination
            num_days: Number of days
            
        Returns:
            Tuple of (response, metadata)
        """
        # Import here to avoid circular imports
        from travel_agent import generate_itinerary
        return generate_itinerary(destination, num_days, enable_logging=False)
    
    def _evaluate_relevance(self, destination: str, num_days: int, response: str) -> float:
        """
        Evaluate answer relevance using simple heuristics.
        
        Args:
            destination: Expected destination
            num_days: Expected number of days
            response: Generated response
            
        Returns:
            Relevance score between 0 and 1
        """
        score = 0.0
        
        # Check if destination is mentioned
        if destination.lower() in response.lower():
            score += 0.3
        
        # Check if number of days is reflected
        if str(num_days) in response or f"{num_days}-day" in response.lower():
            score += 0.3
        
        # Check for itinerary structure
        if "day" in response.lower() and ("1" in response or "first" in response.lower()):
            score += 0.2
        
        # Check for travel-related content
        travel_keywords = ["visit", "explore", "see", "tour", "accommodation", "hotel", "restaurant"]
        if any(keyword in response.lower() for keyword in travel_keywords):
            score += 0.2
        
        return min(score, 1.0)
    
    def _evaluate_contains(self, destination: str, response: str) -> float:
        """
        Evaluate if response contains required elements.
        
        Args:
            destination: Expected destination
            response: Generated response
            
        Returns:
            Contains score between 0 and 1
        """
        score = 0.0
        
        # Check for destination
        if destination.lower() in response.lower():
            score += 0.4
        
        # Check for "Day 1" or similar
        if "day 1" in response.lower() or "day one" in response.lower():
            score += 0.3
        
        # Check for "itinerary"
        if "itinerary" in response.lower():
            score += 0.3
        
        return min(score, 1.0)
    
    def _evaluate_quality(self, response: str, num_days: int) -> float:
        """
        Evaluate response quality using heuristics.
        
        Args:
            response: Generated response
            num_days: Expected number of days
            
        Returns:
            Quality score between 0 and 1
        """
        score = 0.0
        
        # Check for structure
        if "day" in response.lower():
            score += 0.2
        
        # Check for specific activities
        activity_keywords = ["visit", "explore", "see", "tour", "museum", "park", "restaurant"]
        if any(keyword in response.lower() for keyword in activity_keywords):
            score += 0.2
        
        # Check for accommodations
        accommodation_keywords = ["hotel", "accommodation", "stay", "lodging"]
        if any(keyword in response.lower() for keyword in accommodation_keywords):
            score += 0.2
        
        # Check for realistic planning
        if len(response) > 200:  # Substantial response
            score += 0.2
        
        # Check for day count matching
        day_count = response.lower().count("day")
        if day_count >= num_days:
            score += 0.2
        
        return min(score, 1.0)
    
    def convert_logs_to_test_data(self, output_file: str = "eval_data.jsonl"):
        """
        Convert logged interactions to test data format.
        
        Args:
            output_file: Output file for test data
            
        Returns:
            Path to the created test data file
        """
        test_data = []
        
        with open(self.log_file, 'r') as f:
            for line in f:
                if line.strip():
                    log_entry = json.loads(line)
                    
                    # Convert to test format
                    test_case = {
                        "input": {
                            "destination": log_entry["user_input"]["destination"],
                            "num_days": log_entry["user_input"]["num_days"]
                        },
                        "expected": log_entry["planner_output"]
                    }
                    test_data.append(test_case)
        
        with open(output_file, 'w') as f:
            for test_case in test_data:
                f.write(json.dumps(test_case) + '\n')
        
        return output_file
    
    def analyze_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze evaluation results and generate insights.
        
        Args:
            results: Raw evaluation results
            
        Returns:
            Dictionary containing analysis and insights
        """
        analysis = {
            "summary": {
                "total_tests": len(results.get("results", [])),
                "passed_tests": 0,
                "failed_tests": 0,
                "average_scores": {}
            },
            "failed_cases": [],
            "insights": [],
            "recommendations": []
        }
        
        for result in results.get("results", []):
            test_name = result.get("test", {}).get("description", "Unknown")
            passed = result.get("passed", False)
            score = result.get("score", 0)
            
            if passed:
                analysis["summary"]["passed_tests"] += 1
            else:
                analysis["summary"]["failed_tests"] += 1
                analysis["failed_cases"].append({
                    "test": test_name,
                    "score": score,
                    "details": result.get("details", {})
                })
        
        # Generate insights
        if analysis["summary"]["failed_tests"] > 0:
            analysis["insights"].append(
                f"Found {analysis['summary']['failed_tests']} failed test cases that need attention"
            )
        
        if analysis["summary"]["passed_tests"] == analysis["summary"]["total_tests"]:
            analysis["insights"].append("All tests passed - agent is performing well")
        
        # Generate recommendations
        if analysis["failed_cases"]:
            analysis["recommendations"].append(
                "Review and improve agent prompts for failed test cases"
            )
        
        return analysis
    
    def generate_report(self, analysis: Dict[str, Any], output_file: str = "evaluation_report.md"):
        """
        Generate a comprehensive evaluation report.
        
        Args:
            analysis: Analysis results from analyze_results()
            output_file: Output file for the report
        """
        with open(output_file, 'w') as f:
            f.write("# AI Travel Agent Evaluation Report\n\n")
            
            f.write("## Summary\n")
            f.write(f"- Total Tests: {analysis['summary']['total_tests']}\n")
            f.write(f"- Passed: {analysis['summary']['passed_tests']}\n")
            f.write(f"- Failed: {analysis['summary']['failed_tests']}\n\n")
            
            f.write("## Failed Cases\n")
            if analysis["failed_cases"]:
                for case in analysis["failed_cases"]:
                    f.write(f"- **{case['test']}**: Score {case['score']}\n")
            else:
                f.write("- No failed cases\n")
            f.write("\n")
            
            f.write("## Insights\n")
            for insight in analysis["insights"]:
                f.write(f"- {insight}\n")
            f.write("\n")
            
            f.write("## Recommendations\n")
            for rec in analysis["recommendations"]:
                f.write(f"- {rec}\n")
            f.write("\n")
            
            f.write("## Next Steps\n")
            f.write("1. Review failed test cases and improve agent prompts\n")
            f.write("2. Add more diverse test cases to the evaluation set\n")
            f.write("3. Consider implementing additional quality metrics\n")
            f.write("4. Set up automated evaluation pipeline\n")
        
        return output_file 