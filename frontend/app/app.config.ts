export default defineAppConfig({
  ui: {
    colors: {
      primary: 'cyan',
      secondary: 'violet',
      neutral: 'zinc'
    },
    chip: {
      slots: {
        root: 'relative inline-flex items-center justify-center shrink-0',
        base: 'rounded-full ring ring-bg flex items-center justify-center text-inverted font-medium whitespace-nowrap'
      },
      variants: {
        color: {
          myPink: 'bg-[#ECB7B0] text-gray-900'
        },
        position: {
          'my-bottom-left': 'bottom-[2px] left-[2px]'
        },
      }
    },
    button: {
      variants: {
        color: {
          myPink: 'bg-[#ECB7B0] hover:bg-[#ECB7B0]/80 text-gray-900' // Ваш цвет
        }
      }
    }
  }
})