from google import genai
import json
import time

# ==========================================
# CONFIGURATION
# ==========================================
# 🚨 PASTE YOUR API KEY HERE 🚨
GOOGLE_API_KEY = "AIzaSyBOGEMXoQtdhvPwIX2nWum8Oas6ZcxI37k"

# ==========================================
# 1. THE TRACER
# ==========================================
class ExecutionTracer:
    def __init__(self):
        self.trace = []
    def log(self, message):
        self.trace.append(message)
    def get_trace(self):
        return self.trace
    def clear(self):
        self.trace = []

# ==========================================
# 2. THE TARGET PROGRAM
# ==========================================
def target_program(x, y, tracer):
    tracer.log(f"START: Inputs x={x}, y={y}")
    if x > 10:
        tracer.log("Branch 1: x > 10 (TRUE)")
        if y < 5:
            tracer.log("Branch 2: y < 5 (TRUE) -> 🏆 BUG FOUND!")
            return "BUG_FOUND"
        else:
            tracer.log("Branch 2: y < 5 (FALSE)")
            return "Path_A"
    else:
        tracer.log("Branch 1: x > 10 (FALSE)")
        if x == 5:
            tracer.log("Branch 3: x == 5 (TRUE)")
            return "Path_B"
        else:
            tracer.log("Branch 3: x == 5 (FALSE)")
            return "Path_C"

# ==========================================
# 3. THE AGENT
# ==========================================
class AgenticReasoner:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        # We use the name explicitly found in your list
        self.model_name = "gemini-flash-latest"

    def propose_new_inputs(self, last_inputs, last_trace, covered_paths):
        prompt = f"""
        You are a software testing agent.
        STATUS:
        - Tried inputs: {last_inputs}
        - Trace: {json.dumps(last_trace)}
        - Found {len(covered_paths)} paths.

        TASK:
        - Identify which 'if' condition failed.
        - Propose NEW integer inputs (x, y) to flip that condition.
        
        Output JSON only: {{"x": <int>, "y": <int>, "reasoning": "<text>"}}
        """

        try:
            print("🤖 Agent is thinking...")
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config={
                    'response_mime_type': 'application/json'
                }
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"⚠️ API Warning: {e}")
            return {"x": 0, "y": 0, "reasoning": "Error - Retrying"}

# ==========================================
# 4. THE ORCHESTRATOR
# ==========================================
def run_engine():
    print("🚀 Starting ACE Engine (Using 'gemini-flash-latest')...")
    
    tracer = ExecutionTracer()
    agent = AgenticReasoner(GOOGLE_API_KEY)
    
    inputs = {"x": 0, "y": 0}
    covered_paths = set()
    
    for i in range(1, 6):
        print(f"\n--- ITERATION {i} ---")
        
        # 1. Run
        tracer.clear()
        result = target_program(inputs['x'], inputs['y'], tracer)
        
        # 2. Check
        trace_str = str(tracer.get_trace())
        if result == "BUG_FOUND":
            print(f"🎉 SUCCESS! Found the bug with inputs: {inputs}")
            break
            
        if trace_str not in covered_paths:
            print(f"✨ New Path: {result}")
            covered_paths.add(trace_str)
        else:
            print(f"🔁 Duplicate path.")

        # 3. Ask AI
        new_plan = agent.propose_new_inputs(inputs, tracer.get_trace(), covered_paths)
        
        # 4. Update
        inputs = {"x": new_plan['x'], "y": new_plan['y']}
        print(f"🧠 Reasoning: {new_plan.get('reasoning')}")
        
        # Polite wait
        time.sleep(5)

if __name__ == "__main__":
    run_engine()