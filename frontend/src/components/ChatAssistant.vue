<template>
	<div
		v-show="show"
		class="fixed bottom-6 right-6 z-50 flex flex-col items-end gap-4 pointer-events-none"
	>
		<transition
			enter-active-class="transition duration-300 ease-out"
			enter-from-class="opacity-0 translate-y-4 scale-95"
			enter-to-class="opacity-100 translate-y-0 scale-100"
			leave-active-class="transition duration-200 ease-in"
			leave-from-class="opacity-100 translate-y-0 scale-100"
			leave-to-class="opacity-0 translate-y-4 scale-95"
		>
			<div
				v-if="!minimize"
				class="pointer-events-auto w-[380px] h-[600px] max-h-[calc(100vh-120px)] flex flex-col bg-surface-white rounded-xl shadow-xl border border-gray-100 overflow-hidden"
				@click.stop
			>
				<div
					class="flex items-center justify-between px-4 py-3 border-b border-gray-100 bg-white"
				>
					<div class="flex items-center gap-2">
						<div class="text-base font-semibold text-gray-900">
							CESGS AI Assistant
						</div>
					</div>
					<div class="flex gap-1">
						<Button
							@click="minimize = true"
							theme="dark"
							variant="ghost"
							size="lg"
							class="!px-0"
						>
							<CircleX class="text-gray-500" />
						</Button>
					</div>
				</div>

				<div class="flex-1 overflow-hidden flex flex-col min-h-0 bg-gray-50/50">
					<div ref="chatAreaRef" class="flex-1 overflow-y-auto p-4 space-y-4">
						<template v-if="messages.length === 0">
							<div
								class="h-full flex flex-col items-center justify-center text-center p-6 text-gray-500"
							>
								<div
									class="h-12 w-12 rounded-full bg-gradient-right flex items-center justify-center mb-3"
								>
									<AIStarIcon class="h-6 w-6 text-white" />
								</div>
								<h3 class="font-medium text-gray-900 mb-1">
									What can i help for you??
								</h3>
								<p class="text-sm">
									Ask me anything about your course or lessons.
								</p>
							</div>
						</template>
						<AssistantMessage
							v-for="(msg, index) in messages"
							:key="index"
							:userMessage="msg.userMessage"
							:botResponse="msg.botResponse"
							:isLast="index === messages.length - 1"
							:isStreaming="(isSending || typewriterActive) && index === messages.length - 1"
							:sources="msg.sources"
						/>
					</div>

					<div class="p-3 bg-white border-t border-gray-100">
						<form
							@submit.prevent="sendMessage"
							class="flex justify-between gap-x-2"
						>
							<FormWrapper class="[&_input]:h-10 flex-1">
								<TextInput
									:type="'text'"
									size="md"
									variant="subtle"
									placeholder="Ask me anything"
									:disabled="isSending"
									v-model="messageText"
									class="w-full"
								/>
							</FormWrapper>
							<button
								@click="sendMessage"
								:disabled="isSending"
								class="rounded bg-gradient-left p-2 size-10 shadow-sm"
							>
								<SendHorizonalIcon class="h-4 text-white" />
							</button>
						</form>
					</div>
				</div>
			</div>
		</transition>
		<button
			@click="minimize = !minimize"
			class="pointer-events-auto group relative h-14 w-14 rounded-full bg-gradient-right text-white flex items-center justify-center shadow-lg hover:bg-gray-800 hover:scale-105 active:scale-95 transition-all duration-200"
		>
			<transition
				enter-active-class="transition duration-200 ease-out"
				enter-from-class="opacity-0 rotate-90 scale-50"
				enter-to-class="opacity-100 rotate-0 scale-100"
				leave-active-class="transition duration-200 ease-in"
				leave-from-class="opacity-100 rotate-0 scale-100"
				leave-to-class="opacity-0 -rotate-90 scale-50"
				mode="out-in"
			>
				<div v-if="minimize" class="relative">
					<p class="absolute text-sm -left-32 px-2 py-1 rounded-sm bg-gradient-left font-medium">AI Assistant</p>
					<AIStarIcon class="h-6 w-6" />
				</div>
				<ChevronDown v-else class="h-7 w-7" />
			</transition>
		</button>
	</div>
</template>

<script setup>
import { TextInput } from 'frappe-ui'
import { SendHorizonalIcon, ChevronDown, CircleX } from 'lucide-vue-next'
import { ref, watch, onUnmounted } from 'vue'
import MarkdownIt from 'markdown-it'
import AssistantMessage from './AssistantMessage.vue'
import chatSearching from '@/assets/images/search-loading.gif'
import AIStarIcon from './Icons/AIStarIcon.vue'
import FormWrapper from './ui/FormWrapper.vue'
import Button from './ui/Button.vue'

const props = defineProps({})
const show = defineModel()
const minimize = ref(true)
const messages = ref([])
const messageText = ref('')
const chatAreaRef = ref(null)
const isSending = ref(false)
const bsid = ref(null)
const bcid = ref(null)
const targetMarkdown = ref('')
const typewriterActive = ref(false)
let typewriterFrame = null
let charIndex = 0

const cancelTypewriter = () => {
	if (typewriterFrame !== null) {
		cancelAnimationFrame(typewriterFrame)
		typewriterFrame = null
	}
	typewriterActive.value = false
}

const tickTypewriter = () => {
	const target = targetMarkdown.value
	if (charIndex >= target.length) {
		typewriterFrame = null
		typewriterActive.value = false
		return
	}
	charIndex = Math.min(charIndex + 8, target.length)
	const html = `<div>${divWrapper(md.render(target.slice(0, charIndex)))}</div>`
	if (messages.value.length > 0) {
		messages.value[messages.value.length - 1].botResponse = html
	}
	typewriterFrame = requestAnimationFrame(tickTypewriter)
}

watch(targetMarkdown, () => {
	if (typewriterFrame === null && charIndex < targetMarkdown.value.length) {
		typewriterActive.value = true
		typewriterFrame = requestAnimationFrame(tickTypewriter)
	}
})

onUnmounted(cancelTypewriter)

const md = new MarkdownIt()
const divWrapper = (htmlContent) => {
	// Regular Expression for finding tables
	const tableRegex = /<table[\s\S]*?<\/table>/gi
	// Regular Expression for finding images
	const imgRegex = /<img[\s\S]*?>/gi
	// Regular Expression for finding links
	const linkRegex = /<a[\s\S]*?>[\s\S]*?<\/a>/gi
	// Replace <table> elements by wrapping them in a div
	let modifiedContent = htmlContent.replace(
		tableRegex,
		(match) => `<div class="table-wrapper">${match}</div>`,
	)
	// Replace <img> elements by wrapping them in a div with center styling
	modifiedContent = modifiedContent.replace(
		imgRegex,
		(match) => `
      <div class="flex justify-center my-4">
          ${match.replace('<img', '<img class="max-w-full h-auto max-h-96"')}
      </div>
  `,
	)
	// Replace <a> elements by adding an underline style with black color
	modifiedContent = modifiedContent.replace(linkRegex, (match) => {
		// Add inline style for black underline if not already styled
		return match.replace(
			'<a',
			'<a style="text-decoration: underline; text-decoration-color: gray;"',
		)
	})
	return modifiedContent
}

const sendMessage = async () => {
	const newMessage = messageText.value
	if (!newMessage) return
	messageText.value = ''
	isSending.value = true
	cancelTypewriter()
	targetMarkdown.value = ''
	charIndex = 0
	bsid.value = null
	bcid.value = null
	messages.value = [
		...messages.value,
		{ userMessage: newMessage, botResponse: '' },
	]
	const controller = new AbortController()
	const timeoutId = setTimeout(() => controller.abort(), 90_000)
	try {
		const response = await fetch('/api/method/lms.lms.api.chat_llm', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({
				message: newMessage,
				bsid: bsid.value,
			}),
			signal: controller.signal,
		})
		const reader = response.body?.getReader()
		if (!reader) throw new Error('Response body is null')
		const decoder = new TextDecoder()
		let lineBuffer = ''

		while (true) {
			const { done, value } = await reader.read()
			if (done) break

			lineBuffer += decoder.decode(value, { stream: true })

			const lines = lineBuffer.split('\n')
			lineBuffer = lines.pop() ?? ''

			for (const line of lines) {
				const trimmed = line.trim().replace(/^data:\s*/, '')
				if (!trimmed) continue

				let jsonResponse
				try {
					jsonResponse = JSON.parse(trimmed)
				} catch {
					continue
				}

				const {
					response: partialResponse,
					tools,
					bsid: newBsid,
					bcid: newBcid,
				} = jsonResponse

				if (tools && tools.length > 0) {
					const interimResult = tools[tools.length - 1]
					messages.value[messages.value.length - 1].botResponse =
						`<div class="text-sm font-bold flex items-center gap-x-2">
							<img src="${chatSearching}" class="h-6 w-6" />
							${md.render(interimResult)}
						</div>`
				}

				if (partialResponse) {
					targetMarkdown.value = partialResponse
				}

				if (newBsid) bsid.value = newBsid
				if (newBcid) bcid.value = newBcid
			}
		}
	} catch (error) {
		console.error('Error:', error)
		// Handle error, use a valid string for botResponse
		messages.value.pop()
		messages.value = [
			...messages.value,
			{
				userMessage: newMessage,
				botResponse:
					'<div class="alert-message"><p>An error occurred. Please try again.</p></div>',
			},
		]
	} finally {
		clearTimeout(timeoutId)
		isSending.value = false
	}
}

watch(messages, () => {
	if (chatAreaRef.value) {
		chatAreaRef.value.scrollTop = chatAreaRef.value.scrollHeight
	}
})

watch([bcid, bsid], ([newBcid, newBsid]) => {
	if (newBcid && newBsid) {
		// Make sure bsid and bcid are set
		try {
			const fetchSources = async () => {
				const response = await fetch(
					'/api/method/lms.lms.api.llm_get_sources',
					{
						method: 'POST',
						headers: {
							'Content-Type': 'application/json',
						},
						body: JSON.stringify({
							bsid: newBsid,
							bcid: newBcid,
						}),
					},
				)
				// if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
				const sources = await response.json()
				if (sources) {
					// Update the message with sources
					setTimeout(() => {
						// Defer the state update to the next event loop cycle
						const messagesLength = messages.value.length
						const lastMessage = messages.value[messagesLength - 1]
						const updatedMessage = {
							...lastMessage, // Copy the last message
							sources: sources.message, // Add or update sources field
						}
						messages.value.pop()
						messages.value = [...messages.value, updatedMessage]
					}, 0) // Set timeout of 0 to let the rendering phase complete
				}
			}
			fetchSources()
		} catch (e) {
			console.error('Error fetching sources:', e)
		}
	}
})
</script>
