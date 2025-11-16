/**
 * MathCopain API Client
 * Handles all API calls to Flask backend
 */

const API_BASE_URL = 'http://localhost:5000/api';

class APIClient {
    constructor(baseURL = API_BASE_URL) {
        this.baseURL = baseURL;
    }

    /**
     * Generic HTTP request method
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;

        const config = {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            credentials: 'include' // Include cookies for session
        };

        if (options.body && typeof options.body === 'object') {
            config.body = JSON.stringify(options.body);
        }

        try {
            const response = await fetch(url, config);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Request failed');
            }

            return data;
        } catch (error) {
            console.error(`API Error [${endpoint}]:`, error);
            throw error;
        }
    }

    // ========================================================================
    // CLASSROOM ENDPOINTS
    // ========================================================================

    async getClassrooms() {
        return this.request('/teacher/classrooms');
    }

    async createClassroom(data) {
        return this.request('/teacher/classrooms', {
            method: 'POST',
            body: data
        });
    }

    async getClassroomDetails(classroomId) {
        return this.request(`/teacher/classrooms/${classroomId}`);
    }

    async updateClassroom(classroomId, data) {
        return this.request(`/teacher/classrooms/${classroomId}`, {
            method: 'PUT',
            body: data
        });
    }

    async deleteClassroom(classroomId) {
        return this.request(`/teacher/classrooms/${classroomId}`, {
            method: 'DELETE'
        });
    }

    async getClassroomStudents(classroomId) {
        return this.request(`/teacher/classrooms/${classroomId}/students`);
    }

    async addStudentToClassroom(classroomId, studentUsername) {
        return this.request(`/teacher/classrooms/${classroomId}/students`, {
            method: 'POST',
            body: { student_username: studentUsername }
        });
    }

    async removeStudentFromClassroom(classroomId, studentId) {
        return this.request(`/teacher/classrooms/${classroomId}/students/${studentId}`, {
            method: 'DELETE'
        });
    }

    async getAtRiskStudents(classroomId, threshold = 0.40) {
        return this.request(`/teacher/classrooms/${classroomId}/at-risk?threshold=${threshold}`);
    }

    // ========================================================================
    // ASSIGNMENT ENDPOINTS
    // ========================================================================

    async getAssignments(classroomId = null, status = null) {
        let query = '';
        if (classroomId) query += `?classroom_id=${classroomId}`;
        if (status) query += (query ? '&' : '?') + `status=${status}`;

        return this.request(`/teacher/assignments${query}`);
    }

    async createAssignment(data) {
        return this.request('/teacher/assignments', {
            method: 'POST',
            body: data
        });
    }

    async getAssignmentDetails(assignmentId) {
        return this.request(`/teacher/assignments/${assignmentId}`);
    }

    async publishAssignment(assignmentId) {
        return this.request(`/teacher/assignments/${assignmentId}/publish`, {
            method: 'POST'
        });
    }

    async updateAssignment(assignmentId, data) {
        return this.request(`/teacher/assignments/${assignmentId}`, {
            method: 'PUT',
            body: data
        });
    }

    async deleteAssignment(assignmentId) {
        return this.request(`/teacher/assignments/${assignmentId}`, {
            method: 'DELETE'
        });
    }

    async getAssignmentCompletion(assignmentId) {
        return this.request(`/teacher/assignments/${assignmentId}/completion`);
    }

    // ========================================================================
    // ANALYTICS ENDPOINTS
    // ========================================================================

    async getProgressTrajectory(params) {
        const query = new URLSearchParams(params).toString();
        return this.request(`/teacher/analytics/trajectory?${query}`);
    }

    async getPerformanceHeatmap(studentId, daysBack = 30) {
        return this.request(`/teacher/analytics/heatmap?student_id=${studentId}&days_back=${daysBack}`);
    }

    async getPerformanceForecast(studentId, skillDomain, daysAhead = 7) {
        return this.request(
            `/teacher/analytics/forecast?student_id=${studentId}&skill_domain=${skillDomain}&days_ahead=${daysAhead}`
        );
    }

    async getEngagementMetrics(studentId, daysBack = 30) {
        return this.request(`/teacher/analytics/engagement?student_id=${studentId}&days_back=${daysBack}`);
    }

    async compareStudentToClass(studentId, classroomId, skillDomain = null, daysBack = 30) {
        let query = `student_id=${studentId}&classroom_id=${classroomId}&days_back=${daysBack}`;
        if (skillDomain) query += `&skill_domain=${skillDomain}`;

        return this.request(`/teacher/analytics/compare?${query}`);
    }

    async getLeaderboard(classroomId, skillDomain = null, daysBack = 30, topN = 10) {
        let query = `classroom_id=${classroomId}&days_back=${daysBack}&top_n=${topN}`;
        if (skillDomain) query += `&skill_domain=${skillDomain}`;

        return this.request(`/teacher/analytics/leaderboard?${query}`);
    }

    // ========================================================================
    // CURRICULUM ENDPOINTS
    // ========================================================================

    async getCompetencies(gradeLevel, skillDomain = null) {
        let query = `grade_level=${gradeLevel}`;
        if (skillDomain) query += `&skill_domain=${skillDomain}`;

        return this.request(`/teacher/curriculum/competencies?${query}`);
    }

    async getStudentCompetencyProgress(studentId, gradeLevel, skillDomain = null) {
        let query = `student_id=${studentId}&grade_level=${gradeLevel}`;
        if (skillDomain) query += `&skill_domain=${skillDomain}`;

        return this.request(`/teacher/curriculum/student-progress?${query}`);
    }

    async getClassCompetencyOverview(classroomId, gradeLevel) {
        return this.request(
            `/teacher/curriculum/class-overview?classroom_id=${classroomId}&grade_level=${gradeLevel}`
        );
    }

    async getCompetencyGaps(studentId, gradeLevel) {
        return this.request(`/teacher/curriculum/gaps?student_id=${studentId}&grade_level=${gradeLevel}`);
    }

    async getCompetencyRecommendations(studentId, gradeLevel, count = 3) {
        return this.request(
            `/teacher/curriculum/recommendations?student_id=${studentId}&grade_level=${gradeLevel}&count=${count}`
        );
    }

    // ========================================================================
    // REPORT ENDPOINTS
    // ========================================================================

    async generateStudentReport(studentId, classroomId, format = 'structured', daysBack = 30) {
        return this.request('/teacher/reports/student-progress', {
            method: 'POST',
            body: { student_id: studentId, classroom_id: classroomId, format, days_back: daysBack }
        });
    }

    async generateClassReport(classroomId, daysBack = 30) {
        return this.request('/teacher/reports/class-overview', {
            method: 'POST',
            body: { classroom_id: classroomId, days_back: daysBack }
        });
    }

    async generateAtRiskReport(classroomId, threshold = 0.40) {
        return this.request('/teacher/reports/at-risk', {
            method: 'POST',
            body: { classroom_id: classroomId, threshold }
        });
    }

    async generateAssignmentReport(assignmentId) {
        return this.request('/teacher/reports/assignment', {
            method: 'POST',
            body: { assignment_id: assignmentId }
        });
    }

    async generateCurriculumCoverageReport(classroomId, gradeLevel) {
        return this.request('/teacher/reports/curriculum-coverage', {
            method: 'POST',
            body: { classroom_id: classroomId, grade_level: gradeLevel }
        });
    }

    async exportCSV(reportType, data) {
        return this.request('/teacher/reports/export/csv', {
            method: 'POST',
            body: { report_type: reportType, ...data }
        });
    }
}

// Create global API client instance
const api = new APIClient();
