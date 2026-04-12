<template>
	<Dialog
		v-model="show"
		:options="{
			size: 'lg',
		}"
	>
		<template #body>
			<div class="p-5 text-base">
				<div class="text-lg text-ink-gray-9 font-semibold mb-5">
					{{
						assignmentID === 'new'
							? __('Create an Assignment')
							: __('Edit Assignment')
					}}
				</div>
				<div class="space-y-4 max-h-[75vh] overflow-y-auto">
					<FormControl
						v-model="assignment.title"
						:label="__('Title')"
						:required="true"
					/>
					<FormControl
						v-model="assignment.type"
						type="select"
						:options="assignmentOptions"
						:label="__('Submission Type')"
						:required="true"
					/>
					<!-- <FormControl
						v-model="assignment.category"
						type="select"
						:options="categoryOptions"
						:label="__('Category')"
					/> -->
					<FormWrapper class="mt-4" type="combobox">
						<Link
							:label="__('Industry')"
							v-model="assignment.industry"
							doctype="Industry"
						/>
					</FormWrapper>
					<FormControl
						v-model="assignment.passing_score"
						type="number"
						:label="__('Passing Score')"
						:description="__('Minimum score required to pass. Leave empty for no score requirement.')"
					/>
					<div>
						<div class="text-xs text-ink-gray-5 mb-2">
							{{ __('Question') }}
							<span class="text-ink-red-3">*</span>
						</div>
						<TextEditor
							:content="assignment.question"
							@change="(val) => (assignment.question = val)"
							:editable="true"
							:fixedMenu="true"
							editorClass="prose-sm max-w-none border-b border-x bg-surface-gray-2 rounded-b-md py-1 px-2 min-h-[7rem] max-h-[18rem] overflow-y-auto"
						/>
					</div>
				</div>

				<div class="flex justify-end space-x-2 mt-5">
					<router-link
						:to="{
							name: 'AssignmentSubmissionList',
							query: {
								assignmentID: assignmentID,
							},
						}"
					>
						<Button v-if="assignmentID !== 'new'" variant="subtle">
							{{ __('Check Submissions') }}
						</Button>
					</router-link>
					<Button variant="solid" @click="saveAssignment">
						{{ __('Save') }}
					</Button>
				</div>
			</div>
		</template>
	</Dialog>
</template>
<script setup lang="ts">
import { Button, Dialog, FormControl, TextEditor, toast } from 'frappe-ui'
import FormWrapper from '@/components/ui/FormWrapper.vue'
import Link from '@/components/Controls/Link.vue'
import { computed, reactive, watch } from 'vue'
import { escapeHTML } from '@/utils'

const show = defineModel()
const assignments = defineModel<Assignments>('assignments')

interface Assignment {
	title: string
	type: string
	question: string
	industry: string
}

interface Assignments {
	data: Assignment[]
	get: (params: { doctype: string; name: string }) => Promise<Assignment>
	insert: {
		submit: (params: Assignment, options: { onSuccess: () => void }) => void
	}
}

const assignment = reactive({
	title: '',
	type: '',
	question: '',
	industry: '',
	passing_score: null,
	category: null,
})

const props = defineProps({
	assignmentID: {
		type: String,
		default: 'new',
	},
})

watch(
	() => props.assignmentID,
	(val) => {
		if (val !== 'new') {
			assignments.value?.data.forEach((row) => {
				if (row.name === val) {
					assignment.title = row.title
					assignment.type = row.type
					assignment.question = row.question
					assignment.industry = row.industry
					assignment.passing_score = row.passing_score || null
					assignment.category = row.category || null
				}
			})
		}
	},
	{ flush: 'post' }
)

watch(show, (newVal) => {
	if (newVal && props.assignmentID === 'new') {
		assignment.title = ''
		assignment.type = ''
		assignment.question = ''
		assignment.industry = ''
		assignment.passing_score = null
		assignment.category = null
	}
})

const validateTitle = () => {
	assignment.title = escapeHTML(assignment.title.trim())
}

const saveAssignment = () => {
	validateTitle()
	if (props.assignmentID == 'new') {
		createAssignment()
	} else {
		updateAssignment()
	}
}

const createAssignment = () => {
	assignments.value.insert.submit(
		{
			...assignment,
		},
		{
			onSuccess() {
				show.value = false
				toast.success(__('Assignment created successfully'))
			},
		}
	)
}

const updateAssignment = () => {
	assignments.value.setValue.submit(
		{
			...assignment,
			name: props.assignmentID,
		},
		{
			onSuccess() {
				show.value = false
				toast.success(__('Assignment updated successfully'))
			},
		}
	)
}

const assignmentOptions = computed(() => {
	return [
		{ label: __('PDF'), value: 'PDF' },
		{ label: __('Image'), value: 'Image' },
		{ label: __('Document'), value: 'Document' },
		{ label: __('Text'), value: 'Text' },
		{ label: __('URL'), value: 'URL' },
	]
})

const categoryOptions = computed(() => {
	return [
		{ label: '—', value: null },
		{ label: __('Pre-Test'), value: 'Pre-Test' },
		{ label: __('Post-Test'), value: 'Post-Test' },
	]
})
</script>
