<template>
    <div class="container mt-5">
        <h2 class="mb-4">{{ isEditing ? 'Edit' : 'Add' }} JHA</h2>


        <SuccessNotification ref="notification" message="JHA saved Successfully"/>

        <form @submit.prevent="saveJHA">
            <div class="mb-3">
                <label class="form-label">Title</label>
                <input v-model="jha.title" type="text" class="form-control" required />
            </div>

            <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea v-model="jha.job_description" class="form-control" rows="3" required></textarea>
            </div>

            <div class="row mb-3">
                <div class="col">
                    <label class="form-label">Author</label>
                    <input v-model="jha.author" type="text" class="form-control" required />
                </div>
                <div class="col">
                    <label class="form-label">Job Location</label>
                    <input v-model="jha.job_location" type="text" class="form-control" required />
                </div>
            </div>

            <h3>Steps</h3>
            <div class="d-flex justify-content-between align-items-center mb-2">
                <span>Steps</span>
                <div class="tooltip-wrapper">
                    <button
                    class="btn btn-success btn-sm"
                    :disabled="!jha.id"
                    @click.prevent="goToAddStep"
                    >
                    + Add Step
                    </button>
                    <span v-if="!jha.id" class="tooltip-text">Please save the JHA to add steps</span>
                </div>
            </div>

            <table class="table table-striped">
                <thead>
                    <tr>
                        <th style="width: 70px;">Step</th>
                        <th>Description</th>
                        <th>Hazards</th>
                        <th>Controls</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="step in jha.steps" :key="step.id" @click="editStep(step.id)" class="cursor-pointer">
                        <td class="align-middle" @click.stop>
                            <input v-model.number="step.step_number" @focus="captureOldStepNumber(step)" @blur="handleStepNumberChange(step)" type="number" min="1" class="form-control">
                        </td>
                        <td class="align-middle">{{ step.step_description }}</td>
                        <td>
                            <div v-for="(hazard, index) in step.hazards" :key="index">
                                {{ hazard.description }}
                                <hr v-if="step.hazards.length - 1 > index" class="my-2">
                            </div>
                        </td>
                        <td>
                            <div v-for="(hazard, index) in step.hazards" :key="index">
                                {{ hazard.controls }}
                                <hr v-if="step.hazards.length - 1 > index" class="my-2">
                            </div>
                        </td>
                        <td class="align-middle">
                            <button class="btn btn-danger btn-sm" @click.stop="deleteStep(step.id)">Delete</button>
                        </td>
                    </tr>
                </tbody>
            </table>

            <div class="d-flex justify-content-between mt-4">
                <button type="submit" class="btn btn-primary">Save</button>
                <router-link to="/" class="btn btn-secondary">Cancel</router-link>
            </div>
        </form>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import SuccessNotification from './Notification.vue';

export default {
    name: 'JHAForm',
    components: {
        SuccessNotification
    },
    setup() {
        const route = useRoute()
        const router = useRouter()
        const isEditing = ref(false)
        const oldStepNumber = ref(null)
        const jha = ref({
            id: null,
            title: '',
            author: '',
            job_location: '',
            job_description: '',
            steps: []
        })

        const notification = ref(null)

        const fetchJHA = async (id) => {
            try {
                const response = await axios.get(`/jha/${id}`)
                jha.value = response.data
            } catch (error) {
                console.error('Error fetching JHA', error)
            }
        }

        const captureOldStepNumber = (step) => {
            oldStepNumber.value = step.step_number
        }

        
        const handleStepNumberChange = (changeStep) => {
            const newStepNumber = changeStep.step_number

            if (newStepNumber === oldStepNumber.value) {
                return
            }

            const conflictingStep = jha.value.steps.find(
                (step) => step.step_number === newStepNumber && step.id !== changeStep.id
            )
            if (conflictingStep) {
                conflictingStep.step_number = oldStepNumber.value
  
            }
        }

        const saveJHA = async () => {
            try {

                const payload = {
                    title: jha.value.title,
                    author: jha.value.author,
                    job_location: jha.value.job_location,
                    job_description: jha.value.job_description,
                }

                if (isEditing.value) {
                    await axios.put(`/jha/${jha.value.id}`, jha.value)
                    for (const step of jha.value.steps) {
                        await axios.put(`/step/${step.id}`, {
                            step_number: step.step_number,
                            step_description: step.step_description,
                        })
                    }
                } else {
                    const response = await axios.post('/jha', payload)
                    jha.value.id = response.data.id
                }

                notification.value.show()

                await fetchJHA(jha.value.id)
 
            } catch (error) {
                console.error('Error saving JHA', error)
            }
        }

        const goToAddStep = () => {
            if (jha.value.id) {
                router.push({ name: 'AddStep', params: { jhaId: jha.value.id } })
            }
        }


        const editStep = (stepId) => {
            router.push({ name: 'EditStep', params: { jhaId: jha.value.id, stepId } })
        }


        const deleteStep = async (stepId) => {
            try {
                await axios.delete(`/step/${stepId}`)
                jha.value.steps = jha.value.steps.filter(step => step.id !== stepId)
            } catch (error) {
                console.error('Error deleting step', error)
            }
        }

        onMounted(() => {
            if (route.name === 'EditJHA') {
                isEditing.value = true
                fetchJHA(route.params.id)
            }
        })


        return {
            jha,
            isEditing,
            saveJHA,
            editStep,
            deleteStep, 
            notification,
            captureOldStepNumber,
            handleStepNumberChange,
            goToAddStep
        }
    }
}
</script>

<style>
.cursor-pointer {
    cursor: pointer;
}

hr {
    border: 1px solid #ccc;
}

.tooltip-wrapper {
  position: relative;
  display: inline-block;
}

.tooltip-text {
  visibility: hidden;
  width: 200px;
  background-color: #555;
  color: #fff;
  text-align: center;
  padding: 5px;
  border-radius: 6px;

  position: absolute;
  z-index: 1;
  bottom: 125%; 
  left: 50%;
  margin-left: -100px;

  /* Tooltip arrow */
  opacity: 0;
  transition: opacity 0.3s;
}

.tooltip-wrapper:hover .tooltip-text {
  visibility: visible;
  opacity: 1;
}
</style>