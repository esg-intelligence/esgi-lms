<template>
	<div v-if="!forHome || (forHome && upcoming_evals.data?.length)">
		<div class="flex items-center justify-between mb-4">
			<div class="text-xl text-ink-gray-9 font-semibold">
				{{ __('Upcoming Evaluations') }}
			</div>
			<Button
				v-if="
					upcoming_evals.data?.length != evaluationCourses.length &&
					!forHome &&
					upcoming_evals.data?.length
				"
				@click="openEvalModal"
				variant="solid"
			>
				{{ __('Schedule Evaluation') }}
			</Button>
		</div>
		<div v-if="upcoming_evals.data?.length">
			<div
				class="grid gap-4"
				:class="forHome ? 'grid-cols-1 md:grid-cols-2' : 'grid-cols-1'"
			>
				<div v-for="evl in upcoming_evals.data">
					<div
						class="relative border border-gray-100 text-ink-gray-7 rounded-md p-3 flex items-center justify-between"
					>
						<Menu
							v-if="evl.date > dayjs().format()"
							as="div"
							class="absolute right-3 top-2 inline-block text-left"
						>
							<div>
								<MenuButton class="inline-flex w-full justify-center">
									<EllipsisVertical class="w-4 h-4 stroke-1.5" />
								</MenuButton>
							</div>

							<transition
								enter-active-class="transition duration-100 ease-out"
								enter-from-class="transform scale-95 opacity-0"
								enter-to-class="transform scale-100 opacity-100"
								leave-active-class="transition duration-75 ease-in"
								leave-from-class="transform scale-100 opacity-100"
								leave-to-class="transform scale-95 opacity-0"
							>
								<MenuItems
									class="absolute top-0 right-0 mt-2 w-32 rounded-md bg-surface-white border p-1.5"
								>
									<MenuItem v-slot="{ active }">
										<Button
											variant="ghost"
											class="w-full"
											@click="cancelEvaluation(evl)"
										>
											<template #prefix>
												<Ban
													:active="active"
													class="size-4 stroke-1.5"
													aria-hidden="true"
												/>
											</template>
											{{ __('Cancel') }}
										</Button>
									</MenuItem>
								</MenuItems>
							</transition>
						</Menu>
						<div class="min-w-0 flex-1">
							<div class="flex justify-between mb-3">
								<span class="text-base font-semibold text-ink-gray-9 leading-5">
									{{ evl.course_title }}
								</span>
							</div>
							<div
								class="w-full flex flex-col md:flex-row md:items-center gap-x-2 text-sm flex-wrap text-gray-600"
							>
								<div class="flex items-center mb-2">
									<Calendar2Icon class="w-4 h-4 stroke-1.5" />
									<span class="ml-2">
										{{ dayjs(evl.date).format('DD MMMM YYYY') }}
									</span>
								</div>
								<div class="flex items-center mb-2">
									<ClockIcon class="w-4 h-4 stroke-1.5" />
									<span class="ml-2">
										{{ formatTime(evl.start_time) }}
									</span>
								</div>
							</div>
							<div
								v-if="evl.google_meet_link"
								class="flex items-center space-x-2 group/link"
							>
								<div class="flex items-center">
									<Link2Icon class="w-4 h-4 stroke-1.5 text-gray-500" />
									<span
										class="text-gray-500 truncate max-w-[200px] md:max-w-xs"
									>
										{{ evl.google_meet_link }}
									</span>
								</div>

								<button
									@click.stop="copyToClipboard(evl.google_meet_link)"
									class="p-1 hover:bg-gray-100 rounded transition-colors text-primary-500"
									:title="__('Copy Link')"
								>
									<Copy class="size-3.5" />
								</button>
							</div>
						</div>
						<button
							@click="openEvalCall(evl)"
							class="ml-auto size-6 hover:bg-gray-100 rounded"
						>
							<ChevronRight class="text-gray-600 size-4" />
						</button>
					</div>
				</div>
			</div>
		</div>
		<div v-else class="flex flex-col items-center justify-center gap-y-2 mt-6">
			<EmptyIcon class="size-24 mb-6" />
			<h3 class="text-lg font-bold text-gray-900">Nothing to see here yet</h3>
			<p class="text-gray-500 text-ms font-medium">
				{{ __('Schedule an evaluation to get certified.') }}
			</p>
			<Button
				v-if="
					upcoming_evals.data?.length != evaluationCourses.length && !forHome
				"
				@click="openEvalModal"
				variant="solid"
			>
				{{ __('Schedule Evaluation') }}
			</Button>
		</div>
	</div>
	<EvaluationModal
		:batch="batch"
		:endDate="endDate"
		:courses="courses"
		v-model="showEvalModal"
		v-model:reloadEvals="upcoming_evals"
	/>
</template>
<script setup>
import {
	Ban,
	Calendar,
	Clock,
	GraduationCap,
	HeadsetIcon,
	EllipsisVertical,
	Link2Icon,
	Copy,
	ChevronRight,
} from 'lucide-vue-next'
import { inject, ref, getCurrentInstance, computed } from 'vue'
import { formatTime } from '@/utils'
import { createResource, call } from 'frappe-ui'
import EvaluationModal from '@/components/Modals/EvaluationModal.vue'
import { Menu, MenuButton, MenuItems, MenuItem } from '@headlessui/vue'
import Button from './ui/Button.vue'
import Calendar2Icon from './Icons/Calendar2Icon.vue'
import ClockIcon from './Icons/ClockIcon.vue'
import { toast } from 'frappe-ui'

const dayjs = inject('$dayjs')
const showEvalModal = ref(false)
const app = getCurrentInstance()
const { $dialog } = app.appContext.config.globalProperties

const props = defineProps({
	batch: {
		type: String,
		default: null,
	},
	courses: {
		type: Array,
		default: [],
	},
	endDate: {
		type: String,
		default: null,
	},
	forHome: {
		type: Boolean,
		default: false,
	},
})
const copyToClipboard = (text) => {
	navigator.clipboard.writeText(text).then(() => {
		toast.success(__('Link copied to clipboard'))
	})
}
const upcoming_evals = createResource({
	url: 'lms.lms.utils.get_upcoming_evals',
	params: {
		courses: props.courses.map((course) => course.course),
		batch: props.batch,
	},
	auto: true,
})

function openEvalModal() {
	showEvalModal.value = true
}

const openEvalCall = (evl) => {
	window.open(evl.google_meet_link, '_blank')
}

const evaluationCourses = computed(() => {
	return props.courses.filter((course) => {
		return course.evaluator != ''
	})
})

const cancelEvaluation = (evl) => {
	$dialog({
		title: __('Cancel this evaluation?'),
		message: __(
			'Are you sure you want to cancel this evaluation? This action cannot be undone.',
		),
		actions: [
			{
				label: __('Cancel'),
				theme: 'red',
				variant: 'solid',
				onClick(close) {
					call('lms.lms.api.cancel_evaluation', { evaluation: evl }).then(
						() => {
							upcoming_evals.reload()
						},
					)
					close()
				},
			},
		],
	})
}
</script>
