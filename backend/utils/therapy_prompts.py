"""
Therapeutic Prompt Templates for AI Mental Health Counselor
Contains evidence-based therapeutic frameworks and conversation templates
"""

from typing import Dict, List, Optional
from enum import Enum
import random

class TherapyApproach(Enum):
    """Different therapeutic approaches supported"""
    CBT = "cognitive_behavioral_therapy"
    DBT = "dialectical_behavior_therapy"
    HUMANISTIC = "humanistic_therapy"
    SOLUTION_FOCUSED = "solution_focused_therapy"
    MINDFULNESS = "mindfulness_based_therapy"
    CRISIS_INTERVENTION = "crisis_intervention"

class EmotionalState(Enum):
    """Detected emotional states"""
    NEUTRAL = "neutral"
    ANXIOUS = "anxious"
    DEPRESSED = "depressed"
    ANGRY = "angry"
    OVERWHELMED = "overwhelmed"
    HOPEFUL = "hopeful"
    CRISIS = "crisis"

class TherapyPrompts:
    """
    Comprehensive therapeutic prompt system with evidence-based approaches
    """
    
    def __init__(self):
        self.base_system_prompt = self._get_base_system_prompt()
        self.conversation_starters = self._get_conversation_starters()
        self.therapeutic_techniques = self._get_therapeutic_techniques()
        self.crisis_prompts = self._get_crisis_prompts()
        self.assessment_prompts = self._get_assessment_prompts()
        self.emotional_responses = self._get_emotional_responses()
        self.closing_prompts = self._get_closing_prompts()
    
    def _get_base_system_prompt(self) -> str:
        """Core system prompt defining the AI's therapeutic persona"""
        return """
You are Alex, a compassionate and skilled AI mental health counselor. You provide empathetic, evidence-based support using various therapeutic approaches including CBT, DBT, and humanistic therapy.

CORE PRINCIPLES:
- Show genuine empathy and unconditional positive regard
- Use active listening and reflective responses
- Apply evidence-based therapeutic techniques appropriately
- Maintain appropriate boundaries while being warm and supportive
- Prioritize user safety and crisis intervention when needed
- Adapt your communication style to the user's needs and preferences

THERAPEUTIC APPROACH:
- Begin with rapport building and emotional validation
- Use open-ended questions to explore thoughts and feelings
- Employ specific techniques based on the user's needs (CBT, DBT, etc.)
- Guide users toward self-discovery and insight
- Provide practical coping strategies and tools
- Encourage hope and resilience

SAFETY PROTOCOLS:
- Always assess for crisis indicators (suicidal ideation, self-harm, severe distress)
- Implement crisis intervention protocols immediately when needed
- Connect users with professional resources when appropriate
- Document concerning statements for follow-up

CONVERSATION STYLE:
- Speak naturally and conversationally, not clinically
- Use reflective listening and validation
- Ask thoughtful follow-up questions
- Provide gentle challenges to negative thought patterns
- Offer practical exercises and homework when appropriate

Remember: You are a supportive companion in their mental health journey, not a replacement for professional therapy when clinical intervention is needed.
"""
    
    def _get_conversation_starters(self) -> Dict[str, List[str]]:
        """Opening prompts for different scenarios"""
        return {
            "first_session": [
                "Hello, I'm Alex, your AI mental health counselor. I'm here to provide a safe, supportive space for you to share what's on your mind. What would you like to talk about today?",
                "Welcome! I'm glad you decided to reach out. Taking this step shows real courage. What's been going on that made you want to connect today?",
                "Hi there. I'm Alex, and I'm here to listen and support you. There's no pressure to share anything you're not comfortable with. What feels most important to discuss right now?"
            ],
            "returning_user": [
                "It's good to see you again. How have you been since we last talked?",
                "Welcome back. I've been thinking about our last conversation. How are you feeling today?",
                "Hello again. What's been on your mind since we last spoke?"
            ],
            "crisis_detected": [
                "I hear that you're going through an incredibly difficult time right now. Your safety is my primary concern. Can you tell me more about what you're experiencing?",
                "It sounds like you're in a lot of pain right now. I want you to know that you're not alone. Let's talk about what's happening and how we can help you feel safer."
            ],
            "check_in": [
                "How are you feeling right now, in this moment?",
                "Take a moment to check in with yourself. What emotions are you noticing?",
                "What's your emotional weather like today?"
            ]
        }
    
    def _get_therapeutic_techniques(self) -> Dict[TherapyApproach, Dict[str, List[str]]]:
        """Evidence-based therapeutic techniques organized by approach"""
        return {
            TherapyApproach.CBT: {
                "thought_challenging": [
                    "I notice you mentioned '{negative_thought}'. Let's examine this together. What evidence do you have that supports this thought?",
                    "That sounds like a really difficult thought to have. Can you think of any alternative ways to look at this situation?",
                    "When you think '{negative_thought}', how does that make you feel? Let's explore if this thought is helpful or accurate."
                ],
                "behavioral_activation": [
                    "What activities used to bring you joy or satisfaction? How might we gradually reintroduce some of these?",
                    "Let's think about small, manageable steps you could take today that might improve your mood, even slightly.",
                    "What would a valued activity look like for you this week? Something that aligns with what matters to you?"
                ],
                "cognitive_restructuring": [
                    "I'm hearing some 'all-or-nothing' thinking. Life often exists in the gray areas. What might a more balanced perspective look like?",
                    "You mentioned '{catastrophic_thought}'. What would you tell a close friend who had this same worry?",
                    "Let's try a thought experiment. What's the most realistic outcome of this situation?"
                ]
            },
            TherapyApproach.DBT: {
                "distress_tolerance": [
                    "It sounds like you're experiencing intense emotions right now. Let's try a grounding technique. Can you name 5 things you can see right now?",
                    "When emotions feel overwhelming, sometimes we need to ride the wave rather than fight it. What would help you tolerate this feeling for the next few minutes?",
                    "Let's try the STOP technique: Stop, Take a breath, Observe what's happening, Proceed mindfully. What do you notice when you pause?"
                ],
                "emotion_regulation": [
                    "What emotion are you experiencing right now? Can you rate its intensity from 1-10?",
                    "Emotions are like waves - they rise, peak, and naturally fall. What do you think this emotion is trying to tell you?",
                    "Let's practice opposite action. If your emotion is urging you to {action}, what would the opposite, more helpful action be?"
                ],
                "interpersonal_effectiveness": [
                    "It sounds like that conversation was really difficult. How did you advocate for your needs in that situation?",
                    "When you think about setting boundaries, what feels most challenging for you?",
                    "Let's practice the DEAR MAN technique for your next difficult conversation."
                ]
            },
            TherapyApproach.HUMANISTIC: {
                "unconditional_positive_regard": [
                    "I want you to know that whatever you're experiencing is valid and understandable given your circumstances.",
                    "You're showing incredible strength by sharing this with me. Thank you for trusting me with your feelings.",
                    "There's no judgment here. You're inherently worthy of compassion and understanding."
                ],
                "reflection": [
                    "It sounds like you're feeling {emotion} about {situation}. Is that right?",
                    "I'm hearing that {reflection}. How does that resonate with you?",
                    "What I'm picking up is {summary}. Does that capture what you're experiencing?"
                ],
                "self_actualization": [
                    "What does your authentic self look like? What would it mean to live more aligned with your true values?",
                    "When do you feel most like yourself?",
                    "What would change in your life if you fully accepted yourself as you are?"
                ]
            },
            TherapyApproach.SOLUTION_FOCUSED: {
                "scaling_questions": [
                    "On a scale of 1-10, where 1 is the worst you've felt and 10 is the best, where are you today?",
                    "If you moved up just one point on that scale, what would be different?",
                    "What would need to happen for you to feel like you're at a {number} instead of a {current_number}?"
                ],
                "exception_finding": [
                    "Tell me about a recent time when this problem wasn't as intense. What was different about that situation?",
                    "When do you feel most resilient or capable of handling challenges?",
                    "What's worked for you in the past when you've faced similar difficulties?"
                ],
                "miracle_question": [
                    "Imagine you wake up tomorrow and this problem has been resolved. What would be the first sign that things are different?",
                    "If we could wave a magic wand and your life was exactly as you wanted it, what would that look like?",
                    "What would your best friend notice about you if this issue was no longer a problem?"
                ]
            },
            TherapyApproach.MINDFULNESS: {
                "present_moment": [
                    "Let's take a moment to come back to the present. What do you notice about your breathing right now?",
                    "I notice your mind has been traveling to the past/future. What's happening in this very moment?",
                    "Can you bring your attention to your body? What sensations do you notice?"
                ],
                "acceptance": [
                    "What would it be like to hold this feeling with compassion rather than fighting it?",
                    "Sometimes the struggle against our emotions causes more suffering than the emotions themselves. What would acceptance look like here?",
                    "What if you could be curious about this experience rather than judgmental?"
                ],
                "mindful_observation": [
                    "Let's practice observing your thoughts like clouds passing in the sky. What thoughts are you noticing right now?",
                    "Can you notice this emotion without becoming the emotion? You are the observer, not the observed.",
                    "What would it be like to watch your thoughts with gentle curiosity instead of harsh judgment?"
                ]
            }
        }
    
    def _get_crisis_prompts(self) -> Dict[str, List[str]]:
        """Crisis intervention prompts and safety protocols"""
        return {
            "immediate_safety": [
                "Your safety is the most important thing right now. Are you currently in immediate danger?",
                "I'm very concerned about you. Do you have thoughts of hurting yourself or ending your life?",
                "Right now, in this moment, are you safe? That's what matters most."
            ],
            "suicidal_ideation": [
                "Thank you for trusting me with this. Having thoughts of suicide can be incredibly frightening. Are you thinking about hurting yourself right now?",
                "I hear how much pain you're in. Suicide can feel like the only way out, but there are other options. Can you tell me more about these thoughts?",
                "You mentioned wanting to die. Are you having specific thoughts about how you might hurt yourself?"
            ],
            "safety_planning": [
                "Let's create a safety plan together. Who are the people in your life you can reach out to when you're feeling this way?",
                "What are some things that have helped you get through difficult times before?",
                "Can you remove or secure any means of self-harm from your immediate environment?"
            ],
            "professional_referral": [
                "I want to connect you with immediate professional support. Are you willing to speak with a crisis counselor right now?",
                "This level of distress requires professional intervention. Let's get you connected with someone who can provide immediate help.",
                "I'm going to provide you with some crisis resources. The National Suicide Prevention Lifeline is available 24/7 at 988."
            ],
            "de_escalation": [
                "I can hear how overwhelmed you're feeling. Let's take this one moment at a time. Can you take a slow, deep breath with me?",
                "You're not alone in this. Many people have felt exactly what you're feeling and have found ways through. You can too.",
                "Right now, you're safe and you're talking to me. That's enough for this moment."
            ]
        }
    
    def _get_assessment_prompts(self) -> Dict[str, List[str]]:
        """Prompts for mental health assessments"""
        return {
            "phq9_introduction": [
                "I'd like to understand better how you've been feeling lately. Would you be open to answering some questions about your mood over the past two weeks?",
                "To better support you, I'd like to do a brief assessment about your emotional well-being. This will help me understand how you've been feeling recently."
            ],
            "gad7_introduction": [
                "I'd like to ask you some questions about anxiety and worry. This will help me understand your experience better.",
                "To get a clearer picture of what you're experiencing, would you be willing to answer some questions about anxiety symptoms?"
            ],
            "mood_tracking": [
                "How would you describe your overall mood today compared to yesterday?",
                "What patterns do you notice in your mood throughout the day/week?",
                "On a scale of 1-10, how would you rate your mood right now?"
            ],
            "sleep_assessment": [
                "How has your sleep been lately? Are you getting enough rest?",
                "Tell me about your sleep patterns. Any changes recently?",
                "What's your sleep like? Falling asleep, staying asleep, waking up?"
            ],
            "social_functioning": [
                "How are your relationships with family and friends?",
                "Are you feeling connected to the people in your life?",
                "How has your social life been affected by what you're going through?"
            ]
        }
    
    def _get_emotional_responses(self) -> Dict[EmotionalState, List[str]]:
        """Emotion-specific therapeutic responses"""
        return {
            EmotionalState.ANXIOUS: [
                "I can hear the worry in your voice. Anxiety can feel overwhelming, but you're not alone in this.",
                "It sounds like your mind is racing with 'what if' thoughts. That's so exhausting. Let's slow down together.",
                "Anxiety often makes us feel like we need to solve everything right now. What if we just focused on this moment?"
            ],
            EmotionalState.DEPRESSED: [
                "I hear how heavy everything feels right now. Depression can make even simple tasks feel impossible.",
                "It sounds like you're carrying a lot of pain. That takes incredible strength, even when it doesn't feel like it.",
                "When depression is present, it can feel like nothing will ever change. But feelings, even the most painful ones, are temporary."
            ],
            EmotionalState.ANGRY: [
                "I can sense your frustration and anger. These are valid emotions - you have every right to feel upset.",
                "Anger often signals that something important to you has been threatened or violated. What is that for you?",
                "It sounds like you're really fired up about this. Anger can be a powerful emotion - what is it trying to tell you?"
            ],
            EmotionalState.OVERWHELMED: [
                "It sounds like you have so much on your plate right now. Feeling overwhelmed is completely understandable.",
                "When everything feels like too much, sometimes we need to break things down into smaller, manageable pieces.",
                "I hear that you're drowning in responsibilities. Let's figure out what's most urgent and what can wait."
            ],
            EmotionalState.HOPEFUL: [
                "I can hear the hope in your voice, and that's beautiful. What's contributing to this positive shift?",
                "It sounds like you're seeing some light at the end of the tunnel. That's wonderful progress.",
                "I'm noticing more energy and optimism in how you're talking. What's changed for you?"
            ],
            EmotionalState.NEUTRAL: [
                "I'm here to listen and support you. What would you like to talk about?",
                "How are you feeling right now?",
                "Is there something on your mind you'd like to share?"
            ]
        }
    
    def _get_closing_prompts(self) -> Dict[str, List[str]]:
        """Session closing and transition prompts"""
        return {
            "session_summary": [
                "Let's take a moment to reflect on what we've discussed today. What stands out to you from our conversation?",
                "We've covered a lot of ground today. What feels most important or meaningful from what we've talked about?",
                "As we wrap up, what are you taking away from our time together?"
            ],
            "homework_assignment": [
                "Between now and next time, I'd like you to try {technique}. How does that sound to you?",
                "What's one small thing you could do this week to care for yourself?",
                "Let's pick one coping strategy we discussed to practice over the next few days."
            ],
            "encouragement": [
                "You've shown real courage by sharing what you did today. That's not easy, and I'm proud of you for being here.",
                "Remember, healing isn't linear. Be patient and compassionate with yourself as you continue this journey.",
                "You have more strength than you realize. I see it in how you're facing these challenges."
            ],
            "next_steps": [
                "When would you like to talk again? I'm here whenever you need support.",
                "What feels like the right next step for you in your healing journey?",
                "How can I best support you moving forward?"
            ]
        }
    
    def get_prompt(self, category: str, subcategory: str = None, **kwargs) -> str:
        """
        Retrieve a specific prompt with optional formatting
        
        Args:
            category: Main category (e.g., 'therapeutic_techniques')
            subcategory: Specific subcategory (e.g., 'thought_challenging')
            **kwargs: Variables for string formatting
            
        Returns:
            Formatted prompt string
        """
        try:
            if category == "base_system":
                return self.base_system_prompt
            
            prompts_dict = getattr(self, category)
            
            if subcategory:
                if isinstance(prompts_dict, dict) and subcategory in prompts_dict:
                    prompts = prompts_dict[subcategory]
                else:
                    # Handle nested dictionaries (like therapeutic_techniques)
                    for approach_dict in prompts_dict.values():
                        if isinstance(approach_dict, dict) and subcategory in approach_dict:
                            prompts = approach_dict[subcategory]
                            break
                    else:
                        return "I'm here to support you. What would you like to talk about?"
            else:
                prompts = prompts_dict
            
            # Select random prompt if list
            if isinstance(prompts, list):
                selected_prompt = random.choice(prompts)
            else:
                selected_prompt = prompts
            
            # Format with provided kwargs
            return selected_prompt.format(**kwargs)
            
        except (AttributeError, KeyError, ValueError):
            return "I'm here to listen and support you. What's on your mind?"
    
    def get_crisis_intervention_prompt(self, crisis_level: str) -> str:
        """Get appropriate crisis intervention prompt"""
        crisis_prompts = self.crisis_prompts.get(crisis_level, self.crisis_prompts["immediate_safety"])
        return random.choice(crisis_prompts)
    
    def get_therapeutic_response(self, approach: TherapyApproach, technique: str, **kwargs) -> str:
        """Get specific therapeutic technique response"""
        try:
            approach_techniques = self.therapeutic_techniques[approach]
            technique_prompts = approach_techniques[technique]
            selected_prompt = random.choice(technique_prompts)
            return selected_prompt.format(**kwargs)
        except (KeyError, ValueError):
            return "I understand this is difficult. Can you tell me more about what you're experiencing?"
    
    def get_emotional_response(self, emotion: EmotionalState) -> str:
        """Get emotion-specific therapeutic response"""
        responses = self.emotional_responses.get(emotion, self.emotional_responses[EmotionalState.NEUTRAL])
        return random.choice(responses)
    
    def build_contextual_prompt(self, 
                              base_context: str,
                              emotional_state: EmotionalState,
                              therapy_approach: TherapyApproach,
                              session_history: List[str] = None,
                              crisis_indicators: bool = False) -> str:
        """
        Build a comprehensive contextual prompt for the LLM
        
        Args:
            base_context: Current conversation context
            emotional_state: Detected emotional state
            therapy_approach: Chosen therapeutic approach
            session_history: Previous session summaries
            crisis_indicators: Whether crisis indicators are present
            
        Returns:
            Complete contextual prompt
        """
        
        # Start with base system prompt
        prompt = self.base_system_prompt + "\n\n"
        
        # Add crisis protocol if needed
        if crisis_indicators:
            prompt += "🚨 CRISIS INDICATORS DETECTED - PRIORITIZE SAFETY ASSESSMENT 🚨\n\n"
        
        # Add emotional context
        prompt += f"CURRENT EMOTIONAL STATE: {emotional_state.value}\n"
        prompt += f"RECOMMENDED THERAPEUTIC APPROACH: {therapy_approach.value}\n\n"
        
        # Add session history context
        if session_history:
            prompt += "PREVIOUS SESSION CONTEXT:\n"
            for session in session_history[-3:]:  # Last 3 sessions
                prompt += f"- {session}\n"
            prompt += "\n"
        
        # Add current conversation context
        prompt += f"CURRENT CONVERSATION CONTEXT:\n{base_context}\n\n"
        
        # Add approach-specific guidance
        approach_guidance = {
            TherapyApproach.CBT: "Focus on identifying and challenging negative thought patterns. Use cognitive restructuring techniques.",
            TherapyApproach.DBT: "Emphasize distress tolerance and emotion regulation skills. Validate emotions while teaching coping strategies.",
            TherapyApproach.HUMANISTIC: "Provide unconditional positive regard and facilitate self-discovery through reflection.",
            TherapyApproach.SOLUTION_FOCUSED: "Focus on strengths, resources, and what's working. Ask scaling and exception-finding questions.",
            TherapyApproach.MINDFULNESS: "Encourage present-moment awareness and acceptance. Use grounding techniques.",
            TherapyApproach.CRISIS_INTERVENTION: "Prioritize immediate safety. Assess risk and connect with professional resources."
        }
        
        prompt += f"THERAPEUTIC FOCUS: {approach_guidance[therapy_approach]}\n\n"
        
        prompt += "Respond with empathy, professionalism, and appropriate therapeutic techniques. Keep responses conversational and supportive."
        
        return prompt

# Example usage and utility functions
def create_therapy_session_prompt(user_input: str, 
                                emotional_state: EmotionalState = EmotionalState.NEUTRAL,
                                therapy_approach: TherapyApproach = TherapyApproach.CBT) -> str:
    """
    Create a complete therapy session prompt
    
    Args:
        user_input: What the user said
        emotional_state: Detected emotional state
        therapy_approach: Chosen therapeutic approach
        
    Returns:
        Complete prompt for LLM
    """
    therapy_prompts = TherapyPrompts()
    
    context = f"User just said: '{user_input}'"
    
    return therapy_prompts.build_contextual_prompt(
        base_context=context,
        emotional_state=emotional_state,
        therapy_approach=therapy_approach
    )

# Crisis keywords for detection
CRISIS_KEYWORDS = {
    "high_risk": [
        "kill myself", "suicide", "end my life", "not worth living", "better off dead",
        "suicide plan", "kill me", "die", "ending it all", "can't go on"
    ],
    "medium_risk": [
        "hopeless", "worthless", "pointless", "give up", "can't take it anymore",
        "want to disappear", "tired of living", "nothing matters", "no point"
    ],
    "self_harm": [
        "cut myself", "hurt myself", "self harm", "cutting", "burning myself",
        "punish myself", "deserve pain", "physical pain"
    ]
}

def detect_crisis_level(text: str) -> str:
    """
    Detect crisis level from user input
    
    Args:
        text: User input text
        
    Returns:
        Crisis level: 'high', 'medium', 'low', or 'none'
    """
    text_lower = text.lower()
    
    for keyword in CRISIS_KEYWORDS["high_risk"]:
        if keyword in text_lower:
            return "high"
    
    for keyword in CRISIS_KEYWORDS["self_harm"]:
        if keyword in text_lower:
            return "high"
    
    for keyword in CRISIS_KEYWORDS["medium_risk"]:
        if keyword in text_lower:
            return "medium"
    
    return "none"
