<template>
	<div class="flex flex-col items-center justify-center mt-60">
		<EmptyIcon class="size-24 mb-6" />
		<h3 class="text-lg font-bold text-gray-900 mb-2">
			Nothing to see here yet
		</h3>
		<p class="text-gray-500 text-ms font-medium">
			{{ __('Your learning updates will show up here soon') }}
		</p>
	</div>
</template>
<script setup lang="ts">
const props = defineProps({
	type: String,
})
</script>
