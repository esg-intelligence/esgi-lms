<template>
	<div class="px-5 pt-5 pb-10">
		<div v-if="chartDetails.data">
			<div class="grid grid-cols-1 lg:grid-cols-4 gap-4">
				<Tooltip :text="__('Courses in Enrolled')">
					<div class="border rounded-xl p-4 flex items-center gap-4">
						<div class="bg-primary-50 w-12 h-12 rounded-full flex items-center justify-center">
							<Book class="text-primary-500 w-6 h-6" />
						</div>
						<div class="flex-1">
							<div class="text-xl text-gray-900 font-semibold">{{ chartDetails.data.enrollments.count }}
							</div>
							<div class="text-sm text-gray-700">Enrolled</div>
						</div>
					</div>
				</Tooltip>
				<Tooltip :text="__('Courses In Progress')">
					<div class="border rounded-xl p-4 flex items-center gap-4">
						<div class="bg-primary-50 w-12 h-12 rounded-full flex items-center justify-center">
							<BookIcon class="text-primary-500 w-6 h-6" />
						</div>
						<div class="flex-1">
							<div class="text-xl text-gray-900 font-semibold">{{ chartDetails.data.in_progress.count }}
							</div>
							<div class="text-sm text-gray-700">In Progress</div>
						</div>
					</div>
				</Tooltip>
				<Tooltip :text="__('Course Completed')">
					<div class="border rounded-xl p-4 flex items-center gap-4">
						<div class="bg-primary-50 w-12 h-12 rounded-full flex items-center justify-center">
							<TickCircleIcon class="text-primary-500 w-6 h-6" />
						</div>
						<div class="flex-1">
							<div class="text-xl text-gray-900 font-semibold">{{ chartDetails.data.completions.count }}
							</div>
							<div class="text-sm text-gray-700">Completed</div>
						</div>
					</div>
				</Tooltip>
				<Tooltip :text="__('Certifications')">
					<div class="border rounded-xl p-4 flex items-center gap-4">
						<div class="bg-primary-50 w-12 h-12 rounded-full flex items-center justify-center">
							<AwardIcon class="text-primary-500 w-6 h-6" />
						</div>
						<div class="flex-1">
							<div class="text-xl text-gray-900 font-semibold">{{ chartDetails.data.certifications.count
							}}
							</div>
							<div class="text-sm text-gray-700">Certificates</div>
						</div>
					</div>
				</Tooltip>
			</div>
		</div>
	</div>
</template>
<script setup lang="ts">
import { inject } from 'vue'
import { createResource, Tooltip } from 'frappe-ui'
import {
	Book,
} from 'lucide-vue-next'

const dayjs = inject<any>('$dayjs')

const props = defineProps<{
	myLiveClasses: any
}>()

const chartDetails = createResource({
	url: 'lms.lms.api.get_user_chart_details',
	auto: true,
})

</script>
