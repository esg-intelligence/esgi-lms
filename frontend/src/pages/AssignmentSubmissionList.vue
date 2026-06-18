<template>
	<header
		class="sticky top-0 z-10 flex items-center justify-between border-b bg-surface-white px-3 py-2.5 sm:px-5"
	>
		<Breadcrumbs :items="breadcrumbs" />
	</header>
	<div class="md:w-3/4 md:mx-auto py-5 mx-5">
		<div class="grid grid-cols-3 gap-5 mb-5">
			<Link
				doctype="LMS Assignment"
				v-model="assignmentID"
				:placeholder="__('Assignment')"
			/>
			<Link doctype="User" v-model="member" :placeholder="__('Member')" />
			<FormControl
				v-model="status"
				type="select"
				:options="statusOptions"
				:placeholder="__('Status')"
			/>
		</div>

		<template v-if="submissions.loading || submissions.data?.length">
			<div class="flex items-center justify-end gap-2 mb-3 text-sm text-ink-gray-5">
				<span>{{ __('Rows per page:') }}</span>
				<FormControl
					v-model="pageLength"
					type="select"
					:options="pageLengthOptions"
					class="w-24"
				/>
			</div>

			<Table>
				<TableHeader>
					<TableRow>
						<TableHead
							class="cursor-pointer select-none"
							@click="toggleSort('member_name')"
						>
							<div class="flex items-center gap-1">
								{{ __('Member') }}
								<template v-if="sortField === 'member_name'">
									<ChevronUp v-if="sortDirection === 'asc'" class="w-3 h-3" />
									<ChevronDown v-else class="w-3 h-3" />
								</template>
								<ChevronsUpDown v-else class="w-3 h-3 opacity-40" />
							</div>
						</TableHead>
						<TableHead
							class="cursor-pointer select-none"
							@click="toggleSort('assignment_title')"
						>
							<div class="flex items-center gap-1">
								{{ __('Assignment') }}
								<template v-if="sortField === 'assignment_title'">
									<ChevronUp v-if="sortDirection === 'asc'" class="w-3 h-3" />
									<ChevronDown v-else class="w-3 h-3" />
								</template>
								<ChevronsUpDown v-else class="w-3 h-3 opacity-40" />
							</div>
						</TableHead>
						<TableHead>{{ __('Submitted') }}</TableHead>
						<TableHead class="text-center">{{ __('Status') }}</TableHead>
					</TableRow>
				</TableHeader>
				<TableBody>
					<TableRow
						v-for="row in submissions.data"
						:key="row.name"
						class="cursor-pointer hover:bg-surface-gray-1"
						@click="goToSubmission(row)"
					>
						<TableCell>{{ row.member_name }}</TableCell>
						<TableCell>{{ row.assignment_title }}</TableCell>
						<TableCell>{{ row.creation }}</TableCell>
						<TableCell class="text-center">
							<Badge :theme="getStatusTheme(row.status)">{{ row.status }}</Badge>
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
			<Pencil class="size-8 mx-auto stroke-1 text-ink-gray-4" />
			<div class="text-xl font-medium">
				{{ __('No submissions') }}
			</div>
			<div class="leading-5">
				{{ __('There are no submissions for this assignment.') }}
			</div>
		</div>
	</div>
</template>
<script setup>
import {
	Badge,
	Breadcrumbs,
	call,
	createListResource,
	FormControl,
	usePageMeta,
} from 'frappe-ui'
import { computed, inject, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ChevronDown, ChevronUp, ChevronsUpDown, Pencil } from 'lucide-vue-next'
import { sessionStore } from '../stores/session'
import Link from '@/components/Controls/Link.vue'
import Button from '@/components/ui/Button.vue'
import {
	Table,
	TableBody,
	TableCell,
	TableHead,
	TableHeader,
	TableRow,
} from '@/components/ui/table'

const user = inject('$user')
const dayjs = inject('$dayjs')
const { brand } = sessionStore()
const router = useRouter()

const assignmentID = ref('')
const member = ref('')
const status = ref('')
const sortField = ref('creation')
const sortDirection = ref('desc')
const pageLength = ref(50)
const currentPage = ref(1)
const totalCount = ref(0)

const orderBy = computed(() => `${sortField.value} ${sortDirection.value}`)
const totalPages = computed(() => Math.ceil(totalCount.value / pageLength.value) || 1)
const start = computed(() => (currentPage.value - 1) * pageLength.value)
const showingFrom = computed(() => Math.min(start.value + 1, totalCount.value))
const showingTo = computed(() => Math.min(start.value + parseInt(pageLength.value), totalCount.value))

onMounted(() => {
	if (!user.data?.is_instructor && !user.data?.is_moderator) {
		router.push({ name: 'Courses' })
	}
	assignmentID.value = router.currentRoute.value.query.assignmentID
	member.value = router.currentRoute.value.query.member
	status.value = router.currentRoute.value.query.status
	reloadSubmissions()
})

const getAssignmentFilters = () => {
	let filters = {}
	if (assignmentID.value) {
		filters.assignment = assignmentID.value
	}
	if (member.value) {
		filters.member = member.value
	}
	if (status.value) {
		filters.status = status.value
	}
	return filters
}

const submissions = createListResource({
	doctype: 'LMS Assignment Submission',
	fields: ['name', 'assignment', 'assignment_title', 'member_name', 'creation', 'status'],
	orderBy: orderBy.value,
	pageLength: pageLength.value,
	start: 0,
	transform(data) {
		return data.map((row) => ({
			...row,
			creation: dayjs(row.creation).fromNow(),
		}))
	},
})

watch([assignmentID, member, status], () => {
	currentPage.value = 1
	router.push({
		query: {
			assignmentID: assignmentID.value,
			member: member.value,
			status: status.value,
		},
	})
	reloadSubmissions()
})

watch(pageLength, () => {
	currentPage.value = 1
	reloadSubmissions()
})

const reloadSubmissions = () => {
	submissions.update({
		filters: getAssignmentFilters(),
		orderBy: orderBy.value,
		pageLength: parseInt(pageLength.value),
		start: start.value,
	})
	submissions.reload()
	fetchCount()
}

const fetchCount = () => {
	call('frappe.client.get_count', {
		doctype: 'LMS Assignment Submission',
		filters: getAssignmentFilters(),
	}).then((data) => {
		totalCount.value = data
	})
}

const toggleSort = (field) => {
	if (sortField.value === field) {
		sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
	} else {
		sortField.value = field
		sortDirection.value = 'asc'
	}
	currentPage.value = 1
	reloadSubmissions()
}

const prevPage = () => {
	if (currentPage.value > 1) {
		currentPage.value--
		reloadSubmissions()
	}
}

const nextPage = () => {
	if (currentPage.value < totalPages.value) {
		currentPage.value++
		reloadSubmissions()
	}
}

const goToSubmission = (row) => {
	router.push({
		name: 'AssignmentSubmission',
		params: { assignmentID: row.assignment, submissionName: row.name },
	})
}

const pageLengthOptions = [
	{ label: '10', value: 10 },
	{ label: '50', value: 50 },
	{ label: '100', value: 100 },
	{ label: '250', value: 250 },
]

const statusOptions = computed(() => {
	return [
		{ label: '', value: '' },
		{ label: __('Pass'), value: 'Pass' },
		{ label: __('Fail'), value: 'Fail' },
		{ label: __('Not Graded'), value: 'Not Graded' },
	]
})

const getStatusTheme = (status) => {
	if (status === 'Pass') return 'green'
	if (status === 'Not Graded') return 'blue'
	return 'red'
}

const breadcrumbs = computed(() => {
	return [{ label: 'Assignment Submissions' }]
})

usePageMeta(() => {
	return {
		title: __('Assignment Submissions'),
		icon: brand.favicon,
	}
})
</script>
