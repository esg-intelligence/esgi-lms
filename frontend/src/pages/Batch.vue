<template>
	<div v-if="isAdmin || isStudent" class="">
		<header
			class="sticky top-0 z-10 flex items-center justify-between bg-surface-white px-3 py-2.5 sm:px-5"
		>
			<CustomBreadcrumb class="h-7" :items="breadcrumbs" />
			<div class="flex items-center space-x-2">
				<Button
					v-if="isAdmin && batch.data?.certification"
					@click="openCertificateDialog = true"
				>
					{{ __('Generate Certificates') }}
				</Button>
				<Button
					v-if="canMakeAnnouncement()"
					@click="openAnnouncementModal()"
					variant="solid"
					class="!bg-primary-500"
				>
					<span>
						{{ __('Make an Announcement') }}
					</span>
					<template #suffix>
						<SendIcon class="h-4 stroke-1.5" />
					</template>
				</Button>
			</div>
		</header>
		<div class="px-5 py-4" v-if="batch.data">
			<div class="bg-white rounded-xl border mb-6 p-4 flex">
				<div class="flex items-center w-full pr-4">
					<div class="flex-1 px-3 py-3 flex flex-col gap-y-2 justify-center">
						<div class="h-fit">
							<h1 class="text-lg leading-5 font-semibold mb-1 text-gray-900">
								{{ batch.data.title }}
							</h1>
							<p class="short-introduction text-sm text-gray-600 !mb-0">
								{{ batch.data.description }}
							</p>
						</div>
						<div class="w-full flex gap-x-0">
							<div
								v-if="batch.data.seat_count && seats_left > 0"
								class="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-md"
							>
								{{ seats_left }}
								<span v-if="seats_left > 1">
									{{ __('Seats Left') }}
								</span>
								<span v-else-if="seats_left == 1">
									{{ __('Seat Left') }}
								</span>
							</div>
							<div
								v-else-if="batch.data.seat_count && seats_left <= 0"
								class="text-xs bg-red-100 text-red-700 px-2 py-0.5 rounded-md"
							>
								{{ __('Sold Out') }}
							</div>
							<div
								v-if="batch.data.amount"
								class="text-lg font-semibold mb-3 text-ink-gray-9"
							>
								{{
									formatNumberIntoCurrency(
										batch.data.amount,
										batch.data.currency,
									)
								}}
							</div>
						</div>

						<div
							class="w-full flex flex-col md:flex-row md:items-center gap-x-2 text-sm flex-wrap"
						>
							<div class="flex-1 flex items-center space-x-2 md:flex-nowrap">
								<DateRange
									:startDate="batch.data.start_date"
									:endDate="batch.data.end_date"
									class="whitespace-nowrap"
								/>
								<span
									class="text-gray-600 whitespace-nowrap"
									v-if="batch.data.medium"
									>{{ `• ${batch.data.medium}` }}</span
								>
							</div>
							<div class="flex-1 flex items-center text-gray-600">
								<ClockIcon class="h-4 w-4 stroke-1.5 mr-2 !text-gray-900" />
								<span class="text-gray-600 whitespace-nowrap">
									{{ formatTime(batch.data.start_time) }} -
									{{ formatTime(batch.data.end_time) }}
								</span>
								<div v-if="batch.data.timezone" class="flex items-center">
									<Globe class="h-4 w-4 stroke-1.5 mx-2 text-gray-900" />
									<span>
										{{ batch.data.timezone }}
									</span>
								</div>
							</div>
						</div>
					</div>

					<Button
						v-if="isStudent"
						variant="outline"
						@click="showFeedbackModal = true"
					>
						{{ __('Give Feedback') }}
					</Button>
				</div>
			</div>
			<div class="grid grid-cols-1 min-h-[calc(100vh-3.2rem)]">
				<div class="w-full overflow-x-hidden">
					<div class="border-b mb-6">
						<nav
							class="w-full flex space-x-8 overflow-x-hidden hover:overflow-x-auto mininal-scrollbar"
						>
							<button
								v-for="tab in tabs"
								:key="tab.value"
								@click="currentTab = tab.label"
								:class="[
									'pb-2 text-center px-2 border-b-[2px] font-medium transition-colors min-w-40',
									currentTab === tab.label
										? 'border-secondary-500 text-gray-900'
										: 'border-transparent text-ink-gray-5 hover:text-ink-gray-7',
								]"
							>
								{{ __(tab.label) }}
							</button>
						</nav>
					</div>
					<div class="pt-5 px-5">
						<div v-if="currentTab == 'Courses'">
							<BatchCourses :batch="batch.data.name" />
						</div>
						<div v-else-if="currentTab == 'Dashboard' && isStudent">
							<BatchDashboard :batch="batch" :isStudent="isStudent" />
						</div>
						<div v-else-if="currentTab == 'Dashboard'">
							<AdminBatchDashboard :batch="batch" />
						</div>
						<div v-else-if="currentTab == 'Students'">
							<BatchStudents :batch="batch" />
						</div>
						<div v-else-if="currentTab == 'Classes'">
							<LiveClass
								:batch="batch.data.name"
								:zoomAccount="batch.data.zoom_account"
							/>
						</div>
						<div v-else-if="currentTab == 'Assessments'">
							<Assessments :batch="batch.data.name" />
						</div>
						<div v-else-if="currentTab == 'Announcements'">
							<Announcements :batch="batch.data.name" />
						</div>
						<div v-else-if="currentTab == 'Discussions'">
							<Discussions
								doctype="LMS Batch"
								:docname="batch.data.name"
								:title="__('Discussions')"
								:key="batch.data.name"
								:singleThread="true"
								:scrollToBottom="false"
							/>
						</div>
						<div v-else-if="currentTab == 'Feedback'">
							<BatchFeedbackNew :batch="batch.data.name" />
						</div>
					</div>
					<!-- <Tabs
						v-model="tabIndex"
						as="div"
						:tabs="tabs"
						tablistClass="bg-surface-white"
						:class="[
							'[&_[data-state=active]]:text-primary-500',
							'[&>div:first-child>div:first-child>div:first-child]:!bg-primary-500',
							'[&>div:first-child>div:first-child>div:first-child]:!h-[2px]',
							'[&_[data-reka-collection-item]]:px-8 [&_[data-reka-collection-item]>svg]:hidden ',
						]"
					>
						<template #tab="{ tab, selected }" class="overflow-x-hidden">
							<div class="font-medium">
								<button
									class="group -mb-px flex items-center gap-1 border-b border-transparent py-2.5 text-base text-ink-gray-5 duration-300 ease-in-out hover:border-outline-gray-3 hover:text-ink-gray-9"
									:class="{ 'text-ink-gray-9': selected }"
								>
									<component
										v-if="tab.icon"
										:is="tab.icon"
										class="h-4 stroke-1.5"
									/>
									{{ __(tab.label) }}
									<Badge
										v-if="tab.count"
										:class="{
											'text-ink-gray-9 border border-gray-900': selected,
										}"
										variant="subtle"
										theme="gray"
										size="sm"
									>
										{{ tab.count }}
									</Badge>
								</button>
							</div>
						</template>
						<template #tab-panel="{ tab }"> </template>
					</Tabs> -->
				</div>
				<!-- <div class="p-5 border-t md:border-t-0">
				<div class="mb-10">
					<div class="text-ink-gray-7 font-semibold mb-2">
						{{ __('About this batch') }}
					</div>
					<div
						v-html="batch.data.description"
						class="leading-5 mb-4 text-ink-gray-7"
					></div>

					<div class="flex items-center avatar-group overlap mb-5">
						<div
							class="h-6 mr-1"
							:class="{
								'avatar-group overlap': batch.data.instructors.length > 1,
							}"
						>
							<UserAvatar
								v-for="instructor in batch.data.instructors"
								:user="instructor"
							/>
						</div>
						<CourseInstructors :instructors="batch.data.instructors" />
					</div>
					<DateRange
						:startDate="batch.data.start_date"
						:endDate="batch.data.end_date"
						class="mb-3"
					/>
					<div class="flex items-center mb-3 text-ink-gray-7">
						<Clock class="h-4 w-4 stroke-1.5 mr-2" />
						<span>
							{{ formatTime(batch.data.start_time) }} -
							{{ formatTime(batch.data.end_time) }}
						</span>
					</div>
					<div
						v-if="batch.data.timezone"
						class="flex items-center mb-3 text-ink-gray-7"
					>
						<Globe class="h-4 w-4 stroke-1.5 mr-2" />
						<span>
							{{ batch.data.timezone }}
						</span>
					</div>
				</div>
				<div v-if="dayjs().isSameOrAfter(dayjs(batch.data.start_date))">
					<div class="text-ink-gray-7 font-semibold mb-2">
						{{ __('Feedback') }}
					</div>
					<BatchFeedback :batch="batch.data?.name" />
				</div>
			</div> -->
				<AnnouncementModal
					v-model="showAnnouncementModal"
					:batch="batch.data.name"
					:students="batch.data.students"
				/>
			</div>
		</div>
	</div>
	<div v-else-if="!user.data?.name" class="">
		<div class="text-base border rounded-md w-1/3 mx-auto my-32">
			<div class="border-b px-5 py-3 font-medium">
				<span
					class="inline-flex items-center before:bg-surface-red-5 before:w-2 before:h-2 before:rounded-md before:mr-2"
				></span>
				{{ __('Not Permitted') }}
			</div>
			<div class="px-5 py-3">
				<div v-if="user.data" class="mb-4 leading-6">
					{{
						__(
							'You are not a member of this batch. Please checkout our upcoming batches.',
						)
					}}
				</div>
				<div v-else class="mb-4 leading-6">
					{{ __('Please login to access this page.') }}
				</div>
				<router-link
					v-if="user.data"
					:to="{
						name: 'Batches',
						params: {
							batchName: batch.data?.name,
						},
					}"
				>
					<Button variant="solid" class="w-full">
						{{ __('Upcoming Batches') }}
					</Button>
				</router-link>
				<Button
					v-else
					variant="solid"
					class="w-full"
					@click="redirectToLogin()"
				>
					{{ __('Login') }}
				</Button>
			</div>
		</div>
	</div>
	<BulkCertificates
		v-if="batch.data"
		v-model="openCertificateDialog"
		:batch="batch.data"
	/>
	<FeedbackSubmissionModal
		v-if="batch.data"
		v-model="showFeedbackModal"
		:batch="batch.data.name"
	/>
</template>
<script setup>
import { computed, inject, ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { createResource, Tabs, Badge, usePageMeta } from 'frappe-ui'
import {
	Clock,
	LayoutDashboard,
	BookOpen,
	Laptop,
	BookOpenCheck,
	Mail,
	SendIcon,
	MessageCircle,
	Globe,
	ClipboardPen,
	MessageSquareText,
} from 'lucide-vue-next'
import { formatTime } from '@/utils'
import { sessionStore } from '@/stores/session'
import CourseInstructors from '@/components/CourseInstructors.vue'
import UserAvatar from '@/components/UserAvatar.vue'
import BatchDashboard from '@/components/BatchDashboard.vue'
import BatchCourses from '@/components/BatchCourses.vue'
import LiveClass from '@/components/LiveClass.vue'
import BatchStudents from '@/components/BatchStudents.vue'
import AdminBatchDashboard from '@/components/AdminBatchDashboard.vue'
import Assessments from '@/components/Assessments.vue'
import Announcements from '@/components/Annoucements.vue'
import AnnouncementModal from '@/components/Modals/AnnouncementModal.vue'
import Discussions from '@/components/Discussions.vue'
import DateRange from '@/components/Common/DateRange.vue'
import BulkCertificates from '@/components/Modals/BulkCertificates.vue'
import BatchFeedbackNew from '@/components/BatchFeedbackNew.vue'
import FeedbackSubmissionModal from '@/components/Modals/FeedbackSubmissionModal.vue'
import dayjs from 'dayjs/esm'
import CustomBreadcrumb from '@/components/ui/CustomBreadcrumb.vue'
import Button from '@/components/ui/Button.vue'
import ClockIcon from '@/components/Icons/ClockIcon.vue'

const user = inject('$user')
const showAnnouncementModal = ref(false)
const showFeedbackModal = ref(false)
const openCertificateDialog = ref(false)
const route = useRoute()
const router = useRouter()
const { brand } = sessionStore()
const readOnlyMode = window.read_only_mode
const currentTab = ref('Dashboard')
const tabs = computed(() => {
	let batchTabs = []
	batchTabs.push({
		label: 'Dashboard',
		icon: LayoutDashboard,
	})

	if (isAdmin.value) {
		batchTabs.push({
			label: 'Students',
			icon: ClipboardPen,
		})
	}

	batchTabs.push({
		label: 'Courses',
		icon: BookOpen,
	})

	batchTabs.push({
		label: 'Classes',
		icon: Laptop,
	})

	if (isAdmin.value) {
		batchTabs.push({
			label: 'Assessments',
			icon: BookOpenCheck,
		})
	}

	batchTabs.push({
		label: 'Announcements',
		icon: Mail,
	})

	batchTabs.push({
		label: 'Discussions',
		icon: MessageCircle,
	})

	if (isAdmin.value) {
		batchTabs.push({
			label: 'Feedback',
			icon: MessageSquareText,
		})
	}

	return batchTabs
})

const props = defineProps({
	batchName: {
		type: String,
		required: true,
	},
})

onMounted(() => {
	const hash = route.hash
	if (hash) {
		tabs.value.forEach((tab, index) => {
			if (tab.label?.toLowerCase() === hash.replace('#', '')) {
				currentTab.value = tab.label
			}
		})
	}
})

const batch = createResource({
	url: 'lms.lms.utils.get_batch_details',
	cache: ['batch', props.batchName],
	params: {
		batch: props.batchName,
	},
	auto: true,
})

const breadcrumbs = computed(() => {
	let crumbs = [{ label: __('Batches'), route: { name: 'Batches' } }]
	if (!isStudent.value) {
		crumbs.push({
			label: __('Details'),
			route: {
				name: 'BatchDetail',
				params: {
					batchName: batch.data?.name,
				},
			},
		})
	}
	crumbs.push({
		label: batch?.data?.title,
		route: { name: 'Batch', params: { batchName: props.batchName } },
	})
	return crumbs
})

const isStudent = computed(() => {
	return (
		user?.data &&
		batch.data?.students?.length &&
		batch.data?.students.includes(user.data.name)
	)
})

const redirectToLogin = () => {
	window.location.href = `/login?redirect-to=/lms/batches/${props.batchName}`
}

const openAnnouncementModal = () => {
	showAnnouncementModal.value = true
}

watch(currentTab, () => {
	if (currentTab.value != route.hash.replace('#', '')) {
		router.push({ ...route, hash: `#${currentTab.value.toLowerCase()}` })
	}
})

const canMakeAnnouncement = () => {
	if (readOnlyMode) return false

	if (!batch.data?.students?.length) return false

	return user.data?.is_moderator || user.data?.is_evaluator
}

const isAdmin = computed(() => {
	return user.data?.is_moderator || user.data?.is_evaluator
})

usePageMeta(() => {
	return {
		title: batch?.data?.title,
		icon: brand.favicon,
	}
})
</script>
