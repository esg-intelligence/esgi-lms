<template>
	<div v-if="feedbackList.data?.length">
		<div class="mb-10">
			<h2 class="text-xl font-semibold text-ink-gray-9 mb-6">
				{{ __('Batch Feedback') }}
			</h2>
			<div class="grid grid-cols-1 md:grid-cols-3 gap-x-2">
				<div
					v-for="key in ratingKeys"
					:key="key"
					class="flex-1 border rounded-lg p-6 flex justify-center items-center flex-col bg-white border-gray-100 h-fit"
				>
					<div class="text-5xl font-bold text-ink-gray-9">
						{{ average[key]?.toFixed(1) || '0.0' }}
					</div>
					<div class="text-base font-semibold text-gray-900 mb-2">
						{{ __(convertToTitleCase(key)) }}
					</div>
					<span
						class="[&_.\!fill-yellow-500]:!fill-warning-500 [&_.\!fill-yellow-200]:!fill-warning-200 mx-auto"
					>
						<Rating v-model="average[key]" />
					</span>
				</div>
			</div>
		</div>

		<div>
			<h2 class="text-xl font-semibold text-ink-gray-9 mb-6">
				{{ __('Students Feedback') }}
			</h2>
			<div class="space-y-6">
				<div
					v-for="row in feedbackList.data"
					:key="row.name"
					class="pb-6 border-b last:border-b-0"
				>
					<div class="flex items-start gap-3">
						<UserAvatar
							:user="{
								full_name: row.member_name,
								image: row.member_image,
								name: row.member,
							}"
							:size="'2xl'"
						/>

						<div class="flex-1">
							<div class="flex items-center gap-2 mb-1">
								<span class="font-medium text-sm text-ink-gray-9">
									{{ row.member_name }}
								</span>
								<span class="text-ink-gray-5">•</span>
								<span class="text-xs text-ink-gray-5">{{
									timeAgo(row.creation)
								}}</span>
							</div>
							<div
								class="flex mb-6 flex-row gap-6 [&_.\!fill-yellow-500]:!fill-warning-500 [&_.\!fill-yellow-200]:!fill-warning-200"
							>
								<Rating
									v-for="key in ratingKeys"
									v-model="row[key]"
									:label="__(convertToTitleCase(key))"
									:readonly="true"
								/>
							</div>
							<p
								v-if="row.feedback"
								class="text-sm text-ink-gray-7 leading-relaxed"
							>
								{{ row.feedback }}
							</p>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
	<div v-else class="flex flex-col items-center justify-center mt-20">
		<EmptyIcon class="size-24 mb-6" />
		<h3 class="text-lg font-bold text-gray-900 mb-2">
			{{ __('Nothing to see here yet') }}
		</h3>
		<p class="text-gray-500 text-sm font-medium">
			{{ __('No feedback received yet.') }}
		</p>
	</div>
</template>

<script setup>
import { computed } from 'vue'
import { convertToTitleCase, timeAgo } from '@/utils'
import { Button, createListResource, FormControl, Rating } from 'frappe-ui'
import UserAvatar from '@/components/UserAvatar.vue'
import { Star } from 'lucide-vue-next'
import EmptyIcon from '@/components/Icons/EmptyIcon.vue'
import { inject, onMounted, reactive, ref, watch } from 'vue'

const user = inject('$user')
const ratingKeys = ['content', 'instructors', 'value']
const readOnly = ref(false)
const average = reactive({})
const feedback = reactive({})
const showFeedbackForm = ref(true)
const showAllFeedback = ref(false)

const props = defineProps({
	batch: {
		type: String,
		required: true,
	},
})

onMounted(() => {
	let filters = {
		batch: props.batch,
	}
	if (user.data?.is_student) {
		filters['member'] = user.data?.name
	}
	feedbackList.update({
		filters: filters,
	})
	feedbackList.reload()
})

const feedbackList = createListResource({
	doctype: 'LMS Batch Feedback',
	filters: {
		batch: props.batch,
	},
	fields: [
		'content',
		'instructors',
		'value',
		'feedback',
		'name',
		'member',
		'member_name',
		'member_image',
		'creation',
	],
	cache: ['feedbackList', props.batch, user.data?.name],
})

watch(
	() => feedbackList.data,
	() => {
		if (feedbackList.data.length) {
			let data = feedbackList.data
			readOnly.value = true
			showFeedbackForm.value = false

			ratingKeys.forEach((key) => {
				average[key] = 0
			})

			data.forEach((row) => {
				Object.keys(row).forEach((key) => {
					if (ratingKeys.includes(key)) row[key] = row[key] * 5
					feedback[key] = row[key]
				})
				ratingKeys.forEach((key) => {
					average[key] += row[key]
				})
			})
			Object.keys(average).forEach((key) => {
				average[key] = average[key] / data.length
			})
		}
	},
)

const submitFeedback = () => {
	ratingKeys.forEach((key) => {
		feedback[key] = feedback[key] / 5
	})
	feedbackList.insert.submit(
		{
			member: user.data?.name,
			batch: props.batch,
			...feedback,
		},
		{
			onSuccess: () => {
				feedbackList.reload()
				showFeedbackForm.value = false
			},
		},
	)
}
</script>
