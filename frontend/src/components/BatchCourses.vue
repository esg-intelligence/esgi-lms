<template>
	<div>
		<div class="flex items-center justify-between mb-4">
			<div class="text-xl font-semibold text-ink-gray-9">
				{{ __('Courses') }}
			</div>

			<Button
				v-if="canSeeAddButton()"
				@click="openCourseModal()"
				variant="solid"
			>
				<template #prefix>
					<Plus class="h-4 w-4" />
				</template>
				{{ __('Add') }}
			</Button>
		</div>
		<div v-if="courses.data?.length">
			<ListView
				:columns="getCoursesColumns()"
				:rows="courses.data"
				row-key="batch_course"
				:options="{
					showTooltip: false,
					selectable: user.data?.is_student ? false : true,
					getRowRoute: (row) => ({
						name: 'CourseDetail',
						params: { courseName: row.name },
					}),
				}"
			>
				<ListRows>
					<ListRow
						:row="row"
						v-for="row in courses.data"
						class="border border-gray-100 mb-4 px-4 py-3 [&_.h-px]:hidden"
					>
						<template #default="{ column, item }">
							<ListRowItem :item="row[column.key]" :align="column.align">
								<div
									v-if="column.key == 'title'"
									class="w-full flex items-center justify-between"
								>
									<div class="min-w-0 flex-1">
										<p class="text-gray-900 font-semibold text-base mb-1">
											{{ row['title'] }}
										</p>
										<div class="text-sm text-gray-600">
											<span>
												{{ `${row['lessons']} Lessons` }}
											</span>
											<span class="text-gray-700">{{ ` • ` }}</span>
											<span>
												{{ `${row['enrollments']} Enrollments` }}
											</span>
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
								@click="removeCourses(selections, unselectAll)"
							>
								<Trash2 class="h-4 w-4 stroke-1.5" />
							</Button>
						</div>
					</template>
				</ListSelectBanner>
			</ListView>
		</div>
		<div v-else class="flex flex-col items-center justify-center mt-6">
			<EmptyIcon class="size-24 mb-6" />
			<h3 class="text-lg font-bold text-gray-900 mb-2">
				Nothing to see here yet
			</h3>
			<p class="text-gray-500 text-ms font-medium">
				{{ __('No courses added') }}
			</p>
		</div>
		<BatchCourseModal
			v-model="showCourseModal"
			:batch="batch"
			v-model:courses="courses"
		/>
	</div>
</template>
<script setup>
import { ref, inject } from 'vue'
import BatchCourseModal from '@/components/Modals/BatchCourseModal.vue'
import {
	createResource,
	ListHeader,
	ListHeaderItem,
	ListSelectBanner,
	ListRow,
	ListRows,
	ListView,
	ListRowItem,
	toast,
} from 'frappe-ui'
import { ChevronRight, Plus, Trash2 } from 'lucide-vue-next'
import Button from './ui/Button.vue'
const readOnlyMode = window.read_only_mode

const showCourseModal = ref(false)
const user = inject('$user')

const props = defineProps({
	batch: {
		type: String,
		required: true,
	},
})

const courses = createResource({
	url: 'lms.lms.utils.get_batch_courses',
	params: {
		batch: props.batch,
	},
	auto: true,
})

const openCourseModal = () => {
	showCourseModal.value = true
}

const getCoursesColumns = () => {
	return [
		{
			label: 'Title',
			key: 'title',
		},
	]
}

const deleteCourses = createResource({
	url: 'lms.lms.api.delete_documents',
	makeParams(values) {
		return {
			doctype: 'Batch Course',
			documents: values.courses,
		}
	},
})

const removeCourses = (selections, unselectAll) => {
	deleteCourses.submit(
		{
			courses: Array.from(selections),
		},
		{
			onSuccess(data) {
				courses.reload()
				toast.success(__('Courses deleted successfully'))
				unselectAll()
			},
		},
	)
}

const canSeeAddButton = () => {
	if (readOnlyMode) {
		return false
	}
	return user.data?.is_moderator || user.data?.is_evaluator
}
</script>
