<template>
	<div v-if="!$user.data?.is_moderator && !$user.data?.is_instructor" class="flex items-center justify-center min-h-screen">
		<p class="text-gray-500">{{ __('You do not have permission to view this page.') }}</p>
	</div>

	<div v-else-if="userProgress.loading" class="flex items-center justify-center min-h-screen">
		<LoadingIndicator class="h-6 w-6 text-gray-400" />
	</div>

	<div v-else-if="userProgress.data" class="min-h-screen bg-gray-50 pb-12">
		<!-- Header -->
		<div class="bg-white border-b border-gray-100">
			<div class="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8 py-4">
				<button
					@click="$router.back()"
					class="flex items-center gap-1.5 text-sm text-gray-500 hover:text-gray-900 transition-colors mb-4"
				>
					<ArrowLeft class="h-4 w-4" />
					{{ __('Back') }}
				</button>
				<div class="flex items-center gap-3">
					<Avatar
						:label="userProgress.data.user.full_name"
						:image="userProgress.data.user.user_image"
						size="lg"
						class="rounded-full border border-gray-200 flex-shrink-0"
					/>
					<div>
						<h1 class="text-xl font-bold text-gray-900">
							{{ userProgress.data.user.full_name }}
						</h1>
						<p class="text-sm text-gray-500">@{{ userProgress.data.user.username }}</p>
					</div>
				</div>
			</div>
		</div>

		<!-- Course list -->
		<div class="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8 mt-6 space-y-4">
			<p v-if="!userProgress.data.enrollments.length" class="text-center text-gray-500 py-12">
				{{ __('No course enrollments found.') }}
			</p>

			<template v-else>
				<!-- Controls bar: search + rows per page -->
				<div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
					<FormControl
						v-model="searchTerm"
						type="text"
						:placeholder="__('Search by course name')"
						class="sm:max-w-xs"
					/>
					<div class="flex items-center gap-2 text-sm text-gray-500 self-end sm:self-auto">
						<span>{{ __('Rows per page:') }}</span>
						<FormControl
							v-model="pageLength"
							type="select"
							:options="pageLengthOptions"
							class="w-20"
						/>
					</div>
				</div>

				<div
					v-for="enrollment in userProgress.data.enrollments"
					:key="enrollment.course"
					class="bg-white rounded-xl border border-gray-100 overflow-hidden"
				>
					<!-- Course header -->
					<div class="p-5">
						<div class="flex items-start justify-between gap-4">
							<h2 class="text-base font-semibold text-gray-900 leading-snug">
								{{ enrollment.course_title }}
							</h2>
							<span class="flex-shrink-0 text-sm font-medium text-gray-700">
								{{ enrollment.progress || 0 }}%
							</span>
						</div>

						<!-- Progress bar -->
						<div class="mt-2 h-2 w-full rounded-full bg-gray-100 overflow-hidden">
							<div
								class="h-full rounded-full bg-[#00C49F] transition-all"
								:style="{ width: `${enrollment.progress || 0}%` }"
							/>
						</div>

						<div class="mt-3 flex flex-wrap gap-x-5 gap-y-1 text-xs text-gray-500">
							<span>
								{{ __('Time Spent') }}:
								{{ (enrollment.total_time_spent || 0) > 0 ? formatDuration(enrollment.total_time_spent) : '—' }}
							</span>
							<span v-if="enrollment.current_lesson">
								{{ __('Current Lesson') }}: {{ enrollment.current_lesson }}
							</span>
						</div>

						<button
							class="mt-3 flex items-center gap-1 text-xs font-medium text-[#00C49F] hover:text-[#00a082] transition-colors"
							@click="toggleCourse(enrollment.course)"
						>
							<ChevronDown
								class="h-3.5 w-3.5 transition-transform"
								:class="{ 'rotate-180': expandedCourses.has(enrollment.course) }"
							/>
							{{ expandedCourses.has(enrollment.course) ? __('Hide lessons') : __('Show lessons') }}
						</button>
					</div>

					<!-- Chapter / lesson tree -->
					<div v-if="expandedCourses.has(enrollment.course)" class="border-t border-gray-100 divide-y divide-gray-50">
						<div
							v-for="chapter in enrollment.chapters"
							:key="chapter.chapter"
							class="px-5 py-3"
						>
							<p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">
								{{ chapter.title }}
							</p>
							<ul class="space-y-1.5">
								<li
									v-for="lesson in chapter.lessons"
									:key="lesson.lesson"
									class="flex items-center justify-between gap-3 text-sm"
								>
									<span class="text-gray-700 truncate">{{ lesson.title }}</span>
									<span
										class="flex-shrink-0 flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-medium"
										:class="{
											'bg-green-50 text-green-700': lesson.status === 'Complete',
											'bg-amber-50 text-amber-700': lesson.status === 'Partially Complete',
											'bg-gray-100 text-gray-500': lesson.status === 'Not Started',
										}"
									>
										<CheckCircle v-if="lesson.status === 'Complete'" class="h-3 w-3" />
										<Clock v-else-if="lesson.status === 'Partially Complete'" class="h-3 w-3" />
										<Circle v-else class="h-3 w-3" />
										{{ __(lesson.status) }}
									</span>
								</li>
							</ul>
						</div>
						<div v-if="!enrollment.chapters.length" class="px-5 py-3 text-xs text-gray-400">
							{{ __('No chapters found.') }}
						</div>
					</div>
				</div>

				<!-- Pagination bar -->
				<div class="flex items-center justify-between pt-2 text-sm text-gray-500">
					<span v-if="totalCount">
						{{ __('Showing {0}–{1} of {2}').format(showingFrom, showingTo, totalCount) }}
					</span>
					<span v-else></span>
					<div class="flex items-center gap-2">
						<Button variant="outline" :disabled="currentPage === 1" @click="prevPage">
							{{ __('Previous') }}
						</Button>
						<span>{{ __('Page {0} of {1}').format(currentPage, totalPages) }}</span>
						<Button variant="outline" :disabled="currentPage >= totalPages" @click="nextPage">
							{{ __('Next') }}
						</Button>
					</div>
				</div>
			</template>
		</div>
	</div>
</template>

<script setup>
import { createResource, Avatar, LoadingIndicator, Button, FormControl } from 'frappe-ui'
import { ref, computed, inject, onMounted, watch } from 'vue'
import { watchDebounced } from '@vueuse/core'
import { ArrowLeft, ChevronDown, CheckCircle, Clock, Circle } from 'lucide-vue-next'
import { formatDuration } from '@/utils'

const props = defineProps({ username: String })
const $user = inject('$user')

const searchTerm = ref('')
const pageLength = ref(10)
const currentPage = ref(1)

const totalCount = computed(() => userProgress.data?.total ?? 0)
const totalPages = computed(() => Math.ceil(totalCount.value / pageLength.value) || 1)
const start = computed(() => (currentPage.value - 1) * pageLength.value)
const showingFrom = computed(() => Math.min(start.value + 1, totalCount.value))
const showingTo = computed(() => Math.min(start.value + parseInt(pageLength.value), totalCount.value))

const userProgress = createResource({
	url: 'lms.lms.api.get_user_course_progress',
	makeParams: () => ({
		username: props.username,
		start: start.value,
		page_length: pageLength.value,
		search: searchTerm.value,
	}),
})

const expandedCourses = ref(new Set())

const reload = () => {
	expandedCourses.value = new Set()
	userProgress.submit()
}

onMounted(reload)

watch(pageLength, () => {
	currentPage.value = 1
	reload()
})

watch(currentPage, reload)

watchDebounced(searchTerm, () => {
	currentPage.value = 1
	reload()
}, { debounce: 300 })

const toggleCourse = (course) => {
	const next = new Set(expandedCourses.value)
	if (next.has(course)) next.delete(course)
	else next.add(course)
	expandedCourses.value = next
}

const prevPage = () => {
	if (currentPage.value > 1) currentPage.value--
}

const nextPage = () => {
	if (currentPage.value < totalPages.value) currentPage.value++
}

const pageLengthOptions = [
	{ label: '5', value: 5 },
	{ label: '10', value: 10 },
	{ label: '20', value: 20 },
]
</script>
