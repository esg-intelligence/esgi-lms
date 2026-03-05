<template>
	<div class="mt-6">
		<div v-if="!singleThread" class="flex items-center mb-5">
			<Button variant="outline" @click="showTopics = true">
				<template #icon>
					<ChevronLeft class="w-5 h-5 stroke-1.5 text-ink-gray-7" />
				</template>
			</Button>
			<span class="text-lg font-semibold ml-2 text-ink-gray-9">
				{{ topic.title }}
			</span>
		</div>

		<div v-if="replies.data?.length" class="space-y-6 mb-8">
			<div
				v-for="reply in replies.data"
				:key="reply.name"
				class="pb-6 border-b last:border-b-0"
			>
				<div class="flex items-start gap-4">
					<UserAvatar :user="reply.user" size="2xl" class="flex-shrink-0" />
					<div class="flex-1 min-w-0">
						<div class="flex items-center justify-between mb-1">
							<div class="flex items-center gap-2">
								<span class="font-medium text-sm text-ink-gray-9">
									{{ reply.user.full_name }}
								</span>
								<span class="text-ink-gray-5 text-xs">•</span>
								<span class="text-xs text-ink-gray-5">
									{{ timeAgo(reply.creation) }}
								</span>
							</div>
							<div class="flex items-center">
								<Dropdown
									v-if="
										user.data.name == reply.owner &&
										!reply.editable &&
										!readOnlyMode
									"
									:options="[
										{
											label: __('Edit'),
											onClick() {
												reply.editable = true
											},
										},
										{
											label: __('Delete'),
											onClick() {
												deleteReply(reply)
											},
										},
									]"
								>
									<template v-slot="{ open }">
										<MoreHorizontal
											class="w-4 h-4 stroke-1.5 cursor-pointer text-ink-gray-5 hover:text-ink-gray-9 transition-colors"
										/>
									</template>
								</Dropdown>
								<div v-if="reply.editable" class="flex items-center gap-2">
									<Button
										variant="ghost"
										class="h-7 px-2 text-xs"
										@click="postEdited(reply)"
									>
										{{ __('Post') }}
									</Button>
									<Button
										variant="ghost"
										class="h-7 px-2 text-xs text-red-500 hover:bg-red-50"
										@click="reply.editable = false"
									>
										{{ __('Discard') }}
									</Button>
								</div>
							</div>
						</div>
						<TextEditor
							:content="reply.reply"
							@change="(val) => (reply.reply = val)"
							:editable="reply.editable || false"
							:bubbleMenu="reply.editable || false"
							:fixedMenu="false"
							editorClass="ProseMirror prose prose-sm max-w-none text-ink-gray-7 leading-relaxed"
						/>
					</div>
				</div>
			</div>
		</div>

		<div
			v-if="!readOnlyMode && renderEditor"
			class="flex flex-col sm:flex-row items-center gap-3"
		>
			<div
				class="flex-1 flex items-center w-full bg-white border border-gray-200 rounded-lg px-4 py-2 focus-within:border-primary-500 focus-within:ring-1 focus-within:ring-primary-100 transition-all"
			>
				<Message2Icon
					class="w-5 h-5 text-gray-400 mr-2 flex-shrink-0 stroke-1.5"
				/>
				<TextEditor
					:content="newReply"
					:mentions="mentionUsers"
					@change="(val) => (newReply = val)"
					:bubbleMenu="true"
					placeholder="Write a Thread"
					editorClass="ProseMirror pt-1 prose-sm max-w-none flex-1 outline-none min-h-[1.2rem]"
				/>
			</div>
			<Button
				@click="postReply()"
				variant="solid"
				size="lg"
				class="!bg-primary-500 ml-auto sm:w-auto px-6 rounded-lg whitespace-nowrap"
			>
				{{ __('Post Thread') }}
			</Button>
		</div>
	</div>
</template>
<script setup>
import { createResource, TextEditor, Dropdown, toast } from 'frappe-ui'
import { timeAgo } from '@/utils'
import UserAvatar from '@/components/UserAvatar.vue'
import { ChevronLeft, MoreHorizontal } from 'lucide-vue-next'
import { ref, inject, onMounted, onUnmounted } from 'vue'
import Button from './ui/Button.vue'
import Message2Icon from './Icons/Message2Icon.vue'

const showTopics = defineModel('showTopics')
const newReply = ref('')
const socket = inject('$socket')
const user = inject('$user')
const allUsers = inject('$allUsers')
const mentionUsers = ref([])
const renderEditor = ref(false)
const readOnlyMode = window.read_only_mode

const props = defineProps({
	topic: {
		type: Object,
		required: true,
	},
	singleThread: {
		type: Boolean,
		default: false,
	},
})

onMounted(() => {
	socket.on('publish_message', (data) => {
		replies.reload()
	})
	socket.on('update_message', (data) => {
		replies.reload()
	})
	socket.on('delete_message', (data) => {
		replies.reload()
	})
	fetchMentionUsers()
})

const replies = createResource({
	url: 'lms.lms.utils.get_discussion_replies',
	cache: ['replies', props.topic],
	makeParams(values) {
		return {
			topic: props.topic.name,
		}
	},
	auto: true,
})

const newReplyResource = createResource({
	url: 'frappe.client.insert',
	makeParams(values) {
		return {
			doc: {
				doctype: 'Discussion Reply',
				reply: newReply.value,
				topic: props.topic.name,
			},
		}
	},
})

const fetchMentionUsers = () => {
	if (user.data?.is_student) {
		renderEditor.value = true
	} else {
		allUsers.reload(
			{},
			{
				onSuccess(data) {
					mentionUsers.value = Object.values(data).map((user) => {
						return {
							value: user.name,
							label: user.full_name,
						}
					})
					renderEditor.value = true
				},
			},
		)
	}
}

const postReply = () => {
	newReplyResource.submit(
		{},
		{
			validate() {
				if (!newReply.value) {
					return 'Reply cannot be empty'
				}
			},
			onSuccess() {
				newReply.value = ''
				replies.reload()
			},
			onError(err) {
				toast.error(err.messages?.[0] || err)
			},
		},
	)
}

const editReplyResource = createResource({
	url: 'frappe.client.set_value',
	makeParams(values) {
		return {
			doctype: 'Discussion Reply',
			name: values.name,
			fieldname: 'reply',
			value: values.reply,
		}
	},
})

const postEdited = (reply) => {
	editReplyResource.submit(
		{
			name: reply.name,
			reply: reply.reply,
		},
		{
			validate() {
				if (!reply.reply) {
					return 'Reply cannot be empty'
				}
			},
			onSuccess() {
				reply.editable = false
				replies.reload()
			},
		},
	)
}

const deleteReplyResource = createResource({
	url: 'frappe.client.delete',
	makeParams(values) {
		return {
			doctype: 'Discussion Reply',
			name: values.name,
		}
	},
})

const deleteReply = (reply) => {
	deleteReplyResource.submit(
		{
			name: reply.name,
		},
		{
			onSuccess() {
				replies.reload()
			},
		},
	)
}

onUnmounted(() => {
	socket.off('publish_message')
	socket.off('update_message')
	socket.off('delete_message')
})
</script>
