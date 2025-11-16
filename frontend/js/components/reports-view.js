/**
 * Reports View Component
 */

app.component('reports-view', {
    props: {
        classrooms: Array
    },
    data() {
        return {
            reportType: 'class_overview',
            classroomId: null,
            gradeLevel: 'CE2',
            generating: false
        };
    },
    methods: {
        async generateReport() {
            if (!this.classroomId) {
                this.$parent.showNotification('Veuillez sélectionner une classe', 'warning');
                return;
            }

            this.generating = true;
            try {
                let response;
                if (this.reportType === 'class_overview') {
                    response = await api.generateClassReport(this.classroomId, 30);
                } else if (this.reportType === 'at_risk') {
                    response = await api.generateAtRiskReport(this.classroomId, 0.40);
                } else if (this.reportType === 'curriculum') {
                    response = await api.generateCurriculumCoverageReport(this.classroomId, this.gradeLevel);
                }

                this.$parent.showNotification('Rapport généré avec succès', 'success');
                console.log('Report:', response.report);
                // In a real app, would display or download the report
            } catch (error) {
                this.$parent.showNotification('Erreur de génération', 'error');
            } finally {
                this.generating = false;
            }
        }
    },
    template: `
        <div class="reports-container">
            <h2 class="page-title">
                <i class="fas fa-file-alt"></i>
                Génération de rapports
            </h2>

            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">Configurer le rapport</h3>
                </div>

                <div class="modal-body">
                    <div class="form-group">
                        <label class="form-label">Type de rapport</label>
                        <select v-model="reportType" class="form-control">
                            <option value="class_overview">Vue d'ensemble classe</option>
                            <option value="at_risk">Élèves à risque</option>
                            <option value="curriculum">Couverture curriculum</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label class="form-label">Classe</label>
                        <select v-model="classroomId" class="form-control">
                            <option :value="null">-- Sélectionner --</option>
                            <option v-for="classroom in classrooms" :key="classroom.id" :value="classroom.id">
                                {{ classroom.name }}
                            </option>
                        </select>
                    </div>

                    <div v-if="reportType === 'curriculum'" class="form-group">
                        <label class="form-label">Niveau scolaire</label>
                        <select v-model="gradeLevel" class="form-control">
                            <option value="CE1">CE1</option>
                            <option value="CE2">CE2</option>
                            <option value="CM1">CM1</option>
                            <option value="CM2">CM2</option>
                        </select>
                    </div>

                    <button class="btn btn-primary" @click="generateReport" :disabled="generating || !classroomId">
                        <i class="fas fa-file-pdf"></i>
                        {{ generating ? 'Génération...' : 'Générer le rapport' }}
                    </button>
                </div>
            </div>

            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">
                        <i class="fas fa-info-circle"></i>
                        Types de rapports disponibles
                    </h3>
                </div>
                <div style="padding: 1.5rem;">
                    <ul style="list-style: none; padding: 0;">
                        <li style="padding: 0.75rem; border-left: 3px solid var(--primary-color); margin-bottom: 0.5rem; background: var(--light-color);">
                            <strong>Vue d'ensemble classe</strong> - Statistiques complètes, trajectoire, leaderboard, élèves à risque
                        </li>
                        <li style="padding: 0.75rem; border-left: 3px solid var(--danger-color); margin-bottom: 0.5rem; background: var(--light-color);">
                            <strong>Élèves à risque</strong> - Liste détaillée des élèves nécessitant un suivi, avec recommandations
                        </li>
                        <li style="padding: 0.75rem; border-left: 3px solid var(--secondary-color); margin-bottom: 0.5rem; background: var(--light-color);">
                            <strong>Couverture curriculum</strong> - Analyse de la couverture des compétences Éducation Nationale
                        </li>
                    </ul>
                </div>
            </div>

            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">
                        <i class="fas fa-download"></i>
                        Export CSV
                    </h3>
                </div>
                <div class="empty-state">
                    <i class="fas fa-file-csv"></i>
                    <p>Fonctionnalité d'export CSV disponible via l'API</p>
                    <small>Utilisez api.exportCSV() pour télécharger les rapports en CSV</small>
                </div>
            </div>
        </div>
    `
});
