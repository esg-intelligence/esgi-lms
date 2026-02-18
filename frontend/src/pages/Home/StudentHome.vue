<template>
	<div>
		<div v-if="chartDetails.data" class="mt-10">
			<div class="grid grid-cols-1 lg:grid-cols-4 gap-4">
				<Tooltip :text="__('Courses in Enrolled')">
					<div class="border rounded-xl p-4 flex items-center gap-4">
						<div class="bg-primary-50 w-12 h-12 rounded-full flex items-center justify-center">
							<Book class="text-primary-500 w-6 h-6" />
						</div>
						<div class="flex-1">
							<div class="text-xl text-gray-900 font-semibold">{{ chartDetails.data.enrollments.count }}</div>
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
							<div class="text-xl text-gray-900 font-semibold">{{ chartDetails.data.in_progress.count }}</div>
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
							<div class="text-xl text-gray-900 font-semibold">{{ chartDetails.data.completions.count }}</div>
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
							<div class="text-xl text-gray-900 font-semibold">{{ chartDetails.data.certifications.count }}
							</div>
							<div class="text-sm text-gray-700">Certificates</div>
						</div>
					</div>
				</Tooltip>
			</div>
		</div>

		<div v-if="myCourses.data?.length" class="mt-10">
			<div class="flex items-center justify-between mb-8">
				<div>
					<div class="font-semibold text-lg text-ink-gray-9">
						{{__('Continue Learning')}}
					</div>
					<p class="text-base text-gray-600 leading-6">
						{{ __('Resume your courses and continue building your knowledge.') }}
					</p>
				</div>
				<router-link
					:to="{
						name: 'Courses',
					}"
				>
					<span
						class="flex items-center space-x-1 text-base font-medium"
						:class="
							myBatches.data?.length
								? 'text-primary-500 hover:text-primary-600'
								: 'text-gray-500'
						"
					>
						<span>
							{{ __('View all courses') }}
						</span>
					</span>
				</router-link>
			</div>
			<div
				class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5"
			>
				<router-link
					v-for="course in myCourses.data"
					:to="{ name: 'CourseDetail', params: { courseName: course.name } }"
				>
					<CourseCard :course="course" />
				</router-link>
			</div>
		</div>

		<div v-if="popularCourses.data?.length" class="mt-10">
			<div class="flex items-center justify-between mb-8">
				<div>
					<div class="font-semibold text-lg text-ink-gray-9">
						{{__('Our Popular Courses')}}
					</div>
					<p class="text-base text-gray-600 leading-6">
						{{ __('Explore the most popular courses chosen by learners to build essential ESG knowledge and skills.') }}
					</p>
				</div>
				<router-link
					:to="{
						name: 'Courses',
					}"
				>
					<span
						class="flex items-center space-x-1 text-base font-medium"
						:class="
							myBatches.data?.length
								? 'text-primary-500 hover:text-primary-600'
								: 'text-gray-500'
						"
					>
						<span>
							{{ __('View all courses') }}
						</span>
					</span>
				</router-link>
			</div>
			<div
				class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5"
			>
				<router-link
					v-for="course in myCourses.data"
					:to="{ name: 'CourseDetail', params: { courseName: course.name } }"
				>
					<CourseCard :course="course" />
				</router-link>
			</div>
		</div>

		<div v-if="myBatches.data?.length" class="mt-10">
			<div class="flex items-center justify-between mb-3">
				<span class="font-semibold text-lg text-ink-gray-9">
					{{
						myBatches.data?.[0].students.includes(user.data?.name)
							? __('My Batches')
							: __('Our Upcoming Batches')
					}}
				</span>
				<router-link
					:to="{
						name: 'Batches',
					}"
				>
					<span
						class="flex items-center space-x-1 text-primary-500 hover:text-primary-600 text-base font-medium"
					>
						<span>
							{{ __('View all batch') }}
						</span>
					</span>
				</router-link>
			</div>
			<div
				class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5"
			>
				<router-link
					v-for="batch in myBatches.data"
					:to="{ name: 'BatchDetail', params: { batchName: batch.name } }"
				>
					<BatchCard :batch="batch" />
				</router-link>
			</div>
		</div>

		<div class="grid grid-cols-1 md:grid-cols-2 gap-10 md:gap-5 mt-10">
			<UpcomingEvaluations :forHome="true" />
			<div v-if="myLiveClasses.data?.length">
				<div class="font-semibold text-lg mb-3 text-ink-gray-9">
					{{ __('Upcoming Live Classes') }}
				</div>
				<div class="grid grid-cols-1 md:grid-cols-2 gap-5">
					<div
						v-for="cls in myLiveClasses.data"
						class="border rounded-md hover:border-outline-gray-3 p-2"
					>
						<div class="font-semibold text-ink-gray-9 text-lg leading-5 mb-1">
							{{ cls.title }}
						</div>
						<div class="text-ink-gray-7 text-sm leading-5 mb-4">
							{{ cls.description }}
						</div>
						<div class="mt-auto space-y-3 text-ink-gray-7 text-sm">
							<div class="flex items-center space-x-2">
								<Calendar class="w-4 h-4 stroke-1.5" />
								<span>
									{{ dayjs(cls.date).format('DD MMMM YYYY') }}
								</span>
							</div>
							<div class="flex items-center space-x-2">
								<Clock class="w-4 h-4 stroke-1.5" />
								<span>
									{{ formatTime(cls.time) }} -
									{{ dayjs(getClassEnd(cls)).format('HH:mm A') }}
								</span>
							</div>
							<div
								v-if="canAccessClass(cls)"
								class="flex items-center space-x-2 text-ink-gray-9 mt-auto"
							>
								<a
									v-if="user.data?.is_moderator || user.data?.is_evaluator"
									:href="cls.start_url"
									target="_blank"
									class="cursor-pointer inline-flex items-center justify-center gap-2 transition-colors focus:outline-none text-ink-gray-8 bg-surface-gray-2 hover:bg-surface-gray-3 active:bg-surface-gray-4 focus-visible:ring focus-visible:ring-outline-gray-3 h-7 text-base px-2 rounded"
									:class="cls.join_url ? 'w-full' : 'w-1/2'"
								>
									<Monitor class="h-4 w-4 stroke-1.5" />
									{{ __('Start') }}
								</a>
								<a
									:href="cls.join_url"
									target="_blank"
									class="w-full cursor-pointer inline-flex items-center justify-center gap-2 transition-colors focus:outline-none text-ink-gray-8 bg-surface-gray-2 hover:bg-surface-gray-3 active:bg-surface-gray-4 focus-visible:ring focus-visible:ring-outline-gray-3 h-7 text-base px-2 rounded"
								>
									<Video class="h-4 w-4 stroke-1.5" />
									{{ __('Join') }}
								</a>
							</div>
							<Tooltip
								v-else-if="hasClassEnded(cls)"
								:text="__('This class has ended')"
								placement="right"
							>
								<div class="flex items-center space-x-2 text-ink-amber-3 w-fit">
									<Info class="w-4 h-4 stroke-1.5" />
									<span>
										{{ __('Ended') }}
									</span>
								</div>
							</Tooltip>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>
<script setup lang="ts">
import { inject } from 'vue'
import { createResource, Tooltip } from 'frappe-ui'
import { formatTime } from '@/utils'
import {
	Book,
	Calendar,
	Clock,
	Info,
	Monitor,
	Video,
} from 'lucide-vue-next'
import CourseCard from '@/components/CourseCard.vue'
import BatchCard from '@/components/BatchCard.vue'
import UpcomingEvaluations from '@/components/UpcomingEvaluations.vue'

const dayjs = inject<any>('$dayjs')
const user = inject<any>('$user')

const props = defineProps<{
	myLiveClasses: any
}>()

const myCourses = createResource({
	url: 'lms.lms.utils.get_my_courses',
	auto: true,
})

const popularCourses = createResource({
	url: 'lms.lms.utils.get_popular_courses_detail',
	auto: true,
})

const myBatches = createResource({
	url: 'lms.lms.utils.get_my_batches',
	auto: true,
})

const chartDetails = createResource({
	url: 'lms.lms.api.get_user_chart_details',
	auto: true,
})

const getClassEnd = (cls: { date: string; time: string; duration: number }) => {
	const classStart = new Date(`${cls.date}T${cls.time}`)
	return new Date(classStart.getTime() + cls.duration * 60000)
}

const canAccessClass = (cls: {
	date: string
	time: string
	duration: number
}) => {
	if (cls.date < dayjs().format('YYYY-MM-DD')) return false
	if (cls.date > dayjs().format('YYYY-MM-DD')) return false
	if (hasClassEnded(cls)) return false
	return true
}

const hasClassEnded = (cls: {
	date: string
	time: string
	duration: number
}) => {
	const classEnd = getClassEnd(cls)
	const now = new Date()
	return now > classEnd
}
</script>
