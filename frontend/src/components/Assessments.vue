<template>
	<div>
		<div class="flex items-center justify-between mb-4">
			<div class="text-xl font-semibold text-ink-gray-9">
				{{ __('Assessments') }}
			</div>
			<Button
				v-if="canAddAssessments()"
				@click="showModal = true"
				variant="solid"
			>
				<template #prefix>
					<Plus class="h-4 w-4" />
				</template>
				{{ __('Add') }}
			</Button>
		</div>
		<div v-if="assessments.data?.length" class="text-sm">
			<ListView
				:columns="getAssessmentColumns()"
				:rows="assessments.data"
				row-key="name"
				:options="{
					showTooltip: false,
					getRowRoute: (row) => getRowRoute(row),
					selectable: user.data?.is_student ? false : true,
				}"
			>
				<ListRows>
					<ListRow
						:row="row"
						v-for="row in assessments.data"
						class="border border-gray-100 mb-4 px-4 py-3 [&_.h-px]:hidden"
					>
						<template #default="{ column, item }">
							<ListRowItem :item="row[column.key]" :align="column.align">
								<div
									v-if="column.key == 'title'"
									class="w-full flex items-center justify-between"
								>
									<div class="min-w-0 flex-1">
										<p class="text-gray-900 font-semibold text-sm mb-1">
											{{ row['title'] }}
										</p>
										<div class="text-xs text-gray-600">
											{{ getAssessmentTypeLabel(row['assessment_type']) }}
											<span
												v-if="!user.data?.is_moderator"
												class="text-gray-700"
												>{{ ` • ` }}
												<Badge :theme="getStatusTheme(row['status'])">
													{{ row['status'] }}
												</Badge></span
											>
										</div>
									</div>
									<ChevronRight class="block ml-auto text-gray-600 size-4" />
								</div>
								<span v-else></span>
							</ListRowItem>
						</template>
					</ListRow>
				</ListRows>
				<ListSelectBanner>
					<template #actions="{ unselectAll, selections }">
						<div class="flex gap-2">
							<Button
								variant="ghost"
								theme="red"
								@click="removeAssessments(selections, unselectAll)"
							>
								<Trash2 class="h-4 w-4 stroke-1.5" />
							</Button>
						</div>
					</template>
				</ListSelectBanner>
			</ListView>
		</div>
		<div v-else class="flex flex-col items-center justify-center">
			<EmptyIcon class="size-24 mb-6" />
			<h3 class="text-lg font-bold text-gray-900 mb-2">
				Nothing to see here yet
			</h3>
			<p class="text-gray-500 text-ms font-medium">
				{{ __('No Assessments') }}
			</p>
		</div>
	</div>
	<AssessmentModal
		v-model="showModal"
		v-model:assessments="assessments"
		:batch="props.batch"
	/>
</template>
<script setup>
import {
	ListView,
	ListRow,
	ListRows,
	ListHeader,
	ListHeaderItem,
	ListRowItem,
	ListSelectBanner,
	createResource,
	Badge,
} from 'frappe-ui'
import { inject, ref } from 'vue'
import AssessmentModal from '@/components/Modals/AssessmentModal.vue'
import { ChevronRight, Plus, Trash2 } from 'lucide-vue-next'
import Button from './ui/Button.vue'
import EmptyState from './EmptyState.vue'

const user = inject('$user')
const showModal = ref(false)
const readOnlyMode = window.read_only_mode

const props = defineProps({
	batch: {
		type: String,
		required: true,
	},
	rows: {
		type: Array,
	},
	columns: {
		type: Array,
	},
	options: {
		type: Object,
		default: () => ({
			selectable: true,
			totalCount: 0,
			rowCount: 0,
		}),
	},
})

const assessments = createResource({
	url: 'lms.lms.utils.get_assessments',
	params: {
		batch: props.batch,
	},
	auto: true,
})

const deleteAssessments = createResource({
	url: 'lms.lms.api.delete_documents',
	makeParams(values) {
		return {
			doctype: 'LMS Assessment',
			documents: values.assessments,
		}
	},
})

const removeAssessments = (selections, unselectAll) => {
	deleteAssessments.submit(
		{ assessments: Array.from(selections) },
		{
			onSuccess(data) {
				assessments.reload()
				unselectAll()
			},
		},
	)
}

const getRowRoute = (row) => {
	if (row.assessment_type == 'LMS Assignment') {
		if (row.submission) {
			return {
				name: 'AssignmentSubmission',
				params: {
					assignmentID: row.assessment_name,
					submissionName: row.submission.name,
				},
			}
		} else {
			return {
				name: 'AssignmentSubmission',
				params: {
					assignmentID: row.assessment_name,
					submissionName: 'new',
				},
			}
		}
	} else if (row.assessment_type == 'LMS Programming Exercise') {
		if (row.submission) {
			return {
				name: 'ProgrammingExerciseSubmission',
				params: {
					exerciseID: row.assessment_name,
					submissionID: row.submission.name,
				},
			}
		} else {
			return {
				name: 'ProgrammingExerciseSubmission',
				params: {
					exerciseID: row.assessment_name,
					submissionID: 'new',
				},
			}
		}
	} else {
		return {
			name: 'QuizPage',
			params: {
				quizID: row.assessment_name,
			},
		}
	}
}

const canAddAssessments = () => {
	if (readOnlyMode) return false
	return user.data?.is_moderator || user.data?.is_evaluator
}

const getAssessmentColumns = () => {
	let columns = [
		{
			label: 'Assessment',
			key: 'title',
		},
	]

	return columns
}

const getStatusTheme = (status) => {
	if (status === 'Pass' || status === 'Passed') {
		return 'green'
	} else if (status === 'Not Graded') {
		return 'orange'
	} else {
		return 'red'
	}
}

const getAssessmentTypeLabel = (type) => {
	if (type == 'LMS Assignment') {
		return __('Assignment')
	} else if (type == 'LMS Quiz') {
		return __('Quiz')
	} else if (type == 'LMS Programming Exercise') {
		return __('Programming Exercise')
	}
}
</script>
