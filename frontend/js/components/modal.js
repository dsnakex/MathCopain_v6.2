/**
 * Modal Component
 */

app.component('modal', {
    props: {
        title: {
            type: String,
            required: true
        }
    },
    template: `
        <div class="modal-overlay" @click.self="close">
            <div class="modal-container">
                <div class="modal-header">
                    <h2 class="modal-title">{{ title }}</h2>
                    <button class="modal-close" @click="close">&times;</button>
                </div>
                <div class="modal-body">
                    <slot></slot>
                </div>
            </div>
        </div>
    `,
    methods: {
        close() {
            this.$emit('close');
        }
    }
});
