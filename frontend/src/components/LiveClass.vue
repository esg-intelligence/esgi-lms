<template>
	<div
		v-if="hasPermission() && !props.zoomAccount"
		class="flex items-center space-x-2 mb-5 bg-surface-amber-1 py-1 px-2 rounded-md text-ink-amber-3 text-xs"
	>
		<AlertCircle class="size-4 stroke-1.5" />
		<span>
			{{ __('Please add a zoom account to the batch to create live classes.') }}
		</span>
	</div>

	<div class="flex items-center justify-between">
		<div class="text-xl font-semibold text-ink-gray-9">
			{{ __('Live Class') }}
		</div>
		<Button v-if="canCreateClass()" @click="openLiveClassModal">
			<template #prefix>
				<Plus class="h-4 w-4" />
			</template>
			<span>
				{{ __('Add') }}
			</span>
		</Button>
	</div>
	<div v-if="liveClasses.data?.length" class="grid grid-cols-1 gap-5 mt-5">
		<div
			v-for="cls in liveClasses.data"
			class="flex flex-col border border-gray-100 rounded-md h-full text-ink-gray-7 hover:border-outline-gray-3 p-3"
			:class="{
				'cursor-pointer': hasPermission() && cls.attendees > 0,
			}"
			@click="
				() => {
					openAttendanceModal(cls)
				}
			"
		>
			<div class="flex items-center gap-2 mb-1">
				<div class="font-semibold text-ink-gray-9 text-base">
					{{ cls.title }}
				</div>
				<div
					v-if="canAccessClass(cls) && !hasClassEnded(cls)"
					class="flex items-center space-x-1 px-2 py-0.5 bg-red-100 text-red-600 rounded-sm text-[10px] font-bold uppercase tracking-wider animate-pulse"
				>
					<span class="size-1 bg-red-600 rounded-full"></span>
					<span>Live</span>
				</div>
				<Tooltip
					v-else-if="hasClassEnded(cls)"
					:text="__('This class has ended')"
					placement="top"
				>
					<div
						class="flex items-center px-2 py-0.5 bg-surface-amber-1 text-ink-amber-3 rounded-sm text-[10px] font-bold uppercase tracking-wider"
					>
						<span>Ended</span>
					</div>
				</Tooltip>
			</div>
			<div class="mt-auto space-y-2 text-sm">
				<div class="flex items-center space-x-2">
					<Calendar2Icon class="w-4 h-4 stroke-1.5" />
					<span class="text-gray-600">
						{{ dayjs(cls.date).format('DD MMM YYYY') }} • {{ __('Online') }}
					</span>
				</div>
				<div class="flex items-center space-x-2">
					<ClockIcon class="w-4 h-4 stroke-1.5" />
					<span class="text-gray-600">
						{{ dayjs(getClassStart(cls)).format('hh:mm A') }} -
						{{ dayjs(getClassEnd(cls)).format('hh:mm A') }}
					</span>
				</div>
				<div v-if="cls.join_url" class="flex items-center space-x-2 group/link">
					<Link2Icon class="w-4 h-4 stroke-1.5 text-gray-500" />
					<span class="text-gray-500 truncate max-w-[200px] md:max-w-xs">
						{{ cls.join_url }}
					</span>
					<button
						@click.stop="copyToClipboard(cls.join_url)"
						class="p-1 hover:bg-gray-100 rounded transition-colors text-primary-500"
						:title="__('Copy Link')"
					>
						<Copy class="size-3.5" />
					</button>
				</div>
			</div>
		</div>
	</div>
	<div v-else class="flex flex-col items-center justify-center mt-6">
		<EmptyIcon class="size-24 mb-6" />
		<h3 class="text-lg font-bold text-gray-900 mb-2">
			Nothing to see here yet
		</h3>
		<p class="text-gray-500 text-ms font-medium">
			{{ __('No live classes scheduled') }}
		</p>
	</div>

	<LiveClassModal
		:batch="props.batch"
		:zoomAccount="props.zoomAccount"
		v-model="showLiveClassModal"
		v-model:reloadLiveClasses="liveClasses"
	/>

	<LiveClassAttendance v-model="showAttendance" :live_class="attendanceFor" />
</template>
<script setup>
import { createListResource, Button, Tooltip, toast } from 'frappe-ui'
import {
	Plus,
	Clock,
	Calendar,
	Video,
	Monitor,
	Info,
	AlertCircle,
	Link2 as Link2Icon,
	Copy,
} from 'lucide-vue-next'
import { inject, ref } from 'vue'
import LiveClassModal from '@/components/Modals/LiveClassModal.vue'
import LiveClassAttendance from '@/components/Modals/LiveClassAttendance.vue'
import Calendar2Icon from './Icons/Calendar2Icon.vue'
import ClockIcon from './Icons/ClockIcon.vue'

const user = inject('$user')
const showLiveClassModal = ref(false)
const dayjs = inject('$dayjs')
const readOnlyMode = window.read_only_mode
const showAttendance = ref(false)
const attendanceFor = ref(null)

const props = defineProps({
	batch: {
		type: String,
		required: true,
	},
	zoomAccount: String,
})

const liveClasses = createListResource({
	doctype: 'LMS Live Class',
	filters: {
		batch_name: props.batch,
	},
	fields: [
		'title',
		'description',
		'time',
		'date',
		'duration',
		'attendees',
		'start_url',
		'join_url',
		'owner',
	],
	orderBy: 'date',
	auto: true,
})

const openLiveClassModal = () => {
	showLiveClassModal.value = true
}

const canCreateClass = () => {
	if (readOnlyMode) return false
	if (!props.zoomAccount) return false
	return hasPermission()
}

const hasPermission = () => {
	return user.data?.is_moderator || user.data?.is_evaluator
}

const canAccessClass = (cls) => {
	if (cls.date < dayjs().format('YYYY-MM-DD')) return false
	if (cls.date > dayjs().format('YYYY-MM-DD')) return false
	if (hasClassEnded(cls)) return false
	return true
}

const getClassStart = (cls) => {
	return new Date(`${cls.date}T${cls.time}`)
}

const getClassEnd = (cls) => {
	const classStart = getClassStart(cls)
	return new Date(classStart.getTime() + cls.duration * 60000)
}

const hasClassEnded = (cls) => {
	const classEnd = getClassEnd(cls)
	const now = new Date()
	return now > classEnd
}

const openAttendanceModal = (cls) => {
	if (!hasPermission()) return
	if (cls.attendees <= 0) return
	showAttendance.value = true
	attendanceFor.value = cls
}

const copyToClipboard = (text) => {
	navigator.clipboard.writeText(text).then(() => {
		toast.success(__('Link copied to clipboard'))
	})
}
</script>
<style>
.short-introduction {
	display: -webkit-box;
	-webkit-line-clamp: 2;
	-webkit-box-orient: vertical;
	text-overflow: ellipsis;
	width: 100%;
	overflow: hidden;
	margin: 0.25rem 0 1.5rem;
	line-height: 1.5;
}
</style>
