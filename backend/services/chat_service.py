"""
Chat Service for AI Mental Health Counselor
Integrates therapy prompts with Llama 3.1 for therapeutic conversations
"""

import requests
import json
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime

from ..utils.therapy_prompts import (
    TherapyPrompts,
    TherapyApproach,
    EmotionalState,
    detect_crisis_level,
    create_therapy_session_prompt
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatService:
    """
    Main chat service that handles therapeutic conversations
    """
    
    def __init__(self, model_name: str = "llama3.1:8b-instruct-q4_0"):
        self.model_name = model_name
        self.therapy_prompts = TherapyPrompts()
        self.conversation_history: List[Dict] = []
        self.session_context: Dict = {
            "session_start": datetime.now(),
            "emotional_state": EmotionalState.NEUTRAL,
            "therapy_approach": TherapyApproach.CBT,
            "crisis_detected": False,
            "session_summary": ""
        }
    
    def start_session(self, user_id: str = None) -> Dict:
        """
        Start a new therapy session
        
        Args:
            user_id: Optional user identifier
            
        Returns:
            Session initialization response
        """
        # Reset session context
        self.session_context = {
            "session_start": datetime.now(),
            "emotional_state": EmotionalState.NEUTRAL,
            "therapy_approach": TherapyApproach.CBT,
            "crisis_detected": False,
            "session_summary": "",
            "user_id": user_id
        }
        
        # Get welcome message
        welcome_message = self.therapy_prompts.get_prompt(
            "conversation_starters", 
            "first_session"
        )
        
        return {
            "message": welcome_message,
            "session_id": str(self.session_context["session_start"].timestamp()),
            "emotional_state": self.session_context["emotional_state"].value,
            "therapy_approach": self.session_context["therapy_approach"].value
        }
    
    def process_message(self, user_message: str, user_id: str = None) -> Dict:
        """
        Process a user message and generate therapeutic response
        
        Args:
            user_message: The user's message
            user_id: Optional user identifier
            
        Returns:
            Response with AI counselor message and metadata
        """
        try:
            # Detect crisis level
            crisis_level = detect_crisis_level(user_message)
            crisis_detected = crisis_level in ["high", "medium"]
            
            # Update session context
            self.session_context["crisis_detected"] = crisis_detected
            
            # Determine emotional state (simplified - in production, use emotion detection model)
            emotional_state = self._detect_emotional_state(user_message)
            self.session_context["emotional_state"] = emotional_state
            
            # Choose therapy approach based on context
            therapy_approach = self._choose_therapy_approach(user_message, emotional_state, crisis_detected)
            self.session_context["therapy_approach"] = therapy_approach
            
            # Build contextual prompt
            prompt = self._build_therapeutic_prompt(user_message, emotional_state, therapy_approach, crisis_detected)
            
            # Generate response using Llama 3.1
            ai_response = self._generate_response(prompt)
            
            # Store conversation
            conversation_entry = {
                "timestamp": datetime.now(),
                "user_message": user_message,
                "ai_response": ai_response,
                "emotional_state": emotional_state.value,
                "therapy_approach": therapy_approach.value,
                "crisis_level": crisis_level
            }
            self.conversation_history.append(conversation_entry)
            
            # Prepare response
            response = {
                "message": ai_response,
                "emotional_state": emotional_state.value,
                "therapy_approach": therapy_approach.value,
                "crisis_level": crisis_level,
                "session_id": str(self.session_context["session_start"].timestamp())
            }
            
            # Add crisis resources if needed
            if crisis_level == "high":
                response["crisis_resources"] = self._get_crisis_resources()
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return {
                "message": "I'm having trouble processing your message right now. Please try again, and if you're in crisis, please contact a crisis helpline immediately.",
                "error": str(e),
                "crisis_level": "unknown"
            }
    
    def _detect_emotional_state(self, message: str) -> EmotionalState:
        """
        Simple emotion detection based on keywords
        In production, use a proper emotion detection model
        """
        message_lower = message.lower()
        
        # Anxiety indicators
        anxiety_keywords = ["anxious", "worried", "nervous", "stress", "panic", "fear", "scared"]
        if any(keyword in message_lower for keyword in anxiety_keywords):
            return EmotionalState.ANXIOUS
        
        # Depression indicators
        depression_keywords = ["sad", "depressed", "hopeless", "worthless", "tired", "exhausted", "empty"]
        if any(keyword in message_lower for keyword in depression_keywords):
            return EmotionalState.DEPRESSED
        
        # Anger indicators
        anger_keywords = ["angry", "furious", "mad", "frustrated", "irritated", "rage"]
        if any(keyword in message_lower for keyword in anger_keywords):
            return EmotionalState.ANGRY
        
        # Overwhelmed indicators
        overwhelmed_keywords = ["overwhelmed", "too much", "can't handle", "drowning", "swamped"]
        if any(keyword in message_lower for keyword in overwhelmed_keywords):
            return EmotionalState.OVERWHELMED
        
        # Hopeful indicators
        hopeful_keywords = ["hope", "better", "improving", "progress", "optimistic", "positive"]
        if any(keyword in message_lower for keyword in hopeful_keywords):
            return EmotionalState.HOPEFUL
        
        return EmotionalState.NEUTRAL
    
    def _choose_therapy_approach(self, message: str, emotional_state: EmotionalState, crisis_detected: bool) -> TherapyApproach:
        """
        Choose appropriate therapy approach based on context
        """
        if crisis_detected:
            return TherapyApproach.CRISIS_INTERVENTION
        
        # Choose approach based on emotional state and content
        if emotional_state == EmotionalState.ANXIOUS:
            return TherapyApproach.CBT
        elif emotional_state == EmotionalState.DEPRESSED:
            return TherapyApproach.HUMANISTIC
        elif emotional_state == EmotionalState.OVERWHELMED:
            return TherapyApproach.SOLUTION_FOCUSED
        elif emotional_state == EmotionalState.ANGRY:
            return TherapyApproach.DBT
        else:
            return TherapyApproach.CBT
    
    def _build_therapeutic_prompt(self, user_message: str, emotional_state: EmotionalState, 
                                therapy_approach: TherapyApproach, crisis_detected: bool) -> str:
        """
        Build comprehensive therapeutic prompt
        """
        # Get recent conversation context
        recent_context = ""
        if self.conversation_history:
            recent_exchanges = self.conversation_history[-3:]  # Last 3 exchanges
            for exchange in recent_exchanges:
                recent_context += f"User: {exchange['user_message']}\n"
                recent_context += f"Alex: {exchange['ai_response']}\n\n"
        
        current_context = f"{recent_context}User: {user_message}"
        
        return self.therapy_prompts.build_contextual_prompt(
            base_context=current_context,
            emotional_state=emotional_state,
            therapy_approach=therapy_approach,
            crisis_indicators=crisis_detected
        )
    
    def _generate_response(self, prompt: str) -> str:
        """
        Generate response using Llama 3.1 via Ollama
        """
        try:
            response = requests.post(
                'http://localhost:11434/api/generate',
                json={
                    'model': self.model_name,
                    'prompt': prompt,
                    'stream': False,
                    'options': {
                        'temperature': 0.7,
                        'top_p': 0.9,
                        'max_tokens': 500
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', 'I understand. Can you tell me more about that?')
            else:
                logger.error(f"Ollama API error: {response.status_code}")
                return "I'm having trouble connecting right now. Please try again."
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Connection error: {e}")
            return "I'm unable to connect to my language model right now. Please try again later."
    
    def _get_crisis_resources(self) -> Dict:
        """
        Get crisis intervention resources
        """
        return {
            "emergency_contacts": {
                "national_suicide_prevention": "988",
                "crisis_text_line": "Text HOME to 741741",
                "emergency_services": "911"
            },
            "immediate_actions": [
                "Remove any means of self-harm from your environment",
                "Contact a trusted friend or family member",
                "Go to the nearest emergency room if you're in immediate danger",
                "Call 988 for immediate crisis support"
            ],
            "safety_plan": "Consider creating a safety plan with a mental health professional"
        }
    
    def end_session(self) -> Dict:
        """
        End the current therapy session and provide summary
        """
        # Generate session summary
        session_summary = self._generate_session_summary()
        
        # Get closing message
        closing_message = self.therapy_prompts.get_prompt("closing_prompts", "session_summary")
        
        return {
            "message": closing_message,
            "session_summary": session_summary,
            "session_duration": str(datetime.now() - self.session_context["session_start"]),
            "total_exchanges": len(self.conversation_history),
            "emotional_states_observed": self._get_emotional_state_summary()
        }
    
    def _generate_session_summary(self) -> str:
        """
        Generate a summary of the therapy session
        """
        if not self.conversation_history:
            return "Session ended without any conversation."
        
        # Count different emotional states
        emotional_counts = {}
        for entry in self.conversation_history:
            emotion = entry["emotional_state"]
            emotional_counts[emotion] = emotional_counts.get(emotion, 0) + 1
        
        # Find most common emotional state
        primary_emotion = max(emotional_counts.items(), key=lambda x: x[1])[0] if emotional_counts else "neutral"
        
        # Count crisis mentions
        crisis_count = sum(1 for entry in self.conversation_history if entry["crisis_level"] != "none")
        
        summary = f"Session focused on {primary_emotion} experiences. "
        if crisis_count > 0:
            summary += f"Crisis indicators were detected {crisis_count} times. "
        
        summary += f"Total of {len(self.conversation_history)} exchanges occurred."
        
        return summary
    
    def _get_emotional_state_summary(self) -> Dict:
        """
        Get summary of emotional states observed during session
        """
        emotional_counts = {}
        for entry in self.conversation_history:
            emotion = entry["emotional_state"]
            emotional_counts[emotion] = emotional_counts.get(emotion, 0) + 1
        
        return emotional_counts
    
    def get_session_stats(self) -> Dict:
        """
        Get statistics about the current session
        """
        return {
            "session_duration": str(datetime.now() - self.session_context["session_start"]),
            "total_exchanges": len(self.conversation_history),
            "current_emotional_state": self.session_context["emotional_state"].value,
            "current_therapy_approach": self.session_context["therapy_approach"].value,
            "crisis_detected": self.session_context["crisis_detected"],
            "emotional_states_observed": self._get_emotional_state_summary()
        }

# Example usage
if __name__ == "__main__":
    # Initialize chat service
    chat_service = ChatService()
    
    # Start session
    session = chat_service.start_session("user123")
    print(f"Session started: {session['message']}")
    
    # Test conversation
    test_messages = [
        "I'm feeling really anxious about my upcoming presentation",
        "I've been having trouble sleeping lately",
        "I'm so overwhelmed with all my responsibilities"
    ]
    
    for message in test_messages:
        print(f"\nUser: {message}")
        response = chat_service.process_message(message)
        print(f"Alex: {response['message']}")
        print(f"Emotional State: {response['emotional_state']}")
        print(f"Therapy Approach: {response['therapy_approach']}")
    
    # End session
    session_end = chat_service.end_session()
    print(f"\nSession ended: {session_end['message']}")
    print(f"Summary: {session_end['session_summary']}")
