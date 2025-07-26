# 🛫 AI Travel Agent

An AI-powered travel agent that generates personalized travel itineraries using local Deepseek R1 model. It automates the process of researching, planning, and organizing your dream vacation, allowing you to explore exciting destinations with ease.

## Features

- **Research & Discovery**: Find exciting travel destinations, activities, and accommodations
- **Personalized Planning**: Customize itineraries based on your travel duration
- **AI-Powered**: Utilizes Deepseek R1 for intelligent and personalized travel plans
- **Quality Assessment**: Comprehensive evaluation system with built-in quality metrics
- **Automated Logging**: All interactions are logged for continuous improvement

## Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/Shubhamsaboo/awesome-llm-apps.git
cd awesome-llm-apps/ai_agent_tutorials/ai_travel_agent
```

### 2. Install Dependencies

```bash
# Create a virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the Application

```bash
streamlit run travel_agent.py
```

## Architecture

The AI Travel Agent consists of two main components:

### **Researcher Agent**
- Generates search terms based on destination and travel duration
- Searches the web for relevant activities and accommodations using DuckDuckGo
- Analyzes and filters results for relevance

### **Planner Agent**
- Takes research results and user preferences
- Generates personalized draft itineraries
- Includes suggested activities and accommodations
- Ensures realistic and engaging travel plans

## V1 Development Journey

> **Key Assumption**: All decisions and technology choices were made with fast prototyping and MVP development in mind, prioritizing rapid iteration and reduced complexity over long-term scalability.

The AI Travel Agent was developed as an evolution from an existing codebase, focusing on rapid prototyping and efficient development practices. The project's foundation was built upon several strategic technical decisions that prioritized ease of use, reduced overhead, and accelerated development cycles.

### **Initial Codebase Adaptation**

The project began by adapting and extending an existing travel planning codebase. This approach provided a solid foundation while allowing for rapid iteration and feature development.
 
### **API Strategy Evolution**

A significant technical decision involved transitioning from Google APIs to DuckDuckGo's search API. Several key considerations drove this strategic move:

- **Elimination of API Key Requirements**: DuckDuckGo's API eliminates the need for API key management, reducing deployment complexity and potential security concerns
- **Reduced Subscription Overhead**: The absence of usage-based billing and subscription requirements simplifies the development and deployment process
- **Enhanced Privacy**: DuckDuckGo's privacy-focused approach aligns with modern application development best practices
- **Simplified Integration**: The straightforward API integration reduces development time and maintenance overhead

### **Technology Stack Selection**

The development approach prioritized rapid prototyping and efficient development cycles:

#### **Agno Framework Integration**
The Agno framework was selected for its comprehensive agent development capabilities and intuitive API design. This choice enabled:
- Rapid agent creation and configuration
- Seamless integration with DuckDuckGo API.
- Built-in support for complex multi-agent workflows

#### **Streamlit for User Interface**
Streamlit was chosen as the frontend framework due to its:
- Rapid development capabilities for data-driven applications
- Built-in support for real-time updates and interactive components
- Minimal boilerplate code requirements
- Excellent integration with Python-based AI workflows

#### **Ollama for Local Model Management**
The integration of Ollama significantly accelerated the development process by providing:
- **No API Key Requirements**: Eliminates the overhead of managing external API credentials
- **Local Model Execution**: Reduces latency and eliminates dependency on external services
- **Rapid Iteration**: Enables quick testing and refinement of model configurations
- **Cost Efficiency**: Eliminates per-request costs associated with cloud-based model APIs

## Evaluation System

The app includes a comprehensive custom evaluation system with built-in quality assessment:

### **Running Evaluations**

```bash
# Generate sample test data. 
# Note: Use this if no itinerary was generated, hence no log files. 
#Otherwise, start running a comprehensive evaluation.
python run_evaluation.py --generate-sample-data

# Run comprehensive evaluation
python run_evaluation.py --run-eval

# Analyze existing results
python run_evaluation.py --analyze-results
```

### **Development Context & Workflow Insights**

The evaluation system was developed through a strategic decision-making process that prioritized rapid prototyping and seamless integration. After exploring external tools like Watsonx Governance, TruLens, and Promptfoo, the team encountered integration challenges that hindered development velocity. This led to the strategic decision to implement a custom evaluation system that enabled faster iteration and better control over metrics.

#### **Key Development Decisions**
- **Custom Evaluation Functions**: Switching from external tools to custom-built evaluation functions enabled faster iteration and better control over metrics
- **Strategic Metric Selection**: Carefully chosen metrics (relevance, content validation, quality assessment) provided comprehensive coverage without overwhelming complexity
- **Assertion-Based Validation**: Implementing specific assertions for destination mentions, day structures, and travel keywords ensured consistent quality standards

#### **Automation Benefits**
The evaluation workflow automation significantly improved development velocity:
- **Automatic Log Generation**: Seamless capture of all agent interactions for evaluation
- **Smart Test Data Conversion**: Automatic conversion of logs to test data format
- **Fallback Sample Data**: Automatic generation of sample test data when logs are unavailable
- **Structured Output**: Automatic generation of `eval_results.json` and separate report files
- **Real-time Feedback**: Immediate evaluation results enabling rapid iteration

#### **Custom-built-in Evaluation Advantages**
The system uses a custom-built evaluation logic instead of external tools for several advantages:
- **No External Dependencies**: Eliminates the need for external CLI tools
- **Faster Execution**: Direct Python evaluation without subprocess overhead
- **Customizable Metrics**: Easy to modify and extend evaluation criteria
- **Better Integration**: Seamless integration with the existing codebase
- **Transparent Logic**: Clear, readable evaluation algorithms

### **Core Components**

1. **`eval_utils.py`** - Main evaluation utilities
   - `TravelAgentEvaluator` class
   - Logging functionality
   - Built-in evaluation logic
   - Results analysis

2. **`run_evaluation.py`** - Evaluation runner script
   - Batch evaluation execution
   - Sample data generation
   - Report generation

### **Quality Metrics**

#### 1. Answer Relevance
- **Metric**: Built-in relevance scoring
- **Threshold**: 0.7
- **Purpose**: Ensures outputs directly respond to user requests
- **Method**: Heuristic-based scoring using destination mentions, day count, and travel keywords

#### 2. Content Validation
- **Metric**: Contains validation
- **Required Elements**:
  - Destination name (40% weight)
  - "Day 1" or similar structure (30% weight)
  - "itinerary" keyword (30% weight)
- **Purpose**: Validates basic content requirements

#### 3. Quality Rubric
- **Metric**: Multi-factor quality assessment
- **Threshold**: 0.7
- **Criteria**:
  1. Structure (day-by-day format)
  2. Specific activities (museums, parks, restaurants)
  3. Accommodations (hotels, lodging)
  4. Realistic planning (substantial response length)
  5. Day count matching (requested vs. provided)

### Custom Built-in Evaluation Logic

The system uses built-in evaluation functions that implement the following scoring algorithms:

#### Answer Relevance Scoring
```python
def _evaluate_relevance(destination, num_days, response):
    score = 0.0
    # Destination mention (30%)
    if destination.lower() in response.lower():
        score += 0.3
    # Day count reflection (30%)
    if str(num_days) in response or f"{num_days}-day" in response.lower():
        score += 0.3
    # Itinerary structure (20%)
    if "day" in response.lower() and ("1" in response or "first" in response.lower()):
        score += 0.2
    # Travel keywords (20%)
    travel_keywords = ["visit", "explore", "see", "tour", "accommodation", "hotel", "restaurant"]
    if any(keyword in response.lower() for keyword in travel_keywords):
        score += 0.2
    return min(score, 1.0)
```

#### Content Validation
```python
def _evaluate_contains(destination, response):
    score = 0.0
    # Destination (40%)
    if destination.lower() in response.lower():
        score += 0.4
    # Day structure (30%)
    if "day 1" in response.lower() or "day one" in response.lower():
        score += 0.3
    # Itinerary keyword (30%)
    if "itinerary" in response.lower():
        score += 0.3
    return min(score, 1.0)
```

#### Quality Assessment
```python
def _evaluate_quality(response, num_days):
    score = 0.0
    # Structure (20%)
    if "day" in response.lower():
        score += 0.2
    # Activities (20%)
    activity_keywords = ["visit", "explore", "see", "tour", "museum", "park", "restaurant"]
    if any(keyword in response.lower() for keyword in activity_keywords):
        score += 0.2
    # Accommodations (20%)
    accommodation_keywords = ["hotel", "accommodation", "stay", "lodging"]
    if any(keyword in response.lower() for keyword in accommodation_keywords):
        score += 0.2
    # Realistic planning (20%)
    if len(response) > 200:
        score += 0.2
    # Day count matching (20%)
    day_count = response.lower().count("day")
    if day_count >= num_days:
        score += 0.2
    return min(score, 1.0)
```

## Troubleshooting Common Issues

1. **Evaluation Fails**: Check test data format and agent compatibility
2. **Low Scores**: Review agent prompts and instructions
3. **Missing Logs**: Verify logging is enabled in the main app
4. **Import Errors**: Ensure all dependencies are installed

## Next Steps

### **Core Improvements**

#### **1. Improve Agent Prompt: ** Optimize prompts based on user feedback and performance analysis for better response quality.

#### **2. Optimize Agent Performance: ** Significantly improve model response time and system efficiency for better user experience (intelligent caching, and parallel processing)

#### **3. Implement Automated Pipeline: ** Set up comprehensive CI/CD integration for continuous deployment and quality assurance.

#### **4. Add User Feedback Integration**: Integrate comprehensive user feedback collection and analysis to improve model responses

#### **5. Implement Real-time Monitoring**: Create comprehensive real-time monitoring system for live performance tracking and immediate issue detection

#### **6. Build Continuous Learning System**: Develop intelligent system that continuously learns and improves from user interactions and performance data.

### **Evaluation Improvements**

#### **1. Extend Evaluation Metrics**: Add new custom evaluation criteria to the `TravelAgentEvaluator` class for comprehensive quality assessment.

#### **2. Enhance Evaluation Logging**: Capture comprehensive metadata during evaluation runs including model parameters, processing time, and resource usage.

#### **4. Add Comprehensive Test Cases**: Create test cases for edge scenarios and failure modes to improve evaluation robustness.

#### **5. Implement Multi-Agent Evaluation**: Test and evaluate researcher-planner coordination effectiveness for seamless agent communication.

#### **6. Evaluate Against Ground Truth**: Implement ground truth comparison using expert-curated travel itineraries and real-world travel data for accurate quality assessment.

> **Automation Note**: Further automating the evaluation workflow process, enabling real-time report generation, and implementing immediate mitigation strategies for failed assertions will significantly enhance the tool's effectiveness and make it production-ready for continuous deployment scenarios. 


