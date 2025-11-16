/**
 * Assignments View Component
 */

app.component('assignments-view', {
    props: {
        assignments: Array,
        classrooms: Array
    },
    data() {
        return {
            filter: 'all', // all, published, draft
            selectedAssignment: null,
            completions: []
        };
    },
    computed: {
        filteredAssignments() {
            if (this.filter === 'all') return this.assignments;
            if (this.filter === 'published') return this.assignments.filter(a => a.is_published);
            if (this.filter === 'draft') return this.assignments.filter(a => !a.is_published);
            return this.assignments;
        }
    },
    methods: {
        async viewCompletion(assignment) {
            this.selectedAssignment = assignment;
            try {
                const response = await api.getAssignmentCompletion(assignment.id);
                this.completions = response.completions || [];
            } catch (error) {
                this.$parent.showNotification('Erreur de chargement', 'error');
            }
        },

        getClassroomName(classroomId) {
            const classroom = this.classrooms.find(c => c.id === classroomId);
            return classroom ? classroom.name : 'N/A';
        },

        formatDate(dateString) {
            if (!dateString) return 'N/A';
            return new Date(dateString).toLocaleDateString('fr-FR');
        }
    },
    template: `
        <div class="assignments-container">
            <h2 class="page-title">
                <i class="fas fa-tasks"></i>
                Gestion des devoirs
            </h2>

            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">Devoirs ({{ filteredAssignments.length }})</h3>
                    <div style="display: flex; gap: 0.5rem;">
                        <select v-model="filter" class="form-control" style="width: auto;">
                            <option value="all">Tous</option>
                            <option value="published">Publiés</option>
                            <option value="draft">Brouillons</option>
                        </select>
                        <button class="btn btn-primary" @click="$emit('create-assignment')">
                            <i class="fas fa-plus"></i>
                            Nouveau devoir
                        </button>
                    </div>
                </div>

                <div v-if="filteredAssignments.length === 0" class="empty-state">
                    <i class="fas fa-tasks"></i>
                    <h3>Aucun devoir</h3>
                    <p>Créez votre premier devoir</p>
                    <button class="btn btn-primary" @click="$emit('create-assignment')">
                        <i class="fas fa-plus"></i>
                        Créer un devoir
                    </button>
                </div>

                <div v-else class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Titre</th>
                                <th>Classe</th>
                                <th>Domaines</th>
                                <th>Exercices</th>
                                <th>Échéance</th>
                                <th>Statut</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="assignment in filteredAssignments" :key="assignment.id">
                                <td><strong>{{ assignment.title }}</strong></td>
                                <td>{{ getClassroomName(assignment.classroom_id) }}</td>
                                <td>
                                    <span v-for="domain in (assignment.skill_domains || []).slice(0,2)" :key="domain" class="badge info" style="margin-right: 0.25rem;">
                                        {{ domain }}
                                    </span>
                                </td>
                                <td>{{ assignment.exercise_count }}</td>
                                <td>{{ formatDate(assignment.due_date) }}</td>
                                <td>
                                    <span v-if="assignment.is_published" class="badge success">Publié</span>
                                    <span v-else class="badge warning">Brouillon</span>
                                    <span v-if="assignment.is_adaptive" class="badge info" style="margin-left: 0.25rem;">Adaptatif</span>
                                </td>
                                <td>
                                    <div class="card-actions">
                                        <button v-if="!assignment.is_published" class="btn btn-sm btn-success" @click="$emit('publish-assignment', assignment)">
                                            <i class="fas fa-paper-plane"></i>
                                            Publier
                                        </button>
                                        <button class="btn btn-sm btn-primary" @click="viewCompletion(assignment)">
                                            <i class="fas fa-chart-bar"></i>
                                            Suivi
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Assignment Completion Modal -->
            <div v-if="selectedAssignment" class="card">
                <div class="card-header">
                    <h3 class="card-title">
                        <i class="fas fa-chart-bar"></i>
                        Suivi : {{ selectedAssignment.title }}
                    </h3>
                    <button class="btn btn-outline" @click="selectedAssignment = null">
                        <i class="fas fa-times"></i>
                        Fermer
                    </button>
                </div>

                <div v-if="completions.length === 0" class="empty-state">
                    <i class="fas fa-clipboard-check"></i>
                    <p>Aucune donnée de complétion</p>
                </div>

                <div v-else class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Élève</th>
                                <th>Progression</th>
                                <th>Réussite</th>
                                <th>Temps (min)</th>
                                <th>Statut</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="completion in completions" :key="completion.student_id">
                                <td><strong>{{ completion.student_name }}</strong></td>
                                <td>
                                    <div class="progress-bar">
                                        <div class="progress-fill" :style="{width: completion.progress_percentage + '%'}"></div>
                                    </div>
                                    <small>{{ completion.progress }}</small>
                                </td>
                                <td>{{ completion.success_rate ? (completion.success_rate * 100).toFixed(1) + '%' : 'N/A' }}</td>
                                <td>{{ completion.time_spent_minutes || 0 }}</td>
                                <td>
                                    <span class="badge" :class="completion.status === 'completed' ? 'success' : 'warning'">
                                        {{ completion.status === 'completed' ? 'Terminé' : 'En cours' }}
                                    </span>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    `
});
