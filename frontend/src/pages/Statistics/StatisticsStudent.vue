<template>
	<div class="px-5 pt-5 pb-10">
		<div v-if="chartDetails.data">
			<div class="grid grid-cols-1 lg:grid-cols-5 gap-4">
				<Tooltip :text="__('Courses in Enrolled')">
					<div class="border rounded-xl p-4 flex items-center gap-4">
						<div class="bg-primary-50 w-12 h-12 rounded-full flex items-center justify-center">
							<BookIcon class="text-primary-500 w-6 h-6" />
						</div>
						<div class="flex-1">
							<div class="text-xl text-gray-900 font-semibold">{{ chartDetails.data.enrollments.count }}
							</div>
							<div class="text-sm text-gray-700">{{ __('Enrolled') }}</div>
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
							<div class="text-sm text-gray-700">{{ __('In Progress') }}</div>
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
							<div class="text-sm text-gray-700">{{ __('Completed') }}</div>
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
							<div class="text-sm text-gray-700">{{ __('Certificates') }}</div>
						</div>
					</div>
				</Tooltip>
				<Tooltip :text="__('Average time to complete a course')">
					<div class="border rounded-xl p-4 flex items-center gap-4">
						<div class="bg-primary-50 w-12 h-12 rounded-full flex items-center justify-center">
							<ClockIcon class="text-primary-500 w-6 h-6" />
						</div>
						<div class="flex-1">
							<div class="text-xl text-gray-900 font-semibold">
								{{ chartDetails.data.avg_completion_time?.seconds > 0 ? formatDuration(chartDetails.data.avg_completion_time.seconds) : '—' }}
							</div>
							<div class="text-sm text-gray-700">{{ __('Avg Completion Time') }}</div>
						</div>
					</div>
				</Tooltip>
			</div>

			<div v-if="studentChartData.data" class="flex flex-col gap-4 mt-4">
				<div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
					<!-- Chart 1: Pre-Test & Post-Test Gauges -->
					<div class="border rounded-xl">
						<div class="text-lg text-gray-900 font-medium px-5 py-3 border-b">
							{{ __('Average Pre-Test & Post-Test') }}
						</div>
						<div class="flex items-center justify-around px-5 py-3">
							<GaugeChart
								:value="studentChartData.data.pre_test_avg"
								:label="__('Pre-Test')"
								color="#125CA2"
							/>
							<GaugeChart
								:value="studentChartData.data.post_test_avg"
								:label="__('Post-Test')"
								color="#01C295"
							/>
						</div>
					</div>

					<!-- Chart 2: Top 5 Post-Test Scores -->
					<div class="border rounded-xl min-h-72">
						<div class="text-lg text-gray-900 font-medium px-5 py-3 border-b">
							{{ __('Top 5 Courses by Post-Test Score') }}
						</div>
						<div class="px-5 py-3">
							<BarChart
								:data="studentChartData.data.top_courses"
								:name="__('Score (%)')"
							/>
						</div>
					</div>
				</div>

				<!-- Chart 3: Course Status (full width) -->
				<div class="border rounded-xl">
					<div class="text-lg text-gray-900 font-medium px-5 py-3 border-b">
						{{ __('Course Status') }}
					</div>
					<DonutChart :data="studentChartData.data.course_status" />
				</div>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { createResource, Tooltip } from 'frappe-ui'
import { Clock as ClockIcon } from 'lucide-vue-next'
import BookIcon from '@/components/Icons/BookIcon.vue'
import TickCircleIcon from '@/components/Icons/TickCircleIcon.vue'
import AwardIcon from '@/components/Icons/AwardIcon.vue'
import GaugeChart from '@/components/GaugeChart.vue'
import BarChart from '@/components/BarChart.vue'
import DonutChart from '@/components/DonutChart.vue'
import { formatDuration } from '@/utils'

const props = defineProps<{
	myLiveClasses: any
}>()

const chartDetails = createResource({
	url: 'lms.lms.api.get_user_chart_details',
	auto: true,
})

const studentChartData = createResource({
	url: 'lms.lms.api.get_student_chart_data',
	auto: true,
})
</script>
