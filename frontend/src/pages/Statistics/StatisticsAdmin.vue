<template>
	<div v-if="chartDetails.data" class="p-5">
		<div class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-6 gap-4">
			<Tooltip :text="__('Published Courses')">
				<!-- <NumberChart class="border rounded-xl"
						:config="{ title: 'Courses', value: chartDetails.data.courses.count }" /> -->
				<div class="border rounded-xl p-4 flex items-center gap-4">
					<div class="bg-primary-50 w-12 h-12 rounded-full flex items-center justify-center">
						<BookIcon class="text-primary-500 w-6 h-6" />
					</div>
					<div class="flex-1">
						<div class="text-xl text-gray-900 font-semibold">{{ chartDetails.data.courses.count }}</div>
						<div class="text-sm text-gray-700">{{ __('Courses') }}</div>
					</div>
					<div class="flex items-start h-12">
						<div class="text-sm font-medium flex items-center gap-1"
							:class="chartDetails.data.courses.growth >= 0 ? 'text-primary-500' : 'text-error-500'">
							<component :is="chartDetails.data.courses.growth >= 0 ? ArrowUpIcon : ArrowDownIcon"
								class="w-4 h-4" />
							{{ chartDetails.data.courses.growth }}%
						</div>
					</div>
				</div>
			</Tooltip>
			<Tooltip :text="__('Active Members')">
				<!-- <NumberChart class="border rounded-xl"
						:config="{ title: 'Signups', value: chartDetails.data.users.count }" /> -->
				<div class="border rounded-xl p-4 flex items-center gap-4">
					<div class="bg-primary-50 w-12 h-12 rounded-full flex items-center justify-center">
						<UserCircleAddIcon class="text-primary-500 w-6 h-6" />
					</div>
					<div class="flex-1">
						<div class="text-xl text-gray-900 font-semibold">{{ chartDetails.data.users.count }}</div>
						<div class="text-sm text-gray-700">{{ __('Signups') }}</div>
					</div>
					<div class="flex items-start h-12">
						<div class="text-sm font-medium flex items-center gap-1"
							:class="chartDetails.data.users.growth >= 0 ? 'text-primary-500' : 'text-error-500'">
							<component :is="chartDetails.data.users.growth >= 0 ? ArrowUpIcon : ArrowDownIcon"
								class="w-4 h-4" />
							{{ chartDetails.data.users.growth }}%
						</div>
					</div>
				</div>
			</Tooltip>
			<Tooltip :text="__('Course Enrollments')">
				<!-- <NumberChart class="border rounded-xl" :config="{
						title: 'Enrollments',
						value: chartDetails.data.enrollments.count,
					}" /> -->
				<div class="border rounded-xl p-4 flex items-center gap-4">
					<div class="bg-primary-50 w-12 h-12 rounded-full flex items-center justify-center">
						<ClipboardIcon class="text-primary-500 w-6 h-6" />
					</div>
					<div class="flex-1">
						<div class="text-xl text-gray-900 font-semibold">{{ chartDetails.data.enrollments.count }}</div>
						<div class="text-sm text-gray-700">{{ __('Enrollments') }}</div>
					</div>
					<div class="flex items-start h-12">
						<div class="text-sm font-medium flex items-center gap-1"
							:class="chartDetails.data.enrollments.growth >= 0 ? 'text-primary-500' : 'text-error-500'">
							<component :is="chartDetails.data.enrollments.growth >= 0 ? ArrowUpIcon : ArrowDownIcon"
								class="w-4 h-4" />
							{{ chartDetails.data.enrollments.growth }}%
						</div>
					</div>
				</div>
			</Tooltip>
			<Tooltip :text="__('Course Completions')">
				<!-- <NumberChart class="border rounded-xl" :config="{
						title: 'Completions',
						value: chartDetails.data.completions.count,
					}" /> -->
				<div class="border rounded-xl p-4 flex items-center gap-4">
					<div class="bg-primary-50 w-12 h-12 rounded-full flex items-center justify-center">
						<TickCircleIcon class="text-primary-500 w-6 h-6" />
					</div>
					<div class="flex-1">
						<div class="text-xl text-gray-900 font-semibold">{{ chartDetails.data.completions.count }}</div>
						<div class="text-sm text-gray-700">{{ __('Completions') }}</div>
					</div>
					<div class="flex items-start h-12">
						<div class="text-sm font-medium flex items-center gap-1"
							:class="chartDetails.data.completions.growth >= 0 ? 'text-primary-500' : 'text-error-500'">
							<component :is="chartDetails.data.completions.growth >= 0 ? ArrowUpIcon : ArrowDownIcon"
								class="w-4 h-4" />
							{{ chartDetails.data.completions.growth }}%
						</div>
					</div>
				</div>
			</Tooltip>
			<Tooltip :text="__('Certified Members')">
				<!-- <NumberChart class="border rounded-xl" :config="{
						title: 'Certifications',
						value: chartDetails.data.certifications.count,
					}" /> -->
				<div class="border rounded-xl p-4 flex items-center gap-4">
					<div class="bg-primary-50 w-12 h-12 rounded-full flex items-center justify-center">
						<AwardIcon class="text-primary-500 w-6 h-6" />
					</div>
					<div class="flex-1">
						<div class="text-xl text-gray-900 font-semibold">{{ chartDetails.data.certifications.count }}
						</div>
						<div class="text-sm text-gray-700">{{ __('Certifications') }}</div>
					</div>
					<div class="flex items-start h-12">
						<div class="text-sm font-medium flex items-center gap-1"
							:class="chartDetails.data.certifications.growth >= 0 ? 'text-primary-500' : 'text-error-500'">
							<component :is="chartDetails.data.certifications.growth >= 0 ? ArrowUpIcon : ArrowDownIcon"
								class="w-4 h-4" />
							{{ chartDetails.data.certifications.growth }}%
						</div>
					</div>
				</div>
			</Tooltip>
			<Tooltip :text="__('Average time to complete a course (completions only)')">
				<div class="border rounded-xl p-4 flex items-center gap-4">
					<div class="bg-primary-50 w-12 h-12 rounded-full flex items-center justify-center">
						<ClockIcon class="text-primary-500 w-6 h-6" />
					</div>
					<div class="flex-1">
						<div class="text-xl text-gray-900 font-semibold">
							{{ chartDetails.data.avg_completion_time?.seconds > 0 ?
								formatDuration(chartDetails.data.avg_completion_time.seconds) : '—' }}
						</div>
						<div class="text-sm text-gray-700">{{ __('Avg Completion Time') }}</div>
					</div>
				</div>
			</Tooltip>
		</div>
		<div class="grid grid-cols-1 lg:grid-cols-2 gap-4 mt-4">
			<div class="border rounded-xl min-h-72">
				<div>
					<div class="text-lg text-gray-900 font-medium px-5 py-3 border-b">
						{{ __('Daily Signups') }}</div>
				</div>
				<div class="px-5 py-3">
					<AreaChart v-if="signupsChart.data"
						:data="(signupsChart.data || []).map(e => ({ x: e.date, y: e.signups }))"
						:name="__('Signups')" />
				</div>
			</div>
			<div class="border rounded-xl min-h-72">
				<div>
					<div class="text-lg text-gray-900 font-medium px-5 py-3 border-b">
						{{ __('Daily Enrollments') }}</div>
				</div>
				<div class="px-5 py-3">
					<AreaChart v-if="enrollmentChart.data"
						:data="(enrollmentChart.data || []).map(e => ({ x: e.date, y: e.enrollments }))"
						:name="__('Enrollments')" />
				</div>
			</div>
			<div class="border rounded-xl">
				<div>
					<div class="text-lg text-gray-900 font-medium px-5 py-3 border-b">
						{{ __('Daily Certifications') }}</div>
				</div>
				<div class="px-5 py-3">
					<AreaChart v-if="certification.data"
						:data="(certification.data || []).map(e => ({ x: e.date, y: e.certifications }))"
						:name="__('Certifications')" />
				</div>
			</div>
			<div class="border rounded-xl">
				<div>
					<div class="text-lg text-gray-900 font-medium px-5 py-3 border-b">
						{{ __('Course Completions') }}</div>
				</div>
				<DonutChart v-if="courseCompletion.data" :data="courseCompletion.data" />
			</div>
			<div class="border rounded-xl min-h-72">
				<div>
					<div class="text-lg text-gray-900 font-medium px-5 py-3 border-b">
						{{ __('Avg Daily Learning Time per Student') }}</div>
				</div>
				<div class="px-5 py-3">
					<AreaChart v-if="learningTimeChart.data"
						:data="(learningTimeChart.data || []).map(e => ({ x: e.date, y: Math.round(e.count / 60) }))"
						:name="__('Avg Minutes')" />
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import {
	// AxisChart,
	createResource,
	// DonutChart,
	Tooltip,
} from 'frappe-ui'
import { ArrowUpIcon, ArrowDownIcon, Clock as ClockIcon } from 'lucide-vue-next'
import BookIcon from '@/components/Icons/BookIcon.vue'
import UserCircleAddIcon from '@/components/Icons/UserCircleAddIcon.vue'
import ClipboardIcon from "@/components/Icons/ClipboardIcon.vue"
import TickCircleIcon from '@/components/Icons/TickCircleIcon.vue'
import AwardIcon from '@/components/Icons/AwardIcon.vue'
import AreaChart from '@/components/AreaChart.vue'
import DonutChart from '@/components/DonutChart.vue'
import { formatDuration } from '@/utils'

const chartDetails = createResource({
	url: 'lms.lms.api.get_chart_details',
	cache: ['statistics'],
	auto: true,
})

const signupsChart = createResource({
	url: 'lms.lms.utils.get_chart_data',
	params: {
		chart_name: 'New Signups',
	},
	auto: true,
	transform(data) {
		return data.map((item) => {
			return {
				date: new Date(item.date),
				signups: item.count,
			}
		})
	},
})

const enrollmentChart = createResource({
	url: 'lms.lms.utils.get_chart_data',
	cache: ['enrollments'],
	params: {
		chart_name: 'Course Enrollments',
	},
	auto: true,
	transform(data) {
		return data.map((item) => {
			return {
				date: new Date(item.date),
				enrollments: item.count,
			}
		})
	},
})

const certification = createResource({
	url: 'lms.lms.api.get_certifications_chart_data',
	cache: ['certifications'],
	auto: true,
	transform(data) {
		return data.map((item) => {
			return {
				date: new Date(item.date),
				certifications: item.certifications,
			}
		})
	},
})

const courseCompletion = createResource({
	url: 'lms.lms.utils.get_course_completion_data',
	auto: true,
	cache: ['courseCompletion'],
})

const learningTimeChart = createResource({
	url: 'lms.lms.api.get_learning_time_chart_data',
	// cache: ['learningTime'],
	auto: true,
	transform(data) {
		return data.map((item) => {
			return {
				date: new Date(item.date),
				count: item.count,
			}
		})
	},
})
</script>