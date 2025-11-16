/**
 * Classrooms View Component
 */

app.component('classrooms-view', {
    props: {
        classrooms: Array
    },
    data() {
        return {
            selectedClassroom: null,
            students: [],
            loadingStudents: false,
            newStudentUsername: ''
        };
    },
    methods: {
        async selectClass(classroom) {
            this.selectedClassroom = classroom;
            this.loadingStudents = true;

            try {
                const response = await api.getClassroomStudents(classroom.id);
                this.students = response.students || [];
            } catch (error) {
                console.error('Error loading students:', error);
            } finally {
                this.loadingStudents = false;
            }
        },

        async addStudent() {
            if (!this.newStudentUsername.trim()) {
                return;
            }

            try {
                await api.addStudentToClassroom(this.selectedClassroom.id, this.newStudentUsername);
                this.$parent.showNotification('Élève ajouté avec succès', 'success');
                this.newStudentUsername = '';
                await this.selectClass(this.selectedClassroom);
                this.$emit('refresh');
            } catch (error) {
                this.$parent.showNotification(error.message || 'Erreur lors de l\'ajout', 'error');
            }
        },

        async removeStudent(student) {
            if (!confirm(`Retirer ${student.username} de la classe ?`)) {
                return;
            }

            try {
                await api.removeStudentFromClassroom(this.selectedClassroom.id, student.id);
                this.$parent.showNotification('Élève retiré de la classe', 'success');
                await this.selectClass(this.selectedClassroom);
                this.$emit('refresh');
            } catch (error) {
                this.$parent.showNotification('Erreur lors du retrait', 'error');
            }
        },

        getStatusBadge(student) {
            if (student.at_risk) return 'danger';
            if ((student.success_rate || 0) >= 0.7) return 'success';
            return 'warning';
        }
    },
    template: `
        <div class="classrooms-container">
            <h2 class="page-title">
                <i class="fas fa-school"></i>
                Gestion des classes
            </h2>

            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">
                        Mes classes ({{ classrooms.length }})
                    </h3>
                    <button class="btn btn-primary" @click="$emit('create-classroom')">
                        <i class="fas fa-plus"></i>
                        Créer une classe
                    </button>
                </div>

                <div v-if="classrooms.length === 0" class="empty-state">
                    <i class="fas fa-school"></i>
                    <h3>Aucune classe créée</h3>
                    <p>Commencez par créer votre première classe</p>
                    <button class="btn btn-primary" @click="$emit('create-classroom')">
                        <i class="fas fa-plus"></i>
                        Créer une classe
                    </button>
                </div>

                <div v-else class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Classe</th>
                                <th>Niveau</th>
                                <th>Année</th>
                                <th>Élèves</th>
                                <th>Capacité</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="classroom in classrooms" :key="classroom.id">
                                <td><strong>{{ classroom.name }}</strong></td>
                                <td><span class="badge info">{{ classroom.grade_level }}</span></td>
                                <td>{{ classroom.school_year || 'N/A' }}</td>
                                <td>{{ classroom.student_count || 0 }}</td>
                                <td>{{ classroom.max_students || 30 }}</td>
                                <td>
                                    <div class="card-actions">
                                        <button class="btn btn-sm btn-primary" @click="selectClass(classroom)">
                                            <i class="fas fa-users"></i>
                                            Élèves
                                        </button>
                                        <button class="btn btn-sm btn-outline" @click="$emit('edit-classroom', classroom)">
                                            <i class="fas fa-edit"></i>
                                        </button>
                                        <button class="btn btn-sm btn-danger" @click="$emit('delete-classroom', classroom)">
                                            <i class="fas fa-trash"></i>
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Student Management -->
            <div v-if="selectedClassroom" class="card">
                <div class="card-header">
                    <h3 class="card-title">
                        <i class="fas fa-users"></i>
                        Élèves de {{ selectedClassroom.name }}
                    </h3>
                    <button class="btn btn-outline" @click="selectedClassroom = null">
                        <i class="fas fa-times"></i>
                        Fermer
                    </button>
                </div>

                <!-- Add Student Form -->
                <div style="padding: 1rem; border-bottom: 1px solid var(--border-color);">
                    <div style="display: flex; gap: 0.5rem;">
                        <input
                            v-model="newStudentUsername"
                            type="text"
                            class="form-control"
                            placeholder="Nom d'utilisateur de l'élève"
                            @keyup.enter="addStudent"
                        />
                        <button class="btn btn-primary" @click="addStudent">
                            <i class="fas fa-plus"></i>
                            Ajouter
                        </button>
                    </div>
                </div>

                <!-- Students List -->
                <div v-if="loadingStudents" style="padding: 2rem; text-align: center;">
                    <div class="spinner"></div>
                    <p>Chargement...</p>
                </div>

                <div v-else-if="students.length === 0" class="empty-state">
                    <i class="fas fa-user-plus"></i>
                    <h3>Aucun élève dans cette classe</h3>
                    <p>Ajoutez des élèves pour commencer</p>
                </div>

                <div v-else class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Élève</th>
                                <th>Niveau</th>
                                <th>Exercices</th>
                                <th>Taux de réussite</th>
                                <th>Statut</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="student in students" :key="student.id">
                                <td>
                                    <strong>{{ student.username }}</strong>
                                </td>
                                <td>{{ student.grade_level }}</td>
                                <td>{{ student.exercises_completed || 0 }}</td>
                                <td>
                                    <div class="progress-bar">
                                        <div class="progress-fill" :style="{width: ((student.success_rate || 0) * 100) + '%'}"></div>
                                    </div>
                                    <small>{{ ((student.success_rate || 0) * 100).toFixed(1) }}%</small>
                                </td>
                                <td>
                                    <span class="badge" :class="getStatusBadge(student)">
                                        {{ student.at_risk ? 'À risque' : 'Normal' }}
                                    </span>
                                </td>
                                <td>
                                    <button class="btn btn-sm btn-danger" @click="removeStudent(student)">
                                        <i class="fas fa-user-minus"></i>
                                        Retirer
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    `
});
