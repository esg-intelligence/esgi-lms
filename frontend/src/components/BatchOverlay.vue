<template>
	<div
		v-if="batch.data"
		class="w-full h-fit border border-gray-100 rounded-xl flex flex-col md:flex-row"
	>
		<div
			class="w-full md:w-32 aspect-[330/140] md:aspect-square rounded-tl-xl rounded-tr-xl md:rounded-tr-none md:rounded-bl-xl"
		>
			<img
				v-if="!!batch.data?.meta_image"
				:src="batch.data.meta_image"
				class="w-full h-full object-cover rounded-tl-xl rounded-bl-xl"
			/>
			<NoImageFallback
				v-else
				class="w-full h-full rounded-tl-xl rounded-bl-xl"
			/>
		</div>
		<div class="flex-1 px-3 py-3 flex flex-col gap-y-2 justify-center">
			<div class="h-fit">
				<h1 class="text-base leading-5 font-semibold mb-1 text-gray-900">
					{{ batch.data.title }}
				</h1>
				<p class="short-introduction text-xs text-gray-600 !mb-0">
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
					{{ formatNumberIntoCurrency(batch.data.amount, batch.data.currency) }}
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

		<div
			v-if="!readOnlyMode"
			class="flex flex-col justify-center px-3 pb-2 md:pl-0 md:pb-0 md:pr-3"
		>
			<router-link
				v-if="canAccessBatch"
				:to="{
					name: 'Batch',
					params: {
						batchName: batch.data.name,
					},
				}"
			>
				<Button variant="solid" class="w-full mt-4">
					<span>
						{{ isStudent ? __('Visit Batch') : __('Manage Batch') }}
					</span>
				</Button>
			</router-link>
			<router-link
				:to="{
					name: 'Billing',
					params: {
						type: 'batch',
						name: batch.data.name,
					},
				}"
				v-else-if="
					batch.data.paid_batch &&
					batch.data.seats_left > 0 &&
					batch.data.accept_enrollments
				"
			>
				<Button v-if="!isStudent" class="w-full mt-4" variant="solid">
					<span>
						{{ __('Register Now') }}
					</span>
				</Button>
			</router-link>
			<Button
				variant="solid"
				class="w-full mt-2"
				v-else-if="
					batch.data.allow_self_enrollment &&
					batch.data.seats_left &&
					batch.data.accept_enrollments
				"
				@click="enrollInBatch()"
			>
				{{ __('Enroll Now') }}
			</Button>
			<router-link
				v-if="canEditBatch"
				:to="{
					name: 'BatchForm',
					params: {
						batchName: batch.data.name,
					},
				}"
			>
				<Button class="w-full mt-2">
					<span>
						{{ __('Edit') }}
					</span>
				</Button>
			</router-link>
		</div>
	</div>
</template>
<script setup>
import { inject, computed } from 'vue'
import { createResource, toast } from 'frappe-ui'
import {
	BookOpen,
	Clock,
	CreditCard,
	Globe,
	GraduationCap,
	LogIn,
	Pencil,
	Settings,
} from 'lucide-vue-next'
import { formatNumberIntoCurrency, formatTime } from '@/utils'
import DateRange from '@/components/Common/DateRange.vue'
import { useRouter } from 'vue-router'
import ClockIcon from '@/components/Icons/ClockIcon.vue'
import NoImageFallback from './NoImageFallback.vue'
import Button from './ui/Button.vue'

const router = useRouter()
const user = inject('$user')
const readOnlyMode = window.read_only_mode

const props = defineProps({
	batch: {
		type: Object,
		default: null,
	},
})

const enroll = createResource({
	url: 'lms.lms.utils.enroll_in_batch',
	makeParams(values) {
		return {
			batch: props.batch.data.name,
		}
	},
})

const enrollInBatch = () => {
	if (!user.data) {
		window.location.href = `/login?redirect-to=/batches/details/${props.batch.data.name}`
	}
	enroll.submit(
		{},
		{
			onSuccess(data) {
				toast.success(__('You have been enrolled in this batch'))
				router.push({
					name: 'Batch',
					params: {
						batchName: props.batch.data.name,
					},
				})
			},
		},
	)
}

const seats_left = computed(() => {
	if (props.batch.data?.seat_count) {
		return props.batch.data?.seat_count - props.batch.data?.students?.length
	}
	return null
})

const isStudent = computed(() => {
	return props.batch.data?.students?.includes(user.data?.name)
})

const isModerator = computed(() => {
	return user.data?.is_moderator
})

const isEvaluator = computed(() => {
	return user.data?.is_evaluator
})

const isInstructor = computed(() => {
	return (
		props.batch.data?.instructors?.filter(
			(instructor) => instructor.name === user.data?.name,
		).length > 0
	)
})

const canAccessBatch = computed(() => {
	return isModerator.value || isStudent.value || isEvaluator.value
})

const canEditBatch = computed(() => {
	return isModerator.value || isInstructor.value
})
</script>
