/**
 * MathCopain Teacher Dashboard - Vue 3 Application
 */

const { createApp } = Vue;

const app = createApp({
    data() {
        return {
            loading: true,
            currentTab: 'dashboard',
            classrooms: [],
            assignments: [],
            selectedClassroom: null,
            atRiskCount: 0,

            // Modal state
            showModal: false,
            modalTitle: '',
            modalComponent: null,
            modalProps: {},

            // Notifications
            notifications: [],
            notificationId: 0,

            // Tabs configuration
            tabs: [
                {
                    id: 'dashboard',
                    label: 'Tableau de bord',
                    icon: 'fas fa-home'
                },
                {
                    id: 'classrooms',
                    label: 'Classes',
                    icon: 'fas fa-school'
                },
                {
                    id: 'assignments',
                    label: 'Devoirs',
                    icon: 'fas fa-tasks'
                },
                {
                    id: 'analytics',
                    label: 'Analytics',
                    icon: 'fas fa-chart-line'
                },
                {
                    id: 'reports',
                    label: 'Rapports',
                    icon: 'fas fa-file-alt'
                },
                {
                    id: 'curriculum',
                    label: 'Compétences EN',
                    icon: 'fas fa-book'
                }
            ]
        };
    },

    async mounted() {
        await this.loadDashboard();
        this.loading = false;
    },

    methods: {
        /**
         * Load dashboard data
         */
        async loadDashboard() {
            try {
                // Load classrooms
                const classroomsResponse = await api.getClassrooms();
                this.classrooms = classroomsResponse.classrooms || [];

                // Load assignments
                const assignmentsResponse = await api.getAssignments();
                this.assignments = assignmentsResponse.assignments || [];

                // Count at-risk students across all classrooms
                let totalAtRisk = 0;
                for (const classroom of this.classrooms) {
                    try {
                        const atRiskResponse = await api.getAtRiskStudents(classroom.id);
                        totalAtRisk += atRiskResponse.at_risk_students?.length || 0;
                    } catch (e) {
                        console.error(`Error loading at-risk for classroom ${classroom.id}:`, e);
                    }
                }
                this.atRiskCount = totalAtRisk;

                // Update badge
                const dashboardTab = this.tabs.find(t => t.id === 'dashboard');
                if (dashboardTab && totalAtRisk > 0) {
                    dashboardTab.badge = totalAtRisk;
                }

            } catch (error) {
                console.error('Error loading dashboard:', error);
                this.showNotification('Erreur lors du chargement des données', 'error');
            }
        },

        /**
         * Select a classroom
         */
        selectClassroom(classroom) {
            this.selectedClassroom = classroom;
        },

        /**
         * Show create classroom modal
         */
        showCreateClassroomModal() {
            this.modalTitle = 'Créer une classe';
            this.modalComponent = 'create-classroom-form';
            this.modalProps = {};
            this.showModal = true;
        },

        /**
         * Edit classroom
         */
        async editClassroom(classroom) {
            this.modalTitle = 'Modifier la classe';
            this.modalComponent = 'edit-classroom-form';
            this.modalProps = { classroom };
            this.showModal = true;
        },

        /**
         * Delete classroom
         */
        async deleteClassroom(classroom) {
            if (!confirm(`Voulez-vous vraiment archiver la classe "${classroom.name}" ?`)) {
                return;
            }

            try {
                await api.deleteClassroom(classroom.id);
                this.showNotification('Classe archivée avec succès', 'success');
                await this.loadDashboard();
            } catch (error) {
                this.showNotification('Erreur lors de l\'archivage de la classe', 'error');
            }
        },

        /**
         * Show create assignment modal
         */
        showCreateAssignmentModal() {
            this.modalTitle = 'Créer un devoir';
            this.modalComponent = 'create-assignment-form';
            this.modalProps = { classrooms: this.classrooms };
            this.showModal = true;
        },

        /**
         * View assignment details
         */
        async viewAssignment(assignment) {
            this.currentTab = 'assignments';
            // TODO: Show assignment details
        },

        /**
         * Publish assignment
         */
        async publishAssignment(assignment) {
            try {
                await api.publishAssignment(assignment.id);
                this.showNotification('Devoir publié avec succès', 'success');
                await this.loadDashboard();
            } catch (error) {
                this.showNotification('Erreur lors de la publication', 'error');
            }
        },

        /**
         * Generate report
         */
        async generateReport(reportConfig) {
            this.showNotification('Génération du rapport en cours...', 'info');
            // TODO: Implement report generation
        },

        /**
         * Handle modal submit
         */
        async handleModalSubmit(data) {
            try {
                if (this.modalComponent === 'create-classroom-form') {
                    await api.createClassroom(data);
                    this.showNotification('Classe créée avec succès', 'success');
                } else if (this.modalComponent === 'edit-classroom-form') {
                    await api.updateClassroom(data.id, data);
                    this.showNotification('Classe mise à jour', 'success');
                } else if (this.modalComponent === 'create-assignment-form') {
                    await api.createAssignment(data);
                    this.showNotification('Devoir créé avec succès', 'success');
                }

                this.closeModal();
                await this.loadDashboard();
            } catch (error) {
                this.showNotification(error.message || 'Une erreur est survenue', 'error');
            }
        },

        /**
         * Close modal
         */
        closeModal() {
            this.showModal = false;
            this.modalComponent = null;
            this.modalProps = {};
        },

        /**
         * Show notification
         */
        showNotification(message, type = 'info') {
            const id = this.notificationId++;
            this.notifications.push({ id, message, type });

            // Auto-remove after 5 seconds
            setTimeout(() => {
                this.removeNotification(id);
            }, 5000);
        },

        /**
         * Remove notification
         */
        removeNotification(id) {
            const index = this.notifications.findIndex(n => n.id === id);
            if (index !== -1) {
                this.notifications.splice(index, 1);
            }
        },

        /**
         * Get notification icon
         */
        getNotificationIcon(type) {
            const icons = {
                success: 'fas fa-check-circle',
                error: 'fas fa-exclamation-circle',
                warning: 'fas fa-exclamation-triangle',
                info: 'fas fa-info-circle'
            };
            return icons[type] || icons.info;
        },

        /**
         * Logout
         */
        logout() {
            if (confirm('Voulez-vous vraiment vous déconnecter ?')) {
                // TODO: Implement logout
                window.location.href = '/';
            }
        }
    }
});

// Mount app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        app.mount('#app');
    });
} else {
    app.mount('#app');
}
