<template>
	<div
		class="min-h-screen bg-sky-50 font-sans text-gray-900 pb-20 overflow-x-hidden"
	>
		<section class="max-w-full mx-auto relative">
			<div
				class="relative bg-white rounded-b-[3rem] shadow-2xl shadow-primary-900/5 min-h-screen flex flex-col overflow-visible"
			>
				<div
					class="relative z-20 px-12 lg:px-20 pt-8 flex items-center justify-between"
				>
					<div class="flex items-center gap-8">
						<div class="flex items-center gap-3">
							<UnairLogo class="h-10 w-auto" />
							<div class="h-8 w-[1px] bg-gray-200"></div>
							<LMSLogoFull class="h-10 w-auto" />
						</div>
						<nav class="hidden lg:flex items-center gap-6">
							<router-link
								v-for="link in simplifiedNav"
								:key="link.label"
								:to="{ name: link.to }"
								class="text-sm font-bold text-gray-700 hover:text-primary-600 transition-colors"
							>
								{{ link.label }}
							</router-link>
						</nav>
					</div>
					<div class="flex items-center gap-4">
						<UserDropdown v-if="user.data?.name" />
						<template v-else>
							<a
								href="/login"
								class="hidden sm:inline-flex items-center justify-center px-4 h-10 text-sm font-semibold text-primary-600 hover:bg-primary-50 rounded-lg transition-colors"
							>
								Sign In
							</a>
							<a
								href="/login#signup"
								class="inline-flex items-center justify-center px-8 h-10 text-sm font-semibold text-white bg-primary-500 hover:bg-primary-600 rounded-full transition-colors shadow-sm"
							>
								Register
							</a>
						</template>
					</div>
				</div>

				<div
					class="absolute inset-0 pointer-events-none overflow-hidden rounded-[3rem]"
				>
					<div class="absolute top-0 left-0 w-full h-full opacity-30">
						<div
							class="absolute top-[-10%] left-[-10%] w-[60%] h-[120%] bg-primary-50 rotate-[35deg] transform origin-top"
						></div>
						<div
							class="absolute top-[20%] left-[-20%] w-[40%] h-[120%] bg-secondary-50 rotate-[35deg] transform origin-top"
						></div>
						<div
							class="absolute top-[-30%] left-[20%] w-[15%] h-[150%] bg-primary-100/50 rotate-[35deg] transform origin-top"
						></div>
					</div>
				</div>

				<div class="relative flex-1 flex flex-col overflow-visible">
					<div
						class="relative w-full mx-auto flex flex-col md:flex-row items-start md:items-center px-12 lg:px-20 py-12 gap-12"
					>
						<div class="w-full md:w-[60%] flex flex-col space-y-40">
							<div class="relative overflow-hidden w-full">
								<div
									class="flex w-full transition-transform duration-700 ease-in-out"
									:style="{ transform: `translateX(-${currentSlide * 100}%)` }"
								>
									<div
										v-for="(slide, index) in heroSlides"
										:key="index"
										class="w-full flex-shrink-0 flex flex-col justify-center"
									>
										<div
											class="space-y-6 text-center md:text-left px-4 md:px-0"
										>
											<h1
												class="text-4xl lg:text-5xl font-bold text-gray-900 leading-[1.1] tracking-tight"
											>
												<template v-if="slide.highlight">
													{{ slide.title.split(slide.highlight)[0] }}
													<span class="text-primary-500">{{
														slide.highlight
													}}</span>
													{{ slide.title.split(slide.highlight)[1] }}
												</template>
												<template v-else>{{ slide.title }}</template>
											</h1>
											<p
												class="text-xl text-gray-600 font-medium leading-relaxed max-w-xl mx-auto md:mx-0"
											>
												{{ slide.subtitle }}
											</p>
											<div
												v-if="slide.content === 'image'"
												class="relative w-full max-w-xs !mt-16 animate-float mx-auto md:mx-0"
											>
												<img
													:src="slide.imageSrc"
													:alt="slide.title"
													class="w-full h-auto drop-shadow-xl opacity-80"
												/>
											</div>
										</div>
									</div>
								</div>

								<div
									class="flex items-center justify-center md:justify-start gap-x-3 mt-12"
								>
									<button
										v-for="i in heroSlides.length"
										:key="i - 1"
										@click="setSlide(i - 1)"
										class="cursor-pointer transition-all duration-300 rounded-full"
										:class="
											currentSlide === i - 1
												? 'w-10 h-2 bg-primary-500'
												: 'w-3 h-2 bg-gray-200 hover:bg-gray-300'
										"
									></button>
								</div>
							</div>
						</div>
						<div class="relative w-full md:w-[40%] flex justify-center z-10">
							<div
								class="w-full rounded-[30px] max-w-2xl animate-float"
								style="
									box-shadow:
										0 0 #0000004d,
										0 9px 20px #0000004a,
										0 37px 37px #00000042,
										0 84px 50px #00000026,
										0 149px 60px #0000000a,
										0 233px 65px #00000003;
								"
							>
								<div
									class="h-[35rem] md:h-[45rem] w-full border-4 border-[#6C6C6C] p-2 md:p-6 bg-[#222222] rounded-[30px] shadow-2xl flex flex-col overflow-visible"
								>
									<div
										class="h-full w-full overflow-hidden bg-gray-50 rounded-2xl relative flex flex-col"
									>
										<header
											class="sticky top-0 z-20 bg-white/90 backdrop-blur-md px-4 py-3 border-b border-gray-100 flex items-center justify-between"
										>
											<div class="flex items-center gap-3">
												<UnairLogo class="h-5 w-auto" />
												<div class="h-4 w-[1px] bg-gray-200"></div>
												<LMSLogoFull class="h-6 w-auto" />
											</div>
											<div class="flex items-center gap-3">
												<div class="relative">
													<Bell class="size-5 text-gray-500" />
													<div
														class="absolute -top-1 -right-1 size-2.5 bg-red-500 rounded-full border-2 border-white"
													></div>
												</div>
												<Menu class="size-5 text-gray-500" />
											</div>
										</header>

										<div class="flex-1 pb-20">
											<div
												class="px-4 py-3 flex items-center gap-2 overflow-x-auto hide-scrollbar whitespace-nowrap"
											>
												<span class="text-[10px] text-gray-400">Course</span>
												<ChevronRight class="size-2 text-gray-300" />
												<span
													class="text-[10px] text-gray-500 font-medium truncate"
													>1. Introduction to CESGS LMS</span
												>
											</div>

											<div class="px-4 mb-6">
												<div
													class="relative aspect-[16/10] bg-gray-200 rounded-2xl overflow-hidden shadow-sm"
												>
													<iframe
														src="https://drive.google.com/file/d/1RQh6ueGWBlxQfPkAxicWa82UFmLt1bNE/preview"
														width="100%"
														height="100%"
														allow="autoplay"
														allowfullscreen
													></iframe>
													<div
														class="absolute top-4 left-4 bg-[#36BFA6] text-white text-[10px] font-bold px-3 py-1 rounded-full shadow-lg"
													>
														Certification
													</div>
												</div>
											</div>

											<div class="px-4 space-y-4 text-left">
												<h2
													class="text-lg font-extrabold text-gray-900 leading-tight"
												>
													1. Introduction to CESGS LMS
												</h2>
												<div class="flex flex-col gap-x-6 gap-y-1">
													<div class="flex items-center gap-2">
														<BookIcon class="size-4" />
														<div class="text-left">
															<span class="text-[11px] font-bold text-gray-700">
																16
															</span>
															<span class="text-[9px] text-gray-400">
																Lessons
															</span>
														</div>
													</div>
													<div class="flex items-center gap-2">
														<PeopleIcon class="size-4" />
														<div class="text-left">
															<span class="text-[11px] font-bold text-gray-700">
																200
															</span>
															<span class="text-[9px] text-gray-400"
																>Enrolled Students</span
															>
														</div>
													</div>
													<div class="flex items-center gap-2">
														<Star class="size-4 text-orange-500 fill-current" />
														<div class="text-left">
															<span class="text-[11px] font-bold text-gray-700">
																5.0
															</span>
															<span class="text-[9px] text-gray-400"
																>Rating</span
															>
														</div>
													</div>
												</div>
												<div class="pt-4 space-y-2">
													<div
														class="flex justify-between items-center text-[10px] font-bold"
													>
														<span class="text-gray-500">Course progress</span>
														<span class="text-[#36BFA6]">50%</span>
													</div>
													<div
														class="h-2 bg-gray-100 rounded-full overflow-hidden"
													>
														<div
															class="h-full w-1/2 bg-[#36BFA6] rounded-full"
														></div>
													</div>
												</div>
												<div class="pt-4 grid grid-cols-1 gap-3">
													<div
														class="h-12 bg-[#36BFA6] text-white rounded-xl flex items-center justify-center font-bold text-sm shadow-lg"
													>
														Continue Learning
													</div>
												</div>
											</div>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</section>

		<section class="flex flex-col items-center max-w-7xl mx-auto px-4 py-24">
			<div class="flex flex-col items-center text-center space-y-4 mb-16">
				<h2 class="text-2xl font-bold text-gray-800">What is ESG</h2>
				<span class="block w-4/5 mt-4">ESG stands for Environmental, Social, and Governance, a framework used to evaluate how organizations operate responsibly, sustainably, and ethically.</span>
			</div>
			<div class="grid grid-cols-1 lg:grid-cols-3 gap-6 w-full md:w-3/4 px-16 md:px-0">
				<div class="flex flex-col gap-y-2 items-center justify-stretch p-6 rounded shadow-md text-center">
					<Leaf class="h-12 w-12 text-primary-500 mb-3"/>
					<h3 class="font-bold">Environmental</h3>
					<p>Focuses on how a company protects the planet. Includes carbon emissions, renewable energy, waste management, and resource efficiency.</p>
				</div>
				<div class="flex flex-col gap-y-2 items-center justify-stretch p-6 rounded shadow-md text-center">
					<Users class="h-12 w-12 text-primary-500 mb-3"/>
					<h3 class="font-bold">Social</h3>
					<p>Measures how a company treats people and communities. Includes employee wellbeing, diversity & inclusion, human rights, and social impact.</p>
				</div>
				<div class="flex flex-col gap-y-2 items-center justify-stretch p-6 rounded shadow-md text-center">
					<Landmark  class="h-12 w-12 text-primary-500 mb-3"/>
					<h3 class="font-bold">Governance</h3>
					<p>Evaluates how a company is managed and governed. Includes transparency, anti-corruption, leadership structure, and regulatory compliance.</p>
				</div>
			</div>
		</section>

		<section class="flex flex-col items-center max-w-7xl mx-auto px-4 py-24 border-t border-gray-100">
			<div class="text-center space-y-4 mb-16">
				<h2 class="text-2xl font-bold text-gray-800">Why Learn With CESGS</h2>
			</div>
			<div class="grid grid-cols-2 gap-6 w-full md:w-3/4">
				<div class="flex flex-col gap-y-2 items-center justify-stretch p-6 rounded shadow-md text-center">
					<Route class="h-8 w-8 text-primary-500 mb-3"/>
					<h3 class="font-bold">Structured Learning Paths</h3>
					<p>Follow clear step-by-step courses designed for beginners to professionals.</p>
				</div>
				<div class="flex flex-col gap-y-2 items-center justify-stretch p-6 rounded shadow-md text-center">
					<BookOpenText class="h-8 w-8 text-primary-500 mb-3"/>
					<h3 class="font-bold">Practical ESG Knowledge</h3>
					<p>Learn real-world concepts, case studies, and industry-relevant insights.</p>
				</div>
				<div class="flex flex-col gap-y-2 items-center justify-stretch p-6 rounded shadow-md text-center">
					<Presentation  class="h-8 w-8 text-primary-500 mb-3"/>
					<h3 class="font-bold">Interactive Learning Experience</h3>
					<p>Pretests, materials, case analysis, and quizzes keep you engaged.</p>
				</div>
				<div class="flex flex-col gap-y-2 items-center justify-stretch p-6 rounded shadow-md text-center">
					<GraduationCap class="h-8 w-8 text-primary-500 mb-3"/>
					<h3 class="font-bold">Recognized Certification</h3>
					<p>Earn certificates to showcase your ESG skills and knowledge.</p>
				</div>
			</div>
		</section>

		<section class="flex flex-col items-center max-w-7xl mx-auto px-4 py-24 border-t border-gray-100">
			<div class="text-center space-y-4 mb-16">
				<h2 class="text-2xl font-bold text-gray-800">How it Works</h2>
			</div>
			<div class="p-6">
				<div v-for="(step, index) in steps" :key="index" class="relative pb-8 last:pb-0">
					<div v-if="index !== steps.length - 1" class="absolute left-[15px] top-8 h-full w-0.5 bg-primary-300"></div>
					<div class="flex items-start gap-4">
						<div class="relative z-10 flex h-8 w-8 shrink-0 items-center justify-center rounded-full border-2 bg-primary-500 border-primary-500 text-white">
							<span class="text-xs">{{ index + 1 }}</span>
						</div>
						<div class="pt-1">
							<p class="text-base font-semibold text-gray-900">
								{{ step.title }}
							</p>
							<p class="text-sm text-gray-800 mt-1">{{ step.description }}</p>
						</div>
					</div>
				</div>
			</div>
		</section>

		<section id="courses" class="max-w-7xl mx-auto px-4 py-24 border-t border-gray-100">
			<div class="text-center space-y-4 mb-16">
				<h2 class="text-2xl font-bold text-gray-800">Explore Courses</h2>
				<p class="text-gray-500 font-medium text-lg">
					Explore our comprehensive curriculum crafted to equip you with in-demand skills, real-world insights, and the confidence you need to grow, innovate, and succeed in your professional journey.
				</p>
			</div>

			<div class="flex flex-wrap justify-center gap-3 mb-12">
				<button
					v-for="cat in categories"
					:key="cat"
					:class="[
						'px-6 py-3 rounded-xl font-semibold transition-all border-2 whitespace-nowrap',
						activeCategory === cat
							? 'bg-primary-600 border-primary-600 text-white shadow-lg'
							: 'bg-white border-primary-50 text-primary-700 hover:border-primary-200',
					]"
					@click="activeCategory = cat"
				>
					{{ cat }}
				</button>
			</div>

			<div
				v-if="courses.data?.length"
				class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
			>
				<router-link
					v-for="course in courses.data"
					:key="course.name"
					:to="{ name: 'CourseDetail', params: { courseName: course.name } }"
				>
					<CourseCard
						:course="course"
						class="[&_.avatar-group.overlap]:hidden"
					/>
				</router-link>
			</div>
			<div v-else-if="courses.list.loading" class="flex justify-center p-12">
				<div
					class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"
				></div>
			</div>
			<div
				v-else
				class="flex flex-col items-center justify-center py-20 text-center"
			>
				<EmptyIcon class="size-32 mb-6" />
				<h3 class="text-xl font-bold text-gray-900 mb-2">
					Nothing to see here yet
				</h3>
				<p class="text-gray-500 font-medium">
					Your learning updates will show up here soon
				</p>
			</div>

			<div
				v-if="courses.data?.length"
				class="flex items-center justify-center gap-4 mt-16"
			>
				<Button variant="outline" @click="router.push({ name: 'Courses' })"
					>View All Courses</Button
				>
			</div>
		</section>

		<section
			id="batches"
			class="max-w-7xl mx-auto px-4 py-24 border-t border-gray-100"
		>
			<div class="text-center space-y-4 mb-16">
				<h2 class="text-2xl font-bold text-gray-800">Upcoming Batches</h2>
				<p class="text-gray-500 font-medium text-lg max-w-2xl mx-auto">
					Join our upcoming learning cohorts and grow alongside experts and peers in a guided, structured program designed for real progress.
				</p>
				<Button
					v-if="batches.data?.length"
					variant="outline"
					@click="router.push({ name: 'Batches' })"
				>
					View All Batches
				</Button>
			</div>

			<div
				v-if="batches.data?.length"
				class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
			>
				<router-link
					v-for="batch in batches.data"
					:key="batch.name"
					:to="{ name: 'BatchDetail', params: { batchName: batch.name } }"
				>
					<BatchCard :batch="batch" />
				</router-link>
			</div>
			<div v-else-if="batches.list.loading" class="flex justify-center p-12">
				<div
					class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"
				></div>
			</div>
			<div
				v-else
				class="flex flex-col items-center justify-center py-20 text-center bg-white rounded-3xl"
			>
				<EmptyIcon class="size-32 mb-6" />
				<h3 class="text-xl font-bold text-gray-900 mb-2">
					Nothing to see here yet
				</h3>
				<p class="text-gray-500 font-medium">
					Your learning updates will show up here soon
				</p>
			</div>
		</section>

		<section class="max-w-7xl mx-auto px-4 pt-24 pb-16 border-t border-gray-100">
			<div class="text-center space-y-4 mb-16 flex flex-col items-center">
				<h2 class="text-2xl font-bold text-gray-800">Start Your ESG Learning Journey Today</h2>
				<p class="text-gray-500 font-medium text-lg">
					Build practical ESG skills with structured courses, real insights, and recognized certification.
				</p>
				<Button variant="solid" @click="router.push({ name: 'Courses' })">Start Learning</Button>
			</div>
		</section>
	</div>
</template>

<script setup>
import { computed, inject, ref, watch, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePageMeta, createListResource } from 'frappe-ui'
import Button from '@/components/ui/Button.vue'
import {
	Search,
	Users,
	Star,
	ArrowLeft,
	ArrowRight,
	Bell,
	Menu,
	BookOpen,
	ChevronLeft,
	ChevronRight,
	Route,
	BookOpenText,
	Presentation,
	GraduationCap,
	Leaf,
	Landmark,
} from 'lucide-vue-next'
import { sessionStore } from '@/stores/session'
import UnairLogo from '@/components/Icons/UnairLogo.vue'
import LMSLogoFull from '@/components/Icons/LMSLogoFull.vue'
import CourseCard from '@/components/CourseCard.vue'
import BatchCard from '@/components/BatchCard.vue'
import EmptyIcon from '@/components/Icons/EmptyIcon.vue'
import PeopleIcon from '@/components/Icons/PeopleIcon.vue'
import UserDropdown from '@/components/UserDropdown.vue'

const user = inject('$user')
const dayjs = inject('$dayjs')
const router = useRouter()
const { brand } = sessionStore()

const batches = createListResource({
	doctype: 'LMS Batch',
	url: 'lms.lms.utils.get_batches',
	cache: ['home batches', user.data?.name],
	pageLength: 4,
	auto: true,
	filters: {
		published: 1,
		start_date: ['>=', dayjs().format('YYYY-MM-DD')],
	},
	orderBy: 'start_date',
})

const courses = createListResource({
	doctype: 'LMS Course',
	url: 'lms.lms.utils.get_courses',
	cache: ['home_courses', user.data?.name],
	pageLength: 4,
	auto: true,
	filters: {
		published: 1,
		upcoming: 0,
		live: 1,
	},
})

const categoryResource = createListResource({
	doctype: 'LMS Category',
	fields: ['name', 'category'],
	auto: true,
})

const activeCategory = ref('All Courses')

watch(activeCategory, (newCat) => {
	const filters = {
		published: 1,
		upcoming: 0,
		live: 1,
	}
	if (newCat !== 'All Courses') {
		filters.category = newCat
	}
	courses.update({ filters })
	courses.reload()
})

const categories = computed(() => {
	const cats = ['All Courses']
	if (categoryResource.data) {
		categoryResource.data.forEach((cat) => {
			cats.push(cat.category)
		})
	}
	return cats
})

const simplifiedNav = [
	{ label: 'Courses', to: 'Courses' },
	{ label: 'Batches', to: 'Batches' },
]

/* Slider state for Hero section */
const currentSlide = ref(0)
const heroSlides = [
	{
		title: 'CESGS Learning Management System',
		subtitle:
			'Empowering structured learning in one integrated platform. Brought to you by Center for Environmental, Social, and Governance Studies (CESGS) Universitas Airlangga: the first Center of Excellence for Sustainable Business (PUI PT Bisnis Berkelanjutan) and #1 ESG Research Center in Indonesia.',
		content: 'text',
		highlight: 'CESGS',
		layout: 'centered',
	},
	{
		title: 'Sharpen Your Skills with Structured Learning',
		subtitle:
			'Enhance your capabilities through guided lessons, real-world case studies, and focused learning paths designed to build practical ESG expertise.',
		content: 'image',
		imageSrc: '/assets/lms/images/undraw_working-together_r43a.png',
		highlight: 'skills',
	},
	{
		title: 'Learn Efficiently With AI Assistance',
		subtitle:
			'Receive instant explanations, smart recommendations, and learning support that helps you understand complex topics faster and more efficiently.',
		content: 'image',
		imageSrc: '/assets/lms/images/undraw_online-stats_d57c 1.png',
		highlight: 'AI',
	},
	{
		title: 'Learn without limit',
		subtitle: 'Access your courses anytime, anywhere, and progress at your own pace in a flexible environment built for modern learners.',
		content: 'image',
		imageSrc: '/assets/lms/images/undraw_happy-announcement_23nf 1.png',
		highlight: 'limit',
	},
]

const totalSlidesCount = heroSlides.length
const autoPlayTimer = ref(null)

const nextSlide = () => {
	currentSlide.value = (currentSlide.value + 1) % totalSlidesCount
}

const previousSlide = () => {
	currentSlide.value =
		(currentSlide.value - 1 + totalSlidesCount) % totalSlidesCount
}

const setSlide = (index) => {
	currentSlide.value = index
}

onMounted(() => {
	autoPlayTimer.value = setInterval(nextSlide, 8000)
})

onUnmounted(() => {
	if (autoPlayTimer.value) clearInterval(autoPlayTimer.value)
})

const testimonials = [
	{
		quote: 'Successfully hired as QA Tester after studying at CESGS LMS!',
		name: 'Taufik Rafli Margacahya',
		role: 'Quality Assurance Tester at BNI',
		image: null,
	},
	{
		quote: 'Got my dream job in HRD, thanks to the curriculum at CESGS LMS!',
		name: 'Latifah NH Putri',
		role: 'HR Generalist at TIX ID',
		image: null,
	},
	{
		quote: 'Secured 12 internship offers within 3 weeks of joining CESGS LMS!',
		name: 'Muhammad Rizqullah',
		role: 'Performance Marketing Intern at Jakmall.com',
		image: null,
	},
]

const steps = [
  { title: 'Create Your Account', description: 'Register or log in to access your learning dashboard.' },
  { title: 'Choose a Course', description: 'Choose ESG topics and pick a course.' },
  { title: 'Start Learning', description: 'Begin with a pre-test, explore reading materials, review slides, and analyze real case studies.' },
  { title: 'Complete the Quiz', description: 'Test your understanding and reinforce key concepts.' },
  { title: 'Get Certified', description: 'Receive your certificate after successfully completing the course.' },
]

usePageMeta(() => {
	return {
		title: 'E-Learning',
		icon: brand.favicon,
	}
})
</script>

<style scoped>
@keyframes float {
	0%,
	100% {
		transform: translateY(0);
	}
	50% {
		transform: translateY(-20px);
	}
}
.animate-float {
	animation: float 5s ease-in-out infinite;
}
</style>
