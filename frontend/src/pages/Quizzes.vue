<template>
	<header class="sticky top-0 z-10 flex items-center justify-between bg-surface-white px-3 py-2.5 sm:px-5">
		<Breadcrumbs :items="breadcrumbs" />
		<Button v-if="!readOnlyMode" variant="solid" @click="showForm = true">
			<template #prefix>
				<Plus class="w-4 h-4" />
			</template>
			{{ __('Create') }}
		</Button>
	</header>
	<div class="py-5 mx-5">
		<div class="flex items-center justify-between mb-4">
			<div class="text-lg font-semibold text-ink-gray-7">
				{{
					quizzes.data?.length
						? __('{0} Quizzes').format(quizzes.data.length)
						: __('No Quizzes')
				}}
			</div>
			<FormControl v-model="search" type="text" placeholder="Search">
				<template #prefix>
					<FeatherIcon name="search" class="size-4 text-ink-gray-5" />
				</template>
			</FormControl>
		</div>
		<Table v-if="quizzes.data?.length">
			<TableHeader class="bg-surface-gray-2">
				<TableRow>
					<TableHead v-for="column in quizColumns" :key="column.key">
						<div class="flex gap-x-2" :class="column.class == 'text-center' ? 'justify-center' : ''">
							<FeatherIcon :name="column.icon?.toString()" class="h-4 w-4" />
							<span class="block -mt-px">{{ column.label }}</span>
						</div>
					</TableHead>
				</TableRow>
			</TableHeader>
			<TableBody>
				<TableRow v-for="quiz in quizzes.data" :key="quiz.name">
					<TableCell v-for="column in quizColumns" :class="column.class" class="text-base">
						<div v-if="column.key == 'show_answers'">
							<FormControl type="checkbox" v-model="quiz[column.key]" :disabled="true" />
						</div>
						<div v-else-if="column.key == 'modified'" class="text-xs text-ink-gray-5">
							{{ quiz[column.key] }}
						</div>
						<div v-else-if="column.key == 'actions'" class="text-center">
							<Btn class="mr-2" @click="() => {
								// if (readOnlyMode) return
								selectedQuiz = quiz.name
								showDuplicateForm = true
							}">
								Duplicate
							</Btn>
							<router-link :to="{
								name: 'QuizForm',
								params: {
									quizID: quiz.name,
								},
							}">
								<Btn>Detail</Btn>
							</router-link>
						</div>
						<div v-else>
							{{ quiz[column.key] }}
						</div>
					</TableCell>
				</TableRow>
			</TableBody>
		</Table>
		<EmptyState v-else type="Quizzes" />
		<div v-if="quizzes.hasNextPage" class="flex justify-center my-5">
			<Button @click="quizzes.next()">
				{{ __('Load More') }}
			</Button>
		</div>
	</div>
	<Dialog v-model="showForm" :options="{
		title: __('Create a Quiz'),
		size: 'sm',
		actions: [
			{
				label: __('Save'),
				variant: 'solid',
				onClick({ close }) {
					insertQuiz(close)
				},
			},
		],
	}">
		<template #body-content>
			<FormControl v-model="title" :label="__('Title')" type="text" />
		</template>
	</Dialog>
	<QuizForm v-model="showDuplicateForm" :reload="quizzes.reload" :selected="selectedQuiz" />
</template>
<script setup>
import {
	Breadcrumbs,
	createListResource,
	Dialog,
	FeatherIcon,
	FormControl,
	toast,
	usePageMeta,
	Button as Btn
} from 'frappe-ui'
import { useRouter } from 'vue-router'
import { computed, inject, onMounted, ref, watch } from 'vue'
import { Plus } from 'lucide-vue-next'
import { sessionStore } from '@/stores/session'
import { escapeHTML } from '@/utils'
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
import QuizForm from '@/components/Modals/QuizForm.vue'

const { brand } = sessionStore()
const user = inject('$user')
const dayjs = inject('$dayjs')
const router = useRouter()
const search = ref('')
const readOnlyMode = window.read_only_mode
const quizFilters = ref({})
const showForm = ref(false)
const title = ref('')
const showDuplicateForm = ref(false)
const selectedQuiz = ref('')

onMounted(() => {
	if (!user.data?.is_moderator && !user.data?.is_instructor) {
		router.push({ name: 'Courses' })
	} else if (!user.data?.is_moderator) {
		quizFilters.value['owner'] = user.data?.name
	}
})

watch(search, () => {
	quizFilters.value['title'] = ['like', `%${search.value}%`]
	quizzes.update({
		filters: quizFilters.value,
	})
	quizzes.reload()
})

const quizzes = createListResource({
	doctype: 'LMS Quiz',
	filters: quizFilters,
	fields: [
		'name',
		'title',
		'passing_percentage',
		'total_marks',
		'show_answers',
		'max_attempts',
		'modified',
	],
	auto: true,
	cache: ['quizzes', user.data?.name],
	orderBy: 'modified desc',
	transform(data) {
		return data.map((quiz) => {
			return {
				...quiz,
				modified: dayjs(quiz.modified).fromNow(),
			}
		})
	},
})

const validateTitle = () => {
	title.value = escapeHTML(title.value.trim())
}

const insertQuiz = (close) => {
	validateTitle()
	quizzes.insert.submit(
		{
			title: title.value,
		},
		{
			onSuccess(data) {
				toast.success(__('Quiz created successfully'))
				close()
				title.value = ''
				router.push({
					name: 'QuizForm',
					params: {
						quizID: data.name,
					},
				})
			},
			onError(error) {
				toast.error(__('Error creating quiz: {0}', error.message))
			},
		},
	)
}

const deleteQuiz = (selections, unselectAll) => {
	Array.from(selections).forEach(async (quizName) => {
		await quizzes.delete.submit(quizName)
	})
	unselectAll()
	toast.success(__('Quizzes deleted successfully'))
}

const quizColumns = computed(() => {
	return [
		{
			label: __('Title'),
			key: 'title',
			icon: 'file-text',
		},
		{
			label: __('Total Marks'),
			key: 'total_marks',
			class: 'text-center',
			icon: 'hash',
		},
		{
			label: __('Passing Percentage'),
			key: 'passing_percentage',
			class: 'text-center',
			icon: 'percent',
		},
		{
			label: __('Max Attempts'),
			key: 'max_attempts',
			class: 'text-center',
			icon: 'repeat',
		},
		{
			label: __('Show Answers'),
			key: 'show_answers',
			class: 'text-center',
			icon: 'eye',
		},
		{
			label: __('Modified'),
			key: 'modified',
			class: 'text-center',
			icon: 'clock',
		},
		{
			label: __('Actions'),
			key: 'actions',
			class: 'text-center',
			icon: 'settings',
		},
	]
})

const breadcrumbs = computed(() => {
	return [
		{
			label: __('Quizzes'),
			route: {
				name: 'Quizzes',
			},
		},
	]
})

usePageMeta(() => {
	return {
		title: __('Quizzes'),
		icon: brand.favicon,
	}
})
</script>
