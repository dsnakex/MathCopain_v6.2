"""
Feature Engineering for ML Models
Extracts 20+ features from user exercise history

Features categories:
1. Performance récente (recent performance)
2. Tendances (trends)
3. Contexte (context)
4. Compétences (skills)
5. Métacognition (metacognition)
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
import numpy as np
import pandas as pd
from collections import Counter

from database.models import User, ExerciseResponse, SkillProfile
from database.connection import get_session


class FeatureEngineering:
    """
    Extract and engineer features for ML models from user exercise history
    """

    def __init__(self):
        self.feature_names = [
            # Performance récente
            'recent_success_rate',
            'recent_avg_time',
            'streak',
            'recent_exercises_count',

            # Tendances
            'trend_7d',
            'trend_30d',
            'learning_velocity',

            # Contexte
            'hour_of_day',
            'day_of_week',
            'session_length',
            'fatigue_level',

            # Compétences
            'prerequisite_mastery',
            'domain_proficiency',
            'cross_domain_avg',

            # Métacognition
            'self_reported_difficulty',
            'strategy_effectiveness',

            # Démographie
            'grade_level_encoded',
            'learning_style_encoded',

            # Statistiques
            'total_exercises',
            'total_correct',
            'overall_success_rate'
        ]

    def extract_features(self, user_id: int, skill_domain: str, n_recent: int = 10) -> Dict[str, float]:
        """
        Extract all features for a user and skill domain

        Args:
            user_id: User ID
            skill_domain: Skill domain (e.g., 'addition', 'multiplication')
            n_recent: Number of recent exercises to analyze

        Returns:
            Dict of feature_name → value
        """
        with get_session() as session:
            # Get user
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                return self._get_default_features()

            # Get recent exercises (all domains)
            recent_exercises = (
                session.query(ExerciseResponse)
                .filter(ExerciseResponse.user_id == user_id)
                .order_by(ExerciseResponse.created_at.desc())
                .limit(n_recent)
                .all()
            )

            # Get domain-specific exercises
            domain_exercises = (
                session.query(ExerciseResponse)
                .filter(
                    ExerciseResponse.user_id == user_id,
                    ExerciseResponse.skill_domain == skill_domain
                )
                .order_by(ExerciseResponse.created_at.desc())
                .limit(50)
                .all()
            )

            # Get skill profile
            skill_profile = (
                session.query(SkillProfile)
                .filter(
                    SkillProfile.user_id == user_id,
                    SkillProfile.skill_domain == skill_domain
                )
                .first()
            )

            # Get all skill profiles for cross-domain analysis
            all_profiles = (
                session.query(SkillProfile)
                .filter(SkillProfile.user_id == user_id)
                .all()
            )

            # Build features
            features = {}

            # 1. Performance récente
            features.update(self._extract_recent_performance(recent_exercises))

            # 2. Tendances
            features.update(self._extract_trends(domain_exercises))

            # 3. Contexte
            features.update(self._extract_context(recent_exercises))

            # 4. Compétences
            features.update(self._extract_skills(skill_profile, all_profiles, skill_domain))

            # 5. Métacognition
            features.update(self._extract_metacognition(domain_exercises))

            # 6. Démographie
            features.update(self._encode_demographics(user))

            # 7. Statistiques globales
            features.update(self._extract_global_stats(user_id, session))

            return features

    def _extract_recent_performance(self, exercises: List[ExerciseResponse]) -> Dict[str, float]:
        """Extract features from recent exercises"""
        if not exercises:
            return {
                'recent_success_rate': 0.0,
                'recent_avg_time': 0.0,
                'streak': 0,
                'recent_exercises_count': 0
            }

        correct_count = sum(1 for ex in exercises if ex.is_correct)
        success_rate = correct_count / len(exercises)

        # Average time (in seconds)
        times = [ex.time_taken_seconds for ex in exercises if ex.time_taken_seconds]
        avg_time = np.mean(times) if times else 0.0

        # Streak (consecutive correct)
        streak = 0
        for ex in exercises:
            if ex.is_correct:
                streak += 1
            else:
                break

        return {
            'recent_success_rate': success_rate,
            'recent_avg_time': avg_time,
            'streak': streak,
            'recent_exercises_count': len(exercises)
        }

    def _extract_trends(self, exercises: List[ExerciseResponse]) -> Dict[str, float]:
        """Extract trend features"""
        if len(exercises) < 7:
            return {
                'trend_7d': 0.0,
                'trend_30d': 0.0,
                'learning_velocity': 0.0
            }

        now = datetime.now()
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)

        # Success rate last 7 days vs previous 7 days
        recent_7d = [ex for ex in exercises if ex.created_at >= week_ago]
        prev_7d = [ex for ex in exercises if week_ago > ex.created_at >= week_ago - timedelta(days=7)]

        trend_7d = 0.0
        if recent_7d and prev_7d:
            recent_rate = sum(1 for ex in recent_7d if ex.is_correct) / len(recent_7d)
            prev_rate = sum(1 for ex in prev_7d if ex.is_correct) / len(prev_7d)
            trend_7d = recent_rate - prev_rate

        # Learning velocity (improvement per day)
        if len(exercises) >= 2:
            first_exercises = exercises[-10:]  # Oldest 10
            last_exercises = exercises[:10]   # Most recent 10

            first_rate = sum(1 for ex in first_exercises if ex.is_correct) / len(first_exercises)
            last_rate = sum(1 for ex in last_exercises if ex.is_correct) / len(last_exercises)

            days_diff = (exercises[0].created_at - exercises[-1].created_at).days + 1
            learning_velocity = (last_rate - first_rate) / max(days_diff, 1)
        else:
            learning_velocity = 0.0

        return {
            'trend_7d': trend_7d,
            'trend_30d': trend_7d,  # Simplified (could compute actual 30d)
            'learning_velocity': learning_velocity
        }

    def _extract_context(self, exercises: List[ExerciseResponse]) -> Dict[str, float]:
        """Extract contextual features"""
        if not exercises:
            return {
                'hour_of_day': 12,
                'day_of_week': 3,
                'session_length': 1,
                'fatigue_level': 0.0
            }

        # Average hour of day
        hours = [ex.created_at.hour for ex in exercises]
        avg_hour = np.mean(hours) if hours else 12

        # Most common day of week (0=Monday, 6=Sunday)
        days = [ex.created_at.weekday() for ex in exercises]
        most_common_day = Counter(days).most_common(1)[0][0] if days else 3

        # Session length (number of exercises in recent session)
        if exercises:
            session_threshold = timedelta(minutes=30)
            current_session = 1
            for i in range(len(exercises) - 1):
                if exercises[i].created_at - exercises[i+1].created_at < session_threshold:
                    current_session += 1
                else:
                    break
        else:
            current_session = 1

        # Fatigue level (0-1, based on recent performance decline)
        fatigue = 0.0
        if len(exercises) >= 5:
            first_half = exercises[:len(exercises)//2]
            second_half = exercises[len(exercises)//2:]

            first_rate = sum(1 for ex in first_half if ex.is_correct) / len(first_half)
            second_rate = sum(1 for ex in second_half if ex.is_correct) / len(second_half)

            # If performance decreases, fatigue increases
            if first_rate > second_rate:
                fatigue = (first_rate - second_rate)

        return {
            'hour_of_day': avg_hour,
            'day_of_week': most_common_day,
            'session_length': current_session,
            'fatigue_level': min(1.0, fatigue)
        }

    def _extract_skills(
        self,
        skill_profile: Optional[SkillProfile],
        all_profiles: List[SkillProfile],
        current_domain: str
    ) -> Dict[str, float]:
        """Extract skill-related features"""

        # Domain proficiency
        domain_proficiency = skill_profile.proficiency_level if skill_profile else 0.0

        # Cross-domain average
        if all_profiles:
            cross_domain_avg = np.mean([p.proficiency_level for p in all_profiles])
        else:
            cross_domain_avg = 0.0

        # Prerequisite mastery (simplified - could be domain-specific)
        prerequisite_mastery = cross_domain_avg  # Placeholder

        return {
            'prerequisite_mastery': prerequisite_mastery,
            'domain_proficiency': domain_proficiency,
            'cross_domain_avg': cross_domain_avg
        }

    def _extract_metacognition(self, exercises: List[ExerciseResponse]) -> Dict[str, float]:
        """Extract metacognition features"""

        # Self-reported difficulty (placeholder - would come from reflection data)
        self_reported_difficulty = 0.5

        # Strategy effectiveness
        strategy_effectiveness = 0.5
        if exercises:
            strategies = Counter([ex.strategy_used for ex in exercises if ex.strategy_used])
            if strategies:
                # Most common strategy
                most_used = strategies.most_common(1)[0][0]
                strategy_exercises = [ex for ex in exercises if ex.strategy_used == most_used]
                if strategy_exercises:
                    strategy_effectiveness = sum(1 for ex in strategy_exercises if ex.is_correct) / len(strategy_exercises)

        return {
            'self_reported_difficulty': self_reported_difficulty,
            'strategy_effectiveness': strategy_effectiveness
        }

    def _encode_demographics(self, user: User) -> Dict[str, float]:
        """Encode demographic features"""

        # Grade level encoding
        grade_mapping = {
            'CE1': 1, 'CE2': 2, 'CM1': 3, 'CM2': 4
        }
        grade_encoded = grade_mapping.get(user.grade_level, 2.5) if user.grade_level else 2.5

        # Learning style encoding
        style_mapping = {
            'visual': 1, 'auditory': 2, 'kinesthetic': 3,
            'logical': 4, 'narrative': 5
        }
        style_encoded = style_mapping.get(user.learning_style, 3) if user.learning_style else 3

        return {
            'grade_level_encoded': grade_encoded,
            'learning_style_encoded': style_encoded
        }

    def _extract_global_stats(self, user_id: int, session) -> Dict[str, float]:
        """Extract global statistics"""

        total = session.query(ExerciseResponse).filter(ExerciseResponse.user_id == user_id).count()
        correct = session.query(ExerciseResponse).filter(
            ExerciseResponse.user_id == user_id,
            ExerciseResponse.is_correct == True
        ).count()

        success_rate = correct / total if total > 0 else 0.0

        return {
            'total_exercises': total,
            'total_correct': correct,
            'overall_success_rate': success_rate
        }

    def _get_default_features(self) -> Dict[str, float]:
        """Return default feature values for new users"""
        return {name: 0.0 for name in self.feature_names}

    def features_to_array(self, features: Dict[str, float]) -> np.ndarray:
        """
        Convert feature dict to numpy array in correct order

        Args:
            features: Feature dictionary

        Returns:
            numpy array of features
        """
        return np.array([features.get(name, 0.0) for name in self.feature_names])

    def get_feature_names(self) -> List[str]:
        """Get list of feature names in order"""
        return self.feature_names.copy()
