<template>
    <div class="container mt-5">
        <h2 class="mb-4">{{ isEditing ? 'Edit' : 'Add' }} Step for JHA: {{ jhaTitle }}</h2>

        <form @submit.prevent="saveStep">
            <div class="mb-3">
                <label class="form-label">Step Description</label>
                <input v-model="step.step_description" type="text" class="form-control" required />
            </div>

            <h3>Hazards</h3>
            <button type="button" class="btn btn-success mb-3" @click="addHazard">+ Add Hazard</button>

            <table class="table table-bordered">
                <thead class="table-light">
                    <tr>
                        <th>Description</th>
                        <th>Hazard Controls</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="hazard in hazards" :key="hazard.id">
                        <td>
                            <input v-model="hazard.description" type="text" class="form-control" required />
                        </td>
                        <td>
                            <input v-model="hazard.controls" type="text" class="form-control" required />
                        </td>
                        <td>
                            <button type="button" class="btn btn-danger btn-sm"
                                @click="deleteHazard(hazard.id)">Delete</button>
                        </td>
                    </tr>
                </tbody>
            </table>

            <div class="d-flex justify-content-between mt-4">
                <button type="submit" class="btn btn-primary">Save</button>
                <router-link :to="`/jha/${jhaId}`" class="btn btn-secondary">Cancel</router-link>
            </div>
        </form>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter} from 'vue-router'
import axios from 'axios'

export default {
    name: 'StepForm',
    props: ['jhaId', 'stepId'],
    setup(props) {
        const router = useRouter()
        const isEditing = ref(false)
        const jhaTitle = ref('')
        const step = ref({
            id: null,
            step_description: '',
            step_number: null,
            jha_id: null
        })
        const hazards = ref([])

        const fetchJHA = async () => {
            try {
                const response = await axios.get(`/jha/${props.jhaId}`)
                jhaTitle.value = response.data.title
            } catch (error) {
                console.error('Error fetching JHA', error)
            }
        }

        const fetchStep = async () => {
            try {
                if (props.stepId) {
                    isEditing.value = true
                    const response = await axios.get(`/step/${props.stepId}`)
                    step.value = response.data
                    hazards.value = response.data.hazards // Assuming hazards are returned as part of the step
                }
            } catch (error) {
                console.error('Error fetching Step:', error)
            }
        }

        const saveStep = async () => {
            try {
                if (isEditing.value) {
                    // Update step description
                    await axios.put(`/step/${props.stepId}`, {
                        step_description: step.value.step_description
                    })

                    // Update hazards
                    for (const hazard of hazards.value) {
                        if (hazard.id) {
                            // Existing hazard, update it
                            await axios.put(`/hazard/${hazard.id}`, {
                                description: hazard.description,
                                controls: hazard.controls
                            })
                        } else {
                            // New hazard, add it
                            await axios.post(`/step/${props.stepId}/hazard`, {
                                description: hazard.description,
                                controls: hazard.controls
                            })
                        }
                    }
                } else {
                    // Create new step
                    const response = await axios.post(`/jha/${props.jhaId}/step`, {
                        step_description: step.value.step_description
                    })
                    step.value.id = response.data['New Step'].id

                    // Add hazards
                    for (const hazard of hazards.value) {
                        await axios.post(`/step/${step.value.id}/hazard`, {
                            description: hazard.description,
                            controls: hazard.controls
                        })
                    }
                }

                router.push({ name: 'EditJHA', params: { id: props.jhaId } })
            } catch (error) {
                console.error('Error saving Step:', error)
            }
        }

        const addHazard = () => {
            hazards.value.push({
                description: '',
                controls: ''
            })
        }

        const deleteHazard = async (hazard_id) => {
            if (hazard_id) {
                try {
                    await axios.delete(`/hazard/${hazard_id}`)
                    hazards.value = hazards.value.filter(hazard => hazard.id !== hazard_id)
                } catch (error) {
                    console.error('Error deleting Hazard:', error)
                }
            } else {
                // Remove hazard from local list if it's not yet saved to backend
                hazards.value.pop()
            }
        }

        const cancel = () => {
            router.push({ name: 'JHAList' })
        }

        onMounted(() => {
            fetchJHA()
            fetchStep()
        })

        return {
            jhaTitle,
            step,
            hazards,
            isEditing,
            saveStep,
            addHazard,
            deleteHazard,
            cancel
        }
    }
}
</script>