"""
PerformancePredictor - ML for predicting student success and identifying at-risk learners

Uses Random Forest classifier for:
1. Success probability prediction
2. At-risk learner detection
3. Mastery timeline estimation
"""

import os
import pickle
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, classification_report
)
from imblearn.over_sampling import SMOTE

from core.ml.feature_engineering import FeatureEngineering
from database.models import ExerciseResponse, SkillProfile, MLModel
from database.connection import get_session


class PerformancePredictor:
    """
    Predicts student performance and identifies at-risk learners

    Uses Random Forest for binary classification (success/failure prediction)
    """

    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize PerformancePredictor

        Args:
            model_path: Path to saved model file
        """
        self.feature_engineer = FeatureEngineering()
        self.model: Optional[RandomForestClassifier] = None
        self.model_version = "v1.0"
        self.model_path = model_path or "models/performance_predictor_v1.pkl"

        # At-risk threshold
        self.at_risk_threshold = 0.60  # 60% risk threshold

        # Hyperparameters
        self.hyperparameters = {
            'n_estimators': 100,
            'max_depth': 10,
            'min_samples_split': 5,
            'min_samples_leaf': 2,
            'max_features': 'sqrt',
            'random_state': 42,
            'class_weight': 'balanced'  # Handle imbalanced classes
        }

        # Load model if exists
        if os.path.exists(self.model_path):
            self.load_model(self.model_path)

    def train(
        self,
        X: np.ndarray,
        y: np.ndarray,
        test_size: float = 0.2,
        cv_folds: int = 5,
        use_smote: bool = True
    ) -> Dict[str, float]:
        """
        Train the performance prediction model

        Args:
            X: Feature matrix
            y: Target labels (0=failure, 1=success)
            test_size: Test split proportion
            cv_folds: Cross-validation folds
            use_smote: Whether to use SMOTE for class balancing

        Returns:
            Dict of training metrics
        """
        print("🤖 Training PerformancePredictor...")

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )

        # Handle class imbalance with SMOTE
        if use_smote:
            print("  Applying SMOTE for class balancing...")
            smote = SMOTE(random_state=42)
            X_train, y_train = smote.fit_resample(X_train, y_train)

        # Initialize model
        self.model = RandomForestClassifier(**self.hyperparameters)

        # Train
        self.model.fit(X_train, y_train)

        # Evaluate
        train_pred = self.model.predict(X_train)
        test_pred = self.model.predict(X_test)
        test_proba = self.model.predict_proba(X_test)[:, 1]

        metrics = {
            'train_accuracy': accuracy_score(y_train, train_pred),
            'test_accuracy': accuracy_score(y_test, test_pred),
            'test_precision': precision_score(y_test, test_pred, zero_division=0),
            'test_recall': recall_score(y_test, test_pred, zero_division=0),
            'test_f1': f1_score(y_test, test_pred, zero_division=0),
            'test_auc': roc_auc_score(y_test, test_proba),
            'n_samples': len(X),
            'n_features': X.shape[1],
            'class_distribution': {
                'train': {
                    'failure': int((y_train == 0).sum()),
                    'success': int((y_train == 1).sum())
                },
                'test': {
                    'failure': int((y_test == 0).sum()),
                    'success': int((y_test == 1).sum())
                }
            }
        }

        # Cross-validation
        cv_scores = cross_val_score(
            self.model, X, y,
            cv=cv_folds,
            scoring='roc_auc'
        )
        metrics['cv_auc_mean'] = cv_scores.mean()
        metrics['cv_auc_std'] = cv_scores.std()

        print(f"✓ Training completed")
        print(f"  Test Accuracy: {metrics['test_accuracy']:.3f}")
        print(f"  Test AUC: {metrics['test_auc']:.3f}")
        print(f"  Test Recall: {metrics['test_recall']:.3f}")
        print(f"  CV AUC: {metrics['cv_auc_mean']:.3f} ± {metrics['cv_auc_std']:.3f}")

        return metrics

    def predict_success_probability(
        self,
        user_id: int,
        skill_domain: str
    ) -> Tuple[float, Dict]:
        """
        Predict probability of success on next exercise

        Args:
            user_id: User ID
            skill_domain: Skill domain

        Returns:
            Tuple of (success_probability, explanation_dict)
        """
        if self.model is None:
            return 0.5, {
                'probability': 0.5,
                'source': 'default',
                'reason': 'No ML model available'
            }

        # Extract features
        features = self.feature_engineer.extract_features(user_id, skill_domain)
        X = self.feature_engineer.features_to_array(features)

        # Predict probability
        success_probability = self.model.predict_proba(X.reshape(1, -1))[0][1]

        # Build explanation
        explanation = {
            'probability': float(success_probability),
            'confidence_level': self._get_confidence_level(success_probability),
            'source': 'ml_model',
            'model_version': self.model_version,
            'interpretation': self._interpret_probability(success_probability)
        }

        return success_probability, explanation

    def identify_at_risk_learners(
        self,
        user_ids: List[int],
        skill_domain: str,
        horizon_days: int = 7
    ) -> List[Dict]:
        """
        Identify learners at risk of failure

        Args:
            user_ids: List of user IDs to check
            skill_domain: Skill domain
            horizon_days: Prediction horizon (days)

        Returns:
            List of at-risk learner dicts
        """
        at_risk_learners = []

        for user_id in user_ids:
            try:
                # Predict success probability
                success_prob, _ = self.predict_success_probability(user_id, skill_domain)

                # At-risk if probability < threshold
                risk_score = 1.0 - success_prob

                if risk_score >= self.at_risk_threshold:
                    # Get user details
                    with get_session() as session:
                        from database.models import User
                        user = session.query(User).filter(User.id == user_id).first()

                        at_risk_learners.append({
                            'user_id': user_id,
                            'username': user.username if user else f"User {user_id}",
                            'skill_domain': skill_domain,
                            'risk_score': risk_score,
                            'success_probability': success_prob,
                            'risk_level': self._get_risk_level(risk_score),
                            'recommended_action': self._recommend_intervention(risk_score)
                        })

            except Exception as e:
                print(f"⚠️  Error analyzing user {user_id}: {e}")

        # Sort by risk score (highest first)
        at_risk_learners.sort(key=lambda x: x['risk_score'], reverse=True)

        return at_risk_learners

    def predict_mastery_timeline(
        self,
        user_id: int,
        skill_domain: str,
        target_proficiency: float = 0.8
    ) -> Dict:
        """
        Predict when user will achieve mastery

        Args:
            user_id: User ID
            skill_domain: Skill domain
            target_proficiency: Target proficiency level (default 0.8 = 80%)

        Returns:
            Dict with timeline prediction
        """
        with get_session() as session:
            # Get current proficiency
            skill_profile = session.query(SkillProfile).filter(
                SkillProfile.user_id == user_id,
                SkillProfile.skill_domain == skill_domain
            ).first()

            if not skill_profile:
                return {
                    'status': 'no_data',
                    'message': 'No skill profile found'
                }

            current_proficiency = skill_profile.proficiency_level

            if current_proficiency >= target_proficiency:
                return {
                    'status': 'mastered',
                    'current_proficiency': current_proficiency,
                    'message': 'Already achieved mastery!'
                }

            # Get learning velocity from features
            features = self.feature_engineer.extract_features(user_id, skill_domain)
            learning_velocity = features.get('learning_velocity', 0.01)

            # Prevent division by zero
            if learning_velocity <= 0:
                learning_velocity = 0.01  # Minimum velocity

            # Calculate exercises needed
            proficiency_gap = target_proficiency - current_proficiency
            exercises_needed = int(proficiency_gap / learning_velocity)

            # Estimate days (assuming 2 exercises per day)
            exercises_per_day = 2
            days_to_mastery = int(exercises_needed / exercises_per_day)

            # Predict date
            mastery_date = datetime.now() + timedelta(days=days_to_mastery)

            return {
                'status': 'predicted',
                'current_proficiency': current_proficiency,
                'target_proficiency': target_proficiency,
                'exercises_needed': exercises_needed,
                'estimated_days': days_to_mastery,
                'estimated_date': mastery_date.strftime('%Y-%m-%d'),
                'learning_velocity': learning_velocity,
                'confidence': 'medium'  # Could be calculated based on data quality
            }

    def _get_confidence_level(self, probability: float) -> str:
        """Get confidence level from probability"""
        if probability > 0.8 or probability < 0.2:
            return 'high'
        elif probability > 0.6 or probability < 0.4:
            return 'medium'
        else:
            return 'low'

    def _interpret_probability(self, probability: float) -> str:
        """Human-readable interpretation of success probability"""
        if probability >= 0.85:
            return "Très probable de réussir"
        elif probability >= 0.70:
            return "Probable de réussir"
        elif probability >= 0.50:
            return "Chances moyennes"
        elif probability >= 0.30:
            return "Risque d'échec"
        else:
            return "Risque élevé d'échec"

    def _get_risk_level(self, risk_score: float) -> str:
        """Classify risk level"""
        if risk_score >= 0.8:
            return 'critical'
        elif risk_score >= 0.6:
            return 'high'
        elif risk_score >= 0.4:
            return 'medium'
        else:
            return 'low'

    def _recommend_intervention(self, risk_score: float) -> str:
        """Recommend intervention based on risk score"""
        if risk_score >= 0.8:
            return "Intervention immédiate recommandée - revoir les bases"
        elif risk_score >= 0.6:
            return "Suivi rapproché et exercices de renforcement"
        elif risk_score >= 0.4:
            return "Exercices de révision conseillés"
        else:
            return "Continuer avec suivi régulier"

    def get_feature_importance(self, top_n: int = 10) -> pd.DataFrame:
        """Get feature importance scores"""
        if self.model is None:
            return pd.DataFrame()

        importance = self.model.feature_importances_
        feature_names = self.feature_engineer.get_feature_names()

        df = pd.DataFrame({
            'feature': feature_names,
            'importance': importance
        }).sort_values('importance', ascending=False).head(top_n)

        return df

    def save_model(self, filepath: Optional[str] = None):
        """Save trained model to disk"""
        filepath = filepath or self.model_path

        if self.model is None:
            print("⚠️  No model to save")
            return

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        model_data = {
            'model': self.model,
            'version': self.model_version,
            'hyperparameters': self.hyperparameters,
            'at_risk_threshold': self.at_risk_threshold,
            'trained_at': datetime.now().isoformat()
        }

        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)

        print(f"✓ Model saved to: {filepath}")

    def load_model(self, filepath: str):
        """Load trained model from disk"""
        if not os.path.exists(filepath):
            print(f"⚠️  Model file not found: {filepath}")
            return

        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)

        self.model = model_data['model']
        self.model_version = model_data.get('version', 'unknown')
        self.hyperparameters = model_data.get('hyperparameters', {})
        self.at_risk_threshold = model_data.get('at_risk_threshold', 0.60)

        print(f"✓ Model loaded: {filepath} (version {self.model_version})")

    def register_model_in_db(self, metrics: Dict[str, float]):
        """Register trained model in database"""
        with get_session() as session:
            # Deactivate previous models
            session.query(MLModel).filter(
                MLModel.model_name == 'PerformancePredictor'
            ).update({'is_active': False})

            # Register new model
            model_record = MLModel(
                model_name='PerformancePredictor',
                model_version=self.model_version,
                model_type='random_forest',
                training_date=datetime.now(),
                accuracy_metrics=metrics,
                model_path=self.model_path,
                is_active=True
            )

            session.add(model_record)
            session.commit()

            print(f"✓ Model registered in database (ID: {model_record.id})")


if __name__ == "__main__":
    # Example usage
    predictor = PerformancePredictor()

    # Predict success for a user
    # prob, explanation = predictor.predict_success_probability(user_id=1, skill_domain='addition')
    # print(f"Success probability: {prob:.1%}")
    # print(f"Interpretation: {explanation['interpretation']}")

    # Identify at-risk learners
    # at_risk = predictor.identify_at_risk_learners(user_ids=[1, 2, 3], skill_domain='addition')
    # for learner in at_risk:
    #     print(f"{learner['username']}: Risk {learner['risk_level']} ({learner['risk_score']:.0%})")
