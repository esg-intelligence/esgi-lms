<template>
	<header class="sticky top-0 z-10 flex items-center justify-between border-b bg-surface-white px-3 py-2.5 sm:px-5">
		<Breadcrumbs :items="breadcrumbs" />
	</header>

	<div class="md:w-3/4 md:mx-auto py-5 mx-5">
		<template v-if="userList.loading || userList.data?.users?.length || searchTerm">
			<!-- Controls bar -->
			<div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-4">
				<FormControl
					v-model="searchTerm"
					type="text"
					:placeholder="__('Search by name or email')"
					class="sm:max-w-xs"
				/>
				<div class="flex items-center gap-2 text-sm text-ink-gray-5 self-end sm:self-auto">
					<span>{{ __('Rows per page:') }}</span>
					<FormControl
						v-model="pageLength"
						type="select"
						:options="pageLengthOptions"
						class="w-24"
					/>
				</div>
			</div>

			<Table>
				<TableHeader>
					<TableRow>
						<TableHead
							class="cursor-pointer select-none"
							@click="toggleSort('full_name')"
						>
							<div class="flex items-center gap-1">
								{{ __('Name') }}
								<template v-if="sortField === 'full_name'">
									<ChevronUp v-if="sortDirection === 'asc'" class="w-3 h-3" />
									<ChevronDown v-else class="w-3 h-3" />
								</template>
								<ChevronsUpDown v-else class="w-3 h-3 opacity-40" />
							</div>
						</TableHead>
						<TableHead
							class="cursor-pointer select-none"
							@click="toggleSort('name')"
						>
							<div class="flex items-center gap-1">
								{{ __('Email') }}
								<template v-if="sortField === 'name'">
									<ChevronUp v-if="sortDirection === 'asc'" class="w-3 h-3" />
									<ChevronDown v-else class="w-3 h-3" />
								</template>
								<ChevronsUpDown v-else class="w-3 h-3 opacity-40" />
							</div>
						</TableHead>
						<TableHead class="text-right">{{ __('Actions') }}</TableHead>
					</TableRow>
				</TableHeader>
				<TableBody>
					<TableRow v-for="row in userList.data?.users" :key="row.name">
						<TableCell>
							<div class="flex items-center gap-2">
								<Avatar
									:label="row.full_name"
									:image="row.user_image"
									size="sm"
									class="flex-shrink-0"
								/>
								<span>{{ row.full_name }}</span>
							</div>
						</TableCell>
						<TableCell class="text-ink-gray-5">{{ row.name }}</TableCell>
						<TableCell class="text-right">
							<div v-if="row.username" class="flex items-center justify-end gap-3">
								<router-link
									:to="{ name: 'Profile', params: { username: row.username } }"
									:title="__('View profile')"
								>
									<UserIcon class="h-4 w-4 text-gray-400 hover:text-gray-700" />
								</router-link>
								<router-link
									:to="{ name: 'UserCourseProgress', params: { username: row.username } }"
									:title="__('View course progress')"
								>
									<BarChart2 class="h-4 w-4 text-gray-400 hover:text-gray-700" />
								</router-link>
							</div>
						</TableCell>
					</TableRow>
				</TableBody>
			</Table>

			<div class="flex items-center justify-between mt-4 text-sm text-ink-gray-5">
				<span v-if="totalCount">
					{{ __('Showing {0}–{1} of {2}').format(showingFrom, showingTo, totalCount) }}
				</span>
				<span v-else></span>
				<div class="flex items-center gap-2">
					<Button variant="outline" :disabled="currentPage === 1" @click="prevPage">
						{{ __('Previous') }}
					</Button>
					<span>{{ __('Page {0} of {1}').format(currentPage, totalPages) }}</span>
					<Button variant="outline" :disabled="currentPage >= totalPages" @click="nextPage">
						{{ __('Next') }}
					</Button>
				</div>
			</div>
		</template>

		<div
			v-else
			class="text-center p-5 text-ink-gray-5 mt-52 w-3/4 md:w-1/2 mx-auto space-y-2"
		>
			<Users class="size-8 mx-auto stroke-1 text-ink-gray-4" />
			<div class="text-xl font-medium">{{ __('No users') }}</div>
			<div class="leading-5">{{ __('No users were found.') }}</div>
		</div>
	</div>
</template>

<script setup>
import { createResource, Avatar, Button, FormControl, Breadcrumbs, usePageMeta } from 'frappe-ui'
import { ref, computed, inject, onMounted, watch } from 'vue'
import { watchDebounced } from '@vueuse/core'
import { ChevronUp, ChevronDown, ChevronsUpDown, User as UserIcon, BarChart2, Users } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import {
	Table, TableBody, TableCell, TableHead, TableHeader, TableRow,
} from '@/components/ui/table'

const $user = inject('$user')
const router = useRouter()

const searchTerm = ref('')
const sortField = ref('full_name')
const sortDirection = ref('asc')
const pageLength = ref(20)
const currentPage = ref(1)

const orderBy = computed(() => `${sortField.value} ${sortDirection.value}`)
const totalCount = computed(() => userList.data?.total ?? 0)
const totalPages = computed(() => Math.ceil(totalCount.value / pageLength.value) || 1)
const start = computed(() => (currentPage.value - 1) * pageLength.value)
const showingFrom = computed(() => Math.min(start.value + 1, totalCount.value))
const showingTo = computed(() => Math.min(start.value + parseInt(pageLength.value), totalCount.value))

const userList = createResource({
	url: 'lms.lms.api.get_user_list',
	makeParams: () => ({
		start: start.value,
		page_length: pageLength.value,
		search: searchTerm.value,
		order_by: orderBy.value,
	}),
})

const reload = () => userList.submit()

const hasAccess = (u) =>
	u?.is_moderator || u?.is_instructor || u?.is_evaluator || u?.is_system_manager

onMounted(() => {
	if (!hasAccess($user.data)) {
		router.push({ name: 'Courses' })
		return
	}
	reload()
})

const toggleSort = (field) => {
	if (sortField.value === field) {
		sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
	} else {
		sortField.value = field
		sortDirection.value = 'asc'
	}
	currentPage.value = 1
	reload()
}

watch(pageLength, () => {
	currentPage.value = 1
	reload()
})

watch(currentPage, reload)

watchDebounced(searchTerm, () => {
	currentPage.value = 1
	reload()
}, { debounce: 300 })

const prevPage = () => { if (currentPage.value > 1) currentPage.value-- }
const nextPage = () => { if (currentPage.value < totalPages.value) currentPage.value++ }

const pageLengthOptions = [
	{ label: '10', value: 10 },
	{ label: '20', value: 20 },
	{ label: '50', value: 50 },
]

const breadcrumbs = computed(() => [{ label: __('Users') }])

usePageMeta(() => ({ title: __('Users') }))
</script>
