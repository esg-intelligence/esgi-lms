import frappeUIPreset from 'frappe-ui/tailwind'
import animate from 'tailwindcss-animate'

export default {
    darkMode: ['class'],
    presets: [frappeUIPreset],
	content: [
		'./index.html',
		'./src/**/*.{vue,js,ts,jsx,tsx}',
		'./node_modules/frappe-ui/src/**/*.{vue,js,ts,jsx,tsx}',
		'../node_modules/frappe-ui/src/**/*.{vue,js,ts,jsx,tsx}',
		'./node_modules/frappe-ui/frappe/**/*.{vue,js,ts,jsx,tsx}',
		'../node_modules/frappe-ui/frappe/**/*.{vue,js,ts,jsx,tsx}',
	],
	theme: {
    	extend: {
    		fontFamily: {
    			sans: [
    				'Inter',
    				'sans-serif'
    			]
    		},
    		fontSize: {
    			xs: [
    				'0.75rem',
    				{
    					lineHeight: '1rem'
    				}
    			],
    			sm: [
    				'0.875rem',
    				{
    					lineHeight: '1.25rem'
    				}
    			],
    			base: [
    				'1rem',
    				{
    					lineHeight: '1.5rem'
    				}
    			],
    			lg: [
    				'1.125rem',
    				{
    					lineHeight: '1.75rem'
    				}
    			],
    			xl: [
    				'1.25rem',
    				{
    					lineHeight: '1.75rem'
    				}
    			],
    			'2xl': [
    				'1.5rem',
    				{
    					lineHeight: '2rem'
    				}
    			],
    			'3xl': [
    				'1.875rem',
    				{
    					lineHeight: '2.25rem'
    				}
    			],
    			'4xl': [
    				'2.25rem',
    				{
    					lineHeight: '2.5rem'
    				}
    			],
    			'5xl': [
    				'3rem',
    				{
    					lineHeight: '1'
    				}
    			],
    			'6xl': [
    				'3.75rem',
    				{
    					lineHeight: '1'
    				}
    			],
    			'7xl': [
    				'4.5rem',
    				{
    					lineHeight: '1'
    				}
    			],
    			'8xl': [
    				'6rem',
    				{
    					lineHeight: '1'
    				}
    			],
    			'9xl': [
    				'8rem',
    				{
    					lineHeight: '1'
    				}
    			]
    		},
    		colors: {
    			gray: {
    				'0': '#FFFFFF',
    				'50': '#F5F7FA',
    				'100': '#E9EAF0',
    				'200': '#CED1D9',
    				'300': '#B7BAC7',
    				'400': '#A1A5B3',
    				'500': '#8C94A3',
    				'600': '#6E7485',
    				'700': '#4E5566',
    				'800': '#363B47',
    				'900': '#1D2026'
    			},
    			primary: {
    				'0': '#ffffff',
    				'50': '#e6fdf8',
    				'100': '#C3EADD',
    				'200': '#A4DFCB',
    				'300': '#86D4BA',
    				'400': '#68CAA9',
    				'500': '#01C295',
    				'600': '#3E9F7F',
    				'700': '#317F65',
    				'800': '#255F4C',
    				'900': '#194033',
    				'950': '#001310',
    				DEFAULT: 'hsl(var(--primary))',
    				foreground: 'hsl(var(--primary-foreground))'
    			},
    			secondary: {
    				'0': '#ffffff',
    				'50': '#e8f3fb',
    				'100': '#B0C9E0',
    				'200': '#88ADD0',
    				'300': '#6192C1',
    				'400': '#3977B1',
    				'500': '#125CA2',
    				'600': '#0F4D87',
    				'700': '#0C3D6C',
    				'800': '#092E51',
    				'900': '#041220',
    				'950': '#020910',
    				DEFAULT: 'hsl(var(--secondary))',
    				foreground: 'hsl(var(--secondary-foreground))'
    			},
    			error: {
    				'0': '#ffffff',
    				'50': '#FFF0F0',
    				'100': '#FBD5D5',
    				'200': '#F4C8C8',
    				'300': '#EE8F8F',
    				'400': '#E96969',
    				'500': '#E34444',
    				'600': '#B63636',
    				'700': '#882929',
    				'800': '#5B1B1B',
    				'900': '#2D0E0E',
    				'950': '#170707'
    			},
    			warning: {
    				'0': '#ffffff',
    				'50': '#FFF2E5',
    				'100': '#ffebd1',
    				'200': '#FED1A5',
    				'300': '#FEBB79',
    				'400': '#FDA44C',
    				'500': '#FD8E1F',
    				'600': '#CC7319',
    				'700': '#985613',
    				'800': '#65390C',
    				'900': '#331D06',
    				'950': '#190e03'
    			},
    			success: {
    				'0': '#ffffff',
    				'50': '#E1F7E3',
    				'100': '#d3f3d9',
    				'200': '#C3E5C6',
    				'300': '#7BD785',
    				'400': '#4FCA5C',
    				'500': '#23BD33',
    				'600': '#1C9729',
    				'700': '#15711F',
    				'800': '#0E4C14',
    				'900': '#07260A',
    				'950': '#041305'
    			},
    			muted: {
    				'0': '#ffffff',
    				'50': '#f5f6f7',
    				'100': '#ebedef',
    				'200': '#d7dbdf',
    				'300': '#c3c9cf',
    				'400': '#afb7bf',
    				'500': '#A1A5B3',
    				'600': '#81848f',
    				'700': '#61636b',
    				'800': '#404247',
    				'900': '#202124',
    				'950': '#101012',
    				DEFAULT: 'hsl(var(--muted))',
    				foreground: 'hsl(var(--muted-foreground))'
    			},
    			disabled: {
    				'0': '#ffffff',
    				'50': '#fefefe',
    				'100': '#fdfdfd',
    				'200': '#fbfcfc',
    				'300': '#f9fafb',
    				'400': '#f7f8f9',
    				'500': '#F5F7FA',
    				'600': '#c4c6c8',
    				'700': '#939496',
    				'800': '#626364',
    				'900': '#313132',
    				'950': '#181819'
    			},
    			display: '#041220',
    			header: '#0E1113',
    			paragraph: '#6E7485',
    			background: 'hsl(var(--background))',
    			foreground: 'hsl(var(--foreground))',
    			card: {
    				DEFAULT: 'hsl(var(--card))',
    				foreground: 'hsl(var(--card-foreground))'
    			},
    			popover: {
    				DEFAULT: 'hsl(var(--popover))',
    				foreground: 'hsl(var(--popover-foreground))'
    			},
    			accent: {
    				DEFAULT: 'hsl(var(--accent))',
    				foreground: 'hsl(var(--accent-foreground))'
    			},
    			destructive: {
    				DEFAULT: 'hsl(var(--destructive))',
    				foreground: 'hsl(var(--destructive-foreground))'
    			},
    			border: 'hsl(var(--border))',
    			input: 'hsl(var(--input))',
    			ring: 'hsl(var(--ring))',
    			chart: {
    				'1': 'hsl(var(--chart-1))',
    				'2': 'hsl(var(--chart-2))',
    				'3': 'hsl(var(--chart-3))',
    				'4': 'hsl(var(--chart-4))',
    				'5': 'hsl(var(--chart-5))'
    			}
    		},
    		backgroundImage: {
    			'gradient-right': 'linear-gradient(to right, #01C295, #125CA2)',
    			'gradient-left': 'linear-gradient(to left, #01C295, #125CA2)'
    		},
    		textColor: {
    			display: '#041220',
    			header: '#0E1113',
    			paragraph: '#6E7485'
    		},
    		strokeWidth: {
    			'1.5': '1.5'
    		},
    		screens: {
    			'2xl': '1600px',
    			'3xl': '1920px'
    		},
    		borderRadius: {
    			lg: 'var(--radius)',
    			md: 'calc(var(--radius) - 2px)',
    			sm: 'calc(var(--radius) - 4px)'
    		}
    	}
    },
	plugins: [animate],
}
