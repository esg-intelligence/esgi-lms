<template>
	<header class="sticky top-0 z-10 flex items-center justify-between bg-surface-white px-3 py-2.5 sm:px-5">
		<Breadcrumbs :items="breadcrumbs" />
		<div class="flex">
			<router-link class="mr-2" :to="{
				name: 'AssignmentSubmissionList',
			}">
				<Button variant="outline" class="">
					<template #prefix>
						<List class="w-4 h-4" />
					</template>
					{{ __('View All Submissions') }}
				</Button>
			</router-link>
			<Button v-if="!readOnlyMode" variant="solid" class="" @click="
				() => {
					assignmentID = 'new'
					showAssignmentForm = true
				}
			">
				<template #prefix>
					<Plus class="w-4 h-4" />
				</template>
				{{ __('Create') }}
			</Button>
		</div>
	</header>

	<div class="md:w-3/4 md:mx-auto py-5 mx-5">
		<div class="flex items-center justify-between mb-5">
			<div v-if="assignmentCount" class="text-lg font-semibold text-ink-gray-9">
				{{ __('{0} Assignments').format(assignmentCount) }}
			</div>
			<div v-if="assignments.data?.length || assignmentCount > 0" class="grid grid-cols-3 gap-5">
				<FormControl v-model="titleFilter" :placeholder="__('Search by title')" />
				<FormControl v-model="typeFilter" type="select" :options="assignmentTypes" :placeholder="__('Type')" />
				<FormControl v-model="categoryFilter" type="select" :options="assignmentCategories"
					:placeholder="__('Category')" />
			</div>
		</div>
		<!-- <ListView
			v-if="assignments.data?.length"
			:columns="assignmentColumns"
			:rows="assignments.data"
			row-key="name"
			:options="{
				showTooltip: false,
				selectable: false,
				onRowClick: (row) => {
					if (readOnlyMode) return
					assignmentID = row.name
					showAssignmentForm = true
				},
			}"
		>
		</ListView> -->
		<Table v-if="assignments.data?.length">
			<TableHeader>
				<TableRow>
					<TableHead>Title</TableHead>
					<TableHead>Type</TableHead>
					<TableHead>Created</TableHead>
					<TableHead>Actions</TableHead>
				</TableRow>
			</TableHeader>
			<TableBody>
				<TableRow v-for="assignment in assignments.data" :key="assignment.name">
					<TableCell class="font-medium">{{ assignment.title }}</TableCell>
					<TableCell>{{ assignment.type }}</TableCell>
					<TableCell>{{ assignment.creation }}</TableCell>
					<TableCell>
						<Btn class="mr-2" @click="() => {
							if (readOnlyMode) return
							assignmentID = assignment.name
							showAssignmentForm = true
						}">
							Edit
						</Btn>
						<router-link class="mr-2" :to="{
							name: 'AssignmentSubmissionList',
							query: {
								assignmentID: assignment.name,
							},
						}">
							<Btn>Check Submissions</Btn>
						</router-link>
						<Btn class="mr-2" @click="() => {
							if (readOnlyMode) return
							assignmentID = assignment.name
							showDeleteForm = true
						}">
							Delete
						</Btn>
					</TableCell>
				</TableRow>
			</TableBody>
		</Table>
		<EmptyState v-else type="Assignments" />
		<div v-if="assignments.data && assignments.hasNextPage" class="flex justify-center my-5">
			<Button @click="assignments.next()">
				{{ __('Load More') }}
			</Button>
		</div>
	</div>
	<AssignmentForm v-model="showAssignmentForm" v-model:assignments="assignments" :assignmentID="assignmentID" />
	<Dialog v-model="showDeleteForm" :options="{
		title: __('Delete Assignment'),
		size: 'sm',
		actions: [
			{
				label: __('Confirm'),
				variant: 'solid',
				onClick({ close }) {
					deleteAssignment(close)
				},
			},
		],
	}">
		<template #body-content>Are you sure want to delete this?</template>
	</Dialog>
</template>
<script setup>
import {
	Dialog,
	Breadcrumbs,
	call,
	createListResource,
	FormControl,
	ListView,
	usePageMeta,
	toast,
	Button as Btn
} from 'frappe-ui'
import { computed, inject, onMounted, ref, watch } from 'vue'
import { List, Plus } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import { sessionStore } from '../stores/session'
import AssignmentForm from '@/components/Modals/AssignmentForm.vue'
import EmptyState from '@/components/EmptyState.vue'
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
const titleFilter = ref('')
const typeFilter = ref('')
const categoryFilter = ref('')
const showAssignmentForm = ref(false)
const assignmentID = ref('new')
const assignmentCount = ref(0)
const showDeleteForm = ref(false)
const { brand } = sessionStore()
const router = useRouter()
const readOnlyMode = window.read_only_mode

onMounted(() => {
	if (!user.data?.is_moderator && !user.data?.is_instructor) {
		router.push({ name: 'Courses' })
	}
	getAssignmentCount()
	titleFilter.value = router.currentRoute.value.query.title
	typeFilter.value = router.currentRoute.value.query.type
	categoryFilter.value = router.currentRoute.value.query.category
})

watch([titleFilter, typeFilter, categoryFilter], () => {
	router.push({
		query: {
			title: titleFilter.value,
			type: typeFilter.value,
			category: categoryFilter.value,
		},
	})
	reloadAssignments()
})

const reloadAssignments = () => {
	assignments.update({
		filters: assignmentFilter.value,
	})
	assignments.reload()
}

const assignmentFilter = computed(() => {
	let filters = {}
	if (titleFilter.value) {
		filters.title = ['like', `%${titleFilter.value}%`]
	}
	if (typeFilter.value) {
		filters.type = typeFilter.value
	}
	if (categoryFilter.value) {
		filters.category = categoryFilter.value
	}
	if (!user.data?.is_moderator) {
		filters.owner = user.data?.email
	}
	return filters
})

const assignments = createListResource({
	doctype: 'LMS Assignment',
	fields: ['name', 'title', 'type', 'category', 'creation', 'question', 'industry', 'passing_score'],
	orderBy: 'modified desc',
	cache: ['assignments'],
	transform(data) {
		return data.map((row) => {
			return {
				...row,
				creation: dayjs(row.creation).fromNow(),
			}
		})
	},
})

const assignmentColumns = computed(() => {
	return [
		{
			label: __('Title'),
			key: 'title',
			width: 2,
		},
		{
			label: __('Type'),
			key: 'type',
			width: 1,
			align: 'left',
		},
		{
			label: __('Created'),
			key: 'creation',
			width: 1,
			align: 'right',
		},
	]
})

const getAssignmentCount = () => {
	call('frappe.client.get_count', {
		doctype: 'LMS Assignment',
	}).then((data) => {
		assignmentCount.value = data
	})
}

const deleteAssignment = (close) => {
	assignments.delete.submit(
		assignmentID.value,
		{
			onSuccess() {
				toast.success(__('Assignment deleted successfully'))
				close()
			},
			onError(error) {
				toast.error(__('Error deleting assignment', error.message))
			}
		}
	)
}

const assignmentTypes = computed(() => {
	let types = ['', 'Document', 'Image', 'PDF', 'URL', 'Text']
	return types.map((type) => {
		return {
			label: __(type),
			value: type,
		}
	})
})

const assignmentCategories = computed(() => {
	return [
		{ label: '', value: '' },
		{ label: __('Pre-Test'), value: 'Pre-Test' },
		{ label: __('Post-Test'), value: 'Post-Test' },
	]
})

const breadcrumbs = computed(() => [
	{
		label: 'Assignments',
		route: { name: 'Assignments' },
	},
])

usePageMeta(() => {
	return {
		title: __('Assignments'),
		icon: brand.favicon,
	}
})
</script>
