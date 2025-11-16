/**
 * Curriculum View Component
 */

app.component('curriculum-view', {
    props: {
        classrooms: Array,
        selectedClassroom: Object
    },
    data() {
        return {
            classroomId: null,
            gradeLevel: 'CE2',
            overview: null,
            loading: false
        };
    },
    watch: {
        classroomId(newVal) {
            if (newVal) {
                this.loadOverview();
            }
        },
        gradeLevel(newVal) {
            if (this.classroomId) {
                this.loadOverview();
            }
        }
    },
    methods: {
        async loadOverview() {
            if (!this.classroomId || !this.gradeLevel) return;

            this.loading = true;
            try {
                const response = await api.getClassCompetencyOverview(this.classroomId, this.gradeLevel);
                this.overview = response.overview;
            } catch (error) {
                this.$parent.showNotification('Erreur de chargement', 'error');
            } finally {
                this.loading = false;
            }
        },

        getMasteryClass(masteryRate) {
            if (masteryRate >= 0.7) return 'success';
            if (masteryRate >= 0.3) return 'warning';
            return 'danger';
        }
    },
    template: `
        <div class="curriculum-container">
            <h2 class="page-title">
                <i class="fas fa-book"></i>
                Compétences Éducation Nationale
            </h2>

            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">Sélection</h3>
                </div>
                <div class="modal-body">
                    <div class="form-group">
                        <label class="form-label">Classe</label>
                        <select v-model="classroomId" class="form-control">
                            <option :value="null">-- Sélectionner --</option>
                            <option v-for="classroom in classrooms" :key="classroom.id" :value="classroom.id">
                                {{ classroom.name }}
                            </option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label class="form-label">Niveau scolaire</label>
                        <select v-model="gradeLevel" class="form-control">
                            <option value="CE1">CE1</option>
                            <option value="CE2">CE2</option>
                            <option value="CM1">CM1</option>
                            <option value="CM2">CM2</option>
                        </select>
                    </div>
                </div>
            </div>

            <div v-if="loading" class="card">
                <div style="padding: 2rem; text-align: center;">
                    <div class="spinner"></div>
                    <p>Chargement...</p>
                </div>
            </div>

            <div v-else-if="overview">
                <!-- Summary Stats -->
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-icon primary">
                            <i class="fas fa-list"></i>
                        </div>
                        <div class="stat-content">
                            <h3>{{ overview.total_competencies }}</h3>
                            <p>Compétences totales</p>
                        </div>
                    </div>

                    <div class="stat-card">
                        <div class="stat-icon" :class="overview.avg_class_mastery >= 0.7 ? 'primary' : 'warning'">
                            <i class="fas fa-chart-line"></i>
                        </div>
                        <div class="stat-content">
                            <h3>{{ (overview.avg_class_mastery * 100).toFixed(1) }}%</h3>
                            <p>Maîtrise moyenne classe</p>
                        </div>
                    </div>
                </div>

                <!-- Competencies Table -->
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">
                            <i class="fas fa-clipboard-list"></i>
                            Détail des compétences ({{ overview.competencies.length }})
                        </h3>
                    </div>

                    <div class="table-container">
                        <table>
                            <thead>
                                <tr>
                                    <th>Code</th>
                                    <th>Compétence</th>
                                    <th>Domaine</th>
                                    <th>Élèves maîtrisant</th>
                                    <th>Taux de maîtrise</th>
                                    <th>Niveau moyen</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="comp in overview.competencies" :key="comp.code">
                                    <td><code>{{ comp.code }}</code></td>
                                    <td><strong>{{ comp.title }}</strong></td>
                                    <td>
                                        <span class="badge info">{{ comp.domain }}</span>
                                    </td>
                                    <td>{{ comp.students_mastered }} / {{ overview.student_count }}</td>
                                    <td>
                                        <div class="progress-bar">
                                            <div class="progress-fill" :style="{width: (comp.mastery_rate * 100) + '%'}"></div>
                                        </div>
                                        <small>{{ (comp.mastery_rate * 100).toFixed(1) }}%</small>
                                    </td>
                                    <td>
                                        <span class="badge" :class="getMasteryClass(comp.avg_mastery_level)">
                                            {{ (comp.avg_mastery_level * 100).toFixed(0) }}%
                                        </span>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <div v-else class="empty-state" style="margin-top: 2rem;">
                <i class="fas fa-book-open"></i>
                <h3>Sélectionnez une classe et un niveau</h3>
                <p>Choisissez une classe pour voir la couverture du curriculum</p>
            </div>
        </div>
    `
});
