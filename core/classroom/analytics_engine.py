"""
AnalyticsEngine - Advanced analytics and insights for teachers

Provides:
- Progress trajectories over time
- Performance heatmaps by domain/difficulty
- ML-powered performance forecasts
- Engagement analytics (time spent, activity patterns)
- Comparative analytics (student vs class average)
- Trend analysis and anomaly detection
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
import numpy as np
from sqlalchemy import and_, func, desc

from database.models import (
    ExerciseResponse, User, SkillProfile,
    StudentCompetencyProgress, ClassroomEnrollment
)
from database.connection import get_session
from core.ml import PerformancePredictor


class AnalyticsEngine:
    """
    Provides comprehensive analytics for teacher dashboard

    Integrates ML predictions with historical data analysis
    """

    def __init__(self):
        """Initialize AnalyticsEngine"""
        self.ml_predictor = PerformancePredictor()

    # ========================================================================
    # PROGRESS TRAJECTORIES
    # ========================================================================

    def get_student_progress_trajectory(
        self,
        student_id: int,
        skill_domain: Optional[str] = None,
        days_back: int = 30,
        granularity: str = 'daily'
    ) -> Dict:
        """
        Get student's progress trajectory over time

        Args:
            student_id: Student ID
            skill_domain: Optional filter by domain
            days_back: Number of days to look back
            granularity: 'daily' or 'weekly'

        Returns:
            Dict with time series data
        """
        with get_session() as session:
            # Get exercise responses in time range
            cutoff_date = datetime.now() - timedelta(days=days_back)

            query = session.query(ExerciseResponse).filter(
                and_(
                    ExerciseResponse.user_id == student_id,
                    ExerciseResponse.created_at >= cutoff_date
                )
            )

            if skill_domain:
                query = query.filter(ExerciseResponse.skill_domain == skill_domain)

            exercises = query.order_by(ExerciseResponse.created_at).all()

            if not exercises:
                return {
                    'student_id': student_id,
                    'skill_domain': skill_domain,
                    'data_points': [],
                    'message': 'Aucune donnée disponible'
                }

            # Group by time period
            time_buckets = defaultdict(lambda: {'total': 0, 'correct': 0, 'time_spent': 0})

            for exercise in exercises:
                # Determine bucket key
                if granularity == 'daily':
                    bucket_key = exercise.created_at.date().isoformat()
                else:  # weekly
                    week_start = exercise.created_at - timedelta(days=exercise.created_at.weekday())
                    bucket_key = week_start.date().isoformat()

                time_buckets[bucket_key]['total'] += 1
                if exercise.is_correct:
                    time_buckets[bucket_key]['correct'] += 1
                if exercise.time_taken_seconds:
                    time_buckets[bucket_key]['time_spent'] += exercise.time_taken_seconds

            # Build trajectory data
            trajectory = []
            for date_key in sorted(time_buckets.keys()):
                bucket = time_buckets[date_key]
                success_rate = bucket['correct'] / bucket['total'] if bucket['total'] > 0 else 0

                trajectory.append({
                    'date': date_key,
                    'exercises_completed': bucket['total'],
                    'success_rate': success_rate,
                    'avg_time_seconds': (
                        bucket['time_spent'] / bucket['total']
                        if bucket['total'] > 0 else 0
                    )
                })

            # Calculate overall trend (linear regression)
            if len(trajectory) >= 2:
                success_rates = [p['success_rate'] for p in trajectory]
                trend = self._calculate_trend(success_rates)
            else:
                trend = 0.0

            return {
                'student_id': student_id,
                'skill_domain': skill_domain,
                'granularity': granularity,
                'days_back': days_back,
                'data_points': trajectory,
                'overall_trend': trend,
                'trend_direction': 'improving' if trend > 0.01 else ('declining' if trend < -0.01 else 'stable')
            }

    def get_class_progress_trajectory(
        self,
        student_ids: List[int],
        skill_domain: Optional[str] = None,
        days_back: int = 30
    ) -> Dict:
        """
        Get aggregated class progress trajectory

        Args:
            student_ids: List of student IDs
            skill_domain: Optional filter by domain
            days_back: Number of days

        Returns:
            Dict with class-wide trajectory
        """
        with get_session() as session:
            cutoff_date = datetime.now() - timedelta(days=days_back)

            query = session.query(ExerciseResponse).filter(
                and_(
                    ExerciseResponse.user_id.in_(student_ids),
                    ExerciseResponse.created_at >= cutoff_date
                )
            )

            if skill_domain:
                query = query.filter(ExerciseResponse.skill_domain == skill_domain)

            exercises = query.all()

            # Group by day
            daily_stats = defaultdict(lambda: {'total': 0, 'correct': 0})

            for exercise in exercises:
                date_key = exercise.created_at.date().isoformat()
                daily_stats[date_key]['total'] += 1
                if exercise.is_correct:
                    daily_stats[date_key]['correct'] += 1

            # Build trajectory
            trajectory = []
            for date_key in sorted(daily_stats.keys()):
                stats = daily_stats[date_key]
                success_rate = stats['correct'] / stats['total'] if stats['total'] > 0 else 0

                trajectory.append({
                    'date': date_key,
                    'exercises_completed': stats['total'],
                    'class_avg_success_rate': success_rate
                })

            return {
                'student_count': len(student_ids),
                'skill_domain': skill_domain,
                'days_back': days_back,
                'data_points': trajectory
            }

    # ========================================================================
    # PERFORMANCE HEATMAPS
    # ========================================================================

    def generate_performance_heatmap(
        self,
        student_id: int,
        days_back: int = 30
    ) -> Dict:
        """
        Generate heatmap showing performance across domains and difficulties

        Args:
            student_id: Student ID
            days_back: Number of days

        Returns:
            Dict with heatmap data (domain x difficulty matrix)
        """
        with get_session() as session:
            cutoff_date = datetime.now() - timedelta(days=days_back)

            exercises = session.query(ExerciseResponse).filter(
                and_(
                    ExerciseResponse.user_id == student_id,
                    ExerciseResponse.created_at >= cutoff_date
                )
            ).all()

            # Build matrix: domain x difficulty
            heatmap_data = defaultdict(lambda: defaultdict(lambda: {'total': 0, 'correct': 0}))

            for exercise in exercises:
                domain = exercise.skill_domain
                difficulty = exercise.difficulty

                heatmap_data[domain][difficulty]['total'] += 1
                if exercise.is_correct:
                    heatmap_data[domain][difficulty]['correct'] += 1

            # Convert to structured format
            heatmap = []
            for domain in sorted(heatmap_data.keys()):
                domain_row = {
                    'domain': domain,
                    'difficulties': []
                }

                for difficulty in range(1, 6):  # D1-D5
                    cell = heatmap_data[domain][difficulty]
                    success_rate = cell['correct'] / cell['total'] if cell['total'] > 0 else None

                    domain_row['difficulties'].append({
                        'difficulty': difficulty,
                        'success_rate': success_rate,
                        'exercises_count': cell['total'],
                        'status': self._classify_performance(success_rate, cell['total'])
                    })

                heatmap.append(domain_row)

            return {
                'student_id': student_id,
                'days_back': days_back,
                'heatmap': heatmap
            }

    def _classify_performance(self, success_rate: Optional[float], count: int) -> str:
        """Classify performance level"""
        if success_rate is None or count < 3:
            return 'insufficient_data'
        elif success_rate >= 0.8:
            return 'excellent'
        elif success_rate >= 0.6:
            return 'good'
        elif success_rate >= 0.4:
            return 'needs_improvement'
        else:
            return 'struggling'

    # ========================================================================
    # ML-POWERED FORECASTS
    # ========================================================================

    def forecast_student_performance(
        self,
        student_id: int,
        skill_domain: str,
        days_ahead: int = 7
    ) -> Dict:
        """
        Forecast student performance using ML

        Args:
            student_id: Student ID
            skill_domain: Skill domain
            days_ahead: Number of days to forecast

        Returns:
            Dict with forecast data
        """
        # Get current success probability
        try:
            current_prob, confidence = self.ml_predictor.predict_success_probability(
                user_id=student_id,
                skill_domain=skill_domain
            )
        except:
            return {
                'error': 'Insufficient data for forecast',
                'student_id': student_id,
                'skill_domain': skill_domain
            }

        # Get historical trend
        trajectory = self.get_student_progress_trajectory(
            student_id=student_id,
            skill_domain=skill_domain,
            days_back=30,
            granularity='daily'
        )

        trend = trajectory.get('overall_trend', 0.0)

        # Simple linear forecast (can be enhanced with ARIMA/Prophet later)
        forecast_points = []
        current_date = datetime.now().date()

        for days_offset in range(1, days_ahead + 1):
            forecast_date = current_date + timedelta(days=days_offset)

            # Project success probability based on trend
            projected_prob = min(1.0, max(0.0, current_prob + (trend * days_offset)))

            forecast_points.append({
                'date': forecast_date.isoformat(),
                'projected_success_rate': projected_prob,
                'confidence': confidence * 0.95 ** days_offset  # Decay confidence
            })

        # Generate recommendation
        if current_prob < 0.5:
            recommendation = f"⚠️ Risque d'échec en {skill_domain} - intervention recommandée"
            risk_level = 'high'
        elif current_prob < 0.7:
            recommendation = f"Suivi nécessaire en {skill_domain}"
            risk_level = 'medium'
        else:
            recommendation = f"✓ Progression normale en {skill_domain}"
            risk_level = 'low'

        return {
            'student_id': student_id,
            'skill_domain': skill_domain,
            'current_success_probability': current_prob,
            'current_confidence': confidence,
            'trend': trajectory.get('trend_direction', 'unknown'),
            'forecast': forecast_points,
            'recommendation': recommendation,
            'risk_level': risk_level
        }

    # ========================================================================
    # ENGAGEMENT ANALYTICS
    # ========================================================================

    def get_student_engagement_metrics(
        self,
        student_id: int,
        days_back: int = 30
    ) -> Dict:
        """
        Analyze student engagement patterns

        Args:
            student_id: Student ID
            days_back: Number of days

        Returns:
            Dict with engagement metrics
        """
        with get_session() as session:
            cutoff_date = datetime.now() - timedelta(days=days_back)

            exercises = session.query(ExerciseResponse).filter(
                and_(
                    ExerciseResponse.user_id == student_id,
                    ExerciseResponse.created_at >= cutoff_date
                )
            ).all()

            if not exercises:
                return {
                    'student_id': student_id,
                    'message': 'Aucune activité récente'
                }

            # Calculate metrics
            total_exercises = len(exercises)
            total_time_seconds = sum(
                ex.time_taken_seconds for ex in exercises
                if ex.time_taken_seconds
            )

            # Active days (days with at least one exercise)
            active_dates = set(ex.created_at.date() for ex in exercises)
            active_days = len(active_dates)

            # Activity by day of week
            weekday_counts = defaultdict(int)
            for ex in exercises:
                weekday_counts[ex.created_at.strftime('%A')] += 1

            # Activity by hour of day
            hour_counts = defaultdict(int)
            for ex in exercises:
                hour_counts[ex.created_at.hour] += 1

            # Find peak activity time
            peak_hour = max(hour_counts.items(), key=lambda x: x[1])[0] if hour_counts else None

            # Calculate streak (consecutive active days)
            current_streak = self._calculate_current_streak(student_id)

            # Engagement score (0-100)
            # Based on: frequency, consistency, time spent
            frequency_score = min(100, (active_days / days_back) * 100)
            consistency_score = min(100, current_streak * 10)
            time_score = min(100, (total_time_seconds / 3600) * 20)  # 1 hour = 20 points

            engagement_score = (frequency_score + consistency_score + time_score) / 3

            return {
                'student_id': student_id,
                'days_back': days_back,
                'total_exercises': total_exercises,
                'active_days': active_days,
                'avg_exercises_per_day': total_exercises / days_back,
                'total_time_minutes': total_time_seconds // 60,
                'avg_time_per_exercise_seconds': (
                    total_time_seconds / total_exercises
                    if total_exercises > 0 else 0
                ),
                'current_streak': current_streak,
                'peak_activity_hour': peak_hour,
                'engagement_score': engagement_score,
                'engagement_level': self._classify_engagement(engagement_score),
                'weekday_distribution': dict(weekday_counts),
                'hour_distribution': dict(hour_counts)
            }

    def _calculate_current_streak(self, student_id: int) -> int:
        """Calculate current consecutive active days"""
        with get_session() as session:
            # Get exercises ordered by date (most recent first)
            exercises = session.query(ExerciseResponse).filter(
                ExerciseResponse.user_id == student_id
            ).order_by(desc(ExerciseResponse.created_at)).all()

            if not exercises:
                return 0

            # Get unique dates
            dates = sorted(set(ex.created_at.date() for ex in exercises), reverse=True)

            # Count consecutive days from today
            streak = 0
            expected_date = datetime.now().date()

            for date in dates:
                if date == expected_date or date == expected_date - timedelta(days=1):
                    streak += 1
                    expected_date = date - timedelta(days=1)
                else:
                    break

            return streak

    def _classify_engagement(self, score: float) -> str:
        """Classify engagement level"""
        if score >= 75:
            return 'excellent'
        elif score >= 50:
            return 'good'
        elif score >= 25:
            return 'moderate'
        else:
            return 'low'

    # ========================================================================
    # COMPARATIVE ANALYTICS
    # ========================================================================

    def compare_student_to_class(
        self,
        student_id: int,
        classroom_student_ids: List[int],
        skill_domain: Optional[str] = None,
        days_back: int = 30
    ) -> Dict:
        """
        Compare student performance to class average

        Args:
            student_id: Student ID
            classroom_student_ids: All student IDs in class
            skill_domain: Optional filter by domain
            days_back: Number of days

        Returns:
            Dict with comparative metrics
        """
        with get_session() as session:
            cutoff_date = datetime.now() - timedelta(days=days_back)

            # Student metrics
            student_query = session.query(ExerciseResponse).filter(
                and_(
                    ExerciseResponse.user_id == student_id,
                    ExerciseResponse.created_at >= cutoff_date
                )
            )

            if skill_domain:
                student_query = student_query.filter(
                    ExerciseResponse.skill_domain == skill_domain
                )

            student_exercises = student_query.all()

            # Class metrics
            class_query = session.query(ExerciseResponse).filter(
                and_(
                    ExerciseResponse.user_id.in_(classroom_student_ids),
                    ExerciseResponse.created_at >= cutoff_date
                )
            )

            if skill_domain:
                class_query = class_query.filter(
                    ExerciseResponse.skill_domain == skill_domain
                )

            class_exercises = class_query.all()

            # Calculate student stats
            student_total = len(student_exercises)
            student_correct = sum(1 for ex in student_exercises if ex.is_correct)
            student_success_rate = student_correct / student_total if student_total > 0 else 0

            # Calculate class stats
            class_total = len(class_exercises)
            class_correct = sum(1 for ex in class_exercises if ex.is_correct)
            class_avg_success_rate = class_correct / class_total if class_total > 0 else 0

            # Calculate percentile rank
            # Get success rates for all students
            student_success_rates = []
            for sid in classroom_student_ids:
                student_exs = [ex for ex in class_exercises if ex.user_id == sid]
                if student_exs:
                    correct = sum(1 for ex in student_exs if ex.is_correct)
                    rate = correct / len(student_exs)
                    student_success_rates.append(rate)

            # Percentile (what % of class this student is better than)
            if student_success_rates:
                better_than_count = sum(
                    1 for rate in student_success_rates
                    if student_success_rate > rate
                )
                percentile = (better_than_count / len(student_success_rates)) * 100
            else:
                percentile = 50.0

            # Relative performance
            if student_success_rate > class_avg_success_rate + 0.1:
                relative_performance = 'above_average'
            elif student_success_rate < class_avg_success_rate - 0.1:
                relative_performance = 'below_average'
            else:
                relative_performance = 'average'

            return {
                'student_id': student_id,
                'skill_domain': skill_domain,
                'student_metrics': {
                    'exercises_completed': student_total,
                    'success_rate': student_success_rate
                },
                'class_metrics': {
                    'student_count': len(classroom_student_ids),
                    'total_exercises': class_total,
                    'avg_success_rate': class_avg_success_rate
                },
                'comparison': {
                    'percentile': percentile,
                    'relative_performance': relative_performance,
                    'difference_from_avg': student_success_rate - class_avg_success_rate
                }
            }

    # ========================================================================
    # TREND ANALYSIS
    # ========================================================================

    def detect_performance_anomalies(
        self,
        student_id: int,
        skill_domain: str,
        days_back: int = 30
    ) -> List[Dict]:
        """
        Detect anomalies in student performance (sudden drops/spikes)

        Args:
            student_id: Student ID
            skill_domain: Skill domain
            days_back: Number of days

        Returns:
            List of detected anomalies
        """
        trajectory = self.get_student_progress_trajectory(
            student_id=student_id,
            skill_domain=skill_domain,
            days_back=days_back,
            granularity='daily'
        )

        data_points = trajectory.get('data_points', [])

        if len(data_points) < 5:
            return []  # Need at least 5 days of data

        # Calculate moving average and standard deviation
        success_rates = [p['success_rate'] for p in data_points]
        moving_avg = np.convolve(success_rates, np.ones(3)/3, mode='valid')
        std_dev = np.std(success_rates)

        anomalies = []

        # Detect anomalies (points more than 2 std devs from moving avg)
        for i, point in enumerate(data_points[1:-1], start=1):
            current_rate = point['success_rate']
            expected_rate = moving_avg[i-1] if i-1 < len(moving_avg) else np.mean(success_rates)

            deviation = abs(current_rate - expected_rate)

            if deviation > 2 * std_dev and std_dev > 0.1:
                anomaly_type = 'sudden_drop' if current_rate < expected_rate else 'sudden_spike'

                anomalies.append({
                    'date': point['date'],
                    'type': anomaly_type,
                    'actual_success_rate': current_rate,
                    'expected_success_rate': expected_rate,
                    'deviation': deviation,
                    'severity': 'high' if deviation > 3 * std_dev else 'medium'
                })

        return anomalies

    def _calculate_trend(self, values: List[float]) -> float:
        """Calculate linear trend (slope of best-fit line)"""
        if len(values) < 2:
            return 0.0

        n = len(values)
        x = np.arange(n)
        y = np.array(values)

        # Linear regression: y = mx + b
        slope = (n * np.sum(x * y) - np.sum(x) * np.sum(y)) / (n * np.sum(x**2) - np.sum(x)**2)

        return float(slope)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_class_leaderboard(
    classroom_student_ids: List[int],
    skill_domain: Optional[str] = None,
    days_back: int = 30,
    top_n: int = 10
) -> List[Dict]:
    """
    Generate class leaderboard

    Args:
        classroom_student_ids: Student IDs in class
        skill_domain: Optional filter by domain
        days_back: Number of days
        top_n: Number of top students to return

    Returns:
        List of student rankings
    """
    with get_session() as session:
        cutoff_date = datetime.now() - timedelta(days=days_back)

        # Get all exercises for class
        query = session.query(ExerciseResponse).filter(
            and_(
                ExerciseResponse.user_id.in_(classroom_student_ids),
                ExerciseResponse.created_at >= cutoff_date
            )
        )

        if skill_domain:
            query = query.filter(ExerciseResponse.skill_domain == skill_domain)

        exercises = query.all()

        # Calculate stats per student
        student_stats = defaultdict(lambda: {'total': 0, 'correct': 0})

        for ex in exercises:
            student_stats[ex.user_id]['total'] += 1
            if ex.is_correct:
                student_stats[ex.user_id]['correct'] += 1

        # Build leaderboard
        leaderboard = []
        for student_id in classroom_student_ids:
            stats = student_stats[student_id]

            if stats['total'] > 0:
                success_rate = stats['correct'] / stats['total']

                # Get student info
                student = session.query(User).filter(User.id == student_id).first()

                leaderboard.append({
                    'student_id': student_id,
                    'username': student.username if student else f"Student {student_id}",
                    'exercises_completed': stats['total'],
                    'success_rate': success_rate,
                    'score': success_rate * stats['total']  # Weighted score
                })

        # Sort by score
        leaderboard.sort(key=lambda x: x['score'], reverse=True)

        # Add ranks
        for rank, student in enumerate(leaderboard[:top_n], start=1):
            student['rank'] = rank

        return leaderboard[:top_n]
