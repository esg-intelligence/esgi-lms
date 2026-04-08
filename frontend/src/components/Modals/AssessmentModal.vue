<template>
	<Dialog
		v-model="show"
		:options="{
			title: __('Add an assessment'),
			size: 'sm',
		}"
	>
		<template #body-content>
			<div class="space-y-4">
				<FormWrapper type="combobox">
					<FormControl
						type="select"
						:options="assessmentTypes"
						v-model="assessmentType"
						:label="__('Type')"
					/>
				</FormWrapper>
				<FormWrapper type="combobox">
					<Link
						v-model="assessment"
						:doctype="assessmentType"
						:label="__('Assessment')"
						:onCreate="
							(value, close) => {
								close()
								if (assessmentType === 'LMS Quiz') {
									router.push({
										name: 'QuizForm',
										params: {
											quizID: 'new',
										},
									})
								} else if (assessmentType === 'LMS Assignment') {
									router.push({
										name: 'Assignments',
									})
								}
							}
						"
					/>
				</FormWrapper>
			</div>
		</template>
		<template #actions="{ close }">
			<Button class="w-full" variant="solid" @click="addAssessment(close)">
				Submit
			</Button>
		</template>
	</Dialog>
</template>
<script setup>
import { Dialog, FormControl, createResource, toast } from 'frappe-ui'
import Link from '@/components/Controls/Link.vue'
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import FormWrapper from '../ui/FormWrapper.vue'

const show = defineModel()
const assessmentType = ref(null)
const assessment = ref(null)
const assessments = defineModel('assessments')
const router = useRouter()

const props = defineProps({
	batch: {
		type: String,
		default: null,
	},
})

const assessmentResource = createResource({
	url: 'frappe.client.insert',
	makeParams(values) {
		return {
			doc: {
				doctype: 'LMS Assessment',
				parent: props.batch,
				parenttype: 'LMS Batch',
				parentfield: 'assessment',
				assessment_type: assessmentType.value,
				assessment_name: assessment.value,
			},
		}
	},
})

const addAssessment = (close) => {
	assessmentResource.submit(
		{},
		{
			onSuccess(data) {
				assessments.value.reload()
				toast.success(__('Assessment added successfully'))
				close()
			},
		},
	)
}

const assessmentTypes = computed(() => {
	return [
		{ label: __('Quiz'), value: 'LMS Quiz' },
		{ label: __('Assignment'), value: 'LMS Assignment' },
		{ label: __('Programming Exercise'), value: 'LMS Programming Exercise' },
	]
})
</script>
