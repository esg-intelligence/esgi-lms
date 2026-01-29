<template>
	<Dialog
		v-model="show"
		:options="{
			title: __('Help Us Get Better With Your Feedback'),
			size: 'xl',
		}"
	>
		<template #body-content>
			<div class="space-y-4">
				<div
					class="space-y-4 [&_.\!fill-yellow-500]:!fill-warning-500 [&_.\!fill-yellow-200]:!fill-warning-200"
				>
					<Rating
						v-for="key in ratingKeys"
						:key="key"
						v-model="feedback[key]"
						:label="__(convertToTitleCase(key))"
					/>
				</div>
				<FormWrapper type="textarea">
					<FormControl
						v-model="feedback.feedback"
						type="textarea"
						:label="__('Feedback')"
						:rows="6"
						placeholder="Share your thoughts about the batch..."
					/>
				</FormWrapper>
			</div>
		</template>
		<template #actions="{ close }">
			<Button
				variant="solid"
				class="w-full !bg-primary-500"
				:loading="feedbackResource.loading"
				@click="submitFeedback(close)"
			>
				{{ __('Submit Feedback') }}
			</Button>
		</template>
	</Dialog>
</template>

<script setup>
import { reactive, inject } from 'vue'
import { Dialog, Rating, FormControl, createResource } from 'frappe-ui'
import { convertToTitleCase } from '@/utils'
import Button from '@/components/ui/Button.vue'
import FormWrapper from '../ui/FormWrapper.vue'

const show = defineModel()
const props = defineProps({
	batch: {
		type: String,
		required: true,
	},
})

const user = inject('$user')
const ratingKeys = ['content', 'instructors', 'value']
const feedback = reactive({
	content: 0,
	instructors: 0,
	value: 0,
	feedback: '',
})

const feedbackResource = createResource({
	url: 'frappe.client.insert',
	makeParams(values) {
		const payload = { ...feedback }
		// Scale ratings to 0-1 range as per BatchFeedback.vue logic (where it divides by 5 before sending)
		ratingKeys.forEach((key) => {
			payload[key] = payload[key] / 5
		})

		return {
			doc: {
				doctype: 'LMS Batch Feedback',
				batch: props.batch,
				member: user.data?.name,
				...payload,
			},
		}
	},
	onSuccess() {
		show.value = false
		// Reset form
		Object.assign(feedback, {
			content: 0,
			instructors: 0,
			value: 0,
			feedback: '',
		})
	},
})

const submitFeedback = (close) => {
	feedbackResource.submit(
		{},
		{
			onSuccess: () => {
				close()
			},
		},
	)
}
</script>
