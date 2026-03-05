<template>
	<div class="flex items-center justify-between mb-6">
		<div class="text-xl font-semibold text-ink-gray-9">
			{{ __('Announcements') }}
		</div>
	</div>
	<div v-if="communications.data?.length" class="space-y-4">
		<div v-for="comm in communications.data" :key="comm.name">
			<div
				class="flex items-start p-4 rounded-xl border border-gray-100 w-full space-x-4 cursor-pointer bg-white"
			>
				<img
					src="/icons/directbox.png"
					alt="announcement"
					class="w-10 h-10 flex-shrink-0"
				/>
				<div class="notification flex-1">
					<div class="text-gray-900 text-md md:font-medium md:text-lg mb-1">
						{{ comm.subject }}
					</div>
					<div
						class="text-gray-600 text-sm md:text-md mb-2 line-clamp-2"
						v-html="comm.content"
					></div>
					<div class="text-gray-500 font-regular text-xs md:text-sm">
						{{ timeAgo(comm.communication_date) }}
					</div>
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
			{{ __('No announcements') }}
		</p>
	</div>
</template>
<script setup>
import { createResource, Avatar } from 'frappe-ui'
import { timeAgo } from '@/utils'

const props = defineProps({
	batch: {
		type: String,
		required: true,
	},
})

const communications = createResource({
	url: 'lms.lms.api.get_announcements',
	makeParams(value) {
		return {
			batch: props.batch,
		}
	},
	auto: true,
	cache: ['announcement', props.batch],
})
</script>
<style>
.prose-sm p {
	margin: 0 0 0.5rem;
}
</style>
