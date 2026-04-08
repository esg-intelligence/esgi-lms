<template>
	<Dialog v-model="show" :options="{
		size: 'lg',
	}">
		<template #body>
			<div class="p-5 text-base">
				<div class="text-lg text-ink-gray-9 font-semibold mb-5">{{ __('Duplicate Quiz') }}</div>
				<div class="space-y-4 max-h-[75vh] overflow-y-auto">
					<FormControl v-model="quiz.title" :label="__('Title')" :required="true" />
				</div>
				<div class="flex justify-end space-x-2 mt-5">
					<Button variant="solid" @click="save">
						{{ __('Save') }}
					</Button>
				</div>
			</div>
		</template>
	</Dialog>
</template>
<script setup>
import { Button, Dialog, FormControl, toast, createResource } from 'frappe-ui'
import { reactive } from 'vue'
import { escapeHTML } from '@/utils'

const show = defineModel()

const quiz = reactive({
	title: '',
})
const props = defineProps({
	selected: { type: String },
	reload: { type: Function }
})

const resource = createResource({
	url: 'lms.lms.api.duplicate_quiz',
	makeParams(values) {
		return {
			title: values.title,
			base_name: values.base_name
		}
	},
	onSuccess() {
		props.reload()
		toast.success(__('Quiz duplicated successfully'))
	},
})

const validateTitle = () => {
	quiz.title = escapeHTML(quiz.title.trim())
}

const save = () => {
	validateTitle()
	duplicateQuiz()
}

const duplicateQuiz = () => {
	resource.submit(
		{ ...quiz, base_name: props.selected },
		{
			onSuccess() {
				console.log
				show.value = false
			},
		}
	)
}
</script>
