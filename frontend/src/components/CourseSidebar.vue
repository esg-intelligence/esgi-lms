<template>
	<div
		class="md:sticky md:top-14 bg-white space-y-3 rounded-xl w-full border border-gray-100 shadow-xl shadow-gray-100 p-5"
	>
		<h1 class="text-lg font-semibold text-ink-gray-9 mb-2">
			{{ courseTitle }}
		</h1>

		<div v-if="instructors.length" class="flex items-center">
			<span
				class="h-6 mr-1"
				:class="{ 'avatar-group overlap': instructors.length > 1 }"
			>
				<UserAvatar
					v-for="instructor in instructors"
					:key="instructor.name"
					:user="instructor"
				/>
			</span>
			<CourseInstructors :instructors="instructors" />
		</div>

		<div class="flex flex-col text-sm text-ink-gray-5 mb-4">
			<span class="flex items-center gap-x-2">
				<FolderIcon class="h-4 w-4 text-primary-500" />
				{{ modules }} Module
			</span>
			<span class="flex items-center gap-x-2">
				<DocumentTextIcon class="h-4 w-4 text-primary-500" />
				{{ materials }} Materials
			</span>
		</div>

		<div v-if="hasEnrollment" class="text-sm mt-4 mb-2 text-ink-gray-5">
			{{ Math.ceil(lessonProgress) }}% {{ __('completed') }}
		</div>
		<ProgressBar v-if="hasEnrollment" :progress="lessonProgress" />

		<div
			class="w-full h-fit [&_.title-outline]:hide [&_.title-chapter]:!text-sm [&_.title-chapter]:!font-medium"
		>
			<CourseOutline
				:key="outlineKey"
				:courseName="courseName"
				:getProgress="getProgress"
				:lessonProgress="lessonProgress"
			/>
		</div>

		<div class="space-y-2 !mt-10">
			<div class="flex items-center gap-x-2 justify-between">
				<Button v-if="hasPrev" @click="$emit('prev')" variant="outline">
					<template #prefix>
						<ChevronLeft class="w-4 h-4 stroke-1" />
					</template>
					{{ __('Previous') }}
				</Button>

				<Button
					v-if="hasNext"
					@click="$emit('next')"
					variant="solid"
					:disabled="isNextDisabled"
					:class="{ 'opacity-50 cursor-not-allowed': isNextDisabled }"
				>
					{{ __('Next') }}
					<template #suffix>
						<ChevronRight class="w-4 h-4 stroke-1" />
					</template>
				</Button>

				<router-link
					v-else
					:to="{ name: 'CourseDetail', params: { courseName } }"
					class="ml-auto"
				>
					<Button variant="solid" class="ml-2">
						{{ __('Back to Course') }}
					</Button>
				</router-link>
			</div>
		</div>
	</div>
</template>
<script setup>
import { ChevronLeft, ChevronRight } from 'lucide-vue-next'
import CourseInstructors from '@/components/CourseInstructors.vue'
import CourseOutline from '@/components/CourseOutline.vue'
import DocumentTextIcon from '@/components/Icons/DocumentTextIcon.vue'
import FolderIcon from '@/components/Icons/FolderIcon.vue'
import ProgressBar from '@/components/ProgressBar.vue'
import UserAvatar from '@/components/UserAvatar.vue'
import Button from '@/components/ui/Button.vue'

defineProps({
	courseName: {
		type: String,
		required: true,
	},
	courseTitle: {
		type: String,
		default: '',
	},
	instructors: {
		type: Array,
		default: () => [],
	},
	modules: {
		type: Number,
		default: 0,
	},
	materials: {
		type: Number,
		default: 0,
	},
	lessonProgress: {
		type: Number,
		default: 0,
	},
	hasEnrollment: {
		type: Boolean,
		default: false,
	},
	hasPrev: {
		type: Boolean,
		default: false,
	},
	hasNext: {
		type: Boolean,
		default: false,
	},
	isNextDisabled: {
		type: Boolean,
		default: false,
	},
	outlineKey: {
		type: [String, Number],
		default: '',
	},
	getProgress: {
		type: Boolean,
		default: false,
	},
})

defineEmits(['prev', 'next'])
</script>
