/**
 * Analytics View Component
 */

app.component('analytics-view', {
    props: {
        selectedClassroom: Object,
        classrooms: Array
    },
    data() {
        return {
            classroomId: null,
            leaderboard: [],
            loading: false
        };
    },
    watch: {
        classroomId(newVal) {
            if (newVal) {
                this.loadLeaderboard();
            }
        }
    },
    methods: {
        async loadLeaderboard() {
            if (!this.classroomId) return;

            this.loading = true;
            try {
                const response = await api.getLeaderboard(this.classroomId, null, 30, 10);
                this.leaderboard = response.leaderboard || [];
            } catch (error) {
                this.$parent.showNotification('Erreur de chargement', 'error');
            } finally {
                this.loading = false;
            }
        },

        getRankIcon(rank) {
            if (rank === 1) return 'fas fa-trophy' + ' text-warning';
            if (rank === 2) return 'fas fa-medal';
            if (rank === 3) return 'fas fa-award';
            return '';
        }
    },
    template: `
        <div class="analytics-container">
            <h2 class="page-title">
                <i class="fas fa-chart-line"></i>
                Analytics
            </h2>

            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">Sélectionnez une classe</h3>
                    <select v-model="classroomId" class="form-control" style="width: 300px;">
                        <option :value="null">-- Choisir une classe --</option>
                        <option v-for="classroom in classrooms" :key="classroom.id" :value="classroom.id">
                            {{ classroom.name }}
                        </option>
                    </select>
                </div>
            </div>

            <div v-if="classroomId">
                <!-- Leaderboard -->
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">
                            <i class="fas fa-trophy"></i>
                            Classement (Top 10)
                        </h3>
                    </div>

                    <div v-if="loading" style="padding: 2rem; text-align: center;">
                        <div class="spinner"></div>
                        <p>Chargement...</p>
                    </div>

                    <div v-else-if="leaderboard.length === 0" class="empty-state">
                        <i class="fas fa-chart-bar"></i>
                        <p>Aucune donnée disponible</p>
                    </div>

                    <div v-else class="table-container">
                        <table>
                            <thead>
                                <tr>
                                    <th>Rang</th>
                                    <th>Élève</th>
                                    <th>Exercices</th>
                                    <th>Réussite</th>
                                    <th>Score</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="student in leaderboard" :key="student.student_id">
                                    <td>
                                        <strong style="font-size: 1.2em;">
                                            <i :class="getRankIcon(student.rank)" style="margin-right: 0.5rem;"></i>
                                            #{{ student.rank }}
                                        </strong>
                                    </td>
                                    <td><strong>{{ student.username }}</strong></td>
                                    <td>{{ student.exercises_completed }}</td>
                                    <td>
                                        <div class="progress-bar">
                                            <div class="progress-fill" :style="{width: (student.success_rate * 100) + '%'}"></div>
                                        </div>
                                        <small>{{ (student.success_rate * 100).toFixed(1) }}%</small>
                                    </td>
                                    <td>{{ student.score.toFixed(0) }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Placeholder for future charts -->
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">
                            <i class="fas fa-chart-area"></i>
                            Graphiques d'évolution
                        </h3>
                    </div>
                    <div class="empty-state">
                        <i class="fas fa-chart-line"></i>
                        <p>Graphiques de trajectoire de progression disponibles via l'API</p>
                        <small>Utilisez Chart.js pour visualiser les données de l'API analytics/trajectory</small>
                    </div>
                </div>
            </div>

            <div v-else class="empty-state" style="margin-top: 2rem;">
                <i class="fas fa-chart-line"></i>
                <h3>Sélectionnez une classe</h3>
                <p>Choisissez une classe pour voir les analytics</p>
            </div>
        </div>
    `
});
