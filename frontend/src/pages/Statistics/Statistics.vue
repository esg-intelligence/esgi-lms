<template>
	<div v-if="user.data" class="">
		<header class="sticky top-0 z-10 flex items-center justify-between bg-surface-white px-3 py-2.5 sm:px-5">
			<Breadcrumbs :items="breadcrumbs" />
		</header>
		<StatisticsAdmin v-if="isAdmin" />
		<StatisticsStudent v-else />
	</div>
</template>
<script setup>
import {
	// AxisChart,
	Breadcrumbs,
	// DonutChart,
	usePageMeta,
} from 'frappe-ui'
import { computed, inject } from 'vue'
import { useRouter } from 'vue-router'
import { sessionStore } from '../../stores/session'
import StatisticsAdmin from './StatisticsAdmin.vue'
import StatisticsStudent from './StatisticsStudent.vue'

const user = inject('$user')
const { brand } = sessionStore()
const router = useRouter()

const breadcrumbs = computed(() => {
	return [
		{
			label: 'Statistics',
			route: {
				name: 'Statistics',
			},
		},
	]
})

const isAdmin = computed(() => {
	return (
		user.data?.is_moderator ||
		user.data?.is_instructor ||
		user.data?.is_evaluator
	)
})

if (!user.data) {
	router.push({
		name: 'Courses',
	})
}

usePageMeta(() => {
	return {
		title: __('Statistics'),
		icon: brand.favicon,
	}
})
</script>
