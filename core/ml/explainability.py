"""
Explainable AI (XAI) module for MathCopain ML models
Uses SHAP (SHapley Additive exPlanations) for model interpretability

Features:
1. Explain individual predictions
2. Feature importance analysis
3. Fairness audit across demographics
4. Bias detection
"""

from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
import shap

from core.ml.difficulty_optimizer import DifficultyOptimizer
from core.ml.performance_predictor import PerformancePredictor
from core.ml.feature_engineering import FeatureEngineering


class ExplainableAI:
    """
    Provides explainability and fairness analysis for ML models
    """

    def __init__(
        self,
        difficulty_optimizer: Optional[DifficultyOptimizer] = None,
        performance_predictor: Optional[PerformancePredictor] = None
    ):
        """
        Initialize ExplainableAI

        Args:
            difficulty_optimizer: DifficultyOptimizer instance
            performance_predictor: PerformancePredictor instance
        """
        self.difficulty_optimizer = difficulty_optimizer or DifficultyOptimizer()
        self.performance_predictor = performance_predictor or PerformancePredictor()
        self.feature_engineer = FeatureEngineering()

        # SHAP explainers (initialized lazily)
        self._difficulty_explainer: Optional[shap.TreeExplainer] = None
        self._performance_explainer: Optional[shap.TreeExplainer] = None

    def explain_difficulty_prediction(
        self,
        user_id: int,
        skill_domain: str,
        top_n: int = 5
    ) -> Dict:
        """
        Explain why a particular difficulty was recommended

        Args:
            user_id: User ID
            skill_domain: Skill domain
            top_n: Number of top contributing features

        Returns:
            Dict with explanation
        """
        if self.difficulty_optimizer.model is None:
            return {
                'error': 'No difficulty model available'
            }

        # Get features
        features = self.feature_engineer.extract_features(user_id, skill_domain)
        X = self.feature_engineer.features_to_array(features)

        # Get prediction
        difficulty, base_explanation = self.difficulty_optimizer.predict(
            user_id, skill_domain, apply_flow_adjustment=False
        )

        # SHAP explanation
        if self._difficulty_explainer is None:
            self._difficulty_explainer = shap.TreeExplainer(
                self.difficulty_optimizer.model
            )

        shap_values = self._difficulty_explainer.shap_values(X.reshape(1, -1))
        shap_values_array = shap_values[0] if isinstance(shap_values, list) else shap_values

        # Get top contributing features
        feature_names = self.feature_engineer.get_feature_names()
        contributions = []

        for i, (name, value, shap_val) in enumerate(
            zip(feature_names, X, shap_values_array[0])
        ):
            contributions.append({
                'feature': name,
                'value': float(value),
                'contribution': float(shap_val),
                'impact': 'increase' if shap_val > 0 else 'decrease'
            })

        # Sort by absolute contribution
        contributions.sort(key=lambda x: abs(x['contribution']), reverse=True)
        top_contributions = contributions[:top_n]

        # Build human-readable explanation
        explanations = self._build_human_explanation(top_contributions, features)

        return {
            'difficulty': difficulty,
            'top_contributors': top_contributions,
            'explanations': explanations,
            'base_prediction': base_explanation.get('raw_prediction', difficulty)
        }

    def explain_performance_prediction(
        self,
        user_id: int,
        skill_domain: str,
        top_n: int = 5
    ) -> Dict:
        """
        Explain success/failure prediction

        Args:
            user_id: User ID
            skill_domain: Skill domain
            top_n: Number of top contributing features

        Returns:
            Dict with explanation
        """
        if self.performance_predictor.model is None:
            return {
                'error': 'No performance model available'
            }

        # Get features
        features = self.feature_engineer.extract_features(user_id, skill_domain)
        X = self.feature_engineer.features_to_array(features)

        # Get prediction
        success_prob, _ = self.performance_predictor.predict_success_probability(
            user_id, skill_domain
        )

        # SHAP explanation
        if self._performance_explainer is None:
            self._performance_explainer = shap.TreeExplainer(
                self.performance_predictor.model
            )

        shap_values = self._performance_explainer.shap_values(X.reshape(1, -1))

        # For binary classification, take SHAP values for positive class
        if isinstance(shap_values, list) and len(shap_values) == 2:
            shap_values_array = shap_values[1]  # Positive class (success)
        else:
            shap_values_array = shap_values

        # Get top contributing features
        feature_names = self.feature_engineer.get_feature_names()
        contributions = []

        for name, value, shap_val in zip(feature_names, X, shap_values_array[0]):
            contributions.append({
                'feature': name,
                'value': float(value),
                'contribution': float(shap_val),
                'impact': 'positive' if shap_val > 0 else 'negative'
            })

        # Sort by absolute contribution
        contributions.sort(key=lambda x: abs(x['contribution']), reverse=True)
        top_contributions = contributions[:top_n]

        # Build explanations
        explanations = self._build_performance_explanation(top_contributions, features)

        return {
            'success_probability': success_prob,
            'top_contributors': top_contributions,
            'explanations': explanations
        }

    def _build_human_explanation(
        self,
        contributions: List[Dict],
        features: Dict[str, float]
    ) -> List[str]:
        """Build human-readable explanations for difficulty"""
        explanations = []

        for contrib in contributions:
            feature = contrib['feature']
            value = contrib['value']
            impact = contrib['impact']

            if feature == 'recent_success_rate':
                if value > 0.8:
                    explanations.append(f"✓ Excellent taux de réussite ({value:.0%})")
                elif value > 0.6:
                    explanations.append(f"✓ Bon taux de réussite ({value:.0%})")
                else:
                    explanations.append(f"📉 Taux de réussite à améliorer ({value:.0%})")

            elif feature == 'trend_7d':
                if value > 0.1:
                    explanations.append("📈 Progression récente positive")
                elif value < -0.1:
                    explanations.append("📉 Difficulté récente")

            elif feature == 'streak':
                if value >= 3:
                    explanations.append(f"🔥 Série de {int(value)} succès!")

            elif feature == 'fatigue_level':
                if value > 0.3:
                    explanations.append("😴 Signes de fatigue détectés")

            elif feature == 'learning_velocity':
                if value > 0.05:
                    explanations.append("🚀 Apprentissage rapide")

            elif feature == 'domain_proficiency':
                if value > 0.8:
                    explanations.append(f"🌟 Maîtrise du domaine ({value:.0%})")
                elif value < 0.3:
                    explanations.append(f"📚 Domaine à renforcer ({value:.0%})")

        return explanations

    def _build_performance_explanation(
        self,
        contributions: List[Dict],
        features: Dict[str, float]
    ) -> List[str]:
        """Build human-readable explanations for performance prediction"""
        explanations = []

        for contrib in contributions:
            feature = contrib['feature']
            value = contrib['value']
            impact = contrib['impact']

            impact_str = "favorise" if impact == 'positive' else "défavorise"

            if feature == 'recent_success_rate':
                explanations.append(
                    f"Taux de réussite récent ({value:.0%}) {impact_str} la réussite"
                )

            elif feature == 'streak':
                if value >= 3:
                    explanations.append(f"Série de {int(value)} succès {impact_str} la confiance")

            elif feature == 'domain_proficiency':
                explanations.append(
                    f"Maîtrise du domaine ({value:.0%}) {impact_str} la performance"
                )

        return explanations

    def fairness_audit(
        self,
        X_test: np.ndarray,
        y_test: np.ndarray,
        demographics: pd.DataFrame,
        model_type: str = 'performance'
    ) -> Dict:
        """
        Audit model fairness across demographic groups

        Args:
            X_test: Test features
            y_test: Test labels
            demographics: DataFrame with demographic info (grade_level, learning_style)
            model_type: 'difficulty' or 'performance'

        Returns:
            Dict with fairness metrics
        """
        model = (
            self.performance_predictor.model
            if model_type == 'performance'
            else self.difficulty_optimizer.model
        )

        if model is None:
            return {'error': 'Model not available'}

        # Get predictions
        if model_type == 'performance':
            predictions = model.predict_proba(X_test)[:, 1]
        else:
            predictions = model.predict(X_test)

        # Analyze by grade level
        grade_metrics = {}
        for grade in demographics['grade_level'].unique():
            mask = demographics['grade_level'] == grade
            if mask.sum() > 0:
                grade_metrics[grade] = {
                    'count': int(mask.sum()),
                    'mean_prediction': float(predictions[mask].mean()),
                    'std_prediction': float(predictions[mask].std())
                }

        # Analyze by learning style
        style_metrics = {}
        for style in demographics['learning_style'].unique():
            mask = demographics['learning_style'] == style
            if mask.sum() > 0:
                style_metrics[style] = {
                    'count': int(mask.sum()),
                    'mean_prediction': float(predictions[mask].mean()),
                    'std_prediction': float(predictions[mask].std())
                }

        # Compute fairness score (0-1, higher is more fair)
        # Based on variance of predictions across groups
        all_means = [m['mean_prediction'] for m in grade_metrics.values()]
        fairness_variance = np.var(all_means) if all_means else 0
        fairness_score = 1.0 / (1.0 + fairness_variance)

        return {
            'fairness_score': fairness_score,
            'grade_level_metrics': grade_metrics,
            'learning_style_metrics': style_metrics,
            'assessment': self._assess_fairness(fairness_score)
        }

    def _assess_fairness(self, fairness_score: float) -> str:
        """Assess fairness level"""
        if fairness_score > 0.9:
            return "Excellent - Prédictions équitables entre groupes"
        elif fairness_score > 0.7:
            return "Bon - Légères différences entre groupes"
        elif fairness_score > 0.5:
            return "Acceptable - Différences notables entre groupes"
        else:
            return "⚠️ Attention - Biais potentiels détectés"

    def detect_bias(
        self,
        X: np.ndarray,
        sensitive_features: List[int],
        feature_names: List[str]
    ) -> Dict:
        """
        Detect potential bias in sensitive features

        Args:
            X: Feature matrix
            sensitive_features: Indices of sensitive features (e.g., grade_level, learning_style)
            feature_names: Names of all features

        Returns:
            Dict with bias analysis
        """
        bias_report = {
            'sensitive_features': [],
            'recommendations': []
        }

        # Get feature importance from both models
        difficulty_importance = (
            self.difficulty_optimizer.get_feature_importance()
            if self.difficulty_optimizer.model
            else pd.DataFrame()
        )

        performance_importance = (
            self.performance_predictor.get_feature_importance()
            if self.performance_predictor.model
            else pd.DataFrame()
        )

        # Check if sensitive features have high importance
        for idx in sensitive_features:
            feature_name = feature_names[idx]

            # Check in difficulty model
            if not difficulty_importance.empty:
                row = difficulty_importance[difficulty_importance['feature'] == feature_name]
                if not row.empty and row.iloc[0]['importance'] > 0.1:
                    bias_report['sensitive_features'].append({
                        'feature': feature_name,
                        'model': 'difficulty',
                        'importance': float(row.iloc[0]['importance'])
                    })

            # Check in performance model
            if not performance_importance.empty:
                row = performance_importance[performance_importance['feature'] == feature_name]
                if not row.empty and row.iloc[0]['importance'] > 0.1:
                    bias_report['sensitive_features'].append({
                        'feature': feature_name,
                        'model': 'performance',
                        'importance': float(row.iloc[0]['importance'])
                    })

        # Generate recommendations
        if bias_report['sensitive_features']:
            bias_report['recommendations'].append(
                "Surveiller les prédictions pour détecter des biais potentiels"
            )
            bias_report['recommendations'].append(
                "Considérer l'ajustement des pondérations de features sensibles"
            )
        else:
            bias_report['recommendations'].append(
                "✓ Aucun biais évident détecté dans les features sensibles"
            )

        return bias_report


if __name__ == "__main__":
    # Example usage
    xai = ExplainableAI()

    # Explain difficulty prediction
    # explanation = xai.explain_difficulty_prediction(user_id=1, skill_domain='addition')
    # print("Top contributors:", explanation.get('top_contributors', []))
    # print("Explanations:", explanation.get('explanations', []))
