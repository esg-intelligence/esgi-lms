<template>
	<div class="text-gray-700 font-medium flex-1 min-w-0 overflow-hidden">
		<div class="truncate text-sm">
			<span v-if="instructors?.length == 1">
				<router-link
					:to="{
						name: 'Profile',
						params: { username: instructors[0].username },
					}"
					class="hover:text-black"
				>
					{{ instructors[0].full_name }}
				</router-link>
			</span>

			<span v-else-if="instructors?.length == 2">
				<router-link
					:to="{
						name: 'Profile',
						params: { username: instructors[0].username },
					}"
					class="hover:text-black"
				>
					{{ instructors[0].first_name }}
				</router-link>
				<span class="mx-1">{{ __('and') }}</span>
				<router-link
					:to="{
						name: 'Profile',
						params: { username: instructors[1].username },
					}"
					class="hover:text-black"
				>
					{{ instructors[1].first_name }}
				</router-link>
			</span>

			<span v-else-if="instructors?.length > 2">
				<router-link
					:to="{
						name: 'Profile',
						params: { username: instructors[0].username },
					}"
					class="hover:text-black"
				>
					{{ instructors[0].first_name }}
				</router-link>
				<span class="mx-1">
					{{ __('and') }} {{ instructors.length - 1 }} {{ __('others') }}
				</span>
			</span>
		</div>
	</div>
</template>
<script setup>
const props = defineProps({
	instructors: {
		type: Array,
		required: true,
	},
})
</script>
