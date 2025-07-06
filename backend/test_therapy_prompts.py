"""
Enhanced Test script for the therapeutic prompt system
Includes safety improvements and better error handling
"""

import requests
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum
import subprocess
import pytest
from utils.therapy_prompts import TherapyPrompts, EmotionalState, TherapyApproach, detect_crisis_level

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CrisisLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class SafetyProtocol:
    """Enhanced safety protocols for crisis situations"""
    
    CRISIS_KEYWORDS = {
        'critical': ['kill myself', 'suicide', 'end it all', 'kill me'],
        'high': ['hurt myself', 'self harm', 'want to die', 'no point living'],
        'medium': ['hopeless', 'worthless', 'can\'t go on', 'nothing matters'],
        'low': ['sad', 'down', 'upset', 'worried']
    }
    
    CRISIS_RESOURCES = {
        'suicide_hotline': '988',
        'crisis_text': 'Text HOME to 741741',
        'emergency': '911'
    }
    
    @classmethod
    def detect_crisis_level(cls, message: str) -> Tuple[CrisisLevel, List[str]]:
        """Enhanced crisis detection with matched keywords"""
        message_lower = message.lower()
        matched_keywords = []
        
        for level, keywords in cls.CRISIS_KEYWORDS.items():
            for keyword in keywords:
                if keyword in message_lower:
                    matched_keywords.append(keyword)
                    if level == 'critical':
                        return CrisisLevel.CRITICAL, matched_keywords
                    elif level == 'high':
                        return CrisisLevel.HIGH, matched_keywords
                    elif level == 'medium':
                        return CrisisLevel.MEDIUM, matched_keywords
        
        return CrisisLevel.LOW, matched_keywords
    
    @classmethod
    def get_crisis_response(cls, crisis_level: CrisisLevel) -> str:
        """Get appropriate crisis response based on level"""
        if crisis_level == CrisisLevel.CRITICAL:
            return (
                "🚨 I'm very concerned about your safety. Please reach out for immediate help:\n"
                f"• Call 988 (Suicide & Crisis Lifeline)\n"
                f"• Text HOME to 741741\n"
                f"• Call 911 if in immediate danger\n"
                "You don't have to go through this alone."
            )
        elif crisis_level == CrisisLevel.HIGH:
            return (
                "I'm concerned about what you're going through. Please consider:\n"
                f"• Calling 988 for support\n"
                f"• Reaching out to a trusted friend or family member\n"
                "Your life has value, and help is available."
            )
        elif crisis_level == CrisisLevel.MEDIUM:
            return (
                "I hear that you're struggling. These feelings are valid, and support is available:\n"
                f"• 988 Suicide & Crisis Lifeline\n"
                f"• Crisis Text Line: Text HOME to 741741"
            )
        else:
            return ""

class TherapyPrompts:
    """Enhanced therapy prompts with safety integration"""
    
    def __init__(self):
        self.session_start_time = datetime.now()
        self.safety_protocol = SafetyProtocol()
    
    def get_base_system_prompt(self) -> str:
        """Get the base system prompt with safety disclaimers"""
        return """
        You are Alex, a supportive AI mental health assistant. You provide empathetic listening 
        and evidence-based therapeutic guidance. 
        
        IMPORTANT SAFETY PROTOCOLS:
        - You are NOT a replacement for professional mental health care
        - Always prioritize user safety and crisis intervention
        - Encourage professional help when appropriate
        - Maintain clear boundaries about your capabilities
        
        Your approach should be:
        - Empathetic and non-judgmental
        - Based on evidence-based therapeutic techniques
        - Focused on empowering the user
        - Culturally sensitive and inclusive
        
        If you detect any crisis indicators, immediately provide crisis resources.
        """
    
    def create_therapy_session_prompt(
        self, 
        user_input: str, 
        emotional_state: EmotionalState,
        therapy_approach: TherapyApproach,
        session_context: Optional[str] = None
    ) -> str:
        """Create contextual therapy session prompt with safety checks"""
        
        # Safety check first
        crisis_level, keywords = self.safety_protocol.detect_crisis_level(user_input)
        
        base_prompt = self.get_base_system_prompt()
        
        # Add crisis response if needed
        crisis_response = ""
        if crisis_level in [CrisisLevel.CRITICAL, CrisisLevel.HIGH, CrisisLevel.MEDIUM]:
            crisis_response = f"\nCRISIS DETECTED: {self.safety_protocol.get_crisis_response(crisis_level)}\n"
        
        # Therapeutic approach guidance
        approach_guidance = self._get_approach_guidance(therapy_approach)
        
        # Emotional state consideration
        emotional_guidance = self._get_emotional_guidance(emotional_state)
        
        session_prompt = f"""
        {base_prompt}
        
        {crisis_response}
        
        CURRENT SESSION CONTEXT:
        - User's emotional state: {emotional_state.value}
        - Therapeutic approach: {therapy_approach.value}
        - Session context: {session_context or "First interaction"}
        
        THERAPEUTIC APPROACH GUIDANCE:
        {approach_guidance}
        
        EMOTIONAL STATE CONSIDERATIONS:
        {emotional_guidance}
        
        USER INPUT: "{user_input}"
        
        Please respond with empathy, using the specified therapeutic approach while maintaining safety protocols.
        """
        
        return session_prompt
    
    def _get_approach_guidance(self, approach: TherapyApproach) -> str:
        """Get guidance for specific therapeutic approaches"""
        guidance = {
            TherapyApproach.CBT: """
            Focus on:
            - Identifying negative thought patterns
            - Challenging cognitive distortions
            - Developing coping strategies
            - Behavioral activation techniques
            """,
            TherapyApproach.DBT: """
            Focus on:
            - Distress tolerance skills
            - Emotion regulation techniques
            - Interpersonal effectiveness
            - Mindfulness practices
            """,
            TherapyApproach.HUMANISTIC: """
            Focus on:
            - Unconditional positive regard
            - Active listening and reflection
            - Empowering self-discovery
            - Validating emotions and experiences
            """,
            TherapyApproach.SOLUTION_FOCUSED: """
            Focus on:
            - Identifying strengths and resources
            - Setting achievable goals
            - Exploring what's working
            - Building on existing positive behaviors
            """,
            TherapyApproach.MINDFULNESS: """
            Focus on:
            - Present-moment awareness
            - Non-judgmental observation
            - Breathing and grounding techniques
            - Acceptance-based strategies
            """
        }
        return guidance.get(approach, "")
    
    def _get_emotional_guidance(self, state: EmotionalState) -> str:
        """Get guidance for responding to specific emotional states"""
        guidance = {
            EmotionalState.ANXIOUS: """
            - Validate their anxiety as understandable
            - Offer grounding techniques
            - Explore specific worries
            - Provide breathing exercises
            """,
            EmotionalState.DEPRESSED: """
            - Validate their feelings without minimizing
            - Assess for safety concerns
            - Encourage small, manageable steps
            - Explore support systems
            """,
            EmotionalState.OVERWHELMED: """
            - Help break down problems into manageable parts
            - Prioritize immediate needs
            - Offer organizational strategies
            - Validate their experience
            """,
            EmotionalState.ANGRY: """
            - Validate their anger as a normal emotion
            - Explore underlying needs or hurt
            - Offer healthy expression techniques
            - Ensure safety for self and others
            """,
            EmotionalState.NEUTRAL: """
            - Explore their current state of mind
            - Check in on overall wellbeing
            - Discuss goals and aspirations
            - Maintain supportive presence
            """
        }
        return guidance.get(state, "")

class EnhancedTherapyTester:
    """Enhanced testing framework with safety protocols"""
    
    def __init__(self, model_name: str = "llama3.1:8b-instruct-q4_0"):
        self.model_name = model_name
        self.therapy_prompts = TherapyPrompts()
        self.test_results = []
    
    def test_ollama_connection(self) -> bool:
        """Test if Ollama is running and model is available"""
        try:
            # Check if Ollama is running
            response = requests.get('http://localhost:11434/api/tags', timeout=5)
            if response.status_code != 200:
                return False
            
            # Check if model is available
            models = response.json().get('models', [])
            available_models = [model['name'] for model in models]
            
            if self.model_name not in available_models:
                logger.warning(f"Model {self.model_name} not found. Available models: {available_models}")
                return False
            
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama connection failed: {e}")
            return False
    
    def test_crisis_detection(self) -> None:
        """Test enhanced crisis detection"""
        print("\n🚨 Enhanced Crisis Detection Test")
        print("=" * 50)
        
        test_messages = [
            "I'm feeling really sad today",
            "I don't think I can go on anymore",
            "I want to kill myself",
            "Everything feels hopeless and worthless",
            "I'm thinking about hurting myself",
            "I just want to disappear forever",
            "Life has no meaning, I want to end it all"
        ]
        
        for message in test_messages:
            crisis_level, keywords = SafetyProtocol.detect_crisis_level(message)
            response = SafetyProtocol.get_crisis_response(crisis_level)
            
            print(f"\nMessage: '{message}'")
            print(f"Crisis Level: {crisis_level.value}")
            print(f"Keywords Found: {keywords}")
            if response:
                print(f"Crisis Response: {response}")
            print("-" * 30)
    
    def test_therapy_scenarios(self) -> None:
        """Test therapy scenarios with enhanced safety"""
        print("\n🤖 Enhanced AI Mental Health Counselor Test")
        print("=" * 60)
        
        test_scenarios = [
            {
                "user_input": "I'm feeling really anxious about my upcoming job interview",
                "emotional_state": EmotionalState.ANXIOUS,
                "therapy_approach": TherapyApproach.CBT,
                "description": "Anxiety scenario with CBT approach"
            },
            {
                "user_input": "I've been feeling really down lately, like nothing matters",
                "emotional_state": EmotionalState.DEPRESSED,
                "therapy_approach": TherapyApproach.HUMANISTIC,
                "description": "Depression scenario with humanistic approach"
            },
            {
                "user_input": "I want to end my life, I can't take it anymore",
                "emotional_state": EmotionalState.DEPRESSED,
                "therapy_approach": TherapyApproach.HUMANISTIC,
                "description": "Crisis scenario test"
            },
            {
                "user_input": "I'm so overwhelmed with everything I have to do",
                "emotional_state": EmotionalState.OVERWHELMED,
                "therapy_approach": TherapyApproach.SOLUTION_FOCUSED,
                "description": "Overwhelmed scenario with solution-focused approach"
            }
        ]
        
        for i, scenario in enumerate(test_scenarios, 1):
            print(f"\n📋 Test {i}: {scenario['description']}")
            print("-" * 40)
            
            # Build the contextual prompt
            prompt = self.therapy_prompts.create_therapy_session_prompt(
                user_input=scenario['user_input'],
                emotional_state=scenario['emotional_state'],
                therapy_approach=scenario['therapy_approach']
            )
            
            print(f"User: {scenario['user_input']}")
            print(f"Emotional State: {scenario['emotional_state'].value}")
            print(f"Therapy Approach: {scenario['therapy_approach'].value}")
            
            # Test with Ollama CLI
            try:
                cmd = [
                    "ollama", "run", self.model_name
                ]
                result = subprocess.run(
                    cmd,
                    input=prompt,
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                if result.returncode == 0:
                    ai_response = result.stdout.strip()
                    print(f"\n🤖 Alex (AI Counselor): {ai_response}")
                    self.test_results.append({
                        'scenario': scenario['description'],
                        'success': True,
                        'response_length': len(ai_response)
                    })
                else:
                    print(f"❌ Ollama CLI error: {result.stderr}")
                    self.test_results.append({
                        'scenario': scenario['description'],
                        'success': False,
                        'error': result.stderr
                    })
            except subprocess.TimeoutExpired:
                print("❌ Ollama CLI timed out.")
                self.test_results.append({
                    'scenario': scenario['description'],
                    'success': False,
                    'error': 'TimeoutExpired'
                })
            except Exception as e:
                print(f"❌ Ollama CLI error: {e}")
                self.test_results.append({
                    'scenario': scenario['description'],
                    'success': False,
                    'error': str(e)
                })
            print("\n" + "="*60)
    
    def print_test_summary(self) -> None:
        """Print summary of test results"""
        print("\n📊 Test Summary")
        print("=" * 30)
        
        total_tests = len(self.test_results)
        successful_tests = sum(1 for result in self.test_results if result['success'])
        
        print(f"Total Tests: {total_tests}")
        print(f"Successful: {successful_tests}")
        print(f"Failed: {total_tests - successful_tests}")
        print(f"Success Rate: {successful_tests/total_tests*100:.1f}%" if total_tests > 0 else "N/A")


def main():
    """Main test runner"""
    print("🧠 Enhanced AI Mental Health Counselor Test Suite")
    print("=" * 60)
    
    tester = EnhancedTherapyTester()
    
    # Test crisis detection
    tester.test_crisis_detection()
    
    # Test therapy scenarios
    tester.test_therapy_scenarios()
    
    # Print summary
    tester.print_test_summary()
    
    print("\n✅ Enhanced test suite completed!")
    print("\n⚠️  IMPORTANT REMINDER:")
    print("This AI system is for support only and should not replace professional mental health care.")

def test_base_system_prompt():
    prompts = TherapyPrompts()
    prompt = prompts.get_prompt("base_system")
    assert "Alex" in prompt

def test_emotional_response():
    prompts = TherapyPrompts()
    response = prompts.get_emotional_response(EmotionalState.ANXIOUS)
    assert isinstance(response, str)

def test_therapeutic_response():
    prompts = TherapyPrompts()
    response = prompts.get_therapeutic_response(TherapyApproach.CBT, "thought_challenging", negative_thought="I'm not good enough")
    assert "I'm not good enough" in response

def test_crisis_detection_high():
    text = "I want to kill myself"
    level = detect_crisis_level(text)
    assert level == "high"

def test_crisis_detection_medium():
    text = "I feel hopeless and want to give up"
    level = detect_crisis_level(text)
    assert level == "medium"

def test_crisis_detection_none():
    text = "I'm just a bit tired today"
    level = detect_crisis_level(text)
    assert level == "none"

if __name__ == "__main__":
    main()