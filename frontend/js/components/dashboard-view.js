/**
 * Dashboard View Component
 */

app.component('dashboard-view', {
    props: {
        classrooms: Array,
        atRiskCount: Number
    },
    data() {
        return {
            selectedPeriod: 7
        };
    },
    computed: {
        totalStudents() {
            return this.classrooms.reduce((sum, c) => sum + (c.student_count || 0), 0);
        },
        totalAssignments() {
            // Would come from API in real implementation
            return this.classrooms.reduce((sum, c) => sum + (c.assignments_count || 0), 0);
        },
        avgSuccessRate() {
            if (this.classrooms.length === 0) return 0;
            const sum = this.classrooms.reduce((acc, c) => acc + (c.avg_success_rate || 0), 0);
            return (sum / this.classrooms.length * 100).toFixed(1);
        }
    },
    template: `
        <div class="dashboard-container">
            <h2 class="page-title">
                <i class="fas fa-home"></i>
                Tableau de bord
            </h2>

            <!-- Stats Grid -->
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-icon primary">
                        <i class="fas fa-school"></i>
                    </div>
                    <div class="stat-content">
                        <h3>{{ classrooms.length }}</h3>
                        <p>Classes actives</p>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="stat-icon secondary">
                        <i class="fas fa-users"></i>
                    </div>
                    <div class="stat-content">
                        <h3>{{ totalStudents }}</h3>
                        <p>Élèves au total</p>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="stat-icon warning">
                        <i class="fas fa-exclamation-triangle"></i>
                    </div>
                    <div class="stat-content">
                        <h3>{{ atRiskCount }}</h3>
                        <p>Élèves à risque</p>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="stat-icon" :class="avgSuccessRate >= 70 ? 'primary' : 'warning'">
                        <i class="fas fa-chart-line"></i>
                    </div>
                    <div class="stat-content">
                        <h3>{{ avgSuccessRate }}%</h3>
                        <p>Taux de réussite moyen</p>
                    </div>
                </div>
            </div>

            <!-- Classes Overview -->
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">
                        <i class="fas fa-school"></i>
                        Mes classes
                    </h3>
                    <button class="btn btn-primary" @click="$emit('select-classroom', null); $parent.currentTab = 'classrooms'">
                        <i class="fas fa-plus"></i>
                        Nouvelle classe
                    </button>
                </div>

                <div v-if="classrooms.length === 0" class="empty-state">
                    <i class="fas fa-school"></i>
                    <h3>Aucune classe créée</h3>
                    <p>Commencez par créer votre première classe</p>
                    <button class="btn btn-primary" @click="$parent.currentTab = 'classrooms'">
                        Créer une classe
                    </button>
                </div>

                <div v-else class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Classe</th>
                                <th>Niveau</th>
                                <th>Élèves</th>
                                <th>Taux de réussite</th>
                                <th>À risque</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="classroom in classrooms" :key="classroom.id">
                                <td>
                                    <strong>{{ classroom.name }}</strong>
                                </td>
                                <td>
                                    <span class="badge info">{{ classroom.grade_level }}</span>
                                </td>
                                <td>{{ classroom.student_count || 0 }}</td>
                                <td>
                                    <div class="progress-bar">
                                        <div class="progress-fill" :style="{width: (classroom.avg_success_rate * 100) + '%'}"></div>
                                    </div>
                                    <small>{{ ((classroom.avg_success_rate || 0) * 100).toFixed(1) }}%</small>
                                </td>
                                <td>
                                    <span v-if="classroom.at_risk_count > 0" class="badge danger">
                                        {{ classroom.at_risk_count }}
                                    </span>
                                    <span v-else class="badge success">0</span>
                                </td>
                                <td>
                                    <button class="btn btn-sm btn-outline" @click="$emit('select-classroom', classroom); $parent.currentTab = 'classrooms'">
                                        <i class="fas fa-eye"></i>
                                        Voir
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Recent Activity (placeholder) -->
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">
                        <i class="fas fa-clock"></i>
                        Activité récente
                    </h3>
                </div>
                <div class="empty-state">
                    <i class="fas fa-history"></i>
                    <p>Aucune activité récente</p>
                </div>
            </div>
        </div>
    `
});
