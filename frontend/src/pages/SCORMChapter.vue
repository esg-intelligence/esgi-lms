<template>
	<header
		class="sticky top-0 z-10 flex items-center justify-between bg-surface-white px-3 py-2.5 sm:px-5"
	>
		<CustomBreadcrumb
			v-if="breadcrumbs?.length"
			class="h-7"
			:items="breadcrumbs"
		/>
		<Button @click="sidebarMinimized = !sidebarMinimized">
			<template #icon>
				<PanelLeftClose v-if="!sidebarMinimized" class="w-4 h-4 stroke-1.5" />
				<PanelLeftOpen v-else class="w-4 h-4 stroke-1.5" />
			</template>
		</Button>
	</header>
	<ChatAssistant v-model="showAssistantModal" />
	<div :class="['h-screen grid', sidebarMinimized ? '' : 'md:grid-cols-[40%,60%]']">
		<div v-show="!sidebarMinimized" class="px-5 py-3 overflow-y-auto">
			<CourseSidebar
				:courseName="courseName"
				:courseTitle="chapter.doc?.course_title"
				:instructors="instructors.data || []"
				:modules="courseSummary.data?.modules || 0"
				:materials="courseSummary.data?.materials || 0"
				:lessonProgress="lessonProgress"
				:hasEnrollment="!!enrollment.data?.length"
				:hasPrev="!!neighbours.data?.prev"
				:hasNext="!!neighbours.data?.next"
				:isNextDisabled="false"
				:getProgress="!!enrollment.data?.length"
				@prev="switchChapter('prev')"
				@next="switchChapter('next')"
			/>
		</div>

		<div
			v-if="
				readyToRender &&
				(enrollment.data?.length ||
					user.data?.is_moderator ||
					user.data?.is_instructor)
			"
			class="overflow-hidden h-full"
		>
			<iframe
				:src="chapter.doc.launch_file"
				class="w-full h-full"
			/>
		</div>
		<div v-else-if="!enrollment.data?.length">
			<div class="text-center pt-10 px-5 md:px-0 pb-10">
				<div class="text-center">
					<div class="mb-4">
						{{
							__(
								'You are not enrolled in this course. Please enroll to access this lesson.',
							)
						}}
					</div>
					<Button variant="solid" @click="enrollStudent()">
						{{ __('Start Learning') }}
					</Button>
				</div>
			</div>
		</div>
	</div>
</template>
<script setup>
import {
	Button,
	call,
	createDocumentResource,
	createListResource,
	createResource,
	usePageMeta,
} from 'frappe-ui'
import { computed, inject, onBeforeMount, onBeforeUnmount, ref } from 'vue'
import { PanelLeftClose, PanelLeftOpen } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import { useSidebar } from '@/stores/sidebar'
import { sessionStore } from '../stores/session'
import ChatAssistant from '@/components/ChatAssistant.vue'
import CourseSidebar from '@/components/CourseSidebar.vue'
import CustomBreadcrumb from '@/components/ui/CustomBreadcrumb.vue'

const { brand } = sessionStore()
const sidebarStore = useSidebar()
const user = inject('$user')
const socket = inject('$socket')
const router = useRouter()
const readyToRender = ref(false)
const showAssistantModal = ref(true)
const isSuccessfullyCompleted = ref(false)
const lessonProgress = ref(0)
const sidebarMinimized = ref(false)

// If courseRestartOnFailure is true, student has to restart the whole course if failed.
// Otherwise, student could retake the final quiz portion.
// Ideally, this should be configurable along with `Number of failures before course should restart`.
const courseRestartOnFailure = false

const props = defineProps({
	courseName: {
		type: String,
		required: true,
	},
	chapterName: {
		type: String,
		required: true,
	},
})

onBeforeMount(() => {
	sidebarStore.isSidebarCollapsed = true
	progress.reload() // Fix reload scorm content after it was opened
	setupSCORMAPI()
	socket.on('update_lesson_progress', (data) => {
		if (data.course === props.courseName) {
			lessonProgress.value = data.progress
		}
	})
})

onBeforeUnmount(() => {
	sidebarStore.isSidebarCollapsed = false
})

const chapter = createDocumentResource({
	doctype: 'Course Chapter',
	name: props.chapterName,
	auto: true,
	cache: ['chapter', props.chapterName],
	onSuccess(data) {
		progress.submit()
	},
})

const instructors = createResource({
	url: 'lms.lms.utils.get_instructors',
	params: {
		doctype: 'LMS Course',
		docname: props.courseName,
	},
	auto: true,
})

const courseSummary = createResource({
	url: 'lms.lms.utils.get_course_outline_summary',
	params: {
		course: props.courseName,
	},
	auto: true,
})

const neighbours = createResource({
	url: 'lms.lms.utils.get_neighbour_chapter',
	makeParams() {
		return {
			course: props.courseName,
			chapter_name: props.chapterName,
		}
	},
	auto: true,
})

const enrollment = createListResource({
	doctype: 'LMS Enrollment',
	fields: ['member', 'course', 'progress'],
	filters: {
		course: props.courseName,
		member: user.data?.name,
	},
	auto: true,
	cache: ['enrollments', props.courseName, user.data?.name],
	onSuccess(data) {
		if (data.length) lessonProgress.value = data[0].progress || 0
	},
})

const getDataFromLMS = (key) => {
	if (key === 'cmi.core.lesson_status') {
		return progress.data?.status === 'Complete' ? 'passed' : 'incomplete'
	} else if (key === 'cmi.launch_data') {
		return progress.data?.scorm_content || ''
	} else if (key === 'cmi.suspend_data') {
		return progress.data?.scorm_content || ''
	}
	return ''
}

let saveTimeout = null
const debouncedSaveProgress = (scormDetails) => {
	clearTimeout(saveTimeout)
	saveTimeout = setTimeout(() => {
		saveProgress(scormDetails)
	}, 300)
}

const saveDataToLMS = (key, value) => {
	if (key === 'cmi.core.lesson_status') {
		if (value === 'passed') {
			isSuccessfullyCompleted.value = true
			saveProgress({
				is_complete: isSuccessfullyCompleted.value,
				scorm_content: '',
			})
		} else if (value === 'failed' && courseRestartOnFailure) {
			saveProgress({
				is_complete: isSuccessfullyCompleted.value,
				scorm_content: '',
			})
		}
	} else if (key === 'cmi.suspend_data' && !isSuccessfullyCompleted.value) {
		debouncedSaveProgress({
			is_complete: false,
			scorm_content: value,
		})
	}
}

const saveProgress = (scormDetails = null) => {
	call('lms.lms.doctype.course_lesson.course_lesson.save_progress', {
		lesson: chapter.doc.lessons[0].lesson,
		course: props.courseName,
		scorm_details: scormDetails,
	})
}

const progress = createResource({
	url: 'frappe.client.get_value',
	makeParams(values) {
		return {
			doctype: 'LMS Course Progress',
			fieldname: ['status', 'scorm_content'],
			filters: {
				member: user.data?.name,
				lesson: chapter.doc.lessons[0].lesson,
				chapter: chapter.doc.name,
				course: chapter.doc?.course,
			},
		}
	},
	onSuccess(data) {
		readyToRender.value = true
	},
})

const switchChapter = (direction) => {
	const target = neighbours.data?.[direction]
	if (!target) return
	if (target.is_scorm_package) {
		router.push({
			name: 'SCORMChapter',
			params: { courseName: props.courseName, chapterName: target.name },
		})
	} else {
		router.push({
			name: 'Lesson',
			params: {
				courseName: props.courseName,
				chapterNumber: target.idx,
				lessonNumber: 1,
			},
		})
	}
}

const enrollStudent = () => {
	enrollment.insert.submit(
		{
			course: props.courseName,
			member: user.data?.name,
		},
		{
			onSuccess(data) {
				window.location.reload()
			},
		},
	)
}

const setupSCORMAPI = () => {
	window.API_1484_11 = {
		Initialize: () => 'true',
		Terminate: () => 'true',
		GetValue: (key) => {
			console.log(`GET: ${key}`)
			return getDataFromLMS(key)
		},
		SetValue: (key, value) => {
			console.log(`SET: ${key} to value: ${value}`)

			saveDataToLMS(key, value)
			return 'true'
		},
		Commit: () => 'true',
		GetLastError: () => '0',
		GetErrorString: () => '',
		GetDiagnostic: () => '',
	}
	window.API = {
		LMSInitialize: () => 'true',
		LMSFinish: () => 'true',
		LMSGetValue: (key) => {
			console.log(`GET: ${key}`)
			return getDataFromLMS(key)
		},
		LMSSetValue: (key, value) => {
			console.log(`SET: ${key} to value: ${value}`)
			saveDataToLMS(key, value)
			return 'true'
		},
		LMSCommit: () => 'true',
		LMSGetLastError: () => '0',
		LMSGetErrorString: () => '',
		LMSGetDiagnostic: () => '',
	}
}

const breadcrumbs = computed(() => {
	return [
		{
			label: 'Courses',
			route: { name: 'Courses' },
		},
		{
			label: chapter.doc?.course_title,
			route: { name: 'CourseDetail', params: { courseName: props.courseName } },
		},
		{
			label: chapter.doc?.title,
			route: {
				name: 'SCORMChapter',
				params: {
					courseName: props.courseName,
					chapterName: props.chapterName,
				},
			},
		},
	]
})

usePageMeta(() => {
	return {
		title: chapter.doc?.title,
		icon: brand.favicon,
	}
})
</script>
