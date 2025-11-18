"""
DifficultyOptimizer - ML model for optimal difficulty prediction
Uses Gradient Boosting (XGBoost) to predict optimal difficulty level (1-5)

Implements Flow Theory: maintains 70% success rate for optimal learning
"""

import os
import pickle
from datetime import datetime
from typing import Dict, Optional, Tuple
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, r2_score
import xgboost as xgb

from core.ml.feature_engineering import FeatureEngineering
from database.models import ExerciseResponse, MLModel
from database.connection import get_session


class DifficultyOptimizer:
    """
    Predicts optimal difficulty level for a user on a given skill domain

    Uses XGBoost regression to predict difficulty 1-5, with Flow Theory adjustment
    """

    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize DifficultyOptimizer

        Args:
            model_path: Path to saved model file (.pkl)
        """
        self.feature_engineer = FeatureEngineering()
        self.model: Optional[xgb.XGBRegressor] = None
        self.model_version = "v1.0"
        self.model_path = model_path or "models/difficulty_optimizer_v1.pkl"

        self.flow_target = 0.70  # 70% success rate for optimal flow
        self.flow_tolerance = 0.15  # ±15% tolerance

        # Hyperparameters
        self.hyperparameters = {
            'n_estimators': 100,
            'max_depth': 5,
            'learning_rate': 0.1,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'random_state': 42,
            'objective': 'reg:squarederror'
        }

        # Load model if exists
        if os.path.exists(self.model_path):
            self.load_model(self.model_path)

    def train(
        self,
        X: np.ndarray,
        y: np.ndarray,
        test_size: float = 0.2,
        cv_folds: int = 5
    ) -> Dict[str, float]:
        """
        Train the difficulty optimization model

        Args:
            X: Feature matrix (n_samples, n_features)
            y: Target difficulty levels (n_samples,)
            test_size: Proportion of data for testing
            cv_folds: Number of cross-validation folds

        Returns:
            Dict of training metrics
        """
        print("🤖 Training DifficultyOptimizer...")

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )

        # Initialize model
        self.model = xgb.XGBRegressor(**self.hyperparameters)

        # Train
        self.model.fit(
            X_train, y_train,
            eval_set=[(X_test, y_test)],
            verbose=False
        )

        # Evaluate
        train_pred = self.model.predict(X_train)
        test_pred = self.model.predict(X_test)

        metrics = {
            'train_mae': mean_absolute_error(y_train, train_pred),
            'test_mae': mean_absolute_error(y_test, test_pred),
            'train_r2': r2_score(y_train, train_pred),
            'test_r2': r2_score(y_test, test_pred),
            'n_samples': len(X),
            'n_features': X.shape[1]
        }

        # Cross-validation
        cv_scores = cross_val_score(
            self.model, X, y,
            cv=cv_folds,
            scoring='neg_mean_absolute_error'
        )
        metrics['cv_mae_mean'] = -cv_scores.mean()
        metrics['cv_mae_std'] = cv_scores.std()

        print(f"✓ Training completed")
        print(f"  Test MAE: {metrics['test_mae']:.3f}")
        print(f"  Test R²: {metrics['test_r2']:.3f}")
        print(f"  CV MAE: {metrics['cv_mae_mean']:.3f} ± {metrics['cv_mae_std']:.3f}")

        return metrics

    def predict(
        self,
        user_id: int,
        skill_domain: str,
        apply_flow_adjustment: bool = True
    ) -> Tuple[int, Dict]:
        """
        Predict optimal difficulty for a user

        Args:
            user_id: User ID
            skill_domain: Skill domain (e.g., 'addition')
            apply_flow_adjustment: Whether to apply Flow Theory adjustment

        Returns:
            Tuple of (difficulty_level, explanation_dict)
        """
        if self.model is None:
            # No model trained, return default
            return 3, {
                'difficulty': 3,
                'source': 'default',
                'reason': 'No ML model available'
            }

        # Extract features
        features = self.feature_engineer.extract_features(user_id, skill_domain)
        X = self.feature_engineer.features_to_array(features)

        # Predict (continuous)
        difficulty_continuous = self.model.predict(X.reshape(1, -1))[0]

        # Apply Flow Theory adjustment
        if apply_flow_adjustment:
            recent_success_rate = features.get('recent_success_rate', 0.5)
            difficulty_continuous = self._apply_flow_adjustment(
                difficulty_continuous,
                recent_success_rate
            )

        # Discretize to 1-5
        difficulty_level = self._discretize_difficulty(difficulty_continuous)

        # Build explanation
        explanation = self._build_explanation(
            difficulty_level,
            features,
            difficulty_continuous,
            recent_success_rate if apply_flow_adjustment else None
        )

        return difficulty_level, explanation

    def _apply_flow_adjustment(
        self,
        difficulty: float,
        current_success_rate: float
    ) -> float:
        """
        Apply Flow Theory adjustment to maintain optimal challenge

        Args:
            difficulty: Predicted difficulty
            current_success_rate: Recent success rate (0-1)

        Returns:
            Adjusted difficulty
        """
        # Too easy (success rate too high)
        if current_success_rate > self.flow_target + self.flow_tolerance:
            difficulty += 0.5  # Increase difficulty

        # Too hard (success rate too low)
        elif current_success_rate < self.flow_target - self.flow_tolerance:
            difficulty -= 0.5  # Decrease difficulty

        return difficulty

    def _discretize_difficulty(self, difficulty_continuous: float) -> int:
        """
        Convert continuous difficulty to discrete level (1-5)

        Args:
            difficulty_continuous: Continuous difficulty prediction

        Returns:
            Integer difficulty 1-5
        """
        # Clip and round
        difficulty = np.clip(difficulty_continuous, 1.0, 5.0)
        return int(round(difficulty))

    def _build_explanation(
        self,
        difficulty: int,
        features: Dict[str, float],
        raw_prediction: float,
        success_rate: Optional[float]
    ) -> Dict:
        """
        Build human-readable explanation of difficulty choice

        Args:
            difficulty: Final difficulty level
            features: Feature dictionary
            raw_prediction: Raw model prediction
            success_rate: Recent success rate

        Returns:
            Explanation dictionary
        """
        explanation = {
            'difficulty': difficulty,
            'raw_prediction': raw_prediction,
            'source': 'ml_model',
            'model_version': self.model_version,
            'reasons': []
        }

        # Analyze features for explanation
        if success_rate is not None:
            if success_rate > 0.85:
                explanation['reasons'].append("✓ Tu réussis très bien (+85%)")
            elif success_rate > 0.70:
                explanation['reasons'].append("✓ Tu réussis bien (+70%)")
            elif success_rate < 0.55:
                explanation['reasons'].append("📉 Un peu difficile pour toi")

        if features.get('trend_7d', 0) > 0.1:
            explanation['reasons'].append("📈 Tu t'améliores")
        elif features.get('trend_7d', 0) < -0.1:
            explanation['reasons'].append("📉 Un peu de difficulté récemment")

        if features.get('fatigue_level', 0) > 0.3:
            explanation['reasons'].append("😴 Tu sembles un peu fatigué")

        if features.get('prerequisite_mastery', 0) > 0.8:
            explanation['reasons'].append("🎯 Prérequis bien maîtrisés")

        if features.get('streak', 0) >= 3:
            explanation['reasons'].append(f"🔥 Série de {int(features['streak'])} succès!")

        return explanation

    def get_feature_importance(self, top_n: int = 10) -> pd.DataFrame:
        """
        Get feature importance scores

        Args:
            top_n: Number of top features to return

        Returns:
            DataFrame with feature names and importance scores
        """
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
        """
        Save trained model to disk

        Args:
            filepath: Path to save model (.pkl)
        """
        filepath = filepath or self.model_path

        if self.model is None:
            print("⚠️  No model to save")
            return

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        model_data = {
            'model': self.model,
            'version': self.model_version,
            'hyperparameters': self.hyperparameters,
            'trained_at': datetime.now().isoformat()
        }

        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)

        print(f"✓ Model saved to: {filepath}")

    def load_model(self, filepath: str):
        """
        Load trained model from disk

        Args:
            filepath: Path to model file
        """
        if not os.path.exists(filepath):
            print(f"⚠️  Model file not found: {filepath}")
            return

        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)

        self.model = model_data['model']
        self.model_version = model_data.get('version', 'unknown')
        self.hyperparameters = model_data.get('hyperparameters', {})

        print(f"✓ Model loaded: {filepath} (version {self.model_version})")

    def register_model_in_db(self, metrics: Dict[str, float]):
        """
        Register trained model in database

        Args:
            metrics: Training metrics
        """
        with get_session() as session:
            # Deactivate previous models
            session.query(MLModel).filter(
                MLModel.model_name == 'DifficultyOptimizer'
            ).update({'is_active': False})

            # Register new model
            model_record = MLModel(
                model_name='DifficultyOptimizer',
                model_version=self.model_version,
                model_type='xgboost',
                training_date=datetime.now(),
                accuracy_metrics=metrics,
                model_path=self.model_path,
                is_active=True
            )

            session.add(model_record)
            session.commit()

            print(f"✓ Model registered in database (ID: {model_record.id})")


# Training script example
def train_difficulty_optimizer_from_db():
    """
    Train DifficultyOptimizer from historical database data

    This would be run periodically to retrain the model
    """
    print("=" * 60)
    print("Training DifficultyOptimizer from database")
    print("=" * 60)

    feature_engineer = FeatureEngineering()

    # TODO: Extract training data from database
    # This is a placeholder - would need to collect historical data
    # where we know the difficulty that was used and the outcome

    print("⚠️  Training data collection not yet implemented")
    print("Would need historical (user, domain, difficulty, outcome) data")

    # Placeholder for demonstration
    # X, y = collect_training_data_from_db()
    # optimizer = DifficultyOptimizer()
    # metrics = optimizer.train(X, y)
    # optimizer.save_model()
    # optimizer.register_model_in_db(metrics)


if __name__ == "__main__":
    # Example usage
    optimizer = DifficultyOptimizer()

    # Predict for a user
    # difficulty, explanation = optimizer.predict(user_id=1, skill_domain='addition')
    # print(f"Recommended difficulty: D{difficulty}")
    # print("Reasons:", explanation['reasons'])
