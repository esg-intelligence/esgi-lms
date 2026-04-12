<template>
	<header
		class="sticky top-0 z-10 flex items-center justify-between border-b bg-surface-white px-3 py-2.5 sm:px-5"
	>
		<Breadcrumbs v-if="submissionDetails.doc" :items="breadcrumbs" />
		<div class="space-x-2">
			<Badge
				v-if="submissionDetails.isDirty"
				:label="__('Not Saved')"
				variant="subtle"
				theme="orange"
			/>
			<Button variant="solid" @click="saveSubmission()">
				{{ __('Save') }}
			</Button>
		</div>
	</header>
	<div v-if="submissionDetails.doc" class="w-2/3 border-x mx-auto py-5">
		<div class="text-xl px-10 font-semibold text-ink-gray-9 mb-5">
			{{ submissionDetails.doc.member_name }}
		</div>
		<div class="space-y-4 border-b pb-5 px-10">
			<div class="grid grid-cols-2 gap-5">
				<FormControl
					v-model="submissionDetails.doc.quiz_title"
					:label="__('Quiz')"
					:disabled="true"
				/>
				<FormControl
					v-model="submissionDetails.doc.member_name"
					:label="__('Member')"
					:disabled="true"
				/>
			</div>

			<div class="grid grid-cols-2 gap-5">
				<FormControl
					v-model="submissionDetails.doc.score"
					:label="__('Score')"
					:disabled="true"
				/>
				<FormControl
					v-model="submissionDetails.doc.percentage"
					:label="__('Percentage')"
					:disabled="true"
				/>
			</div>

			<div v-if="isOpenEndedSubmission" class="pt-2 space-y-3">
				<div class="text-sm font-medium text-ink-gray-7">{{ __('Grade Submission') }}</div>
				<div
					v-if="submissionDetails.doc.status && submissionDetails.doc.status !== 'Not Graded'"
					class="text-sm text-ink-gray-6"
				>
					{{ __('Current status:') }}
					<span
						class="font-semibold"
						:class="submissionDetails.doc.status === 'Pass' ? 'text-ink-green-2' : 'text-ink-red-3'"
					>
						{{ submissionDetails.doc.status }}
					</span>
					<span v-if="submissionDetails.doc.status === 'Fail' && submissionDetails.doc.fail_count" class="text-ink-gray-5 ml-1">
						({{ __('Fail #{0}').format(submissionDetails.doc.fail_count) }})
					</span>
				</div>
				<div class="flex gap-2">
					<Button variant="solid" theme="green" @click="gradeSubmission('Pass')" :loading="grading">
						{{ __('Pass') }}
					</Button>
					<Button variant="subtle" theme="red" @click="gradeSubmission('Fail')" :loading="grading">
						{{ __('Fail') }}
					</Button>
				</div>
			</div>
		</div>

		<div class="divide-y">
			<div
				v-for="(row, index) in submissionDetails.doc.result"
				class="py-5 px-10 space-y-4"
			>
				<div class="text-ink-gray-9">
					<span class="font-semibold"> {{ __('Question') }}: </span>
					<span class="leading-5" v-html="row.question"> </span>
				</div>
				<div class="text-ink-gray-9">
					<span class="font-semibold"> {{ __('Answer') }}: </span>
					<span class="leading-5" v-html="row.answer"></span>
				</div>
				<div class="grid grid-cols-2 gap-5">
					<FormControl v-model="row.marks" :label="__('Marks')" />
					<FormControl
						v-model="row.marks_out_of"
						:label="__('Marks out of')"
						:disabled="true"
					/>
				</div>
			</div>
		</div>
	</div>
</template>
<script setup>
import {
	createDocumentResource,
	createResource,
	Breadcrumbs,
	FormControl,
	Button,
	Badge,
	usePageMeta,
	toast,
	call,
} from 'frappe-ui'
import { computed, onBeforeUnmount, onMounted, inject, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { sessionStore } from '@/stores/session'

const { brand } = sessionStore()
const router = useRouter()
const user = inject('$user')

onMounted(() => {
	if (!user.data?.is_instructor && !user.data?.is_moderator)
		router.push({ name: 'Courses' })

	window.addEventListener('keydown', keyboardShortcut)
})

onBeforeUnmount(() => {
	window.removeEventListener('keydown', keyboardShortcut)
})

const keyboardShortcut = (e) => {
	if (
		e.key === 's' &&
		(e.ctrlKey || e.metaKey) &&
		!e.target.classList.contains('ProseMirror')
	) {
		saveSubmission()
		e.preventDefault()
	}
}

const props = defineProps({
	submission: {
		type: String,
		required: true,
	},
})

const submissionDetails = createDocumentResource({
	doctype: 'LMS Quiz Submission',
	name: props.submission,
	auto: true,
})

const breadcrumbs = computed(() => {
	return [
		{
			label: __('Quiz Submissions'),
			route: {
				name: 'QuizSubmissionList',
				params: {
					quizID: submissionDetails.doc.quiz,
				},
			},
		},
		{
			label: submissionDetails.doc.quiz_title,
		},
	]
})

const grading = ref(false)

const quizQuestions = createResource({
	url: 'frappe.client.get_list',
	makeParams() {
		return {
			doctype: 'LMS Quiz Question',
			filters: { parent: submissionDetails.doc?.quiz },
			fields: ['type'],
		}
	},
	auto: false,
})

watch(
	() => submissionDetails.doc?.quiz,
	(quiz) => {
		if (quiz) quizQuestions.reload()
	}
)

const isOpenEndedSubmission = computed(() => {
	if (!quizQuestions.data?.length) return false
	return quizQuestions.data.every((q) => q.type === 'Open Ended')
})

const gradeSubmission = (status) => {
	grading.value = true
	call(
		'lms.lms.doctype.lms_quiz_submission.lms_quiz_submission.grade_quiz_submission',
		{ submission_name: props.submission, status }
	)
		.then(() => {
			submissionDetails.reload()
			toast.success(__('Submission graded successfully'))
		})
		.catch((err) => {
			toast.error(err.messages?.[0] || err)
		})
		.finally(() => {
			grading.value = false
		})
}

const saveSubmission = () => {
	submissionDetails.save.submit(
		{},
		{
			onError(err) {
				toast.error(err.messages?.[0] || err)
			},
		}
	)
}

usePageMeta(() => {
	return {
		title: `${submissionDetails.doc?.quiz_title}`,
		icon: brand.favicon,
	}
})
</script>
