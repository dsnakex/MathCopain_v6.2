"""
Analytics Engine for MathCopain Phase 7

Provides comprehensive analytics and performance insights for students.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from database.connection import DatabaseSession
from database.models import User, ExerciseResponse, SkillProfile


class AnalyticsEngine:
    """
    Engine for generating student analytics and performance insights.

    Provides methods for:
    - Progress trajectory tracking
    - Performance heatmaps
    - Engagement metrics
    - Performance forecasting
    """

    def __init__(self):
        """Initialize the analytics engine"""
        self.skill_domains = ['addition', 'soustraction', 'multiplication', 'division', 'fractions']

    def get_student_progress_trajectory(
        self,
        student_id: int,
        skill_domain: str,
        days_back: int = 30,
        granularity: str = 'daily'
    ) -> Optional[Dict[str, Any]]:
        """
        Get student's progress trajectory over time.

        Args:
            student_id: Student's user ID
            skill_domain: Mathematical domain to analyze
            days_back: Number of days to look back
            granularity: 'daily' or 'weekly'

        Returns:
            Dictionary with trajectory data and trend analysis
        """
        try:
            with DatabaseSession() as session:
                start_date = datetime.now() - timedelta(days=days_back)

                # Get exercise responses
                responses = session.query(ExerciseResponse).filter(
                    ExerciseResponse.user_id == student_id,
                    ExerciseResponse.skill_domain == skill_domain,
                    ExerciseResponse.created_at >= start_date
                ).order_by(ExerciseResponse.created_at).all()

                if not responses:
                    return None

                # Group by date
                daily_data = {}
                for response in responses:
                    date_key = response.created_at.strftime('%Y-%m-%d')
                    if date_key not in daily_data:
                        daily_data[date_key] = {'correct': 0, 'total': 0}
                    daily_data[date_key]['total'] += 1
                    if response.is_correct:
                        daily_data[date_key]['correct'] += 1

                # Build data points
                data_points = []
                for date_str, data in sorted(daily_data.items()):
                    success_rate = data['correct'] / data['total'] if data['total'] > 0 else 0
                    data_points.append({
                        'date': date_str,
                        'success_rate': success_rate,
                        'exercises_completed': data['total']
                    })

                # Determine trend
                if len(data_points) >= 2:
                    first_half = sum(p['success_rate'] for p in data_points[:len(data_points)//2]) / (len(data_points)//2)
                    second_half = sum(p['success_rate'] for p in data_points[len(data_points)//2:]) / (len(data_points) - len(data_points)//2)

                    if second_half > first_half + 0.05:
                        trend = 'improving'
                    elif second_half < first_half - 0.05:
                        trend = 'declining'
                    else:
                        trend = 'stable'
                else:
                    trend = 'insufficient_data'

                return {
                    'data_points': data_points,
                    'trend_direction': trend,
                    'total_exercises': sum(p['exercises_completed'] for p in data_points)
                }

        except Exception as e:
            print(f"Error getting progress trajectory: {e}")
            return None

    def generate_performance_heatmap(
        self,
        student_id: int,
        days_back: int = 30
    ) -> Optional[Dict[str, Any]]:
        """
        Generate a performance heatmap showing success rates by domain and difficulty.

        Args:
            student_id: Student's user ID
            days_back: Number of days to analyze

        Returns:
            Dictionary with heatmap data
        """
        try:
            with DatabaseSession() as session:
                start_date = datetime.now() - timedelta(days=days_back)

                # Get all responses
                responses = session.query(ExerciseResponse).filter(
                    ExerciseResponse.user_id == student_id,
                    ExerciseResponse.created_at >= start_date
                ).all()

                if not responses:
                    return None

                # Build heatmap
                heatmap_data = {}
                for domain in self.skill_domains:
                    heatmap_data[domain] = {i: {'correct': 0, 'total': 0} for i in range(1, 6)}

                for response in responses:
                    domain = response.skill_domain
                    difficulty = response.difficulty_level

                    if domain in heatmap_data and 1 <= difficulty <= 5:
                        heatmap_data[domain][difficulty]['total'] += 1
                        if response.is_correct:
                            heatmap_data[domain][difficulty]['correct'] += 1

                # Format output
                heatmap = []
                for domain in self.skill_domains:
                    difficulties = []
                    for diff in range(1, 6):
                        data = heatmap_data[domain][diff]
                        if data['total'] > 0:
                            rate = data['correct'] / data['total']
                            status = 'excellent' if rate >= 0.8 else 'good' if rate >= 0.6 else 'needs_work'
                        else:
                            rate = None
                            status = 'no_data'

                        difficulties.append({
                            'difficulty': diff,
                            'success_rate': rate,
                            'status': status,
                            'count': data['total']
                        })

                    heatmap.append({
                        'domain': domain,
                        'difficulties': difficulties
                    })

                return {'heatmap': heatmap}

        except Exception as e:
            print(f"Error generating heatmap: {e}")
            return None

    def get_student_engagement_metrics(
        self,
        student_id: int,
        days_back: int = 30
    ) -> Optional[Dict[str, Any]]:
        """
        Get student engagement metrics.

        Args:
            student_id: Student's user ID
            days_back: Number of days to analyze

        Returns:
            Dictionary with engagement metrics
        """
        try:
            with DatabaseSession() as session:
                start_date = datetime.now() - timedelta(days=days_back)

                # Get exercise responses
                responses = session.query(ExerciseResponse).filter(
                    ExerciseResponse.user_id == student_id,
                    ExerciseResponse.created_at >= start_date
                ).order_by(ExerciseResponse.created_at).all()

                if not responses:
                    return None

                # Calculate metrics
                total_exercises = len(responses)

                # Active days
                active_dates = set(r.created_at.strftime('%Y-%m-%d') for r in responses)
                active_days = len(active_dates)

                # Current streak
                today = datetime.now().date()
                streak = 0
                current_date = today

                while current_date.strftime('%Y-%m-%d') in active_dates:
                    streak += 1
                    current_date -= timedelta(days=1)

                # Engagement score (0-100)
                # Based on: frequency, consistency, volume
                frequency_score = min(active_days / days_back * 100, 100)
                volume_score = min(total_exercises / (days_back * 5) * 100, 100)  # 5 exercises/day = 100%
                streak_bonus = min(streak * 5, 20)  # Up to 20 bonus points for streak

                engagement_score = (frequency_score * 0.4 + volume_score * 0.4 + streak_bonus)

                # Engagement level
                if engagement_score >= 80:
                    level = 'excellent'
                elif engagement_score >= 60:
                    level = 'good'
                elif engagement_score >= 40:
                    level = 'moderate'
                else:
                    level = 'low'

                return {
                    'engagement_score': engagement_score,
                    'engagement_level': level,
                    'active_days': active_days,
                    'total_exercises': total_exercises,
                    'current_streak': streak,
                    'avg_exercises_per_day': total_exercises / active_days if active_days > 0 else 0
                }

        except Exception as e:
            print(f"Error getting engagement metrics: {e}")
            return None

    def forecast_student_performance(
        self,
        student_id: int,
        skill_domain: str,
        days_ahead: int = 7
    ) -> Optional[Dict[str, Any]]:
        """
        Forecast student performance for the next N days.

        Args:
            student_id: Student's user ID
            skill_domain: Mathematical domain to forecast
            days_ahead: Number of days to forecast

        Returns:
            Dictionary with forecast data
        """
        try:
            with DatabaseSession() as session:
                # Get recent performance
                start_date = datetime.now() - timedelta(days=30)

                responses = session.query(ExerciseResponse).filter(
                    ExerciseResponse.user_id == student_id,
                    ExerciseResponse.skill_domain == skill_domain,
                    ExerciseResponse.created_at >= start_date
                ).order_by(ExerciseResponse.created_at).all()

                if not responses:
                    return None

                # Calculate current success rate
                correct = sum(1 for r in responses if r.is_correct)
                total = len(responses)
                current_rate = correct / total if total > 0 else 0

                # Simple trend analysis
                recent_responses = responses[-10:] if len(responses) >= 10 else responses
                recent_correct = sum(1 for r in recent_responses if r.is_correct)
                recent_rate = recent_correct / len(recent_responses) if recent_responses else current_rate

                # Determine trend
                if recent_rate > current_rate + 0.05:
                    trend = 'improving'
                    trend_factor = 0.02  # 2% improvement per day
                elif recent_rate < current_rate - 0.05:
                    trend = 'declining'
                    trend_factor = -0.01  # 1% decline per day
                else:
                    trend = 'stable'
                    trend_factor = 0

                # Generate forecast
                forecast = []
                for i in range(1, days_ahead + 1):
                    forecast_date = datetime.now() + timedelta(days=i)
                    projected_rate = min(max(current_rate + (trend_factor * i), 0), 1)

                    forecast.append({
                        'date': forecast_date.strftime('%Y-%m-%d'),
                        'projected_success_rate': projected_rate,
                        'confidence': max(0.9 - (i * 0.05), 0.5)  # Confidence decreases over time
                    })

                # Risk assessment
                if current_rate < 0.5:
                    risk_level = 'high'
                    recommendation = f"Focus on {skill_domain} fundamentals. Consider reviewing basic concepts."
                elif current_rate < 0.7:
                    risk_level = 'medium'
                    recommendation = f"Good progress in {skill_domain}. Practice regularly to improve."
                else:
                    risk_level = 'low'
                    recommendation = f"Excellent performance in {skill_domain}. Try more challenging exercises."

                return {
                    'current_success_probability': current_rate,
                    'current_confidence': 0.85,
                    'risk_level': risk_level,
                    'trend': trend,
                    'forecast': forecast,
                    'recommendation': recommendation
                }

        except Exception as e:
            print(f"Error forecasting performance: {e}")
            return None

    def get_class_overview(
        self,
        classroom_id: int,
        days_back: int = 30
    ) -> Optional[Dict[str, Any]]:
        """
        Get overview analytics for an entire classroom.

        Args:
            classroom_id: Classroom ID
            days_back: Number of days to analyze

        Returns:
            Dictionary with class overview data
        """
        # This would be implemented for teacher dashboard
        # For now, return placeholder
        return {
            'total_students': 0,
            'avg_engagement': 0,
            'avg_success_rate': 0,
            'top_performers': [],
            'needs_attention': []
        }
